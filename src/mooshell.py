from sys import (platform, path, exit)
from os import (rmdir, chdir, mkdir, getcwd, path, scandir, removedirs,
remove, rename, stat_result, system, walk, getenv, name)
from shutil import move, copy
from UI import UIColors, UIDocs, GetShellInput
from Net import NetToolClass
from pprint import pprint
from datetime import date
from time import sleep
from typing import Union
from Variables import *
from requests import get
from utility import dumptofile, getContent, getHeaders
from database import *
from Functionality import OS
from Tools import Tools
from Crypto import EncryptionTool


HOME = getenv("HOMEPATH")
ROOT = HOME + "\\Moo"
if name == "posix":
    HOME = "/mnt"
    ROOT = HOME + "/Moo"

# INTRO: str = DOC
# COMMANDS: str = availableCommands
# CD_DOC = cdDoc
# TOUCH_DOC = touchDoc
# SCRAP_DOC = scanDoc
# CAT_DOC = catDoc
# SCAN_DOC = scanDoc
# MKDIR_DOC = mkDoc
# MV_DOC = mvDoc
# RM_DOC = Rmdoc
# FONT_DOWNLOADER_DOC = FontdownloaderDoc
# ORG_DOC = ORGdoc

NOT_EMP = (
    lambda : print("THIS COMMAND is {!NOT_EMPLEMENTED} BUT M STILL WORKING ON IT!")
)


class mooShell:

    def __init__(self):
        self.InitShell()
        print(self.UIDocs.INTRO)

    def setEnvAttributes(self):
        
        self.UIDocs = UIDocs
        self.osClass = OS(self)
        self.neTools = NetToolClass(self)
        self.Tools = Tools(self)
        self.Encryptor = EncryptionTool(self)
        
        
        # The commands that the shell supports.
        self.PMap = {
            "CD": self.osClass.cd,
            "DIR": self.osClass.ls,
            "LS": self.osClass.ls,
            "ORGANIZE": self.osClass.organize,
            "MKDIR": self.osClass.mkdir,
            "RMDIR": self.osClass.rmdir,
            "RM": self.osClass.rm,
            "TOUCH": self.osClass.touch,
            "SCAN": self.osClass.scan,
            "CP": self.osClass.cp,
            "MV": self.osClass.mv,
            "CAT": self.osClass.cat,
            "NET": self.neTools.NetExec,
            "YD": self.neTools.YoutubeDownloader,
            "PACKAGEI": self.Tools.package_info,
            "FONTS": self.Tools.DownloadFonts,
            "SERVE": self.neTools.NetServer,
            "AUDIONIFY": NOT_EMP,
            "SS": self.neTools.SecureShellTool,
            "HASH": self.Encryptor.hashVal,
            "DECODE": self.Encryptor.Decode,
            "ENCODE": self.Encryptor.Encode,
            "EXIT": self.quit
        }

        self.UIColors = UIColors
        self.PRIMARY = UIColors.BLUE
        self.SECANDARY = UIColors.WHITE
        self.YELLOW = UIColors.YELLOW
        self.ERR = UIColors.RED
        self.SUC = UIColors.GREEN
        self.RUN = True

    def SetCwd(self, new: str) -> None: 
        if path.exists(new): 
            self.cwd = new
            return True
        return False

    def LogDict(self, data: dict) -> None:
        for i, k in enumerate(data):
            if k == "content":
                print(f"{UIColors.LIGHTYELLOW_EX}[{i}]-------------------------------- {self.SUC}{k} ----------------------------------------------")
                print(f'{UIColors.LIGHTYELLOW_EX}{data[k]}')            
            else:
                print(f"{UIColors.LIGHTYELLOW_EX}[{i}] {self.SUC}{k}{self.SECANDARY}: {UIColors.LIGHTYELLOW_EX}{data[k]}")
    def Log(self, *arg, **kwargs) -> None: print(*arg, **kwargs)
    def LogError(self, *arg, **kwargs) -> None: self.Log(self.ERR, *arg, **kwargs)
    def LogInfo(self, *arg, **kwargs) -> None: self.Log(self.SECANDARY, *arg, **kwargs)
    def LogSuccess(self, *arg, **kwargs) -> None: self.Log(self.SUC, *arg, **kwargs)

    def InitShell(self):
        if not path.exists(ROOT):
            mkdir(ROOT)
        self.setEnvAttributes()
        self.PMap["CD"](ROOT)
        self.SetCwd(ROOT)

    def GetInput(self, prompt):
        buff = input(f"{self.UIColors.LIGHTYELLOW_EX}{prompt}{self.UIColors.LIGHTYELLOW_EX}")
        return buff

    def run(self):
        """ THE ENTRY POINT FOR THE PROGRAM. """
        while self.RUN:
            self.program = GetShellInput(self.cwd)
            self.processProgram()
    
    def processProgram(self, External = False, ExtProgram = None):
        """ A func to parse and process the program name and args. """
        if not ExtProgram: 
            PName = self.program.ProgramName.upper().strip()
            
            if PName:
                if PName in self.PMap:
                    code = self.PMap[PName]
                    self.program.ExecuteProgram(code)
                    return

                self.osClass.ExecuteSysCommand(self.program)
            return
            
    def cmd(self, cmd):
        return ("0")

    def appendToFile(self, fileName, content):
        with open(fileName, "a+") as f:
            if isinstance(content, bytes):
                f.write(content.decode())
            else:
                f.write(str(content))

    def overwrite(self, fileName, content):
        with open(fileName, "w+") as f:
            if isinstance(content, bytes):
                f.write(content.decode())
            else:
                f.write(str(content))

    def quit(self):
        
        for i in ['-','\\' , '|', '/'] * 2:
            print(f'{UIColors.LIGHTBLACK_EX} quiting {i}', end="\r")
            sleep(.3)

        self.RUN = False