def confirmation(message: str, yes_is_default: bool = True) -> bool:
    while True:
        default_choice = "Y/n" if yes_is_default else "y/N"
        print(message)
        answer = input(f"Do you want to continue? ({default_choice}) ")

        if answer.lower() not in ["y", "n", ""]:
            continue

        if answer.lower() == "y" or (answer.lower() == "" and yes_is_default):
            return True
        return False
