'''
    Emiliano Antonio Pineda Hernandez A01332517
    Diego Aguilar Gutierrez A01652642
    
'''
import re

def email(str):
    if re.search("^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$", str):
        return True
    else:
        return False

def phone_number(str):
    if re.search("(\+[0-9]{1-3}[\s]*\([0-9]{1,3}\)[\s]*)*[\s]*[0-9]{2,3}[\s]*[0-9]{4}[\s]*[0-9]{4}",str):
        return True
    else:
        return False

def hexadecimal(str):
    if re.search("^(0[xX](?=0*[1-9a-fA-F]0*)[0-9a-fA-F]{8}$)",str):
        return True
    else:
        return False