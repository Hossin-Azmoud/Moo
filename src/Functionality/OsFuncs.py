
from os import (rmdir, chdir, mkdir, getcwd, path, scandir, removedirs,
remove, rename, stat_result, system, walk, getenv, name)
from subprocess import check_output, run, PIPE, Popen

class OS:

	def __init__(self, interface):
		self.interface = interface

	def cd(self, *arg):
		
		directoryName = getcwd()
		
		if len(arg) > 0: directoryName = arg[0]

		if directoryName == '--help':
			print(self.interface.UIDocs.CD_DOC)
			return

		if path.exists(directoryName):
			chdir(f"{directoryName}")
			self.interface.SetCwd(getcwd())
			return

		self.interface.LogError("it seems like it does not exist!")

	def ls(self, *arg):
		""" List The current or passed directory.. """
		
		print()
		
		directoryName = self.interface.cwd
		
		if len(arg) > 0:
			directoryName = arg[0]

		for dirObj in scandir(directoryName):
			if dirObj.is_file():
				self.interface.LogInfo(self.interface.SUC + ' [.]  ' + self.interface.SECANDARY + dirObj.name + " | " + str(dirObj.stat().st_size) + " byte")
			else:
				self.interface.LogInfo(self.interface.PRIMARY + ' [*]  ' + self.interface.SECANDARY + dirObj.name )

		print()

	def mv(self, *arg):
		""" Move a file or a directory from src to a certain dist """
		argc = len(arg)
		
		if argc >= 1:
			
			if argc == 1:
				if arg[0] == "--help" or arg[0] == "-h":
					print(self.interface.UIDocs.MV_DOC)
					return

			src, dist = arg[0], arg[1]
			if path.exists(src):
				
				if not path.exists(dist):
					self.mkdir(dist)
				try:
					move(src, dist)
				
				except:
					system(f"move {src} {dist}")
			else:
				self.interface.LogError("the file specified to be moved does not exist!!")

	def rm(self, *arg):
		""" remove file/files """
		if len(arg) >= 1:
			if len(arg) == 1:
				file = arg[0]
				if path.isfile(file):
					if path.exists(file):
						try:
							remove(file)
						except:
							system(f"del {file}")
						return

					self.interface.LogError(f"the file specified to be deleted does not exist {file}!!")
					return

				self.interface.LogError(f"the file specified to be deleted is not a file. {file}!!")
				return

			for file in arg:
				self.rm(file)

	def mkdir(self, *arg):
		""" make a new directory/multiple directories... """
		if len(arg) >= 1:
			if len(arg) == 1:
				directoryName = arg[0]
				mkdir(directoryName)
				return

			for i in arg: 
				self.mkdir(i)
			return

	def rmdir(self, *arg):
		""" remove the passed dir name. """
		if len(arg) >= 1:
			if len(arg) == 1:
				directoryName = arg[0]
				dircontent = [i for i in scandir(directoryName)]
				
				if len(dircontent) == 0:
					if path.exists(directoryName): rmdir(directoryName)
					else: self.interface.LogError(f"Directory NOT FOUND !\n {i}")
					return

				for i in dircontent:
					if i.is_file():
						self.rm(i.path)
					else:
						self.rmdir(i.path)
				
				if path.exists(directoryName): 
					rmdir(directoryName)
					return
			
				self.interface.LogError(f"Directory NOT FOUND !\n {i}")
				return

			for i in arg:
				if path.exists(i): self.rmdir(i)
				else:
					self.interface.LogError(f"Directory NOT FOUND !\n {i}")
			return
	
	def touch(self, *arg):
		""" create new file/files. """
		
		if len(arg) >= 1:
			if len(arg) == 1:
				path_ = arg[0]
				
				if path_ == '--help' or path_ == '-h':
					print(self.interface.UIDocs.TOUCH_DOC)
					return

				if path.exists(path_):
					self.interface.LogInfo(f"THIS FILE ALREADY EXISTS -> {path_}")
					answer = input("wanna procced( y, n ): ").strip().upper()
					if answer == "Y": 
						with open(path_, "w+") as f: return
					return
				else:
					with open(path_, "w+") as f: return

			elif len(arg) > 1:
				for i in arg:
					self.touch(i)
	
	def cat(self, *arg):
		""" display the content of a file. """
		if len(arg) >= 1:
			file = arg[0]
			if file.upper().strip() == "--HELP" or file.upper().strip() == "-H":
				self.interface.LogInfo(self.interface.UIDocs.CAT_DOC)
				return

			if path.isfile(file):
				with open(file) as fp:
					bf = fp.read()
					print()
					self.interface.LogInfo(bf)
					print()
				return

			self.interface.LogError(f"IT IS  NOT A VALID FILENAME: {file}")
			return

	def cp(self, *arg):
		
		if files == None:
			print(f"{CYAN} description:\n {WHITE} A command to copy files \n {CYAN} Usage:\n {WHITE}cp <filepath> <destinationpath>")
 
		elif len(files) < 2:
			print(f"{RED} something was not specified\n {YELLOW}check if you specified both the file and destination")
		elif len(files) > 2:
			for _ in files[:-1]:
				self.cp([_, files[-1]])
			print(f'{GREEN} copied {len(files)} files!!')
		else:
			try:
				copy(files[0], files[1])
				print(f'{GREEN} copied one file!!')
			except:
				system(f"copy {files[0]} {files[1]}")

	def ExecuteSysCommand(self, Program):
		""" If some command is not yet available in this class, it will reach out to syscommands"""
		"""  TODO: This command manager can not pipe the execution flow to another external shell! which is annoying ! """
		# Argc: int
		# Argv: list[str]
		# ProgramName: str
		
		command = [
			Program.ProgramName, *Program.Argv
		]

		if Program.Argc >= 1:
			# self.interface.LogInfo(f"running command {command}")

			p = run(
				command, 
				shell=True,
				stdout=PIPE,
				stdin=PIPE,
				encoding="utf-8"
			)

			# while pipe.returncode is None: 
			# 	pipe.poll()
			self.interface.LogInfo(p.stdin)
	def organize(self, *arg):
		
		if len(arg) > 0:
			path_ = arg[0]
			if path_.strip().upper() == "--HELP":
				print(self.interface.UIDocs.ORG_DOC)
				return
			
			if not path.exists(path_):
				print("the path does not exist.")
				return
			
			for i in scandir(path_):
				sp = str(i.name).split('.')
				if len(sp) > 1:
					if sp[len(sp) - 1] in ["rs", "go", "py", "ps", "bash", "yaml", "html", "c", "cpp", "c++", "r", "rb", "js", "css", "scss", "json", "tsx", "c#", "java", "rs"]: self.mv(i.path, "code")
					elif sp[len(sp) - 1] in ["mp3", "m4a", "wav"]: self.mv(i.path, "Audio")
					elif sp[len(sp) - 1] == "txt": self.mv(i.path, "text_files")
					elif sp[len(sp) - 1] in ["docx", "pdf", "ai", "fig", "psd", "xd"]: self.mv(i.path, "Docs")
					elif sp[len(sp) - 1] in ["mp4", "webm", "mkv"]: self.mv(i.path, "videos")
					elif sp[len(sp) - 1] in ["gif", "jpeg", "png", "svg"]: self.mv(i.path, "pictures")
					elif sp[len(sp) - 1] in ["exe", "", "msi"]: self.mv(i.path, "Programs")
					elif sp[len(sp) - 1] == "iso": self.mv(i.path, "ISO")
					else: self.mv(i.path, "other")
				else:
					if i.is_file(): 
						self.mv(i.path, "other")

			self.interface.LogSuccess("Completed!!")




