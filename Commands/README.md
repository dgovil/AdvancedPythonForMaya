# Custom Commands

## Overview

In this project we'll be creating custom commands.

These are functions that can be called from the `maya.cmds` library
as well as from MEL. This means we don't have to wrap calls to our code in a
`python("doThis")` or other similar methods.

They let us conveniently extend the functionality available inside of Maya
and let any scripts call out to them as if they were native functions.

We'll be creating two commands:

* A simple Hello World command that is capable of taking an argument
* A Distribute command that can distribute objects in our scene

We'll also be learning about the following concepts:

* Decorators
* staticmethods and classmethods
* Loading and unloading plugins

## Decorators

Decorators are functions that wrap other functions.

They can really help to clean up our code but also let us easily modify functions in place.

