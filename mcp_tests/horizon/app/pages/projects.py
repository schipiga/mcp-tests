"""
Projects page.

@author: schipiga@mirantis.com
"""

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pom import ui
from selenium.webdriver.common.by import By

from mcp_tests.horizon.app import ui as _ui

from .base import PageBase


@ui.register_ui(
    checkbox=_ui.CheckBox(By.CSS_SELECTOR, 'input[type="checkbox"]'),
    dropdown_menu=_ui.DropdownMenu(),
    link_project=ui.UI(By.CSS_SELECTOR, 'td[data-cell-name="name"] a'))
class RowProject(_ui.Row):
    """Project row of projects table."""


class TableProjects(_ui.Table):
    """Projects table."""

    columns = {'name': 2}
    row_cls = RowProject


@ui.register_ui(field_name=ui.TextField(By.NAME, 'name'))
class FormCreateProject(_ui.Form):
    """Form to create new project."""

    submit_locator = By.CSS_SELECTOR, 'input.btn.btn-primary'


@ui.register_ui(
    button_create_project=ui.Button(By.ID, 'tenants__action_create'),
    button_filter_projects=ui.Button(By.CLASS_NAME, 'fa-search'),
    field_filter_projects=ui.TextField(By.NAME, 'tenants__filter__q'),
    form_create_project=FormCreateProject(By.CSS_SELECTOR,
                                          'form[action*="identity/create"]'),
    form_delete_project_confirm=_ui.Form(By.CSS_SELECTOR, 'div.modal-content'),
    table_projects=TableProjects(By.ID, 'tenants'))
class PageProjects(PageBase):
    """Projects page."""

    url = "/identity/"
    navigate_items = "Identity", "Projects"
