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

'''Enter APEX Setup Credentials'''
username = "gwachtel@legacymotorclub.com"
password = "Sarahapplejax@123"

trd_instance = Trd()
auth_payload = { 'username': username, 'password': password }
token = trd_instance.get_apex_token(auth_payload)

'''Load execution plan'''
file_path = get_file_path()
execution_plan = trd_instance.apex_execution_plan_load(file_path)
apex_direct_plan = trd_instance.apex_direct_plan(token, execution_plan)
