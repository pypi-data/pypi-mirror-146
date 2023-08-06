import re
from itertools import repeat
from typing import Final, Optional

_simple_pattern: Final = re.compile(
    "^(?:unsigned\\s)?(?P<type>[a-zA-Z]+)(?:\\s?\\([^)]+\\))?(?:\\sin\\s[\\[][^]]+[]])?(?:[,.\\s].*)?$")

_container_of_pattern: Final = re.compile(
    "^(?:[Aa][n]?\\s)?(?P<container>[a-zA-Z]+)\\sof\\s(?::class:`[~!]?(?P<reference>[^`]+)`|"
    "(?P<data>[a-zA-Z]+))(?P<qualifier>[',.\\s].*)?$")

_prop_collection_of_pattern: Final = re.compile(
    "^(?:[Aa][n]?\\s)?(?::class:`[~!]?(?P<base>[^`]+)`\\s+)?:class:`bpy_prop_collection`\\sof\\s"
    "(?::class:`[~!]?(?P<reference>[^`]+)`|(?P<data>[a-zA-Z]+))(?P<qualifier>[',.\\s].*)?$")

_exp_list_value_of_pattern: Final = re.compile(
    "^(?:[Aa][n]?\\s)?:class:`[~!]?bge.types.EXP_ListValue`\\sof\\s(?::class:`[~!]?(?P<reference>[^`]+)`|"
    "(?P<data>[a-zA-Z]+))(?P<qualifier>[',.\\s].*)?$")

_qualified_list_pattern: Final = re.compile(
    "^(?:[Aa][n]?\\s)?list\\s*\\([a-zA-Z\\s]*vector\\sof\\s[0-9]+\\s(?P<data>[a-zA-Z]+)"
    "(?:[,.\\s][^)]*)?\\)(?:[,.\\s].*)?$")

_list_bracket_pattern: Final = re.compile(
    "^list\\s*\\[(?::class:`[~!]?(?P<reference>[^`]+)`|(?P<data>[a-zA-Z]+))](?:[,.\\s].*)?$")

_array_of_pattern: Final = re.compile(
    "^(?:[Aa][n]?\\s)?(?P<data>[a-z]+)\\sarray\\sof\\s(?P<count>[0-9]+)\\sitems.*$")

_multi_array_of_pattern: Final = re.compile(
    "^(?:[Aa][n]?\\s)?(?P<data>[a-z]+)\\smulti-dimensional\\sarray\\sof\\s(?P<rows>[0-9]+)"
    "\\s*\\*\\s*(?P<cols>[0-9]+)\\sitems.*$")

_dictionary_pattern: Final = re.compile(
    "^(?:[Aa]\\s)?dict(?:ionary)?\\s*[\\[(](?P<key>[^,\\s]+)\\s*,\\s*(?P<value>[^])]+)[])].*$")

_reference_pattern: Final = re.compile(
    "^:class:`[~!]?(?P<name>[a-zA-Z_0-9.\\s]+)(?:\\s*<(?P<target>[a-zA-Z_0-9.]+)>)?`(?:[,.\\s].*)?$")

_reference_item_pattern: Final = re.compile(
    "^[-\\s]*:class:`[~!]?(?P<name>[a-zA-Z_0-9.\\s]+)(?:\\s*<(?P<target>[a-zA-Z_0-9.]+)>)?`$")

_union_pattern: Final = re.compile(
    "^(?::class:`[~!]?[^`]+`|[a-zA-Z]+)(:?\\sor\\s(?::class:`[~!]?[^`]+`|[a-zA-Z]+))+(?:[,.\\s].*)?$")

_matrix_pattern: Final = re.compile("^(?:[Aa]\\s)?(?:[0-9xX*]+\\s)?[Mm]atrix|"
                                    "[Mm]atrix(?:\\s?[0-9a-z\\s\\[\\]()]+)?$")

_known_types: Final = {
    "any": "typing.Any",
    "str": "str",
    "strs": "str",
    "string": "str",
    "strings": "str",
    "int": "int",
    "ints": "int",
    "integer": "int",
    "integers": "int",
    "float": "float",
    "floats": "float",
    "double": "float",
    "doubles": "float",
    "bool": "bool",
    "bools": "bool",
    "boolean": "bool",
    "booleans": "bool",
    "class": "typing.Type",
    "classes": "typing.Type",
    "type": "typing.Type",
    "types": "typing.Type",
    "object": "bpy.types.Object",
    "objects": "bpy.types.Object",
    "callable": "typing.Callable",
    "callables": "typing.Callable",
    "function": "typing.Callable",
    "functions": "typing.Callable",
    "dict": "typing.Dict[str, typing.Any]",
    "dictionary": "typing.Dict[str, typing.Any]",
    "dictionaries": "typing.Dict[str, typing.Any]",
    "set": "typing.Set[typing.Any]",
    "sets": "typing.Set[typing.Any]",
    "sequence": "typing.Sequence[typing.Any]",
    "sequences": "typing.Sequence[typing.Any]",
    "list": "typing.List[typing.Any]",
    "lists": "typing.List[typing.Any]",
    "array": "typing.Tuple[typing.Any, ...]",
    "arrays": "typing.Tuple[typing.Any, ...]",
    "tuple": "typing.Tuple[typing.Any, ...]",
    "tuples": "typing.Tuple[typing.Any, ...]"
}

_container_types: Final = {
    "list": "typing.List[#T#]",
    "set": "typing.Set[#T#]",
    "vector": "typing.List[#T#]",
    "sequence": "typing.Sequence[#T#]",
    "iterable": "typing.Iterable[#T#]",
    "pair": "typing.Tuple[#T#, #T#]",
    "tuple": "typing.Tuple[#T#, ...]"
}


def parse_simple(text: str) -> Optional[str]:
    result = _simple_pattern.match(text)

    if result:
        type_info = result.group("type").lower()

        if type_info in _known_types:
            return _known_types[type_info]

    return None


def parse_reference(text: str) -> Optional[str]:
    result = _reference_pattern.match(text)

    type_info = result.group("target") or result.group("name") if result else None

    return "typing.Any" if type_info == "AnyType" else type_info


def parse_qualified_list(text: str) -> Optional[str]:
    result = _qualified_list_pattern.match(text)

    if not result:
        return None

    data_type = result.group("data")

    if data_type in _known_types:
        return f"typing.List[{_known_types[data_type]}]"

    return None


def parse_bracket_list(text: str) -> Optional[str]:
    result = _list_bracket_pattern.match(text)

    if not result:
        return None

    data_type = result.group("data")

    if data_type in _known_types:
        data_type = _known_types[data_type]

    if not data_type:
        data_type = result.group("reference")

    if data_type:
        return f"typing.List[{data_type}]"

    return None


def parse_prop_collection_of(text: str) -> Optional[str]:
    result = _prop_collection_of_pattern.match(text)

    if not result:
        return None

    base_type = result.group("base")

    # noinspection DuplicatedCode
    data_type = result.group("data")
    qualifier = result.group("qualifier")

    if data_type in _known_types:
        data_type = _known_types[data_type]
    else:
        reference = result.group("reference")
        data_type = parse_reference("".join((":class:`", reference, "`"))) if reference else None

    if not data_type:
        return None

    if qualifier:
        qualifier = qualifier.strip()

        if qualifier.startswith("tuple"):
            data_type = f"typing.Tuple[{data_type}, ...]"
        elif qualifier.startswith("list"):
            data_type = f"typing.List[{data_type}]"
        elif qualifier.startswith("sequence"):
            data_type = f"typing.Sequence[{data_type}]"

    types = [base_type] if base_type else []
    types.append(f"typing.Sequence[{data_type}]")
    types.append(f"typing.Mapping[str, {data_type}]")
    types.append("bpy.types.bpy_prop_collection")

    return f"typing.Union[{', '.join(types)}]"


def parse_exp_list_value_of(text: str) -> Optional[str]:
    result = _exp_list_value_of_pattern.match(text)

    if not result:
        return None

    data_type = result.group("data")

    # noinspection DuplicatedCode
    qualifier = result.group("qualifier")

    if data_type in _known_types:
        data_type = _known_types[data_type]
    else:
        reference = result.group("reference")
        data_type = parse_reference("".join((":class:`", reference, "`"))) if reference else None

    if not data_type:
        return None

    if qualifier:
        qualifier = qualifier.strip()

        if qualifier.startswith("tuple"):
            data_type = f"typing.Tuple[{data_type}, ...]"
        elif qualifier.startswith("list"):
            data_type = f"typing.List[{data_type}]"
        elif qualifier.startswith("sequence"):
            data_type = f"typing.Sequence[{data_type}]"

    types = (
        f"typing.Sequence[{data_type}]",
        f"typing.Mapping[str, {data_type}]",
        "bge.types.EXP_ListValue"
    )

    return f"typing.Union[{', '.join(types)}]"


def parse_container_of(text: str) -> Optional[str]:
    result = _container_of_pattern.match(text)

    if not result:
        return None

    container_type = result.group("container")

    data_type = result.group("data")
    qualifier = result.group("qualifier")

    if container_type in _container_types:
        container_type = _container_types[container_type]
    else:
        container_type = None

    if data_type in _known_types:
        data_type = _known_types[data_type]
    else:
        reference = result.group("reference")
        data_type = parse_reference("".join((":class:`", reference, "`"))) if reference else None

    if not data_type or not container_type:
        return None

    if qualifier:
        qualifier = qualifier.strip()

        if qualifier.startswith("tuple"):
            data_type = f"typing.Tuple[{data_type}, ...]"
        elif qualifier.startswith("list"):
            data_type = f"typing.List[{data_type}]"
        elif qualifier.startswith("sequence"):
            data_type = f"typing.Sequence[{data_type}]"

    return container_type.replace("#T#", data_type)


def parse_array_of(text: str) -> Optional[str]:
    result = _array_of_pattern.match(text)

    if not result:
        return None

    data_type = result.group("data")
    count = int(result.group("count"))

    if data_type in _known_types:
        data_type = _known_types[data_type]
    else:
        return None

    if count > 5:
        return f"typing.Tuple[{data_type}, ...]"

    return f"typing.Tuple[{', '.join(repeat(data_type, count))}]"


def parse_multi_array_of(text: str) -> Optional[str]:
    result = _multi_array_of_pattern.match(text)

    if not result:
        return None

    data_type = result.group("data")
    rows = int(result.group("rows"))
    cols = int(result.group("cols"))

    if data_type in _known_types:
        data_type = _known_types[data_type]
    else:
        return None

    def make_tuple(t, n):
        if n > 5:
            return f"typing.Tuple[{t}, ...]"

        return f"typing.Tuple[{', '.join(repeat(t, n))}]"

    return make_tuple(make_tuple(data_type, cols), rows)


def parse_matrix(text: str) -> Optional[str]:
    if _matrix_pattern.match(text):
        return "mathutils.Matrix"

    return None


def parse_dictionary(text: str) -> Optional[str]:
    result = _dictionary_pattern.match(text)

    if not result:
        return None

    def guess_type(v):
        if not v:
            return "typing.Any"

        if v in _known_types:
            return _known_types[v]

        return parse_reference(v) or "typing.Any"

    key = guess_type(result.group("key"))
    value = guess_type(result.group("value"))

    return f"typing.Dict[{key}, {value}]"


def parse_union(text: str) -> Optional[str]:
    result = _union_pattern.match(text)

    if not result:
        return None

    expressions = tuple(text.replace("\n", "").split(" or "))

    if "None" in expressions:
        return None

    parsed_types = tuple(map(parse_type, expressions))

    if None in parsed_types or len(expressions) != len(set(parsed_types)):
        return None

    return f"typing.Union[{', '.join(parsed_types)}]"


def parse_union_types(text: str) -> Optional[str]:
    lines = text.split("\n")

    if len(lines) < 3:
        return None

    parsed_types = []

    for line in filter(lambda l: any(l.strip()), lines[1:]):
        result = _reference_item_pattern.match(line)

        if not result:
            return None

        type_info = result.group("target") or result.group("name") if result else None

        parsed_types.append(type_info)

    return f"typing.Union[{', '.join(parsed_types)}]"


def parse_special_cases(text: str) -> Optional[str]:
    text = text.lower()

    if "enum in" in text:
        return "str"
    elif "enum set in" in text:
        return "typing.Set[str]"

    if text.startswith("function"):
        return "typing.Callable"

    if text.startswith("vector"):
        return "mathutils.Vector"
    else:
        segments = text.split(" ")

        if len(segments) > 1 and segments[1] == "vector":
            return "mathutils.Vector"

    return None


def parse_type(text: str) -> Optional[str]:
    parsers = (
        parse_array_of,
        parse_multi_array_of,
        parse_qualified_list,
        parse_bracket_list,
        parse_container_of,
        parse_prop_collection_of,
        parse_exp_list_value_of,
        parse_dictionary,
        parse_union,
        parse_union_types,
        parse_reference,
        parse_simple,
        parse_matrix,
        parse_special_cases
    )

    try:
        return next(filter(lambda r: r, map(lambda p: p(text), parsers)))
    except StopIteration:
        return None
