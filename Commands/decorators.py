# Decorators are functions that wrap other functions

# Lets say we have a function
def foo():
    print("This is foo")


# If we run foo
# It will print
# This is foo
print("\n\n--------------------\nCalling Foo without any wrappers\n")
foo()
# This should give us back the name of foo which is foo
print(foo.__name__)


# But now lets say we want to always wrap foo inside some other logic.
# We'll create another function and call it spam that takes a function

def spam(func):
    print("This is spam")
    # We capture the value returned by foo
    value = func()
    # Then we finish up
    print("Spam is done")
    # and finally return the value
    return value


# We can now wrap foo when we call it
# This should print
# This is spam
# This is foo
# Spam is done
print("\n\n--------------------\nCalling foo directly wrapped by spam\n")
spam(foo)


# But we have to remember to do this everytime we call foo
# Another way to do this is to wrap foo and hold it as a new foo
# So lets make a second spam, called deferSpam

# So first we define the outer layer that will create a new function
def deferSpam(func):
    # This function will wrap around foo
    # We don't know what arguments foo will take if any,
    # so we just capture every argument just in case and give it to foo to deal with
    def wrapperSpam(*args, **kwargs):
        # Inside this generated function, we'll do everything we did in spam
        print("This is wrapper spam spam")
        # Just like above we store the value returned by foo
        value = func(*args, **kwargs)
        # Then finish up and return that value
        print("wrapperSpam is done")
        return value

    # The outer function then returns the newly created function that wraps around foo
    return wrapperSpam


# We can then wrap foo forever by doing this
# Now foo will actually be a copy of wrapperSpam that knows to call foo
print("\n\n--------------------\nCalling foo wrapped by wrapperSpam created by deferSpam\n")
foo = deferSpam(foo)

# So if I call foo now
# This should print
# This is spam
# This is foo
# Spam is done
foo()

# in fact we can check stuff about foo
print("\n\n--------------------\n")
# This tells us that foo is now actually wrapperSpam
print(foo.__name__)


# This is kind of ugly, so a better way to do it so like so
# Lets create a new function
# We can wrap it directly by deferSpam using the @ symbol
# This is a python syntax for doing the wrapping we did above at definition time
@deferSpam
def hello(name):
    print("Hello, %s" % name)


# Now lets call it
print("\n\n--------------------\nCalling hello wrapped by wrapperSpam created by deferSpam\n")
# This should print
# This is spam
# Hello, David
# Spam is done
hello('David')
# But the name is still wrapperSpam
print hello.__name__

# So lets import something to help us out here instead
# Typically for decorators we also make use of the functools.wraps function
# This itself is a decorator that fixes some issues with decorators.

from functools import wraps


# Lets create a new wrapper
def eggs(func):
    # But this time we use functools.wraps as a decorator and give it the func argument
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Then we make the decorator as we did above
        print("This is eggs")
        ret = func(*args, **kwargs)
        print("Eggs is done")
        return ret

    return wrapper


# Now lets make a new function and add the eggs decorator
@eggs
def goodbye(name):
    print("Goodbye, %s" % name)


# Lets call it
# This will print
# This is eggs
# Goodbye, Mary
# Eggs is done
goodbye('Mary')
# But now lets check the name
# This will now print goodbye
print goodbye.__name__

# And that's the beauty of functools.wraps
# It can hide the fact that our function was ever decorated.
# This is very useful because now any code that wants to know the original function doesn't have to search for it
# It can just call it like it was never decorated
# This is great for functions like help() in python that need to know the original functions docstrings etc..
