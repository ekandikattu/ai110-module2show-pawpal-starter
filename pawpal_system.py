from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Pet:
    breed: str
    weight: float
    health_status: str

    def getBreed(self) -> str:
        pass

    def getWeight(self) -> float:
        pass

    def getStatus(self) -> str:
        pass

    def setBreed(self, breed: str) -> None:
        pass

    def setWeight(self, weight: float) -> None:
        pass

    def setStatus(self, status: str) -> None:
        pass

    def showPetInfo(self) -> str:
        pass


@dataclass
class Task:
    name: str
    duration: int
    priority: int
    task_type: str
    pet_name: Optional[str] = None


class Owner:
    def __init__(self, gender: str, age: int, preferences: str = "") -> None:
        pass

    def addPet(self, pet: Pet) -> None:
        pass

    def removePet(self, breed: str) -> bool:
        pass

    def showPets(self) -> List[str]:
        pass

    def showOwnerInfo(self) -> str:
        pass

    def getPreferences(self) -> str:
        pass

    def setPreferences(self, preferences: str) -> None:
        pass

    def addTask(self, task: Task) -> None:
        pass

    def removeTask(self, task_name: str) -> bool:
        pass

    def changeTask(
        self,
        task_name: str,
        duration: Optional[int] = None,
        priority: Optional[int] = None,
    ) -> bool:
        pass

    def showTasks(self) -> List[str]:
        pass


class Scheduler:
    def __init__(self) -> None:
        pass

    def makeSchedule(
        self,
        tasks: List[Task],
        time_available: int,
        preferences: str = "",
    ) -> List[Task]:
        pass

    def showSchedule(self) -> List[str]:
        pass
