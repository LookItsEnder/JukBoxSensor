import dearpygui.dearpygui as dpg
import signal
import os
import subprocess

dpg.create_context()
dpg.create_viewport(title='JukBox Geophone Setup',min_height=300,min_width=300,max_height=300,max_width=300)

process_ID = 0
def start_connection(sender):
    global process_ID
    print(f"Button {sender} has been clicked!")
    process = subprocess.Popen(["python3",R"C:\Users\freimundcj07\Documents\GitHub\JukBoxSensor\temp.py"])
    process_ID = process.pid
    print(process_ID)

def stop_connection(sender):
    global process_ID
    print(f"Button {sender} has been clicked!")
    print(process_ID)
    try:
        os.kill(process_ID, signal.SIGTERM)
        print(f"Process {process_ID} sent SIGTERM signal for graceful termination.")
    except OSError as e:
        print(f"Error terminating process {process_ID}: {e}")

with dpg.window(label=" ",width=300,height=300,no_move=True, no_close=True,no_collapse=True,no_resize=True,menubar=False):
    dpg.add_text("Welcome to JukBox!")
    dpg.add_button(label="Start", callback=start_connection)
    dpg.add_button(label="Stop", callback=stop_connection)


dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()