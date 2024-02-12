# Written with help from GPT-4.

from functools import wraps
import jinja2
from jinja2 import meta
import inspect


def prompt(func):
    """Wrap a Python function into a Jinja2-templated prompt.
    Args:
      func (function): The function to wrap.
    Returns: 
      The wrapped function.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        docstring = func.__doc__

        sig = inspect.signature(func)
        kwargs = sign.bind(*args, **kwargs).arguments
        env = jinja2.Environment()

        parsed_content = env.parse(docstring)

        # get all variables in the docstring
        vars = meta.find_undeclared_variables(parsed_content)

        # check if all variables are in kwargs
        for var in vars:
            if var not in kwargs:
                raise ValueError(f"Variable '{var}' was not passed into the function")

        # interpolate docstring with args and kwargs
        template = jinja2.Template(docstring)
        return template.render(**kwargs)

    return wrapper
