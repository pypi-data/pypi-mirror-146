'''
	Author  : RoodRepo
	Git     : https://github.com/roodrepo/unit_test_advanced
	Contact : roodrepo@gmail.com
	
	Title       : Unit Test Advanced
	Version     : 0.1.x
	Description : Execute unit tests using the production code - Program multiple scenarios and override custom data if needed
'''

from importlib import import_module as sys_import_module
import random

class UnitTest:
	
	_memory                  : dict = {}
	_execution_plans         : list = []
	_loaded_plans            : list = []
	
	_verbose                 : bool
	_log                     : bool
	_is_enabled              : bool
	_parent_execution_plan   : str
	_children_execution_plan : str
	_script_counter          : dict  = {}
	_pooltest                        = None
	
	_count_limit_identify_infinite_loop : int
	
	def __init__(self, is_enabled = False, parent_execution_plan = 'all', children_execution_plan = 'all', count_limit_identify_infinite_loop = 2, verbose = False):
		'''
			is_enabled: If true, UnitTesting is activated, otherwise will execute the default function in all cases
			
			parent_execution_plan / children_execution_plan
				"all"       executes all paths possible
				"random"    executes ONE random path based on all the potential possibilities
				"main"      executes the first path of all tests
			
			count_limit_identify_infinite_loop: Count to prevent looping multiple time on the same class. If set to 2, one class in an execution plan cannot be executed more than twice
			
			verbose: display progress of the execution
		'''
		
		self.updateSettings(**{
			'verbose'                               : verbose,
			'is_enabled'                            : is_enabled,
			'parent_execution_plan'                 : parent_execution_plan,
			'children_execution_plan'               : children_execution_plan,
			'count_limit_identify_infinite_loop'    : count_limit_identify_infinite_loop,
		})
		
		
		
	
	def updateSettings(self, **kwargs):
		'''
			Securing the settings to update to a define list. Multiple settings can be updated at once
		'''
		
		updatable_settings = ['verbose', 'is_enabled', 'parent_execution_plan', 'children_execution_plan', 'count_limit_identify_infinite_loop']
		for kwarg, value in kwargs.items():
			if kwarg in updatable_settings:
				setattr(self, f'_{kwarg}', value)
	
	def log(self, *args, level = 0):
		'''
			Print out texts when unit test mode is enabled
		'''
		
		if self._log == True:
			args = list(args)
			
			if level == 1:
				args.insert(0, f'{"":4}')
			elif level == 2:
				args.insert(0, f'{"":8}')
			elif level == 3:
				args.insert(0, f'{"":12}')
			elif level == 4:
				args.insert(0, f'{"":16}')
				
			print(*args)
			
	def _print(self, *args, level = 0):
		'''
			Print out texts when verbose mode is enabled
		'''
		
		if self._verbose == True:
			args = list(args)
			
			if level == 1:
				args.insert(0, f'{"":4}')
			elif level == 2:
				args.insert(0, f'{"":8}')
			elif level == 3:
				args.insert(0, f'{"":12}')
			elif level == 4:
				args.insert(0, f'{"":16}')
				
			print(*args)
	
	
	
	def _importModule(self, module):
		'''
			Dynamically import modules if a string is passed
		'''
		if isinstance(module, str):
			_tmp = module.split('.')
			module_path = '.'.join(_tmp[:-1])
			class_name  = _tmp[-1]
			
			# Importing the object dynamically
			module = sys_import_module(module_path)
			return getattr(module, class_name)
		else:
			return module
	
	
	
	def _resetCounter(self):
		'''
			For each execution plan, resetting both the counter and memory
		'''
		self._script_counter = {}
		
	def _resetMemory(self):
		self._memory         = {}
	
	
	
	def override(self, id, function, *args, **kwargs):
		'''
			id: The function to execute within the class if that function exists
			function: The actual function to execute in case the function-id does not exists
			*args and **kwargs are the argument to pass to both the fake function and real function
		'''
		
		if self._is_enabled == True and hasattr(self._pooltest, id):
			return getattr(self._pooltest, id)(*args, **kwargs)
		else:
			return function(*args, **kwargs)
	
	
	
	def returnValue(self, value):
		'''
			Simply return the passed value. Useful when just a value needs to be faked out during unit test
		'''
		
		return value
	
	
	def _checkInfiniteLoop(self, plans_list):
		'''
			Checks how many time a class is called and raise an error when the limit "count_limit_identify_infinite_loop" is reached
		'''
		
		for module_list in plans_list:
			module_name_list = [module.__name__ for module in module_list]
			module_over_the_limit = {module_name: True if module_name_list.count(module_name) >= self._count_limit_identify_infinite_loop else False for module_name in module_name_list}
			for module_name, is_limit_reached in module_over_the_limit.items():
				if is_limit_reached == True:
					raise Exception(f'Possible infinite loop identified on {module_name}')
	
	
	
	def _run(self, module):
		'''
			Executing all the main functions of a class
			pooltest        : Storing the current class executed for the unit test. Passing memory to access previous stored data
			trigger_params  : Parameters (dict) to pass from the class to the triggered function
			trigger         : Action (function) to trigger for the unit test
			finalCheck     : Final check after the action is complete
		'''
		
		if self._is_enabled == True:
			module = self._importModule(module)
			
			init_params = {}
			if hasattr(module, 'memory'):
				init_params = {'memory': self._memory}

			self._log = True
			if hasattr(module, 'log') and module.log == False:
				self._log = False
				
				
			if hasattr(module, 'init_params'):
				init_params = {**init_params, **module.init_params}
			
			self._pooltest = module(**init_params)
			
			
			params = {}
			if hasattr(self._pooltest, 'trigger_params'):
				params = self._pooltest.trigger_params
			
			if hasattr(module, 'trigger'):
				
				module.trigger(**params, UT= self)
			
			if hasattr(self._pooltest, 'finalCheck'):
				self._pooltest.finalCheck()
				
			# Updating the memory attribute
			if hasattr(self._pooltest, 'memory'):
				self._memory = self._pooltest.memory
	
	
	
	def _runExecutionPlan(self, execution_plan):
		'''
			Running an execution plan
		'''
		
		if self._is_enabled == True:
			self._resetMemory()
			self._print('Running execution plan: ', execution_plan)
			for module in execution_plan:
				self._run(module)
	
	
	
	
	def preparePlans(self, list_unit_tests = []):
		'''
			Preparing the plans according to the settings and list passed.
			This function also prepare the execution tree for parents and children possibilities
		'''
		
		if self._is_enabled == True:
			for unit_test in list_unit_tests:
				self._resetCounter()
				if isinstance(unit_test, list):
					self._execution_plans.append(unit_test)
				else:
					self._createExecutionPlans(unit_test)
					
			self._preventExecutionPlansDuplicates()
	
	
	
	def getExecutionPlans(self):
		'''
			Return all the current execution plans
		'''
		
		return self._execution_plans
	
	
	
	def resetExecutionPlans(self):
		'''
			Resetting the execution plan list
		'''
		
		self._execution_plans    = []
		self._loaded_plans       = []
	
	
	
	def execute(self, list_unit_tests = None):
		'''
			Entry point to start the unit tests
			Either prepare a list and execute or pass the list as argument to perform both actions at once
		'''
		
		if self._is_enabled == True:
			
			if list_unit_tests != None:
				self.preparePlans(list_unit_tests)
				
			for ep in self._execution_plans:
				self._runExecutionPlan(ep)
				
			self.resetExecutionPlans()
			
			
			
	def _preventExecutionPlansDuplicates(self):
		'''
			Removing duplicated plans
		'''
		
		final_plans = []
		for plan in self._execution_plans:
			_modules_in_plan = []
			for _module in plan:
				_modules_in_plan.append(_module.__name__)
				
			if _modules_in_plan not in self._loaded_plans:
				self._loaded_plans.append(_modules_in_plan)
				final_plans.append(plan)
				
		self._execution_plans = final_plans
		
	
	def _checkRelationship(self, obj, attr, check_obj):
		'''
			If verbose mode is enable, print out if the reversed relation is not found
		'''
		
		if self._verbose == True:
			if (hasattr(obj, attr) == False):
				self._print(f'{obj} do not have {check_obj} in {attr}', level= 1)
			else:
				_imported_modules = []
				for _module in getattr(obj, attr):
					_imported_modules.append(self._importModule(_module))
					
				if check_obj not in _imported_modules:
					self._print(f'{obj} do not have {check_obj} in {attr}', level= 1)

	def _getParentPlans(self, plans):
		'''
			From a plan, create the parent tree
		'''
		
		new_plans = []
		dependencies_found = False
		for plan in plans:
			if hasattr(plan[0], 'dependencies'):
				dependencies_found = True
				if self._parent_execution_plan == 'all':
					for dependency in plan[0].dependencies:
						dependency = self._importModule(dependency)
						new_plans.append([dependency] + plan.copy())
						
						# Relationship verification
						self._checkRelationship(dependency, 'children', plan[-1])
						
				else:
					idx = 0
					if self._parent_execution_plan == 'random':
						idx = random.randint(0, len(plan[0].dependencies) -1)
						
					dependency = self._importModule(plan[0].dependencies[idx])
					new_plans.append([dependency] + plan.copy())
					
					# Relationship verification
					self._checkRelationship(dependency, 'children', plan[-1])
					
			else:
				new_plans.append(plan.copy())
				
		self._checkInfiniteLoop(new_plans)
		
		if dependencies_found == True:
			plans = self._getParentPlans(new_plans)
			
		return plans
	
	
	
	def _getChildrenPlans(self, plans):
		'''
			From a plan, create the children tree
		'''
		
		new_plans = []
		dependencies_found = False
		# print(plans)
		for plan in plans:
			
			if hasattr(plan[-1], 'children'):
				dependencies_found = True
				if self._children_execution_plan == 'all':
					for child in plan[-1].children:
						child = self._importModule(child)
						new_plans.append(plan.copy() + [child])
						
						# Relationship verification
						self._checkRelationship(child, 'dependencies', plan[-1])
						
						
				else:
					idx = 0
					if self._children_execution_plan == 'random':
						idx = random.randint(0, len(plan[-1].children) -1)
						
					child = self._importModule(plan[-1].children[idx])
					new_plans.append(plan.copy() + [child])
					
					# Relationship verification
					self._checkRelationship(child, 'dependencies', plan[-1])
			else:
				new_plans.append(plan.copy())
			
		self._checkInfiniteLoop(new_plans)
		
		if dependencies_found == True:
			plans = self._getChildrenPlans(new_plans)
			
		return plans
	
	
	
	def _createExecutionPlans(self, module):
		'''
			Manage and put together the parent tree and children tree
		'''
		
		current_plans = [[module]]
		
		self._print('Checking relationships...')
		current_plans = self._getParentPlans(current_plans)
		current_plans = self._getChildrenPlans(current_plans)
		
		self._execution_plans += current_plans
	