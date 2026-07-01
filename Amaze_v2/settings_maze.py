#!/usr/bin/python3
from typing import Any


CONFIG_FIELDS = {
    "WIDTH":        int,
    "HEIGHT":       int,
    "ENTRY":        tuple,
    "EXIT":         tuple,
    "OUTPUT_FILE":  str,
    "PERFECT":      bool
}


class ConfigError(Exception):
    def __init__(self, msg: str = "Unknown configuration error."):
        print(f"CONFIGURATION FILE ERROR: {msg}")


def validate_config(config: dict[str, Any]) -> bool:
    for key, _value in CONFIG_FIELDS.items():
        if key not in config.keys():
            raise ConfigError(f"{key} not found in config file.")
    if len(config) < len(CONFIG_FIELDS):
        raise ConfigError("Not enough fields defined in configuration file.")
    elif config["WIDTH"] < 2:
        raise ConfigError(f"Invalid 'WIDTH' field {config['WIDTH']}")
    elif config["HEIGHT"] < 2:
        raise ConfigError(f"Invalid 'HEIGHT' field {config['HEIGHT']}")
    elif (config["ENTRY"][0] < 0 or config["ENTRY"][0] > config["WIDTH"] - 1 or
          config["ENTRY"][1] < 0 or config["ENTRY"][1] > config["HEIGHT"] - 1):
        raise ConfigError(f"Invalid 'ENTRY' field {config['ENTRY']}")
    elif (config["EXIT"][0] < 0 or config["EXIT"][0] > config["WIDTH"] - 1 or
            config["EXIT"][1] < 0 or config["EXIT"][1] > config["HEIGHT"] - 1):
        raise ConfigError(f"Invalid 'EXIT' field {config['EXIT']}")
    elif config["ENTRY"] == config["EXIT"]:
        raise ConfigError(f"'ENTRY' and 'EXIT' fields can not be equal "
                          f"'{config['EXIT']}'")
    else:
        return True


def format_config(line: str) -> list[Any]:
    # Validate line:
    lst: list[Any] = line.strip('\n').split('=')
    if len(lst) != 2 and line[0] != '#':
        raise ConfigError(f"Invalid line format '{line}'.\n"
                          "The configuration file must contain "
                          "one 'KEY'='VALUE' pair per line.")
    if lst[0] in CONFIG_FIELDS.keys():
        # Formatting the VALUE part to the proper type.
        if (CONFIG_FIELDS[lst[0]] is int
                or CONFIG_FIELDS[lst[0]] is str
                or CONFIG_FIELDS[lst[0]] is bool):
            lst[1] = CONFIG_FIELDS[lst[0]](lst[1])
        elif CONFIG_FIELDS[lst[0]] is tuple:
            tuple_lst: list[Any] = lst[1].split(',')
            if len(tuple_lst) != 2:
                raise ConfigError(f"Invalid tuple for '{lst[0]}': '{lst[1]}'.")
            else:
                lst[1] = (int(tuple_lst[0]), int(tuple_lst[1]))
        else:
            raise ConfigError()
    return lst


def get_config() -> dict[str, Any]:
    content: dict[str, Any] = {}
    with open("config.txt", mode="rt", encoding="utf-8") as file:
        file_c = file.read().split('\n')
        for line in file_c:
            value = format_config(line)
            content[value[0]] = value[1]
    validate_config(content)
    return content


if __name__ == "__main__":
    try:
        config_content = get_config()
        print(config_content)
    except (ConfigError) as msg:
        print(msg)
