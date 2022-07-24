from typing import Optional

import rich
from rich.style import Style
from rich.text import Text


class Reporter:
    def __init__(self) -> None:
        self.console: rich.console.Console = rich.get_console()

    def success(self, message: str, *, title: Optional[str] = None):
        text = self.stylize_text(title or "SUCCESS", "green", message)
        self.console.print(text)

    def fail(self, message: str, *, title: Optional[str] = None):
        text = self.stylize_text(title or "FAIL", "red", message)
        self.console.print(text)

    def skip(self, message: str, *, title: Optional[str] = None):
        text = self.stylize_text(title or "SKIPPED", "bright_cyan", message)
        self.console.print(text)

    @staticmethod
    def stylize_text(status: str, color: str, message: str) -> Text:
        text = Text(f" {status} ", style=Style(bgcolor=color))
        text.append(f" {message}", style=Style(bgcolor="black", color=color))
        return text


if __name__ == "__main__":
    r = Reporter()
    r.success("Success!")
    r.fail("Fail!")
    r.skip("Skipped!")
