from unit_test_advanced.UnitTest import UnitTest


def initUT(arg):
	param_name = None
	
	def decorator(func):
		def wrapper(*args, **kwargs):
			
			final_ut_param_name = 'UT'
			list_args = func.__code__.co_varnames
			if param_name is None:
				if 'UT' not in list_args:
					from typing import get_type_hints
					for _var, _type in get_type_hints(func).items():
						if _type is UnitTest:
							final_ut_param_name = _var
							break
			else:
				final_ut_param_name = param_name
			
			if final_ut_param_name in list_args:
				args = list(args)
				index_ut = list_args.index(final_ut_param_name)
				
				if len(args) - 1 >= index_ut:
					if isinstance(args[index_ut], UnitTest) is False:
						args.insert(index_ut, UnitTest())
				
				elif final_ut_param_name not in kwargs and final_ut_param_name in list_args:
					kwargs[final_ut_param_name] = UnitTest()
			
			return func(*args, **kwargs)
		return wrapper
	
	if callable(arg):
		
		return decorator(arg)
	else:
		param_name = arg
		return decorator