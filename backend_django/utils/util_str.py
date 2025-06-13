import re

def containe_str(s1:str, s2:str):
    if not s2 or s2 == '':
        return False
    return s1.find(s2)!= -1


def camel_string_to_underline(s:str):
    def  _convert_to_underline_field_name(match_str):
        return match_str.group(1)+'_'+match_str.group(2).lower()
    underline_string = re.sub(r'([a-z])([A-Z])', _convert_to_underline_field_name , s)
    return underline_string


def underline_to_camel_string(s:str):
    def  _convert_to_camel_field_name(match_str):
        if match_str.start() == 0:
            return match_str.string[match_str.start():match_str.end()]
        return match_str.group(1).upper()
    camel_string = re.sub(r'_([a-z])', _convert_to_camel_field_name, s)
    return camel_string


if __name__ == '__main__':
    s1 = 'abcDefGhij'
    s2 = 'DefGhij'
    s3 = 'adcD'
    print(f'{s1} => {camel_string_to_underline(s1)}')
    print(f'{s2} => {camel_string_to_underline(s2)}')
    print(f'{s3} => {camel_string_to_underline(s3)}')
    # s2 = 'abc_def_ghij'
    # print(f'{s2} => {underline_to_camel_string(s2)}')

