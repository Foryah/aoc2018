def load_input(path: str) -> str:
    with open(path, "r") as f:
        return f.read().rstrip()
