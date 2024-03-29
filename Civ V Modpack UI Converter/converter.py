########################################################################
#                                                                      #
# © 2021 - MPL 2.0 - Rsge - v2.1.2                                     #
# https://github.com/Rsge/Civ-V-EUI-Modpack-Converter                  #
#                                                                      #
# WINDOWS ONLY!                                                        #
# 7-ZIP NEEDED!                                                        #
# If you want to use WinRar you'll have to change the methods yourself #
# (or just download 7-zip =P)                                          #
#                                                                      #
########################################################################


#------------------------------------------#
# Customize these according to your setup: #
#------------------------------------------#

# Vanilla EUI file (in vanilla_packs_folder)
VANILLA_EUI_ZIP = "!EUI.7z"

# CUC-version file name of EUI
MODDED_EUI_ZIP = "!EUI_CUC.7z"

# Folder containing the vanilla packs in DLC folder
# (Sid Meier's Civilization V\Assets\DLC\ThisVariableAsFolderName)
VANILLA_PACKS_FOLDER = "zz_Vanilla_Versions" 

#-----------------------------------------------------#
# Don't change anything after here                    #
# [except if you know what you're doing of course ;)] #
#-----------------------------------------------------#

# Imports
import os
import winreg as wr
import os.path as p
from os.path import join as j
from glob import glob as g
import subprocess
import shutil
import re


## Functions
print("Defining functions...")
# Closing functions
null = open(os.devnull, 'w')
def quit():
    null.close()
    print("Done.\n")
    input("Press Enter to exit. . .")
    exit(0)
def error(msg):
    null.close()
    print("Error!\n{}\n".format(msg))
    input("Press Enter to exit. . .")
    exit(1)

# Get 7-zip install dir.
def get_szip_dir():
    key_location = r"SOFTWARE\7-Zip"
    value = "Path"
    try:
        key = wr.OpenKey(wr.HKEY_LOCAL_MACHINE, key_location)
        install_dir = wr.QueryValueEx(key, value)[0]
        wr.CloseKey(key)
    except:
        error("No 7-zip installation found!\nIf you insist on using WinRar, change the script yourself ¯\_(ツ)_/¯")
    return install_dir

# Get Civ V install dir.
def get_civ_install_dir():
    key_location = r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\steam app 8930"
    value = "installlocation"
    try:
        key = wr.OpenKey(wr.HKEY_LOCAL_MACHINE, key_location)
        install_dir = wr.QueryValueEx(key, value)[0]
        wr.CloseKey(key)
    except:
        error("No Civ 5 installation found!")
    return install_dir

# Unzip using 7-zip.
def unzip(file_path):
    subprocess.run([szip, 'x', file_path], stdout=null, stderr=null)
def zip(dir_path, file_path):
    subprocess.run([szip, 'a', dir_path, file_path], stdout=null, stderr=null)

## Global values
print("Configuring variables...")
# Names
MODPACK_DIR_NAME = "MP_MODSPACK"
PRESERVATION_EXTENSION = ".orig"
LOAD_TAG_MARKER = "ContextPtr:LoadNewContext"
UNIT_PANEL_TAG = "LuaEvents.UnitPanelActionAddin"
UNIT_PANEL_INSERT_MARKER = "--Insert ContextPtr for modded unit panel buttons here\n"
EUI_CUC_FILE_NAME = ["CityBannerManager.lua",
                      "CityView.lua",
                      "Highlights.xml"]
UNIT_PANEL_FILE_NAME = "UnitPanel.lua"
IGE_COMPAT_FILE_NAME = "IGE_Window.lua"
# Paths
szip = j(get_szip_dir(), "7z.exe")
modsave_path = j(os.getcwd(), "..")
base_path = j(get_civ_install_dir(), "Assets", "DLC")
vanilla_packs_path =  j(base_path, VANILLA_PACKS_FOLDER)
eui_folder_path = j(base_path, "UI_bc1")
modpack_path = j(base_path, MODPACK_DIR_NAME)
mods_path = j(modpack_path, "Mods")
ui_folder_path = j(modpack_path, "UI")
# Files
FILE_EXT = "*.lua"
file_ext_recursive = j("**", FILE_EXT)
vanilla_eui_zip_path = j(vanilla_packs_path, VANILLA_EUI_ZIP)
modded_eui_zip_path = j(base_path, MODDED_EUI_ZIP)
base_ui_files = j(base_path, "..", "UI", file_ext_recursive)
gnk_ui_files = j(base_path, "Expansion", "UI", file_ext_recursive)
bnw_ui_files = j(base_path, "Expansion2", "UI", file_ext_recursive)
mod_files = j(mods_path, file_ext_recursive)
ui_files = j(ui_folder_path, FILE_EXT)
eui_files = j(eui_folder_path, file_ext_recursive)

# Global variables
eui_only = False
vanilla_ui_file_names = []
unit_panel_addon_file_names = []
load_tags = {}


# Change working dir to base path.
os.chdir(base_path)

# Get modpack zip.
while True:
    modpack_name = input("\nWhich pack should be converted?\n(Type 'EUI' to just convert EUI)\n")
    if modpack_name == "EUI":
        eui_only = True
        break
    modpack_zips = g(j(vanilla_packs_path, modpack_name + ".*"))
    if len(modpack_zips) > 0:
        modpack_zip = modpack_zips[0]
        break
    print("This file doesn't exist, try again.")
print("")

# Remove previous modpack.
print("Removing previous modpack and EUI leftovers...")
if os.path.isdir(modpack_path):
    shutil.rmtree(modpack_path)
if os.path.isdir(eui_folder_path):
    shutil.rmtree(eui_folder_path)


# Compile EUI with colored unlocked citizens.
if not os.path.isfile(modded_eui_zip_path):
    print("Creating colored unlocked citizens EUI...")
    unzip(vanilla_eui_zip_path)
    for eui_cuc_file_name in EUI_CUC_FILE_NAME:
        eui_cuc_file = g(j(modsave_path, eui_cuc_file_name + "*"))[0]
        orig_eui_file = g(j(eui_folder_path, "*", eui_cuc_file_name))[0]
        shutil.move(orig_eui_file, orig_eui_file + PRESERVATION_EXTENSION)
        shutil.copyfile(eui_cuc_file, orig_eui_file)
    zip(MODDED_EUI_ZIP, eui_folder_path)
else:
    # Unzip EUI
    print("Unzipping EUI...")
    unzip(modded_eui_zip_path)

# Stop here if only EUI should be converted.
if eui_only:
    quit()


# Unzip modpack zip.
print("Unzipping Modpack...")
unzip(j(vanilla_packs_path, modpack_zip))


# Get vanilla UI files.
print("Gathering Vanilla UI file list...")
globbed = g(base_ui_files, recursive=True)
globbed.extend(g(gnk_ui_files, recursive=True))
globbed.extend(g(bnw_ui_files, recursive=True))
for file in globbed:
    file_name = p.basename(file)
    if not file_name in ui_files:
        vanilla_ui_file_names.append(file_name)

# Manage mod files.
print("Managing mod's files:")
for mod_file in g(mod_files, recursive = True):
    mod_file_name = p.basename(mod_file)
    mod_file_short_path = mod_file.removeprefix(mods_path + os.sep)
    # IGE UI compat file
    if mod_file_name == IGE_COMPAT_FILE_NAME:
        print("\tProviding IGE-EUI-compat...")
        shutil.move(mod_file, mod_file + PRESERVATION_EXTENSION)
        shutil.copyfile(g(j(modsave_path, IGE_COMPAT_FILE_NAME + "*"))[0], mod_file)
    # Delete UI overwrite duplicates.
    elif mod_file_name in vanilla_ui_file_names:
        print('\tRemoving overwriting file "{}"...'.format(mod_file_short_path))
        os.remove(mod_file)
    # Get unit panel addon files.
    else:
        with open(mod_file, 'r') as file:
            lines = file.readlines()
        for line in lines:
            if UNIT_PANEL_TAG in line:
                print('\tDetecting unit panel addon in file "{}"...'.format(mod_file_short_path))
                unit_panel_addon_file_names.append(mod_file_name)
                break


# Delete useless desktop.ini. (Thanks True...)
ini_files = re.sub(r"\.\w+$", ".ini", mod_files)
for ini_file in g(ini_files, recursive = True):
    ini_file_name = p.basename(ini_file)
    if ini_file_name == "desktop.ini":
        print("Removing useless desktop.ini (Thanks True)...")
        os.remove(mod_file)


# Get stuff from UI files.
for ui_file in g(ui_files):        
    ui_file_name = p.basename(ui_file)
    print("Getting tags from modpack UI's " + ui_file_name + "...")
    load_tags[ui_file_name] = []
    with open(ui_file, 'r') as file:
        lines = file.readlines()
    for line in lines:
        if line.startswith(LOAD_TAG_MARKER):
            load_tags[ui_file_name].append(line)

# Insert stuff into EUI files.
for eui_file in g(eui_files):
    eui_file_name = p.basename(eui_file)
    # Base UI files
    if eui_file_name in load_tags.keys():
        print("Writing tags to EUI's " + eui_file_name + "...")
        with open(eui_file, 'a') as file:
            file.write('\n')
            for load_tag in load_tags[eui_file_name]:
                file.write(load_tag)
    # Modcompat unit panel
    elif eui_file_name == UNIT_PANEL_FILE_NAME and len(unit_panel_addon_file_names) > 0:
        print("Providing EUI-UnitPanel-Modcompat...")
        unit_panel_load_tags = ""
        for unit_panel_addon_file_name in unit_panel_addon_file_names:
            unit_panel_load_tags += '{}("{}")\n'.format(LOAD_TAG_MARKER, p.splitext(unit_panel_addon_file_name)[0])
        shutil.move(eui_file, eui_file + PRESERVATION_EXTENSION)
        shutil.copyfile(g(j(modsave_path, UNIT_PANEL_FILE_NAME + "*"))[0], eui_file)
        with open(eui_file, 'r') as file:
            lines = file.readlines()
        lines[lines.index(UNIT_PANEL_INSERT_MARKER)] = unit_panel_load_tags
        with open(eui_file, 'w') as file:
            file.write("".join(lines))


# Move EUI folder.
print("Moving EUI folder...")
shutil.move(eui_folder_path, modpack_path)
print("Removing UI folder...")
shutil.rmtree(ui_folder_path)

# Zip modpack folder.
print("Zipping Modpack...")
zip(modpack_name + "_EUI.7z", modpack_path)

# Finish up.
quit()