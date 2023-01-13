""" 

THIS PACKAGE IS A UI ELEMENTS PACKAGE. HANDLES THE UI ASPECTS OF THE PROJECT.
[.] SHELL
[.] PRINTERS
[.] LOGGERS

"""
from .Enums import UIDocs, UIColors
from .program import constructNewProgram, Program
	
def GetShellInput(Current_directory: str) -> Program:
	""" Entry point for the shell UI """
	i = input(f'{ UIColors.GREEN }[MOO] { UIColors.YELLOW } { Current_directory } => { UIColors.WHITE }')
	return constructNewProgram(i.strip().split(' '))
