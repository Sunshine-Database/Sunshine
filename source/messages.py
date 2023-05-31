from colorama import Fore, Style

class Message:
    """
    Message-class used to issue errors, success messages, and warnings.
    """
    def __init__(self, text: str, type: str) -> None:
        self.text = text
        self.type = type

    def __call__(self) -> None:
        match self.type:
            case 'success':
                print(Fore.GREEN  + f'Success: {self.text}' + Style.RESET_ALL)
            case 'warning':
                print(Fore.YELLOW + f'Warning: {self.text}' + Style.RESET_ALL)
            case 'error':
                print(Fore.RED    + f'Error:   {self.text}' + Style.RESET_ALL)
            case _:
                return