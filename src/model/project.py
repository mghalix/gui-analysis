from dataclasses import dataclass

from .student import Student


@dataclass(frozen=True)
class Project:
    title: str
    participants: list[Student]

    def __str__(self) -> str:
        out = self.title + "\n"
        for student in self.participants:
            out += str(student) + "\n"
        return out

    def __iter__(self):
        return ProjectIterator(self.participants)


class ProjectIterator:
    def __init__(self, participants: list[Student]):
        self.participants = participants
        self.index = 0

    def __next__(self):
        if self.index < len(self.participants):
            result = self.participants[self.index]
            self.index += 1
            return result
        raise StopIteration
