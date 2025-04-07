# Copyright 2018 Dirk Thomas
# Licensed under the Apache License, Version 2.0

from pathlib import Path

from colcon_core.environment import EnvironmentExtensionPoint
from colcon_core.environment import logger
from colcon_core.plugin_system import satisfies_version
from colcon_core.shell import create_environment_hook


class PkgConfigEnvironment(EnvironmentExtensionPoint):
    """
    Extend the environment variable PKG_CONFIG_PATH.

    A package needs to provide files 'lib/pkgconfig/*.pc' or
    'share/pkgconfig/*.pc' to extend the environment variable.
    """

    def __init__(self):  # noqa: D107
        super().__init__()
        satisfies_version(
            EnvironmentExtensionPoint.EXTENSION_POINT_VERSION, '^1.0')

    def create_environment_hooks(self, prefix_path, pkg_name):  # noqa: D102
        environment_hooks = []
        subdirectories = [Path('share') / 'pkgconfig'] \
            + [(p / 'pkgconfig').relative_to(prefix_path)
               for p in prefix_path.glob('lib*')]
        for subdirectory in subdirectories:
            full_pkgconfig_path = prefix_path / subdirectory
            logger.log(1, "checking '%s' for .pc files" % full_pkgconfig_path)
            if any(full_pkgconfig_path.glob('*.pc')):
                environment_hooks += create_environment_hook(
                    'pkg_config_%s' % subdirectory.parent.name,
                    prefix_path, pkg_name, 'PKG_CONFIG_PATH',
                    str(subdirectory), mode='prepend')
        return environment_hooks
