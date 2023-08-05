from unit_test_advanced.functools import initUT
from unit_test_advanced.UnitTest import UnitTest

@initUT
def test1(UT, a, b):
	print('test1: ', type(UT), a, b)
	
@initUT
def test2(UT_other_name: UnitTest, a, b):
	print('test2: ', type(UT_other_name), a, b)
	
	
@initUT('UT_other_name')
def test3(UT_other_name, a, b):
	print('test3: ', type(UT_other_name), UT_other_name._parent_execution_plan, a, b)
	
@initUT('UT_other_name')
def test4(UT_other_name, a, b):
	print('test4: ', type(UT_other_name), a, b)
		
		
		
test1(1, 2)
test2(1, 2)
test3(1, 2)
test3( UnitTest(parent_execution_plan= 'child'), 1, 2)
test4(UT_other_name= 'value is passed', a= 1, b= 2)