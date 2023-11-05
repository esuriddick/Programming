#*****************************************************************************#
# RESOURCES
#*****************************************************************************#
#https://github.com/Microsoft/DirectXTex/wiki/Texconv
#https://stackoverflow.com/questions/42467735/how-to-convert-dx10-dds-image-to-png-using-directxtex

#*****************************************************************************#
# MODULES
#*****************************************************************************#
#Main
import subprocess
import os
import shutil

#Krita
from krita import *
from PyQt5.QtWidgets import (QMessageBox
                             ,QFileDialog
                             ,QDialog
                             ,QWidget
                             ,QGridLayout
                             ,QVBoxLayout
                             ,QLabel
                             ,QComboBox
                             ,QCheckBox
                             ,QPushButton)

#*****************************************************************************#
# MAIN CODE
#*****************************************************************************#

class dds_exporter(Extension):

    def __init__(self, parent):
        # This is initialising the parent, always important when subclassing.
        super().__init__(parent)

    def setup(self):
        pass

    def createActions(self, window):
        action = window.createAction("ER_DDS_EXPORTER", "Export as DDS", "tools/scripts")
        action.triggered.connect(self.exportDocument)       
        
    def exportDocument(self):
        # Get the document:
        doc =  Krita.instance().activeDocument()
        
        # Saving a non-existent document causes crashes, so lets check for that first.
        if doc is not None:
            # File Dialog Window
            output_file = QFileDialog().getSaveFileName(caption = "Save file"
                                                             ,filter = "DDS files (*.dds)")[0]
            
            if output_file != '':

                #Settings
                ##Create base grid
                cWidget = QWidget()
                grid = QGridLayout(cWidget) 
                
                ##Create layout
                vBox_left = QVBoxLayout()
                vBox_right = QVBoxLayout()
                
                ##Intermediate conversion format
                temp_file_format_label = QLabel('Intermediate format:')
                vBox_left.addWidget(temp_file_format_label)
                temp_file_format = QComboBox()
                temp_file_format.addItems(['TGA'
                                           ,'PNG'
                                           ,'TIF'])
                temp_file_format.setCurrentIndex(0)
                vBox_right.addWidget(temp_file_format)
                
                ##Compression type
                compression_type_label = QLabel('Compression type:')
                vBox_left.addWidget(compression_type_label)
                compression_type = QComboBox()
                compression_type_options = ['BC1_UNORM (DXT1)'
                                            ,'BC1_UNORM_SRGB'
                                            ,'BC2_UNORM (DXT3)'
                                            ,'BC2_UNORM_SRGB'
                                            ,'BC3_UNORM (DXT5)'
                                            ,'BC3_UNORM_SRGB'
                                            ,'BC4_UNORM'
                                            ,'BC4_SNORM'
                                            ,'BC5_UNORM'
                                            ,'BC5_SNORM'
                                            ,'BC6H_UF16'
                                            ,'BC6H_SF16'
                                            ,'BC7_UNORM (DXT10)'
                                            ,'BC7_UNORM_SRGB']
                compression_type.addItems(compression_type_options)
                default_compression_option = 'BC7_UNORM (DXT10)'
                for default_compression_index in range(len(compression_type_options)):
                    if compression_type_options[default_compression_index] == default_compression_option:
                        break
                compression_type.setCurrentIndex(default_compression_index)
                vBox_right.addWidget(compression_type)
                
                ##Alpha channel(s)
                alpha_channels_label = QLabel('Use single alpha channel?')
                vBox_left.addWidget(alpha_channels_label)
                alpha_channels = QCheckBox()
                alpha_channels.setText('Yes')
                alpha_channels.setChecked(True)
                vBox_right.addWidget(alpha_channels)
                
                ##MIP maps generation
                generate_mipmaps_label = QLabel('Generate MIP maps?')
                vBox_left.addWidget(generate_mipmaps_label)
                generate_mipmaps = QCheckBox()
                generate_mipmaps.setText('Yes')
                generate_mipmaps.setChecked(True)
                vBox_right.addWidget(generate_mipmaps)
                
                ##Force headers to file
                force_DX_header_label = QLabel('Force header:')
                vBox_left.addWidget(force_DX_header_label)
                force_DX_header = QComboBox()
                force_DX_header.addItems(['None'
                                          ,'DX9'
                                          ,'DX10'])
                force_DX_header.setCurrentIndex(0)
                vBox_right.addWidget(force_DX_header)
                
                #Buttons
                Confirm_Button = QPushButton("Save") 
                vBox_right.addWidget(Confirm_Button)
                Cancel_Button = QPushButton("Cancel") 
                vBox_left.addWidget(Cancel_Button)
                
                ##Attach layouts to grid
                grid.addLayout(vBox_left, 0, 0)
                grid.addLayout(vBox_right, 0, 1)
                
                
                ##Buttons functionality
                def Confirm_Button_Clicked():
                    if alpha_channels.isChecked() == True:
                        alpha_channels_command = '-pmalpha'
                    else:
                        alpha_channels_command = '-alpha'
                    if generate_mipmaps.isChecked() == True:
                        generate_mipmaps_command = '-m 0'
                    else:
                        generate_mipmaps_command = '-m 1'
                    temp_file_format_command = temp_file_format.currentText()
                    compression_type_command = compression_type.currentText().split(' (')[0]
                    if compression_type.currentText().split(' (')[0].split('_')[-1].upper() == 'SRGB':
                        colorspace_command = '-srgb'
                    else:
                        colorspace_command = ''
                    if force_DX_header.currentText() == 'None':
                        force_DX_header_command = ''
                    elif force_DX_header.currentText() == 'DX9':
                        force_DX_header_command = '-dx9'
                    elif force_DX_header.currentText() == 'DX10':
                        force_DX_header_command = '-dx10'
                    settings_window.done(0)
                    
                    #Create temporary directory
                    temp_directory_location = os.path.join(os.path.dirname(__file__), 'erase')
                    if not os.path.isdir(temp_directory_location):
                        os.makedirs(temp_directory_location)
                    
                    #Save document in an intermediate format temporarily
                    temp_file_extension = '.' + temp_file_format_command.lower()
                    output_file_name = os.path.splitext(os.path.basename(output_file))[0]
                    temp_file_path = os.path.join(temp_directory_location, output_file_name + temp_file_extension)
                    doc.saveAs(temp_file_path)
                    
                    #Command Line
                    converter_path = os.path.join(os.path.dirname(__file__), 'resources', 'texconv.exe')
                    output_file_path = os.path.dirname(output_file)
                    args = [converter_path
                            ,"-y"
                            ,"-ft"
                            ,"DDS"
                            ,"-f"
                            ,compression_type_command
                            ,colorspace_command
                            ,alpha_channels_command
                            ,generate_mipmaps_command
                            ,force_DX_header_command
                            ,"-o"
                            ,output_file_path
                            ,temp_file_path]
                    while '' in args:
                        args.remove('')
                    argline = " ".join(args)
                    for i in [converter_path, output_file_path, temp_file_path]:
                        argline = argline.replace(i, '"' + i + '"')
                    
                    #Convert document
                    try:
                        subprocess.run(argline
                                       ,shell = True
                                       ,check = True)
                    except subprocess.CalledProcessError as e:
                        shutil.rmtree(temp_directory_location)
                        messageBox = QMessageBox()
                        messageBox.setWindowTitle('An error occurred')
                        messageBox.setIcon(QMessageBox.Critical)
                        messageBox.setText(f"Krita encountered the following error: {e}")
                        messageBox.setStandardButtons(QMessageBox.Close)
                        messageBox.exec()
                        
                    #Clean temporary file(s) and folder
                    shutil.rmtree(temp_directory_location)
                    
                def Cancel_Button_Clicked():
                    settings_window.done(1)
                    
                Confirm_Button.clicked.connect(Confirm_Button_Clicked)
                Cancel_Button.clicked.connect(Cancel_Button_Clicked)
                
                ##Create window and show it
                settings_window = QDialog() 
                settings_window.setLayout(grid)
                settings_window.setWindowTitle("DDS Export Settings") 
                settings_window.exec_()

        else:
            messageBox = QMessageBox()
            messageBox.setWindowTitle('No active document open')
            messageBox.setIcon(QMessageBox.Warning)
            messageBox.setText("Krita was unable to detect any open document.")
            messageBox.setStandardButtons(QMessageBox.Close)
            messageBox.exec()