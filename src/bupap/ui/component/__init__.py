from nicegui import ui

from .adduser import AddUser
from .avatar import Avatar
from .errors import Errors
from .gantt import Gantt, GanttData, GanttEntryData, GanttEntryType, GanttMode, GanttRowData
from .header import Header
from .pick_date import PickDate
from .router import RequestInfo, Router
from .user_card import user_card

# from .avatar import Avatar


def separator_line():
    return ui.element("hr").classes("h-px my-1 bg-gray-200 border-0 dark:bg-gray-700")
