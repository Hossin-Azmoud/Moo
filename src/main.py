from mooshell import mooShell
from UI import UIColors
from pytube import YouTube





def main():
	shell = mooShell()
	shell.run()
	print(UIColors.WHITE)

def main3():
	r = True
	SPACE = ' '
	
	BQ = "\""
	SQ = "\'"
	startedQ = False
	endedQ = False

	while r:
		
		buff = []
		tbuff = ''
		i = input("Enter a command: ")
		i = i.strip()
		if i == 'q':
			r = False
			continue
		else:
			# parse command
			for j in range(len(i)):
				c =  i[j]
				
				if (c == BQ) or (c == SQ):
						if not startedQ:
							startedQ = True
						else:
							endedQ = True

						if startedQ and endedQ:
							if tbuff:
								buff.append(tbuff.replace(BQ, "").replace(SQ, ""))
							tbuff = ''
							startedQ = False
							endedQ = False
							
						if startedQ and not endedQ:
							tbuff += c

				elif (
					(c != SPACE) and (not startedQ)
				) or startedQ:
					tbuff += c
					if j == len(i) - 1:
						if tbuff:
							buff.append(tbuff)
						tbuff = ''
						
				else:
					if tbuff:
						buff.append(tbuff)
					tbuff = ''

		print(buff)
	
(
	lambda : main() if (__name__ == '__main__') else None
)()