class UnitTestAction(object):
	
	# Attribute to pass data from one class to another in the execution plan
	_memory         : dict  = {}
	dependencies    : list
	children        : list
	
	def __init__(self, memory, **kwargs):
		self.memory = memory
	
	@property
	def memory(self):
		return self._memory
	
	@memory.setter
	def memory(self, memory):
		self._memory = {
			**self._memory,
			**memory,
		}
