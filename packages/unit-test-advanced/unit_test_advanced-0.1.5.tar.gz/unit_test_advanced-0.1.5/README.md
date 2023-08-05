Unit Test Advanced
==========

### *The Python Unit Test Toolkit*

Unit Test Advanced is the Python testing toolkit for programmable execution plans. It makes it easy to write, test and scale complex applications and libraries.

This package gives you the flexibility to use the production code to run the tests, assert results at any time within the code, and inject custom data. Lightweight with no dependencies, it is compatible with any framework such as Django or Flask.


## Features

- Program multiple execution plans
- Pass values from one step to another
- No code duplication; use production code to run tests
- Inject custom data
- Auto-create execution plans from the relationship between all tests

## Advantages

- Highly flexible
- Lightweight and independent
- Open-source
- Real use cases
- Support & documentation

## Authors

- Rudy Fernandez

## Install
The easiest way to install the Unit Test Advanced library is to use a package manager:
`pip install unit-test-advanced`


## Prepare the tests

Examples can be found [here](https://github.com/roodrepo/unit_test_advanced/tree/v0-dev/examples)

### Create a test class

```python
from unit_test_advanced.UnitTestAction import UnitTestAction
import os, sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.append(BASE_DIR)
from step1 import run as step1_run
		
class step1_checkFileExist_success(UnitTestAction):
	
    # Function to execute to run the action to test. 
	trigger = step1_run # NOT step1_run()
	
	def final_check(self):
		if os.path.exists(f'{BASE_DIR}/{FILE_NAME}') == False:
			raise BaseException(f'The file {FILE_NAME} is missing')

```

### Main attributes of a test class

| Attribute  | Type | Required | Info |
|:-:|:-:|:-:|:-|
| `init_params`  | dict  | no | *Kwargs to pass to the test-class when instantiated* |
| `trigger_params`  | dict  | no | *Kwargs to pass to trigger when executed* |
| `trigger`  | function  | no | *Action to execute to run the action to test.* |
| `dependencies`  | list  | no | *Previous test-classes required to run the current test (Ns-1)* |
| `children`  | list  | no | *Next test-classes to run after the current test (Ns+1)* |
| `memory`  | dict  | no | *Passing values from one test action to the next ones within the same execution plan* |
| `finalCheck`  | method  | no | *Final method called when the action is complete* |

**Make sure not to execute function while passing it to "trigger":**
`trigger = step1_run`
**NOT**
`trigger = step1_run(*args, **kwargs)`

#### Create relationships
```python

class relationExample_lvl1_1:
	children = ['scenarios.relationExample_lvl2_1', 'scenarios.relationExample_lvl2_2']

class relationExample_lvl1_2:
	children           = ['scenarios.relationExample_lvl1_2']
	
	
	
class relationExample_lvl2_1:
	dependencies  = [relationExample_lvl1_1, relationExample_lvl1_2]
	children           = ['scenarios.relationExample_lvl3_1']

class relationExample_lvl2_2:
	dependencies = [relationExample_lvl1_1]
	
	
	
# Extending the class "UnitTestAction" gives more features such as accessing the memory attribute
class relationExample_lvl3_1(UnitTestAction):
	dependencies = [relationExample_lvl2_1]
	
		def __init__(self, **kwargs):
			super().__init__(**kwargs)
```

### Value assertation
Extend your unit test class with the package of your choice
```python
from django.test import TestCase
from unit_test_advanced.UnitTestAction import UnitTestAction
import os, sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.append(BASE_DIR)
from step1 import run as step1_run
		
class step1_checkFileExist_success(UnitTestAction, TestCase):
	
	trigger = step1_run
	
	def final_check(self):
		self.assertEqual(os.path.exists(f'{BASE_DIR}/{FILE_NAME}'), True)
```
In case you use the **\_\_init\_\_** method, do not forget to initialize the parents 
```python
def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# your code here
```

### Execute scenarios
```python
from unit_test_advanced.UnitTest import UnitTest

UT = UnitTest(
    is_enabled              = True,  # Default is False. MUST be set to true here when we run the unit tests
    parent_execution_plan   = 'all', # Default is 'all'. Accepted values are 'all', 'main', or 'random'
    children_execution_plan = 'all', # Default is 'all'. Accepted values are 'all', 'main', or 'random'
    count_limit_identify_infinite_loop = 2, # Default is 2
    verbose                 = True, # Default is False
)

UT.execute([
    # When a single test-class is passed, the relationship tree will get build based on the settings "parent_execution_plan" and "children_execution_plan"
    relationExample_lvl1_1,
    # A list of unit test classes
    [
        relationExample_lvl1_1,
        relationExample_lvl1_2,
    ],
])
```

### UnitTest methods

| Attribute | Description |
|:-:|:-|
| `__init__`  | *Init the settings*  |
| `updateSettings`  | *Update the settings* |
| `override`  | *Inject data in the function triggered by the test-class* |
| `returnValue`  | *Used when overriding a single value* |
| `preparePlans`  | *Preparing all scenarios according to the settings and list passed* |
| `getExecutionPlans`  | *Get all the execution plans prepared* |
| `resetExecutionPlans`  | *Reset all the prepared execution plans* |
| `execute`  | *Execute all the unit tests from the list* |

#### \_\_init\_\_ and updateSettings
| Argument | Type | Default | Description |
|:-:|:-:|:-:|:-|
| `is_enabled` | bool | False | *Set to "True" **only** when used to run the unit tests* |
| `parent_execution_plan` | str | all | *Algorithm to create the branches from on the "dependencies" side. Accepted values are "all", "main", and "random"* |
| `children_execution_plan` | str | all | *Algorithm to create the branches from on the "children" side. Accepted values are "all", "main", and "random"* |
| `count_limit_identify_infinite_loop` | int | 2 | *Max amount of a test-class execution within an execution plan* |
| `verbose` | bool | False | *Display information while running* |

Execution plan algorithms:
- **all**: All possible execution plans are prepared
- **main**: If multiple dependencies or children, the algorithm select the first one
- **random** : If multiple dependencies or children, the algorithm randomly select a path

#### override
| Argument | Type | Default | Description |
|:-:|:-:|:-:|:-|
| `id` | bool |  | *Method to execute within the test-class to override the original function* |
| `function` | str |  | *Function to execute if the "id" method is not found within the test-class* |
| `*args` |  |  | *Arguments passed to the function or the "id" method* |
| `**kwargs` |  |  | *Arguments passed to the function or the "id" method* |

#### returnValue
| Argument | Type | Default | Description |
|:-:|:-:|:-:|:-|
| `value` |  |  | *Return the value passed* |

#### preparePlans
| Argument | Type | Default | Description |
|:-:|:-:|:-:|:-|
| `list_unit_tests` | list | [] | *Prepare all the execution plans from the list* |

#### getExecutionPlans
Does not have any attribute

#### resetExecutionPlans
Does not have any attribute

#### execute
| Argument | Type | Default | Description |
|:-:|:-:|:-:|:-|
| `list_unit_tests` | list | None | *Execute the prepared unit tests. The method "preparePlans" is not required if the list of plans is passed here.* |

## Prepare actions
#### With decorators
```python
from unit_test_advanced.functools import initUT

@initUT
def run():
	pass

if __name__ == '__main__':
	run()
```

**If you need to inject custom data within the function, it needs to accept the parameter UT**

```python
from unit_test_advanced.functools import initUT

@initUT
def run(UT):
	pass

if __name__ == '__main__':
	run()
```

#### Without decorators
```python
from unit_test_advanced.UnitTest import UnitTest

# For each entry point, the function must accept the parameter UT
def run(UT = None):
	UT = UT if type(UT) == type(UnitTest) else UnitTest()

if __name__ == '__main__':
	run()
```

#### With another parameter name
```python
from unit_test_advanced.functools import initUT
from unit_test_advanced.UnitTest import UnitTest

# Default value is 'UT'
@initUT
def test1(UT, a, b):
	print('test1: ', type(UT), a, b)

# Looking for the parameter with the type UnitTest
@initUT
def test2(UT_other_name: UnitTest, a, b):
	print('test2: ', type(UT_other_name), a, b)
	
# Explicitly state the name
@initUT('UT_other_name')
def test3(UT_other_name, a, b):
	print('test3: ', type(UT_other_name), UT_other_name._parent_execution_plan, a, b)

if __name__ == '__main__':
    test1(1, 2)
    test2(1, 2)
    test3(1, 2)
    test3( UnitTest(parent_execution_plan= 'child'), 1, 2)
    test3(UT_other_name= 'value is passed', a= 1, b= 2)
```


## My first unit test
In production, you have two actions triggered serially: [Step1](https://github.com/roodrepo/unit_test_advanced/blob/v0-dev/examples/step1.py) and [Step2](https://github.com/roodrepo/unit_test_advanced/blob/v0-dev/examples/step2.py).
For this example, we will keep things simple:

| Action | Result | Verification  |
|:-:|:-:|:-:|
| `python step1.py` | File "myfile.txt" created | Does the file "myfile.txt" exist? |
| `python step2.py` | Add response of a fake API call in the file | Does the file contains the string "result"? |

When executing the file step2.py, the script prints out the content of the file at the end: *File content after executing step2.py: "{"result": "success"}"*

#### Unit test for Step1
```python
import os
from step1 import run as step1_run

class step1_checkFileExist_success:
	
	# Function to execute to run the action to test
	trigger = step1_run

	def finalCheck(self):
	
		BASE_DIR = os.path.dirname(os.path.abspath(__file__))
		FILE_NAME = 'myfile.txt'
		
		if os.path.exists(f'{BASE_DIR}/{FILE_NAME}') == False:
			raise BaseException(f'The file {FILE_NAME} is missing')
```

#### Unit test for Step2
```python
import os
from step2 import run as step2_run

class step2_NoOverride:
	
	trigger = step2_run
	
	def finalCheck(self):
		
		BASE_DIR = os.path.dirname(os.path.abspath(__file__))
		FILE_NAME = 'myfile.txt'
		
		f = open(f'{BASE_DIR}/{FILE_NAME}', 'r')
		if 'result' not in f.read():
			raise BaseException(f'Content invalid')
```

#### Execution plans file
The actual example file can be found [here](https://github.com/roodrepo/unit_test_advanced/blob/v0-dev/examples/unit_tests_example0.py)

----

##### [Scenario 1](https://github.com/roodrepo/unit_test_advanced/blob/v0-dev/examples/unit_tests_example0_1.py): Test passed
```python
from unit_test_advanced.UnitTest import UnitTest
import os, sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.append(BASE_DIR)

from scenarios import step1_checkFileExist_success, step2_NoOverride


def run():
	UT = UnitTest(
		is_enabled              = True,  # Default is False. MUST be set to true here when we run the unit tests
	)
	
	UT.execute([
		# A list of unit test classes
		[
			step1_checkFileExist_success,
			step2_NoOverride,
		],
	])
	

if __name__ == '__main__':
	run()
```
`python unit_tests_example0_1.py`
> File content after executing step1.py: ""
> File content after executing step2.py: "{"result": "success"}"

----

##### [Scenario 2](https://github.com/roodrepo/unit_test_advanced/blob/v0-dev/examples/unit_tests_example0_2.py): Override data & test passed
```python
from unit_test_advanced.UnitTest import UnitTest
import os, sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.append(BASE_DIR)

from scenarios import step1_checkFileExist_success, step2_overrideDataExample


def run():
	UT = UnitTest(
		is_enabled              = True,  # Default is False. MUST be set to true here when we run the unit tests
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
```
`python unit_tests_example0_2.py`
> File content after executing step1.py: ""
> File content after executing step2.py: "{"result": "**ok** "}"

----

#### [Scenario 3](https://github.com/roodrepo/unit_test_advanced/blob/v0-dev/examples/unit_tests_example0_3.py): Override data & test failed
```python
from unit_test_advanced.UnitTest import UnitTest
import os, sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.append(BASE_DIR)

from scenarios import step1_checkFileExist_success, step2_Override_fail


def run():
	UT = UnitTest(
		is_enabled              = True,  # Default is False. MUST be set to true here when we run the unit tests
	)
	
	UT.execute([
		# A list of unit test classes
		[
			step1_checkFileExist_success,
			step2_Override_fail,
		],
	])
	

if __name__ == '__main__':
	run()
```
`python unit_tests_example0_3.py`
> File content after executing step1.py: ""
> File content after executing step2.py: "**{"code": 200}**"
> BaseException: Invalid API response

## More scenarios
#### [Scenario 4](https://github.com/roodrepo/unit_test_advanced/blob/v0-dev/examples/unit_tests_example0_4.py): override a value
#### [Scenario 5](https://github.com/roodrepo/unit_test_advanced/blob/v0-dev/examples/unit_tests_example1.py): multiple execution plans
#### [Scenario 6](https://github.com/roodrepo/unit_test_advanced/blob/v0-dev/examples/unit_tests_example2.py): create execution plans automatically based on dependencies
