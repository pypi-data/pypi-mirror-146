from unit_test_advanced.UnitTestAction import UnitTestAction
import os, sys, json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.append(BASE_DIR)
from step1 import run as step1_run
from step2 import run as step2_run
from step3 import run as step3_run

FILE_NAME = 'myfile.txt'

class resetWorkspace(UnitTestAction):
	
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		
		if os.path.exists(f'{BASE_DIR}/{FILE_NAME}') == True:
			os.remove(f'{BASE_DIR}/{FILE_NAME}')
		
		
class step1_checkFileExist_success:
	
	# Function to execute to run the action to test
	trigger = step1_run

	def finalCheck(self):
		if os.path.exists(f'{BASE_DIR}/{FILE_NAME}') == False:
			raise BaseException(f'The file {FILE_NAME} is missing')

class step1_checkFileExistUseMemory_success(UnitTestAction):
	
	# Function to execute to run the action to test
	trigger = step1_run
	
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		
		self.memory = {
			'print_memory_message'  : True,
			'value_in_memory'       : '######### This value is passed along all the classes of a plan and can be modified at any time'
		}
		
	def finalCheck(self):
		if os.path.exists(f'{BASE_DIR}/{FILE_NAME}') == False:
			raise BaseException(f'The file {FILE_NAME} is missing')

class step2_NoOverride:
	
	trigger = step2_run
	
	def finalCheck(self):
		f = open(f'{BASE_DIR}/{FILE_NAME}', 'r')
		if 'result' not in f.read():
			raise BaseException(f'Content invalid')
		
class step2_Override_fail:
	
	trigger = step2_run
	
	def fakeApiCall(self, **kwargs):
		return json.dumps({
			'code': 200
		})
	
	def finalCheck(self):
		f = open(f'{BASE_DIR}/{FILE_NAME}', 'r')
		if 'result' not in f.read():
			raise BaseException(f'Invalid API response')

class step2_overrideDataExample(UnitTestAction):
	
	trigger = step2_run
	
	def fakeApiCall(self, **kwargs):
		return json.dumps({
			'result': 'ok'
		})
	
	def finalCheck(self):
		f = open(f'{BASE_DIR}/{FILE_NAME}', 'r')
		if 'result' not in f.read():
			raise BaseException(f'Invalid API response')
		
class step3_checkFileContent_Fail(UnitTestAction):
	
	trigger = step3_run
	
		
	def finalCheck(self):
		
		expected_content = 'Awesome package !!'
		f = open(f'{BASE_DIR}/{FILE_NAME}', 'r')
		if f.read() != expected_content:
			raise BaseException(f'Issue with file content. Expected content is "{expected_content}"')

'''
	This class doesn't have the method "fakeApiCall", The value in the file at the end is "actual api call"
	For the final check, we want to re use the exact same check as the class "step2_overrideDataExample"
'''
class step2_WithOverrideSimpleValue(UnitTestAction):
	
	trigger = step2_run
	
	# Without this method, the program gets the actual value
	def overrideValue(self, **kwargs):
	    return True
	
	def finalCheck(self):
		
		if 'print_memory_message' in self.memory and self.memory['print_memory_message'] == True:
			print(self.memory['value_in_memory'])
			
		step2_overrideDataExample.finalCheck(self)
		





class relationExample_lvl1_1:
	children = ['scenarios.relationExample_lvl2_1', 'scenarios.relationExample_lvl2_2']

class relationExample_lvl1_2:
	children = ['scenarios.relationExample_lvl3_2']

class relationExample_lvl1_3:
	pass

class relationExample_lvl1_4:
	pass

class relationExample_lvl1_5:
	pass





class relationExample_lvl2_1:
	dependencies    = [relationExample_lvl1_1, relationExample_lvl1_2]
	children        = ['scenarios.relationExample_lvl3_1', 'scenarios.relationExample_lvl3_2']

class relationExample_lvl2_2:
	dependencies = [relationExample_lvl1_1, relationExample_lvl1_2]

class relationExample_lvl2_3:
	dependencies = [relationExample_lvl1_3]





class relationExample_lvl3_1:
	dependencies = [relationExample_lvl2_1, relationExample_lvl2_3, relationExample_lvl1_4]

class relationExample_lvl3_2:
	dependencies = [relationExample_lvl2_1]

class relationExample_lvl3_3:
	pass

class relationExample_lvl3_4:
	pass

class relationExample_lvl3_5:
	pass


SCENARIO_1 = [
	resetWorkspace,
	step1_checkFileExist_success,
	step2_overrideDataExample,
]

SCENARIO_2 = [
	resetWorkspace,
	step1_checkFileExist_success,
	step2_overrideDataExample,
	step3_checkFileContent_Fail,
]

