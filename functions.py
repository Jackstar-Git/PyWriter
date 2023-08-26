import os

def clear():

    if os.name == "cmd" or "dos":
        clearer = "cls"
    else:
        clearer = "clear"

    os.system(clearer)