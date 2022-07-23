#****************************************************************************#
# LIBRARIES
#****************************************************************************#
import tkinter as tk
from tkinter import ttk
import random

#****************************************************************************#
# GENERATOR
#****************************************************************************#

# Initiate Window
#-----------------------------------------------------------------------------
window = tk.Tk()

# Window Configuration
#-----------------------------------------------------------------------------
window.title('D&D - One Shot Campaign Generator')
window.geometry('600x225')
window.resizable(width=False, height=False)
#window.grid_columnconfigure(0, weight=1) #Center the button
window.grid_rowconfigure(5, weight=1) #Center the button

# Style
#-----------------------------------------------------------------------------
#style = ttk.Style(window)
#print(style.theme_names()) #Available themes
#style.theme_use(style.theme_names()[5])
#print(style.theme_use()) #Theme in use

# Functions
#-----------------------------------------------------------------------------
##Variables
Random_Characters = tk.StringVar()
Random_Goal = tk.StringVar()
Random_Theme_or_NPCs = tk.StringVar()
Random_StartScene = tk.StringVar()
Random_PlotTwist = tk.StringVar()

##Lists
Character_Types = ['young spellcasters'
                   ,'infamous gnomes'
                   ,'hungry bards'
                   ,'from the same village'
                   ,'troubled sages'
                   ,'powerful tieflings'
                   ,'cursed knights'
                   ,'shapechanging members of a ruling family'
                   ,'outcast paladins'
                   ,'elite spies'
                   ,'all ogres (or other monster)'
                   ,'despised monster hunters'
                   ,'penniless warriors'
                   ,'secretive guild artisans'
                   ,'chaotic folk heroes'
                   ,'members of the same crime family'
                   ,'dramatic barbarians'
                   ,'veteran instructors at an academy'
                   ,'imprisoned lords and ladies'
                   ,'heroic leaders of a temple'
                   ]

Goals = ['investigate why a spirit is not at rest'
         ,'recover a legendary chariot'
         ,'steal something from a vain storm giant'
         ,'explore an elven shipwreck'
         ,'find someone at a festival where everyone is a shapechanger'
         ,'investigate the history of a necromantic crown'
         ,'slay a fiendish beholder'
         ,'survive an elemental apocalypse'
         ,'destroy a bejeweled artifact'
         ,'infiltrate a cult'
         ,'capture a famous awakened beast'
         ,'protect a fortified tavern'
         ,'collect a bounty on a flamboyant orc warchief'
         ,'steal a herd of dinosaurs'
         ,'escape from an arcane asylum'
         ,'find a buyer for a cursed boat'
         ,'put on a fashion show'
         ,'befriend an honorable archmage'
         ,"destroy a walled noble's estate"
         ,'complete a ritual in a magical laboratory'         
         ]

Theme_or_NPC = ['snakes'
                ,'a desperate apprentice who betrays them'
                ,'a criminal organisation'
                ,'an attractive barbarian who falls in love with a character'
                ,'the Shadowfell'
                ,'a dangerous mercenary who has important information for them'
                ,'giants'
                ,'a talkative sage who turns out to be the villain'
                ,'shapechangers'
                ,'a young sorcerer who offers them aid'
                ]

StartScene = ['a chase scene'
              ,'foes about to ambush them'
              ,'a disrupted wedding'
              ,'the group camped and about to be attacked'
              ,'a local festival'
              ,'a sinking vessel'
              ,'the loan of a magic item'
              ,'the characters in a fight'
              ,'a funeral'
              ,'the characters outside some ruins'
              ]

PlotTwist = ['there is a fire'
             ,'they uncover a secret stockpile'
             ,'there is a romantic complication'
             ,'someone betrays them'
             ,'a ghost gives them aid'
             ,'there is a planar portal'
             ,'an old friend appears'
             ,'they encounter a magical trap'
             ,'there is an earthquake'
             ,'a rival turns up'
              ]

##Functions
def Generate():
    #Character Types
    Random_Characters.set(Character_Types[random.randint(0, len(Character_Types)-1)])
    
    #Goals
    Random_Goal.set(Goals[random.randint(0, len(Goals)-1)])
    
    #Theme or NPCs
    Random_Theme_or_NPCs.set(Theme_or_NPC[random.randint(0, len(Theme_or_NPC)-1)])
    
    #Start Scene
    Random_StartScene.set(StartScene[random.randint(0, len(StartScene)-1)])
    
    #Start Scene
    Random_PlotTwist.set(PlotTwist[random.randint(0, len(PlotTwist)-1)])    

# Elements
#-----------------------------------------------------------------------------
##Buttons
Button_Generate = ttk.Button(window
                             ,text = 'Generate'
                             ,command = Generate)

##Text
Label_Characters = ttk.Label(window
                             ,text = 'The characters are'
                             ,font='TkDefaultFont 10')

Label_Goal = ttk.Label(window
                             ,text = 'Trying to'
                             ,font='TkDefaultFont 10')

Label_Theme_or_NPCs = ttk.Label(window
                             ,text = 'It involves'
                             ,font='TkDefaultFont 10')

Label_StartScene = ttk.Label(window
                             ,text = 'It starts with'
                             ,font='TkDefaultFont 10')

Label_PlotTwist = ttk.Label(window
                             ,text = 'At some point'
                             ,font='TkDefaultFont 10')

##Results
Label_Characters_Output = ttk.Label(window
                                    ,textvariable = Random_Characters
                             ,font='TkDefaultFont 10 bold')

Label_Goal_Output = ttk.Label(window
                              ,textvariable = Random_Goal
                             ,font='TkDefaultFont 10 bold')

Label_Theme_or_NPCs_Output = ttk.Label(window
                                       ,textvariable = Random_Theme_or_NPCs
                                       ,font='TkDefaultFont 10 bold')

Label_StartScene_Output = ttk.Label(window
                                    ,textvariable = Random_StartScene
                             ,font='TkDefaultFont 10 bold')

Label_PlotTwist_Output = ttk.Label(window
                                   ,textvariable = Random_PlotTwist
                             ,font='TkDefaultFont 10 bold')

# Layout
#-----------------------------------------------------------------------------
Labels_ipadx = 4
Labels_ipady = 4
Labels_padx = 2
Labels_pady = 4

## Row 0
Row_Number = 0
Label_Characters.grid(row = Row_Number
                     ,column = 0
                     ,ipadx = Labels_ipadx  #Internal X-axis
                     ,ipady = Labels_ipady  #Internal Y-axis
                     ,padx = Labels_padx   #External X-axis
                     ,pady = Labels_pady   #External Y-axis
                     ,sticky = 'E'
                     )
Label_Characters_Output.grid(row = Row_Number
                     ,column = 1
                     ,ipadx = Labels_ipadx  #Internal X-axis
                     ,ipady = Labels_ipady  #Internal Y-axis
                     ,padx = Labels_padx   #External X-axis
                     ,pady = Labels_pady   #External Y-axis
                     ,sticky = 'W'
                     )

## Row 1
Row_Number = 1
Label_Goal.grid(row = Row_Number
                     ,column = 0
                     ,ipadx = Labels_ipadx  #Internal X-axis
                     ,ipady = Labels_ipady  #Internal Y-axis
                     ,padx = Labels_padx   #External X-axis
                     ,pady = Labels_pady   #External Y-axis
                     ,sticky = 'E'
                     )
Label_Goal_Output.grid(row = Row_Number
                     ,column = 1
                     ,ipadx = Labels_ipadx  #Internal X-axis
                     ,ipady = Labels_ipady  #Internal Y-axis
                     ,padx = Labels_padx   #External X-axis
                     ,pady = Labels_pady   #External Y-axis
                     ,sticky = 'W'
                     )

## Row 2
Row_Number = 2
Label_Theme_or_NPCs.grid(row = Row_Number
                     ,column = 0
                     ,ipadx = Labels_ipadx  #Internal X-axis
                     ,ipady = Labels_ipady  #Internal Y-axis
                     ,padx = Labels_padx   #External X-axis
                     ,pady = Labels_pady   #External Y-axis
                     ,sticky = 'E'
                     )
Label_Theme_or_NPCs_Output.grid(row = Row_Number
                                ,column = 1
                                ,ipadx = Labels_ipadx  #Internal X-axis
                                ,ipady = Labels_ipady  #Internal Y-axis
                                ,padx = Labels_padx   #External X-axis
                                ,pady = Labels_pady   #External Y-axis
                                ,sticky = 'W'
                                )

## Row 3
Row_Number = 3
Label_StartScene.grid(row = Row_Number
                     ,column = 0
                     ,ipadx = Labels_ipadx  #Internal X-axis
                     ,ipady = Labels_ipady  #Internal Y-axis
                     ,padx = Labels_padx   #External X-axis
                     ,pady = Labels_pady   #External Y-axis
                     ,sticky = 'E'
                     )
Label_StartScene_Output.grid(row = Row_Number
                     ,column = 1
                     ,ipadx = Labels_ipadx  #Internal X-axis
                     ,ipady = Labels_ipady  #Internal Y-axis
                     ,padx = Labels_padx   #External X-axis
                     ,pady = Labels_pady   #External Y-axis
                     ,sticky = 'W'
                     )

## Row 4
Row_Number = 4
Label_PlotTwist.grid(row = Row_Number
                     ,column = 0
                     ,ipadx = Labels_ipadx  #Internal X-axis
                     ,ipady = Labels_ipady  #Internal Y-axis
                     ,padx = Labels_padx   #External X-axis
                     ,pady = Labels_pady   #External Y-axis
                     ,sticky = 'E'
                     )
Label_PlotTwist_Output.grid(row = Row_Number
                     ,column = 1
                     ,ipadx = Labels_ipadx  #Internal X-axis
                     ,ipady = Labels_ipady  #Internal Y-axis
                     ,padx = Labels_padx   #External X-axis
                     ,pady = Labels_pady   #External Y-axis
                     ,sticky = 'W'
                     )

## Row 5
Row_Number = 5
Button_Generate.place(relx = 0.5
                      ,rely = 0.95
                      ,anchor='s'
                      )

# Listen to events in the window
#-----------------------------------------------------------------------------
window.mainloop()

#****************************************************************************#
# COMPILATION
#****************************************************************************#
#!pyinstaller --noconsole --onefile DD_OneShot_Campaigns_Generator.py