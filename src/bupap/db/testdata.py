from dataclasses import dataclass, field
from datetime import datetime, time, timedelta
from random import choice, randint, random, sample, seed
from typing import cast

import sqlalchemy as sa
import sqlalchemy.orm
from loguru import logger

from bupap.ui.crud.project import assign_project_role, create_project
from bupap.ui.crud.task import (
    create_task,
    estimate_task,
    get_estimate,
    get_next_tasks,
    run_auto_scheduling,
    store_schedule_history,
    task_done,
    update_statistics,
)
from bupap.ui.crud.team import assign_team_project, assign_team_role, create_team
from bupap.ui.crud.user import create_user
from bupap.ui.crud.work import end_work_period, start_work_period
from bupap.ui.viewmodel import (
    ClockIn,
    ClockOut,
    NewEstimate,
    NewProject,
    NewTask,
    NewTeam,
    NewUser,
    TaskDone,
    TaskStart,
    TimesinkEnd,
    TimesinkStart,
)

from . import (
    EstimateType,
    Frequency,
    Project,
    ScheduleRule,
    Task,
    TaskPriority,
    TaskType,
    Team,
    Timesink,
    User,
    Weekdays,
)
from . import session as db_session


@dataclass
class TestdataUsers:
    # backend
    db_cmarmo: User
    db_tthorley: User
    db_oneville: User
    db_sreece: User
    db_hbrant: User
    db_lpettersson: User
    db_llewis: User
    db_wbest: User

    # frontend
    db_macquafredda: User
    db_cmorandi: User
    db_ffierro: User
    db_pharley: User
    db_lduke: User
    db_amartinson: User
    db_eready: User
    db_rtravieso: User
    db_ateel: User

    @property
    def backend_devs(self):
        return [
            self.db_tthorley,
            self.db_oneville,
            self.db_sreece,
            self.db_hbrant,
            self.db_lpettersson,
            self.db_llewis,
            self.db_wbest,
        ]

    @property
    def frontend_devs(self):
        return [
            self.db_cmorandi,
            self.db_ffierro,
            self.db_pharley,
            self.db_lduke,
            self.db_amartinson,
            self.db_eready,
            self.db_rtravieso,
            self.db_ateel,
        ]

    @property
    def backend_leads(self):
        return [self.db_cmarmo, self.db_tthorley]

    @property
    def frontend_leads(self):
        return [self.db_macquafredda, self.db_cmorandi]

    @property
    def backend_all(self):
        return [self.db_cmarmo] + self.backend_devs

    @property
    def frontend_all(self):
        return [self.db_macquafredda] + self.frontend_devs

    @property
    def all(self):
        return self.backend_all + self.frontend_all

    @property
    def all_devs(self):
        return self.backend_devs + self.frontend_devs


@dataclass
class TestdataProjects:
    db_proj_tooling: Project
    db_proj_tooling_debugger: Project
    db_proj_tooling_metrics: Project
    db_proj_tooling_build_tools: Project
    db_proj_tooling_deployment: Project
    db_proj_tooling_testing_tools: Project
    db_proj_showcase_y: Project
    db_proj_management: Project
    db_proj_x: Project

    @property
    def backend(self):
        return [self.db_proj_tooling, self.db_proj_management, self.db_proj_x]

    @property
    def frontend(self):
        return [self.db_proj_showcase_y, self.db_proj_management, self.db_proj_x]

    @property
    def top_level(self):
        return [
            self.db_proj_tooling,
            self.db_proj_showcase_y,
            self.db_proj_management,
            self.db_proj_x,
        ]


@dataclass
class TestdataState:
    users: TestdataUsers
    projects: TestdataProjects
    session: sa.orm.Session
    current: datetime
    possible_devs: dict[int, Task] = field(default_factory=dict)


TOOL_SUBPROJECTS = ["debugger", "metrics", "build tools", "deployment", "testing tools"]


def add_testdata(end: datetime = None):
    """
    Fills the database with testdata to be used in internal tests and demonstrations.
    """

    with db_session() as session:
        if len(session.scalars(sa.select(User)).all()) != 1 or any(
            session.scalars(sa.select(cls)).first() is not None for cls in [Team, Project]
        ):
            logger.warning("Database already has data, skipping creation of testdata")
            return

        logger.info("Creating Testdata")

        # Backend
        db_backend = create_team(NewTeam(name="Team Backend"), external_session=session)

        # fmt: off
        db_cmarmo = create_user(NewUser("cmarmo", " Caradog Marmo ", "cmarmo"), external_session=session)
        db_tthorley = create_user(NewUser("tthorley", "Theodore Thorley", "tthorley"), external_session=session)
        db_oneville = create_user(NewUser("oneville", "Owain Neville", "oneville"), external_session=session)
        db_sreece = create_user(NewUser("sreece", "Sabina Reece", "sreece"), external_session=session)
        db_hbrant = create_user(NewUser("hbrant", "Hugo Brant", "hbrant"), external_session=session)
        db_lpettersson = create_user(NewUser("lpettersson", "Lea Pettersson", "lpettersson"), external_session=session)
        db_llewis = create_user(NewUser("llewis", "Lorene Lewis", "llewis"), external_session=session)
        db_wbest = create_user(NewUser("wbest", "Winfield Best", "wbest"), external_session=session)
        # fmt: on

        session.flush()
        assign_team_role(db_backend.id, db_cmarmo.id, "Lead", external_session=session)
        assign_team_role(db_backend.id, db_tthorley.id, "Lead", external_session=session)
        assign_team_role(db_backend.id, db_tthorley.id, "Developer", external_session=session)
        assign_team_role(db_backend.id, db_oneville.id, "Developer", external_session=session)
        assign_team_role(db_backend.id, db_sreece.id, "Developer", external_session=session)
        assign_team_role(db_backend.id, db_hbrant.id, "Developer", external_session=session)
        assign_team_role(db_backend.id, db_lpettersson.id, "Developer", external_session=session)
        assign_team_role(db_backend.id, db_llewis.id, "Developer", external_session=session)
        assign_team_role(db_backend.id, db_wbest.id, "Developer", external_session=session)

        # Frontend
        db_frontend = create_team(NewTeam(name="Team Frontend"), external_session=session)

        # fmt: off
        db_macquafredda = create_user(NewUser("macquafredda", "Dr. Maud Acquafredda", "macquafredda"), external_session=session)
        db_cmorandi = create_user(NewUser("cmorandi", "Caterina Morandi", "cmorandi"), external_session=session)
        db_ffierro = create_user(NewUser("ffierro", "Fausto Fierro", "ffierro"), external_session=session)
        db_pharley = create_user(NewUser("pharley", "Pablo Harley", "pharley"), external_session=session)
        db_lduke = create_user(NewUser("lduke", "Lluïsa Duke", "lduke"), external_session=session)
        db_amartinson = create_user(NewUser("amartinson", "Agathe Martinson", "amartinson"), external_session=session)
        db_eready = create_user(NewUser("eready", "Elettra Ready", "eready"), external_session=session)
        db_rtravieso = create_user(NewUser("rtravieso", "Rosemonde Travieso", "rtravieso"), external_session=session)
        db_ateel = create_user(NewUser("ateel", "Alfonsina Teel", "ateel"), external_session=session)
        # fmt: on

        session.flush()
        assign_team_role(db_frontend.id, db_macquafredda.id, "Lead", external_session=session)
        assign_team_role(db_frontend.id, db_cmorandi.id, "Lead", external_session=session)
        assign_team_role(db_frontend.id, db_cmorandi.id, "Developer", external_session=session)
        assign_team_role(db_frontend.id, db_ffierro.id, "Developer", external_session=session)
        assign_team_role(db_frontend.id, db_pharley.id, "Developer", external_session=session)
        assign_team_role(db_frontend.id, db_lduke.id, "Developer", external_session=session)
        assign_team_role(db_frontend.id, db_amartinson.id, "Developer", external_session=session)
        assign_team_role(db_frontend.id, db_eready.id, "Developer", external_session=session)
        assign_team_role(db_frontend.id, db_rtravieso.id, "Developer", external_session=session)
        assign_team_role(db_frontend.id, db_ateel.id, "Developer", external_session=session)

        # Projects

        # fmt: off
        db_proj_tooling = create_project(NewProject("Internal Tooling", "Project for internal scripts and larger tooling needs.", "#b0bec5"), external_session=session)
        db_proj_showcase_y = create_project(NewProject("Showcase Y", "Mockups for project X. Frontend only, will be built if a customer buys it.", "#aed581"), external_session=session)
        db_proj_management = create_project(NewProject("Management tasks", "A place for direct tasks from management that don't fit anywhere else.", "#4db6ac"), external_session=session)
        db_proj_x = create_project(NewProject("Project X", "Our greatest hit.", "#ffb74d"), external_session=session)

        session.flush()
        db_proj_tooling_debugger = create_project(NewProject("Internal Tooling - debugger", "Subproject of internal tooling", "#b0bec5", parent_id=db_proj_tooling.id), external_session=session)
        db_proj_tooling_metrics = create_project(NewProject("Internal Tooling - metrics", "Subproject of internal tooling", "#b0bec5", parent_id=db_proj_tooling.id), external_session=session)
        db_proj_tooling_build_tools = create_project(NewProject("Internal Tooling - build_tools", "Subproject of internal tooling", "#b0bec5", parent_id=db_proj_tooling.id), external_session=session)
        db_proj_tooling_deployment = create_project(NewProject("Internal Tooling - deployment", "Subproject of internal tooling", "#b0bec5", parent_id=db_proj_tooling.id), external_session=session)
        db_proj_tooling_testing_tools = create_project(NewProject("Internal Tooling - testing_tools", "Subproject of internal tooling", "#b0bec5", parent_id=db_proj_tooling.id), external_session=session)

        session.flush()
        db_proj_tooling_deployment_ci =  create_project(NewProject("Internal Tooling - deployment - ci", "Subproject of internal tooling - depoloyment", "#b0bec5", parent_id=db_proj_tooling_deployment.id), external_session=session)

        session.flush()
        db_proj_tooling_deployment_ci_secrets =  create_project(NewProject("Internal Tooling - deployment - ci - secrets", "Subproject of internal tooling - depoloyment - ci", "#b0bec5", parent_id=db_proj_tooling_deployment_ci.id), external_session=session)
        # fmt: on

        session.flush()

        assign_team_project(db_backend.id, db_proj_tooling.id, external_session=session)
        assign_team_project(db_backend.id, db_proj_management.id, external_session=session)
        assign_team_project(db_backend.id, db_proj_x.id, external_session=session)
        assign_team_project(db_frontend.id, db_proj_tooling.id, external_session=session)
        assign_team_project(db_frontend.id, db_proj_showcase_y.id, external_session=session)
        assign_team_project(db_frontend.id, db_proj_management.id, external_session=session)
        assign_team_project(db_frontend.id, db_proj_x.id, external_session=session)

        # start
        if end is None:
            end = datetime.utcnow()
        start = end.date() - timedelta(days=30)  # 365*2)
        start -= timedelta(days=start.weekday())
        start = datetime.combine(start, time(hour=8))

        # state
        state = TestdataState(
            users=TestdataUsers(
                db_cmarmo=db_cmarmo,
                db_tthorley=db_tthorley,
                db_oneville=db_oneville,
                db_sreece=db_sreece,
                db_hbrant=db_hbrant,
                db_lpettersson=db_lpettersson,
                db_llewis=db_llewis,
                db_wbest=db_wbest,
                db_macquafredda=db_macquafredda,
                db_cmorandi=db_cmorandi,
                db_ffierro=db_ffierro,
                db_pharley=db_pharley,
                db_lduke=db_lduke,
                db_amartinson=db_amartinson,
                db_eready=db_eready,
                db_rtravieso=db_rtravieso,
                db_ateel=db_ateel,
            ),
            projects=TestdataProjects(
                db_proj_tooling=db_proj_tooling,
                db_proj_tooling_debugger=db_proj_tooling_debugger,
                db_proj_tooling_metrics=db_proj_tooling_metrics,
                db_proj_tooling_build_tools=db_proj_tooling_build_tools,
                db_proj_tooling_deployment=db_proj_tooling_deployment,
                db_proj_tooling_testing_tools=db_proj_tooling_testing_tools,
                db_proj_showcase_y=db_proj_showcase_y,
                db_proj_management=db_proj_management,
                db_proj_x=db_proj_x,
            ),
            session=session,
            current=start,
        )
        # schedule
        for user in state.users.all_devs:
            session.add(
                ScheduleRule(
                    user=user,
                    timezone="Europe/Berlin",
                    start=time(10),
                    end=time(18),
                    freq=Frequency.DAILY,
                    byweekday=Weekdays.MONDAY
                    | Weekdays.TUESDAY
                    | Weekdays.WEDNESDAY
                    | Weekdays.THURSDAY
                    | Weekdays.FRIDAY,
                    interval=1,
                    dtstart=(start - timedelta(days=2)).date(),
                )
            )
        session.flush()
        # tasks
        unassigned_devs = state.users.all_devs
        unplanned_tasks = []
        possible_devs = state.possible_devs

        db_timesink_meeting = session.scalars(
            sa.Select(Timesink).where(Timesink.name == "Meeting")
        ).one()
        db_timesink_other = session.scalars(
            sa.Select(Timesink).where(Timesink.name == "Other")
        ).one()
        db_timesink_planning = session.scalars(
            sa.Select(Timesink).where(Timesink.name == "Planning")
        ).one()
        db_estimate_type = session.scalars(
            sa.Select(EstimateType).where(EstimateType.name == "Thought-out")
        ).one()
        events = [
            {"at": start + timedelta(hours=2), "type": "meeting"},
            {"at": start + timedelta(hours=8), "type": "shift_end"},
        ]
        for db_dev in state.users.all_devs:
            start_work_period(ClockIn(db_dev.id, state.current), external_session=session)
        while state.current < end:
            if len(unplanned_tasks) < 10:
                for i in range(10):
                    db_task = generate_task_for_project(state, state.projects.top_level)
                    unplanned_tasks.append(db_task.id)

            invert_unplanned = {}
            for db_task_id in unplanned_tasks:
                db_dev = possible_devs[db_task_id]
                for db_dev in db_dev:
                    invert_unplanned.setdefault(db_dev.id, []).append(db_task_id)

            for db_dev in list(unassigned_devs):
                db_tasks = get_next_tasks(db_dev.id, 1, external_session=session)
                if db_tasks and (not invert_unplanned.get(db_dev.id) or randint(0, 9) < 8):
                    if db_task.id in unplanned_tasks:
                        unplanned_tasks.remove(db_task.id)
                    db_task: Task = db_tasks[0]
                    start_work_period(
                        TaskStart(db_task.id, db_dev.id, state.current), external_session=session
                    )
                    unassigned_devs.remove(db_dev)
                    db_estimate = get_estimate(db_dev, db_task)
                    assert db_estimate is not None
                    duration = db_estimate.estimated_duration * (random() + 0.8)
                    events.append(
                        {
                            "at": state.current + duration,
                            "type": "finished_task",
                            "person": db_dev,
                            "task": db_task,
                        }
                    )

            new_schedule_necessary = False
            for db_dev in list(unassigned_devs):
                to_plan = invert_unplanned.get(db_dev.id)
                if to_plan:
                    new_schedule_necessary = True
                    unassigned_devs.remove(db_dev)
                    events.append(
                        {
                            "at": state.current + timedelta(minutes=10 * len(to_plan)),
                            "type": "finished_planning",
                            "person": db_dev,
                        }
                    )
                    for db_task_id in to_plan:
                        if db_task_id in unplanned_tasks:
                            unplanned_tasks.remove(db_task_id)
                        duration = timedelta(hours=randint(4, 12))
                        estimate_task(
                            NewEstimate(
                                db_task_id, db_dev.id, db_estimate_type.id, duration, state.current
                            ),
                            external_session=session,
                        )
                    start_work_period(
                        TimesinkStart(db_timesink_planning.id, db_dev.id, state.current),
                        external_session=session,
                    )

                    invert_unplanned[db_dev.id] = []

            if new_schedule_necessary:
                run_auto_scheduling(
                    datetime.combine(state.current.date(), time()), external_session=session
                )

            # handle next event
            events.sort(key=lambda evt: evt["at"])
            next_event = events.pop(0)
            previous = state.current
            state.current = cast(datetime, next_event["at"])
            if state.current >= end:
                break
            if next_event["type"] == "finished_task":
                task_done(TaskDone(next_event["task"].id, state.current), external_session=session)
                unassigned_devs.append(next_event["person"])
            if next_event["type"] == "finished_planning":
                end_work_period(
                    TimesinkEnd(db_timesink_planning.id, db_dev.id, state.current),
                    external_session=session,
                )
                unassigned_devs.append(next_event["person"])
            if next_event["type"] == "shift_end":
                for db_dev in state.users.all_devs:
                    end_work_period(ClockOut(db_dev.id, state.current), external_session=session)
                next_shift = timedelta(hours=16)
                for evt in events:
                    if evt["type"] != "meeting":
                        evt["at"] += next_shift
                unassigned_devs.extend(
                    [evt["person"] for evt in events if evt["type"] == "finished_planning"]
                )
                events = [evt for evt in events if evt["type"] != "finished_planning"]
                state.current += next_shift
                if state.current >= end:
                    break
                for db_dev in state.users.all_devs:
                    start_work_period(ClockIn(db_dev.id, state.current), external_session=session)
                events.append({"at": state.current + timedelta(hours=8), "type": "shift_end"})
            if next_event["type"] == "meeting":
                for db_dev in state.users.all_devs:
                    start_work_period(
                        TimesinkStart(db_timesink_meeting.id, db_dev.id, state.current),
                        external_session=session,
                    )
                meeting_duration = timedelta(hours=1)
                for evt in events:
                    if evt["type"] != "shift_end":
                        evt["at"] += meeting_duration
                unassigned_devs.extend(
                    [evt["person"] for evt in events if evt["type"] == "finished_planning"]
                )
                events = [evt for evt in events if evt["type"] != "finished_planning"]
                state.current += meeting_duration
                if state.current >= end:
                    break
                for db_dev in state.users.all_devs:
                    end_work_period(
                        TimesinkEnd(db_timesink_meeting.id, db_dev.id, state.current),
                        external_session=session,
                    )
                events.append(
                    {
                        "at": state.current + timedelta(hours=24) - meeting_duration,
                        "type": "meeting",
                    }
                )
            if previous.day != state.current.day:
                update_statistics(
                    datetime.combine(state.current.date(), time()), external_session=session
                )
                run_auto_scheduling(
                    datetime.combine(state.current.date(), time()), external_session=session
                )
                store_schedule_history(
                    datetime.combine(state.current.date(), time()), external_session=session
                )
                logger.info(f" * Testdata created for {previous.date().isoformat()}")
                # TODO: if current different day than previous: update history
            # if current different month than previous: print info
    logger.info("Testdata created")


def generate_task_for_project(state: TestdataState, db_projects: list[Project]):
    db_proj = choice(db_projects)
    users = state.users
    match (db_proj):
        case state.projects.db_proj_tooling:
            subproj = choice(
                [
                    state.projects.db_proj_tooling_debugger,
                    state.projects.db_proj_tooling_metrics,
                    state.projects.db_proj_tooling_build_tools,
                    state.projects.db_proj_tooling_deployment,
                    state.projects.db_proj_tooling_testing_tools,
                ]
            )
            adj = choice(["fancy", "crazy", "interesting", "necessary"])
            obj = choice(["feature", "improvement", "thing"])
            denom = choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            name = f"add {adj} new {obj} {denom}"
            priority = choice([TaskPriority.LOW, TaskPriority.MEDIUM, TaskPriority.HIGH])
            task = NewTask(
                subproj.id,
                TaskType.FEATURE,
                priority,
                state.current,
                name,
                description="Should really have been available already. Why has no one thought of that?",
            )
        case state.projects.db_proj_management:
            manager = choice(["Noelia", "Eskil", "Odile", "José", "Fedele"])
            task = choice(["create powerpoint", "write report", "collect data"])
            on = choice(["planned feature", "user engagement", "app usage"])
            name = f"{task} on {on} for {manager}"
            priority = choice([TaskPriority.HIGH, TaskPriority.VERY_HIGH])
            task = NewTask(
                db_proj.id,
                TaskType.FEATURE,
                priority,
                state.current,
                name,
                description="Should really have been available already. Why has no one thought of that?",
            )
        case state.projects.db_proj_showcase_y:
            obj = choice(["button", "slider", "text field", "label", "sidebar"])
            denom = choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            page = choice(["landing page", "user page", "history page"])
            action = choice([("rework design of", "on"), ("add", "to"), ("remove", "from")])
            name = f"{action[0]} {obj} {denom} {action[1]} {page}"
            priority = choice([TaskPriority.VERY_LOW, TaskPriority.LOW, TaskPriority.MEDIUM])
            task = NewTask(
                db_proj.id,
                TaskType.FEATURE,
                priority,
                state.current,
                name,
                description="That will make it a million times better! I promise!",
            )
        case state.projects.db_proj_x:
            feature = choice(
                [
                    "phase bubble",
                    "tritonic gluon turbine",
                    "phase ray flipper",
                    "beryllium dorsal booster",
                    "zinc chroniton shell",
                ]
            )
            action = choice(["add", "implement", "redesign", "fix"])
            # TODO: ggod candiate to try sub tasks, e.g.:
            # - evalute usage
            # - design specs
            # - build prototype
            # - implement
            name = f"{action} {feature}"
            priority = choice([TaskPriority.LOW, TaskPriority.MEDIUM, TaskPriority.HIGH])
            task = NewTask(
                db_proj.id,
                TaskType.FEATURE,
                priority,
                state.current,
                name,
                description="Task should be clear from name.",
            )
    db_task = create_task(task, external_session=state.session)
    if random() > 0.8:
        state.session.flush()
        for i in range(3):
            subtask = NewTask(
                task.project_id,
                TaskType.FEATURE,
                priority,
                state.current,
                f"Subtask {i}",
                f"step {i}",
                parent_id=db_task.id,
            )
            db_subtask = create_task(subtask, external_session=state.session)
            if random() > 0.5:
                state.session.flush()
                for j in range(3):
                    subsubtask = NewTask(
                        task.project_id,
                        TaskType.FEATURE,
                        priority,
                        state.current,
                        f"Sub-Subtask {i}/{j}",
                        f"step {i}/{j}",
                        parent_id=db_subtask.id,
                    )
                    create_task(subsubtask, external_session=state.session)
    state.session.flush()
    users = []
    if db_proj in state.projects.frontend:
        users.extend(sample(state.users.frontend_devs, 3))
    if db_proj in state.projects.backend:
        users.extend(sample(state.users.backend_devs, 3))
    state.possible_devs[db_task.id] = users

    assert db_task is not None
    return db_task
