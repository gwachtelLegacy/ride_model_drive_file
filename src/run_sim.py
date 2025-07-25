from trd import Trd
import tkinter as tk
from tkinter import filedialog, messagebox

def get_file_path():
    # Create a hidden root window
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select an exectution plan JSON file")
    if file_path:
        print("Selected file:", file_path)
    else:
        print("No file selected.")
    return file_path

def get_sim_experiment_type(execution_plan):
 for i in range(0, len(execution_plan['data']['plan']['$sequence'])):
        # i is to find the index of the general exporter.  This is used later to put the data-bridge as the next $sequence item
        item = execution_plan['data']['plan']['$sequence'][i]
        if item['module_name']  == "general-exporter":
            sim_output_dict = {}
            sim_output_dict['all_outputs'] = item['module_data']['export_points']['output']
            sim_output_dict['units'] = item['module_data']['export_points']['units']
            sim_output_dict['segments'] = 'metadata.experiment.segments'
            print('Sim output dict')
            print(sim_output_dict)
            return sim_output_dict, i + 1
        
        
'''Enter APEX Setup Credentials and environment'''
username = "gwachtel@legacymotorclub.com"
password = "Sarahapplejax@123"
enviroment = 'staging'  #Options are dev, staging, prod

trd_instance = Trd(enviroment)
auth_payload = { 'username': username, 'password': password }
token = trd_instance.get_apex_token(auth_payload)

'''Load execution plan'''
file_path = get_file_path()
execution_plan = trd_instance.apex_execution_plan_load(file_path)
sim_output_dict, data_bridge_index = get_sim_experiment_type(execution_plan)
execution_plan_with_data_bridge = trd_instance.create_data_bridge(execution_plan, sim_output_dict, data_bridge_index)
apex_direct_plan = trd_instance.apex_direct_plan(token, execution_plan_with_data_bridge)
