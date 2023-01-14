from dataclasses import dataclass

@dataclass
class Program:
	Argc: int
	Argv: list[str]
	ProgramName: str

	def ExecuteProgram(self, Code: callable) -> None: Code(*self.Argv)


def  constructNewProgram(input_: str) -> Program:

	NewArgs = parse( input_ )

	return Program(
		Argc=len(NewArgs),
		Argv=NewArgs[1:],
		ProgramName=NewArgs[0]
	)

D_QUOTE = "\""
S_QUOTE = "\'"
SPACE = " "

def parse(argv: str) -> list: 

	argv = argv.strip().strip(D_QUOTE).strip(S_QUOTE)

	return [
		i.strip().strip(S_QUOTE).strip(S_QUOTE) for i in argv.split(SPACE)
	]


def parse_t(argv: str) -> list:
	""" TEST LATER """
	newArgv, acc, start, end, specs = [], "", False, False, ["\"", "\'"]
	argv = argv.strip().strip("\"").strip("\'")

	for i in argv:

		if i in specs:
			if start: end = True
			else: start = True
			acc += i

		else:
			if i == " ":			
				if start and end:
					newArgv.append(acc)
					
					if start and end: start, end = False, False
					acc = ""
				
				elif (not start and not end):
					newArgv.append(acc)
					acc = ""
			else: 
				acc += i

	return newArgv
