import requests
import json
import os
import uuid


class Trd:
    def __init__(self):
        self.redis_cache_url = "http://trdhydra.toyota.com/api/v1/chassis-tuner/lmc_cup_gen7/execution-plans/cache"
        self.hydra_auth_url = "https://trdhydra.toyota.com/api/v1/auth/login"
        self.apex_auth_url = "https://www.apex-mp.com/api/platform/login"
        self.apex_direct_plan_url = "https://apex-setup.app.apex-mp.com/api/sim/direct_plan"
    
    def get_hydra_token(self, auth_payload):
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(self.hydra_auth_url, headers=headers, json=auth_payload)
        response_dict = response.json()
        token = response_dict['data']['token']
        if token:
            print('Token obtained')
        return token
    

    def get_apex_token(self, auth_payload):
        headers = {"MediaType": "application/json"}
        send_payload = requests.post(
            url=self.apex_auth_url, headers=headers, data=auth_payload, timeout=(15, 30)
        )
        status = json.loads(send_payload.text)
        if "data" in status.keys():
            token = status["data"]["auth"]["access_token"]
            return token

        raise PermissionError("Error Logging into Apex. Check Credentials")


    def hydra_execution_plan_load(self, file_path):
        
        """Loads the plan file and builds the execution plan from APEX.  Hydra is a different data structure"""
        with open(file_path, 'r') as f:
            json_data = json.load(f)

        # Build execution plan dictionary
        execution_plan = {"execution_plan": {}}
        for key in json_data['data']:
            execution_plan['execution_plan'][key] = json_data['data'][key]
        execution_plan['execution_plan']['type'] = json_data['type']
        execution_plan['execution_plan']['user_id'] = json_data['user_id']

        # Generate UUIDs
        base_uuid = str(uuid.uuid4())
        custom_uuid = 'bac' + base_uuid[3:]
        for field in ['session_id', 'corr_cancel_id', 'corr_group_id']:
            execution_plan['execution_plan'][field] = custom_uuid
        return execution_plan
    

    def apex_execution_plan_load(self, file_path):
            
            with open(file_path, 'r') as f:
                execution_plan = json.load(f)
            return execution_plan
    

    def hydra_cache_post(self, token, execution_plan):
        headers = {
            "Content-Type": "application/json"
        }
        if token:
            headers["Authorization"] = f"Bearer {token}"
        """Sends the execution plan to the Hydra endpoint."""
        if not execution_plan:
            raise ValueError("Execution plan not initialized. Call `cache_call()` first.")
        response = requests.post(self.redis_cache_url, headers=headers, json=execution_plan)
        print("Status Code:", response.status_code)
        print("Response Body:", response.text)
        return response
    
    def apex_direct_plan(self, token, execution_plan):
        headers = {
        "Content-Type": "application/json",
        "Cookie": f"apex_platform_token={token}",
    }
        response = requests.post(self.apex_direct_plan_url, headers=headers, json=execution_plan)
        print("Status Code:", response.status_code)
        print("Response Body:", response.text)
        return response
    


