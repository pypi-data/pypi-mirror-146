from bedrockz._imports import *
from bedrockz.core import merge_fn, automerge
from bedrockz.files import get_root, vscode_config, app_folder


def attach_list(incoming: Union[BoxList, Box], value: Any) -> Union[BoxList , List]:
    """Append a value to a dict."""
    if isinstance(incoming, (BoxList, list)):
        incoming.append(incoming)
        return incoming
    
    return [value]


def attach_dict(incoming: Union[BoxList, Box], value: Dict[str, Any]) -> Union[BoxList , List]:
    """Append a value to a dict."""
    if not isinstance(incoming, (Box, Dict)):
        
        incoming.append(incoming)
        return incoming
    
    return [value]


async def to_box(value: Union[str, bytes]) -> dict:
    """Get a default dict."""
    value = {} if not value else orjson.loads(value) # type: ignore
    
    return Box(value, default_box=True)


@asynccontextmanager
async def get_config(path: Path):
    apath = AioPath(path)
    json_box = Box({}, default_box=True)
    try:
        file_str = await apath.read_bytes()
        json_box = await to_box(file_str) # type: ignore
        yield json_box

    finally:
        await apath.write_text(orjson.dumps(json_box.to_dict()).decode("utf-8"))
    


async def main():
    async with get_config(vscode_config()) as bdd:
        b1 = bdd.copy()
        b2 = bdd.copy()
        b1.hello = [1, 2]
        b2.hello = [3, 4]
        # merge_fn([b1, b2])
        
        b3 = bdd.copy()
        b4 = bdd.copy()
        
        b3.hello = [1, 2]
        b4.hello = ""
        # merged = merge_fn([b3, b4])
        merged = automerge(b3, b4)
        logger.info(merged)
        

if __name__ == "__main__":
    run(main)


