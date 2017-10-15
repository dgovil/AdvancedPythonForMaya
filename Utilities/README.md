# Utilities

# Overview

In this final Python project we'll learn to make a fwe utility functions

* Callbacks

    We'll be creating a callback manager that will let us connect callbacks to events in Maya.
    
    This architecture will be cleaner than directly connecting multiple tools to Maya as our
    callback manager will handle errors for us that each tool won't have to.

* Python Contexts

    Contexts in Python let us wrap large blocks of code inside a temporary scope, which
    can also handle cleanup if something fails.
    
    We'll use this to create a context that handles cleanup of nodes if something fails,
    and which gives us access to all the nodes created while this context is alive.