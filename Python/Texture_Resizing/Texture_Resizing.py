#-----------------------------------------------------------------------------#
# REQUIREMENTS (PYTHON 3.11.9)
#-----------------------------------------------------------------------------#
#!pip install Pillow==10.4.0

#-----------------------------------------------------------------------------#
# MODULES
#-----------------------------------------------------------------------------#
from PIL import Image
import os
import tkinter as tk                       #Basic UI
from tkinter import ttk                    #Improved UI elements
from tkinter import filedialog as fd       #File dialog window

#---------------------------------------------------------------------------#
# GUI
#---------------------------------------------------------------------------#
process_canceled = 0

# Functions
#---------------------------------------------------------------------------#
def close_window():
    global process_canceled
    process_canceled = 1
    root.destroy()
    
def select_input_file():
    filetypes = [
                 ('PNG files', '*.png')
                 ,('TGA files', '*.tga')
                 ,('JPG files', '*.jpg')
                 ,('JPEG files', '*.jpeg')
                 ,('DDS files', '*.dds')
                 ,('All files', '*')
                ]

    filepath = fd.askopenfilename(title = "Select a File"
                                  ,filetypes = filetypes
                                  )
    
    if filepath:
        fp_input_string.set(f"{filepath}")
    else:
        fp_input_string.set('')
        
def texture_resize():
    root.destroy()
    
# Instantiate Window
#---------------------------------------------------------------------------#
root = tk.Tk()

# Window Settings
#---------------------------------------------------------------------------#
root.title('Texture Resizing')

# Grid Settings
#---------------------------------------------------------------------------#
num_rows = 3
num_cols = 4
for i in range(num_rows):
    root.grid_rowconfigure(i, weight = 1)
for j in range(num_cols):
    root.grid_columnconfigure(j, weight = 1)
    
# First column
for row in range(num_rows):
    frame = tk.Frame(root
                     ,borderwidth = 1
                     ,relief = 'solid'
                     ,padx = 10
                     ,pady = 10)
    frame.grid(row = row
               ,column = 0
               ,sticky = 'nsew')
    
    if row == 0:
        label = ttk.Label(frame
                          ,text = 'File')
        label.pack(expand = True)
        
    elif row == 1:
        fp_input_string = tk.StringVar()
        fp_input_string.set('')
        fp_input = ttk.Label(frame
                             ,textvariable = fp_input_string)
        fp_input.pack(expand = True)
        
# Second column
for row in range(num_rows):
    frame = tk.Frame(root
                     ,borderwidth = 1
                     ,relief = 'solid'
                     ,padx = 10
                     ,pady = 10)
    frame.grid(row = row
               ,column = 1
               ,sticky = 'nsew')
    
    if row == 0:
        label = ttk.Label(frame
                          ,text = '')
        label.pack(expand = True)
        
    elif row == 1:
        button_fp_input = ttk.Button(frame
                                     ,text = 'Select File'
                                     ,command = select_input_file)
        button_fp_input.pack(expand = True)

# Third column
for row in range(num_rows):
    frame = tk.Frame(root
                     ,borderwidth = 1
                     ,relief = 'solid'
                     ,padx = 10
                     ,pady = 10)
    frame.grid(row = row
               ,column = 2
               ,sticky = 'nsew')
    
    if row == 0:
        label = ttk.Label(frame
                          ,text = 'New Size')
        label.pack(expand = True)
        
    elif row == 1:
        options_01 = [2 ** x for x in range(4, 14)] # Goes from 16 to 8192 (8K)
        resize_value = tk.StringVar()
        resize_value.set('16')
        resize = ttk.Combobox(frame
                              ,textvariable = resize_value)
        resize['values'] = options_01
        resize.pack(expand = True)
        
    elif row == 2:
        button_cancel = ttk.Button(frame
                                   ,text = 'Cancel'
                                   ,command = close_window)
        button_cancel.pack(expand = True)
        
# Fourth column
for row in range(num_rows):
    frame = tk.Frame(root
                     ,borderwidth = 1
                     ,relief = 'solid'
                     ,padx = 10
                     ,pady = 10)
    frame.grid(row = row
               ,column = 3
               ,sticky = 'nsew')
    if row == 0:
        label = ttk.Label(frame
                          ,text = 'Resampling method')
        label.pack(expand = True)
    
    elif row == 1:
        options_02 = ['Bilinear', 'Nearest', 'Bicubic', 'Lanczos']
        reasample_value = tk.StringVar()
        reasample_value.set('Bilinear')
        resample = ttk.Combobox(frame
                                ,textvariable = reasample_value)
        resample['values'] = options_02
        resample.pack(expand = True)
    
    elif row == 2:
        button_submit = ttk.Button(frame
                                   ,text = 'Submit'
                                   ,command = texture_resize)
        button_submit.pack(expand = True)
    
# Launch Window
#---------------------------------------------------------------------------#
root.mainloop()

if fp_input_string.get() == '':
    process_canceled = 1
    
if process_canceled == 0:

    #-------------------------------------------------------------------------#
    # VARIABLES
    #-------------------------------------------------------------------------#
    input_filepath = fp_input_string.get()
    _, input_fileextension = os.path.splitext(input_filepath)
    image_resize_size = int(resize_value.get())
    for i in options_02:
        if i == reasample_value.get():
            if i == 'Bilinear':
                resampling_technique = Image.Resampling.BILINEAR
            elif i == 'Nearest':
                resampling_technique = Image.Resampling.NEAREST
            elif i == 'Bicubic':
                resampling_technique = Image.Resampling.BICUBIC
            elif i == 'Lanczos':
                resampling_technique = Image.Resampling.LANCZOS
    
    #-------------------------------------------------------------------------#
    # RESIZE IMAGE
    #-------------------------------------------------------------------------#
    resized_image = Image.open(input_filepath)
    resized_image.thumbnail(size = (image_resize_size, image_resize_size) # (width, height)
                            ,resample = resampling_technique)
        
    #-------------------------------------------------------------------------#
    # FINAL WINDOW
    #-------------------------------------------------------------------------#
    
    # Functions
    #---------------------------------------------------------------------------#
    def preview_image():
        resized_image.show()
        
    def save_image():
        filetypes = [('TGA files', '*.tga')
                     ,('PNG files', '*.png')
                     ,('All files', '*.*')]
        file_path = fd.asksaveasfilename(defaultextension = '.tga'
                                         ,filetypes = filetypes)
        if file_path:
            resized_image.save(file_path)
    
    # Instantiate Window
    #-------------------------------------------------------------------------#
    root = tk.Tk()
    
    # Window Settings
    #-------------------------------------------------------------------------#
    root.title('Texture Resizing')
    root.geometry('200x150')
    
    # Grid Settings
    #-------------------------------------------------------------------------#
    for i in range(2):  # 2 rows
        root.grid_rowconfigure(i, weight = 1)
    for j in range(1):  # 1 columns
        root.grid_columnconfigure(j, weight = 1)
        
    # First column
    for row in range(2):
        frame = tk.Frame(root
                         ,borderwidth = 1
                         ,relief = 'solid'
                         ,padx = 10
                         ,pady = 10)
        frame.grid(row = row
                   ,column = 0
                   ,sticky = 'nsew')
        if row == 0:
            button_preview = ttk.Button(frame
                                        ,text = 'Preview image'
                                        ,command = preview_image)
            button_preview.pack(expand = True)
        else:
            button_save = ttk.Button(frame
                                     ,text = 'Save image'
                                     ,command = save_image)
            button_save.pack(expand = True)
            
    # Launch Window
    #---------------------------------------------------------------------------#
    root.mainloop()
    
#!auto-py-to-exe