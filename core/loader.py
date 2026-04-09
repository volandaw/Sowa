import yaml


def load_yaml(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_manifesto(path: str):
    return load_yaml(path)


def load_dilemmas(path: str):
    return load_yaml(path)


def load_sages(path: str):
    return load_yaml(path)