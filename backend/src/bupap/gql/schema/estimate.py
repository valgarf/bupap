from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Annotated, Self

import strawberry

from bupap import db
from bupap.gql.common.context import InfoContext
from bupap.ui.crud.task import get_estimate_data

from ..common.db_type import DBConvExtension, DBType, map_to_db
from .common import Timedelta

if TYPE_CHECKING:
    from .task import Task
    from .user import User


@strawberry.type
class EstimateType(DBType, strawberry.relay.Node):
    _db_table = db.EstimateType
    db_id: int = map_to_db("id")
    name: str = map_to_db()
    description: str = map_to_db()
    relative: bool = map_to_db()
    min_datapoints: int = map_to_db()
    max_datapoints: int = map_to_db()
    default_shift_optimistic: float = map_to_db()
    default_shift_pessimistic: float = map_to_db()
    default_shift_average: float = map_to_db()
    # estimates: list["Estimate"] = map_to_db()
    estimate_statistics: list["EstimateStatistics"] = map_to_db()


@strawberry.type
class Estimate(DBType, strawberry.relay.Node):
    _db_table = db.Estimate

    db_id: int = map_to_db("id")
    task: Annotated["Task", strawberry.lazy(".task")] = map_to_db()
    user: Annotated["User", strawberry.lazy(".user")] = map_to_db()
    estimate_type: EstimateType = map_to_db()

    created_at: datetime = map_to_db()
    estimated_duration: Timedelta = map_to_db()
    expectation_optimistic: Timedelta = map_to_db()
    expectation_pessimistic: Timedelta = map_to_db()
    expectation_average: Timedelta = map_to_db()


@strawberry.type
class EstimateDatapoint:
    estimate: Estimate
    value: float
    actual_work: Timedelta
    num_work_periods: int
    start: datetime
    end: datetime


@strawberry.type
class EstimateStatistics(DBType, strawberry.relay.Node):
    _db_table = db.EstimateStatistics

    db_id: int = map_to_db("id")
    num_datapoints: int = map_to_db()
    evaluated: datetime = map_to_db()

    # shifts are either given in seconds (non-relative estimate type) or as multipliers (relative
    # estimate type)
    shift_optimistic: float = map_to_db()
    shift_pessimistic: float = map_to_db()
    shift_average: float = map_to_db()

    user: Annotated["User", strawberry.lazy(".user")] = map_to_db()
    estimate_type: EstimateType = map_to_db()

    @strawberry.field
    def sufficient(self) -> bool:
        return self.db_obj.num_datapoints >= self.db_obj.estimate_type.min_datapoints

    @strawberry.field
    def datapoints(self, info: InfoContext) -> list[EstimateDatapoint]:
        db_self: db.EstimateStatistics = self.db_obj
        session = info.context.db_session
        db_estimates = get_estimate_data(
            session, db_self.user_id, db_self.estimate_type_id, db_self.evaluated
        )
        if not db_estimates:
            return []
        result = []
        for db_estimate in db_estimates:
            db_work_periods = [
                wp
                for wp in db_estimate.task.work_periods
                if wp.duration is not None and wp.user_id == db_self.user_id
            ]
            actual_work = sum([wp.duration for wp in db_work_periods], start=timedelta())
            value = (
                actual_work / db_estimate.estimated_duration
                if db_self.estimate_type.relative
                else (actual_work - db_estimate.estimated_duration).total_seconds()
            )
            result.append(
                EstimateDatapoint(
                    estimate=Estimate(db_estimate),
                    value=value,
                    actual_work=actual_work,
                    num_work_periods=len(db_work_periods),
                    start=min(wp.started_at for wp in db_work_periods),
                    end=max(wp.ended_at for wp in db_work_periods),
                )
            )
        return result
