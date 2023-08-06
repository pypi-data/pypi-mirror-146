# copyright: (c) 2020 by Jesse Johnson.
# license: LGPL-3.0, see LICENSE.md for more details.
"""Provide configuration for proman."""

import os
from dataclasses import dataclass
from typing import Optional

from compendium.loader import ConfigFile

from . import exception

index_url = 'https://pypi.org'
url_base = 'https://api.github.com'


@dataclass
class Config(ConfigFile):
    """Provide configuration."""

    filepath: str
    index_url: str = url_base
    include_prereleases: bool = False
    digest_algorithm: str = 'sha256'
    lookup_memory: Optional[str] = None
    writable: bool = True

    def __post_init__(self) -> None:
        """Initialize settings from configuration."""
        super().__init__(
            self.filepath,
            writable=self.writable,
            separator='.',
        )
        if os.path.isfile(self.filepath):
            try:
                self.load()
            except Exception:
                raise exception.PromanException('could not load configuration')
