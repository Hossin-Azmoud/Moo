
from .constants import *
from enum import Enum
from colorama import Fore

class Colors:
	""" Enum for shell colors. """
	BLACK = Fore.BLACK
	BLUE = Fore.BLUE
	CYAN = Fore.CYAN
	GREEN = Fore.GREEN
	LIGHTBLACK_EX = Fore.LIGHTBLACK_EX
	LIGHTBLUE_EX = Fore.LIGHTBLUE_EX
	LIGHTCYAN_EX = Fore.LIGHTCYAN_EX
	LIGHTGREEN_EX = Fore.LIGHTGREEN_EX
	LIGHTMAGENTA_EX = Fore.LIGHTMAGENTA_EX
	LIGHTRED_EX = Fore.LIGHTRED_EX
	LIGHTWHITE_EX = Fore.LIGHTWHITE_EX
	LIGHTYELLOW_EX = Fore.LIGHTYELLOW_EX
	MAGENTA = Fore.MAGENTA
	RED = Fore.RED
	RESET = Fore.RESET
	WHITE = Fore.WHITE
	YELLOW = Fore.YELLOW



class Docs:
	""" ENUMS FOR DOCUMENTATION. """
	
	INTRO: str = DOC
	COMMANDS: str = availableCommands
	CD_DOC = cdDoc
	TOUCH_DOC = touchDoc
	SCRAP_DOC = scanDoc
	CAT_DOC = catDoc
	SCAN_DOC = scanDoc
	MKDIR_DOC = mkDoc
	MV_DOC = mvDoc
	RM_DOC = Rmdoc
	FONT_DOWNLOADER_DOC = FontdownloaderDoc
	ORG_DOC = ORGdoc

UIColors = Colors()
UIDocs = Docs()