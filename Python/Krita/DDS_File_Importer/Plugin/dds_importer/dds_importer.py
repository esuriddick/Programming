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

#Linux
from sys import platform

#*****************************************************************************#
# MAIN CODE
#*****************************************************************************#

class dds_importer(Extension):

    def __init__(self, parent):
        # This is initialising the parent, always important when subclassing.
        super().__init__(parent)

    def setup(self):
        pass

    def createActions(self, window):
        action = window.createAction("ER_DDS_IMPORTER", "Import DDS", "tools/scripts")
        action.triggered.connect(self.importDocument)       
        
    def importDocument(self):
        
        # File Dialog Window
        input_file = QFileDialog().getOpenFileName(caption = "Select file"
                                                   ,filter = "DDS files (*.dds)")[0]
        
        if input_file != '':
            
            #Settings
            ##Create base grid
            cWidget = QWidget()
            grid = QGridLayout(cWidget) 
            
            ##Create layout
            vBox_left = QVBoxLayout()
            vBox_right = QVBoxLayout()
            
            ##Import format
            import_format_label = QLabel('Format:')
            vBox_left.addWidget(import_format_label)
            import_format = QComboBox()
            import_format.addItems(['TGA'
                                    ,'PNG'
                                    ,'TIF'])
            import_format.setCurrentIndex(0)
            vBox_right.addWidget(import_format)
            
            #Buttons
            Confirm_Button = QPushButton("Import") 
            vBox_right.addWidget(Confirm_Button)
            Cancel_Button = QPushButton("Cancel") 
            vBox_left.addWidget(Cancel_Button)
            
            ##Attach layouts to grid
            grid.addLayout(vBox_left, 0, 0)
            grid.addLayout(vBox_right, 0, 1)
            
            ##Buttons functionality
            def Confirm_Button_Clicked():
                import_format_command = import_format.currentText()
                settings_window.done(0)
                
                #Create temporary directory
                temp_directory_location = os.path.join(os.path.dirname(__file__), 'erase')
                if not os.path.isdir(temp_directory_location):
                    os.makedirs(temp_directory_location)
                    
                #Command Line
                converter_path = os.path.join(os.path.dirname(__file__), 'resources', 'texconv.exe')
                args = [converter_path
                        ,"-y"
                        ,"-ft"
                        ,import_format_command
                        ,"-f"
                        ,'R8G8B8A8_UNORM'
                        ,'-srgb'
                        ,'-m 1'
                        ,"-o"
                        ,temp_directory_location
                        ,input_file]
                while '' in args:
                    args.remove('')
                argline = ("wine " if platform != "win32" else '') + " ".join(args)
                for i in [converter_path, temp_directory_location, input_file]:
                    if platform != "win32":
                        argline = argline.replace(i, '"$(winepath -w \'' + i + '\')"')
                    else:
                        argline = argline.replace(i, '"' + i + '"')
                    
                #Create document from DDS
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
                    
                #Open file in Krita
                try:
                    input_file_name = os.path.splitext(os.path.basename(input_file))[0]
                    temp_file_path = os.path.join(temp_directory_location, input_file_name + '.' + import_format_command.lower())
                    newDocument = Krita.instance().openDocument(temp_file_path)
                    Krita.instance().activeWindow().addView(newDocument)
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
            settings_window.setWindowTitle("DDS Import Settings") 
            settings_window.exec_()
