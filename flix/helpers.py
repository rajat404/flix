import linecache
import sys
import traceback
from decorator import decorator
from settings import logger


@decorator
def print_error(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except:
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        traceback_text = ''.join(traceback.format_exception(*sys.exc_info()))
        logger.error('EXCEPTION IN:\nFUNCTION: {}\nERROR: {}\nEXCEPTION: {}'.format(
            fn.__name__, exc_obj, traceback_text))
        print('EXCEPTION IN:\nFUNCTION: {}\nERROR: {}\nEXCEPTION: {}'.format(
            fn.__name__, exc_obj, traceback_text))
        print('-'*50)
        return False


def flatten(lis):
    """
    Takes a list (nested or regular), and returns a flat list
    """
    result = []
    for item in lis:
        if isinstance(item, list):
            result.extend(flatten(item))
        # won't accept empty dict or tuple
        elif item not in [None, (), {}]:
            result.append(item)
    return result
