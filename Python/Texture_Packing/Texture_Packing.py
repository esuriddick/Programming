#-----------------------------------------------------------------------------#
# REQUIREMENTS (PYTHON 3.11.9)
#-----------------------------------------------------------------------------#
#!pip install Pillow==10.4.0

#-----------------------------------------------------------------------------#
# MODULES
#-----------------------------------------------------------------------------#
from PIL import Image
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

def select_file_R():
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
        fp_R_string.set(f"{filepath}")
    else:
        fp_R_string.set('')
        
def select_file_G():
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
        fp_G_string.set(f"{filepath}")
    else:
        fp_G_string.set('')
    
def select_file_B():
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
        fp_B_string.set(f"{filepath}")
    else:
        fp_B_string.set('')

def select_file_A():
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
        fp_A_string.set(f"{filepath}")
    else:
        fp_A_string.set('')

def texture_pack():
    root.destroy()

# Instantiate Window
#---------------------------------------------------------------------------#
root = tk.Tk()

# Window Settings
#---------------------------------------------------------------------------#
root.title('Texture Packing')

# Grid Settings
#---------------------------------------------------------------------------#
for i in range(6):  # 6 rows
    root.grid_rowconfigure(i, weight = 1)
for j in range(5):  # 5 columns
    root.grid_columnconfigure(j, weight = 1)
    
# First column
for row in range(6):
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
                          ,text = 'Target Channel')
        label.pack(expand = True)
        
    elif row == 1:
        label = ttk.Label(frame
                          ,text = 'Red')
        label.pack(expand = True)
        
    elif row == 2:
        label = ttk.Label(frame
                          ,text = 'Green')
        label.pack(expand = True)
        
    elif row == 3:
        label = ttk.Label(frame
                          ,text = 'Blue')
        label.pack(expand = True)
        
    elif row == 4:
        label = ttk.Label(frame
                          ,text = 'Alpha')
        label.pack(expand = True)
        
# Second column
for row in range(6):
    options = ['Grayscale', 'Red', 'Green', 'Blue', 'Alpha']
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
                          ,text = 'Source Channel')
        label.pack(expand = True)
        
    elif row == 1:
        source_R_value = tk.StringVar()
        source_R_value.set('Grayscale')
        source_R = ttk.Combobox(frame
                                ,textvariable = source_R_value)
        source_R['values'] = options
        source_R.pack(expand = True)
        
    elif row == 2:
        source_G_value = tk.StringVar()
        source_G_value.set('Grayscale')
        source_G = ttk.Combobox(frame
                                ,textvariable = source_G_value)
        source_G['values'] = options
        source_G.pack(expand = True)
        
    elif row == 3:
        source_B_value = tk.StringVar()
        source_B_value.set('Grayscale')
        source_B = ttk.Combobox(frame
                                ,textvariable = source_B_value)
        source_B['values'] = options
        source_B.pack(expand = True)
        
    elif row == 4:
        source_A_value = tk.StringVar()
        source_A_value.set('Grayscale')
        source_A = ttk.Combobox(frame
                                ,textvariable = source_A_value)
        source_A['values'] = options
        source_A.pack(expand = True)

# Third column
for row in range(6):
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
                          ,text = 'File')
        label.pack(expand = True)
        
    elif row == 1:
        fp_R_string = tk.StringVar()
        fp_R_string.set('')
        fp_R = ttk.Label(frame
                         ,textvariable = fp_R_string)
        fp_R.pack(expand = True)
        
    elif row == 2:
        fp_G_string = tk.StringVar()
        fp_G_string.set('')
        fp_G = ttk.Label(frame
                         ,textvariable = fp_G_string)
        fp_G.pack(expand = True)
        
    elif row == 3:
        fp_B_string = tk.StringVar()
        fp_B_string.set('')
        fp_B = ttk.Label(frame
                         ,textvariable = fp_B_string)
        fp_B.pack(expand = True)
        
    elif row == 4:
        fp_A_string = tk.StringVar()
        fp_A_string.set('')
        fp_A = ttk.Label(frame
                         ,textvariable = fp_A_string)
        fp_A.pack(expand = True)

# Fourth column
for row in range(6):
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
                          ,text = '')
        label.pack(expand = True)
        
    elif row == 1:
        button_fp_R = ttk.Button(frame
                                 ,text = 'Select File'
                                 ,command = select_file_R)
        button_fp_R.pack(expand = True)
        
    elif row == 2:
        button_fp_G = ttk.Button(frame
                                 ,text = 'Select File'
                                 ,command = select_file_G)
        button_fp_G.pack(expand = True)
        
    elif row == 3:
        button_fp_B = ttk.Button(frame
                                 ,text = 'Select File'
                                 ,command = select_file_B)
        button_fp_B.pack(expand = True)
        
    elif row == 4:
        button_fp_A = ttk.Button(frame
                                 ,text = 'Select File'
                                 ,command = select_file_A)
        button_fp_A.pack(expand = True)
        
    elif row == 5:
        button_cancel = ttk.Button(frame
                                   ,text = 'Cancel'
                                   ,command = close_window)
        button_cancel.pack(expand = True)
        
# Fifth column
for row in range(6):
    frame = tk.Frame(root
                     ,borderwidth = 1
                     ,relief = 'solid'
                     ,padx = 10
                     ,pady = 10)
    frame.grid(row = row
               ,column = 4
               ,sticky = 'nsew')
    
    if row == 0:
        label = ttk.Label(frame
                          ,text = 'Black?')
        label.pack(expand = True)
        
    elif row == 1:
        checkbox_R_var = tk.BooleanVar()
        checkbox_R_var.set(True)
        checkbox_R = ttk.Checkbutton(frame
                                     ,variable = checkbox_R_var)
        checkbox_R.pack(expand = True)
        
    elif row == 2:
        checkbox_G_var = tk.BooleanVar()
        checkbox_G_var.set(True)
        checkbox_G = ttk.Checkbutton(frame
                                     ,variable = checkbox_G_var)
        checkbox_G.pack(expand = True)
        
    elif row == 3:
        checkbox_B_var = tk.BooleanVar()
        checkbox_B_var.set(True)
        checkbox_B = ttk.Checkbutton(frame
                                     ,variable = checkbox_B_var)
        checkbox_B.pack(expand = True)
        
    elif row == 5:
        button_submit = ttk.Button(frame
                                   ,text = 'Submit'
                                   ,command = texture_pack)
        button_submit.pack(expand = True)

# Launch Window
#---------------------------------------------------------------------------#
root.mainloop()

if fp_R_string.get() == '' and fp_G_string.get() == '' and fp_B_string.get() == '' and fp_A_string.get() == '':
    process_canceled = 1

if process_canceled == 0:

    #-------------------------------------------------------------------------#
    # VARIABLES
    #-------------------------------------------------------------------------#
    list_channels = ['R'
                     ,'G'
                     ,'B'
                     ,'A']
    
    list_filepaths = [fp_R_string.get()
                      ,fp_G_string.get()
                      ,fp_B_string.get()
                      ,fp_A_string.get()]
    
    list_source_channels = [source_R_value.get()
                            ,source_G_value.get()
                            ,source_B_value.get()
                            ,source_A_value.get()]
    
    list_black_filled = [checkbox_R_var.get()
                         ,checkbox_G_var.get()
                         ,checkbox_B_var.get()]
    
    list_extracted_channels = []
    
    for i in list_filepaths:
        if i != '' and i is not None:
            image = Image.open(i)
            width, height = image.size
            break
    
    #-------------------------------------------------------------------------#
    # EXTRACT CHANNELS
    #-------------------------------------------------------------------------#
    for i in range(len(list_channels)):
        if list_filepaths[i] != '' and list_filepaths[i] is not None:
            image = Image.open(list_filepaths[i])
            if list_source_channels[i] != 'Grayscale':
                list_extracted_channels.append(image.getchannel(list_source_channels[i][0]))
            else:
                list_extracted_channels.append(image.convert('L'))
        else:
            if i != 3:
                if list_black_filled[i]:
                    list_extracted_channels.append(Image.new('L'
                                                             ,(width, height)
                                                             ,color = 'black'))
                else:
                    list_extracted_channels.append(Image.new('L'
                                                             ,(width, height)
                                                             ,color = 'white'))
    
    #-------------------------------------------------------------------------#
    # MERGE CHANNELS
    #-------------------------------------------------------------------------#
    if len(list_extracted_channels) < 4:
        mode = 'RGB'
        new_image = Image.merge(mode
                                ,(list_extracted_channels[0]
                                ,list_extracted_channels[1]
                                ,list_extracted_channels[2]))
    else:
        mode = 'RGBA'
        new_image = Image.merge(mode
                                ,(list_extracted_channels[0]
                                ,list_extracted_channels[1]
                                ,list_extracted_channels[2]
                                ,list_extracted_channels[3]))
        
    #-------------------------------------------------------------------------#
    # FINAL WINDOW
    #-------------------------------------------------------------------------#
    
    # Functions
    #---------------------------------------------------------------------------#
    def preview_image():
        new_image.show()
        
    def save_image():
        filetypes = [('TGA files', '*.tga')
                     ,('PNG files', '*.png')
                     ,('JPG files', '*.jpg')
                     ,('All files', '*.*')]
        file_path = fd.asksaveasfilename(defaultextension = '.tga'
                                         ,filetypes = filetypes)
        if file_path:
            new_image.save(file_path)
    
    # Instantiate Window
    #-------------------------------------------------------------------------#
    root = tk.Tk()
    
    # Window Settings
    #-------------------------------------------------------------------------#
    root.title('Texture Packing')
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
