from dataclasses import dataclass


@dataclass
class Notification:
    def __init__(self) -> None:
        self._errors: list[str] = []
    
    def add_error(self, msg: str) -> None:
        self._errors.append(msg)
    
    @property
    def has_errors(self):
        return len(self._errors) > 0

    @property
    def messages(self) -> str:
        return ",".join(self._errors)