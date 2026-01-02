import dearpygui.dearpygui as dpg
import signal
import os
import subprocess
import json

dpg.create_context()
with dpg.theme() as menu_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg, (200, 0, 0, 255)) #menu bar color
        dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255, 255)) #text color

dpg.create_viewport(title='JukBox Geophone Setup',width=500,height=300,min_height=300,min_width=300,resizable=False)
process_ID = 0
with open("station.json",'r') as file:
    data = json.load(file)

def set_url():
    global data
    with open("station.json",'w') as file:
        data['network'] =  dpg.get_value("url_part1")
        data['station'] =  dpg.get_value("url_part2")
        data['location'] = dpg.get_value("url_part3")
        data['channel'] =  dpg.get_value("url_part4")
        dpg.set_value("stat_name",f"Station Name: {data['network']}.{data['station']}.{data['location']}.{data['channel']}")
        json.dump(data,file,indent=4)

def port_5678():
    global data
    with open("station.json",'w') as file:
        if(dpg.get_value(5678)==False):
            data['port']=443
            dpg.set_value("Port",f"Data Collection is on port {data['port']}")
        else:
            data['port'] = 5678
            dpg.set_value("Port",f"Data Collection is on port {data['port']}")
        json.dump(data,file,indent=4)

def custom_port():
    global data
    with open("station.json",'w') as file:
        data['port'] = dpg.get_value("customPort")
        dpg.set_value("Port",f"Data Collection is on port {data['port']}")
        json.dump(data,file,indent=4)

def start_connection(sender):
    global process_ID
    global data
    print(f"Button {sender} has been clicked, starting connection on port {data['port']}!")
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
        with dpg.menu(label="Settings"):
            with dpg.menu(label="Change Active Port"):
                dpg.add_text("Default Value: 443")
                dpg.add_menu_item(tag=5678,label="Set to 5678", callback=port_5678, check=True)
                dpg.add_text("Custom Port:")
                dpg.add_input_int(tag="customPort",min_clamped=True,min_value=0,callback=custom_port)
            with dpg.menu(label="Change Station Name"):
                dpg.add_text(tag="stat_name", default_value=f"Station Name: {data['network']}.{data['station']}.{data['location']}.{data['channel']}")
                with dpg.group(horizontal=True):
                    for i in range(1, 5):
                        dpg.add_input_text(
                            tag=f"url_part{i}",
                            width=40,
                            decimal=False
                        )
                        if i < 4:
                            dpg.add_text(".")        
                dpg.add_button(label="Enter",callback=set_url)

    dpg.add_text("Welcome to JukBox!")
    dpg.add_text(tag=1,default_value="There is no active connection.")
    dpg.add_button(label="Start Data Collection", callback=start_connection)
    dpg.add_button(label="Stop Data Collection", callback=stop_connection)
    dpg.add_text(tag="Port",default_value=f"Data Collection is on port {data['port']}")

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
try:
    os.kill(process_ID, signal.SIGTERM)
    print(f"Process {process_ID} sent SIGTERM signal for graceful termination.")
except OSError as e:
    print(f"Error terminating process {process_ID}: {e}")
dpg.destroy_context()