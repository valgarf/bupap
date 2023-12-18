from .index import create_index_page
from .login import create_login_page
from .projects import create_projects_page
from .tasks import create_tasks_page
from .teams import create_teams_page
from .users import create_users_page


def create_all_pages():
    create_login_page()
    create_index_page()
    create_projects_page()
    create_teams_page()
    create_users_page()
    create_tasks_page()
