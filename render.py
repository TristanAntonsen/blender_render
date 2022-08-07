import subprocess
import os
from os.path import exists
import argparse

## Blender setup
EXE_PATH_BLENDER = r"C:/Program Files/Blender Foundation/Blender 3.1/blender.exe"  #location of blender on computer\

## Main function to call Blender & run _render_script.py with Blender
def render_with_blender(_file_name, _output_image_name, settings):

    ## creating settings
    if settings['cycles']:
        renderer = 'CYCLES'
    elif settings['workbench']:
        renderer = 'BLENDER_WORKBENCH'
    elif settings['cycles'] and settings['workbench']:
        renderer = 'CYCLES'
    else:
        renderer = 'BLENDER_WORKBENCH'

    if settings['side_view']:
        view = 'side'
    else:
        view = 'front'

    if exists("tmp.txt"):
        os.remove("tmp.txt")

    tmp_file = open("tmp.txt",'w')

    current_dir = os.getcwd()

    file_path = os.path.join(current_dir,_file_name)
    export_path = os.path.join(current_dir,_output_image_name)

    inputList = [file_path,export_path,renderer,view]

    tmp_file.write(','.join(inputList)) # Filepath of stl to read

    if exists("tmp.txt"):
        tmp_file = open('tmp.txt','r')
        subprocess.call([EXE_PATH_BLENDER,'render.blend','--background','--python','_render_script.py'])


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('file_name') # file to render
    parser.add_argument('-f', action='store_true') # argument is directory
    parser.add_argument('-c', action='store_true') # cycles render engine
    parser.add_argument('-w', action='store_true') # workbench render engine
    parser.add_argument('-s', action='store_true') # side view

    args = parser.parse_args()
    file_name = args.file_name.replace("/","\\")
    output_image = file_name.replace('.stl','')

    render_settings = {
        'cycles' : args.c,
        'workbench' : args.w,
        'side_view' : args.s
    }

    if args.f:
        dir = file_name
        files = os.listdir(dir)
        for file in files:
            if '.png' in file:
                continue
            file_path = dir + '\\' + file
            output_path = file_path.replace('.stl','')
            render_with_blender(file_path,output_path,settings=render_settings)
    else:
        render_with_blender(file_name,output_image,settings=render_settings)

    # p = subprocess.Popen(["C:\\Users\\Tristan Antonsen\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe", output_image + ".png"]) ## open preview in VS code