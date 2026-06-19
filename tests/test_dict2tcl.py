import pytest
from delphes.dict2tcl import dict2tcl

cases = [
    (
        {"a": 1},
        "set a 1",
        "set_int",
    ),
    (
        {"a": True},
        "set a true",
        "set_bool",
    ),
    (
        {"a": ""},
        "set a {}",
        "set_string_empty",
    ),
    (
        {"a": "bcd"},
        "set a bcd",
        "set_string_simple",
    ),
    (
        {"a": "b c\td"},
        "set a bcd",
        "set_string_spaces_tabs",
    ),
    (
        {"a": "\n\tb c\td \n"},
        "set a bcd",
        "set_string_normalised",
    ),
    (
        {"a": [i for i in range(3)]},
        "set a [list 0 1 2]",
        "set_list",
    ),
    (
        {"a": {"Class": "b", "c": 1}},
        "module b a {\n    set c 1\n}",
        "module_int",
    ),
    (
        {"a": {"Class": "b", "c": ""}},
        "module b a {\n    set c {}\n}",
        "module_string_empty",
    ),
    (
        {"a": {"Class": "b", "c": "def"}},
        "module b a {\n    set c def\n}",
        "module_string_simple",
    ),
    (
        {"a": {"Class": "b", "c": "d e\tf"}},
        "module b a {\n    set c def\n}",
        "module_string_spaces_tabs",
    ),
    (
        {"a": {"Class": "b", "c": "\n\td e\tf \n"}},
        "module b a {\n    set c def\n}",
        "module_string_normalised",
    ),
    (
        {"a": {"Class": "b", "c": "\n\td e\tf \n g h\ti"}},
        "module b a {\n    set c {\n        d e\tf\n        g h\ti\n    }\n}",
        "module_multiline",
    ),
    (
        {"a": {"Class": "b", "c": [i for i in range(3)]}},
        "module b a {\n    set c [list 0 1 2]\n}",
        "module_list",
    ),
]


def make_param(input, output, id):
    return pytest.param(input, output, id=id)


@pytest.mark.parametrize("input,output", [make_param(*c) for c in cases])
def test_dict2tcl(input, output):
    assert dict2tcl(input) == output
