from infrastructure.dto.ParamDetails import ParamDetails


class ExecutionContext:
    def __init__(self, req):
        self.action_name = req['actionName']
        self.execution_id = req['executionId']
        self.global_params = self.get_params(req['globalParams'])
        self.action_params = self.get_params(req['actionParams'])
        self.bigid_base_url = req['bigidBaseUrl']
        self.bigid_token = req['bigidToken']
        self.tpa_id = req['tpaId']
        self.update_result_callback = req['updateResultCallback']

    def get_params(self, params_list):
        params = []
        for param in params_list:
            params.append(ParamDetails(param['paramName'], param['paramValue']))
        return params
