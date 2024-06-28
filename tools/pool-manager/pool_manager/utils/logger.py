from rich.console import Console

console = Console()

class Logger:
    def __format_msg(self, *args):
        return ", ".join(args)

    def plain(self, *args):
        console.log(self.__format_msg(*args))

    def error(self, *args):
        console.print(f"[red][ERROR][/red] - {self.__format_msg(*args)}")
