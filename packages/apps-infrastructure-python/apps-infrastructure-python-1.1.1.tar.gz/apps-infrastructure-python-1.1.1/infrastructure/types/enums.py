from enum import Enum


class TaskStatus(Enum):
    COMPLETED = 1
    ERROR = 2
    IN_PROGRESS = 3


class IconType(Enum):
    icon = 1,
    sideBarIcon = 2
