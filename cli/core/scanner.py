
import os


def scan_skills(path: str) -> list:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Path not found: {path}")
    if not os.path.isdir(path):
        raise NotADirectoryError(f"Not a directory: {path}")

    skills = []
    for root, _, files in os.walk(path):
        for f in files:
            if f.endswith(".md"):
                p = os.path.join(root, f)
                try:
                    content = open(p, encoding="utf-8").read()
                except OSError as e:
                    print(f"⚠ Could not read {p}: {e}")
                    content = ""
                skills.append({"name": f, "path": p, "content": content})
    return skills
