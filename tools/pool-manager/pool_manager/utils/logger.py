from rich import print as rprint

class Logger:
    def plain(self, *args):
        rprint(args)

    def error(self, *args):
        rprint("[red][ERROR][/red]", args)
