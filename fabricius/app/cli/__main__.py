from pathlib import Path

import click

plugin_folder = Path(__file__).parent.joinpath("commands")


class FabriciusCLI(click.MultiCommand):
    def list_commands(self, ctx: click.Context) -> list[str]:
        rv: list[str] = [
            str(file.stem)
            for file in plugin_folder.iterdir()
            if file.suffix == ".py" and not file.name.startswith("__")
        ]
        rv.sort()
        return rv

    def get_command(self, ctx: click.Context, cmd_name: str) -> click.Command | None:
        ns: dict[str, click.Command] = {}
        fn = plugin_folder.joinpath(f"{cmd_name}.py")
        with open(fn) as f:
            code = compile(f.read(), fn, "exec")
            eval(code, ns, ns)
        return ns["run"]


cli = FabriciusCLI(help="Fabricius: Template rendering engine.")

if __name__ == "__main__":
    cli()
