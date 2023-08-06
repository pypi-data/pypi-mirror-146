from bedrockz._imports import *

from bedrockz import format as fmt

IMPORTANT_PATHS = {
    "BROWNIE": Path.home() / ".brownie" / "packages",
    "DEFAULT_ROOT_FILES": ["pyproject.toml", "pyproject.lock", "requirements.txt", "setup.py"],
}


def get_dir(path: Path) -> Path:
    if path.is_dir():
        return path
    return path.parent

def get_cwd(file: Optional[str] = None) -> Path:
    """Get current working directory or passed in file."""
    return Path.cwd() if (not file) else get_dir(Path(file))


def get_root(start: Optional[Path] = None, by_files:list=[]) -> Path:
    """Get root directory of a project by looking for a file in the directory tree."""
    count = 0
    start = get_cwd() if (not start) else start
    current = start
    
    while count < 3:
        opened_fs = open_fs(start.as_posix())
        iterator = list(opened_fs.walk.files(filter=by_files))
        
        if iterator:
            
            relative_file = iterator[0][1:]
            current = (current / relative_file).parent
            break
        count +=1
        current = start.parent
    return current

def get_contract_folders(root: Path) -> list:
    """Get all contract folders in a project."""
    sol_files = get_contract_files(root)
    
    folders = pipe(sol_files, 
                   map(lambda x: get_parent_above("contracts", x)), 
                   unique, 
                   list)
    return folders

def get_parent_above(name: str, path: Path) -> Path:
    """Recursively look for the level above a parent folder with a given name."""
    return path.parent if (name == path.parts[-1]) else get_parent_above(name, path.parent)
    
def get_contract_files(root: Path) -> Iterable[Path]:
    """Get all contract files in a project."""
    sol_files = root.glob("**/contracts/**/*.sol")
    return sol_files

def force_exist(path: Path) -> Path:
    if not path.exists():
        if not path.is_dir():
            path.parent.mkdir(parents=True)
            path.touch(exist_ok=True)
            return path
        path.mkdir(parents=True)
    return path

"""
# Specific Smart Contract Commands Here
---

"""
def get_brownie_pms():
    """Get all brownie packages providers"""
    brownie_packages = get_contract_folders(IMPORTANT_PATHS["BROWNIE"])
    provider_packages: Dict[str, List[Path]] = {}
    for package in brownie_packages:
        parent_name = package.parent.name
        if parent_name not in provider_packages:
            provider_packages[parent_name] = []
        provider_packages[parent_name].append(package)
        # provider_packages[pacekage.parent] = get_contract_files(package)
    return provider_packages




# VSCode File Manipulation

def vscode_config(root: Optional[Path] = None, force: bool=True) -> Path:
    """Get the vscode settings file."""
    root_files = IMPORTANT_PATHS["DEFAULT_ROOT_FILES"]
    root = get_root(by_files=root_files) if (not root) else root # type: ignore
    return force_exist(root / ".vscode" / "settings.json")


def app_folder(name: str, author: str="curious", version: str="0.0.1"):
    return open_fs(f'usercache://{name}:{author}:{version}')


class BrowniePM:
    def __init__(self) -> None:
        self.pkg_set: Dict[str, List[Path]] = keymap(fmt.lowercase, get_brownie_pms())
    
    @property
    def root(self):
        return IMPORTANT_PATHS["BROWNIE"]
    
    
    
    @property
    def groups(self) -> List[str]:
        return list(self.pkg_set.keys())

    @property
    def remapped_dict(self) -> Dict[str, Path]:
        primaries = {}
        for group, packages in self.pkg_set.items():
            primaries[f"@{group}"] = list(sorted(packages, key=lambda x: version.parse(x.name.split("@")[1])))[0]
        return primaries
    @property
    def remappings(self) -> List[str]:
        _remappings = []
        for lib, package in self.remapped_dict.items():
            if lib.startswith("@"):
                _remappings.append(f"{lib}={package.as_posix()}")
                continue
            _remappings.append(f"@{lib}={package.as_posix()}")
        return _remappings
    
# class CacheFS:
#     def __init__(self, name: str):
#         self.name = name
#         self.app_dir = typer.get_app_dir(name)
    
#     def __enter__(self):
        
#         return self
    
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         self    
# class CacheFS:
#     def __init__(self, name: str):
#         self.name = name
#         self.app_dir = typer.get_app_dir(name)
    
#     def __enter__(self):
        
#         return self
    
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         self
     

def main():
    brownie_pms = get_brownie_pms()
    # get_contract_folders(IMPORTANT_PATHS["BROWNIE"])
    map(lambda x: x.relative_to(), brownie_pms)
    logger.info(brownie_pms)

if __name__ == "__main__":
    main()
