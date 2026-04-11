import os
import yaml


def load_yaml(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_manifesto(path: str):
    return load_yaml(path)


def load_sages(path: str):
    return load_yaml(path)


def list_dilemma_sets(folder_path: str):
    files = []
    for name in os.listdir(folder_path):
        if name.endswith(".yaml"):
            files.append(name)
    return sorted(files)


def load_dilemma_set(folder_path: str, filename: str):
    return load_yaml(os.path.join(folder_path, filename))