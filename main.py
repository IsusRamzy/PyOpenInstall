# 0.0.3 Dev

### The source code of the PyOpenInstall project ###
# If you want to suggest an edit, make a pull request to database.json
# Contributions to the source code are welcome!
import json
import requests
import os
from os.path import expanduser
import zipfile
import sys

pyversion = sys.version_info
home = expanduser("~")
pypath = f'{home}/.local/lib/python{pyversion.major}.{pyversion.minor}/site-packages'

try:
    database = requests.get('https://raw.githubusercontent.com/IsusRamzy/PyOpenInstall/master/database.json').text
except requests.ConnectionError:
    print('CONNECTION FAILED')
    quit()
except json.JSONDecodeError:
    print('Database not valid.\nIt looks like that you edited it.\nYou can delete the database.json file then install it from the PyOpenInstal project.')
    quit()

option = int(input("""                Welcome
Welcome to the PyOpenInstall project!
If you want to install a module: enter 1

If you want to uninstall a module: enter 2

If you want to update PyOpenInstall: enter 3

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
            zip_ref.extractall(pypath+'/'+module+'-repo')
        master_name = ''
        for root, dirs, files in os.walk(f"{pypath}/{target['name']}-repo"):
            print(dirs)
            master_name = dirs[0]
            break
        
        master = f"{pypath}/{target['name']}-repo/{master_name}/{target['name']}"
        todelete = f"{pypath}/{target['name']}-repo"
        if os.name == 'posix': # Unix-Like: MacOS, Linux, ...
            os.system(f'mv "{master}" "{pypath}/{target["name"]}"')
            os.system(f'rm -rf "{todelete}"')
        elif os.name == 'nt': # Windows
            os.system(f'move "{master}" "{pypath}/{target["name"]}"')
            os.system(f'rmdir "{todelete}"')
        elif os.name == 'java':
            print('You CANNOT RUN PYOPENINSTALL ON JVM')
            quit()
        else:
            print("OS NOT DETECTED")
            quit()
        print('Module Saved')

        
    except requests.ConnectionError:
        print('CONNECTION FAILED')
        quit()
    except KeyError:
        print('Database not valid.\nIt looks like that you edited it.\nYou can delete the database.json file then install it from the PyOpenInstall project.')

elif option == 2:
    module = input('Name: ')
    try:
        os.system(f'rm -rf "{pypath}/{module}"')
        print('Module Deleted')
    except FileNotFoundError:
        print("MODULE NOT FOUND")

elif option == 3:
    try:
        code = requests.get('https://raw.githubusercontent.com/IsusRamzy/PyOpenInstall/master/main.py').text
        version = code.split('\n')[0] # First Line
        with open(__file__) as file:
            current_version = file.read().split('\n')[0]
        if current_version == version:
            print('PyOpenInstall is already the latest version.')
        if 'Stable' in version:
            with open(__file__, 'w') as file:
                file.write(code)
            print(f'PyOpenInstall Updated from {current_version} to {version}')
        elif 'Beta' in version:
            okay = input("This is a beta version, not very stable.\nUpgrade? (Y/n):").lower()
            if okay == 'n':
                print('UPGRADE ABORTED')
            elif okay == 'y':
                with open(__file__, 'w') as file:
                    file.write(code)
                print(f'PyOpenInstall Updated from {current_version} to {version}')
        elif 'Dev' in version:
            okay = input("This is a development version. It's even less stable than beta versions. It may completely break PyOpenInstall.\nDevelopers use it to test upgrades before making them stable. Upgrade? (Y/n):").lower()
            if okay == 'n':
                print('UPGRADE ABORTED')
            elif okay == 'y':
                with open(__file__, 'w') as file:
                    file.write(code)
                print(f'PyOpenInstall Updated from {current_version} to {version}')
    except requests.ConnectionError:
        print('CONNECTION FAILED')
        quit()
