# isort: off

from auto_all import start_all, end_all

start_all(globals())
# isort: on
import itertools
import uuid
from contextlib import asynccontextmanager
from pathlib import Path
from typing import (Any, Callable, Dict, Iterable, List, Optional, Tuple,
                    TypeVar, Union)

import fs
import orjson
import typer
from anyio import Path as AioPath
from anyio import run
from box import Box, BoxList
from cytoolz.curried import (concat, filter, groupby, itemfilter, itemmap,
                             keyfilter, keymap, map, merge, merge_with,
                             partition_all, pipe, unique, valfilter, valmap)
from forbiddenfruit import curse
from fs import open_fs
from inflection import camelize, parameterize, tableize, titleize, underscore
from loguru import logger
from packaging import version

# isort: off



def type_name(self):
    return self.__name__

curse(type, "name", property(type_name))

end_all(globals())

# isort: on
