

"""
	[ ] TODO: Make some tools.. 
"""

from requests import get, post

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


