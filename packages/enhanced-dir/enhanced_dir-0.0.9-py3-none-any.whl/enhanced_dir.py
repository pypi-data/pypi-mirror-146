def enhanced_dir(arg, categorize=True, show_types=False, checks=False):
    from collections import defaultdict
    if not categorize:
        return dir(arg)
    passed = defaultdict(lambda: defaultdict(set))
    failed = defaultdict(set)
    passed_ = defaultdict(lambda: defaultdict(set))
    failed_ = defaultdict(lambda: defaultdict(set))
    x = arg
    for method in dir(arg):
        type_ = type(eval(f'x.{method}'))
        try:
            qualname = eval(f'x.{method}.__qualname__')
            qualname = qualname.split('.')
            passed['x'][qualname[0]].add(qualname[1])
            passed_['x'][type_].add(qualname[1])

        except:
            failed['x'].add(method)
            failed_['x'][type_].add(method)

    if checks:
        checks_ = {}
        try:
            class A(x):
                pass

            checks_['inheritable'] = True
        except:
            checks_['inheritable'] = False

        try:
            a = defaultdict(arg)
            checks_['defaultdict_arg'] = True
        except:
            checks_['defaultdict_arg'] = False

        try:
            d = {arg: 1}
            checks_['dict_key'] = True
        except:
            checks_['dict_key'] = False

        try:
            for i in arg:
                pass
            checks_['iterable'] = True
        except:
            checks_['iterable'] = False
    if show_types and checks:
        return [[passed], [passed_], [checks_]]
    elif show_types == False and checks == True:
        return [[passed], [checks_]]
    elif show_types == True and checks == False:
        return [[passed], [passed_]]

    return passed
