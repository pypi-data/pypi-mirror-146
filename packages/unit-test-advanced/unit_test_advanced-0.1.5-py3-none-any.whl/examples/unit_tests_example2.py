from unit_test_advanced.UnitTest import UnitTest

import os, sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from scenarios import relationExample_lvl1_1, relationExample_lvl2_1, relationExample_lvl3_1

def run():
	UT = UnitTest(
		is_enabled              = True,  # Default is False. MUST be set to true here when we run the unit tests
		parent_execution_plan   = 'all', # Default is 'all', other accepted values are 'all', 'main', or 'random'
		children_execution_plan = 'all', # Default is 'all', other accepted values are 'all', 'main', or 'random'
		count_limit_identify_infinite_loop = 2, # Default is 2
		verbose                 = True, # Default is False
	)
	
	print('')
	print('--', 'Execution tree from the top:')
	print('')

	UT.preparePlans([
		relationExample_lvl1_1
	])
	for plan in UT.getExecutionPlans():
		print(plan)
		
		
	print('')
	# In verbose mode, it displays when a relationship does not go both way
	print('--', 'Execution tree from the bottom:')
	print('')

	UT.resetExecutionPlans()
	UT.preparePlans([
		relationExample_lvl3_1
	])
	for plan in UT.getExecutionPlans():
		print(plan)


	print('')
	print('--', 'Execution tree from the middle (Main plan on parent side and all scenarios possible on the children):')
	print('')

	UT.updateSettings(
		parent_execution_plan   = 'main',
		verbose                 = False,
	)

	UT.resetExecutionPlans()
	UT.preparePlans([
		relationExample_lvl2_1
	])
	for plan in UT.getExecutionPlans():
		print(plan)

	print('')
	print('--', 'Execution tree from the middle (Main plan on parent side and random scenario on the children):')
	print('')

	UT.updateSettings(
		children_execution_plan   = 'random'
	)

	UT.resetExecutionPlans()
	UT.preparePlans([
		relationExample_lvl2_1
	])
	for plan in UT.getExecutionPlans():
		print(plan)
	
if __name__ == '__main__':
	run()