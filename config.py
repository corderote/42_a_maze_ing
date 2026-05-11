#!/usr/bin/python3


CONFIG_FIELDS = {
    "WIDTH":        int,
    "HEIGHT":       int,
    "ENTRY":        tuple,
    "EXIT":         tuple,
    "OUTPUT_FILE":  str,
    "PERFECT":      bool
}


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
            print("Type not supported")
    elif lst[0][0] != '#':
        print("Innvalid line")
    return lst


def get_config() -> dict:
    content: dict = {}
    with open("config.txt", mode="rt", encoding="utf-8") as file:
        file_c = file.read().split('\n')
        for line in file_c:
            value = line.strip('\n').split('=')
            value = format_config(value)
            content[value[0]] = value[1]
    return content


if __name__ == "__main__":
    config_content = get_config()
    print(config_content)
