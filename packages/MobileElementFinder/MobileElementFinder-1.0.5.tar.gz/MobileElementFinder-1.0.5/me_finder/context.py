"""Context and configuration."""

import datetime
import os
from configparser import ConfigParser
from typing import List, TextIO

import attr
from mgedb import MGEdb
import logging

LOG = logging.getLogger(__name__)


@attr.s(auto_attribs=True, frozen=True, slots=True)
class ExecutionContext:
    """Manages script execution."""

    output: TextIO
    sample_name: str
    num_threads: int
    kma_path: str
    idx_db_path: str
    blastn_path: str
    makeblastdb_path: str
    config: ConfigParser
    default_config: ConfigParser
    mge_db: MGEdb
    fq_files: List[str]
    base_wd_dir: str
    timestamp: datetime.datetime = datetime.datetime.now()

    def file_path(self, *local_path: str) -> str:
        """Recursivly create directories in working dir."""
        filename = local_path[-1]
        dirname = self.dir_path(*local_path[:-1])
        return os.path.join(dirname, filename)

    def dir_path(self, *local_path: str) -> str:
        """Recursivly create directories in working dir."""
        dir_path: str = os.path.join(self.base_wd_dir, self.sample_name,
                                     *local_path)
        os.makedirs(dir_path, exist_ok=True)
        return dir_path

    def check_path(self, *local_path: str) -> str:
        """Return path to file and verify if file exist."""
        dir_path: str = os.path.join(self.base_wd_dir, self.sample_name,
                                     *local_path[:-1])
        filepath: str = os.path.join(dir_path, local_path[-1])
        if not os.path.isfile(filepath):
            raise FileNotFoundError
        return filepath

    def cnf_get_default(self, func_name: str, *args):
        """Get default configuration from config parser objects."""
        section = args[0]
        if not self.config.has_option(*args):
            cnf = self.default_config
            LOG.warning(f'Section "{section}" not in supplied config file, fallback to default config')
        else:
            cnf = self.config
        f = getattr(cnf, func_name)
        return f(*args)

