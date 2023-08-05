# Author: Sergey Kolesnikov (scitator@gmail.com)
# Licence: Apache 2.0


def _is_module_available(module_call):
    try:
        eval(module_call)
        return True
    except ImportError:
        return False


IS_NUMPY_AVAILABLE = _is_module_available("exec('import numpy')")
IS_SKLEARN_AVAILABLE = _is_module_available("exec('import sklearn')")

IS_PANDAS_AVAILABLE = _is_module_available("exec('import pandas')")
IS_MATPLOTLIB_AVAILABLE = _is_module_available("exec('import matplotlib')")
IS_SEABORN_AVAILABLE = _is_module_available("exec('import seaborn')")
