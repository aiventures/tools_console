""" Utility Module for Console """

# COLORING CONSOLE OUTPUT
# https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
COLOR_GREY="COLOR_GREY"
COLOR_RED="COLOR_RED"
COLOR_RED_BG="COLOR_RED_BG"
COLOR_GREEN="COLOR_GREEN"
COLOR_GREEN_BG="COLOR_GREEN_BG"
COLOR_YELLOW="COLOR_YELLOW"
COLOR_YELLOW_BG="COLOR_YELLOW_BG"
COLOR_BLUE="COLOR_BLUE"
COLOR_BLUE_BG="COLOR_BLUE_BG"
COLOR_PURPLE="COLOR_PURPLE"
COLOR_PURPLE_BG="COLOR_PURPLE_BG"
COLOR_LIGHTBLUE="COLOR_LIGHTBLUE"
COLOR_LIGHTBLUE_BG="COLOR_LIGHTBLUE_BG"
COLOR_WHITE="COLOR_WHITE"
COLOR_WHITE_BG="COLOR_WHITE_BG"
COLOR_DEFAULT=COLOR_WHITE
COLOR_DEFAULT_BG=COLOR_WHITE_BG
# colors white background
COLOR_GREY_WH="COLOR_GREY_WH"
COLOR_RED_WH="COLOR_RED_WH"
COLOR_GREEN_WH="COLOR_GREEN_WH"
COLOR_YELLOW_WH="COLOR_YELLOW_WH"
COLOR_BLUE_WH="COLOR_BLUE_WH"
COLOR_PURPLE_WH="COLOR_PURPLE_WH"
COLOR_LIGHTBLUE_WH="COLOR_LIGHTBLUE_WH"
COLOR_BLACK_WH="COLOR_BLACK_WH"
COLOR_DEFAULT_WH="COLOR_DEFAULT_WH"

COLORCODES={
    COLOR_GREY:"1;30;40",
    COLOR_RED:"1;31;40",
    COLOR_GREEN:"1;32;40",
    COLOR_YELLOW:"1;33;40",
    COLOR_BLUE:"1;34;40",
    COLOR_PURPLE:"1;35;40",
    COLOR_LIGHTBLUE:"1;36;40",
    COLOR_WHITE:"1;37;40",
    COLOR_RED_BG:"1;31;41",
    COLOR_GREEN_BG:"1;37;42",
    COLOR_YELLOW_BG:"1;37;43",
    COLOR_BLUE_BG:"1;37;44",
    COLOR_PURPLE_BG:"1;37;45",
    COLOR_LIGHTBLUE_BG:"1;37;46",
    COLOR_WHITE_BG:"1;37;47",
    COLOR_GREY_WH:"1;30;47",
    COLOR_RED_WH:"1;31;47",
    COLOR_GREEN_WH:"1;32;47",
    COLOR_YELLOW_WH:"1;33;47",
    COLOR_BLUE_WH:"1;34;47",
    COLOR_PURPLE_WH:"1;35;47",
    COLOR_LIGHTBLUE_WH:"1;36;47",
    COLOR_BLACK_WH:"1;30;47"
}
# derived color codes
COLORCODES[COLOR_DEFAULT]=COLORCODES[COLOR_WHITE]
COLORCODES[COLOR_DEFAULT_BG]=COLORCODES[COLOR_WHITE_BG]
COLORCODES[COLOR_DEFAULT_WH]=COLORCODES[COLOR_BLACK_WH]

COLOR_LIST=list(COLORCODES.keys())

def get_col_text(text,color):
    """ get color formatted string """
    return f'\x1b[{COLORCODES[color]}m{text}\x1b[0m'

def print_colors():
    print("--- print_colors() ---")
    for k,v in COLORCODES.items():
        print(f'{get_col_text(k+": ("+v+")",k):} ')

if __name__ == "__main__":
    pass
    # print_colors()