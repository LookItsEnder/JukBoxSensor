import dearpygui.dearpygui as dpg
import signal
import os
import subprocess
import portconfig

dpg.create_context()
with dpg.theme() as menu_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg, (200, 0, 0, 255)) #menu bar color
        dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255, 255)) #text color

dpg.create_viewport(title='JukBox Geophone Setup',width=500,height=300,min_height=300,min_width=300,resizable=False)
process_ID = 0

def port_5678():
    if(dpg.get_value(5678)==False):
        portconfig.port_s=8001
        dpg.set_value("Port",f"Data Collection is on port {portconfig.port_s}")
    else:
        portconfig.port_s = 5678
        dpg.set_value("Port",f"Data Collection is on port {portconfig.port_s}")

def custom_port():
    portconfig.port_s = dpg.get_value("customPort")
    dpg.set_value("Port",f"Data Collection is on port {portconfig.port_s}")


def start_connection(sender):
    global process_ID
    print(f"Button {sender} has been clicked, starting connection on port {portconfig.port_s}!")
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

with dpg.window(tag="prim",label=" ",width=500,height=300,no_move=True,no_resize=True,no_collapse=True,no_title_bar=True):
    dpg.bind_theme(menu_theme)
    with dpg.menu_bar():
        with dpg.menu(label="Network Settings"):
            with dpg.menu(label="Change Active Port"):
                dpg.add_text("Default Value: 8001")
                dpg.add_menu_item(tag=5678,label="Set to 5678", callback=port_5678, check=True)
                dpg.add_text("Custom Port:")
                dpg.add_input_int(tag="customPort",min_clamped=True,min_value=0,callback=custom_port)
            
    dpg.add_text("Welcome to JukBox!")
    dpg.add_text(tag=1,default_value="There is no active connection.")
    dpg.add_button(label="Start Data Collection", callback=start_connection)
    dpg.add_button(label="Stop Data Collection", callback=stop_connection)
    dpg.add_text(tag="Port",default_value=f"Data Collection is on port {portconfig.port_s}")

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
try:
    os.kill(process_ID, signal.SIGTERM)
    print(f"Process {process_ID} sent SIGTERM signal for graceful termination.")
except OSError as e:
    print(f"Error terminating process {process_ID}: {e}")
dpg.destroy_context()