# Introduction to the OpenMaya API

## Overview

In this intro project we'll be going over the following concepts:

* Comparing languages
* Learning about the two OpenMaya APIs
* Installing up our devkit and other assets
* Setting up autocomplete in the editor
* Writing a simple hello world script
* Comparing the speed of OpenMaya and Commands libraries

This project may seem basic, but it gives us a very good foundation to start
building our knowledge on.

### C++ vs Python

The OpenMaya API is available under both C++ and Python.
The reasons to use both ultimately come down to the differences in the language.

|   |  Pros |   Cons|
|---|:---|---:|
|**C++**| Fast and optimized|  Long setup process |
|| Compile time checking so fewer bugs | Code has to be recompiled for every Maya and OS version |
|| Can use multithreading |Cannot be interactively modified during runtime |
|||Minimal standard library|
|**Python**| Same script file can run without recompiling  | Slower than C++  |
||Can be used both for plugins and interactively | No simple multithreading |
||Make use of both cmds and OpenMaya | |
||Massive standard library||

### Standalone vs Plugins

Python allows us to use the OpenMaya API inside standalone scripts for Maya
as well as inside plugins.

This means we can make use of many of the features and intermix them in our regular scripts
without having to write and load plugins for Maya.

At the same time, we can still make plugins if we need to make custom commands or nodes,
but this gives us a lot of flexibility to develop our code how we want.

### Naming

The Maya API has many well defined conventions for the naming of objects in code.

These denote the kind of object we're interacting with and help keep our code organizes,
both in the editor and mentally.

|  Prefix |  Description  |
|---|---|
| MFn  | Sets of functions that let us interact with MObjects of a given type  |
| MIt | Iterators that let us loop through items, components and other objects |
| MPx | Proxy classes which are designed to be derived from to make our plugins |
| M | Everything else has a simple M prefix to denote it's part of Maya and they wrap the internal objects.  For example MObject wraps Maya Objects and MGlobal wraps Maya's Global methods |
