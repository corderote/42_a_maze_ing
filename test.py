#! /usr/bin/env python3

if __name__ == "__main__":
    import config
    cng: dict = config.get_config()
    print(cng)
