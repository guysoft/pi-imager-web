#!/usr/bin/python3
import json
import os


def get_path_id(path, output_json):
    for i, item in enumerate(output_json["os_list"]):
        print(item["name"])
        if item["name"] == path:
            return i
    return

def make_unofficial_menu(official):
    unofficial_subitems = []
    official_subsystem = official["os_list"]
    official_entry = {"name": "Official",
                      "description": "The officialy mainained raspberrypi imager repository",
                      "icon": "icons/cat_raspberry_pi_os.png",
                      "subitems": official_subsystem}
    
    unofficial_entry = {"name": "Unfficial",
                    "description": "The community mainained raspberrypi imager repository",
                    "icon": "https://raw.githubusercontent.com/guysoft/pi-imager/qml/icons/cat_unofficialpi.png",
                    "subitems": unofficial_subitems}
    
    os_list = [official_entry, unofficial_entry]
    
    output_json = {"imager": official["imager"], "os_list": os_list}
    return output_json, unofficial_subitems

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Take a folder of pi-imager json files and merge them on to os_list')
    parser.add_argument('input_folder', type=str, help='Input file of json distros')
    parser.add_argument('base_json', type=str, help='Input file of json distros')
    parser.add_argument('output_file', type=str, help='Ouptut of json to be uploaded and published')

    args = parser.parse_args()
    
    # Load base json
    with open(args.base_json) as f:
        official = json.load(f)
    
    output_json, unofficial_subitems = make_unofficial_menu(official)
    
    # Add all the extra distros
    for file_basename in os.listdir(args.input_folder):
        full_name = os.path.join(args.input_folder, file_basename)
        json_data = None
        
        with open(full_name) as f:
            json_data = json.load(f)
          
        # Disable path handeling for now
        # path = json_data["path"][0]
        # for os_list in json_data["os_list"]:
        #     output_json["os_list"][get_path_id(path, output_json)]["subitems"].insert(0, os_list)
        unofficial_subitems.append(json_data["os_list"])
    
    with open(args.output_file, "w") as w:
        json.dump(output_json, w)
    print("Done")
