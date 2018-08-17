# Advanced Python for Maya

In this project, we'll be learning how to use the Python API for OpenMaya to create a variety of plugins and tools for Maya.



The OpenMaya API gives us deeper access to Maya's internals than the Commands API that is used by MEL and Python,
without having to switch to using C++.

At the end of the course, we'll also be converting a Python Plugin to C++.

# Software Used

For this course I'll be using the following programs:

* Autodesk Maya 2018

    While you can follow most of this course in Maya 2011 and above, I highly recommend using Maya 2018 if possible.

    A trial is available here:

    https://www.autodesk.ca/en/products/maya/free-trial

    You can also get a student edition if you are part of an officially recognized educational institution:

    https://www.autodesk.com/education/free-software/maya

* PyCharm

    You can use any text editor you like, but I will be using PyCharm because it is my personal preference.

    You can get PyCharm EDU here:

    https://www.jetbrains.com/pycharm-edu/download/



# Resources

## Maya Documentation

Autodesk has great documentation for the Maya API. I highly recommend giving it a read

### General Documentation

This is a general overview of how the API is structured and how it interacts with Maya.
Most of this is written with C++ in mind, but it is a very useful resource.

http://help.autodesk.com/view/MAYAUL/2018/ENU//?guid=__files_API_Introduction_htm

### Python 2.0 API

This is the documentation for the API we'll be covering.

It isn't as complete as the API for C++ but is easier to read

http://help.autodesk.com/view/MAYAUL/2018/ENU//?guid=__py_ref_index_html


### C++ API

The C++ is the main API for Maya, and is the best reference for any of the code we'll be using.

If you can't find information on something in the Python API docs, this is the best place to fallback to.

http://help.autodesk.com/view/MAYAUL/2018/ENU//?guid=__cpp_ref_index_html


## Devkit

You will want to get the Maya developer kit so that you can use autocompletion and see some of Autodesks code examples.

Read here on how to install the devkit

http://help.autodesk.com/view/MAYAUL/2018/ENU//?guid=__files_Setting_up_your_build_environment_htm

* Maya 2018
    https://www.autodesk.com/developer-network/platform-technologies/maya#
    
    https://s3-us-west-2.amazonaws.com/autodesk-adn-transfer/ADN+Extranet/M%26E/Maya/devkit+2018/Maya2018-DEVKIT_Windows.zip
    
    https://s3-us-west-2.amazonaws.com/autodesk-adn-transfer/ADN+Extranet/M%26E/Maya/devkit+2018/Maya2018_DEVKIT_Linux.tgz
    
* Maya 2017 ext 3
    https://www.autodesk.com/developer-network/platform-technologies/maya#
    
    https://s3-us-west-2.amazonaws.com/autodesk-adn-transfer/ADN+Extranet/M%26E/Maya/devkit+2017/Maya2017u3_DEVKIT_Windows.zip

Older versions of Maya will either have it bundled or can reuse the devkits from above.

## Books and Blogs

There are many other bits of content that are extremely useful to learn the API.

I'll be adding them here.

* **Chad Vernons Blog** : http://www.chadvernon.com/blog/


