# Written with help from GPT-4.

from functools import wraps
import jinja2
from jinja2 import meta
import inspect


def prompt(func):
    """Wraps a Python function into a Jinja2-templated prompt.

    This decorator allows rendering the function's docstring using
    Jinja2 templates, while ensuring all variables referenced in the
    docstring are passed as arguments to the function.

    Args:
        func: The function to wrap.

    Returns:
        The wrapped function.

    Raises:
        ValueError: If a variable in the docstring is not passed into the function.
  """
    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper function that renders the Jinja2-templated docstring.

           Args:
                *args: Positional arguments to the function.
                **kwargs: Keyword arguments to the function.

            Returns:
                The rendered Jinja2 template containing the docstring.
        """
        # get the function's docstring.
        docstring = func.__doc__
        # map args and kwargs onto func's signature.
        signature = inspect.signature(func)
        bound_arguments = signature.bind_partial(*args, **kwargs)
        bound_arguments.apply_defaults()
        kwargs = bound_arguments.arguments
        # create a Jinja2 environment
        env = jinja2.Environment()
        # parse the docstring
        parsed_content = env.parse(docstring)
        # get all variables in the docstring
        variables = meta.find_undeclared_variables(parsed_content)
        # check if all variables are in kwargs
        for var in variables:
            if var not in kwargs:
                raise ValueError(f"Variable '{var}' was not passed into the function")
        # interpolate docstring with args and kwargs
        template = jinja2.Template(docstring)
        return template.render(**kwargs)
    return wrapper
