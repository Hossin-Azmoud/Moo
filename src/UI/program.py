from dataclasses import dataclass

@dataclass
class Program:
	Argc: int
	Argv: list[str]
	ProgramName: str

	def ExecuteProgram(self, Code: callable) -> None: Code(*self.Argv)

	def Log(self):
		print("PROG_NAME: ", self.ProgramName)
		print("ARGS: ", self.Argv)
def  constructNewProgram(input_: list[str]):
	NewArgs = filterArgs(input_)

	return Program(
		Argc=len(NewArgs),
		Argv=NewArgs[1:],
		ProgramName=NewArgs[0]
	)
def filterArgs(argv: list[str]) -> list: return [i.replace('\'', '').replace('\"', '') for i in argv]
