import dearpygui.dearpygui as dpg
import signal
import os
import subprocess

dpg.create_context()
with dpg.theme() as menu_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg, (200, 0, 0, 255)) #menu bar color
        dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255, 255)) #text color

dpg.create_viewport(title='JukBox Geophone Setup',width=300,height=300,min_height=300,min_width=300,resizable=False)

process_ID = 0

def start_connection(sender):
    global process_ID
    print(f"Button {sender} has been clicked!")
    dpg.set_value(1,"Connection is ACTIVE.")
    process = subprocess.Popen(["python3",R"temp.py"])
    process_ID = process.pid
    print(process_ID)

def stop_connection(sender):
    global process_ID
    print(f"Button {sender} has been clicked!")
    dpg.set_value(1,"There is no active connection.")
    print(process_ID)
    try:
        os.kill(process_ID, signal.SIGTERM)
        print(f"Process {process_ID} sent SIGTERM signal for graceful termination.")
    except OSError as e:
        print(f"Error terminating process {process_ID}: {e}")

with dpg.window(tag="prim",label=" ",width=300,height=300,no_move=True,no_resize=True,no_collapse=True,no_title_bar=True):
    dpg.bind_theme(menu_theme)
    with dpg.menu_bar():
        with dpg.menu(label="Advanced Settings"):
            dpg.add_menu_item(label="Network Settings")
    
    dpg.add_text("Welcome to JukBox!")
    dpg.add_text(tag=1,default_value="There is no active connection.")
    dpg.add_button(label="Start Data Collection", callback=start_connection)
    dpg.add_button(label="Stop Data Collection", callback=stop_connection)


dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()