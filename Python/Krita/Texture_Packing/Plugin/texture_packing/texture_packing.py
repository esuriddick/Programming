#-----------------------------------------------------------------------------#
# RESOURCES
#-----------------------------------------------------------------------------#
#Krita's pre-defined actions: https://scripting.krita.org/action-dictionary
#Krita's scripting school: https://scripting.krita.org/lessons/introduction
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
                                        ,'Red'
                                        ,'Green'
                                        ,'Blue'])
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
                                        ,'Red'
                                        ,'Green'
                                        ,'Blue'])
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
                                        ,'Red'
                                        ,'Green'
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
        origin_channel_combo_A.addItems(['Grayscale'
                                        ,'Red'
                                        ,'Green'
                                        ,'Blue'])
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
                                        
                # Functions
                 # Define function to translate from origin channel to target channel
                def ExtractOriginRGBChannelToTargetChannel(target_channel = 'R', origin_channel = 'R', file_index = 0):
                    try:
                        if dict_origin_channels[origin_channel] not in [dict_transfer_channels[target_channel], 'Grayscale'] and target_channel != 'A':
                            
                            # Open Image
                            temp_doc = application.openDocument(list_textures[file_index])
                            application.activeWindow().addView(temp_doc)
                            currentLayer = temp_doc.activeNode()
                            
                            # Extract information from single channel
                            if dict_origin_channels[origin_channel] == 'Red':
                                currentLayer.setBlendingMode('copy_red')
                            elif dict_origin_channels[origin_channel] == 'Green':
                                currentLayer.setBlendingMode('copy_green')
                            elif dict_origin_channels[origin_channel] == 'Blue':
                                currentLayer.setBlendingMode('copy_blue')
                                
                            # Export Separate Channel Image
                            temp_doc.setBatchmode(True) #No popups while saving
                            temp_file_name = 'separate_channel.tga'
                            temp_file_path = os.path.join(temp_directory_location, temp_file_name)
                            temp_doc.saveAs(temp_file_path)
                            
                            # Close Image
                            temp_doc.setModified(False)
                            application.action('file_close').trigger()
                            
                            # Import Separate Channel Image
                            temp_doc = application.openDocument(temp_file_path)
                            temp_root = temp_doc.rootNode()
                            application.activeWindow().addView(temp_doc)
                            currentLayer = temp_doc.activeNode()
                            os.remove(temp_file_path)
                            
                            # Convert to grayscale
                            #print(Krita.instance().filters()) #To see available filters
                            colorFilter = application.filter('hsvadjustment')
                            colorFilterConfig = colorFilter.configuration()
                            #print(colorFilterConfig.properties()) #To see what properties can be setup
                            colorFilterConfig.setProperty('s', -100)
                            colorFilter.apply(currentLayer, 0, 0, temp_doc.width(), temp_doc.height())
                            temp_doc.refreshProjection()
                            
                            # Create fill layer for target channel
                            params_size = krita.Selection()  #Initial selection is empty
                            params_size.invert()  #Invert empty
                            params_color = krita.InfoObject()
                            params_color.setProperty('color', dict_transfer_channels_colours[target_channel])
                            color_fill = temp_doc.createFillLayer('Target_Channel_Fill'
                                                                  ,'color'
                                                                  ,params_color
                                                                  ,params_size)
                            temp_root.addChildNode(color_fill, None)
                            
                            # Change blending mode to Binary -> AND on fill layer
                            layerFoundByName = temp_doc.nodeByName('Target_Channel_Fill')
                            temp_doc.setActiveNode(layerFoundByName)
                            layerFoundByName.setBlendingMode('and')
                            
                            # Save image to be used for the proper channel
                            temp_doc.setBatchmode(True) #No popups while saving
                            temp_file_name = 'target_channel_' + str(target_channel) + '.tga'
                            temp_file_path = os.path.join(temp_directory_location, temp_file_name)
                            temp_doc.saveAs(temp_file_path)
                            
                            # Close Image
                            temp_doc.setModified(False)
                            application.action('file_close').trigger()
                            
                            # Define New Image Path
                            list_textures[i] = temp_file_path
                            
                        else:
                            # Open Image
                            temp_doc = application.openDocument(list_textures[file_index])
                            application.activeWindow().addView(temp_doc)
                            currentLayer = temp_doc.activeNode()
                            
                            # Extract information from single channel
                            if dict_origin_channels[origin_channel] == 'Red':
                                currentLayer.setBlendingMode('copy_red')
                            elif dict_origin_channels[origin_channel] == 'Green':
                                currentLayer.setBlendingMode('copy_green')
                            elif dict_origin_channels[origin_channel] == 'Blue':
                                currentLayer.setBlendingMode('copy_blue')

                            # Export Separate Channel Image
                            temp_doc.setBatchmode(True) #No popups while saving
                            temp_file_name = 'separate_channel.tga'
                            temp_file_path = os.path.join(temp_directory_location, temp_file_name)
                            temp_doc.saveAs(temp_file_path)

                            # Close Image
                            temp_doc.setModified(False)
                            application.action('file_close').trigger()
                            
                            # Import Separate Channel Image
                            temp_doc = application.openDocument(temp_file_path)
                            temp_root = temp_doc.rootNode()
                            application.activeWindow().addView(temp_doc)
                            currentLayer = temp_doc.activeNode()
                            os.remove(temp_file_path)
                            
                            # Convert to grayscale
                            if dict_origin_channels[origin_channel] != 'Grayscale':
                                #print(Krita.instance().filters()) #To see available filters
                                colorFilter = application.filter('hsvadjustment')
                                colorFilterConfig = colorFilter.configuration()
                                #print(colorFilterConfig.properties()) #To see what properties can be setup
                                colorFilterConfig.setProperty('s', -100)
                                colorFilter.apply(currentLayer, 0, 0, temp_doc.width(), temp_doc.height())
                                temp_doc.refreshProjection()
                            
                            # Save image to be used for the proper channel
                            temp_doc.setBatchmode(True) #No popups while saving
                            temp_file_name = 'target_channel_' + str(target_channel) + '.tga'
                            temp_file_path = os.path.join(temp_directory_location, temp_file_name)
                            temp_doc.saveAs(temp_file_path)
                            
                            # Close Image
                            temp_doc.setModified(False)
                            application.action('file_close').trigger()
                            
                            # Define New Image Path
                            list_textures[i] = temp_file_path
                            
                    except subprocess.CalledProcessError as e:
                        shutil.rmtree(temp_directory_location)
                        messageBox = QMessageBox()
                        messageBox.setWindowTitle('An error occurred')
                        messageBox.setIcon(QMessageBox.Critical)
                        messageBox.setText(f"Krita encountered the following error: {e}")
                        messageBox.setStandardButtons(QMessageBox.Close)
                        messageBox.exec()

                try:
                    # Create temporary directory
                    temp_directory_location = os.path.join(os.path.dirname(__file__), 'erase')
                    if not os.path.isdir(temp_directory_location):
                        os.makedirs(temp_directory_location)
                    
                    # Generate textures for different target and origin channels (i = 0 -> R / i = 1 -> G / i = 2 -> B / i = 3 -> A)
                    for i in range(len(list_textures)):
                        if list_textures[i] not in ['', 'No file selected.']:
                            ExtractOriginRGBChannelToTargetChannel(target_channel = list(dict_transfer_channels.keys())[i]
                                                                   ,origin_channel = list(dict_origin_channels.keys())[i]
                                                                   ,file_index = i)
                    
                    # Create new document
                    doc_size = header_04_label.currentText().split('x')[0]
                    #createDocument(width, height, name, colorSpace, bitDepth, colorProfile, DPI)
                    doc = application.createDocument(int(doc_size), int(doc_size), 'New Document', 'RGBA', 'U8', '', 72.0)
                    root = doc.rootNode()
                    application.activeWindow().addView(doc)
                    currentDoc = application.activeDocument()
                    
                    # Copy the images to the new document (i = 0 -> R / i = 1 -> G / i = 2 -> B / i = 3 -> A)
                    for i in range(len(list_textures)):
                        if list_textures[i] not in ['', 'No file selected.']:
                            temp_doc = application.openDocument(list_textures[i])
                            application.activeWindow().addView(temp_doc)
                            currentLayer = temp_doc.activeNode()
                            currentLayer.setName(list_textures_names[i])
                            application.action('copy_layer_clipboard').trigger()
                            application.action('windows_previous').trigger()
                            application.action('paste_layer_from_clipboard').trigger()
                    
                    # Hide Initial Layer
                    layerFoundByName = currentDoc.nodeByName('Background')
                    layerFoundByName.setVisible(False)
                    
                    # Refresh Document
                    doc.setBatchmode(True) #No popups while saving
                    currentDoc.saveAs(os.path.join(temp_directory_location, 'temporary_project.kra'))
                    currentDoc.setModified(False)
                    application.action('file_close_all').trigger()
                    doc = application.openDocument(os.path.join(temp_directory_location, 'temporary_project.kra'))
                    application.activeWindow().addView(doc)
                    currentDoc = application.activeDocument()
                    root = currentDoc.rootNode()
                    
                    # Erase Initial Layer
                    layerFoundByName = currentDoc.nodeByName('Background')
                    if layerFoundByName:
                        currentDoc.setActiveNode(layerFoundByName)
                        application.action('remove_layer').trigger()
                    
                    # Clear temporary folder
                    shutil.rmtree(temp_directory_location)
                    
                    # Finishing code
                    messageBox = QMessageBox()
                    messageBox.setWindowTitle("Finish the process throug the Scripter")
                    messageBox.setText(f"You may find the script to use here: {os.path.join(os.path.dirname(__file__), 'resources')}")
                    messageBox.setStandardButtons(QMessageBox.Close)
                    messageBox.exec()

                except subprocess.CalledProcessError as e:
                    shutil.rmtree(temp_directory_location)
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