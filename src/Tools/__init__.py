from time import sleep
from sys import stdout
from os import getcwd
from requests import get

FONT_WEB = [
	f"https://fonts.google.com/download?family=",
	f"https://dl.dafont.com/dl/?f="
]

APIS = ["Google Font", "Dafont"]
SUCCESS = 200

class Tools:
	
	def __init__(self, interface):
		# DEPENDENCY. 
		self.interface = interface

	def DownloadFonts(self, *argv) -> None:
		if len(argv) >= 1:
			
			fontName = argv[0]
			
			
			if fontName != '--help':
				response = {}
				index = -1
				for i, u in enumerate(FONT_WEB):
					response = get(u + fontName)
					
					if response.status_code == SUCCESS and len(response.content) > 200:
						index += (i + 1)
						break

				if index >= 0:

					self.interface.Log(f"""
{self.interface.UIColors.YELLOW}
File name: {self.interface.UIColors.LIGHTYELLOW_EX}{fontName}.zip
{self.interface.UIColors.YELLOW}size:  {self.interface.UIColors.LIGHTYELLOW_EX}{float(len(response.content)) / float(1024)} KB | {len(response.content)} B
{self.interface.UIColors.YELLOW}provider: {self.interface.UIColors.LIGHTYELLOW_EX}google fonts
{self.interface.UIColors.YELLOW}Download directory: {self.interface.UIColors.LIGHTYELLOW_EX}{getcwd()}
{self.interface.UIColors.YELLOW}Api: {self.interface.UIColors.LIGHTYELLOW_EX}{APIS[index]}
					""")

					Ans = input("Want to continue, (y, n): ")
					if Ans.strip().upper() == "Y":
					
						with open(f"{fontName}.zip", "wb") as f:
							f.write(response.content)
							self.interface.Log(f"{self.interface.UIColors.GREEN}successfully donwloaded {fontName}")
					return

				self.interface.LogInfo("")
				self.interface.LogInfo(f"The font you are looking for was not found")
				self.interface.LogInfo(f"name: {fontName}")
				self.interface.LogInfo("")

				return

		self.interface.Log(self.interface.UIDocs.FONT_DOWNLOADER_DOC)

	def package_info(self, *argv) -> None:
	
		if len(argv) == 0:
			return
		
		package_name = argv[0]
		package = __import__(package_name)

		INFO = f"STARTING REPORT FOR {package_name}\n"

		for x in INFO:
			stdout.write(x)
			sleep(1)

		members = dir(package)
		run = True

		while run:

			for i, mod_object_ in enumerate(members):	
				if not '__' in mod_object_:
					self.interface.Log(f"({i}) => {mod_object_}")

			self.interface.Log(f"(-1) => exit this shell.")
			self.interface.Log("(-200) => save information in a file.")

			input_ = input("Choose function/Class (index is above): ")
			if input_:
				input_ = int(input_)
				if input_ == -1:
					run = False
				else:
					if input_ <= len(members) - 1:
						help(members[input_])

					else:
						self.interface.Log("wrong index !")