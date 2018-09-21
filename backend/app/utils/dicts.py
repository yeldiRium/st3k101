__author__ = "Noah Hummel"


def merge_error_dicts(er, err):
    for k, v in er:
        if k not in err:
            err[k] = v
        else:
            v2 = err[k]
            if isinstance(v, list):
                if isinstance(v2, list):
                    err[k] = list(set([*v, *v2]))
                else:
                    err[k] = list(set([*v, v2]))
            elif isinstance(v, dict):
                if not isinstance(err[k], dict):
                    raise ValueError('Structure does not match.')
                err[k] = merge_error_dicts(er[k], err[k])
            else:
                err[k] = [v, err[k]]

    return err
