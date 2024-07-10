### The source code of the PyOpenInstall project ###
# If you want to suggest an edit, make a pull request to database.json
# Contributions to the source code are welcome!
import json
import requests
import os
from os.path import expanduser
import zipfile

home = expanduser("~")

try:
    with open('database.json') as datafile:
        database = json.load(datafile)
except FileNotFoundError:
    print('Database not found.\nIt looks like that you deleted it.\nYou can install it from the PyOpenInstall project.')
    quit()
except json.JSONDecodeError:
    print('Database not valid.\nIt looks like that you edited it.\nYou can delete the database.json file then install it from the PyOpenInstal project.')
    quit()

option = int(input("""
            Welcome
Welcome to the PyOpenInstall project!
If you want to install a module: enter 1

If you want to uninstall a module: enter 2

If you want to update a module: enter 4

If you want to update PyOpenInstall: enter 5

Enter your option: """))

def find_module_by_name(name):
    for module in database:
        if module['name'] == name:
            return 0, module
    return 1, 'MODULE NOT FOUND'

if option == 1:
    module = input('Name: ')
    try:
        status, target = find_module_by_name(module)
        if status == 1:
            print(target)
            quit()
        link = target['link']
        print('Reading module data...')
        response = requests.get(link, headers={'User-Agent': 'PyOpenInstall'})
        path = home+'/PyOpenInstall/'+target['name']+'-zip'+'.zip'
        with open(path, 'wb') as file:
            file.write(response.content)

        # unzip the downloaded file
        with zipfile.ZipFile(path, 'r') as zip_ref:
            zip_ref.extractall(target['name']+'-repo')
        master = f"{target['name']}-repo/{target['name']}-master/{target['name']}"
        if os.name == 'posix':
            os.system(f'mv "{master}" "{target["name"]}"')
        elif os.name == 'nt':
            os.system(f'move "{master}" "{target["name"]}"')
        else:
            print("OS NOT DETECTED")
            quit()
        os.remove(master)
        print('Module Saved')

        
    except requests.ConnectionError:
        print('CONNECTION FAILED')
        quit()
    except KeyError:
        print('Database not valid.\nIt looks like that you edited it.\nYou can delete the database.json file then install it from the PyOpenInstal project.')