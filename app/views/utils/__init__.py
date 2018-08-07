def parse_params(multi_dict):
    pargs = {}
    for key in multi_dict.keys():
        if key.endswith('[]'):
            pargs[key[:-2]] = multi_dict.getlist(key)
        else:
            pargs[key] = multi_dict.get(key)

    return pargs
