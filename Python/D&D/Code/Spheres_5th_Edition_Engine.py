#MODULES
import pdfrw
import math
import textwrap
wrapper = textwrap.TextWrapper(width = 85)

#FUNCTION - DETERMINE CASTING ABILITY MODIFIER (KAM)
def KAM_identifier(KAM):
    KAM_dict = {
            "STR": False,
            "DEX": False,
            "CON": False,
            "INT": False,
            "WIS": False,
            "CHA": False
            }
    KAM_dict[KAM] = True
    return(KAM_dict)
    
#FUNCTION - DETERMINE THE PROFICIENCY MODIFIER SIGN
def Sign_Determination(value):
    if int(value) > 0:
        return(str("+" + str(value)))
    else:
        return(str(value))

#FUNCTION - DETERMINE ROLL BONUS TO SAVING THROWS AND SKILLS
def Roll_bonus(PROFICIENCY, ATTRIBUTE_BONUS, PROFICIENCY_BONUS):
    if ATTRIBUTE_BONUS == "":
        ATTRIBUTE_BONUS = 0
    else:
        ATTRIBUTE_BONUS = max(int(ATTRIBUTE_BONUS), 0)
    if PROFICIENCY_BONUS == "":
        PROFICIENCY_BONUS = 0
    else:
        PROFICIENCY_BONUS = max(int(PROFICIENCY_BONUS), 0)
    if(PROFICIENCY == 1):
        roll_bonus = int(PROFICIENCY_BONUS) + math.floor((int(ATTRIBUTE_BONUS - 10) / 2))
        if(roll_bonus > 0):
            roll_bonus = str("+" + str(roll_bonus))
        return(roll_bonus)
    else:
        roll_bonus = math.floor((int(ATTRIBUTE_BONUS - 10) / 2))
        if(roll_bonus > 0):
            roll_bonus = str("+" + str(roll_bonus))
        return(roll_bonus)
        
#FUNCTION - PASSIVE WISDOM AND INTELLIGENCE
def Passive_Calculation(skill_value, base = 10):
    if(isinstance(skill_value, str)):
        skill_value = skill_value[1:]
        return(base + int(skill_value))
    else:
        return(base + int(skill_value))
    
#FUNCTION - SPELL SAVE DC
def Spell_Save_DC(proficiency, skill_value, base = 8):
    if(isinstance(proficiency, str)):
        proficiency = proficiency[1:]
    if proficiency == '':
        proficiency = 0
    return(base + int(proficiency) + int(skill_value))

#FUNCTION - MAXIMUM HP
def Maximum_HP(HP, CON_Modifier, level):
    return(max(HP + int(CON_Modifier)  * level, 1))
        
#FUNCTION - CONVERT LEVEL TO EXPERIENCE POINTS
def convert_to_experience_points(value):
    level_thresholds = [
            0,
            300,
            900,
            2700,
            6500,
            14000,
            23000,
            34000,
            48000,
            64000,
            85000,
            100000,
            120000,
            140000,
            165000,
            195000,
            225000,
            265000,
            305000,
            355000,
            355000
            ]
    if value > 20:
        value = 20
    return(str(level_thresholds[value - 1]) + " / " + str(level_thresholds[value]))
    
#FUNCTION - TOOL PROFICIENCY BONUS
def Tool_bonus(proficiency, bonus):
    if proficiency == True:
        if int(bonus) > 0:
            return(str("+" + str(bonus)))
        else:
            return("")
    else:
        return("")
        
#FUNCTION - LANGUAGE AND OTHER PROFICIENCIES
def Text_boxes_lang_and_other(langs, others, textbox):
    if textbox == 1:
        if len(langs) <= 6:
            return("Languages: " + ", ".join(langs))
        elif len(langs) > 6:
            return("Languages: " + ', '.join(langs[:6]))
    elif textbox == 2:
        if len(langs) <= 6:
            if len(others) <= 6:
                return("Others: " + ", ".join(others))
            elif (len(others) > 6) & (len(others) <= 14):
                return("Others: " + ", ".join(others[:6]))
        elif len(langs) > 6:
            return(', '.join(langs[6:]))
    elif textbox == 3:
        if len(langs) > 6:
            if len(others) <= 6:
                return("Others: " + ", ".join(others))
            elif len(others) > 6:
                return("Others: " + ", ".join(others[:6]))
        else:
            if len(others) <= 6:
                return("")
            elif len(others) > 6:
                return(", ".join(others[6:]))
    elif textbox == 4:
        if len(langs) > 6:
            if len(others) > 6:
                return(", ".join(others[6:]))
            else:
                return("")
        else:
            return("")

#FUNCTION - TEXT WRAPPING
def text_wrap(string, number):
    number = number - 1
    word_list = wrapper.wrap(text=string)
    if len(word_list) < (number + 1):
        out = ""
    else:
        out = word_list[number]
    return(str(out))

#FUNCTION - FILL PDF
def fill_simple_pdf_file(data, template_input, template_output):
    data_dict = {
            "SAVING THROW": data.get("saving_throws_proficiencies", False)["STR"],
            "SAVING THROW_2": data.get("saving_throws_proficiencies", False)["DEX"],
            "SAVING THROW_3": data.get("saving_throws_proficiencies", False)["CON"],
            "SAVING THROW_4": data.get("saving_throws_proficiencies", False)["INT"],
            "SAVING THROW_5": data.get("saving_throws_proficiencies", False)["WIS"],
            "SAVING THROW_6": data.get("saving_throws_proficiencies", False)["CHA"],
            "Check Box17": data.get("skills_proficiencies", False)["Athletics"],
            "Check Box18": data.get("kam", False)["STR"],
            "Check Box20": data.get("kam", False)["DEX"],
            "Check Box21": data.get("kam", False)["CON"],
            "Check Box22": data.get("kam", False)["INT"],
            "Check Box23": data.get("kam", False)["WIS"],
            "Check Box24": data.get("kam", False)["CHA"],
            "Check Box30": data.get("tools_proficiencies", False)[1],
            "Check Box31": data.get("tools_proficiencies", False)[3],
            "Check Box32": data.get("tools_proficiencies", False)[5],
            "Check Box34": data.get("tools_proficiencies", False)[0],
            "Check Box35": data.get("tools_proficiencies", False)[2],
            "Check Box36": data.get("tools_proficiencies", False)[4],
            "Check Box45": data.get("skills_proficiencies", False)["Acrobatics"],
            "Check Box48": data.get("martial_focus", False),
            "Check Box49": data.get("skills_proficiencies", False)["Sleight of Hand"],
            "Check Box50": data.get("skills_proficiencies", False)["Stealth"],
            "Check Box51": data.get("skills_proficiencies", False)["Arcana"],
            "Check Box52": data.get("skills_proficiencies", False)["History"],
            "Check Box53": data.get("skills_proficiencies", False)["Investigation"],
            "Check Box54": data.get("skills_proficiencies", False)["Nature"],
            "Check Box55": data.get("skills_proficiencies", False)["Religion"],
            "Check Box56": data.get("skills_proficiencies", False)["Animal Handling"],
            "Check Box57": data.get("skills_proficiencies", False)["Insight"],
            "Check Box58": data.get("skills_proficiencies", False)["Medicine"],
            "Check Box59": data.get("skills_proficiencies", False)["Perception"],
            "Check Box60": data.get("skills_proficiencies", False)["Survival"],
            "Check Box61": data.get("skills_proficiencies", False)["Deception"],
            "Check Box62": data.get("skills_proficiencies", False)["Intimidation"],
            "Check Box63": data.get("skills_proficiencies", False)["Performance"],
            "Check Box64": data.get("skills_proficiencies", False)["Persuasion"],
            
            "1": Text_boxes_lang_and_other(data.get("languages", ""), data.get("other_proficiencies", ""), 1),
            "1_2": data.get("weapon_02", "")[4],
            "1_3": data.get("weapon_03", "")[4],
            "1_4": data.get("weapon_04", "")[4],
            "2": Text_boxes_lang_and_other(data.get("languages", ""), data.get("other_proficiencies", ""), 2),
            "2_2": data.get("weapon_03", "")[0],
            "2_3": data.get("weapon_04", "")[0],
            "3": Text_boxes_lang_and_other(data.get("languages", ""), data.get("other_proficiencies", ""), 3),
            "attack bonus 1": data.get("weapon_01", "")[1],
            "Attack Bonus 2": data.get("weapon_02", "")[1],
            "Attack Bonus 3": data.get("weapon_03", "")[1],
            "Attack Bonus 4": data.get("weapon_04", "")[1],
            "Damage1": data.get("weapon_01", "")[2] + " / " + data.get("weapon_01", "")[3],
            "EQUIPMENT 1": text_wrap(data.get("equipment", ""), 1),
            "EQUIPMENT 2": text_wrap(data.get("equipment", ""), 2),
            "EQUIPMENT 3": text_wrap(data.get("equipment", ""), 3),
            "EQUIPMENT 4": text_wrap(data.get("equipment", ""), 4),
            "EQUIPMENT 5": text_wrap(data.get("equipment", ""), 5),
            "EQUIPMENT 6": text_wrap(data.get("equipment", ""), 6),
            "EQUIPMENT 7": text_wrap(data.get("equipment", ""), 7),
            "EQUIPMENT 8": text_wrap(data.get("equipment", ""), 8),
            "EQUIPMENT 9": text_wrap(data.get("equipment", ""), 9),
            "EQUIPMENT 10": text_wrap(data.get("equipment", ""), 10),
            "LANGUAGES AND OTHER PROFICIENCIESI 1": text_wrap(data.get("equipment", ""), 11),
            "LANGUAGES AND OTHER PROFICIENCIESI 2": text_wrap(data.get("equipment", ""), 12),
            "LANGUAGES AND OTHER PROFICIENCIESI 3": text_wrap(data.get("equipment", ""), 13),
            "LANGUAGES AND OTHER PROFICIENCIESI 4": text_wrap(data.get("equipment", ""), 14),
            "OTHER 1": data.get("weapon_01", "")[4],
            "OTHER 2": data.get("weapon_02", "")[0],
            "Str_Score": data.get("ATR", "10")["STR"],
            "undefined": data.get("weapon_02", "")[2] + " / " + data.get("weapon_02", "")[3],
            "undefined_2": data.get("weapon_03", "")[2] + " / " + data.get("weapon_03", "")[3],
            "undefined_3": data.get("weapon_04", "")[2] + " / " + data.get("weapon_04", "")[3],
            "Weapon Name": data.get("weapon_01", "")[0],
            "Text1": data.get("name", ""),
            "Text2": data.get("class", "") + " / " + str(data.get("level", "")),
            "Text3": data.get("background", "") + " / " + data.get("tradition", ""),
            "Text4": data.get("player", ""),
            "Text5": data.get("race", ""),
            "Text6": data.get("alignment", ""),
            "Text11": text_wrap(data.get("equipment", ""), 15),
            "Text12": data.get("currencies", "")[0],
            "Text13": data.get("currencies", "")[1],
            "Text14": data.get("currencies", "")[2],
            "Text15": data.get("currencies", "")[3],
            "Text16": convert_to_experience_points(data.get("level", "")),
            "Text17": data.get("tools_names", False)[0],
            "Text18": data.get("tools_names", False)[2],
            "Text20": data.get("tools_names", False)[1],
            "Text21": data.get("tools_names", False)[3],
            "Text22": data.get("tools_names", False)[5],
            "Text23": data.get("tools_bonus", False)[1],
            "Text24": data.get("tools_bonus", False)[3],
            "Text25": data.get("tools_bonus", False)[5],
            "Text26": data.get("tools_bonus", False)[0],
            "Text27": data.get("tools_bonus", False)[2],
            "Text28": data.get("tools_bonus", False)[4],
            "Text30": data.get("ATR_Modifiers", "0")["STR"],
            "Text31": data.get("ATR", "10")["DEX"],
            "Text32": data.get("ATR_Modifiers", "0")["DEX"],
            "Text33": data.get("ATR", "10")["CON"],
            "Text34": data.get("ATR_Modifiers", "0")["CON"],
            "Text35": data.get("ATR", "10")["INT"],
            "Text36": data.get("ATR_Modifiers", "0")["INT"],
            "Text38": data.get("ATR", "10")["WIS"],
            "Text39": Passive_Calculation(data.get("skills_bonus", 0)["Perception"]),
            "Text40": Passive_Calculation(data.get("skills_bonus", 0)["Investigation"]),
            "Text41": data.get("ATR_Modifiers", "0")["WIS"],
            "Text42": data.get("ATR", "10")["CHA"],
            "Text43": data.get("ATR_Modifiers", "0")["CHA"],
            "Text49": data.get("speed", ""),
            "Text50": data.get("AC", ""),
            "Text51": "0",
            "Text52": Maximum_HP(HP = data.get("max_hp", ""), CON_Modifier = data.get("ATR_Modifiers", "0")["CON"], level = data.get("level", "")),
            "Text53": Maximum_HP(HP = data.get("max_hp", ""), CON_Modifier = data.get("ATR_Modifiers", "0")["CON"], level = data.get("level", "")),
            "Text54": data.get("level", ""),
            "Text55": data.get("hit_dice", ""),
            "Text56": data.get("level", ""),
            "Text58": data.get("proficiency_bonus", ""),
            "Text65": data.get("name", ""),
            "Text66": data.get("saving_throws_bonus", 0)["STR"],
            "Text67": data.get("skills_bonus", 0)["Athletics"],
            "Text69": data.get("saving_throws_bonus", 0)["DEX"],
            "Text70": data.get("skills_bonus", 0)["Acrobatics"],
            "Text71": data.get("skills_bonus", 0)["Sleight of Hand"],
            "Text72": data.get("skills_bonus", 0)["Stealth"],
            "Text73": "NA", #Reserved for Initiative
            "Text74": data.get("saving_throws_bonus", 0)["CON"],
            "Text75": data.get("saving_throws_bonus", 0)["INT"],
            "Text76": data.get("skills_bonus", 0)["Arcana"],
            "Text77": data.get("skills_bonus", 0)["History"],
            "Text78": data.get("skills_bonus", 0)["Investigation"],
            "Text79": data.get("skills_bonus", 0)["Nature"],
            "Text80": data.get("skills_bonus", 0)["Religion"],
            "Text81": data.get("saving_throws_bonus", 0)["WIS"],
            "Text82": data.get("skills_bonus", 0)["Animal Handling"],
            "Text83": data.get("skills_bonus", 0)["Insight"],
            "Text84": data.get("skills_bonus", 0)["Medicine"],
            "Text85": data.get("skills_bonus", 0)["Perception"],
            "Text86": data.get("skills_bonus", 0)["Survival"],
            "Text87": data.get("saving_throws_bonus", 0)["CHA"],
            "Text88": data.get("skills_bonus", 0)["Deception"],
            "Text89": data.get("skills_bonus", 0)["Intimidation"],
            "Text90": data.get("skills_bonus", 0)["Performance"],
            "Text91": data.get("skills_bonus", 0)["Persuasion"],
            "Text92": data.get("tools_names", False)[4],
            "Text93": Text_boxes_lang_and_other(data.get("languages", ""), data.get("other_proficiencies", ""), 4),
            "Text94": data.get("age", ""),
            "Text95": data.get("height", ""),
            "Text131": data.get("name", ""),
            "Text134": Spell_Save_DC(proficiency = data.get("proficiency_bonus", ""), skill_value = data.get("ATR_Modifiers", "0")[list(data["kam"].keys())[list(data["kam"].values()).index(True)]]),
            "Text135": data.get("tradition", ""),
            "Text136": list(data["kam"].keys())[list(data["kam"].values()).index(True)]
    }
    return fill_pdf(template_input, template_output, data_dict)

#FUNCTION - CREATE FILLED PDF
def fill_pdf(input_pdf_path, output_pdf_path, data_dict):
    ANNOT_KEY = "/Annots"
    ANNOT_FIELD_KEY = "/T"
    ANNOT_VAL_KEY = "/V"
    ANNOT_RECT_KEY = "/Rect"
    SUBTYPE_KEY = "/Subtype"
    WIDGET_SUBTYPE_KEY = "/Widget"
    template_pdf = pdfrw.PdfReader(input_pdf_path)
    for page in template_pdf.pages:
        annotations = page[ANNOT_KEY]
        for annotation in annotations:
            if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                if annotation[ANNOT_FIELD_KEY]:
                    key = annotation[ANNOT_FIELD_KEY][1:-1]
                    #print(key) #Debug of the form fields identified
                    if key in data_dict.keys():
                        if type(data_dict[key]) == bool:
                            if data_dict[key] == True:
                                annotation.update(pdfrw.PdfDict(V = pdfrw.PdfName("Yes"),
                                                                AS = pdfrw.PdfName("Yes")))
                        else:
                            annotation.update(pdfrw.PdfDict(V="{}".format(data_dict[key])))
                            annotation.update(pdfrw.PdfDict(AP=""))
    template_pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject("true")))
    pdfrw.PdfWriter().write(output_pdf_path, template_pdf)
