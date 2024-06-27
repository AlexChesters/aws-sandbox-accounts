from rich import print as rprint

class Logger:
    def plain(self, *args):
        rprint(args)
