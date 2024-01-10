from abc import ABC, abstractmethod


class A(ABC):
	
	def __init__(self, d) -> None:
		self.popos(d)
	
	@abstractmethod
	def popos(self, d):
		print(d)
	
class B(A):
	def __init__(self, d) -> None:
		super().__init__(d)
		self.c = "dd"
	def popos(self, d):
		print("sss" + str(d))
		
b = B("2")
