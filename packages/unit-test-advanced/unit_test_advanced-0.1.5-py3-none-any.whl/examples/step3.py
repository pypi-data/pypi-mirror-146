import os
from unit_test_advanced.functools import initUT

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

'''
	Writing some content in the file created from step1
'''

# For each entry point, the function must accept the parameter UT
@initUT
def run(UT):
	
	f = open(f'{BASE_DIR}/myfile.txt', 'w+')
	f.write('This package sucks')
	f.close()
	
	f = open(f'{BASE_DIR}/myfile.txt', 'r')
	print(f'File content after executing {os.path.basename(__file__)}: "{f.read()}"')
	f.close()

class Step4:
	
	@classmethod
	def testfunc(cls, UT, a, b):
		print(a, b)
		
if __name__ == '__main__':
	Step4.testfunc(1, 2)
	# run()