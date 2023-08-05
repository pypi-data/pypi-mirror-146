import os, json
from unit_test_advanced.functools import initUT

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

'''
	overrideing some data that will be different according from where the file is executed.
	If the file is run directly, the content of "myfile.txt" is "actual api call".
	However, when run from the unit test, the content is "fake api call". The function "fakeApiCall" from the class step2_overrideDataExample is actually executed instead of "imagineThisIsAnApiCall".
'''


def imagineThisIsAnApiCall(myParam):
	return json.dumps({
		'result': 'success'
	})

# For each entry point, the function must accept the parameter UT
@initUT
def run(UT):
	
	f = open(f'{BASE_DIR}/myfile.txt', 'w+')
	
	is_overrideed = UT.override(
		'overrideValue',
		UT.returnValue,
		value= True
	)
	
	f.write(
		UT.override(
			'fakeApiCall',
			imagineThisIsAnApiCall,
			myParam = 'value to pass'
		)
	)
	f.close()
	
	f = open(f'{BASE_DIR}/myfile.txt', 'r')
	print(f'File content after executing {os.path.basename(__file__)}: "{f.read()}"')
	f.close()
	
if __name__ == '__main__':
	run()
