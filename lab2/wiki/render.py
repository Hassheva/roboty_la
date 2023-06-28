def render(data_in, key_value):
    result = ''
    key = ''
    meet_key = False

    for symbol in data_in:
        if meet_key == False:
            if symbol != '{':
                result += symbol
            else:
                meet_key = True
        else:
            if symbol != '}':
                key += symbol
                #key is ready
            else:
                meet_key = False
                result += dict_of_code_symbol[key]
                key = ''


    print(result)
    print(key)

my_html = "{lol} <html> {var} </html>"

dict_of_code_symbol = {
    "var": 'Hello Yana',
    "lol": "by",
    "oosdjfosjdfo": [1, 2, 3, 4]
}
#path_out = '/Users/yana/wiki/wiki/'

data_out = render(my_html, dict_of_code_symbol)

