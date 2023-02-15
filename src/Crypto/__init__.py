from .Shell import Command, Shell
from .UtilFuncs import LoadConfig
from .Algorithms import *
# EncodingManager

class EncryptionTool:
	
	def __init__(self, interface):
		self.interface = interface

	

	def Wrapper(self, func: callable, All: list, *argv: list) -> None:
		if len(argv) == 0:
			return

		if len(argv) < 2:
			if (argv[0].upper().strip() == "--HELP") or argv[0].upper().strip() == "-H":
				self.interface.LogInfo()
				self.interface.LogInfo(self.Help())
				self.interface.LogInfo()
			if (argv[0].upper().strip() == "--ALL") or argv[0].upper().strip() == "-A":
				self.iterate(All)
			return
		
		self.interface.LogInfo()
		self.interface.LogInfo(func(*argv))
		self.interface.LogInfo()

	def iterate(self, Mp) -> None:
		self.interface.Log()

		for Algorithm in Mp:
			self.interface.Log(f"{self.interface.UIColors.GREEN}[!]{self.interface.UIColors.WHITE} {Algorithm}")

		self.interface.Log()

	def Encode(self, *argv: list):
		
		def f(*a: list):
			EncoderName = a[0].upper().strip()
			Text = a[1]
			# print(type(ENCODING))
			if EncoderName not in ENCODING:
				print()
				print(f"False algorithm name, {EncoderName}")
				print("you can only use from this list:")
				self.iterate(ENCODING)
				return


			func_ = ENCODING[EncoderName][ENCODE]
			encode = EncodingManager(func_, ENCODE)
			return encode(Text)

		self.Wrapper(f, ENCODING,*argv)
		
	
	def Decode(self, *argv: list):
		
		def f(*a: list):
			DecoderName = a[0].upper().strip()
			Text = a[1]
			if DecoderName not in ENCODING:
				print()
				print(f"False algorithm name, {DecoderName}")
				print("you can only use from this list:")
				self.iterate(ENCODING)
				return

			func_ = ENCODING[DecoderName][DECODE]
			decode = EncodingManager(func_, DECODE)
			return decode(Text)

		self.Wrapper(f, ENCODING,*argv)

	def hashVal(self, *argv: list):
		
		def f(*a: list):
			HasherName = a[0].upper().strip()
			Text = a[1]

			if HasherName not in HASHING:
				print()
				print(f"  False algorithm name, {DecoderName}")
				print("  you can only use from this list:")
				self.iterate(HASHING)
				return

			return Hasher(HASHING[HasherName.upper().strip()], Text)

		self.Wrapper(f, HASHING, *argv)

	def Help(self):
		return """

To encode/Decode:
	Encode/Decode <BASE64|...> <Text>
	Encode/Decode --help/-h for displaying help.
	Encode/Decode --All to see available algorithm
To hash:
	Hash <SHA256|...> <Text>
	Hash --help/-h for displaying help.
	Hash --All to see available algorithm
"""