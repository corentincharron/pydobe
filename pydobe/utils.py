from collections import UserDict


class IntStringDict(UserDict):
    def __getitem__(self, key):
        try:
            return self.data[key]
        except KeyError:
            pass
        try:
            for k, v in self.data.items():
                if v.lower() == key.lower():
                    return k
        except KeyError:
            pass
        raise KeyError(key)

    def __setitem__(self, key, value):
        if isinstance(key, int):
            self.data[key] = value
        elif isinstance(key, str):
            self.data[value] = key
        else:
            pass


def hex_to_rgb(hex_value):
    hex_value = hex_value.lstrip("#")
    color_value_list = list(int(hex_value[i : i + 2], 16) for i in (0, 2, 4))
    return color_value_list
