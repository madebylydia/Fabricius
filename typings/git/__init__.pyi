from typing import Optional as Optional

from git.cmd import Git as Git
from git.config import GitConfigParser as GitConfigParser
from git.db import *
from git.diff import *
from git.exc import *
from git.index import *
from git.objects import *
from git.refs import *
from git.remote import *
from git.repo import Repo as Repo
from git.types import PathLike as PathLike
from git.util import Actor as Actor
from git.util import BlockingLockFile as BlockingLockFile
from git.util import LockFile as LockFile
from git.util import Stats as Stats
from git.util import rmtree as rmtree

# Names in __all__ with no definition:
#   AmbiguousObjectName
#   BadName
#   BadObject
#   BadObjectType
#   BaseIndexEntry
#   Blob
#   BlobFilter
#   CacheError
#   CheckoutError
#   CommandError
#   Commit
#   Diff
#   DiffIndex
#   Diffable
#   FetchInfo
#   GitCmdObjectDB
#   GitCommandError
#   GitCommandNotFound
#   GitDB
#   GitError
#   HEAD
#   Head
#   HookExecutionError
#   IndexEntry
#   IndexFile
#   IndexObject
#   InvalidDBRoot
#   InvalidGitRepositoryError
#   List
#   NULL_TREE
#   NoSuchPathError
#   ODBError
#   Object
#   ParseError
#   PushInfo
#   RefLog
#   RefLogEntry
#   Reference
#   Remote
#   RemoteProgress
#   RemoteReference
#   RepositoryDirtyError
#   RootModule
#   RootUpdateProgress
#   Sequence
#   StageType
#   Submodule
#   SymbolicReference
#   TYPE_CHECKING
#   Tag
#   TagObject
#   TagReference
#   Tree
#   TreeModifier
#   Tuple
#   Union
#   UnmergedEntriesError
#   UnsafeOptionError
#   UnsafeProtocolError
#   UnsupportedOperation
#   UpdateProgress
#   WorkTreeRepositoryUnsupported
#   remove_password_if_present
#   safe_decode
#   to_hex_sha
