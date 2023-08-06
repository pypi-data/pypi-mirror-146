import chattingapiru
import chattingapien


class Client:
    def __init__(self, lang: str):
        self.lang = lang.upper()

    def get(self, text: str):
        if self.lang == "RU":
            return chattingapiru.get(text.casefold())
        else:
            return chattingapien.get(text.casefold())
