import collections.abc
import functools
import typing

import click

from fabricius.app.config import Config


def pass_config[
    **Func, Return
](
    function: collections.abc.Callable[typing.Concatenate["Config", Func], Return]
) -> collections.abc.Callable[Func, Return]:
    @click.pass_context
    def wrapper(ctx: click.Context, *args: Func.args, **kwargs: Func.kwargs) -> Return:
        # Typehinting by shadowing an any type, damn, what a smartass I am.
        return ctx.invoke(function, ctx.obj["config"], *args, **kwargs)

    return functools.update_wrapper(wrapper, function)
