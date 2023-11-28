import math
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from itertools import tee
from typing import Callable, overload

import sqlalchemy as sa
from loguru import logger
from more_itertools import peekable

from bupap import db
from bupap.ui.viewmodel.task import NewEstimate, NewTask, TaskDone
from bupap.ui.viewmodel.work import WorkPeriodEnd

from .common import get_from_id, return_obj_or_id, set_task_state
from .work import end_work_period


@overload
def create_task(project: NewTask, external_session: None) -> int:
    ...


@overload
def create_task(project: NewTask, external_session: db.Session) -> db.Task:
    ...


def create_task(task: NewTask, external_session: db.Session | None = None):
    if not task.name:
        raise RuntimeError("Incomplete data to create a project.")
    with db.use_or_open_session(external_session) as session:
        session.flush()
        db_project = get_from_id(session, db.Project, task.project_id)
        db_parent = None
        if task.parent_id is not None:
            db_parent = get_from_id(session, db.Task, task.parent_id)
            if db_parent.project != db_project:
                raise RuntimeError(
                    f"Cannot create subtask in project {db_project.name} for parent task {db_parent.id} from project {db_parent.project.name}"
                )
        db_task = db.Task(
            name=task.name,
            description=task.description,
            project=db_project,
            parent=db_parent,
            automatic_schedule=True,
            task_state=None,  # Note: fixed before added to session
            task_type=task.task_type,
            task_priority=task.priority,
            created_at=task.created_at,
            order_id=None,  # Note: fixed before added to session
        )

        def _recursive_children(task: NewTask, db_task: db.Task):
            for ctask in task.children:
                db_child_task = db.Task(
                    name=ctask.name,
                    description=ctask.description,
                    project=db_project,
                    parent=db_task,
                    automatic_schedule=True,
                    task_state=None,  # Note: fixed before added to session
                    task_type=ctask.task_type,
                    task_priority=ctask.priority,
                    created_at=ctask.created_at,
                    order_id=None,  # Note: fixed before added to session
                    attached=True,  # Otherwise it will only be set on flush
                )
                _recursive_children(ctask, db_child_task)

        _recursive_children(task, db_task)
        set_task_state(db_task, db.TaskState.REQUEST, session=session)
        session.add(db_task)
        return return_obj_or_id(external_session, session, db_task, always_flush=True)


def estimate_task(estimate: NewEstimate, external_session: db.Session | None = None):
    with db.use_or_open_session(external_session) as session:
        db_task = get_from_id(session, db.Task, estimate.task_id)
        db_user = get_from_id(session, db.User, estimate.user_id)
        db_estimate_type = get_from_id(session, db.EstimateType, estimate.estimate_type_id)
        # TODO: calc expectation
        db_statistics = [
            es for es in db_user.estimate_statistics if es.estimate_type_id == db_estimate_type.id
        ]
        if db_statistics:
            shifts = [
                db_statistics[0].shift_pessimistic,
                db_statistics[0].shift_average,
                db_statistics[0].shift_optimistic,
            ]
        else:
            shifts = [
                db_estimate_type.default_shift_pessimistic,
                db_estimate_type.default_shift_average,
                db_estimate_type.default_shift_optimistic,
            ]
        if db_estimate_type.relative:
            expected = [estimate.duration * s for s in shifts]
        else:
            expected = [estimate.duration + timedelta(seconds=s) for s in shifts]
        db_estimate = db.Estimate(
            task=db_task,
            user=db_user,
            estimate_type=db_estimate_type,
            created_at=estimate.created_at,
            estimated_duration=estimate.duration,
            expectation_pessimistic=expected[0],
            expectation_average=expected[1],
            expectation_optimistic=expected[2],
        )
        # TODO: remove existing estimate for same task / user combination
        # TODO: set 'active' estimate for multiple estimates (gut feeling vs. throught through)

        session.add(db_estimate)


def _recursive_attached(db_task, cb: Callable[[db.Task], None]):
    cb(db_task)
    for db_child in db_task.children:
        if db_child.attached:
            _recursive_attached(db_child, cb)


def task_done(task: TaskDone, external_session: db.Session | None = None):
    with db.use_or_open_session(external_session) as session:
        db_task = get_from_id(session, db.Task, task.task_id)

        db_open_work_period = db_task.open_work_period
        if db_open_work_period is not None:
            end_work_period(
                WorkPeriodEnd(db_open_work_period.id, task.finished_at), external_session=session
            )

        set_task_state(db_task, db.TaskState.DONE)

        def set_finished(t):
            t.finished_at = task.finished_at

        _recursive_attached(db_task, set_finished)
        session.flush()


@overload
def get_next_tasks(user_id: int, num_tasks: int, external_session: None) -> list[int]:
    ...


@overload
def get_next_tasks(user_id: int, num_tasks: int, external_session: db.Session) -> list[db.Task]:
    ...


def get_next_tasks(user_id: int, num_tasks: int, external_session: db.Session | None = None):
    with db.use_or_open_session(external_session) as session:
        db_tasks = session.scalars(
            sa.Select(db.Task)
            .where(db.Task.scheduled_assignee_id == user_id)
            .where(db.Task.task_state.in_([db.TaskState.PLANNING, db.TaskState.SCHEDULED]))
            .order_by(db.Task.order_id)
            .limit(num_tasks)
        ).all()
        if external_session is None:
            return [t.id for t in db_tasks]
        return db_tasks


def _actual_work_for_estimate(db_estimate: db.Estimate) -> timedelta:
    return sum(
        [wp.duration for wp in db_estimate.task.work_periods if wp.duration is not None],
        start=timedelta(),
    )


def _estimate_to_value(db_estimate: db.Estimate, relative: bool) -> float:
    actual_work = _actual_work_for_estimate(db_estimate)
    estimated_work = db_estimate.estimated_duration
    if relative:
        return actual_work / estimated_work
    else:
        return (actual_work - estimated_work).total_seconds()


def get_estimate_data(
    session: db.Session, user_id, estimate_type_id, before: datetime | None = None
) -> list[db.Estimate]:
    db_estimate_type = session.get(db.EstimateType, estimate_type_id)
    query = (
        sa.select(db.Estimate)
        .join(db.Estimate.task)
        .join(db.Task.work_periods)
        .where(db.Estimate.estimate_type_id == estimate_type_id)
        .where(db.Estimate.user_id == user_id)
        .where(db.Task.task_state == db.TaskState.DONE)
        .where(user_id == db.WorkPeriod.user_id)
        .group_by(db.Estimate.id)
    )
    if before is not None:
        query = query.where(db.Task.finished_at < before)
    query = query.order_by(sa.desc(db.Task.finished_at)).limit(db_estimate_type.max_datapoints)
    return session.scalars(query).all()


@dataclass
class EstimateDatapoint:
    value: float
    task_id: int
    task_name: str
    estimate: timedelta
    actual_work: timedelta
    num_work_periods: int
    start: datetime
    end: datetime


@dataclass
class EstimateStatistics:
    user_id: int
    user_name: str
    estimate_type_id: int
    estimate_type_name: str
    relative: bool
    sufficient: bool
    data: list[EstimateDatapoint]


def get_estimate_statistics(
    user_id,
    estimate_type_id,
    before: datetime | None = None,
    external_session: db.Session | None = None,
) -> EstimateStatistics | None:
    with db.use_or_open_session(external_session) as session:
        db_estimate_type = session.get(db.EstimateType, estimate_type_id)
        db_user = session.get(db.User, user_id)
        db_estimates = get_estimate_data(session, user_id, estimate_type_id, before)
        if not db_estimates:
            return None
        data = []
        for db_estimate in db_estimates:
            db_work_periods = [
                wp
                for wp in db_estimate.task.work_periods
                if wp.duration is not None and wp.user_id == user_id
            ]
            actual_work = sum([wp.duration for wp in db_work_periods], start=timedelta())
            value = (
                actual_work / db_estimate.estimated_duration
                if db_estimate_type.relative
                else (actual_work - db_estimate.estimated_duration).total_seconds()
            )
            data.append(
                EstimateDatapoint(
                    actual_work=actual_work,
                    estimate=db_estimate.estimated_duration,
                    value=value,
                    task_id=db_estimate.task_id,
                    task_name=db_estimate.task.name,
                    num_work_periods=len(db_work_periods),
                    start=min(wp.started_at for wp in db_work_periods),
                    end=max(wp.ended_at for wp in db_work_periods),
                )
            )
        return EstimateStatistics(
            db_user.id,
            db_user.name,
            db_estimate_type.id,
            db_estimate_type.name,
            db_estimate_type.relative,
            len(data) > db_estimate_type.min_datapoints,
            data,
        )


def update_statistics(now: datetime | None = None, external_session: db.Session | None = None):
    if now is None:
        now = datetime.utcnow()
    with db.use_or_open_session(external_session) as session:
        for db_user in session.scalars(sa.Select(db.User)):
            for db_estimate_type in session.scalars(sa.Select(db.EstimateType)):
                db_estimates = get_estimate_data(session, db_user.id, db_estimate_type.id)
                if len(db_estimates) < db_estimate_type.min_datapoints:
                    continue
                values = [
                    _estimate_to_value(est, db_estimate_type.relative) for est in db_estimates
                ]
                values.sort()
                num_remove = math.ceil(0.05 * len(values))
                db_statistics = session.scalars(
                    sa.select(db.EstimateStatistics)
                    .where(db.EstimateStatistics.user == db_user)
                    .where(db.EstimateStatistics.estimate_type == db_estimate_type)
                ).first()
                if db_statistics is None:
                    db_statistics = db.EstimateStatistics(
                        user=db_user, estimate_type=db_estimate_type
                    )
                    session.add(db_statistics)
                db_statistics.evaluated = now
                db_statistics.shift_pessimistic = values[-num_remove - 1]
                db_statistics.shift_optimistic = values[num_remove]
                db_statistics.shift_average = sum(values) / len(values)
                db_statistics.num_datapoints = len(values)


@dataclass
class _UserState:
    now: datetime
    db_user: db.User
    db_prev_task: db.Task | None = None
    prev_count: int = 0
    optimistic_iterator: peekable = field(init=False)
    average_iterator: peekable = field(init=False)
    pessimistic_iterator: peekable = field(init=False)

    @property
    def last_end(self):
        if self.db_prev_task is not None:
            return self.db_prev_task.scheduled_average_end
        else:
            return self.now

    def __post_init__(self):
        base_iterator = db.iterate_schedule(
            self.db_user, (self.now - timedelta(days=1)).date(), naive=True
        )
        next_schedule = None
        while next_schedule is None or next_schedule[1] < self.now:
            try:
                next_schedule = next(base_iterator)
            except StopIteration:
                next_schedule = None
                base_iterator = iter([])
                break
        self.optimistic_iterator, self.average_iterator, self.pessimistic_iterator = [
            peekable(it) for it in tee(base_iterator, 3)
        ]
        if next_schedule is not None:
            self.optimistic_iterator.prepend(next_schedule)
            self.average_iterator.prepend(next_schedule)
            self.pessimistic_iterator.prepend(next_schedule)


def _calculate_end_time(
    start: datetime,
    schedule_iterator: peekable,
    duration: timedelta,
) -> datetime:
    try:
        while schedule_iterator.peek()[1] < start:
            next(schedule_iterator)
        start = max(start, schedule_iterator.peek()[0])
        while schedule_iterator.peek()[1] < start + duration:
            duration -= schedule_iterator.peek()[1] - start
            start = schedule_iterator.peek()[1]
            next(schedule_iterator)
            start = max(start, schedule_iterator.peek()[0])
        return start + duration
    except StopIteration:
        return datetime.max


def _add_task_next(
    user_state: _UserState,
    db_task: db.Task,
):
    # TODO: apply correction factor
    count_prev = user_state.prev_count
    corr_fac = math.sqrt(max(count_prev, 4) - 1) / math.sqrt(max(count_prev, 4))
    if user_state.db_prev_task is not None:
        start_average = user_state.db_prev_task.scheduled_average_end
        start_optimistic = user_state.db_prev_task.scheduled_optimistic_end
        start_pessimistic = user_state.db_prev_task.scheduled_pessimistic_end
        # if count_prev > 4: # TODO apply correction factor
    else:
        start_average = user_state.now
        start_optimistic = user_state.now
        start_pessimistic = user_state.now
    db_task.scheduled_assignee = user_state.db_user
    set_task_state(db_task, db.TaskState.SCHEDULED)
    # TODO: apply work schedule for realistic timeline!
    db_estimate = get_estimate(user_state.db_user, db_task)
    end_average = _calculate_end_time(
        start_average, user_state.average_iterator, db_estimate.expectation_average
    )
    end_optimistic = _calculate_end_time(
        start_optimistic, user_state.optimistic_iterator, db_estimate.expectation_optimistic
    )
    end_pessimistic = _calculate_end_time(
        start_pessimistic, user_state.pessimistic_iterator, db_estimate.expectation_pessimistic
    )

    db_task.scheduled_optimistic_start = start_optimistic
    db_task.scheduled_optimistic_end = end_optimistic
    db_task.scheduled_average_start = start_average
    db_task.scheduled_average_end = end_average
    db_task.scheduled_pessimistic_start = start_pessimistic
    db_task.scheduled_pessimistic_end = end_pessimistic

    user_state.prev_count += 1
    user_state.db_prev_task = db_task
    # db_task.scheduled_average_end = last_end + db_estimate.


@dataclass
class Estimate:
    ids: list[int]
    created_at: datetime
    estimated_duration: timedelta
    expectation_optimistic: timedelta
    expectation_pessimistic: timedelta
    expectation_average: timedelta
    task: db.Task
    user: db.User

    @classmethod
    def from_db_estimate(cls, value: db.Estimate):
        return cls(
            ids=[value.id],
            created_at=value.created_at,
            estimated_duration=value.estimated_duration,
            expectation_optimistic=value.expectation_optimistic,
            expectation_pessimistic=value.expectation_pessimistic,
            expectation_average=value.expectation_average,
            task=value.task,
            user=value.user,
        )

    @classmethod
    def combine(cls, task: db.Task, values: list[db.Estimate]):
        users = {v.user for v in values}
        assert len(users) == 1

        return cls(
            ids=[el for v in values for el in v.ids],
            created_at=max(v.created_at for v in values),
            estimated_duration=sum(v.estimated_duration for v in values),
            expectation_optimistic=sum(v.expectation_optimistic for v in values),
            expectation_pessimistic=sum(v.expectation_pessimistic for v in values),
            expectation_average=sum(v.expectation_average for v in values),
            task=task,
            user=list(users)[0],
        )


def get_estimate(db_user: db.User, db_task: db.Task, recursive: bool = True) -> Estimate:
    db_estimates = [e for e in db_task.estimates if e.user_id == db_user.id]
    result = max(db_estimates, key=lambda e: e.created_at, default=None)
    if result is not None:
        result = Estimate.from_db_estimate(result)

    if recursive and db_task.children:
        child_estimates = [get_estimate(db_user, c, True) for c in db_task.children]
        if all(ce is not None for ce in child_estimates) and (
            result is None or any(ce.created_at > result.created_at for ce in child_estimates)
        ):
            result = Estimate.combine(db_task, child_estimates)
    return result


def run_auto_scheduling(now: datetime | None, external_session: db.Session | None = None):
    if now is None:
        now = datetime.utcnow()
    with db.use_or_open_session(external_session) as session:
        db_tasks_to_schedule = session.scalars(
            sa.select(db.Task)
            .where(db.Task.automatic_schedule == True)
            .where(
                (db.Task.task_state == db.TaskState.PLANNING)
                | (db.Task.task_state == db.TaskState.SCHEDULED)
            )
            .where(db.Task.estimates.any())
        ).all()
        db_tasks_fixed = session.scalars(
            sa.select(db.Task)
            .where(db.Task.automatic_schedule == False)
            .where(db.Task.task_state == db.TaskState.SCHEDULED)
        ).all()
        db_users = session.scalars(sa.select(db.User)).all()

        user_states = {db_user.id: _UserState(now, db_user) for db_user in db_users}
        db_fixed_user = {db_user.id: [] for db_user in db_users}
        for db_task in db_tasks_fixed:
            assert db_task.scheduled_assignee_id is not None
            db_fixed_user[db_task.scheduled_assignee_id].append(db_task)
        for db_user in db_users:
            user_state = user_states[db_user.id]
            db_user_tasks = db_fixed_user[db_user.id]
            db_active_task = None
            awp = db_user.active_work_period
            db_user_tasks.sort(key=lambda t: t.order_id)
            if isinstance(awp, db.WorkPeriodTask):
                db_active_task = awp
            else:
                db_active_task = db_user.interrupted_task
            if db_active_task in db_user_tasks:
                db_user_tasks.remove(db_active_task)
                db_user_tasks = [db_active_task] + db_user_tasks
            for db_task in db_user_tasks:
                _add_task_next(user_state, db_task)

        while db_tasks_to_schedule:
            user_state = min(user_states.values(), key=lambda us: us.last_end, default=None)
            if not user_state:
                logger.warning(
                    f"Failed to schedule tasks: {[t.name for t in db_tasks_to_schedule]}"
                )
                break
            db_estimates = [
                e
                for t in db_tasks_to_schedule
                if (e := get_estimate(user_state.db_user, t)) is not None
            ]
            if not db_estimates:
                del user_states[user_state.db_user.id]
                continue
            # TODO: select task with highest priority
            _add_task_next(user_state, db_estimates[0].task)
            db_tasks_to_schedule.remove(db_estimates[0].task)


def store_schedule_history(now: datetime | None, external_session: db.Session | None = None):
    if now is None:
        now = datetime.utcnow()
    with db.use_or_open_session(external_session) as session:
        tasks = session.scalars(
            sa.select(db.Task)
            .where(db.Task.finished_at == None)
            .where(db.Task.scheduled_average_end != None)
        )
        for t in tasks:
            session.add(
                db.TaskHistory(
                    task=t,
                    date=now,
                    scheduled_average_end=t.scheduled_average_end,
                    scheduled_optimistic_end=t.scheduled_optimistic_end,
                    scheduled_pessimistic_end=t.scheduled_pessimistic_end,
                )
            )
