#----------------------------------------------------------------------------#
#MODULES
import math
import Spheres_5th_Edition_Engine
import tkinter as tk
import tkinter.ttk as ttk
#----------------------------------------------------------------------------#

#----------------------------------------------------------------------------#
#FUNCTIONS
def character_limit(entry_text, limit):
    entry_text_str = str(entry_text.get())
    if (len(entry_text_str) > 0):
        value = int(entry_text_str[:limit])
        return(entry_text.set(value))
         
def only_numbers(data):
    return data.isdigit()

def floor_number(value, floor = 0):
    if value == "":
        return(floor)
    else:
        return(max(int(value), floor))

def cap_number(value, cap = 20):
    if value == "":
        return(cap)
    else:
        return(min(int(value), cap))

def convert_int_to_bool(value):
    if (value == 1):
        return(True)
    else:
        return(False)
        
def Button_Generate_PDF():
    if __name__ == "__main__":
        #BASICS
        Player_Name = INPUT_PLAYER_NAME.get()
        Character_Name = INPUT_CHARACTER_NAME.get()
        Race = INPUT_RACE.get()
        Class = INPUT_CLASS.get()
        Background = INPUT_BACKGROUND.get()
        Alignment = INPUT_ALIGNMENT.get()
        Level = cap_number(floor_number(INPUT_LEVEL.get(), floor = 1))
        Age = floor_number(INPUT_AGE.get(), floor = 0)
        Height = INPUT_HEIGHT.get()
        Tradition = INPUT_TRADITION.get()
        Martial_Focus = convert_int_to_bool(INPUT_MARTIAL_FOCUS.get())
        KAM = INPUT_KAM.get()
        
        #STATS
        Proficiency_Bonus = floor_number(INPUT_PROFICIENCY_MODIFIER.get())
        ATR_dict = {
            "STR" : INPUT_ATR_STRENGTH.get(),
            "DEX" : INPUT_ATR_DEXTERITY.get(),
            "CON" : INPUT_ATR_CONSTITUTION.get(),
            "INT" : INPUT_ATR_INTELLIGENCE.get(),
            "WIS" : INPUT_ATR_WISDOM.get(),
            "CHA" : INPUT_ATR_CHARISMA.get()
            }
        ATR_Modifiers_dict = {
            "STR" : math.floor((int(floor_number(ATR_dict.get("STR", 10))) - 10) / 2),
            "DEX" : math.floor((int(floor_number(ATR_dict.get("DEX", 10))) - 10) / 2),
            "CON" : math.floor((int(floor_number(ATR_dict.get("CON", 10))) - 10) / 2),
            "INT" : math.floor((int(floor_number(ATR_dict.get("INT", 10))) - 10) / 2),
            "WIS" : math.floor((int(floor_number(ATR_dict.get("WIS", 10))) - 10) / 2),
            "CHA" : math.floor((int(floor_number(ATR_dict.get("CHA", 10))) - 10) / 2)
            }
        Skills_Proficiencies_dict = {
                "Acrobatics" : convert_int_to_bool(INPUT_PROF_ACROBATICS.get()),
                "Animal Handling" : convert_int_to_bool(INPUT_PROF_ANIMAL_HANDLING.get()),
                "Arcana" : convert_int_to_bool(INPUT_PROF_ARCANA.get()),
                "Athletics" : convert_int_to_bool(INPUT_PROF_ATHLETICS.get()),
                "Deception" : convert_int_to_bool(INPUT_PROF_DECEPTION.get()),
                "History" : convert_int_to_bool(INPUT_PROF_HISTORY.get()),
                "Insight" : convert_int_to_bool(INPUT_PROF_INSIGHT.get()),
                "Intimidation" : convert_int_to_bool(INPUT_PROF_INTIMIDATION.get()),
                "Investigation" : convert_int_to_bool(INPUT_PROF_INVESTIGATON.get()),
                "Medicine" : convert_int_to_bool(INPUT_PROF_MEDICINE.get()),
                "Nature" : convert_int_to_bool(INPUT_PROF_NATURE.get()),
                "Perception" : convert_int_to_bool(INPUT_PROF_PERCEPTION.get()),
                "Performance" : convert_int_to_bool(INPUT_PROF_PERFORMANCE.get()),
                "Persuasion" : convert_int_to_bool(INPUT_PROF_PERSUASION.get()),
                "Religion" : convert_int_to_bool(INPUT_PROF_RELIGION.get()),
                "Sleight of Hand" : convert_int_to_bool(INPUT_PROF_SLEIGHT_OF_HAND.get()),
                "Stealth" : convert_int_to_bool(INPUT_PROF_STEALTH.get()),
                "Survival" : convert_int_to_bool(INPUT_PROF_SURVIVAL.get())
                }
        Skills_Bonus = {
                "Acrobatics" : Spheres_5th_Edition_Engine.Roll_bonus(INPUT_PROF_ACROBATICS.get(), ATR_dict.get("DEX", 10), INPUT_PROFICIENCY_MODIFIER.get()),
                "Animal Handling" : Spheres_5th_Edition_Engine.Roll_bonus(INPUT_PROF_ANIMAL_HANDLING.get(), ATR_dict.get("WIS", 10), INPUT_PROFICIENCY_MODIFIER.get()),
                "Arcana" : Spheres_5th_Edition_Engine.Roll_bonus(INPUT_PROF_ARCANA.get(), ATR_dict.get("INT", 10), INPUT_PROFICIENCY_MODIFIER.get()),
                "Athletics" : Spheres_5th_Edition_Engine.Roll_bonus(INPUT_PROF_ATHLETICS.get(), ATR_dict.get("STR", 10), INPUT_PROFICIENCY_MODIFIER.get()),
                "Deception" : Spheres_5th_Edition_Engine.Roll_bonus(INPUT_PROF_DECEPTION.get(), ATR_dict.get("CHA", 10), INPUT_PROFICIENCY_MODIFIER.get()),
                "History" : Spheres_5th_Edition_Engine.Roll_bonus(INPUT_PROF_HISTORY.get(), ATR_dict.get("INT", 10), INPUT_PROFICIENCY_MODIFIER.get()),
                "Insight" : Spheres_5th_Edition_Engine.Roll_bonus(INPUT_PROF_INSIGHT.get(), ATR_dict.get("WIS", 10), INPUT_PROFICIENCY_MODIFIER.get()),
                "Intimidation" : Spheres_5th_Edition_Engine.Roll_bonus(INPUT_PROF_INTIMIDATION.get(), ATR_dict.get("CHA", 10), INPUT_PROFICIENCY_MODIFIER.get()),
                "Investigation" : Spheres_5th_Edition_Engine.Roll_bonus(INPUT_PROF_INVESTIGATON.get(), ATR_dict.get("INT", 10), INPUT_PROFICIENCY_MODIFIER.get()),
                "Medicine" : Spheres_5th_Edition_Engine.Roll_bonus(INPUT_PROF_MEDICINE.get(), ATR_dict.get("WIS", 10), INPUT_PROFICIENCY_MODIFIER.get()),
                "Nature" : Spheres_5th_Edition_Engine.Roll_bonus(INPUT_PROF_NATURE.get(), ATR_dict.get("INT", 10), INPUT_PROFICIENCY_MODIFIER.get()),
                "Perception" : Spheres_5th_Edition_Engine.Roll_bonus(INPUT_PROF_PERCEPTION.get(), ATR_dict.get("WIS", 10), INPUT_PROFICIENCY_MODIFIER.get()),
                "Performance" : Spheres_5th_Edition_Engine.Roll_bonus(INPUT_PROF_PERFORMANCE.get(), ATR_dict.get("CHA", 10), INPUT_PROFICIENCY_MODIFIER.get()),
                "Persuasion" : Spheres_5th_Edition_Engine.Roll_bonus(INPUT_PROF_PERSUASION.get(), ATR_dict.get("CHA", 10), INPUT_PROFICIENCY_MODIFIER.get()),
                "Religion" : Spheres_5th_Edition_Engine.Roll_bonus(INPUT_PROF_RELIGION.get(), ATR_dict.get("INT", 10), INPUT_PROFICIENCY_MODIFIER.get()),
                "Sleight of Hand" : Spheres_5th_Edition_Engine.Roll_bonus(INPUT_PROF_SLEIGHT_OF_HAND.get(), ATR_dict.get("DEX", 10), INPUT_PROFICIENCY_MODIFIER.get()),
                "Stealth" : Spheres_5th_Edition_Engine.Roll_bonus(INPUT_PROF_STEALTH.get(), ATR_dict.get("DEX", 10), INPUT_PROFICIENCY_MODIFIER.get()),
                "Survival" : Spheres_5th_Edition_Engine.Roll_bonus(INPUT_PROF_SURVIVAL.get(), ATR_dict.get("WIS", 10), INPUT_PROFICIENCY_MODIFIER.get())
                }
        Saving_throws_dict = {
                "STR" : convert_int_to_bool(INPUT_SAV_THROW_STR.get()),
                "DEX" : convert_int_to_bool(INPUT_SAV_THROW_DEX.get()),
                "CON" : convert_int_to_bool(INPUT_SAV_THROW_CON.get()),
                "INT" : convert_int_to_bool(INPUT_SAV_THROW_INT.get()),
                "WIS" : convert_int_to_bool(INPUT_SAV_THROW_WIS.get()),
                "CHA" : convert_int_to_bool(INPUT_SAV_THROW_CHA.get())
                }
        Saving_throws_Bonus = {
                "STR" : Spheres_5th_Edition_Engine.Roll_bonus(INPUT_SAV_THROW_STR.get(), ATR_dict.get("STR", 10), INPUT_PROFICIENCY_MODIFIER.get()),
                "DEX" : Spheres_5th_Edition_Engine.Roll_bonus(INPUT_SAV_THROW_DEX.get(), ATR_dict.get("DEX", 10), INPUT_PROFICIENCY_MODIFIER.get()),
                "CON" : Spheres_5th_Edition_Engine.Roll_bonus(INPUT_SAV_THROW_CON.get(), ATR_dict.get("CON", 10), INPUT_PROFICIENCY_MODIFIER.get()),
                "INT" : Spheres_5th_Edition_Engine.Roll_bonus(INPUT_SAV_THROW_INT.get(), ATR_dict.get("INT", 10), INPUT_PROFICIENCY_MODIFIER.get()),
                "WIS" : Spheres_5th_Edition_Engine.Roll_bonus(INPUT_SAV_THROW_WIS.get(), ATR_dict.get("WIS", 10), INPUT_PROFICIENCY_MODIFIER.get()),
                "CHA" : Spheres_5th_Edition_Engine.Roll_bonus(INPUT_SAV_THROW_CHA.get(), ATR_dict.get("CHA", 10), INPUT_PROFICIENCY_MODIFIER.get())
                }
        
        #PROFICIENCIES AND LANGUAGES
        Tools_proficiencies = [
                convert_int_to_bool(INPUT_KIT_PROEF_01.get()),
                convert_int_to_bool(INPUT_KIT_PROEF_02.get()),
                convert_int_to_bool(INPUT_KIT_PROEF_03.get()),
                convert_int_to_bool(INPUT_KIT_PROEF_04.get()),
                convert_int_to_bool(INPUT_KIT_PROEF_05.get()),
                convert_int_to_bool(INPUT_KIT_PROEF_06.get())
                ]
        Tools_bonus = [
                Spheres_5th_Edition_Engine.Tool_bonus(convert_int_to_bool(INPUT_KIT_PROEF_01.get()), INPUT_PROFICIENCY_MODIFIER.get()),
                Spheres_5th_Edition_Engine.Tool_bonus(convert_int_to_bool(INPUT_KIT_PROEF_02.get()), INPUT_PROFICIENCY_MODIFIER.get()),
                Spheres_5th_Edition_Engine.Tool_bonus(convert_int_to_bool(INPUT_KIT_PROEF_03.get()), INPUT_PROFICIENCY_MODIFIER.get()),
                Spheres_5th_Edition_Engine.Tool_bonus(convert_int_to_bool(INPUT_KIT_PROEF_04.get()), INPUT_PROFICIENCY_MODIFIER.get()),
                Spheres_5th_Edition_Engine.Tool_bonus(convert_int_to_bool(INPUT_KIT_PROEF_05.get()), INPUT_PROFICIENCY_MODIFIER.get()),
                Spheres_5th_Edition_Engine.Tool_bonus(convert_int_to_bool(INPUT_KIT_PROEF_06.get()), INPUT_PROFICIENCY_MODIFIER.get())
                ]
        Tools_names = [
                INPUT_KIT_NAME_01.get(),
                INPUT_KIT_NAME_02.get(),
                INPUT_KIT_NAME_03.get(),
                INPUT_KIT_NAME_04.get(),
                INPUT_KIT_NAME_05.get(),
                INPUT_KIT_NAME_06.get()
                ]
        Languages = [
                INPUT_LANGUAGE_01.get(),
                INPUT_LANGUAGE_02.get(),
                INPUT_LANGUAGE_03.get(),
                INPUT_LANGUAGE_04.get(),
                INPUT_LANGUAGE_05.get(),
                INPUT_LANGUAGE_06.get(),
                INPUT_LANGUAGE_07.get(),
                INPUT_LANGUAGE_08.get(),
                INPUT_LANGUAGE_09.get(),
                INPUT_LANGUAGE_10.get(),
                INPUT_LANGUAGE_11.get(),
                INPUT_LANGUAGE_12.get(),
                INPUT_LANGUAGE_13.get(),
                INPUT_LANGUAGE_14.get(),
                ]
        Languages = [i for i in Languages if i]
        Other_Proficiencies = [
                INPUT_OTHER_PROF_01.get(),
                INPUT_OTHER_PROF_02.get(),
                INPUT_OTHER_PROF_03.get(),
                INPUT_OTHER_PROF_04.get(),
                INPUT_OTHER_PROF_05.get(),
                INPUT_OTHER_PROF_06.get(),
                INPUT_OTHER_PROF_07.get(),
                INPUT_OTHER_PROF_08.get(),
                INPUT_OTHER_PROF_09.get(),
                INPUT_OTHER_PROF_10.get(),
                INPUT_OTHER_PROF_11.get(),
                INPUT_OTHER_PROF_12.get(),
                INPUT_OTHER_PROF_13.get(),
                INPUT_OTHER_PROF_14.get()
                ]
        Other_Proficiencies = [i for i in Other_Proficiencies if i]
        
        #EQUIPMENT
        Currencies = [
                INPUT_CURR_CP.get(),
                INPUT_CURR_SP.get(),
                INPUT_CURR_GP.get(),
                INPUT_CURR_PP.get()
                ]
        Equipment = INPUT_EQUIPMENT.get("1.0", "end-1c")
        Weapon_01 = [
                INPUT_WEAPON_NAME_01.get(),
                Spheres_5th_Edition_Engine.Sign_Determination(floor_number(INPUT_WEAPON_ATTACK_BONUS_01.get())),
                INPUT_WEAPON_DAMAGE_01.get(),
                INPUT_WEAPON_TYPE_01.get(),
                INPUT_WEAPON_OTHER_01.get()
                ]
        Weapon_02 = [
                INPUT_WEAPON_NAME_02.get(),
                Spheres_5th_Edition_Engine.Sign_Determination(floor_number(INPUT_WEAPON_ATTACK_BONUS_02.get())),
                INPUT_WEAPON_DAMAGE_02.get(),
                INPUT_WEAPON_TYPE_02.get(),
                INPUT_WEAPON_OTHER_02.get()
                ]
        Weapon_03 = [
                INPUT_WEAPON_NAME_03.get(),
                Spheres_5th_Edition_Engine.Sign_Determination(floor_number(INPUT_WEAPON_ATTACK_BONUS_03.get())),
                INPUT_WEAPON_DAMAGE_03.get(),
                INPUT_WEAPON_TYPE_03.get(),
                INPUT_WEAPON_OTHER_03.get()
                ]
        Weapon_04 = [
                INPUT_WEAPON_NAME_04.get(),
                Spheres_5th_Edition_Engine.Sign_Determination(floor_number(INPUT_WEAPON_ATTACK_BONUS_04.get())),
                INPUT_WEAPON_DAMAGE_04.get(),
                INPUT_WEAPON_TYPE_04.get(),
                INPUT_WEAPON_OTHER_04.get()
                ]
        
        #COMBAT
        Combat_Info = {
                        "AC": floor_number(INPUT_COMBAT_AC.get(), floor = 0),
                        "HP": floor_number(INPUT_COMBAT_HP.get(), floor = 1),
                        "Speed": floor_number(INPUT_COMBAT_SPEED.get(), floor = 1),
                        "HitDice_Sides": floor_number(INPUT_COMBAT_HDSides.get(), floor = 1)
                        }
        
        #DEFINE WHAT TO FILL IN PDF - DICTIONARY
        sample_data_dict = {
                "AC": Combat_Info["AC"],
                "alignment": Alignment,
                "ATR": ATR_dict,
                "ATR_Modifiers": dict(map(lambda x: (x[0], Spheres_5th_Edition_Engine.Sign_Determination(x[1])), ATR_Modifiers_dict.items())),
                "background": Background,
                "class": Class,
                "currencies": Currencies,
                "equipment": Equipment,
                "hit_dice": Combat_Info["HitDice_Sides"],
                "kam": Spheres_5th_Edition_Engine.KAM_identifier(KAM),
                "languages": Languages,
                "level": Level,
                "age": Age,
                "height": Height,
                "martial_focus": Martial_Focus,
                "max_hp": Combat_Info["HP"],
                "name": Character_Name,
                "other_proficiencies": Other_Proficiencies,
                "player": Player_Name,
                "proficiency_bonus": Spheres_5th_Edition_Engine.Sign_Determination(Proficiency_Bonus),
                "race": Race,
                "skills_bonus": Skills_Bonus, 
                "skills_proficiencies": Skills_Proficiencies_dict,
                "saving_throws_bonus": Saving_throws_Bonus,
                "saving_throws_proficiencies": Saving_throws_dict,
                "speed": Combat_Info['Speed'],
                "tools_bonus": Tools_bonus,
                "tools_names": Tools_names,
                "tools_proficiencies": Tools_proficiencies,
                "tradition": Tradition,
                "weapon_01": Weapon_01,
                "weapon_02": Weapon_02,
                "weapon_03": Weapon_03,
                "weapon_04": Weapon_04
                }
        
        #INPUT AND OUTFILE FILE NAMES
        pdf_template = "Spheres_of_Power_and_Might_(5th_Edition)_Character_Sheet.pdf"
        pdf_output = "Spheres_of_Power_and_Might_-_" + Character_Name.replace(" ", "_") + ".pdf"
        
        #EXECUTE FUNCTIONS
        Spheres_5th_Edition_Engine.fill_simple_pdf_file(sample_data_dict, pdf_template, pdf_output)
#----------------------------------------------------------------------------#

#----------------------------------------------------------------------------#
#INTERFACE
##MAIN WINDOW - SETUP
root = tk.Tk()
root.title("Spheres of Power and Might (5th Edition) - Character Sheet Generator")
tabControl = ttk.Notebook(root) #Notebook(master=None, options) - The options accepted by the Notebook() method are height, padding and width
validation_number = root.register(only_numbers)

##TABS - SETUP
tab1 = ttk.Frame(tabControl)    #Frame(master=None, options) - The options accepted by the Frame() method are class_, cursor, padding, relief, style, takefocus, height and width
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)
tab5 = ttk.Frame(tabControl)
tab6 = ttk.Frame(tabControl)
tabControl.add(tab1, text="Basics")  #add(child, options) - The options supported by add() method are sticky, state, padding, text, image, compound and underline
tabControl.add(tab2, text="Stats")
tabControl.add(tab3, text="Proficiencies and Languages")
tabControl.add(tab4, text="Equipment")
tabControl.add(tab5, text="Combat")
tabControl.add(tab6, text="Generate")
tabControl.pack(expand=1, fill="both")  #Packing the tab control to make the tabs visible

##TABS - CONTENT
###INPUTS
INPUT_PLAYER_NAME = tk.StringVar()
INPUT_CHARACTER_NAME = tk.StringVar()
INPUT_RACE = tk.StringVar()
INPUT_CLASS = tk.StringVar()
INPUT_BACKGROUND = tk.StringVar()
INPUT_ALIGNMENT = tk.StringVar()
INPUT_LEVEL = tk.StringVar()
INPUT_AGE = tk.StringVar()
INPUT_HEIGHT = tk.StringVar()
INPUT_TRADITION = tk.StringVar()
INPUT_KAM = tk.StringVar()
INPUT_MARTIAL_FOCUS = tk.IntVar()
INPUT_PROFICIENCY_MODIFIER = tk.StringVar()
INPUT_ATR_STRENGTH = tk.StringVar()
INPUT_ATR_DEXTERITY = tk.StringVar()
INPUT_ATR_CONSTITUTION = tk.StringVar()
INPUT_ATR_INTELLIGENCE = tk.StringVar()
INPUT_ATR_WISDOM = tk.StringVar()
INPUT_ATR_CHARISMA = tk.StringVar()
INPUT_PROF_ACROBATICS = tk.IntVar()
INPUT_PROF_ANIMAL_HANDLING = tk.IntVar()
INPUT_PROF_ARCANA = tk.IntVar()
INPUT_PROF_ATHLETICS = tk.IntVar()
INPUT_PROF_DECEPTION = tk.IntVar()
INPUT_PROF_HISTORY = tk.IntVar()
INPUT_PROF_INSIGHT = tk.IntVar()
INPUT_PROF_INTIMIDATION = tk.IntVar()
INPUT_PROF_INVESTIGATON = tk.IntVar()
INPUT_PROF_MEDICINE = tk.IntVar()
INPUT_PROF_NATURE = tk.IntVar()
INPUT_PROF_PERCEPTION = tk.IntVar()
INPUT_PROF_PERFORMANCE = tk.IntVar()
INPUT_PROF_PERSUASION = tk.IntVar()
INPUT_PROF_RELIGION = tk.IntVar()
INPUT_PROF_SLEIGHT_OF_HAND = tk.IntVar()
INPUT_PROF_STEALTH = tk.IntVar()
INPUT_PROF_SURVIVAL = tk.IntVar()
INPUT_SAV_THROW_STR = tk.IntVar()
INPUT_SAV_THROW_DEX = tk.IntVar()
INPUT_SAV_THROW_CON = tk.IntVar()
INPUT_SAV_THROW_INT = tk.IntVar()
INPUT_SAV_THROW_WIS = tk.IntVar()
INPUT_SAV_THROW_CHA = tk.IntVar()
INPUT_KIT_PROEF_01 = tk.IntVar()
INPUT_KIT_PROEF_02 = tk.IntVar()
INPUT_KIT_PROEF_03 = tk.IntVar()
INPUT_KIT_PROEF_04 = tk.IntVar()
INPUT_KIT_PROEF_05 = tk.IntVar()
INPUT_KIT_PROEF_06 = tk.IntVar()
INPUT_KIT_NAME_01 = tk.StringVar()
INPUT_KIT_NAME_02 = tk.StringVar()
INPUT_KIT_NAME_03 = tk.StringVar()
INPUT_KIT_NAME_04 = tk.StringVar()
INPUT_KIT_NAME_05 = tk.StringVar()
INPUT_KIT_NAME_06 = tk.StringVar()
INPUT_LANGUAGE_01 = tk.StringVar()
INPUT_LANGUAGE_02 = tk.StringVar()
INPUT_LANGUAGE_03 = tk.StringVar()
INPUT_LANGUAGE_04 = tk.StringVar()
INPUT_LANGUAGE_05 = tk.StringVar()
INPUT_LANGUAGE_06 = tk.StringVar()
INPUT_LANGUAGE_07 = tk.StringVar()
INPUT_LANGUAGE_08 = tk.StringVar()
INPUT_LANGUAGE_09 = tk.StringVar()
INPUT_LANGUAGE_10 = tk.StringVar()
INPUT_LANGUAGE_11 = tk.StringVar()
INPUT_LANGUAGE_12 = tk.StringVar()
INPUT_LANGUAGE_13 = tk.StringVar()
INPUT_LANGUAGE_14 = tk.StringVar()
INPUT_OTHER_PROF_01 = tk.StringVar()
INPUT_OTHER_PROF_02 = tk.StringVar()
INPUT_OTHER_PROF_03 = tk.StringVar()
INPUT_OTHER_PROF_04 = tk.StringVar()
INPUT_OTHER_PROF_05 = tk.StringVar()
INPUT_OTHER_PROF_06 = tk.StringVar()
INPUT_OTHER_PROF_07 = tk.StringVar()
INPUT_OTHER_PROF_08 = tk.StringVar()
INPUT_OTHER_PROF_09 = tk.StringVar()
INPUT_OTHER_PROF_10 = tk.StringVar()
INPUT_OTHER_PROF_11 = tk.StringVar()
INPUT_OTHER_PROF_12 = tk.StringVar()
INPUT_OTHER_PROF_13 = tk.StringVar()
INPUT_OTHER_PROF_14 = tk.StringVar()
INPUT_CURR_CP = tk.StringVar()
INPUT_CURR_SP = tk.StringVar()
INPUT_CURR_GP = tk.StringVar()
INPUT_CURR_PP = tk.StringVar()
INPUT_WEAPON_NAME_01 = tk.StringVar()
INPUT_WEAPON_ATTACK_BONUS_01 = tk.StringVar()
INPUT_WEAPON_DAMAGE_01 = tk.StringVar()
INPUT_WEAPON_TYPE_01 = tk.StringVar()
INPUT_WEAPON_OTHER_01 = tk.StringVar()
INPUT_WEAPON_NAME_02 = tk.StringVar()
INPUT_WEAPON_ATTACK_BONUS_02 = tk.StringVar()
INPUT_WEAPON_DAMAGE_02 = tk.StringVar()
INPUT_WEAPON_TYPE_02 = tk.StringVar()
INPUT_WEAPON_OTHER_02 = tk.StringVar()
INPUT_WEAPON_NAME_03 = tk.StringVar()
INPUT_WEAPON_ATTACK_BONUS_03 = tk.StringVar()
INPUT_WEAPON_DAMAGE_03 = tk.StringVar()
INPUT_WEAPON_TYPE_03 = tk.StringVar()
INPUT_WEAPON_OTHER_03 = tk.StringVar()
INPUT_WEAPON_NAME_04 = tk.StringVar()
INPUT_WEAPON_ATTACK_BONUS_04 = tk.StringVar()
INPUT_WEAPON_DAMAGE_04 = tk.StringVar()
INPUT_WEAPON_TYPE_04 = tk.StringVar()
INPUT_WEAPON_OTHER_04 = tk.StringVar()
INPUT_COMBAT_AC = tk.StringVar()
INPUT_COMBAT_HP = tk.StringVar()
INPUT_COMBAT_SPEED = tk.StringVar()
INPUT_COMBAT_HDSides = tk.StringVar()

###TAB 01
ttk.Label(tab1, text = "D&D 5th Edition").grid(column = 0, row = 0, padx = 5, pady = 10, columnspan = 6)

ttk.Label(tab1, text = "Player Name:").grid(column = 0, row = 1, padx = 5, pady = 10, sticky = "e")
ttk.Entry(tab1, textvariable = INPUT_PLAYER_NAME).grid(column = 1, row = 1, padx = 5, pady = 10)

ttk.Label(tab1, text = "Character Name:").grid(column = 2, row = 1, padx = 5, pady = 10, sticky = "e")
ttk.Entry(tab1, textvariable = INPUT_CHARACTER_NAME).grid(column = 3, row = 1, padx = 5, pady = 10)

ttk.Label(tab1, text = "Race:").grid(column = 4, row = 1, padx = 5, pady = 10, sticky = "e")
ttk.Entry(tab1, textvariable = INPUT_RACE).grid(column = 5, row = 1, padx = 5, pady = 10)

ttk.Label(tab1, text = "Class:").grid(column = 0, row = 2, padx = 5, pady = 10, sticky = "e")
ttk.Entry(tab1, textvariable = INPUT_CLASS).grid(column = 1, row = 2, padx = 5, pady = 10)

ttk.Label(tab1, text = "Background:").grid(column = 2, row = 2, padx = 5, pady = 10, sticky = "e")
ttk.Entry(tab1, textvariable = INPUT_BACKGROUND).grid(column = 3, row = 2, padx = 5, pady = 10)

ALIGNMENT_OPTIONS = [
        "Lawful good",
        "Neutral good",
        "Chaotic good",
        "Lawful neutral",
        "True neutral",
        "Chaotic neutral",
        "Lawful evil",
        "Neutral evil",
        "Chaotic evil"
        ]
ttk.Label(tab1, text = "Alignment:").grid(column = 4, row = 2, padx = 5, pady = 10, sticky = "e")
ttk.OptionMenu(tab1, INPUT_ALIGNMENT, ALIGNMENT_OPTIONS[0], *ALIGNMENT_OPTIONS).grid(column = 5, row = 2, padx = 5, pady = 10, sticky = "w")

ttk.Label(tab1, text = "Level:").grid(column = 0, row = 3, padx = 5, pady = 10, sticky = "e")
ttk.Entry(tab1, textvariable = INPUT_LEVEL, width = 3, validate="key", validatecommand=(validation_number, '%S')).grid(column = 1, row = 3, padx = 5, pady = 10, sticky = "w")
INPUT_LEVEL.trace("w", lambda *args: character_limit(INPUT_LEVEL, 2))

ttk.Label(tab1, text = "Age:").grid(column = 2, row = 3, padx = 5, pady = 10, sticky = "e")
ttk.Entry(tab1, textvariable = INPUT_AGE, width = 4, validate = "key", validatecommand=(validation_number, '%S')).grid(column = 3, row = 3, padx = 5, pady = 10, sticky = "w")

ttk.Label(tab1, text = "Height:").grid(column = 4, row = 3, padx = 5, pady = 10, sticky = "e")
ttk.Entry(tab1, textvariable = INPUT_HEIGHT, width = 5).grid(column = 5, row = 3, padx = 5, pady = 10, sticky = "w")

ttk.Label(tab1, text = "Spheres of Power and Might").grid(column = 0, row = 4, padx = 5, pady = 10, columnspan = 6)

ttk.Label(tab1, text = "Tradition:").grid(column = 0, row = 5, padx = 5, pady = 10, sticky = "e")
ttk.Entry(tab1, textvariable = INPUT_TRADITION).grid(column = 1, row = 5, padx = 5, pady = 10)

KAM_OPTIONS = [
        "STR",
        "DEX",
        "CON",
        "INT",
        "WIS",
        "CHA"
        ]
ttk.Label(tab1, text = "KAM:").grid(column = 2, row = 5, padx = 5, pady = 10, sticky = "e")
ttk.OptionMenu(tab1, INPUT_KAM, KAM_OPTIONS[0], *KAM_OPTIONS).grid(column = 3, row = 5, padx = 5, pady = 10, sticky = "w")

ttk.Checkbutton(tab1, text = "Martial Focus?", variable = INPUT_MARTIAL_FOCUS, onvalue = 1, offvalue = 0).grid(column = 4, row = 5, padx = 5, pady = 10, sticky = "w")

###TAB 02
ttk.Label(tab2, text = "Attributes").grid(column = 0, columnspan = 2, row = 0, padx = 5, pady = 10)

ttk.Label(tab2, text = "Proficiency").grid(column = 0, row = 1, padx = 5, pady = 10, sticky = "e")
ttk.Entry(tab2, textvariable = INPUT_PROFICIENCY_MODIFIER, width = 3, validate="key", validatecommand=(validation_number, '%S')).grid(column = 1, row = 1, padx = 5, pady = 10, sticky = "w")
INPUT_PROFICIENCY_MODIFIER.trace("w", lambda *args: character_limit(INPUT_PROFICIENCY_MODIFIER, 2))

ttk.Label(tab2, text = "STR").grid(column = 0, row = 2, padx = 5, pady = 10, sticky = "e")
ttk.Entry(tab2, textvariable = INPUT_ATR_STRENGTH, width = 3, validate="key", validatecommand=(validation_number, '%S')).grid(column = 1, row = 2, padx = 5, pady = 10, sticky = "w")
INPUT_ATR_STRENGTH.trace("w", lambda *args: character_limit(INPUT_ATR_STRENGTH, 2))

ttk.Label(tab2, text = "DEX").grid(column = 0, row = 3, padx = 5, pady = 10, sticky = "e")
ttk.Entry(tab2, textvariable = INPUT_ATR_DEXTERITY, width = 3, validate="key", validatecommand=(validation_number, '%S')).grid(column = 1, row = 3, padx = 5, pady = 10, sticky = "w")
INPUT_ATR_DEXTERITY.trace("w", lambda *args: character_limit(INPUT_ATR_DEXTERITY, 2))

ttk.Label(tab2, text = "CON").grid(column = 0, row = 4, padx = 5, pady = 10, sticky = "e")
ttk.Entry(tab2, textvariable = INPUT_ATR_CONSTITUTION, width = 3, validate="key", validatecommand=(validation_number, '%S')).grid(column = 1, row = 4, padx = 5, pady = 10, sticky = "w")
INPUT_ATR_CONSTITUTION.trace("w", lambda *args: character_limit(INPUT_ATR_CONSTITUTION, 2))

ttk.Label(tab2, text = "INT").grid(column = 0, row = 5, padx = 5, pady = 10, sticky = "e")
ttk.Entry(tab2, textvariable = INPUT_ATR_INTELLIGENCE, width = 3, validate="key", validatecommand=(validation_number, '%S')).grid(column = 1, row = 5, padx = 5, pady = 10, sticky = "w")
INPUT_ATR_INTELLIGENCE.trace("w", lambda *args: character_limit(INPUT_ATR_INTELLIGENCE, 2))

ttk.Label(tab2, text = "WIS").grid(column = 0, row = 6, padx = 5, pady = 10, sticky = "e")
ttk.Entry(tab2, textvariable = INPUT_ATR_WISDOM, width = 3, validate="key", validatecommand=(validation_number, '%S')).grid(column = 1, row = 6, padx = 5, pady = 10, sticky = "w")
INPUT_ATR_WISDOM.trace("w", lambda *args: character_limit(INPUT_ATR_WISDOM, 2))

ttk.Label(tab2, text = "CHA").grid(column = 0, row = 7, padx = 5, pady = 10, sticky = "e")
ttk.Entry(tab2, textvariable = INPUT_ATR_CHARISMA, width = 3, validate="key", validatecommand=(validation_number, '%S')).grid(column = 1, row = 7, padx = 5, pady = 10, sticky = "w")
INPUT_ATR_CHARISMA.trace("w", lambda *args: character_limit(INPUT_ATR_CHARISMA, 2))

ttk.Label(tab2, text = "Skill proficiencies").grid(column = 2, columnspan = 2, row = 0, padx = 5, pady = 10)

ttk.Checkbutton(tab2, text = "Acrobatics", variable = INPUT_PROF_ACROBATICS, onvalue = 1, offvalue = 0).grid(column = 2, row = 1, padx = 5, pady = 10, sticky = "w")
ttk.Checkbutton(tab2, text = "Animal Handling", variable = INPUT_PROF_ANIMAL_HANDLING, onvalue = 1, offvalue = 0).grid(column = 2, row = 2, padx = 5, pady = 10, sticky = "w")
ttk.Checkbutton(tab2, text = "Arcana", variable = INPUT_PROF_ARCANA, onvalue = 1, offvalue = 0).grid(column = 2, row = 3, padx = 5, pady = 10, sticky = "w")
ttk.Checkbutton(tab2, text = "Athletics", variable = INPUT_PROF_ATHLETICS, onvalue = 1, offvalue = 0).grid(column = 2, row = 4, padx = 5, pady = 10, sticky = "w")
ttk.Checkbutton(tab2, text = "Deception", variable = INPUT_PROF_DECEPTION, onvalue = 1, offvalue = 0).grid(column = 2, row = 5, padx = 5, pady = 10, sticky = "w")
ttk.Checkbutton(tab2, text = "History", variable = INPUT_PROF_HISTORY, onvalue = 1, offvalue = 0).grid(column = 2, row = 6, padx = 5, pady = 10, sticky = "w")
ttk.Checkbutton(tab2, text = "Insight", variable = INPUT_PROF_INSIGHT, onvalue = 1, offvalue = 0).grid(column = 2, row = 7, padx = 5, pady = 10, sticky = "w")
ttk.Checkbutton(tab2, text = "Intimidation", variable = INPUT_PROF_INTIMIDATION, onvalue = 1, offvalue = 0).grid(column = 2, row = 8, padx = 5, pady = 10, sticky = "w")
ttk.Checkbutton(tab2, text = "Investigation", variable = INPUT_PROF_INVESTIGATON, onvalue = 1, offvalue = 0).grid(column = 2, row = 9, padx = 5, pady = 10, sticky = "w")

ttk.Checkbutton(tab2, text = "Medicine", variable = INPUT_PROF_MEDICINE, onvalue = 1, offvalue = 0).grid(column = 3, row = 1, padx = 5, pady = 10, sticky = "w")
ttk.Checkbutton(tab2, text = "Nature", variable = INPUT_PROF_NATURE, onvalue = 1, offvalue = 0).grid(column = 3, row = 2, padx = 5, pady = 10, sticky = "w")
ttk.Checkbutton(tab2, text = "Perception", variable = INPUT_PROF_PERCEPTION, onvalue = 1, offvalue = 0).grid(column = 3, row = 3, padx = 5, pady = 10, sticky = "w")
ttk.Checkbutton(tab2, text = "Performance", variable = INPUT_PROF_PERFORMANCE, onvalue = 1, offvalue = 0).grid(column = 3, row = 4, padx = 5, pady = 10, sticky = "w")
ttk.Checkbutton(tab2, text = "Persuasion", variable = INPUT_PROF_PERSUASION, onvalue = 1, offvalue = 0).grid(column = 3, row = 5, padx = 5, pady = 10, sticky = "w")
ttk.Checkbutton(tab2, text = "Religion", variable = INPUT_PROF_RELIGION, onvalue = 1, offvalue = 0).grid(column = 3, row = 6, padx = 5, pady = 10, sticky = "w")
ttk.Checkbutton(tab2, text = "Sleight of Hand", variable = INPUT_PROF_SLEIGHT_OF_HAND, onvalue = 1, offvalue = 0).grid(column = 3, row = 7, padx = 5, pady = 10, sticky = "w")
ttk.Checkbutton(tab2, text = "Stealth", variable = INPUT_PROF_STEALTH, onvalue = 1, offvalue = 0).grid(column = 3, row = 8, padx = 5, pady = 10, sticky = "w")
ttk.Checkbutton(tab2, text = "Survival", variable = INPUT_PROF_SURVIVAL, onvalue = 1, offvalue = 0).grid(column = 3, row = 9, padx = 5, pady = 10, sticky = "w")

ttk.Label(tab2, text = "Saving throws proficiencies").grid(column = 4, columnspan = 2, row = 0, padx = 5, pady = 10)

ttk.Checkbutton(tab2, text = "STR", variable = INPUT_SAV_THROW_STR, onvalue = 1, offvalue = 0).grid(column = 4, row = 1, padx = 5, pady = 10, sticky = "w")
ttk.Checkbutton(tab2, text = "DEX", variable = INPUT_SAV_THROW_DEX, onvalue = 1, offvalue = 0).grid(column = 4, row = 2, padx = 5, pady = 10, sticky = "w")
ttk.Checkbutton(tab2, text = "CON", variable = INPUT_SAV_THROW_CON, onvalue = 1, offvalue = 0).grid(column = 4, row = 3, padx = 5, pady = 10, sticky = "w")

ttk.Checkbutton(tab2, text = "INT", variable = INPUT_SAV_THROW_INT, onvalue = 1, offvalue = 0).grid(column = 5, row = 1, padx = 5, pady = 10, sticky = "w")
ttk.Checkbutton(tab2, text = "WIS", variable = INPUT_SAV_THROW_WIS, onvalue = 1, offvalue = 0).grid(column = 5, row = 2, padx = 5, pady = 10, sticky = "w")
ttk.Checkbutton(tab2, text = "CHA", variable = INPUT_SAV_THROW_CHA, onvalue = 1, offvalue = 0).grid(column = 5, row = 3, padx = 5, pady = 10, sticky = "w")

###TAB 03
ttk.Label(tab3, text = "Tools and Kits").grid(column = 0, columnspan = 2, row = 0, padx = 5, pady = 10)

ttk.Label(tab3, text = "Proficiency").grid(column = 0, row = 1, padx = 5, pady = 10)
ttk.Label(tab3, text = "Tool / Kit").grid(column = 1, row = 1, padx = 5, pady = 10)

ttk.Checkbutton(tab3, variable = INPUT_KIT_PROEF_01, onvalue = 1, offvalue = 0).grid(column = 0, row = 2, padx = 5, pady = 10)
ttk.Entry(tab3, textvariable = INPUT_KIT_NAME_01).grid(column = 1, row = 2, padx = 5, pady = 10)

ttk.Checkbutton(tab3, variable = INPUT_KIT_PROEF_02, onvalue = 1, offvalue = 0).grid(column = 0, row = 3, padx = 5, pady = 10)
ttk.Entry(tab3, textvariable = INPUT_KIT_NAME_02).grid(column = 1, row = 3, padx = 5, pady = 10)

ttk.Checkbutton(tab3, variable = INPUT_KIT_PROEF_03, onvalue = 1, offvalue = 0).grid(column = 0, row = 4, padx = 5, pady = 10)
ttk.Entry(tab3, textvariable = INPUT_KIT_NAME_03).grid(column = 1, row = 4, padx = 5, pady = 10)

ttk.Checkbutton(tab3, variable = INPUT_KIT_PROEF_04, onvalue = 1, offvalue = 0).grid(column = 0, row = 5, padx = 5, pady = 10)
ttk.Entry(tab3, textvariable = INPUT_KIT_NAME_04).grid(column = 1, row = 5, padx = 5, pady = 10)

ttk.Checkbutton(tab3, variable = INPUT_KIT_PROEF_05, onvalue = 1, offvalue = 0).grid(column = 0, row = 6, padx = 5, pady = 10)
ttk.Entry(tab3, textvariable = INPUT_KIT_NAME_05).grid(column = 1, row = 6, padx = 5, pady = 10)

ttk.Checkbutton(tab3, variable = INPUT_KIT_PROEF_06, onvalue = 1, offvalue = 0).grid(column = 0, row = 7, padx = 5, pady = 10)
ttk.Entry(tab3, textvariable = INPUT_KIT_NAME_06).grid(column = 1, row = 7, padx = 5, pady = 10)

ttk.Label(tab3, text = "Languages").grid(column = 2, columnspan = 2, row = 0, padx = 5, pady = 10)

ttk.Entry(tab3, textvariable = INPUT_LANGUAGE_01).grid(column = 2, row = 1, padx = 5, pady = 10)

ttk.Entry(tab3, textvariable = INPUT_LANGUAGE_02).grid(column = 3, row = 1, padx = 5, pady = 10)

ttk.Entry(tab3, textvariable = INPUT_LANGUAGE_03).grid(column = 2, row = 2, padx = 5, pady = 10)

ttk.Entry(tab3, textvariable = INPUT_LANGUAGE_04).grid(column = 3, row = 2, padx = 5, pady = 10)

ttk.Entry(tab3, textvariable = INPUT_LANGUAGE_05).grid(column = 2, row = 3, padx = 5, pady = 10)

ttk.Entry(tab3, textvariable = INPUT_LANGUAGE_06).grid(column = 3, row = 3, padx = 5, pady = 10)

ttk.Entry(tab3, textvariable = INPUT_LANGUAGE_07).grid(column = 2, row = 4, padx = 5, pady = 10)

ttk.Entry(tab3, textvariable = INPUT_LANGUAGE_08).grid(column = 3, row = 4, padx = 5, pady = 10)

ttk.Entry(tab3, textvariable = INPUT_LANGUAGE_09).grid(column = 2, row = 5, padx = 5, pady = 10)

ttk.Entry(tab3, textvariable = INPUT_LANGUAGE_10).grid(column = 3, row = 5, padx = 5, pady = 10)

ttk.Entry(tab3, textvariable = INPUT_LANGUAGE_11).grid(column = 2, row = 6, padx = 5, pady = 10)

ttk.Entry(tab3, textvariable = INPUT_LANGUAGE_12).grid(column = 3, row = 6, padx = 5, pady = 10)

ttk.Entry(tab3, textvariable = INPUT_LANGUAGE_13).grid(column = 2, row = 7, padx = 5, pady = 10)

ttk.Entry(tab3, textvariable = INPUT_LANGUAGE_14).grid(column = 3, row = 7, padx = 5, pady = 10)

ttk.Label(tab3, text = "Other Proficiencies").grid(column = 4, columnspan = 2, row = 0, padx = 5, pady = 10)

ttk.Entry(tab3, textvariable = INPUT_OTHER_PROF_01).grid(column = 4, row = 1, padx = 5, pady = 10)

ttk.Entry(tab3, textvariable = INPUT_OTHER_PROF_02).grid(column = 5, row = 1, padx = 5, pady = 10)

ttk.Entry(tab3, textvariable = INPUT_OTHER_PROF_03).grid(column = 4, row = 2, padx = 5, pady = 10)

ttk.Entry(tab3, textvariable = INPUT_OTHER_PROF_04).grid(column = 5, row = 2, padx = 5, pady = 10)

ttk.Entry(tab3, textvariable = INPUT_OTHER_PROF_05).grid(column = 4, row = 3, padx = 5, pady = 10)

ttk.Entry(tab3, textvariable = INPUT_OTHER_PROF_06).grid(column = 5, row = 3, padx = 5, pady = 10)

ttk.Entry(tab3, textvariable = INPUT_OTHER_PROF_07).grid(column = 4, row = 4, padx = 5, pady = 10)

ttk.Entry(tab3, textvariable = INPUT_OTHER_PROF_08).grid(column = 5, row = 4, padx = 5, pady = 10)

ttk.Entry(tab3, textvariable = INPUT_OTHER_PROF_09).grid(column = 4, row = 5, padx = 5, pady = 10)

ttk.Entry(tab3, textvariable = INPUT_OTHER_PROF_10).grid(column = 5, row = 5, padx = 5, pady = 10)

ttk.Entry(tab3, textvariable = INPUT_OTHER_PROF_11).grid(column = 4, row = 6, padx = 5, pady = 10)

ttk.Entry(tab3, textvariable = INPUT_OTHER_PROF_12).grid(column = 5, row = 6, padx = 5, pady = 10)

ttk.Entry(tab3, textvariable = INPUT_OTHER_PROF_13).grid(column = 4, row = 7, padx = 5, pady = 10)

ttk.Entry(tab3, textvariable = INPUT_OTHER_PROF_14).grid(column = 5, row = 7, padx = 5, pady = 10)

###TAB 04
ttk.Label(tab4, text = "Currency").grid(column = 0, columnspan = 4, row = 0, padx = 5, pady = 10)

ttk.Label(tab4, text = "CP").grid(column = 0, row = 1, padx = 5, pady = 10)
ttk.Entry(tab4, textvariable = INPUT_CURR_CP, width = 4, validate="key", validatecommand=(validation_number, '%S')).grid(column = 0, row = 2, padx = 5, pady = 10, sticky = "w")
INPUT_CURR_CP.trace("w", lambda *args: character_limit(INPUT_CURR_CP, 3))

ttk.Label(tab4, text = "SP").grid(column = 1, row = 1, padx = 5, pady = 10)
ttk.Entry(tab4, textvariable = INPUT_CURR_SP, width = 4, validate="key", validatecommand=(validation_number, '%S')).grid(column = 1, row = 2, padx = 5, pady = 10, sticky = "w")
INPUT_CURR_SP.trace("w", lambda *args: character_limit(INPUT_CURR_SP, 3))

ttk.Label(tab4, text = "GP").grid(column = 2, row = 1, padx = 5, pady = 10)
ttk.Entry(tab4, textvariable = INPUT_CURR_GP, width = 4, validate="key", validatecommand=(validation_number, '%S')).grid(column = 2, row = 2, padx = 5, pady = 10, sticky = "w")
INPUT_CURR_GP.trace("w", lambda *args: character_limit(INPUT_CURR_GP, 3))

ttk.Label(tab4, text = "PP").grid(column = 3, row = 1, padx = 5, pady = 10)
ttk.Entry(tab4, textvariable = INPUT_CURR_PP, width = 4, validate="key", validatecommand=(validation_number, '%S')).grid(column = 3, row = 2, padx = 5, pady = 10, sticky = "w")
INPUT_CURR_PP.trace("w", lambda *args: character_limit(INPUT_CURR_PP, 3))

ttk.Label(tab4, text = "Equipment").grid(column = 0, columnspan = 4, row = 3, padx = 5, pady = 10)

INPUT_EQUIPMENT = tk.Text(tab4, width = 20, height = 12)
INPUT_EQUIPMENT.grid(column = 0, columnspan = 4, row = 4, rowspan = 12, padx = 5, pady = 10)

ttk.Label(tab4, text = "Weapons").grid(column = 4, columnspan = 8, row = 0, padx = 5, pady = 10)

ttk.Label(tab4, text = "Name").grid(column = 4, row = 1, padx = 5, pady = 10)
ttk.Entry(tab4, textvariable = INPUT_WEAPON_NAME_01).grid(column = 4, row = 2, padx = 5, pady = 10)

ttk.Label(tab4, text = "Attack Bonus").grid(column = 5, row = 1, padx = 5, pady = 10)
ttk.Entry(tab4, textvariable = INPUT_WEAPON_ATTACK_BONUS_01, width = 3, validate="key", validatecommand=(validation_number, '%S')).grid(column = 5, row = 2, padx = 5, pady = 10)
INPUT_WEAPON_ATTACK_BONUS_01.trace("w", lambda *args: character_limit(INPUT_WEAPON_ATTACK_BONUS_01, 2))

ttk.Label(tab4, text = "Damage").grid(column = 6, row = 1, padx = 5, pady = 10)
ttk.Entry(tab4, textvariable = INPUT_WEAPON_DAMAGE_01, width = 4).grid(column = 6, row = 2, padx = 5, pady = 10)

ttk.Label(tab4, text = "Type").grid(column = 7, row = 1, padx = 5, pady = 10)
ttk.Entry(tab4, textvariable = INPUT_WEAPON_TYPE_01, width = 6).grid(column = 7, row = 2, padx = 5, pady = 10)

ttk.Label(tab4, text = "Other").grid(column = 4, row = 3, padx = 5, pady = 10)
ttk.Entry(tab4, textvariable = INPUT_WEAPON_OTHER_01, width = 30).grid(column = 5, columnspan = 3, row = 3, padx = 5, pady = 10)

ttk.Label(tab4, text = "Name").grid(column = 4, row = 4, padx = 5, pady = 10)
ttk.Entry(tab4, textvariable = INPUT_WEAPON_NAME_02).grid(column = 4, row = 5, padx = 5, pady = 10)

ttk.Label(tab4, text = "Attack Bonus").grid(column = 5, row = 4, padx = 5, pady = 10)
ttk.Entry(tab4, textvariable = INPUT_WEAPON_ATTACK_BONUS_02, width = 3, validate="key", validatecommand=(validation_number, '%S')).grid(column = 5, row = 5, padx = 5, pady = 10)
INPUT_WEAPON_ATTACK_BONUS_02.trace("w", lambda *args: character_limit(INPUT_WEAPON_ATTACK_BONUS_02, 2))

ttk.Label(tab4, text = "Damage").grid(column = 6, row = 4, padx = 5, pady = 10)
ttk.Entry(tab4, textvariable = INPUT_WEAPON_DAMAGE_02, width = 4).grid(column = 6, row = 5, padx = 5, pady = 10)

ttk.Label(tab4, text = "Type").grid(column = 7, row = 4, padx = 5, pady = 10)
ttk.Entry(tab4, textvariable = INPUT_WEAPON_TYPE_02, width = 6).grid(column = 7, row = 5, padx = 5, pady = 10)

ttk.Label(tab4, text = "Other").grid(column = 4, row = 6, padx = 5, pady = 10)
ttk.Entry(tab4, textvariable = INPUT_WEAPON_OTHER_02, width = 30).grid(column = 5, columnspan = 3, row = 6, padx = 5, pady = 10)

ttk.Label(tab4, text = "Name").grid(column = 8, row = 1, padx = 5, pady = 10)
ttk.Entry(tab4, textvariable = INPUT_WEAPON_NAME_03).grid(column = 8, row = 2, padx = 5, pady = 10)

ttk.Label(tab4, text = "Attack Bonus").grid(column = 9, row = 1, padx = 5, pady = 10)
ttk.Entry(tab4, textvariable = INPUT_WEAPON_ATTACK_BONUS_03, width = 3, validate="key", validatecommand=(validation_number, '%S')).grid(column = 9, row = 2, padx = 5, pady = 10)
INPUT_WEAPON_ATTACK_BONUS_03.trace("w", lambda *args: character_limit(INPUT_WEAPON_ATTACK_BONUS_03, 2))

ttk.Label(tab4, text = "Damage").grid(column = 10, row = 1, padx = 5, pady = 10)
ttk.Entry(tab4, textvariable = INPUT_WEAPON_DAMAGE_03, width = 4).grid(column = 10, row = 2, padx = 5, pady = 10)

ttk.Label(tab4, text = "Type").grid(column = 11, row = 1, padx = 5, pady = 10)
ttk.Entry(tab4, textvariable = INPUT_WEAPON_TYPE_03, width = 6).grid(column = 11, row = 2, padx = 5, pady = 10)

ttk.Label(tab4, text = "Other").grid(column = 8, row = 3, padx = 5, pady = 10)
ttk.Entry(tab4, textvariable = INPUT_WEAPON_OTHER_03, width = 30).grid(column = 9, columnspan = 3, row = 3, padx = 5, pady = 10)

ttk.Label(tab4, text = "Name").grid(column = 8, row = 4, padx = 5, pady = 10)
ttk.Entry(tab4, textvariable = INPUT_WEAPON_NAME_04).grid(column = 8, row = 5, padx = 5, pady = 10)

ttk.Label(tab4, text = "Attack Bonus").grid(column = 9, row = 4, padx = 5, pady = 10)
ttk.Entry(tab4, textvariable = INPUT_WEAPON_ATTACK_BONUS_04, width = 3, validate="key", validatecommand=(validation_number, '%S')).grid(column = 9, row = 5, padx = 5, pady = 10)
INPUT_WEAPON_ATTACK_BONUS_04.trace("w", lambda *args: character_limit(INPUT_WEAPON_ATTACK_BONUS_04, 2))

ttk.Label(tab4, text = "Damage").grid(column = 10, row = 4, padx = 5, pady = 10)
ttk.Entry(tab4, textvariable = INPUT_WEAPON_DAMAGE_04, width = 4).grid(column = 10, row = 5, padx = 5, pady = 10)

ttk.Label(tab4, text = "Type").grid(column = 11, row = 4, padx = 5, pady = 10)
ttk.Entry(tab4, textvariable = INPUT_WEAPON_TYPE_04, width = 6).grid(column = 11, row = 5, padx = 5, pady = 10)

ttk.Label(tab4, text = "Other").grid(column = 8, row = 6, padx = 5, pady = 10)
ttk.Entry(tab4, textvariable = INPUT_WEAPON_OTHER_04, width = 30).grid(column = 9, columnspan = 3, row = 6, padx = 5, pady = 10)

###TAB 05
ttk.Label(tab5, text = "AC:").grid(column = 0, row = 0, padx = 5, pady = 10, sticky = "e")
ttk.Entry(tab5, textvariable = INPUT_COMBAT_AC, width = 3, validate = "key", validatecommand=(validation_number, '%S')).grid(column = 1, row = 0, padx = 5, pady = 10, sticky = "w")

ttk.Label(tab5, text = "Maximum HP (without CON modifier):").grid(column = 2, row = 0, padx = 5, pady = 10, sticky = "e")
ttk.Entry(tab5, textvariable = INPUT_COMBAT_HP, width = 3, validate = "key", validatecommand=(validation_number, '%S')).grid(column = 3, row = 0, padx = 5, pady = 10, sticky = "w")

ttk.Label(tab5, text = "Speed:").grid(column = 4, row = 0, padx = 5, pady = 10, sticky = "e")
ttk.Entry(tab5, textvariable = INPUT_COMBAT_SPEED, width = 3, validate = "key", validatecommand=(validation_number, '%S')).grid(column = 5, row = 0, padx = 5, pady = 10, sticky = "w")

ttk.Label(tab5, text = "Hit Dice (sides):").grid(column = 6, row = 0, padx = 5, pady = 10, sticky = "e")
ttk.Entry(tab5, textvariable = INPUT_COMBAT_HDSides, width = 3, validate = "key", validatecommand=(validation_number, '%S')).grid(column = 7, row = 0, padx = 5, pady = 10, sticky = "w")

###TAB 06
ttk.Button(tab6, text = "Generate the PDF file", command = Button_Generate_PDF).pack(pady = 30)

##APPLICATION
root.mainloop()
#----------------------------------------------------------------------------#

#----------------------------------------------------------------------------#
#COMPILATION
#!pyinstaller --clean --noconsole --onefile Spheres_5th_Edition_Application.py