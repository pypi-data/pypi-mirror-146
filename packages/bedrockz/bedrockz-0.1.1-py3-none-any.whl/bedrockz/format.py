import uuid
from typing import (Any, Callable, Dict, Iterable, List, Optional, Tuple,
                    TypeVar, Union)

from inflection import camelize, parameterize, tableize, titleize, underscore



    


def snake_case(name: str) -> str:
    return underscore(name.strip().replace(" ", "_")).lower()

def lowercase(name: str) -> str:
    return name.strip().replace(" ", "").lower()