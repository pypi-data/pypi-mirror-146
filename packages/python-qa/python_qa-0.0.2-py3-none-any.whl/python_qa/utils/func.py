import inspect


def func_parameters_dic(func, *args, **kwargs):  # ToDo: to realize completely, not only dic
    parameters = {}
    args_spec = inspect.getfullargspec(func)
    args_order = list(args_spec.args)
    args_dict = dict(zip(args_spec.args, args))
    return args_dict
