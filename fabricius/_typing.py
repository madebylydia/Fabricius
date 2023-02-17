"""
Copy of the typing.py library from the CPython repository.
All credits goes to the Python Software Foundation (PSF)
Copyright © 2001-2023 Python Software Foundation; All Rights Reserved

Copied to reflect changes of https://github.com/python/cpython/pull/31628
"""


import collections
import collections.abc
import contextlib
import functools
import sys
from abc import ABCMeta

__all__ = ["Generic", "Protocol"]


_PROTO_ALLOWLIST = {
    "collections.abc": [
        "Callable",
        "Awaitable",
        "Iterable",
        "Iterator",
        "AsyncIterable",
        "Hashable",
        "Sized",
        "Container",
        "Collection",
        "Reversible",
    ],
    "contextlib": ["AbstractContextManager", "AbstractAsyncContextManager"],
}


_cleanups = []
_caches = {}


def _tp_cache(func=None, /, *, typed=False):
    """Internal wrapper caching __getitem__ of generic types with a fallback to
    original function for non-hashable arguments.
    """

    def decorator(func):
        # The callback 'inner' references the newly created lru_cache
        # indirectly by performing a lookup in the global '_caches' dictionary.
        # This breaks a reference that can be problematic when combined with
        # C API extensions that leak references to types. See GH-98253.

        cache = functools.lru_cache(typed=typed)(func)
        _caches[func] = cache
        _cleanups.append(cache.cache_clear)
        del cache

        @functools.wraps(func)
        def inner(*args, **kwds):
            with contextlib.suppress(TypeError):
                return _caches[func](*args, **kwds)
            return func(*args, **kwds)

        return inner

    return decorator(func) if func is not None else decorator


def _caller(depth=1, default="__main__"):
    with contextlib.suppress(AttributeError):
        return sys._getframemodulename(depth + 1) or default
    with contextlib.suppress(AttributeError, ValueError):
        return sys._getframe(depth + 1).f_globals.get("__name__", default)
    return None


def _allow_reckless_class_checks(depth=3):
    """Allow instance and class checks for special stdlib modules.
    The abc and functools modules indiscriminately call isinstance() and
    issubclass() on the whole MRO of a user class, which may contain protocols.
    """
    return _caller(depth) in {"abc", "functools", None}


def _get_protocol_attrs(cls):
    """Collect protocol members from a protocol class objects.
    This includes names actually defined in the class dictionary, as well
    as names that appear in annotations. Special names (above) are skipped.
    """
    attrs = set()
    for base in cls.__mro__[:-1]:  # without object
        if base.__name__ in ("Protocol", "Generic"):
            continue
        annotations = getattr(base, "__annotations__", {})
        for attr in list(base.__dict__.keys()) + list(annotations.keys()):
            if not attr.startswith("_abc_") and attr not in EXCLUDED_ATTRIBUTES:
                attrs.add(attr)
    return attrs


def _is_callable_members_only(cls):
    # PEP 544 prohibits using issubclass() with protocols that have non-method members.
    return all(callable(getattr(cls, attr, None)) for attr in _get_protocol_attrs(cls))


def _no_init_or_replace_init(self, *args, **kwargs):
    cls = type(self)

    if cls._is_protocol:
        raise TypeError("Protocols cannot be instantiated")

    # Already using a custom `__init__`. No need to calculate correct
    # `__init__` to call. This can lead to RecursionError. See bpo-45121.
    if cls.__init__ is not _no_init_or_replace_init:
        return

    # Initially, `__init__` of a protocol subclass is set to `_no_init_or_replace_init`.
    # The first instantiation of the subclass will call `_no_init_or_replace_init` which
    # searches for a proper new `__init__` in the MRO. The new `__init__`
    # replaces the subclass' old `__init__` (ie `_no_init_or_replace_init`). Subsequent
    # instantiation of the protocol subclass will thus use the new
    # `__init__` and no longer call `_no_init_or_replace_init`.
    for base in cls.__mro__:
        init = base.__dict__.get("__init__", _no_init_or_replace_init)
        if init is not _no_init_or_replace_init:
            cls.__init__ = init
            break
    else:
        # should not happen
        cls.__init__ = object.__init__

    cls.__init__(self, *args, **kwargs)


class Generic:
    """Abstract base class for generic types.
    A generic type is typically declared by inheriting from
    this class parameterized with one or more type variables.
    For example, a generic mapping type might be defined as::
      class Mapping(Generic[KT, VT]):
          def __getitem__(self, key: KT) -> VT:
              ...
          # Etc.
    This class can then be used as follows::
      def lookup_name(mapping: Mapping[KT, VT], key: KT, default: VT) -> VT:
          try:
              return mapping[key]
          except KeyError:
              return default
    """

    __slots__ = ()
    _is_protocol = False

    @_tp_cache
    def __class_getitem__(cls, params):
        """Parameterizes a generic class.
        At least, parameterizing a generic class is the *main* thing this method
        does. For example, for some generic class `Foo`, this is called when we
        do `Foo[int]` - there, with `cls=Foo` and `params=int`.
        However, note that this method is also called when defining generic
        classes in the first place with `class Foo(Generic[T]): ...`.
        """
        if not isinstance(params, tuple):
            params = (params,)

        params = tuple(_type_convert(p) for p in params)
        if cls in (Generic, Protocol):
            # Generic and Protocol can only be subscripted with unique type variables.
            if not params:
                raise TypeError(f"Parameter list to {cls.__qualname__}[...] cannot be empty")
            if not all(_is_typevar_like(p) for p in params):
                raise TypeError(
                    f"Parameters to {cls.__name__}[...] must all be type variables "
                    f"or parameter specification variables."
                )
            if len(set(params)) != len(params):
                raise TypeError(f"Parameters to {cls.__name__}[...] must all be unique")
        else:
            # Subscripting a regular Generic subclass.
            for param in cls.__parameters__:
                prepare = getattr(param, "__typing_prepare_subst__", None)
                if prepare is not None:
                    params = prepare(cls, params)
            _check_generic(cls, params, len(cls.__parameters__))

            new_args = []
            for param, new_arg in zip(cls.__parameters__, params):
                if isinstance(param, TypeVarTuple):
                    new_args.extend(new_arg)
                else:
                    new_args.append(new_arg)
            params = tuple(new_args)

        return _GenericAlias(cls, params, _paramspec_tvars=True)

    def __init_subclass__(cls, *args, **kwargs):
        super().__init_subclass__(*args, **kwargs)
        tvars = []
        if "__orig_bases__" in cls.__dict__:
            error = Generic in cls.__orig_bases__
        else:
            error = (
                Generic in cls.__bases__
                and cls.__name__ != "Protocol"
                and type(cls) != _TypedDictMeta
            )
        if error:
            raise TypeError("Cannot inherit from plain Generic")
        if "__orig_bases__" in cls.__dict__:
            tvars = _collect_parameters(cls.__orig_bases__)
            # Look for Generic[T1, ..., Tn].
            # If found, tvars must be a subset of it.
            # If not found, tvars is it.
            # Also check for and reject plain Generic,
            # and reject multiple Generic[...].
            gvars = None
            for base in cls.__orig_bases__:
                if isinstance(base, _GenericAlias) and base.__origin__ is Generic:
                    if gvars is not None:
                        raise TypeError("Cannot inherit from Generic[...] multiple types.")
                    gvars = base.__parameters__
            if gvars is not None:
                tvarset = set(tvars)
                gvarset = set(gvars)
                if not tvarset <= gvarset:
                    s_vars = ", ".join(str(t) for t in tvars if t not in gvarset)
                    s_args = ", ".join(str(g) for g in gvars)
                    raise TypeError(
                        f"Some type variables ({s_vars}) are" f" not listed in Generic[{s_args}]"
                    )
                tvars = gvars
        cls.__parameters__ = tuple(tvars)


class _ProtocolMeta(ABCMeta):
    # This metaclass is really unfortunate and exists only because of
    # the lack of __instancehook__.
    def __instancecheck__(cls, instance):
        # We need this method for situations where attributes are
        # assigned in __init__.
        if (
            getattr(cls, "_is_protocol", False)
            and not getattr(cls, "_is_runtime_protocol", False)
            and not _allow_reckless_class_checks(depth=2)
        ):
            raise TypeError(
                "Instance and class checks can only be used with" " @runtime_checkable protocols"
            )

        if (
            not getattr(cls, "_is_protocol", False) or _is_callable_members_only(cls)
        ) and issubclass(instance.__class__, cls):
            return True
        if cls._is_protocol and all(
            hasattr(instance, attr) and
            # All *methods* can be blocked by setting them to None.
            (not callable(getattr(cls, attr, None)) or getattr(instance, attr) is not None)
            for attr in _get_protocol_attrs(cls)
        ):
            return True
        return super().__instancecheck__(instance)


class Protocol(Generic, metaclass=_ProtocolMeta):
    """Base class for protocol classes.

    Protocol classes are defined as::

        class Proto(Protocol):
            def meth(self) -> int:
                ...

    Such classes are primarily used with static type checkers that recognize
    structural subtyping (static duck-typing), for example::

        class C:
            def meth(self) -> int:
                return 0

        def func(x: Proto) -> int:
            return x.meth()

        func(C())  # Passes static type check

    See PEP 544 for details. Protocol classes decorated with
    @typing.runtime_checkable act as simple-minded runtime protocols that check
    only the presence of given attributes, ignoring their type signatures.
    Protocol classes can be generic, they are defined as::

        class GenProto(Protocol[T]):
            def meth(self) -> T:
                ...
    """

    __slots__ = ()
    _is_protocol = True
    _is_runtime_protocol = False

    def __init_subclass__(cls, *args, **kwargs):
        super().__init_subclass__(*args, **kwargs)

        # Determine if this is a protocol or a concrete subclass.
        if not cls.__dict__.get("_is_protocol", False):
            cls._is_protocol = any(b is Protocol for b in cls.__bases__)

        # Set (or override) the protocol subclass hook.
        def _proto_hook(other):
            if not cls.__dict__.get("_is_protocol", False):
                return NotImplemented

            # First, perform various sanity checks.
            if not getattr(cls, "_is_runtime_protocol", False):
                if _allow_reckless_class_checks():
                    return NotImplemented
                raise TypeError(
                    "Instance and class checks can only be used with"
                    " @runtime_checkable protocols"
                )
            if not _is_callable_members_only(cls):
                if _allow_reckless_class_checks():
                    return NotImplemented
                raise TypeError("Protocols with non-method members" " don't support issubclass()")
            if not isinstance(other, type):
                # Same error message as for issubclass(1, int).
                raise TypeError("issubclass() arg 1 must be a class")

            # Second, perform the actual structural compatibility check.
            for attr in _get_protocol_attrs(cls):
                for base in other.__mro__:
                    # Check if the members appears in the class dictionary...
                    if attr in base.__dict__:
                        if base.__dict__[attr] is None:
                            return NotImplemented
                        break

                    # ...or in annotations, if it is a sub-protocol.
                    annotations = getattr(base, "__annotations__", {})
                    if (
                        isinstance(annotations, collections.abc.Mapping)
                        and attr in annotations
                        and issubclass(other, Generic)
                        and other._is_protocol
                    ):
                        break
                else:
                    return NotImplemented
            return True

        if "__subclasshook__" not in cls.__dict__:
            cls.__subclasshook__ = _proto_hook

        # We have nothing more to do for non-protocols...
        if not cls._is_protocol:
            return

        # ... otherwise check consistency of bases, and prohibit instantiation.
        for base in cls.__bases__:
            if not (
                base in (object, Generic)
                or base.__module__ in _PROTO_ALLOWLIST
                and base.__name__ in _PROTO_ALLOWLIST[base.__module__]
                or issubclass(base, Generic)
                and base._is_protocol
            ):
                raise TypeError(
                    "Protocols can only inherit from other" " protocols, got %r" % base
                )
        if cls.__init__ is Protocol.__init__:
            cls.__init__ = _no_init_or_replace_init
