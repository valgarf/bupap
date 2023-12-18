from enum import Flag, auto

# NOTE
# feature request stages:
#   requests -> planning -> backlog -> scheduled
# bug / adhoc tasks:
#   backlog -> scheduled


class Permission(Flag):
    ADMIN_SETTINGS = auto()  # modify administration settings

    MODIFY_SELF = (
        auto()
    )  # modify your own name, mail, image, etc. (you can always set your own password)
    MODIFY_USERS = auto()  # modify any user including passwords!
    ASSIGN_USERS = auto()  # assign users to teams
    ASSIGN_PROJECTS = auto()  # assign projects to teams

    OPEN_REQUESTS = auto()  # enter in requests stage
    APPROVE_REQUESTS = auto()  # entered into planning phase
    ASSIGN_PRIORITY = auto()  # assign priority to tasks
    CREATE_SUBTASKS = auto()  # allow creation of subtasks on existing tasks
    ESTIMATE_TASKS = auto()  # allow time estimation of tasks
    FINALIZE_PLANNING = auto()  # move from planning to backlog stage
    AUTO_SCHEDULE_TASKS = auto()  # move tasks from backlog to scheduled stage
    ASSIGN_TASKS = auto()  # explicitely assign tasks to users
    ASSIGN_SELF = auto()  # assign tasks to yourself

    REPORT_BUGS = auto()  # create bug tasks
    ADHOC_TASKS = auto()  # create adhoc tasks


default_global_roles = {
    "Admin": Permission(sum(el.value for el in Permission)),
    "User": Permission.MODIFY_SELF,
}

default_team_roles = {
    "Lead": Permission.APPROVE_REQUESTS
    | Permission.AUTO_SCHEDULE_TASKS
    | Permission.ASSIGN_TASKS
    | Permission.ADHOC_TASKS,
    "Developer": Permission.MODIFY_SELF
    | Permission.CREATE_SUBTASKS
    | Permission.ESTIMATE_TASKS
    | Permission.FINALIZE_PLANNING
    | Permission.ASSIGN_SELF
    | Permission.REPORT_BUGS
    | Permission.ADHOC_TASKS,
}

default_project_roles = {
    "Product Owner": Permission.OPEN_REQUESTS
    | Permission.REPORT_BUGS
    | Permission.ADHOC_TASKS
    | Permission.ASSIGN_PRIORITY,
    "Stakeholder": Permission.OPEN_REQUESTS | Permission.REPORT_BUGS,
    "Reporter": Permission.REPORT_BUGS,
}
