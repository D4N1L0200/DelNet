import subprocess


def echo(args: list[str]) -> str:
    """Echoes the input"""
    return " ".join(args)


def stop(args: list[str]) -> str:
    """Stops the client and server"""
    return "STOP"


def c_eval(args: list[str]) -> str:
    """Evals the input and returns the result"""
    return str(eval(" ".join(args)))


def c_help(args: list[str]) -> str:
    """Sends this message"""
    return "\n".join([f"{cmd} -> {COMMANDS[cmd].__doc__}" for cmd in COMMANDS])


def history(args: list[str]) -> str:
    """Sends the full command history"""

    if not args:
        with open("history.log", "r") as f:
            lines = f.readlines()
        return "".join(lines)

    match args[0]:
        case "clear":
            with open("history.log", "w") as f:
                f.write("")
            return "Cleared command history"
        case _:
            return "Unknown subcommand"

def update(args: list[str]) -> str:
    """Updates from github"""
    if len(args) == 1:
        py_path = r"C:\Users\danil\Documents\Dev\DelNet\.venv\Scripts\python.exe"
        subprocess.Popen([py_path, "update.py", args[0]])
        return "STOP"
    return "Usage: update <version>"


COMMANDS = {
    "echo": echo,
    "eval": c_eval,
    "help": c_help,
    "stop": stop,
    "history": history,
    "update": update,
}


# ORIGINAL