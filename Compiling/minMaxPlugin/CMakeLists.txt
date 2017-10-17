# Define the minimum required CMake version to run this project.
# CMake is a lot nicer above 3.4 so I always set that as my minimum
cmake_minimum_required(VERSION 3.4)

# We set the project name up here
project(minMaxPlugin)

# If noone has defined a default Maya version, then define it here
# I'm using 2018, so lets set it to that.
if(NOT DEFINED MAYA_VERSION)
    set(MAYA_VERSION 2018 CACHE STRING "Maya version")
endif()

# Then we tell CMake where it can find our modules
set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/modules)

# We'll also let CMake know about the directory we save our scripts in
set(PROJECT_SOURCE_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/source)

# We tell it which files are part of our project and store it in a variable called SOURCE_FILES
set(
    SOURCE_FILES
    ${PROJECT_SOURCE_DIRECTORY}/minMax.h
    ${PROJECT_SOURCE_DIRECTORY}/minMax.cpp
)

# It then needs to find the Maya package to know how to load up all the Maya modules
find_package(Maya REQUIRED)

# We'll add our project as a library
add_library(${PROJECT_NAME} SHARED ${SOURCE_FILES})

# And tell it to link against the Maya main library
target_link_libraries(${PROJECT_NAME} PRIVATE Maya::Maya)
# It also needs to link against that library
target_include_directories(${PROJECT_NAME} PRIVATE Maya::Maya)

# Finally we use the MAYA_PLUGIN, to generate a plugin of our project name
MAYA_PLUGIN(${PROJECT_NAME})