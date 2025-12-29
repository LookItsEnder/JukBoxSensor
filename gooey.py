import dearpygui.dearpygui as dpg
import signal
import subprocess

dpg.create_context()
dpg.create_viewport(title='JukBox Geophone Setup',min_height=300,min_width=300,max_height=300,max_width=300)

PID = 0
def start_connection(sender):
    print(f"Button {sender} has been clicked!")
    process = subprocess.Popen(["python","temp.py"])
    PID <- process.pid
    print(PID)

def stop_connection(sender):
    print(f"Button {sender} has been clicked!")
    process = subprocess.Popen(signal.SIGINT)

with dpg.window(label=" ",width=300,height=300,no_move=True, no_close=True,no_collapse=True,no_resize=True,menubar=False):
    dpg.add_text("Welcome to JukBox!")
    dpg.add_button(label="Start", callback=start_connection)
    dpg.add_button(label="Stop")


dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()