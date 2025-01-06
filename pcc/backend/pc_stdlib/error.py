from sys import exit, stderr

def error(msg: str) -> None:
    print(msg, file=stderr)
    exit(1)