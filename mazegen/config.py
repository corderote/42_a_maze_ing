#!/usr/bin/python3
from typing import Any
from mazegen.constants import CONFIG_FIELDS


class ConfigError(Exception):
    """
    Custom exception raised for critical configuration errors.

    This exception is triggered during file reading, key-value parsing,
    type casting, or logical validation constraints. It prints a styled
    error message upon instantiation.
    """
    def __init__(self, msg: str = "Unknown configuration error."):
        print(f"CONFIGURATION FILE ERROR: {msg}")


def validate_config(config: dict[str, Any]) -> bool:
    """
    Validates the logical constraints and bounds of the parsed configuration.

    This function checks that all mandatory fields are present, maze dimensions
    fall within allowable limits (2 to 50 cels), coordinate ranges for entry
    and exit points are within grid boundaries, and output file extension rules
    are strictly followed.

    Args:
        config (dict[str, Any]): The configuration dictionary containing all
                                 parsed parameters.

    Returns:
        bool: True if the entire configuration object passes all constraints.

    Raises:
        ConfigError: If a dimension is out of bounds, mandatory fields are
                     missing, coordinates overlap/overflow, or an illegal
                     file extension is selected.
    """
    # Validate number of FIELDS
    if len(config) < len(CONFIG_FIELDS):
        raise ConfigError("Not enough fields defined in configuration file.")
    # Validate the MANDATORY FIELDS:
    for key, _ in CONFIG_FIELDS.items():
        if key not in config.keys():
            raise ConfigError(f"{key} not found in config file.")
    # Validate WIDTH
    if config["WIDTH"] < 2 or config["WIDTH"] > 50:
        raise ConfigError(f"Invalid 'WIDTH' value: {config['WIDTH']}")
    # Validate HEIGHT
    if config["HEIGHT"] < 2 or config["HEIGHT"] > 50:
        raise ConfigError(f"Invalid 'HEIGHT' value: {config['HEIGHT']}")
    # Validate Entry and Exit
    if config["ENTRY"] == config["EXIT"]:
        raise ConfigError(f"'ENTRY' and 'EXIT' fields can not be equal:"
                          f"'{config['EXIT']}'")
    elif (config["ENTRY"][0] < 0 or config["ENTRY"][0] > config["WIDTH"] - 1 or
          config["ENTRY"][1] < 0 or config["ENTRY"][1] > config["HEIGHT"] - 1):
        raise ConfigError(f"Invalid 'ENTRY' field {config['ENTRY']}")
    elif (config["EXIT"][0] < 0 or config["EXIT"][0] > config["WIDTH"] - 1 or
          config["EXIT"][1] < 0 or config["EXIT"][1] > config["HEIGHT"] - 1):
        raise ConfigError(f"Invalid 'EXIT' field {config['EXIT']}")
    # Validate OUTPUT_FILE:
    if config["OUTPUT_FILE"].endswith('.py'):
        raise ConfigError("ARE YOU DUMB? "
                          "OUTPUT_FILE can not end with '.py'")
    return True


def format_config(line: str) -> list[Any]:
    """
    Parses a raw configuration string line into a typed key-value pair.

    The method splits a structural line by the '=' delimiter. It maps the
    isolated key against expected types using `CONFIG_FIELDS`, casting values
    dynamically into primitives (`int`, `str`, `bool`) or extracting nested
    multi-integer Cartesian values into a `tuple[int, int]` coordinate
    structure.

    Args:
        line (str): A single string line extracted from the configuration file.

    Returns:
        list[Any]: A 2-element list holding the string key at index 0 and its
                   properly type-cast value at index 1.

    Raises:
        ConfigError: If the string line does not match the 'KEY=VALUE' format,
                     if tuple conversion fails due to missing dimensions, or if
                     an unhandled parameter structure is encountered.
    """
    # Validate line:
    lst: list[Any] = line.strip('\n').split('=')
    if len(lst) != 2:
        raise ConfigError(f"Invalid line format '{line}'.\n"
                          "The configuration file must contain "
                          "one 'KEY'='VALUE' pair per line.")
    if lst[0] in CONFIG_FIELDS.keys():
        # Formatting the VALUE part to the proper type.
        if (CONFIG_FIELDS[lst[0]] is int
                or CONFIG_FIELDS[lst[0]] is str):
            lst[1] = CONFIG_FIELDS[lst[0]](lst[1])
        elif CONFIG_FIELDS[lst[0]] is bool:
            if lst[1] == "True":
                lst[1] = True
            elif lst[1] == "False":
                lst[1] = False
            else:
                raise ConfigError(f"Invalid value for {lst[0]}")
        elif CONFIG_FIELDS[lst[0]] is tuple:
            tuple_lst: list[Any] = lst[1].split(',')
            if len(tuple_lst) != 2:
                raise ConfigError(f"Invalid tuple for '{lst[0]}': '{lst[1]}'.")
            else:
                lst[1] = (int(tuple_lst[0]), int(tuple_lst[1]))
        else:
            raise ConfigError()
    return lst


def get_config(filepath: str) -> dict[str, Any]:
    """
    Reads, parses, and fully validates a maze configuration file from disk.

    This function opens the target configuration file using UTF-8 encoding in
    read-text mode. It iterates over all available structural lines, skipping
    blank carriage returns and comment syntax blocks (`#`). Valid pairs are
    packaged into a structured dictionary object before undergoing semantic
    checks through `validate_config`.

    Args:
        filepath (str): The physical directory or relative route to the `.txt`
        source file.

    Returns:
        dict[str, Any]: A type-safe dictionary mapping configuration keys to
        their formatted values.

    Raises:
        ConfigError: Cascaded from `format_config` or `validate_config` if
            formatting rules or boundary constraints are violated.
        FileNotFoundError: Inherited if the provided system file route cannot
            be opened.
    """
    content: dict[str, Any] = {}
    with open(filepath, mode="rt", encoding="utf-8") as file:
        file_c = file.read().split('\n')
        for line in file_c:
            if line != '' and line[0] != '#':
                value = format_config(line)
                content[value[0]] = value[1]
    validate_config(content)
    return content
