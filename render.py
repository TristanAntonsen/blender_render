import subprocess
import os
from os.path import exists
import sys
import argparse

## Blender setup
EXE_PATH_BLENDER = r"C:/Program Files/Blender Foundation/Blender 3.1/blender.exe"  #location of blender on computer\

## Main function to call Blender & run _render_script.py with Blender
def render_with_blender(_file_name,_output_image_name):

    if exists("tmp.txt"):
        os.remove("tmp.txt")

    tmp_file = open("tmp.txt",'w')

    current_dir = os.getcwd()

    file_path = os.path.join(current_dir,_file_name)
    export_path = os.path.join(current_dir,_output_image_name)

    inputList = [file_path,export_path]

    tmp_file.write(','.join(inputList)) # Filepath of stl to read

    if exists("tmp.txt"):
        tmp_file = open('tmp.txt','r')
        subprocess.call([EXE_PATH_BLENDER,'render.blend','--background','--python','_render_script.py'])


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('file_name')
    parser.add_argument('-c', action='store_true')
    parser.add_argument('-w', action='store_true')
    args = parser.parse_args()
    file_name = args.file_name
    output_image = file_name.replace('.stl','.png')
    render_with_blender(file_name,output_image)

    p = subprocess.Popen(["C:\\Users\\Tristan Antonsen\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe", output_image]) ## open preview in VS code