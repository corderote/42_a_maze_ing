#!/usr/bin/python3


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


def validate_config(config: dict) -> bool:
    if len(config) < len(CONFIG_FIELDS):
        raise ConfigError("Not enough fields defined in configuration file.")
    elif config("WIDTH") < 2:
        raise ConfigError(f"Invalid 'WIDTH' field {config['WIDTH']}")
    elif config("HEIGHT") < 2:
        raise ConfigError(f"Invalid 'HEIGHT' field {config['HEIGHT']}")
    elif (config("ENTRY")[0] < 2 or config("ENTRY")[0] > config("WIDTH") or
            config("ENTRY")[1] < 2 or config("ENTRY")[1] > config("HEIGHT")):
        raise ConfigError(f"Invalid 'ENTRY' field {config['ENTRY']}")
    elif (config("EXIT")[0] < 2 or config("EXIT")[0] > config("WIDTH") or
            config("EXIT")[1] < 2 or config("EXIT")[1] > config("HEIGHT")):
        raise ConfigError(f"Invalid 'EXIT' field {config['EXIT']}")
    elif config("ENTRY") == config("EXIT"):
        raise ConfigError(f"'ENTRY' and 'EXIT' fields can not be equal "
                          f"'{config['EXIT']}'")
    else:
        return True


def format_config(lst: list[str]) -> list:
    if lst[0] in CONFIG_FIELDS.keys() and lst[0][0] != '#':
        if (CONFIG_FIELDS[lst[0]] is int
                or CONFIG_FIELDS[lst[0]] is str
                or CONFIG_FIELDS[lst[0]] is bool):
            lst[1] = CONFIG_FIELDS[lst[0]](lst[1])
        elif CONFIG_FIELDS[lst[0]] is tuple:
            lst[1] = lst[1].split(',')
            for nbr in range(0, len(lst[1])):
                lst[1][nbr] = int(lst[1][nbr])
            lst[1] = CONFIG_FIELDS[lst[0]](lst[1])
        else:
            raise ConfigError(f"Not supported field type '{lst[1]}'.")
    elif lst[0][0] != '#':
        raise ConfigError(f"Invalid line format '{lst[0]}={lst[1]}'.")
    return lst


def get_config() -> dict:
    content: dict = {}
    with open("config.txt", mode="rt", encoding="utf-8") as file:
        file_c = file.read().split('\n')
        for line in file_c:
            value = line.strip('\n').split('=')
            if len(value) != 2:
                raise ConfigError(f"Invalid line format '{line}'.")
            value = format_config(value)
            content[value[0]] = value[1]
    return content


if __name__ == "__main__":
    config_content = get_config()
    print(config_content)
