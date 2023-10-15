from typing import overload

import sqlalchemy as sa

from bupap import db
from bupap.ui.viewmodel.work import (
    ClockIn,
    ClockOut,
    TaskEnd,
    TaskStart,
    TimesinkEnd,
    TimesinkStart,
    WorkPeriodEnd,
)

from .common import get_from_id, return_obj_or_id, set_task_state


def start_work_period(
    work: TaskStart | TimesinkStart | ClockIn, external_session: db.Session | None = None
):
    with db.use_or_open_session(external_session) as session:
        db_user = get_from_id(session, db.User, work.user_id)
        db_prev_work_period = None
        db_work_period = None
        if isinstance(work, TaskStart):
            db_task = get_from_id(session, db.Task, work.task_id)
            db_work_period = db.WorkPeriodTask(task=db_task)
            db_prev_work_period = db_user.active_work_period
            db_user.interrupted_task = None
            set_task_state(db_task, db.TaskState.IN_PROGRESS)
        elif isinstance(work, TimesinkStart):
            db_timesink = get_from_id(session, db.Timesink, work.timesink_id)
            db_work_period = db.WorkPeriodTimesink(timesink=db_timesink)
            db_prev_work_period = db_user.active_work_period
            if db_prev_work_period is not None and isinstance(
                db_prev_work_period, db.WorkPeriodTask
            ):
                db_user.interrupted_task = db_prev_work_period.task
        elif isinstance(work, ClockIn):
            if db_user.active_working:
                return
            db_work_period = db.WorkPeriodWorking()
        else:
            assert False
        db_work_period.started_at = work.started_at
        db_work_period.user = db_user
        session.add(db_work_period)
        if db_prev_work_period is not None:
            end_work_period(
                WorkPeriodEnd(db_prev_work_period.id, ended_at=work.started_at),
                external_session=session,
            )

        if isinstance(db_work_period, db.WorkPeriodWorking):
            # clocking in, check if we can continue interrupted task
            db_interrupted = db_work_period.user.interrupted_task
            if db_interrupted is not None:
                start_work_period(
                    TaskStart(db_interrupted.id, db_work_period.user.id, work.started_at),
                    external_session=session,
                )


def end_work_period(
    work: WorkPeriodEnd | TaskEnd | TimesinkEnd | ClockOut,
    external_session: db.Session | None = None,
):
    with db.use_or_open_session(external_session) as session:
        db_work_period = None
        if isinstance(work, WorkPeriodEnd):
            db_work_period = get_from_id(session, db.WorkPeriod, work.work_period_id)
        elif isinstance(work, TaskEnd):
            db_work_period = session.scalars(
                sa.select(db.WorkPeriodTask)
                .where(db.WorkPeriodTask.user_id == work.user_id)
                .where(db.WorkPeriodTask.task_id == work.task_id)
                .where(db.WorkPeriodTask.ended_at == None)
            ).first()
        elif isinstance(work, TimesinkEnd):
            db_work_period = session.scalars(
                sa.select(db.WorkPeriodTimesink)
                .where(db.WorkPeriodTimesink.user_id == work.user_id)
                .where(db.WorkPeriodTimesink.timesink_id == work.timesink_id)
                .where(db.WorkPeriodTimesink.ended_at == None)
            ).first()
        elif isinstance(work, ClockOut):
            db_user = get_from_id(session, db.User, work.user_id)
            db_work_period = db_user.active_working

        if db_work_period is None:
            return
        db_work_period.ended_at = work.ended_at

        if isinstance(db_work_period, db.WorkPeriodWorking):
            # Clocking out, set active task as interrupted task
            db_user = db_work_period.user
            db_active_work_period = db_user.active_work_period
            if isinstance(db_active_work_period, db.WorkPeriodTask):
                db_user.interrupted_task = db_active_work_period.task
            if db_active_work_period is not None:
                db_active_work_period.ended_at = work.ended_at

        if isinstance(db_work_period, db.WorkPeriodTimesink):
            # Ending timesink, reactivate interrupted task
            db_interrupted = db_work_period.user.interrupted_task
            if db_interrupted is not None:
                start_work_period(
                    TaskStart(db_interrupted.id, db_work_period.user_id, work.ended_at),
                    external_session=session,
                )

        # if isinstance(db_work_period, db.WorkPeriodTask):
        #     db_work_period.user.interrupted_task = None
