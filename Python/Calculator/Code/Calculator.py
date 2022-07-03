#****************************************************************************#
# LIBRARIES
#****************************************************************************#
import locale
import tkinter as tk
from tkinter import ttk

#****************************************************************************#
# CALCULATOR
#****************************************************************************#

# Initiate Window
#-----------------------------------------------------------------------------
window = tk.Tk()

# Window Configuration
#-----------------------------------------------------------------------------
window.title('Calculator')
window.geometry('317x320')
window.resizable(width=False, height=False)

# Style
#-----------------------------------------------------------------------------
#style = ttk.Style(window)
#print(style.theme_names()) #Available themes
#style.theme_use(style.theme_names()[5])
#print(style.theme_use()) #Theme in use

# Functions
#-----------------------------------------------------------------------------
results = ''

def press(button):
    # Select the temporary variable created to hold inputs
    global results
 
    # Update the results
    results = results + str(button)
 
    # Refresh the output
    equation.set(results)
    
def press_equal():
    # Try and except statement is used for handling the errors
    try:
        # Select the temporary variable created to hold inputs
        global results
 
        # Function eval calculates the result from the expression
        # and str function converts it to a string
        total = str(eval(results))
 
        # Refresh the output
        equation.set(total)
 
        # Reset the input
        results = ''
 
    # If an error occurs when doing the calculation, warn the user
    except:
        # Refresh the output
        equation.set('ERROR')
        
        # Reset the input
        results = ''
        
def clear():
    # Select the temporary variable created to hold inputs
    global results
    
    # Refresh the output
    equation.set('')
    
    # Reset the input
    results = ''

# Elements
#-----------------------------------------------------------------------------
## Results
equation = tk.StringVar()
Output = ttk.Entry(textvariable = equation, width = 50, state = 'readonly', justify='right')

## Numbers
Button_00 = ttk.Button(text = '0', command = lambda: press(0))
Button_01 = ttk.Button(text = '1', command = lambda: press(1))
Button_02 = ttk.Button(text = '2', command = lambda: press(2))
Button_03 = ttk.Button(text = '3', command = lambda: press(3))
Button_04 = ttk.Button(text = '4', command = lambda: press(4))
Button_05 = ttk.Button(text = '5', command = lambda: press(5))
Button_06 = ttk.Button(text = '6', command = lambda: press(6))
Button_07 = ttk.Button(text = '7', command = lambda: press(7))
Button_08 = ttk.Button(text = '8', command = lambda: press(8))
Button_09 = ttk.Button(text = '9', command = lambda: press(9))

## Symbols
Button_Division = ttk.Button(text = '÷', command = lambda: press('/'))
Button_Multiplication = ttk.Button(text = 'x', command = lambda: press('*'))
Button_Subtraction = ttk.Button(text = '-', command = lambda: press('-'))
Button_Addition = ttk.Button(text = '+', command = lambda: press('+'))
Button_Decimal = ttk.Button(text = locale.localeconv()['decimal_point'], command = lambda: press(locale.localeconv()['decimal_point']))
Button_Power = ttk.Button(text = 'Power', command = lambda: press('**'))
Button_Left_Parenthesis = ttk.Button(text = '(', command = lambda: press('('))
Button_Right_Parenthesis = ttk.Button(text = ')', command = lambda: press(')'))

## Special
Button_Clear = ttk.Button(text = 'C', command = clear)
Button_Equal = ttk.Button(text = '=',command = press_equal)

# Layout
#-----------------------------------------------------------------------------
Buttons_ipadx = 0
Buttons_ipady = 14

## Row 0
Row_Number = 0
Output.grid(row = Row_Number
            ,column = 0
            ,ipadx = 4  #Internal X-axis
            ,ipady = 4  #Internal Y-axis
            ,padx = 2   #External X-axis
            ,pady = 10   #External Y-axis
            ,columnspan = 4)

## Row 1
Row_Number = 1
Button_Left_Parenthesis.grid(row = Row_Number
               ,column = 0
               ,ipadx = Buttons_ipadx  #Internal X-axis
               ,ipady = Buttons_ipady  #Internal Y-axis
               )
Button_Right_Parenthesis.grid(row = Row_Number
               ,column = 1
               ,ipadx = Buttons_ipadx  #Internal X-axis
               ,ipady = Buttons_ipady  #Internal Y-axis
               )
Button_Clear.grid(row = Row_Number
               ,column = 2
               ,ipadx = Buttons_ipadx  #Internal X-axis
               ,ipady = Buttons_ipady  #Internal Y-axis
               )
Button_Division.grid(row = Row_Number
                           ,column = 3
                           ,ipadx = Buttons_ipadx  #Internal X-axis
                           ,ipady = Buttons_ipady  #Internal Y-axis
                           )

## Row 2
Row_Number = 2
Button_07.grid(row = Row_Number
               ,column = 0
               ,ipadx = Buttons_ipadx  #Internal X-axis
               ,ipady = Buttons_ipady  #Internal Y-axis
               )
Button_08.grid(row = Row_Number
               ,column = 1
               ,ipadx = Buttons_ipadx  #Internal X-axis
               ,ipady = Buttons_ipady  #Internal Y-axis
               )
Button_09.grid(row = Row_Number
               ,column = 2
               ,ipadx = Buttons_ipadx  #Internal X-axis
               ,ipady = Buttons_ipady  #Internal Y-axis
               )
Button_Multiplication.grid(row = Row_Number
                           ,column = 3
                           ,ipadx = Buttons_ipadx  #Internal X-axis
                           ,ipady = Buttons_ipady  #Internal Y-axis
                           )

## Row 3
Row_Number = 3
Button_04.grid(row = Row_Number
               ,column = 0
               ,ipadx = Buttons_ipadx  #Internal X-axis
               ,ipady = Buttons_ipady  #Internal Y-axis
               )
Button_05.grid(row = Row_Number
               ,column = 1
               ,ipadx = Buttons_ipadx  #Internal X-axis
               ,ipady = Buttons_ipady  #Internal Y-axis
               )
Button_06.grid(row = Row_Number
               ,column = 2
               ,ipadx = Buttons_ipadx  #Internal X-axis
               ,ipady = Buttons_ipady  #Internal Y-axis
               )
Button_Subtraction.grid(row = Row_Number
                           ,column = 3
                           ,ipadx = Buttons_ipadx  #Internal X-axis
                           ,ipady = Buttons_ipady  #Internal Y-axis
                           )

## Row 4
Row_Number = 4
Button_01.grid(row = Row_Number
               ,column = 0
               ,ipadx = Buttons_ipadx  #Internal X-axis
               ,ipady = Buttons_ipady  #Internal Y-axis
               )
Button_02.grid(row = Row_Number
               ,column = 1
               ,ipadx = Buttons_ipadx  #Internal X-axis
               ,ipady = Buttons_ipady  #Internal Y-axis
               )
Button_03.grid(row = Row_Number
               ,column = 2
               ,ipadx = Buttons_ipadx  #Internal X-axis
               ,ipady = Buttons_ipady  #Internal Y-axis
               )
Button_Addition.grid(row = Row_Number
                           ,column = 3
                           ,ipadx = Buttons_ipadx  #Internal X-axis
                           ,ipady = Buttons_ipady  #Internal Y-axis
                           )

## Row 5
Row_Number = 5
Button_Power.grid(row = Row_Number
                           ,column = 0
                           ,ipadx = Buttons_ipadx  #Internal X-axis
                           ,ipady = Buttons_ipady  #Internal Y-axis
                           )
Button_00.grid(row = Row_Number
               ,column = 1
               ,ipadx = Buttons_ipadx  #Internal X-axis
               ,ipady = Buttons_ipady  #Internal Y-axis
               )
Button_Decimal.grid(row = Row_Number
                           ,column = 2
                           ,ipadx = Buttons_ipadx  #Internal X-axis
                           ,ipady = Buttons_ipady  #Internal Y-axis
                           )
Button_Equal.grid(row = Row_Number
                           ,column = 3
                           ,ipadx = Buttons_ipadx  #Internal X-axis
                           ,ipady = Buttons_ipady  #Internal Y-axis
                           )

# Listen to events in the window
#-----------------------------------------------------------------------------
window.mainloop()

#****************************************************************************#
# COMPILATION
#****************************************************************************#
#!pyinstaller --noconsole --onefile Calculator.py
