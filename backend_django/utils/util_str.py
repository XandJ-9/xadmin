
def containe_str(s1:str, s2:str):
    if not s2 or s2 == '':
        return False
    return s1.find(s2)!= -1