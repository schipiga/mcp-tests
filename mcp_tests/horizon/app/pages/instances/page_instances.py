"""
Instances page.

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

from ..base import PageBase


@ui.register_ui(field_count=ui.TextField(By.NAME, 'count'),
                field_name=ui.TextField(By.NAME, 'name'))
class TabDetails(ui.Block):
    """Details tab."""


class RadioVolumeCreate(ui.UI):
    """Radio buttons group to create volume or no."""

    @property
    @ui.wait_for_presence
    def value(self):
        """Value of radio buttons group."""
        return self.webelement.find_element(
            By.XPATH, 'label[contains(@class, "active")]').text

    @value.setter
    @ui.wait_for_presence
    def value(self, val):
        """Set value of radio buttons group."""
        self.webelement.find_element(
            By.XPATH, 'label[text()="{}"]'.format(val)).click()


@ui.register_ui(
    label_alert=ui.UI(By.CSS_SELECTOR, 'span.invalid'))
class CellAvailable(_ui.Cell):
    """Cell."""


@ui.register_ui(
    button_add=ui.Button(By.CSS_SELECTOR, 'button.btn.btn-default'))
class RowAvailable(_ui.Row):
    """Row with available item."""

    cell_cls = CellAvailable


class TableAvailableSources(_ui.Table):
    """Available sources table."""

    columns = {'name': 2}
    row_cls = RowAvailable


@ui.register_ui(
    combobox_boot_source=ui.ComboBox(By.NAME, 'boot-source-type'),
    radio_volume_create=RadioVolumeCreate(
        By.XPATH,
        '//div[contains(@class, "btn-group") and label[@id="vol-create"]]'),
    table_available_sources=TableAvailableSources(
        By.CSS_SELECTOR, 'available table'))
class TabSource(ui.Block):
    """Source tab."""


class TableAvailableFlavors(_ui.Table):
    """Available flavors table."""

    columns = {'name': 2, 'ram': 4, 'root_disk': 6}
    row_cls = RowAvailable
    row_xpath = './/tr[contains(@ng-repeat-start, "displayedItems")]'


@ui.register_ui(
    table_available_flavors=TableAvailableFlavors(
        By.CSS_SELECTOR, 'available table'))
class TabFlavor(ui.Block):
    """Flavor tab."""


class TableAvailableNetworks(_ui.Table):
    """Available networks table."""

    columns = {'name': 2}
    row_cls = RowAvailable


@ui.register_ui(
    table_available_networks=TableAvailableNetworks(
        By.CSS_SELECTOR, 'available table'))
class TabNetwork(ui.Block):
    """Network tab."""


@ui.register_ui(
    item_source=ui.UI(By.XPATH, '//li//span[text()="Source"]'),
    item_flavor=ui.UI(By.XPATH, '//li//span[text()="Flavor"]'),
    item_network=ui.UI(By.XPATH, '//li//span[text()="Networks"]'),
    tab_details=TabDetails(By.CSS_SELECTOR,
                           'ng-include[ng-form="launchInstanceDetailsForm"]'),
    tab_source=TabSource(By.CSS_SELECTOR,
                         'ng-include[ng-form="launchInstanceSourceForm"]'),
    tab_flavor=TabFlavor(By.CSS_SELECTOR,
                         'ng-include[ng-form="launchInstanceFlavorForm"]'),
    tab_network=TabNetwork(By.CSS_SELECTOR,
                           'ng-include[ng-form="launchInstanceNetworkForm"]'))
class FormLaunchInstance(_ui.Form):
    """Form to launch new instance."""

    submit_locator = By.CSS_SELECTOR, 'button.btn.btn-primary.finish'
    cancel_locator = By.CSS_SELECTOR, 'button.btn[ng-click="cancel()"]'


@ui.register_ui(
    item_lock=ui.UI(By.CSS_SELECTOR, '*[id*="action_lock"]'),
    item_unlock=ui.UI(By.CSS_SELECTOR, '*[id*="action_unlock"]'))
class DropdownMenu(_ui.DropdownMenu):
    """Dropdown menu for instance row."""


@ui.register_ui(
    checkbox=_ui.CheckBox(By.CSS_SELECTOR, 'input[type="checkbox"]'),
    dropdown_menu=DropdownMenu(),
    link_instance=ui.Link(By.CSS_SELECTOR, 'td > a'))
class RowInstance(_ui.Row):
    """Row with instance."""

    transit_statuses = ('Build',)


class TableInstances(_ui.Table):
    """Instances table."""

    columns = {'name': 2, 'status': 7}
    row_cls = RowInstance


@ui.register_ui(
    button_delete_instances=ui.Button(By.ID, 'instances__action_delete'),
    button_filter_instances=ui.Button(By.ID, 'instances__action_filter'),
    button_launch_instance=ui.Button(By.ID, "instances__action_launch-ng"),
    field_filter_instances=ui.TextField(By.NAME, 'instances__filter__q'),
    form_launch_instance=FormLaunchInstance(
        By.CSS_SELECTOR,
        'wizard[ng-controller="LaunchInstanceWizardController"]'),
    table_instances=TableInstances(By.ID, 'instances'))
class PageInstances(PageBase):
    """Instances page."""

    url = "/project/instances/"
    navigate_items = "Project", "Compute", "Instances"
