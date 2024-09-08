#-----------------------------------------------------------------------------#
# RESOURCES
#-----------------------------------------------------------------------------#
#Krita's pre-defined actions: https://scripting.krita.org/action-dictionary
#Krita's scripting school: https://scripting.krita.org/lessons/introduction
#Krita's document class: https://api.kde.org/krita/html/classDocument.html
#Krita's node class references: https://api.kde.org/krita/html/classNode.html
#Blending mode names: https://invent.kde.org/graphics/krita/-/blob/master/libs/pigment/KoCompositeOpRegistry.h

#-----------------------------------------------------------------------------#
# MODULES
#-----------------------------------------------------------------------------#

# Main
#-----------------------------------------------------------------------------#
import subprocess
import os
import shutil

# Krita
#-----------------------------------------------------------------------------#
from krita import *
from PyQt5.QtWidgets import (QWidget
                            ,QGridLayout
                            ,QVBoxLayout
                            ,QLabel
                            ,QComboBox
                            ,QPushButton
                            ,QDialog
                            ,QFileDialog
                            ,QMessageBox)

#-----------------------------------------------------------------------------#
# MAIN CODE
#-----------------------------------------------------------------------------#

class texture_packing(Extension):

    def __init__(self, parent):
        # This is initialising the parent, always important when subclassing.
        super().__init__(parent)

    def setup(self):
        pass

    def createActions(self, window):
        action = window.createAction("ER_TEXTURE_PACKING", "Texture Packing", "tools/scripts")
        action.triggered.connect(self.packTextures)       
        
    def packTextures(self):

        # Design Menu
        ## Base Grid
        cWidget = QWidget()
        grid = QGridLayout(cWidget) 
        
        ## Define Layout
        vBox_01 = QVBoxLayout()
        vBox_02 = QVBoxLayout()
        vBox_03 = QVBoxLayout()
        vBox_04 = QVBoxLayout()
        
        ## Row 00 - Headers
        header_01_label = QLabel('Target Channel')
        header_02_label = QLabel('Origin Channel')
        header_03_label = QLabel('File')
        header_04_label = QComboBox()
        header_04_label = QComboBox()
        header_04_label.addItems(['16x16'
                                  ,'32x32'
                                  ,'64x64'
                                  ,'128x128'
                                  ,'256x256'
                                  ,'512x512'
                                  ,'1024x1024'
                                  ,'2048x2048'
                                  ,'4096x4096'
                                  ,'8192x8192'
                                  ,'16384x16384'])
        header_04_label.setCurrentIndex(6) #Default value
        
        vBox_01.addWidget(header_01_label)
        vBox_02.addWidget(header_02_label)
        vBox_03.addWidget(header_03_label)
        vBox_04.addWidget(header_04_label)
        
        ## Row 01 - Red Channel
        channel_01_label = QLabel('Red')
        vBox_01.addWidget(channel_01_label)
        
        origin_channel_combo_R = QComboBox()
        origin_channel_combo_R.addItems(['Grayscale'
                                        ,'Red'])
        origin_channel_combo_R.setCurrentIndex(0)
        vBox_02.addWidget(origin_channel_combo_R)
        
        texture_path_R = QLabel('No file selected.')
        vBox_03.addWidget(texture_path_R)
        
        select_file_R = QPushButton("Select file") 
        vBox_04.addWidget(select_file_R)  
        
        ## Row 02 - Green Channel
        channel_02_label = QLabel('Green')
        vBox_01.addWidget(channel_02_label)
        
        origin_channel_combo_G = QComboBox()
        origin_channel_combo_G.addItems(['Grayscale'
                                        ,'Green'])
        origin_channel_combo_G.setCurrentIndex(0)
        vBox_02.addWidget(origin_channel_combo_G)
        
        texture_path_G = QLabel('No file selected.')
        vBox_03.addWidget(texture_path_G)
        
        select_file_G = QPushButton("Select file") 
        vBox_04.addWidget(select_file_G)  
        
        ## Row 03 - Blue Channel
        channel_03_label = QLabel('Blue')
        vBox_01.addWidget(channel_03_label)
        
        origin_channel_combo_B = QComboBox()
        origin_channel_combo_B.addItems(['Grayscale'
                                        ,'Blue'])
        origin_channel_combo_B.setCurrentIndex(0)
        vBox_02.addWidget(origin_channel_combo_B)
        
        texture_path_B = QLabel('No file selected.')
        vBox_03.addWidget(texture_path_B)
        
        select_file_B = QPushButton("Select file") 
        vBox_04.addWidget(select_file_B)  
        
        ## Row 04 - Alpha Channel
        channel_04_label = QLabel('Alpha')
        vBox_01.addWidget(channel_04_label)
        
        origin_channel_combo_A = QComboBox()
        origin_channel_combo_A.addItems(['Grayscale'])
        origin_channel_combo_A.setCurrentIndex(0)
        vBox_02.addWidget(origin_channel_combo_A)
        
        texture_path_A = QLabel('No file selected.')
        vBox_03.addWidget(texture_path_A)
        
        select_file_A = QPushButton("Select file") 
        vBox_04.addWidget(select_file_A)  
        
        ## Buttons
        empty_01_label = QLabel('')
        vBox_01.addWidget(empty_01_label)
        empty_02_label = QLabel('')
        vBox_02.addWidget(empty_02_label)
        Cancel_Button = QPushButton("Cancel") 
        vBox_03.addWidget(Cancel_Button)
        Confirm_Button = QPushButton("Submit") 
        Confirm_Button.setIcon(Krita.instance().icon('animation_play'))
        vBox_04.addWidget(Confirm_Button)  
        
        ##Attach layouts to grid
        grid.addLayout(vBox_01, 0, 0)
        grid.addLayout(vBox_02, 0, 1)
        grid.addLayout(vBox_03, 0, 2)
        grid.addLayout(vBox_04, 0, 3)

        ## Buttons - Functionality
        def select_file_R_Clicked():
            selected_file_R = QFileDialog().getOpenFileName(caption = "Select file for Red channel")[0]
            texture_path_R.setText(str(selected_file_R))
            
        def select_file_G_Clicked():
            selected_file_G = QFileDialog().getOpenFileName(caption = "Select file for Green channel")[0]
            texture_path_G.setText(str(selected_file_G))
            
        def select_file_B_Clicked():
            selected_file_B = QFileDialog().getOpenFileName(caption = "Select file for Blue channel")[0]
            texture_path_B.setText(str(selected_file_B))
            
        def select_file_A_Clicked():
            selected_file_A = QFileDialog().getOpenFileName(caption = "Select file for Alpha channel")[0]
            texture_path_A.setText(str(selected_file_A))
        
        def Confirm_Button_Clicked():
        
            # Check if any texture was added:
            if (texture_path_R.text() == 'No file selected.' or texture_path_R.text() == '') and (texture_path_G.text() == 'No file selected.' or texture_path_G.text() == '') and (texture_path_B.text() == 'No file selected.' or texture_path_B.text() == '') and (texture_path_A.text() == 'No file selected.' or texture_path_A.text() == ''):
                messageBox = QMessageBox()
                messageBox.setWindowTitle('An error occurred')
                messageBox.setIcon(QMessageBox.Warning)
                messageBox.setText("You have not selected any file for the target channels.")
                messageBox.setStandardButtons(QMessageBox.Close)
                messageBox.exec()
            else:
                settings_window.done(0)
            
                # Initialize variables
                application = Krita.instance()
                
                list_textures = [texture_path_R.text()
                                 ,texture_path_G.text()
                                 ,texture_path_B.text()
                                 ,texture_path_A.text()]

                list_textures_names = ['Channel_R'
                                       ,'Channel_G'
                                       ,'Channel_B'
                                       ,'Channel_A']
                                       
                dict_transfer_channels = {'R' : channel_01_label.text()
                                          ,'G' : channel_02_label.text()
                                          ,'B' : channel_03_label.text()
                                          ,'A' : channel_04_label.text()}
                                          
                dict_transfer_channels_colours = {'R' : '#ff0000'
                                                  ,'G' : '#00ff00'
                                                  ,'B' : '#0000ff'}
                                       
                dict_origin_channels = {'R' : origin_channel_combo_R.currentText()
                                        ,'G' : origin_channel_combo_G.currentText()
                                        ,'B' : origin_channel_combo_B.currentText()
                                        ,'A' : origin_channel_combo_A.currentText()}
                                        
                # Functionality
                try:
                                      
                    # Create new document
                    doc_size = header_04_label.currentText().split('x')[0]
                    #createDocument(width, height, name, colorSpace, bitDepth, colorProfile, DPI)
                    doc = application.createDocument(int(doc_size), int(doc_size), 'New Document', 'RGBA', 'U8', '', 100.0)
                    application.activeWindow().addView(doc)
                    currentDoc = application.activeDocument()
                    
                    # Copy the images to the new document (i = 0 -> R / i = 1 -> G / i = 2 -> B / i = 3 -> A)
                    node = currentDoc.nodeByName('Background')
                    for i in range(len(list_textures)):
                        if list_textures[i] not in ['', 'No file selected.']:
                            if i == 0:
                                FileLayer_R = currentDoc.createFileLayer('Channel_R' #Layer Name
                                                                         ,list_textures[i] #File path
                                                                         ,'None') #Scaling Method
                                FileLayer_R.setBlendingMode('copy_red')
                                root = currentDoc.rootNode()
                                root.addChildNode(FileLayer_R, node)                                
                                
                            elif i == 1:
                                FileLayer_G = currentDoc.createFileLayer('Channel_G'
                                                                         ,list_textures[i]
                                                                         ,'None')
                                FileLayer_G.setBlendingMode('copy_green')
                                root = currentDoc.rootNode()
                                root.addChildNode(FileLayer_G, node)
                            elif i == 2:
                                FileLayer_B = currentDoc.createFileLayer('Channel_B'
                                                                         ,list_textures[i]
                                                                         ,'None')
                                FileLayer_B.setBlendingMode('copy_blue')
                                root = currentDoc.rootNode()
                                root.addChildNode(FileLayer_B, node)
                            elif i == 3:
                                FileLayer_A = currentDoc.createFileLayer('Channel_A'
                                                                         ,list_textures[i]
                                                                         ,'None')
                                root = currentDoc.rootNode()
                                root.addChildNode(FileLayer_A, node)
                    
                                # Remove Initial Layer
                                node.remove()
                                
                                # Add Background Layer for Transparency Mask
                                params_size = krita.Selection()  #Initial selection is empty
                                params_size.invert()  #Invert empty
                                params_color = krita.InfoObject()
                                params_color.setProperty('color', '#ffffff')
                                color_fill = currentDoc.createFillLayer('Alpha_Channel_Fill'
                                                                        ,'color'
                                                                        ,params_color
                                                                        ,params_size)
                                root = currentDoc.rootNode()
                                root.addChildNode(color_fill, FileLayer_A)
                                
                        else:
                            if i == 0:
                                # Add Black layer
                                params_size = krita.Selection()  #Initial selection is empty
                                params_size.invert()  #Invert empty
                                params_color = krita.InfoObject()
                                params_color.setProperty('color', '#000000')
                                FileLayer_R = currentDoc.createFillLayer('Channel_R'
                                                                         ,'color'
                                                                         ,params_color
                                                                         ,params_size)
                                FileLayer_R.setBlendingMode('copy_red')
                                root = currentDoc.rootNode()
                                root.addChildNode(FileLayer_R, node)
                            
                            elif i == 1:
                                # Add Black layer
                                params_size = krita.Selection()  #Initial selection is empty
                                params_size.invert()  #Invert empty
                                params_color = krita.InfoObject()
                                params_color.setProperty('color', '#000000')
                                FileLayer_G = currentDoc.createFillLayer('Channel_G'
                                                                         ,'color'
                                                                         ,params_color
                                                                         ,params_size)
                                FileLayer_G.setBlendingMode('copy_green')
                                root = currentDoc.rootNode()
                                root.addChildNode(FileLayer_G, node)
                            
                            elif i == 2:
                                # Add Black layer
                                params_size = krita.Selection()  #Initial selection is empty
                                params_size.invert()  #Invert empty
                                params_color = krita.InfoObject()
                                params_color.setProperty('color', '#000000')
                                FileLayer_B = currentDoc.createFillLayer('Channel_B'
                                                                         ,'color'
                                                                         ,params_color
                                                                         ,params_size)
                                FileLayer_B.setBlendingMode('copy_blue')
                                root = currentDoc.rootNode()
                                root.addChildNode(FileLayer_B, node)
                    
                    # Refresh Document
                    doc.setBatchmode(True) #No popups while saving
                    currentDoc.setModified(False)
                    application.action('file_close_all').trigger()
                    application.activeWindow().addView(doc)
                    currentDoc = application.activeDocument()

                except subprocess.CalledProcessError as e:
                    messageBox = QMessageBox()
                    messageBox.setWindowTitle('An error occurred')
                    messageBox.setIcon(QMessageBox.Critical)
                    messageBox.setText(f"Krita encountered the following error: {e}")
                    messageBox.setStandardButtons(QMessageBox.Close)
                    messageBox.exec()
        
        def Cancel_Button_Clicked():
            settings_window.done(1)
        
        select_file_R.clicked.connect(select_file_R_Clicked)
        select_file_G.clicked.connect(select_file_G_Clicked)
        select_file_B.clicked.connect(select_file_B_Clicked)
        select_file_A.clicked.connect(select_file_A_Clicked)
        Confirm_Button.clicked.connect(Confirm_Button_Clicked)
        Cancel_Button.clicked.connect(Cancel_Button_Clicked)

        ## Generate window
        settings_window = QDialog() 
        settings_window.setLayout(grid)
        settings_window.setWindowTitle("Texture Packing") 
        settings_window.exec_()