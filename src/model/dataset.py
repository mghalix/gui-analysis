from dataclasses import dataclass, field

from ..control.utils.file_utils import CACHE_DIR, get_extension, get_name
from .extension import Extension


# @dataclass(frozen=True)
@dataclass
class Dataset:
    url: str = ""
    name: str = field(init=False)
    ext: Extension = field(init=False)

    def __post_init__(self) -> None:
        # object.__setattr__(self, "name", get_name(self.url))
        # object.__setattr__(self, "ext", get_extension(self.url))
        if self.url == "":
            return

        self.name = get_name(self.url)
        self.ext = get_extension(self.url)

    @property
    def cached_path(self) -> str:
        return CACHE_DIR + self.name + str(self.ext.value)

    @property
    def full_name(self) -> str:
        return self.name + str(self.ext.value)

    @property
    def dir(self) -> str:
        return CACHE_DIR

    def __str__(self) -> str:
        return self.cached_path
