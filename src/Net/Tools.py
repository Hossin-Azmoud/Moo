

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
	
	def __init__(self, interface): self.interface = interface

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


