from unit_test_advanced.UnitTest import UnitTest
import os, sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.append(BASE_DIR)

from scenarios import step1_checkFileExist_success, step2_overrideDataExample


def run():
	UT = UnitTest(
		is_enabled              = True,  # Default is False. MUST be set to true here when we run the unit tests
		parent_execution_plan   = 'all', # Default is 'all', other accepted values are 'all', 'main', or 'random'
		children_execution_plan = 'all', # Default is 'all', other accepted values are 'all', 'main', or 'random'
		count_limit_identify_infinite_loop = 2, # Default is 2
		verbose                 = False, # Default is False
	)
	
	UT.execute([
		# A list of unit test classes
		[
			step1_checkFileExist_success,
			step2_overrideDataExample,
		],
	])
	

if __name__ == '__main__':
	run()