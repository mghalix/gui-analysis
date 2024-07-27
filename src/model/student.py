from dataclasses import dataclass


@dataclass(frozen=True)
class Student:
    id: int
    name: str

    def __str__(self) -> str:
        # return str(self.id) + ". " + self.name
        return self.name
