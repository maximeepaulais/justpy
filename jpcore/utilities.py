"""
utilities for justpy
"""
import asyncio
import inspect
import os

def find_files(path: str, ext: str) -> list:
        """
        find files with the given extension in the given path

        Args:
            path(str): the path to start with
            ext(str): the extension to search for

        Returns:
            list: a list of files found
        """
        foundFiles = []
        for root, _dirs, files in os.walk(path, topdown=False):
            for name in files:
                if name.endswith(ext):
                    filepath = os.path.join(root, name)
                    foundFiles.append(filepath)
        return foundFiles

def print_request(request):
    # See https://www.starlette.io/routing/ for path_params
    # and https://github.com/encode/starlette/blob/master/starlette/routing.py line 82
    print(type(request._scope))
    d = dict(request._scope)
    print(d)
    d.pop("headers")
    print(d)
    fields = [
        "path",
        "method",
        "url",
        "headers",
        "query_params",
        "path_params",
        "client",
        "cookies",
        "state",
    ]
    print("*************************************")
    for field in fields:
        # print(field, request[field])
        try:
            print(field, request[field])
        except:
            print(field, getattr(request, field))
    print(request.url.path, request.url.port, request.url.scheme, dir(request.url))
    for i, j in request.query_params.items():
        print(i, j)
    print("URL related -------")
    for j in [
        "components",
        "fragment",
        "hostname",
        "is_secure",
        "netloc",
        "password",
        "path",
        "port",
        "query",
        "replace",
        "scheme",
        "username",
    ]:
        print(j, getattr(request.url, j))
    for j in getattr(request.url, "components"):
        print(j)
    print("*************************************")


def run_task(task):
    """
    Helper function to facilitate running a task in the async loop
    """
    try:
        # 1. Try to get the loop that is actually running right now
        loop = asyncio.get_running_loop()
        loop.create_task(task)
    except RuntimeError:
        # 2. If no loop is running, we cannot schedule the task.
        # In Python 3.13, creating a new loop here via get_event_loop() 
        # would be useless because that new loop wouldn't be running.
        print("Error: run_task called but no asyncio loop is running.")


async def create_delayed_task(task, delay):
    await asyncio.sleep(delay)
    # asyncio.create_task automatically finds the running loop in Py3.7+
    asyncio.create_task(task)


def print_func_info(*args):
    # Calling function name
    print(inspect.stack()[1][3])
    for i in args:
        print(i)
