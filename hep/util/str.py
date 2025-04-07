class Str:
    @staticmethod
    def replace_str_in_list(list_str: list[str], from_str: str, to_str: str):
        return [x.replace(from_str, to_str) for x in list_str]
