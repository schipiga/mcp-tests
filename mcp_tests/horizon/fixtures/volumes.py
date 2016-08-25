"""
Fixtures for volumes.

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

import pytest
from waiting import wait

from mcp_tests.horizon.config import EVENT_TIMEOUT
from mcp_tests.horizon.steps import VolumesSteps

from mcp_tests.horizon.utils import AttrDict, generate_ids

__all__ = [
    'create_backups',
    'create_snapshot',
    'create_snapshots',
    'create_volume',
    'create_volumes',
    'snapshot',
    'volume',
    'volumes_steps'
]


@pytest.fixture
def volumes_steps(login, horizon):
    """Fixture to get volumes steps."""
    return VolumesSteps(horizon)


@pytest.yield_fixture
def create_volumes(volumes_steps):
    """Fixture to create volumes with options.

    Can be called several times during test.
    """
    volumes = []

    def _create_volumes(volume_names):
        _volumes = []

        for volume_name in volume_names:
            volumes_steps.create_volume(volume_name, check=False)
            volumes_steps.close_notification('info')
            volume = AttrDict(name=volume_name)

            volumes.append(volume)
            _volumes.append(volume)

        tab_volumes = volumes_steps.tab_volumes()
        for volume_name in volume_names:
            tab_volumes.table_volumes.row(
                name=volume_name).wait_for_status('Available')

        return _volumes

    yield _create_volumes

    if volumes:
        volumes_steps.delete_volumes([volume.name for volume in volumes])


@pytest.yield_fixture
def create_volume(volumes_steps):
    """Fixture to create volume with options.

    Can be called several times during test.
    """
    volumes = []

    def _create_volume(volume_name, volume_type=''):
        volumes_steps.create_volume(volume_name, volume_type=volume_type)
        volume = AttrDict(name=volume_name)
        volumes.append(volume)
        return volume

    yield _create_volume

    for volume in volumes:
        volumes_steps.delete_volume(volume.name)


@pytest.fixture
def volume(create_volume):
    """Fixture to create volume with default options before test."""
    volume_name = next(generate_ids('volume'))
    return create_volume(volume_name)


@pytest.fixture
def snapshot(create_snapshot):
    """Fixture to create volume snapshot with default options before test."""
    snapshot_name = next(generate_ids('snapshot'))
    return create_snapshot(snapshot_name)


@pytest.yield_fixture
def create_snapshots(volume, volumes_steps):
    """Callable fixture to create volume snapshots with options.

    Can be called several times during test.
    """
    snapshots = []

    def _create_snapshots(snapshot_names):
        _snapshots = []

        for snapshot_name in snapshot_names:
            volumes_steps.create_snapshot(volume.name, snapshot_name,
                                          check=False)
            volumes_steps.close_notification('info')
            snapshot = AttrDict(name=snapshot_name)

            snapshots.append(snapshot)
            _snapshots.append(snapshot)

        tab_snapshots = volumes_steps.tab_snapshots()
        for snapshot_name in snapshot_names:
            tab_snapshots.table_snapshots.row(
                name=snapshot_name, status='Available').wait_for_presence(30)

        return _snapshots

    yield _create_snapshots

    if snapshots:
        volumes_steps.delete_snapshots(
            [snapshot.name for snapshot in snapshots])


@pytest.yield_fixture
def create_snapshot(volume, volumes_steps):
    """Callable fixture to create snapshot with options.

    Can be called several times during test.
    """
    snapshots = []

    def _create_snapshot(snapshot_name):
        volumes_steps.create_snapshot(volume.name, snapshot_name)
        snapshot = AttrDict(name=snapshot_name)
        snapshots.append(snapshot)
        return snapshot

    yield _create_snapshot

    for snapshot in snapshots:
        volumes_steps.delete_snapshot(snapshot.name)


@pytest.yield_fixture
def create_backups(volume, volumes_steps):
    """Callable fixture to create backups with options.

    Can be called several times during test.
    """
    backups = []

    def _create_backups(backup_names):
        _backups = []

        for backup_name in backup_names:
            volumes_steps.create_backup(volume.name, backup_name)
            backup = AttrDict(name=backup_name)

            backups.append(backup)
            _backups.append(backup)

        return _backups

    yield _create_backups

    if backups:
        volumes_steps.delete_backups([b.name for b in backups])
