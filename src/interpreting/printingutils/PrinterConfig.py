CONFIG = {
    'MAX_OBJECT_DEPTH': 2,
    'MAX_LIST_LENGTH': 7,
    'COLOR': True,
    'TAB_SIZE': 2,
    'LIMIT_SLOT_ANNOTATIONS': True,
    'LIMIT_CODE': True,
    'MAX_ANNOTATION_SIZE': 30,
    'USE_CODE_STRING': True,
    'USE_ALT_STRING' : False, 
    'REMOVE_ANNOTATIONS' : True
}

# For any color, '\033[38;2;r;g;bm' (replace r, g, b with rgb). Remember to end with ENDC.
# Test colors with echo -e "\033[38;2;255;140;60m Test Orange \033[0m" (works in git bash, windows cmd and posh)

COLORS = {
    "HEADER": "\033[95m",
    "YELLOW": "\033[38;2;255;230;120m",
    "BLUE": "\033[38;2;140;255;215m",
    "GREEN": "\033[38;2;0;255;0m",
    "RED": "\033[38;2;180;60;60m",
    "ORANGE": "\033[38;2;255;140;60m",
    "ENDC": "\033[0m",
}

OBJECT_COLORS = {
    'warn': COLORS['RED'],
    'annotation': COLORS['ORANGE'],
    'code': COLORS['BLUE'],
    'type': COLORS['YELLOW'],
    'slot_name': COLORS['HEADER']
}

def setup_config():
    try: 
        from PersonalConfig import CONFIG as P_CONFIG
        global CONFIG
        CONFIG.update(P_CONFIG)
    except:
        pass

    try:
        from PersonalConfig import COLORS as P_COLORS
        global OBJECT_COLORS 
        OBJECT_COLORS.update(P_COLORS)
        print("Config Loaded.")
    except:
        pass

def add_color(string, type):
    if not CONFIG['COLOR']:
        return string
    return f"{OBJECT_COLORS[type]}{string}{COLORS['ENDC']}"