# Custom Nodes

## Overview

In this project, we'll learn to create custom nodes to be used in our node graph.

The two nodes we'll be creating are:

* A simple math node
* A mesh deformer

Python is useful for prototyping graph nodes, where we can quickly explore ideas
without having to setup our compiler, and load C++ nodes in.

However you should try and keep your use Python nodes in production to a minimum,
especially with Maya 2016 and higher.

This is because only one Python node can run at a time, whereas many C++ nodes can run at aonce.

Depending on your graph, this can severely bottleneck performance and can prevent
you from using Parallel evaluation. Python is also generally slower by default than C++

That said, it is incredibly useful for prototyping your ideas and many movies
have used Python nodes in production. The ability to quickly write an idea in code
is still an invaluable skill to have.