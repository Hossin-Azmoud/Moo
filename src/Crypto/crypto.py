from base64 import *

class CryptoCode:
	""" 
		TODO: Implement this class to support various types of encryption and encoding. 
		Examples {
			Base64
			Sha256
			SHA5
			base-n
		}
	
		in order to generalize this class we spread our implementation down to these general f
		
		Encode(in: str|bytes, fn: callable) -> bytes
		Decode(in: str|bytes, fn: callable) -> bytes
		Hash(in: str|bytes, fn: callable) -> bytes
		Encrypt(in: str|bytes, fn: callable) -> bytes
		Decrypt(in: str|bytes, fn: callable) -> bytes
	
	"""

	def __init__(self, interface) -> None:
		self.interface = interface

	def Encode(self, b: str|bytes, fn: Callable) -> bytes:
		pass

	def Decode(self, b: str|bytes, fn: Callable) -> bytes:
		pass

	def Hash(self, b: str|bytes, fn: Callable) -> bytes:
		pass

	def Encrypt(self, b: str|bytes, fn: Callable) -> bytes:
		pass

	def Decrypt(self, b: str|bytes, fn: Callable) -> bytes:
		pass

