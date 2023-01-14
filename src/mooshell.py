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
# USERPROFILE = getenv("USERPROFILE")

if name == "posix":
    HOME = "/mnt"
    ROOT = HOME + "/Moo"
else:
    HOME = getenv("HOMEPATH")
    ROOT = HOME + "\\Moo"

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

        self.PMap = {
            "CD": self.osClass.cd,
            "DIR": self.osClass.ls,
            "LS": self.osClass.ls,
            "ORGANIZE": self.osClass.organize,
            "MKDIR": self.osClass.mkdir,
            "RMDIR": self.osClass.rmdir,
            "RM": self.osClass.rm,
            "TOUCH": self.osClass.touch,
            "SCAN": NOT_EMP,
            "MV": self.osClass.mv,
            "CAT": self.osClass.cat,
            "NET": self.neTools.NetExec,
            "EXIT": self.quit
        }

        self.PRIMARY = UIColors.BLUE
        self.SECANDARY = UIColors.WHITE
        self.YELLOW = UIColors.YELLOW
        self.ERR = UIColors.RED
        self.SUC = UIColors.GREEN
        self.RUN = True

    def SetCwd(self, new: str) -> None:
        self.cwd = new

    def LogDict(self, data: dict) -> None:
        for i, k in enumerate(data):
            if k == "content":
                print(f"{UIColors.LIGHTYELLOW_EX}[{i}]-------------------------------- {self.SUC}{k} ----------------------------------------------")
                print(f'{UIColors.LIGHTYELLOW_EX}{data[k]}')
                
            else:
                print(f"{UIColors.LIGHTYELLOW_EX}[{i}] {self.SUC}{k}{self.SECANDARY}: {UIColors.LIGHTYELLOW_EX}{data[k]}")


    def LogError(self, *arg, **kwargs) -> None:
        print(self.ERR, *arg, **kwargs)
    def LogInfo(self, *arg, **kwargs) -> None:
        print(self.SECANDARY, *arg, **kwargs)
    def LogSuccess(self, *arg, **kwargs) -> None:
        print(self.SUC, *arg, **kwargs)

    def InitShell(self):
        if not path.exists(ROOT):
            mkdir(ROOT)
        self.setEnvAttributes()
        self.PMap["CD"](ROOT)
        self.SetCwd(ROOT)

    def run(self):
        """ THE ENTRY POINT FOR THE PROGRAM. """
        while self.RUN:
            try:
                self.program = GetShellInput(self.cwd)
                self.processProgram()
            
            except Exception as e:
                print(f"{self.ERR} some went bad!! :(", e) 

    def processProgram(self):
        PName = self.program.ProgramName.upper()
        if PName:
            if PName in self.PMap:
                code = self.PMap[PName]
                self.program.ExecuteProgram(code)
                return

            self.osClass.ExecuteSysCommand(self.program)

    def processArgs(self):
        
        if len(self.prompt.split(' ')) == 1:
            self.promp =  self.prompt.strip().upper()
           
            if self.promp == "LS" or self.promp == "DIR":
                self.ls()
            elif self.promp == "HELP":
                print(HELP)
            
            elif self.promp == "CD":
                print()
                print(self.cwd)
                print()

            elif self.promp == "FONTD":
                print(FontdownloaderDoc)
            elif self.promp == "QUIT" or self.promp == "EXIT":
                self.quit()
            elif self.promp == "ENCODER":
                self.args = None
                self.Cmd()
            elif self.promp == "scan":
                print(scanDoc)
            elif self.promp == "COMMANDS":
                print(availableCommands)
            elif self.promp == "SCRAP":
                print(ScrapDoc)
            elif self.promp == "DATABASE":
                print(doc)
            elif self.promp == "CP":
                self.cp()
            elif self.promp == "MV":
                print(mvDoc)
            elif self.promp == "ORG":
                self.ORGANIZE('.')

            elif self.promp == "COMPILER":
                self.args = ["compiler.py"]

                self.Cmd()
            else:
                self.args = None
                self.Cmd()

        elif len(self.prompt.split(' ')) > 1:
            self.prompt = self.prompt.split(' ')
            if self.prompt[0].strip().upper() == "CD":
                self.changedir(self.prompt[1])

            elif self.prompt[0].strip().upper() == "ORG":
                self.ORG(self.prompt[1])

            elif self.prompt[0].strip().upper() == "FONTD":
                self.donwloadFont()
            elif self.prompt[0].strip().upper() == "DATABASE":
                self.callDataBase(self.prompt)
            elif self.prompt[0].strip().upper() == "TOUCH":
                if len(self.prompt) > 2:
                    self.touch(self.prompt[1:])
                else:
                    self.touch(self.prompt[1])
            elif self.prompt[0].strip().upper() == "RM":
                if len(self.prompt) == 2:
                    if self.prompt[1] == '--help' or self.prompt[1] == '-h':
                        print(Rmdoc)
                    else:
                        self.rm(self.prompt[1])
                elif len(self.prompt) > 2:
                    self.rm(self.prompt[1:])
                elif len(self.prompt) > 2:
                        print(Rmdoc)

            elif self.prompt[0].strip().upper() == "MV":
                if len(self.prompt) == 3:
                    self.mv(self.prompt[1], self.prompt[2])
                elif len(self.prompt) > 3:
                    self.mv(self.prompt[1:-1], self.prompt[-1])
                elif len(self.prompt) == 2:
                    if self.prompt[1] == '--help' or self.prompt[1] == '-h':
                        print(mvDoc)
                    else:
                        print("seems like the distination has not been specified yet!!")
                else:
                    print(mvDoc)
            elif self.prompt[0].strip().upper() == "SCAN":
                if self.prompt[1] == "--help" or self.prompt[1] == '-h':
                    print(scanDoc)
                else:
                    self.scan(self.prompt[1])
            elif self.prompt[0].strip().upper() == "MKDIR":
                if self.prompt[1].strip().upper() == '--help' or self.prompt[1].strip().upper() == '-h':
                    print(mkDoc)
                else:
                    try:
                        mkdir(self.prompt[1])
                    except:
                        print('something went wrong!!')
            elif self.prompt[0].strip().upper() == "RMDIR":
                try:
                    rmdir(self.prompt[1])
                except:
                    print('something went wrong!!')
            elif self.prompt[0].strip().upper() == "ENCODER":
                self.setArgs()
                self.Cmd()
            elif self.prompt[0].strip().upper() == "COMPILER":
    
                self.args = [f"{self.prompt[0]}.py", *self.prompt[1:]]
                self.Cmd()
            elif self.prompt[0].strip().upper() == "CAT":
                if self.prompt[1] == '--help' or self.prompt[1] == '-h':
                    print(catDoc)
                else:
                    self.cat()

            elif self.prompt[0].strip().upper() == "LS" or self.prompt[0].strip().upper() == "DIR":
                self.cwd = self.prompt[1]
                self.ls()
            elif self.prompt[0].strip().upper() == "HELP":
                print()
                print(availableCommands)
                print()

            elif self.prompt[0].strip().upper() == "SCRAP":
                if len(self.prompt) == 2:
                    if self.prompt[1] == '--help' or self.prompt[1] == '-h':
                        print(ScrapDoc)
                    else:
                        self.scrap(self.prompt[1])
                elif len(self.prompt) >= 3:
                    self.scrap(self.prompt[1], self.prompt[2:])
            elif self.prompt[0].strip().upper() == "MIM":
                self.mim(self.prompt[1])
                print("quiting mim")
            
            elif self.prompt[0].strip().upper() == "CP":
                self.cp(self.prompt[1:])

            else:
                self.setArgs()
                self.Cmd()
    
    def setArgs(self): self.args = ' '.join(self.prompt[0:])
    
    
    
    def donwloadFont(self):
        fontName = self.prompt[1].strip()
        if fontName != '--help':
            urls = [
                f"https://fonts.google.com/download?family={fontName}",
                f"https://dl.dafont.com/dl/?f={fontName}"
            ]

            reqs = [get(urls[0]), get(urls[1])]
            APIS = ["Google Font", "Dafont"]
            
            for i, res in enumerate(reqs):
                
                if int(res.status_code) == 200:
                    if len(res.content) < 200:
                        print(f"{Fore.RED}[*] {Fore.MAGENTA}{fontName} was not fount in {APIS[i]}")
                    else:
                        print(f"""{Fore.YELLOW}
File name: {Fore.LIGHTYELLOW_EX}{fontName}.zip
{Fore.YELLOW}size:  {Fore.LIGHTYELLOW_EX}{len(res.content)} Bytes
{Fore.YELLOW}provider: {Fore.LIGHTYELLOW_EX}google fonts
{Fore.YELLOW}Download directory: {Fore.LIGHTYELLOW_EX}{getcwd()}
{Fore.YELLOW}Api: {Fore.LIGHTYELLOW_EX}{APIS[i]}
""")
                        with open(f"{fontName}.zip", "wb") as f:
                            print(f"{Fore.BLUE}downloading.. {fontName}")
                            f.write(res.content)
                        print(f"{Fore.GREEN}successfully donwloaded {fontName}")
                        break
                else:
                    print(f"{Fore.RED}[*] {Fore.MAGENTA}{fontName} was not fount in {APIS[i]}")
        else:
            print(FontdownloaderDoc)

    def callDataBase(self, argv: list, n=0):
        if len(argv) == n+2 or len(argv) == n+1:
            if argv[n+1] == '--help':
                print(doc)
            elif argv[n+1] == '--version':
                print('0.0.0!')
            else:
                if argv[n+1] == "--register":
                    dbname = input(f"{YELLOW}DbName: {WHITE}")
                    
                    for _ in ['\\', '|', '/', '-', '\\', '|', '/', '-', '\\', '|', '/', '-']:
                        print(f"{BLUE} initializing database! {_}{WHITE}", end="\r")
                        sleep(0.3)
                    print(f'{YELLOW}initialized!!{WHITE}')
                    db = database(dbName=dbname)
                    db.register()
                    db.cleanUp()
                
                elif argv[n+1] == "--login":
                    dbname = input(f"{YELLOW}DbName: {WHITE}")
                    dbpassword = input(f"{YELLOW}Password: {WHITE}")
                    print(f"{BLUE}Querying the database..{WHITE}")
                    db = database(dbName=dbname, password=dbpassword)
                    db.QueryDb()
                    db.cleanUp()
                elif argv[n+1] == "--getItems":
                    dbname = input(f"{YELLOW}DbName: {WHITE}")
                    dbpassword = input(f"{YELLOW}Password: {WHITE}")
                    print(f"{BLUE}Querying the database..{WHITE}")
                    db = database(dbName=dbname, password=dbpassword)
                    db.database(dbName=dbname, password=dbpassword)
                    db.getItems()
                    db.cleanUp()
                elif argv[n+1] == "--getHeaders":
                    dbname = input(f"{YELLOW}DbName: {WHITE}")
                    dbpassword = input(f"{YELLOW}Password: {WHITE}")
                    print(f"{BLUE}Querying the database..{WHITE}")
                    db = database(dbName=dbname, password=dbpassword)
                    db.database(dbName=dbname, password=dbpassword)
                    db.getHeaders()
                    db.cleanUp()
                elif argv[n+1] == "--update":
                    dbname = input(f"{YELLOW}DbName: {WHITE}")
                    dbpassword = input(f"{YELLOW}Password: {WHITE}")
                    db.database(dbName=dbname, password=dbpassword)
                    db.OPEN()
                    # logic to post!!
                    db.cleanUp()
                else:
                    print(doc)

        elif len(argv) > 2:
            if argv[1+n] == "--register":
                # cmd = arg0 --register dbName password  (make new db, with this name and passsword!)
                if len(argv) == 4+n:    
                    for _ in ['\\', '|', '/', '-', '\\', '|', '/', '-', '\\', '|', '/', '-']:
                        print(f"{BLUE} initializing database! {_}{WHITE}", end="\r")
                        sleep(0.3)
                    print(f'{YELLOW}initialized!!{WHITE}')
                    db = database(dbName=argv[2+n])
                    db.register(psswd=argv[3+n])
                    db.cleanUp()
                    exit(0)
                else:
                    print(f"{RED}either the database name of the password is messing!{WHITE}")

            elif argv[1+n] == "--login":
                if len(argv) == 4+n:
                    #cmd2 = arg0 --login dbName password (login using this name and password!)
                    print(f"{BLUE}Querying the database..{WHITE}")
                    sleep(2)
                    db = database(dbName=argv[2+n], password=argv[3+n])
                    db.QueryDb()
                    db.cleanUp()
                else:
                    print(f"{RED}either the database name of the password is messing!{WHITE}")
            elif argv[1+n] == "--update":
                if len(argv) >= 5+n:
                    db = database(dbName=argv[2+n], password=argv[3+n])
                    db.POST([argv[4+n], argv[5+n]])
                    db.cleanUp()
                else:
                    print(len(argv))
                    print(f"{RED}either the database name of the password is messing!{WHITE}")

        else:
            print(doc)

    def scan(self, ext):
        out = [i.name for i in scandir(self.cwd) if i.name.endswith(ext)]
        if len(out) > 0:
            for _ in out:
                print(f"{GREEN} ==> {_}")
        else:
            print("there is no files for the specified extention!")
        return out
    
    
    def scrap(self, url, args=[]):
        if not "http" in url.split(":"):
            url = "http://" + url
            
        if len(args) == 0:

            if get(url).status_code == 200:
                
                res = {
                    0: get(url).content,
                    1: get(url).headers,
                    2: get(url).encoding,
                    3: get(url).json,
                    4: get(url).text
                }

                print(f"{GREEN} status_code = 200 OK")
                scr = True
                reqprompt = f"""
{LIGHTCYAN_EX}
    specify what you want:
    => (0) content
    => (1) headers
    => (2) Encoding
    => (3) json
    => (4) text
    => (99) exit
"""
                while scr:
                    req = int(input(reqprompt))
                    print()
                    try:
                        if req in res.keys():
                            req2 = res[req]                    
                            print(req2.decode("latin1") if isinstance(req2, bytes) else req2)
                            print()
                            redcondition = str(input("want to redirect to a file (yes/no, y/n): "))
                            if redcondition.strip().upper() in ['YES', 'Y']:
                                redirect = str(input("file to redirect to:"))
                                dumptofile(redirect, req2)
                            else:
                                pass
                        else:
                            if req == 99:
                                scr = False
                            else:
                                print(f"{self.ERR}the number you specified is wrong! try again{RESET}")
                    except Exception as e:
                        print(f'{self.ERR}something went wrong!', e)
            else:
                print(f"{GREEN} status_code =  {get(url).status_code} :(")
        else:
            if len(args) > 3:
                if args[-1]:
                    if len(args) == 3:
                        if args[0].upper().strip() == 'HEADERS':
                            self.redirectOutput(getHeaders(url), args[1], args[2])
                        elif args[0].upper().strip() == 'CONTENT':
                            self.redirectOutput(getContent(url), args[1], args[2])
                        else:
                           self.redirectOutput(getContent(url), args[1], args[2])
                    else:
                        print(f"{MAGENTA} expected 4 arguments, got {len(args)} instead!")
                else:
                    print(f"{MAGENTA} expected 4 arguments, got {len(args)} instead!")
            else:
                if args[0].upper().strip() == 'HEADERS':
                    re0 = getHeaders(url)
                elif args[0].upper().strip() == 'CONTENT':
                    re0 = getContent(url)
                else:
                    re0 = getContent(url)
                print("-"*20)
                
                try: print(re0.decode("latin1") if isinstance(re0, bytes) else re0) 
                except: print(re0) # print(req2.decode() if isinstance(req2, Bytes) else req2)

                print("-"*20)
                redirect = input(f'[*] {YELLOW}file to redirect to ({MAGENTA}PRESS ENTER TO IGNORE): ')
                if redirect:
                    dumptofile(redirect, re0)


    def scandrive(self, name): pass

    def redirectOutput(self, content, method=None, fileName=None):
        if not method:
            method = ">"
        else:
            if method == ">":
                self.appendToFile(fileName, content)
            elif method == ">>":
                self.overwrite(fileName, content)
            else:
                print(f"{method} is not a valid switch, either use > to append or >> to overwrite") 

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
        
        for i in ['-','\\' , '|', '/']*2:
            print(f'{UIColors.LIGHTBLACK_EX} quiting {i}', end="\r")
            sleep(.3)

        self.RUN = False



