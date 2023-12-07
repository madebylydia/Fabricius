from typing import (
    Any,
    BinaryIO,
    Callable,
    Dict,
    Iterator,
    List,
    Mapping,
    NamedTuple,
    Optional,
    Sequence,
    TextIO,
    Type,
    Union,
)

from _typeshed import Incomplete
from git.cmd import Git
from git.config import GitConfigParser
from git.db import GitCmdObjectDB
from git.index import IndexFile
from git.objects import Commit, Submodule, Tree
from git.refs import HEAD, Head, Reference, TagReference
from git.refs.symbolic import SymbolicReference
from git.remote import Remote
from git.types import (
    TBD,
    Commit_ish,
    ConfigLevels_Tup,
    Lit_config_levels,
    PathLike,
    Tree_ish,
)
from git.util import IterableList
from gitdb.db.loose import LooseObjectDB

from .fun import rev_parse as fun_rev_parse

class BlameEntry(NamedTuple):
    commit: Dict[str, "Commit"]
    linenos: range
    orig_path: Optional[str]
    orig_linenos: range

class Repo:
    DAEMON_EXPORT_FILE: str
    git: Incomplete
    working_dir: PathLike
    git_dir: PathLike
    re_whitespace: Incomplete
    re_hexsha_only: Incomplete
    re_hexsha_shortened: Incomplete
    re_envvars: Incomplete
    re_author_committer_start: Incomplete
    re_tab_full_line: Incomplete
    unsafe_git_clone_options: Incomplete
    config_level: ConfigLevels_Tup
    GitCommandWrapperType = Git
    odb: Incomplete
    def __init__(
        self,
        path: Optional[PathLike] = ...,
        odbt: Type[LooseObjectDB] = ...,
        search_parent_directories: bool = ...,
        expand_vars: bool = ...,
    ) -> None: ...
    def __enter__(self) -> Repo: ...
    def __exit__(self, *args: Any) -> None: ...
    def __del__(self) -> None: ...
    def close(self) -> None: ...
    def __eq__(self, rhs: object) -> bool: ...
    def __ne__(self, rhs: object) -> bool: ...
    def __hash__(self) -> int: ...
    description: Incomplete
    @property
    def working_tree_dir(self) -> Optional[PathLike]: ...
    @property
    def common_dir(self) -> PathLike: ...
    @property
    def bare(self) -> bool: ...
    @property
    def heads(self) -> IterableList[Head]: ...
    @property
    def references(self) -> IterableList[Reference]: ...
    refs = references
    branches = heads
    @property
    def index(self) -> IndexFile: ...
    @property
    def head(self) -> HEAD: ...
    @property
    def remotes(self) -> IterableList[Remote]: ...
    def remote(self, name: str = ...) -> Remote: ...
    @property
    def submodules(self) -> IterableList[Submodule]: ...
    def submodule(self, name: str) -> Submodule: ...
    def create_submodule(self, *args: Any, **kwargs: Any) -> Submodule: ...
    def iter_submodules(self, *args: Any, **kwargs: Any) -> Iterator[Submodule]: ...
    def submodule_update(self, *args: Any, **kwargs: Any) -> Iterator[Submodule]: ...
    @property
    def tags(self) -> IterableList[TagReference]: ...
    def tag(self, path: PathLike) -> TagReference: ...
    def create_head(
        self,
        path: PathLike,
        commit: Union["SymbolicReference", "str"] = ...,
        force: bool = ...,
        logmsg: Optional[str] = ...,
    ) -> Head: ...
    def delete_head(self, *heads: Union[str, Head], **kwargs: Any) -> None: ...
    def create_tag(
        self,
        path: PathLike,
        ref: Union[str, "SymbolicReference"] = ...,
        message: Optional[str] = ...,
        force: bool = ...,
        **kwargs: Any,
    ) -> TagReference: ...
    def delete_tag(self, *tags: TagReference) -> None: ...
    def create_remote(self, name: str, url: str, **kwargs: Any) -> Remote: ...
    def delete_remote(self, remote: Remote) -> str: ...
    def config_reader(
        self, config_level: Optional[Lit_config_levels] = ...
    ) -> GitConfigParser: ...
    def config_writer(self, config_level: Lit_config_levels = ...) -> GitConfigParser: ...
    def commit(self, rev: Union[str, Commit_ish, None] = ...) -> Commit: ...
    def iter_trees(self, *args: Any, **kwargs: Any) -> Iterator["Tree"]: ...
    def tree(self, rev: Union[Tree_ish, str, None] = ...) -> Tree: ...
    def iter_commits(
        self,
        rev: Union[str, Commit, "SymbolicReference", None] = ...,
        paths: Union[PathLike, Sequence[PathLike]] = ...,
        **kwargs: Any,
    ) -> Iterator[Commit]: ...
    def merge_base(self, *rev: TBD, **kwargs: Any) -> List[Union[Commit_ish, None]]: ...
    def is_ancestor(self, ancestor_rev: Commit, rev: Commit) -> bool: ...
    def is_valid_object(self, sha: str, object_type: Union[str, None] = ...) -> bool: ...
    daemon_export: Incomplete
    alternates: Incomplete
    def is_dirty(
        self,
        index: bool = ...,
        working_tree: bool = ...,
        untracked_files: bool = ...,
        submodules: bool = ...,
        path: Optional[PathLike] = ...,
    ) -> bool: ...
    @property
    def untracked_files(self) -> List[str]: ...
    def ignored(self, *paths: PathLike) -> List[str]: ...
    @property
    def active_branch(self) -> Head: ...
    def blame_incremental(
        self, rev: str | HEAD, file: str, **kwargs: Any
    ) -> Iterator["BlameEntry"]: ...
    def blame(
        self,
        rev: Union[str, HEAD],
        file: str,
        incremental: bool = ...,
        rev_opts: Optional[List[str]] = ...,
        **kwargs: Any,
    ) -> List[List[Commit | List[str | bytes] | None]] | Iterator[BlameEntry] | None: ...
    @classmethod
    def init(
        cls,
        path: Union[PathLike, None] = ...,
        mkdir: bool = ...,
        odbt: Type[GitCmdObjectDB] = ...,
        expand_vars: bool = ...,
        **kwargs: Any,
    ) -> Repo: ...
    def clone(
        self,
        path: PathLike,
        progress: Optional[
            Callable[[int, Union[str, float], Union[str, float, None], str], None]
        ] = ...,
        multi_options: Optional[List[str]] = ...,
        allow_unsafe_protocols: bool = ...,
        allow_unsafe_options: bool = ...,
        **kwargs: Any,
    ) -> Repo: ...
    @classmethod
    def clone_from(
        cls,
        url: PathLike,
        to_path: PathLike,
        progress: Optional[
            Callable[[int, Union[str, float], Union[str, float, None], str], None]
        ] = ...,
        env: Optional[Mapping[str, str]] = ...,
        multi_options: Optional[List[str]] = ...,
        allow_unsafe_protocols: bool = ...,
        allow_unsafe_options: bool = ...,
        **kwargs: Any,
    ) -> Repo: ...
    def archive(
        self,
        ostream: Union[TextIO, BinaryIO],
        treeish: Optional[str] = ...,
        prefix: Optional[str] = ...,
        **kwargs: Any,
    ) -> Repo: ...
    def has_separate_working_tree(self) -> bool: ...
    rev_parse = fun_rev_parse
    def currently_rebasing_on(self) -> Commit | None: ...
