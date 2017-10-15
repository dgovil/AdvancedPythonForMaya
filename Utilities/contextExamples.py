# A context wraps code blocks with functionality that runs before and after the code block is done.
# This lets us set up things and then clean up after, even if our code errors

# A common example is the file callback
# We open files like this without a callback
# First we open it
thisFile = open(__file__)
# Then we do something with the contents
print(thisFile.read())
# Finally we close it
# But if we error between the open and close, or forget
# The file may not be closed
# This can cause issues like corruption, or preventing the file being opened elsewhere
# or preventing us opening more files
thisFile.close()

# Instead we can use a context
# The open context will automatically close our file when the code inside it is done running, even if it errors
with open(__file__) as thisFile:
    print(thisFile.read())

# A context is essentially an advanced way of doing a try/finally
# But a lot more powerful
try:
    thisFile = open(__file__)
    print(thisFile.read())
finally:
    print("Closing path in try/finally")
    thisFile.close()

# A quick way of making a context is with a decorator
# This is an example of how can emulate the open context
# First import contextlib
from contextlib import contextmanager


# Then we can wrap our function
@contextmanager
def openFile(path, mode='r'):
    # We put our setup code in the try
    try:
        thisFile = open(path, mode)
        # Then with the yield we give it back outside our function
        # Yield is like return except the function can keep running after
        yield thisFile
    finally:
        # Then we close out the file path
        print("Closing path in decorator context")
        thisFile.close()


with openFile(__file__) as thisFile:
    print(thisFile.read())


# Finally a more advanced way to create a context is using a class
# We create the class as normal
class OpenFile(object):
    def __init__(self, path, mode='r'):
        # The init method is what receives all our input for the context
        # In this case we'll just store the values

        self.path = path
        self.mode = mode
        self.openFile = None

    def __enter__(self):
        # The enter method is where all the setup of our context happens
        self.openFile = open(self.path, self.mode)
        return self.openFile

    def __exit__(self, exc_type, exc_val, exc_tb):
        # The exit method is where we can do any of the cleanup we need to do.
        # It gets back a few arguments, in order these are:
        # exc_type: the type of exception that occured or None if nothing went wrong
        # exc_val: the actual exception
        # exc_tb: the traceback of the exception

        # So with that knowledge, lets close out the file if we can
        if self.openFile:
            print("Closing path in class context")
            self.openFile.close()

        # Then raise the exception we got
        if exc_val:
            raise exc_val


with OpenFile(__file__) as thisFile:
    raise RuntimeError('Test')
