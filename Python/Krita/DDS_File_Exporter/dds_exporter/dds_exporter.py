#*****************************************************************************#
# RESOURCES
#*****************************************************************************#
#https://github.com/Microsoft/DirectXTex/wiki/Texconv

#*****************************************************************************#
# MODULES
#*****************************************************************************#
#Main
import subprocess
import os
import shutil
import configparser

#Krita
from krita import *
from PyQt5.QtCore import QFileInfo
from PyQt5.QtWidgets import QMessageBox, QFileDialog

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
                ##Read .INI file
                settings_location = os.path.join(os.path.dirname(__file__), 'settings.ini')
                config = configparser.ConfigParser()
                config.read(settings_location)
                
                if os.path.isfile(settings_location) == False:
                    messageBox = QMessageBox()
                    messageBox.setWindowTitle('An error occurred')
                    messageBox.setIcon(QMessageBox.Critical)
                    messageBox.setText(settings_location)
                    messageBox.setText(f"Krita was unable to load the configuration file. Please ensure that the file 'settings.ini' is in the following path: {settings_location}.")
                    messageBox.setStandardButtons(QMessageBox.Close)
                    messageBox.exec()
                
                ##Load variables - Function
                def retrieve_value(parameter, section = 'SETTINGS', lower = True):
                    value_parameter = config[section][parameter].split('#')[0].strip()
                    if lower == True:
                        value_parameter = value_parameter.lower()
                    else:
                        value_parameter = value_parameter.upper()
                    value_parameter = value_parameter.replace("'", '')
                    return value_parameter
                
                ##Load variables - Store
                converter_path = os.path.join(os.path.dirname(__file__), 'resources', 'texconv.exe')
                if os.path.isfile(converter_path) == False:
                    messageBox = QMessageBox()
                    messageBox.setWindowTitle('An error occurred')
                    messageBox.setIcon(QMessageBox.Critical)
                    messageBox.setText(settings_location)
                    messageBox.setText(f"Krita was unable to load the converter application. Please ensure that the file 'texconv.exe' is in the following path: {converter_path}.")
                    messageBox.setStandardButtons(QMessageBox.Close)
                    messageBox.exec()
   
                compression_type = retrieve_value(parameter = 'compression_type'
                                                  ,lower = False)
                if retrieve_value(parameter = 'generate_mipmaps') == 'true':
                    generate_mipmaps = '-m 0'
                else:
                    generate_mipmaps = '-m 1'
                alpha_option = ('-' + retrieve_value(parameter = 'alpha_option')).replace("'", '')
                if retrieve_value(parameter = 'force_DX9_header') == 'false':
                    force_DX9_header = ''
                    if retrieve_value(parameter = 'force_DX10_header') == 'false':
                        force_DX10_header = ''
                    else:
                        force_DX10_header = '-dx10'
                else:
                    force_DX9_header = '-dx9'
                    force_DX10_header = ''
                
                #Create temporary directory
                temp_directory_location = os.path.join(os.path.dirname(__file__), 'erase')
                if not os.path.isdir(temp_directory_location):
                    os.makedirs(temp_directory_location)
                
                #Save document in PNG format temporarily
                output_file_name = os.path.splitext(os.path.basename(output_file))[0]
                temp_file_path = os.path.join(temp_directory_location, output_file_name + '.png')
                doc.setBatchmode(True)  #Disable export pop-up window
                info = InfoObject()
                info.setProperty("compression", 1)
                info.setProperty("indexed", False)
                info.setProperty("interlaced", False)
                info.setProperty("saveSRGBProfile", False)
                info.setProperty("forceSRGB", True)
                info.setProperty("alpha", True)
                info.setProperty("transparencyFillcolor", [0,0,0])
                doc.exportImage(temp_file_path, info)
                doc.setBatchmode(False)
                
                #Command Line
                output_file_path = os.path.dirname(output_file)
                args = [converter_path
                        ,"-y"
                        ,"-ft"
                        ,"DDS"
                        ,"-f"
                        ,compression_type
                        ,generate_mipmaps
                        ,alpha_option
                        ,force_DX9_header
                        ,force_DX10_header
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
                    messageBox.setText(settings_location)
                    messageBox.setText(f"Krita encountered the following error: {e}")
                    messageBox.setStandardButtons(QMessageBox.Close)
                    messageBox.exec()
                    
                #Clean temporary file(s) and folder
                shutil.rmtree(temp_directory_location)

        else:
            messageBox = QMessageBox()
            messageBox.setWindowTitle('No active document open')
            messageBox.setIcon(QMessageBox.Warning)
            messageBox.setText("Krita was unable to detect any open document.")
            messageBox.setStandardButtons(QMessageBox.Close)
            messageBox.exec()