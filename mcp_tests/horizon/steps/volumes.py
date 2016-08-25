"""
Volumes steps.

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

import pom
from waiting import wait

from mcp_tests.horizon.config import EVENT_TIMEOUT

from .base import BaseSteps


class VolumesSteps(BaseSteps):
    """Volumes steps."""

    def page_volumes(self):
        """Open volumes page if it isn't opened."""
        return self._open(self.app.page_volumes)

    def tab_volumes(self):
        """Open volumes tab."""
        with self.page_volumes() as page:
            page.label_volumes.click()
            return page.tab_volumes

    @pom.timeit('Step')
    def create_volume(self, volume_name, source_type='Image', volume_type='',
                      check=True):
        """Step to create volume."""
        tab_volumes = self.tab_volumes()
        tab_volumes.button_create_volume.click()

        with tab_volumes.form_create_volume as form:
            form.field_name.value = volume_name
            form.combobox_source_type.value = source_type

            image_sources = form.combobox_image_source.values
            form.combobox_image_source.value = image_sources[-1]

            if volume_type is not None:
                if not volume_type:
                    volume_type = form.combobox_volume_type.values[-1]
                form.combobox_volume_type.value = volume_type

            form.submit()

        if check:
            self.close_notification('info')
            tab_volumes.table_volumes.row(
                name=volume_name).wait_for_status('Available')

    @pom.timeit('Step')
    def delete_volume(self, volume_name, check=True):
        """Step to delete volume."""
        tab_volumes = self.tab_volumes()

        with tab_volumes.table_volumes.row(
                name=volume_name).dropdown_menu as menu:
            menu.button_toggle.click()
            menu.item_delete.click()

        tab_volumes.form_confirm.submit()

        if check:
            self.close_notification('success')
            tab_volumes.table_volumes.row(
                name=volume_name).wait_for_absence(EVENT_TIMEOUT)

    @pom.timeit('Step')
    def edit_volume(self, volume_name, new_volume_name, check=True):
        """Step to edit volume."""
        tab_volumes = self.tab_volumes()

        tab_volumes.table_volumes.row(
            name=volume_name).dropdown_menu.item_default.click()

        tab_volumes.form_edit_volume.field_name.value = new_volume_name
        tab_volumes.form_edit_volume.submit()

        if check:
            self.close_notification('info')
            tab_volumes.table_volumes.row(
                name=new_volume_name).wait_for_presence()

    @pom.timeit('Step')
    def delete_volumes(self, volume_names, check=True):
        """Step to delete volumes."""
        tab_volumes = self.tab_volumes()

        for volume_name in volume_names:
            tab_volumes.table_volumes.row(
                name=volume_name).checkbox.select()

        tab_volumes.button_delete_volumes.click()
        tab_volumes.form_confirm.submit()

        if check:
            self.close_notification('success')
            for volume_name in volume_names:
                tab_volumes.table_volumes.row(
                    name=volume_name).wait_for_absence(EVENT_TIMEOUT)

    @pom.timeit('Step')
    def view_volume(self, volume_name, check=True):
        """Step to view volume."""
        self.tab_volumes().table_volumes.row(
            name=volume_name).link_volume.click()

        if check:
            assert self.app.page_volume.info_volume.label_name.value \
                == volume_name

    @pom.timeit('Step')
    def change_volume_type(self, volume_name, volume_type=None, check=True):
        """Step to change volume type."""
        tab_volumes = self.tab_volumes()

        with tab_volumes.table_volumes.row(
                name=volume_name).dropdown_menu as menu:
            menu.button_toggle.click()
            menu.item_change_volume_type.click()

        with tab_volumes.form_change_volume_type as form:
            if not volume_type:
                volume_type = form.combobox_volume_type.values[-1]
            form.combobox_volume_type.value = volume_type
            form.submit()

        if check:
            self.close_notification('info')
            tab_volumes.table_volumes.row(
                name=volume_name, type=volume_type).wait_for_presence()

    @pom.timeit('Step')
    def upload_volume_to_image(self, volume_name, image_name, check=True):
        """Step to upload volume to image."""
        tab_volumes = self.tab_volumes()

        with tab_volumes.table_volumes.row(
                name=volume_name).dropdown_menu as menu:
            menu.button_toggle.click()
            menu.item_upload_to_image.click()

        with tab_volumes.form_upload_to_image as form:
            form.field_image_name.value = image_name
            form.submit()

        if check:
            self.close_notification('info')
            tab_volumes.table_volumes.row(
                name=volume_name).wait_for_status('Available')

    @pom.timeit('Step')
    def extend_volume(self, volume_name, new_size=2, check=True):
        """Step to extend volume size."""
        tab_volumes = self.tab_volumes()

        with tab_volumes.table_volumes.row(
                name=volume_name).dropdown_menu as menu:
            menu.button_toggle.click()
            menu.item_extend_volume.click()

        with tab_volumes.form_extend_volume as form:
            form.field_new_size.value = new_size
            form.submit()

        if check:
            self.close_notification('info')
            tab_volumes.table_volumes.row(
                name=volume_name, size=new_size).wait_for_presence()

    def page_admin_volumes(self):
        """Open admin volumes page if it isn't opened."""
        return self._open(self.app.page_admin_volumes)

    def tab_admin_volumes(self):
        """Open admin volumes tab."""
        with self.page_admin_volumes() as page:
            page.label_volumes.click()
            return page.tab_volumes

    @pom.timeit('Step')
    def change_volume_status(self, volume_name, status=None, check=True):
        """Step to change volume status."""
        tab_volumes = self.tab_admin_volumes()

        with tab_volumes.table_volumes.row(
                name=volume_name).dropdown_menu as menu:
            menu.button_toggle.click()
            menu.item_update_volume_status.click()

        with tab_volumes.form_update_volume_status as form:
            if not status:
                status = form.combobox_status.values[-1]
            form.combobox_status.value = status
            form.submit()

        if check:
            self.close_notification('success')
            tab_volumes.table_volumes.row(
                name=volume_name, status=status).wait_for_presence()

    @pom.timeit('Step')
    def launch_volume_as_instance(self, volume_name, instance_name,
                                  network_name, count=1, check=True):
        """Step to launch volume as instance."""
        tab_volumes = self.tab_volumes()

        with tab_volumes.table_volumes.row(
                name=volume_name).dropdown_menu as menu:
            menu.button_toggle.click()
            menu.item_launch_volume_as_instance.click()

        with tab_volumes.form_launch_instance as form:

            with form.tab_details as tab:
                tab.field_name.value = instance_name
                tab.field_count.value = count

            form.item_flavor.click()
            with form.tab_flavor as tab:
                tab.table_available_flavors.row(
                    name='m1.tiny').button_add.click()

            form.item_network.click()
            with form.tab_network as tab:
                tab.table_available_networks.row(
                    name=network_name).button_add.click()

            form.submit()

    @pom.timeit('Step')
    def attach_instance(self, volume_name, instance_name, check=True):
        """Step to attach instance."""
        tab_volumes = self.tab_volumes()

        with tab_volumes.table_volumes.row(
                name=volume_name).dropdown_menu as menu:
            menu.button_toggle.click()
            menu.item_manage_attachments.click()

        with tab_volumes.form_manage_attachments as form:
            instance_value = next(val for val in form.combobox_instance.values
                                  if instance_name in val)
            form.combobox_instance.value = instance_value
            form.submit()

        if check:
            self.close_notification('info')

            with tab_volumes.table_volumes.row(name=volume_name) as row:
                row.wait_for_status('In-use')
                assert instance_name in row.cell('attached_to').value

    @pom.timeit('Step')
    def detach_instance(self, volume_name, instance_name, check=True):
        """Step to detach instance."""
        tab_volumes = self.tab_volumes()

        with tab_volumes.table_volumes.row(
                name=volume_name).dropdown_menu as menu:
            menu.button_toggle.click()
            menu.item_manage_attachments.click()

        tab_volumes.form_manage_attachments.table_instances.row(
            name=instance_name).detach_volume_button.click()

        tab_volumes.form_confirm.submit()

        if check:
            self.close_notification('success')
            tab_volumes.table_volumes.row(
                name=volume_name).wait_for_status('Available')

    @pom.timeit('Step')
    def create_transfer(self, volume_name, transfer_name, check=True):
        """Step to create transfer."""
        tab_volumes = self.tab_volumes()

        with tab_volumes.table_volumes.row(
                name=volume_name).dropdown_menu as menu:
            menu.button_toggle.click()
            menu.item_create_transfer.click()

        with tab_volumes.form_create_transfer as form:
            form.field_name.value = transfer_name
            form.submit()

        if check:
            self.close_notification('success')

            with self.app.page_volume_transfer.form_transfer_info as form:
                transfer_id = form.field_transfer_id.value
                transfer_key = form.field_transfer_key.value

            self.tab_admin_volumes().table_volumes.row(
                name=volume_name,
                status='awaiting-transfer').wait_for_presence()

            return transfer_id, transfer_key

    @pom.timeit('Step')
    def accept_transfer(self, transfer_id, transfer_key, volume_name,
                        check=True):
        """Step to accept transfer."""
        tab_volumes = self.tab_volumes()

        tab_volumes.button_accept_transfer.click()

        with tab_volumes.form_accept_transfer as form:
            form.field_transfer_id.value = transfer_id
            form.field_transfer_key.value = transfer_key
            form.submit()

        if check:
            self.close_notification('success')
            tab_volumes.table_volumes.row(
                name=volume_name, status='Available').wait_for_presence()

    @pom.timeit('Step')
    def migrate_volume(self, volume_name, new_host=None, check=True):
        """Step to migrate host."""
        tab_volumes = self.tab_admin_volumes()

        with tab_volumes.table_volumes.row(
                name=volume_name).dropdown_menu as menu:
            menu.button_toggle.click()
            menu.item_migrate_volume.click()

        with tab_volumes.form_migrate_volume as form:
            old_host = form.field_current_host.value

            if not new_host:
                new_host = form.combobox_destination_host.values[-1]

            form.combobox_destination_host.value = new_host
            form.submit()

        if check:
            self.close_notification('success')

            tab_volumes.table_volumes.row(
                name=volume_name, host=new_host,
                status='Available').wait_for_presence()

            page_volumes = self.page_admin_volumes()

            def is_old_host_volume_absent():
                page_volumes.refresh()
                page_volumes.label_volumes.click()
                return not page_volumes.tab_volumes.table_volumes.row(
                    name=volume_name, host=old_host).is_present

            wait(is_old_host_volume_absent, timeout_seconds=EVENT_TIMEOUT * 2)

            return old_host, new_host

    def tab_snapshots(self):
        """Open volume snapshots tab."""
        with self.page_volumes() as page:
            page.label_snapshots.click()
            return page.tab_snapshots

    def tab_backups(self):
        """Open volume backups tab."""
        with self.page_volumes() as page:
            page.label_backups.click()
            return page.tab_backups

    @pom.timeit('Step')
    def create_snapshot(self, volume_name, snapshot_name, description=None,
                        check=True):
        """Step to create volume snapshot."""
        tab_volumes = self.tab_volumes()

        with tab_volumes.table_volumes.row(
                name=volume_name).dropdown_menu as menu:
            menu.button_toggle.click()
            menu.item_create_snapshot.click()

        with tab_volumes.form_create_snapshot as form:
            form.field_name.value = snapshot_name
            if description is not None:
                self.field_description.value = description
            form.submit()

        if check:
            self.close_notification('info')
            self.tab_snapshots().table_snapshots.row(
                name=snapshot_name, status='Available').wait_for_presence()

    @pom.timeit('Step')
    def delete_snapshot(self, snapshot_name, check=True):
        """Step to delete volume snapshot."""
        tab_snapshots = self.tab_snapshots()

        with tab_snapshots.table_snapshots.row(
                name=snapshot_name).dropdown_menu as menu:
            menu.button_toggle.click()
            menu.item_delete.click()

        tab_snapshots.form_confirm.submit()

        if check:
            self.close_notification('success')
            tab_snapshots.table_snapshots.row(
                name=snapshot_name).wait_for_absence(EVENT_TIMEOUT)

    @pom.timeit('Step')
    def delete_snapshots(self, snapshot_names, check=True):
        """Step to delete volume snapshots."""
        tab_snapshots = self.tab_snapshots()

        for snapshot_name in snapshot_names:
            tab_snapshots.table_snapshots.row(
                name=snapshot_name).checkbox.select()

        tab_snapshots.button_delete_snapshots.click()
        tab_snapshots.form_confirm.submit()

        if check:
            self.close_notification('success')
            for snapshot_name in snapshot_names:
                tab_snapshots.table_snapshots.row(
                    name=snapshot_name).wait_for_absence(EVENT_TIMEOUT)

    @pom.timeit('Step')
    def update_snapshot(self, snapshot_name, new_snapshot_name,
                        description=None, check=True):
        """Step to update volume snapshot."""
        tab_snapshots = self.tab_snapshots()

        with tab_snapshots.table_snapshots.row(
                name=snapshot_name).dropdown_menu as menu:
            menu.button_toggle.click()
            menu.item_edit.click()

        with tab_snapshots.form_edit_snapshot as form:
            form.field_name.value = new_snapshot_name
            if description is not None:
                form.field_description.value = description
            form.submit()

        if check:
            self.close_notification('info')
            self.tab_snapshots().table_snapshots.row(
                name=new_snapshot_name,
                status='Available').wait_for_presence()

    @pom.timeit('Step')
    def create_volume_from_snapshot(self, snapshot_name, check=True):
        """Step to create volume from spanshot."""
        tab_snapshots = self.tab_snapshots()

        with tab_snapshots.table_snapshots.row(
                name=snapshot_name).dropdown_menu as menu:
            menu.button_toggle.click()
            menu.item_default.click()

        tab_snapshots.form_create_volume.submit()

        if check:
            self.close_notification('info')
            self.tab_volumes().table_volumes.row(
                name=snapshot_name).wait_for_status('Available')

    @pom.timeit('Step')
    def create_backup(self, volume_name, backup_name, description=None,
                      container=None, check=True):
        """Step to create volume backup."""
        tab_volumes = self.tab_volumes()

        with tab_volumes.table_volumes.row(
                name=volume_name).dropdown_menu as menu:
            menu.button_toggle.click()
            menu.item_create_backup.click()

        with tab_volumes.form_create_backup as form:
            form.field_name.value = backup_name

            if description is not None:
                self.field_description.value = description

            if container is not None:
                self.field_container.value = container

            form.submit()

        if check:
            self.close_notification('success')
            self.tab_backups().table_backups.row(
                name=backup_name,
                status='Available').wait_for_presence(EVENT_TIMEOUT)

    @pom.timeit('Step')
    def delete_backups(self, backup_names, check=True):
        """Step to delete volume backups."""
        tab_backups = self.tab_backups()

        for backup_name in backup_names:
            tab_backups.table_backups.row(
                name=backup_name).checkbox.select()

        tab_backups.button_delete_backups.click()
        tab_backups.form_confirm.submit()

        if check:
            self.close_notification('success')
            for backup_name in backup_names:
                tab_backups.table_backups.row(
                    name=backup_name).wait_for_absence(EVENT_TIMEOUT)
