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
from PyQt5.QtWidgets import QMessageBox, QFileDialog

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
            converter_path = os.path.join(os.path.dirname(__file__), 'resources', 'texconv.exe')
            compression_type = 'R8G8B8A8_UNORM'
            generate_mipmaps = '-m 1'
            intermediate_format = 'PNG'
            
            #Create temporary directory
            temp_directory_location = os.path.join(os.path.dirname(__file__), 'erase')
            if not os.path.isdir(temp_directory_location):
                os.makedirs(temp_directory_location)
                
            #Command Line
            args = [converter_path
                    ,"-y"
                    ,"-ft"
                    ,intermediate_format.upper()
                    ,"-f"
                    ,compression_type
                    ,"-srgbi"
                    ,generate_mipmaps
                    ,"-o"
                    ,temp_directory_location
                    ,input_file]
            while '' in args:
                args.remove('')
            argline = " ".join(args)
            for i in [converter_path, temp_directory_location, input_file]:
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
                temp_file_path = os.path.join(temp_directory_location, input_file_name + '.' + intermediate_format.lower())
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