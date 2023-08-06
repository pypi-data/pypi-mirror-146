""" Checks PyPi for version updates """

from __future__ import annotations

import sys
import textwrap
import time
from datetime import datetime, timedelta
from typing import NamedTuple

import requests

from mcli import config, version
from mcli.config import FeatureFlag, MCLIConfig


class Version(NamedTuple):
    """ An Easier to work with Version Encapsulation"""
    major: int
    minor: int
    patch: int
    extras: str = ''

    def __lt__(self, o: object) -> bool:
        assert isinstance(o, Version)
        if self.major != o.major:
            return self.major < o.major
        if self.minor != o.minor:
            return self.minor < o.minor
        if self.patch != o.patch:
            return self.patch < o.patch
        if self.extras and not o.extras:
            return True
        if not self.extras and o.extras:
            return False

        if self.extras and o.extras:
            # alphas check
            # TODO: maybe more version semantics but for now lets only support alphas
            try:
                return int(self.extras.split('a')[1]) < int(o.extras.split('a')[1])
            # pylint: disable-next=bare-except
            except:
                return True
        return False

    def __eq__(self, o: object) -> bool:
        assert isinstance(o, Version)
        return self.major == o.major \
            and  self.minor == o.minor \
            and self.patch == o.patch \
            and self.extras == o.extras

    @classmethod
    def from_string(cls, text: str) -> Version:
        """Parses a semantic version of the form X.Y.Z[a0-9*]?

        Does not use `v` prefix and only supports optional alpha version tags

        Args:
            text: The text to parse

        Returns:
            Returns a Version object
        """
        text = text.lstrip('v')
        major, minor, patch = text.split('.')
        extras = ''
        if not patch.isdigit():
            if 'a' in patch:
                extras = patch[patch.index('a'):]
                patch = patch[:patch.index('a')]
        return Version(
            major=int(major),
            minor=int(minor),
            patch=int(patch),
            extras=extras,
        )

    def __str__(self) -> str:
        return f'v{self.major}.{self.minor}.{self.patch}{self.extras}'


current_version = Version(
    major=version.__version_major__,
    minor=version.__version_minor__,
    patch=version.__version_patch__,
    extras=version.__version_extras__,
)


def get_latest_mcli_version() -> Version:
    try:
        r = requests.get('https://pypi.org/pypi/mosaicml-cli/json').json()
        version_number = r.get('info', {}).get('version', None)
        return Version.from_string(version_number)
    except:  # pylint: disable=bare-except
        return current_version


def get_latest_alpha_mcli_version() -> Version:
    try:
        r = requests.get('https://pypi.org/pypi/mosaicml-cli/json').json()
        version_numbers = r.get('releases', {}).keys()
        all_versions = sorted([Version.from_string(x) for x in version_numbers], reverse=True)
        return all_versions[0]
    except:  # pylint: disable=bare-except
        return current_version


# pylint: disable-next=too-many-statements
def check_new_update_available() -> None:
    try:
        conf = MCLIConfig.load_config()
    except Exception:  # pylint: disable=broad-except
        return
    last_update_time_days = (datetime.now() - conf.last_update_check).total_seconds() / (60 * 60 * 24)
    update_check_days = config.UPDATE_CHECK_FREQUENCY_DAYS
    if conf.feature_enabled(FeatureFlag.ALPHA_TESTER):
        update_check_days = 2.0 / 24.0
    if last_update_time_days < update_check_days or conf.dev_mode:
        if conf.dev_mode:
            print('DEV: Skipping update check')
        # Skipping check
        return

    print('Checking for new MCLI updates')
    conf.last_update_check = datetime.now()
    if conf.feature_enabled(FeatureFlag.ALPHA_TESTER):
        latest_version = get_latest_alpha_mcli_version()
    else:
        latest_version = get_latest_mcli_version()
        # The case where they are on a prerelease but without being an alpha tester
        if current_version > latest_version:
            print('MCLI Version up to date! Prerelease found!\n')
            conf.save_config()
            return

    if current_version != latest_version:
        print('New Version of MCLI detected\n')
        print('-' * 30)
        print(f'Local version: \t\t{current_version}')
        print(f'Most Recent version: \t{latest_version}')
        print('-' * 30 + '\n')
        if conf.feature_enabled(FeatureFlag.ALPHA_TESTER):
            print('Thanks for being an Alpha tester!')
    else:
        print('MCLI Version up to date!\n')

    version_upgrade_message = 'pip install --upgrade mosaicml-cli'
    if conf.feature_enabled(FeatureFlag.ALPHA_TESTER):
        version_upgrade_message = f"pip install mosaicml-cli={str( latest_version ).replace('v','')}"
    version_update_required_message = textwrap.dedent(f"""
    Please update your mcli version to continue using mcli
    To do so, run:

    {version_upgrade_message}
    """)

    if conf.feature_enabled(FeatureFlag.ALPHA_TESTER):
        print(version_update_required_message)
        conf.last_update_check = datetime.now() - timedelta(days=config.UPDATE_CHECK_FREQUENCY_DAYS, minutes=-120)
        print('This message will repeat every hour if you ignore it')
        conf.save_config()
        time.sleep(1)
        sys.exit(1)

    if current_version.major != latest_version.major:
        print('Major version out of sync.')
        print(version_update_required_message)
        sys.exit(1)

    if current_version.minor != latest_version.minor:
        print('Minor version out of sync.')
        print(version_update_required_message)
        sys.exit(1)

    if latest_version.patch - current_version.patch >= 2:
        print('Patch version >= 2 versions out of date.')
        print(version_update_required_message)
        sys.exit(1)

    if latest_version.patch != current_version.patch:
        print('Patch version out of date.')
        print(
            textwrap.dedent(f"""
        You can continue, but we recommend updating mcli ASAP
        This message will reset every two hours

        To update mcli run:

        {version_upgrade_message}

        Ctrl-c to exit and update now
        """))
        time.sleep(5)
        conf.last_update_check = datetime.now() - timedelta(days=config.UPDATE_CHECK_FREQUENCY_DAYS, minutes=-120)

    conf.save_config()
