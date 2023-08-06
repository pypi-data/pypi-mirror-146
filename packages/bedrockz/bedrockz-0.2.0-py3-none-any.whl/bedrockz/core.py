
from bedrockz._imports import *


def _type_match(type_tuple: Tuple[Any, Any]) -> bool:
    
    if len(type_tuple) < 2:
        return True
    
    t1, t2 = type_tuple
    return (
            type(t1) == type(t2)
            or isinstance(t2, type(t1)) 
            or isinstance(t1, type(t2))
            )

def merge_fn(val_list: List[Any]):
    list_set = orjson.loads(orjson.dumps(val_list))
    if not val_list:
        raise ValueError("No values to compare")
    type_list = pipe(val_list, 
                     partition_all(2), 
                     map(_type_match), 
                     filter(lambda x: not bool(x)), 
                     filter(lambda x: x is not None), 
                     list)
    
    
    if not type_list:
        if isinstance(list_set[0], list):
            return concat(list_set)
        if isinstance(list_set[0], dict):
            return merge(*list_set)
        if all(list_set[0] == val for val in list_set):
            return list_set[0]
        return list(val_list)
    
    grouped = pipe(val_list, groupby(lambda x: type(x).name), valmap(lambda x: x[0] if isinstance(x[0], list) else x))


    return grouped


def convert_dict(box_base: Box):
    jsonified = box_base.to_json()
    resp = orjson.loads(jsonified)
    

    return resp
            
def automerge(
    dict1: Union[Box, BoxList, Dict],
    dict2: Union[Box, BoxList, Dict],
) -> Dict[str, Any]:
    """Append a value to a dict."""
    compare_box = None
    merge_box = None
    
    if isinstance(dict1, (Box)):
        compare_box = convert_dict(dict1)
    if isinstance(dict2, (Box)):
        merge_box = convert_dict(dict2)

    merged = merge_with(merge_fn, compare_box, merge_box)
    return merged



# def 


# def name():
#     pass

# import addict
# from loguru import logger
# from matplotlib.pyplot import title
# import networkx as nx
# from addict import Addict as DDict
# from auto_all import end_all
# from auto_all import start_all
# from toolz import curry
# from mako.lookup import TemplateLookup
# from pydantic import BaseModel
# from pydantic import root_validator
# from pydantic import validate_arguments
# from sqlalchemy.engine.base import Engine
# from sqlalchemy.sql import ClauseElement
# from retworkx.visualization import graphviz_draw
# from contextlib import contextmanager

# _T = TypeVar("_T")


# FOLDER_PATH = Path(__file__).parent
# MAKO_LOOPUP = TemplateLookup(
#     directories=[(FOLDER_PATH / "templates"), (FOLDER_PATH / "service")],
#     output_encoding="utf-8",
#     encoding_errors="replace",
# )

# start_all(globals())


# def singleton(cls):
#     instance = [None]

#     def wrapper(*args, **kwargs):
#         if instance[0] is None:
#             instance[0] = cls(*args, **kwargs)
#         return instance[0]

#     return wrapper


# @singleton
# class DynamicGlobalMap(addict.Dict):
#     pass


# def consistent_naming(name: str) -> str:
#     return underscore(parameterize(name))


# def consistent_classes(name: str) -> str:
#     return camelize(underscore(name))


# def consistent_table(name: str) -> str:
#     return titleize(parameterize(name))


# @validate_arguments
# def int_sect(a: set, b: set) -> set:
#     """Get the intersection of a and b sets.

#     Args:
#         a (set): Set we're getting from.
#         b (set): Set we're trying to exclude.

#     Returns:
#         set: [description]
#     """
#     return set(a) & set(b)


# @validate_arguments
# def get_common(a: set, b: set) -> set:
#     """Get the intersection of a and b sets.

#     Args:
#         a (set): Set we're getting from.
#         b (set): Set we're trying to exclude.

#     Returns:
#         set: [description]
#     """
#     return set(a) & set(b)


# @validate_arguments
# def sym_diff(a: set, b: set) -> set:
#     return a.symmetric_difference(b)


# @curry
# def in_set(posts: Iterable[Any], item: Any) -> bool:
#     return item in posts


# @lru_cache
# def make_cache(node_json: str):
#     return hashlib.md5(node_json).hexdigest()  # type: ignore


# # ----------------------------------------------------------------
# #                        SQL Utils
# # ----------------------------------------------------------------

# # from sqlalchemy.sql.expression import Vis


# @curry
# def execute(statement: ClauseElement, engine: Engine):
#     return engine.execute(statement)


# # ----------------------------------------------------------------
# #                        NetworkX Shit
# # ----------------------------------------------------------------


# def bfs_preds(G: nx.Graph, source, depth_limit=None):
#     return nx.bfs_predecessors(G, source=source, depth_limit=depth_limit)


# def template_by_name(name: str):
#     return MAKO_LOOPUP.get_template(name)


# import orjson
# import xxhash


# class hashabledict(dict):
#     def __hash__(self):
#         x = xxhash.xxh32()
#         x.update(
#             orjson.dumps(self, option=orjson.OPT_NON_STR_KEYS | orjson.OPT_SORT_KEYS)
#         )
#         return x.intdigest()


# class InsertParameters(BaseModel):
#     data: Dict[str, Any]
#     event_at: datetime = datetime.now()
#     bucket: Optional[str]
#     tags: Dict[str, Any] = {}

#     @root_validator
#     def check_bucket(cls, values: dict):
#         doti = DDict(**values)
#         buck = doti.bucket
#         if buck:
#             doti.bucket = tableize(buck)
#             return doti.to_dict()

#         if "bucket" not in doti.data.keys():
#             raise ValueError("Bucket not added.")

#         nested_bucket = doti.data.bucket
#         if not isinstance(nested_bucket, str):
#             raise TypeError(
#                 "A bucket was found in 'data' but it wasn't the right type."
#             )
#         doti.data.pop("bucket", None)

#         doti.bucket = str(nested_bucket)
#         return doti.to_dict()


# def hexid() -> str:
#     return uuid.uuid4().hex[:5]


# def create_token():
#     pass


# def __dataclass_transform__(
#     *,
#     eq_default: bool = True,
#     order_default: bool = False,
#     kw_only_default: bool = False,
#     field_descriptors: Tuple[Union[type, Callable[..., Any]], ...] = (()),
# ) -> Callable[[_T], _T]:
#     return lambda a: a


# def graphviz_show(
#     graph,
#     node_attr_fn=None,
#     edge_attr_fn=None,
#     graph_attr=None,
#     filename: Optional[str] = None,
#     image_type=None,
#     method=None,
# ):
#     drawing = graphviz_draw(
#         graph, node_attr_fn, edge_attr_fn, graph_attr, method=method
#     )

#     if drawing is None:
#         logger.info(
#             "There was some error with drawing the graph. Empty response returned."
#         )

#         return
#     drawing.show(title=(filename.split(".")[0] if filename else "A Graph Image"))


# def is_list(value):
#     return isinstance(value, list)


# def listify(value: Union[Any, List[Any]]) -> List[Any]:
#     if not is_list(value):
#         return [value]
#     return value


# def first_key(d: dict) -> Union[str, int]:
#     return next(iter(d))


# end_all(globals())
