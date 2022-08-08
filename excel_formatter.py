from email.mime import image
import openpyxl
from openpyxl.styles import Alignment
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('name') # file to render
args = parser.parse_args()

if args.name:
    workbook_name = f'orientation_feedback_{args.name}.xlsx'
else:
    workbook_name = 'orientation_feedback.xlsx'


IMAGE_WIDTH = 190
COLUMN_WIDTH = 25.74 #dumb
ROW_HEIGHT = 150



def Insert_Image(ws, path, anchor):
    ## anchor: cell ('A1')
    ## path: image file path'

    img = openpyxl.drawing.image.Image(path)
    img.height = IMAGE_WIDTH
    img.width= IMAGE_WIDTH
    img.anchor = anchor
    ws.add_image(img)

# wb = openpyxl.Workbook() # create a new workbook
wb = openpyxl.load_workbook(filename = 'template.xlsx') # read an existing workbook
ws = wb.worksheets[0]

for i in range(2,100):
    ws.row_dimensions[i].height = ROW_HEIGHT / 3
ws.column_dimensions['A'].width = COLUMN_WIDTH
ws.column_dimensions['B'].width = COLUMN_WIDTH

image_path = 'files/Fake_connector_front.png'

image_files = sorted(os.listdir('images'))

for i, file in enumerate(image_files):
    row = 3 * (i + 2) - 4
    if ("_oriented") in file:
        row -= 3
    if row < 2:
        row = 2
        
    if '.png' not in file:
        continue
    if 'ISO' in file:
        column = 'A'
    elif 'FRONT' in file:
        column = 'B'
    Insert_Image(ws, f"images/{file}",f"{column}{row}") # ORIENTED IMAGE
    current_cell = ws.cell(row=row, column=3)
    current_cell.value = file.replace('_FRONT','').replace('_oriented','').replace('.png','')
    current_cell.alignment = Alignment(horizontal='center', vertical='center')

    ws.merge_cells(f"A{row}:A{row + 2}")
    ws.merge_cells(f"B{row}:B{row + 2}")


# Insert_Image(ws, f"images/Ball Middle - V7A_oriented_FRONT.png",f"A{1}")

wb.save(workbook_name)

os.startfile(workbook_name)
