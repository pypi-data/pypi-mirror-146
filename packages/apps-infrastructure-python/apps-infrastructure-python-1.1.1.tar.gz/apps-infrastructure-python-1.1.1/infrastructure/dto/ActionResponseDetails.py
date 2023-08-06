from infrastructure.types.enums import TaskStatus


class ActionResponseDetails:
    def __init__(self, execution_id, status: TaskStatus = TaskStatus.IN_PROGRESS, progress=0, message=""):
        self.execution_id = execution_id
        self.status = status
        self.progress = progress
        self.message = message
