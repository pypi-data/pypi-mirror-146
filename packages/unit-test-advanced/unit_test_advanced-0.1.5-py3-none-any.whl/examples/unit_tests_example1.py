from unit_test_advanced.UnitTest import UnitTest
import os, sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.append(BASE_DIR)

from scenarios import SCENARIO_1, SCENARIO_2
from scenarios import resetWorkspace, step2_WithOverrideSimpleValue, step1_checkFileExistUseMemory_success


'''
	This example showcase some basic scenarios with SCENARIO_2 failing purposely
'''
def run():
	UT = UnitTest(
		is_enabled              = True,  # Default is False. MUST be set to true here when we run the unit tests
		parent_execution_plan   = 'random', # Default is 'all', other accepted values are 'all', 'main', or 'random'
		children_execution_plan = 'all', # Default is 'all', other accepted values are 'all', 'main', or 'random'
		count_limit_identify_infinite_loop = 2, # Default is 2
		verbose                 = False, # Default is False
	)
	
	# What parameters to pass in the list
	UT.execute([
		# When a single test-class is passed, the relationship tree will get build based on the settings "parent_execution_plan" and "children_execution_plan"
		resetWorkspace,
		# A list of unit test classes
		[
			resetWorkspace,
			step1_checkFileExistUseMemory_success,
			step2_WithOverrideSimpleValue, # This test contains an example of how to use the memory
		],
		# Variables containing a list of unit test classes
		SCENARIO_1, # Unit test passed
		SCENARIO_2, # Unit test failed on "step3_checkFileContent_Fail" -> The content of the file is not as expected
	])
	
	
if __name__ == '__main__':
	run()