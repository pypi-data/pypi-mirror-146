import os
from unit_test_advanced.functools import initUT

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

'''
	Simply creating a file
'''

# For each entry point, the function must accept the parameter UT
@initUT
def run():
	
	f = open(f'{BASE_DIR}/myfile.txt', 'w+')
	f.close()
	
	f = open(f'{BASE_DIR}/myfile.txt', 'r')
	print(f'File content after executing {os.path.basename(__file__)}: "{f.read()}"')
	f.close()
	
if __name__ == '__main__':
	run()


