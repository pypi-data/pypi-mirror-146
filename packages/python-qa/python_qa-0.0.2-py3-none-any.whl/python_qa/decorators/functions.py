import functools

from python_qa.utils.func import func_parameters_dic
from python_qa.utils.random import logger


class Decorators:
    @staticmethod
    def step(title: str = None):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                param = func_parameters_dic(func, *args, **kwargs)
                logger.info("Executing: " + title.format(*args, **kwargs))
                return func(*args, **kwargs)

            return wrapper

        return decorator
