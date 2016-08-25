"""
Fixtures for flavors.

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

from mcp_tests.horizon.steps import FlavorsSteps

from mcp_tests.horizon.utils import AttrDict, generate_ids

__all__ = [
    'create_flavor',
    'create_flavors',
    'flavor',
    'flavors_steps'
]


@pytest.fixture
def flavors_steps(login, horizon):
    """Fixture to get flavors steps."""
    return FlavorsSteps(horizon)


@pytest.yield_fixture
def create_flavors(flavors_steps, horizon):
    """Fixture to create flavors with options.

    Can be called several times during test.
    """
    flavors = []

    def _create_flavors(*flavor_names):
        _flavors = []

        for flavor_name in flavor_names:
            flavors_steps.create_flavor(flavor_name)
            flavor = AttrDict(name=flavor_name)

            flavors.append(flavor)
            _flavors.append(flavor)

        return _flavors

    yield _create_flavors

    if flavors:
        flavors_steps.delete_flavors([flavor.name for flavor in flavors])


@pytest.yield_fixture
def create_flavor(flavors_steps):
    """Fixture to create flavor with options.

    Can be called several times during test.
    """
    flavors = []

    def _create_flavor(flavor_name):
        flavors_steps.create_flavor(flavor_name)
        flavor = AttrDict(name=flavor_name)
        flavors.append(flavor)
        return flavor

    yield _create_flavor

    for flavor in flavors:
        flavors_steps.delete_flavor(flavor.name)


@pytest.fixture
def flavor(create_flavor):
    """Fixture to create flavor with default options before test."""
    flavor_name = next(generate_ids('flavor'))
    return create_flavor(flavor_name)
