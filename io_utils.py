def load_file_safely(path: str, label: str) -> list[str]:

    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        return []
    except OSError:
        return []

    return [line for line in lines if line]
