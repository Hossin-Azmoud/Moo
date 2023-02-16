

"""
	[ ] TODO: Make some tools.. 
"""

from requests import get, post
from pytube import YouTube, Stream
from dataclasses import dataclass
from typing import Optional
import http.server
import socketserver
import socket
from time import time
from os import path
from subprocess import run
from json import dumps, loads
from datetime import datetime
from hashlib import sha256
from threading import Thread
@dataclass
class SecureShellClient:
	def __init__(self, host, interface, port, ClientName="client"):
		
		if port:
			self.PORT: int = port
		else:
			self.PORT: int = 4500

		self.HOST: str = host
		self.USERNAME: str = ClientName
		self.interface = interface
		self.SOCKET: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.HEADER: int = 128
		self.DISCONNECTING: str = "!DISCONNECT"
		self.FORMAT: str = "utf-8"
		self.logged_in = False

	def initialize(self):
		
		while not self.logged_in:
			clientName = self.interface.GetInput("User: ")
			Password   = self.interface.GetInput("password: ")
			
			if clientName and Password:
				
				msg = dumps({
					'user': clientName,
					'ConnectedAt': str(datetime.now()),
					'pwd': Password
				})

				self.send(msg)
				msg, n = self.receiveMessage()
				
				if n > 0:
					decodedMsg = loads(msg)
					if decodedMsg["code"] == 200:
						self.logged_in = True
					else:
						self.interface.LogInfo("Could not log in ? check if the password is legit!")

			else:
				self.interface.LogInfo("Empty value, recheck your username or password!")

	def connect(self):
		self.interface.LogInfo(f"Connecting to: {self.HOST}:{self.PORT}")
		self.SOCKET.connect((self.HOST, self.PORT))
		self.initialize()
		
		if self.logged_in:
			self.StartTransaction()

		self.EndTransaction()

	def EndTransaction(self):
		self.SOCKET.close()

	def StartTransaction(self):
		run = True
		print(f"[!] Secure Shell (client) started {socket.gethostname()}@{self.HOST}:{self.PORT}")
		
		while run:
			msg = self.interface.GetInput(f"{socket.gethostname()}@{self.HOST}: ")
			
			if (len(msg) > 0):
				if msg == "!DISCONNECT": 
					run = False
					self.send(dumps({
						"cmd": "!DISCONNECT"
					}))

				else:
					cmd = {
						"cmd": msg
					}

					self.send(dumps(cmd))
					msg, n = self.receiveMessage()
					
					if n > 0:
						Decoded = loads(msg)
						outPut = Decoded["out"]
						self.interface.LogInfo(outPut)
	
	def receiveMessage(self) -> tuple[str, int]:
	
		msg_len = self.SOCKET.recv(self.HEADER).decode(self.FORMAT) # recv the length of the message.
		print(msg_len)
		msg_len = int(msg_len)
		msg = self.SOCKET.recv(msg_len).decode(self.FORMAT) # recv the message.
		return (msg, msg_len)

	def send(self, msg: str):
		msg = msg.encode(self.FORMAT)
		self.SOCKET.send(str(len(msg)).encode(self.FORMAT))
		self.SOCKET.send(msg)
		

# client_ = Client()
# client_.connect()
# client_.close()

class SecureShell:
	"""
		Init message:
			{
				'U': clientName,
				'ConnectedAt': Date.Now(),
				'pwd': Password
			}
		genericMsg:
			{
				'cmd': command
			}

	"""


	def __init__(self, interface, pwd, port):
		self.interface = interface
		self.pwd = sha256(pwd.encode()).hexdigest()
		self.ClientName = "Default-Client"
		if port:
			self.PORT: int = port
		else:
			self.PORT = 4000

		self.HOST: str = socket.gethostbyname(socket.gethostname())
		self.SOCKET: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.HEADER: int = 128
		self.FORMAT: str = "utf-8"
		self.DISCONNECTING: str = "!DISCONNECT"
		self.clientLoggedIn = False


	def SetClient(self, NewC) -> None: 
		if NewC: self.ClientName = NewC

	def authenticate(self, conn) -> None:
	
		while not self.clientLoggedIn:	
			
			msg, n = self.receiveMessage(conn)
			
			if n > 0:
				decodedMsg = loads(msg)
				
				if sha256(decodedMsg["pwd"].encode()).hexdigest() == self.pwd:
					self.clientLoggedIn = True
					self.SetClient(decodedMsg["user"])
					self.send(dumps({
						"code": 200
					}), conn)

				else:
					self.send(dumps({
						"code": 400
					}), conn)

			else:
				self.send(dumps({
					"code": 400
				}), conn)

	def connect(self, conn, address):
		connected = True
		# Login!
		self.authenticate(conn)

		if self.clientLoggedIn:
			
			while connected:
				m, n = self.receiveMessage(conn)
				decoded = loads(m)
				if n > 0:
					if decoded["cmd"] == "!DISCONNECT":
						connected = False
					else:
						# TODO: Make a handler for the commands comming from the network.
						self.execute(decoded["cmd"], conn)

	def receiveMessage(self, conn):
		msg_len = conn.recv(self.HEADER).decode(self.FORMAT)
		msg_len = int(msg_len)
		data = conn.recv(msg_len).decode(self.FORMAT)
		return (
			data, msg_len
		)

	def execute(self, command, conn) -> None:
		try:
			out = run(command, shell=True, stdin=PIPE, stdout=PIPE).stdout
			conn.send(str(len(out)).encode(self.FORMAT))
			conn.send(out)
		except:
			conn.send('1'.encode(self.FORMAT))
			conn.send(" ".encode(self.FORMAT))

	def startSecureShell(self):
		self.bind_()
		self.SOCKET.listen(10)
		print(f"[!] Secure Shell (server) started {socket.gethostname()}@{self.HOST}:{self.PORT}")

		while True:
			conn, address = self.SOCKET.accept()
			Thread_ = Thread(target=self.connect, args=(conn, address))
			Thread_.start()

		self.endSecureShell()



	def send(self, msg: str, conn):
		msg = msg.encode(self.FORMAT)
		conn.send(str(len(msg)).encode(self.FORMAT))
		conn.send(msg)

	def bind_(self):
		self.SOCKET.bind((self.HOST, self.PORT))

	def endSecureShell(self):
		self.SOCKET.close()

@dataclass
class YTVideosWrapper:
	
	def __init__(self, YouTubeObject, interface):
		if interface:
			self.interface = interface

		self.YouTubeObject: YouTubes = YouTubeObject
		self.YouTubeObject.register_on_progress_callback(self.OnVideoProgress)
		
		# self.FMap = {
		# 	"BYTE": 1024 / (1024 ** 0)
		# 	"KB": 1024,
		# 	"KB": 1024,
		# }

		if self.YouTubeObject:
			self.Author:         str            = self.YouTubeObject.author
			self.Title:          str            = self.YouTubeObject.title
			self.Streams:        list[Stream]   = self.YouTubeObject.streams
			self.streamCount:     int           = len(self.Streams)
			self.publish_date:   str            = str(self.YouTubeObject.publish_date).split(" ")[0]
			self.Views:          int            = self.YouTubeObject.views
	
	def OnVideoProgress(self, stream: Stream, chunk: bytes, bytes_remaining: int):
		# Todo: Make progress bar.
		self.interface.LogInfo(f"{len(chunk)}/{stream.filesize} bytes was downloaded from", end="\r")

	def Download(self):
		continue_flag = self.Info()
		
		if continue_flag:
			index = self.PickIndex()
			
			if (index >= 0) and (index < self.streamCount):
				self.Load(index)

	def Load(self, i: int, 
		output_path: Optional[str] = None,
		filename: Optional[str] = None,
		filename_prefix: Optional[str] = None,
		skip_existing: bool = True,
		timeout: Optional[int] = None,
		max_retries: Optional[int] = 0
	) -> None:
		""" Loads a stream by index. """
		s = self.Streams[i]
		
		e = s.mime_type
		r = s.resolution
		print(f"Loading: {e} | {r} | {self.Title}")

		s.download()

		# self.YouTubeObject.get(e, r)

	def Info(self) -> bool:
		self.interface.LogInfo(f"""
[*] Author   :  {self.Author      }
[*] Title    :  {self.Title       }
[*] Pub-date :  {self.publish_date}
[*] views    :  {self.Views       }
""")

		continue_ = self.interface.GetInput("Want to continue: (Yes/No/y/n/Y/N): ")
		
		return (
			continue_.upper().strip() in ["YES", "Y", "YEAH"]
		)

	def LogStreamInfo(self, index: int) -> None:
		s = self.Streams[index]
		self.interface.LogInfo(f"{self.interface.UIColors.GREEN}#{index} {self.interface.UIColors.WHITE}{s.mime_type} | {s.resolution} | {(s.filesize // 1024)} KB")
	
	def PickIndex(self) -> int:
		
		for i in range(self.streamCount): self.LogStreamInfo(i)
		
		ok = False

		while not ok:
			index = self.interface.GetInput(f"Pick a resolution: (0 <= i < {self.streamCount}): ")
			try:
				index = int(index)
				if index < 0:
					self.interface.LogError(f"Index must be positive (i > 0).")
				elif index >= self.streamCount:
					self.interface.LogError(f"Index must be less than (i < {self.streamCount}).")
				else:
					ok = True
			except ValueError:
				self.interface.LogError("Index must be an integer.")

		return index
	
	def __dict__(self) -> dict:
		
		return {
			"Author": self.Author,
			"Streams": self.Streams,
			"Publish_date": self.publish_date,
			"Views": self.Views
		}


def GetNextByToken(List, current, Token) -> str | None:
	if List[current] == Token:
		if (current < len(List) - 1):
			return (List[current + 1] if len(List[current + 1]) > 0 else None)

class Server:
	def __init__(self, interface, port = 8080):
		self.Handler = http.server.SimpleHTTPRequestHandler
		self.host = socket.gethostbyname(socket.gethostname())
		self.port = port
		if interface:
			self.interface = interface
		self.directory = "."

	def gather_params(self, *args):
		
		if len(args) > 0:
			if (args[0].upper().strip() == "--HELP") or (args[0].upper().strip() == "-H"): 
				self.Help()
				return
			for i in range(len(args)):
				
				Next = GetNextByToken(args, i, '-p')
				
				if Next:
					try:
						self.port = int(Next)
					except ValueError:
						self.interface.LogError(f"-p must be an integer not { type(args[i + 1]) }")
					
					continue

				Next = GetNextByToken(args, i, '-d')

				if Next:
					d = str(Next)
					f = self.interface.SetCwd(d)
					
					if not f:
						self.interface.LogError(f"{d} does not seem to exist ? try another directory.")
						return

					self.interface.PMap["CD"](d)
					self.directory = d
		else: 
			self.Help()

	def LogServerInfo(self, info: list[str]): self.interface.LogInfo(f"{self.interface.UIColors.LIGHTYELLOW_EX}{info[0]}: {self.interface.UIColors.YELLOW}{info[1]} seconds")

	def serve(self):
		#TODO: Make a server from scratch in python.
		with socketserver.TCPServer((self.host, self.port), self.Handler) as HTTPHandler:
			
			self.interface.LogInfo()
			self.LogServerInfo([
				'Serving At',
				f'http://{self.host}:{self.port}'
			])
			self.LogServerInfo([
				'Serving: ',
				self.directory
			])
			

			if path.exists(path.join(self.directory, "index.html")):
				self.LogServerInfo([
					'HTML FILE DETECTED: ',
					'index.html'
				])

			try:
				started_at = time()
				HTTPHandler.serve_forever()

			except KeyboardInterrupt:
				self.interface.LogInfo(f"{self.interface.UIColors.GREEN}The Server was successfully closed.")
				UpT = time() - started_at
				
				if UpT > 60:
					self.LogServerInfo([
						"UpTime ", 
						f"{UpT // 60} Minutes"
					])

				else:
					self.LogServerInfo([
						"UpTime ", 
						f"{UpT} Seconds"
					])
	
			self.interface.LogInfo()


	def Help(self):
		self.interface.LogInfo("""

CommandLine Tool to serve a directory (DEFAULT IS CWD).
[USAGE] serve -p [OPTIONAL_PORT=8080] -d [OPTIONAL_DIR=`./`]

""")


class NetToolClass:
	
	def __init__(self, interface): 
		self.interface = interface
		
	def NetExec(self, *args, **kwargs):
		
		if len(args) > 0:
			subcommand = args[0]
			if subcommand.upper() == "GET":
				self.NetGet(*args[1:], **kwargs)
			elif subcommand.upper() == "POST":
				self.NetPost(*args[1:], **kwargs)

	def NetServer(self, *args):
		NewServer = Server(self.interface)
		NewServer.gather_params(*args)
		NewServer.serve()
	
	def SecureShellTool(self, *args):
		if len(args) > 0:
			if len(args) == 1:
				farg = args[0]
				if (farg.upper().strip() == "-H") and (farg.upper().strip() == "--HELP"):
					self.interface.LogInfo("""

Tool to open a secure connexion.
[USAGE] ss [client|server] [Port:int] [Host: str]

""")
					return
			else:

				Rule = args[0]
				Host = None
				Port = None

				
				if len(args) >= 2: Port = int(args[1])
				
				if Rule.upper().strip() == "CLIENT": 
					if len(args) < 3:
						self.interface.LogError("A Host was never specified!")
						return

					Host = args[2]

				if Rule.upper().strip() == "CLIENT": 
					shell = SecureShellClient(Host, self.interface, Port)
					shell.connect()

				if Rule.upper().strip() == "SERVER": 
					pwd = self.interface.GetInput("password: ")
					shell = SecureShell(self.interface, pwd, Port)
					shell.startSecureShell()
		else:
			self.interface.LogInfo("""

Tool to open a secure connexion.
[USAGE] ss [client|server] [Port:int] [Host: str]

""")

	def YoutubeDownloader(self, *args):
		"""
			>> age_restricted
			>> allow_oauth_cache
			>> author
			>> bypass_age_gate
			>> caption_tracks
			>> captions
			>> channel_id
			>> channel_url
			>> check_availability
			>> description
			>> embed_html
			>> embed_url
			>> fmt_streams
			>> initial_data
			>> js
			>> js_url
			>> keywords
			>> length
			>> metadata
			>> publish_date
			>> rating
			>> register_on_complete_callback
			>> register_on_progress_callback
			>> stream_monostate
			>> streaming_data
			>> streams
			>> thumbnail_url
			>> title
			>> use_oauth
			>> vid_info
			>> video_id
			>> views
			>> watch_html
			>> watch_url
		"""
		if len(args) > 0:
			# if "-f" in args:
			
			farg = args[0]
			if (farg.upper().strip() == "--HELP") or (farg.upper().strip() == "-H"):
				self.printYDHelp()
				return

			URL = farg
			if "https://" not in URL: URL = f"https://{URL}"

			LoadedObj                = YouTube(URL)
			
			Wrapper: YTVideosWrapper = YTVideosWrapper(
				LoadedObj, (self.interface)
			)

			Wrapper.Download()
		else:
			self.printYDHelp()
		
	def printYDHelp(self):
		self.interface.LogInfo("""
[DESC] Download youtube videos using url.
[USAGE] YD <URL> <Optional: OutPutDirectory>
""")

	def NetGet(self, *args, **kwargs):
		res = get(args[0], **kwargs)	
		
		data = {
			"code": res.status_code,
			**res.headers
		}

		if data["Content-Type"] == "text/html; charset=utf-8" or data["Content-Type"] == 'application/json; charset=utf-8':
			data["content"] = res.content.decode()
		else:
			data["content"] = data["Content-Type"]
	
		self.interface.LogDict(data)	

	def NetPost(self, *args, **kwargs):
		res = post(args[0], **kwargs)
		
		data = {
			"code": res.status_code,
			**res.headers
		}

		if data["Content-Type"] == "text/html; charset=utf-8" or data["Content-Type"] == 'application/json; charset=utf-8':
			data["content"] = res.content.decode()
		else:
			data["content"] = data["Content-Type"]

		self.interface.LogDict(data)


