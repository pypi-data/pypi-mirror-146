import json
import falcon

from infrastructure.services.logs_service import LogsService
from infrastructure.dto.ExecutionContext import ExecutionContext


class BaseExecutionService:
    def __init__(self):
        self.actions = {}
        self.logger = LogsService("logs")
        return

    def execute(self, execution_context: ExecutionContext):
        if execution_context.action_name in self.actions.keys():
            action_response = self.actions[execution_context.action_name](execution_context)
            response = {'executionId': action_response.execution_id, 'statusEnum': action_response.status.name,
                        'progress': action_response.progress, 'message': action_response.message}
            return json.dumps(response, ensure_ascii=False)
        raise NameError("Action doesn't exists")

    def set_actions(self, actions):
        self.actions = actions
