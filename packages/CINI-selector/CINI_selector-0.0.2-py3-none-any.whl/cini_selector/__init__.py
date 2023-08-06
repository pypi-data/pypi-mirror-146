# -*- coding: utf-8 -*-
"""
cini_selector: Module that work with the Spanish CINI code notification. Helping to verify if the code are valid or not. And help on each level The diffewrent options that the user have.
"""
__author__  = "Robert Rijnbeek"
__email__   = "robert270384@gmail.com"
__version__ = "0.0.2"

# ======== IMPORTS ===========

import json

from os.path import join


class CINI_Constructor():
    def __init__(self):
        self.cini_dict = {}
        self.ImportConfigurationFile()
        self.cini_1 = ""
        self.cini_2 = ""
        self.cini_3 = ""
        self.cini_4 = ""
        self.cini_5 = ""
        self.cini_6 = ""
        self.cini_7 = ""
        self.cinicode = ""
        self.selector_list = []

# ========= INIT FUNCTION ==============
    def ImportConfigurationFile(self): 
        try:
            file1 = open(join("src","cini_selector","CONFIG_FILE","CINI_Configuration_File.json"),"r")
            CINI_STRING = file1.read()
            CINI_DICT =json.loads(CINI_STRING)
            self.cini_dict = CINI_DICT
        except Exception as exc:
            assert print(f"ERROR: Importing configuration file:{exc}")

# =========== GETTERS ================
    def CINI_getter(self):
        return self.cinicode

    def Selector_CINI_getter(self):
        return self.selector_list
    
# ============SETTER =================
    def CINI_Builder(self):
        try:
            self.cinicode = "".join(['I',self.cini_1,self.cini_2,self.cini_3,self.cini_4,self.cini_5,self.cini_6,self.cini_7])
            return True
        except Exception as exc:
            print(f"ERROR: Unespected error building the CINI code:{exc}")
            return False

    def CINI_reset(self):
        try:
            self.cini_1 = ""
            self.cini_2 = ""
            self.cini_3 = ""
            self.cini_4 = ""
            self.cini_5 = ""
            self.cini_6 = ""
            self.cini_7 = ""
            self.cinicode = ""
            return True
        except Exception as exc:
            print(f"ERROR: Unespected error in method 'CINI_reset' :{exc}")
            return False
    
    def CINI_Setter_by_Level(self,VALUE,LEVEL):
        try:
            if LEVEL in range(1,8):
                value = str(VALUE)
                if LEVEL == 1:
                    self.cini_1 = value
                elif LEVEL == 2:
                    self.cini_2 = value
                elif LEVEL == 3:
                    self.cini_3 = value
                elif LEVEL == 4:
                    self.cini_4 = value
                elif LEVEL == 5:
                    self.cini_5 = value
                elif LEVEL == 6:
                    self.cini_6 = value
                elif LEVEL == 7:
                    self.cini_7 = value
                return True
            else:
                print("ERROR: defining the CINI code")
                return False
        except Exception as exc:
            print(f"ERROR: Unespected error:{exc}")
            return False

    def Define_Selector(self,SELECTOR_LIST):
        try:
            if len(SELECTOR_LIST)>7: 
                print(f"ERROR: The argument '{SELECTOR_LIST}' has more than 7 arguments")
                return False
            selectors = SELECTOR_LIST
            cini_array = self.cini_dict["cini"]
            level = 0
            while len(selectors) >0 :
                level += 1 
                filter_code = selectors[0]
                find_value = False
                for ind,row in enumerate(cini_array):
                    cod = row["cod"]
                    if str(cod) == str(filter_code):
                        if level == 7:
                            self.CINI_Setter_by_Level(filter_code,level)
                            cini_array = []
                            selectors.pop(0)
                            find_value = True
                            break
                        else:
                            cini_array = cini_array[ind]["next"]
                            selectors.pop(0)
                            self.CINI_Setter_by_Level(filter_code,level)
                            find_value = True
                            break
                if find_value is False:
                    print(f"ERROR: code value '{filter_code}' at level '{level}' does not exist")
                    return False
            
            selector_list =[]
            for row in cini_array:
                cod = row["cod"]
                des = row["des"]
                selector_list.append([cod,des])
            
            self.selector_list = selector_list
            return True
        except Exception as exc:
            print(f"ERROR: Unespected error in 'Define_Selector':{exc}")
            return False

# ================= VERIFICATION ===================
    
    def Is_CINI_Complete(self):
        try:
            if "" in (self.cini_1,self.cini_2,self.cini_3,self.cini_4,self.cini_5,self.cini_6,self.cini_7):
                return False
            else:
                return True
        except Exception as exc:
            print(f"ERROR: Unespected error in the method: 'Is_CINI_Complete': {exc}")
            return False

if __name__ == "__main__":

    pass