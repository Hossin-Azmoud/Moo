ENCODE, DECODE = 0, 1

def Encode(Func: callable):
	def f(s: str | bytes):
		assert isinstance(s, str) or isinstance(s, bytes), "This function can not encode %s Object" % type(s)
		if isinstance(s, str):
			s = s.encode()
		return Func(s).decode()
	
	return f

def Decode(Func: callable):
	def f(s: str | bytes):
		assert isinstance(s, str), "This function can not encode %s Object" % type(s)
		return Func(s).decode()
	
	return f

Functions = [
	Encode,
	Decode
]

def EncodingManager(Func: callable, Op: int) -> callable:
	assert (Op >= 0) and (Op <= len(Functions) - 1), 'This Operation is not NotImplemented or incorrect!, index [%s]' % Op
	return Functions[Op](Func)

# EncodingManager(func_, DECODE)
# 				^^^^^  ^^^^^^
# 				Encode, key 