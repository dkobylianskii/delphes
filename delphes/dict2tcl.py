import re

SPACE_RE = re.compile(r"\s")


def dict2tcl(value, level=0):
    sep = "\n" + " " * 4 * level
    end = "\n" + " " * 4 * (level - 1)
    if isinstance(value, dict):
        if level == 0:
            params = {k: v for k, v in value.items() if not isinstance(v, dict)}
            modules = {k: v for k, v in value.items() if isinstance(v, dict)}
            items = [f"set {k} {dict2tcl(v, level + 1)}" for k, v in params.items()]
            items.extend(f"module {v['Class']} {k} {dict2tcl(v, level + 1)}" for k, v in modules.items())
            return sep.join(items)
        else:
            items = [f"set {k} {dict2tcl(v, level + 1)}" for k, v in value.items() if k != "Class"]
            return "{" + sep + sep.join(items) + end + "}"
    if isinstance(value, list):
        items = [dict2tcl(v, level + 1) for v in value]
        return "[list " + " ".join(items) + "]"
    if isinstance(value, str):
        lines = [v.strip() for v in value.splitlines()]
        lines = [v for v in lines if v]
        if len(lines) > 1:
            return "{" + sep + sep.join(lines) + end + "}"
        if lines:
            return SPACE_RE.sub("", lines[0])
        return "{}"
    return str(value)
