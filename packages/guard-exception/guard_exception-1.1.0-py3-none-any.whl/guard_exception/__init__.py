__autor__ = "Rafael Fernando Garcia Sagastume"
__copyright__ = "Copyright 2022, Rafael Fernando Garcia Sagastume, Guatemala, Escuintla"  # noqa
__license__ = "BSD 3-Clause License"
__version__ = "1.1.0"
__maintainer__ = "Rafael Fernando Garcia Sagastume <https://github.com/rafaelsagastume>"  # noqa
__status__ = "Production"


class guard_exception:
    def __init__(self):
        pass

    def guardException(self, f, **kwargs):
        """
        Description: catch fatal errors or any type of error,
        used to easily normalize executions in fast tween calls with PythonKit

        arguments: f: function to be executed
        kwargs: arguments to be passed to the function

        return: result of the function or str error message if any error occurs
        """

        error = None
        result = None
        try:
            result = f(**kwargs)
        except Exception as e:
            error = e.__str__()

        return {"data": result, "error": error}

    def guardSearchKeyException(self, dic, key):
        """
        Description: search a key in a dictionary,
        used to easily normalize executions in fast tween calls with PythonKit

        arguments: dic: dictionary to be searched
        key: key to be searched

        return: result of the search or str error message if any error occurs
        """

        error = None
        result = None
        try:
            result = dic[key]
        except Exception as e:
            error = e.__str__()

        return {"data": result, "error": error}

    def guardSearchKeryRecursiveException(self, dic, key):
        """
        Description: search a key in a dictionary,
        used to easily normalize executions in fast tween calls with PythonKit

        arguments: dic: dictionary to be searched
        key: key array to be searched

        return: result of the search or str error message if any error occurs
        """

        error = None
        result = None
        try:
            for index in range(len(key)):
                result = dic[key[index]]
                dic = result

        except Exception as e:
            result = None
            error = e.__str__()

        return {"data": result, "error": error}

    def guardExceptionWithOutParams(self, f):
        """
        Description: catch fatal errors or any type of error,
        used to easily normalize executions in fast tween calls with PythonKit

        arguments: f: function to be executed

        return: result of the function or str error message if any error occurs
        """

        error = None
        result = None
        try:
            result = f()
        except Exception as e:
            error = e.__str__()

        return {"data": result, "error": error}

    def guardExceptionIsIterable(self, dic, key):
        """
        Description: catch fatal errors or any type of error,
        used to easily normalize executions in fast tween calls with PythonKit

        arguments: dict => dictionary to be searched
        key: key to search

        return: (1 or 0) => (True or False)
        """

        error = None
        result = 1
        try:
            aux = (dic[key])
            if aux is None:
                result = 0
            else:
                result = 1
        except Exception as e:
            result = 0
            error = e.__str__()

        return {"data": result, "error": error}
