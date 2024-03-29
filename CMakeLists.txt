cmake_minimum_required(VERSION 3.22)

project(campo
  VERSION 0.3.12
  DESCRIPTION "Modelling framework for fields and agents"
  HOMEPAGE_URL "https://campo.computationalgeography.org/"
  LANGUAGES NONE
)

set(CMAKE_MODULE_PATH
    $ENV{CMAKE_MODULE_PATH}
    ${CMAKE_CURRENT_SOURCE_DIR}/environment/cmake
)


set(DEV_CURRENT_YEAR "2024")

set(${PROJECT_NAME}_ORGANISATION_NAME "Computational Geography group, Dept. of Physical Geography, Utrecht University")
set(${PROJECT_NAME}_COPYRIGHT
     "2020 - ${DEV_CURRENT_YEAR}, ${${PROJECT_NAME}_ORGANISATION_NAME}")

find_package(Python 3.8
  REQUIRED COMPONENTS Interpreter
)

include(FetchContent)

enable_testing()


option(
  CAMPO_BUILD_WHEEL
  "Campo build wheel"
  OFF
)

if(NOT ${CAMPO_INSTALL_DIR})
  set(CAMPO_INSTALL_DIR ${CAMPO_INSTALL_DIR})
else()
  set(CAMPO_INSTALL_DIR ${CMAKE_BINARY_DIR}/package)
endif()

add_subdirectory(source)
add_subdirectory(documentation)

message(STATUS "-------------------------------------------------")
message(STATUS "Campo configuration summary:")
message(STATUS "  Version:                " ${${PROJECT_NAME}_VERSION})
message(STATUS "  Installation directory: " ${CAMPO_INSTALL_DIR} )
message(STATUS "  Build configuration:")
message(STATUS "    Python interpreter:   " ${Python_EXECUTABLE})
message(STATUS "    Python version:       " ${Python_VERSION_MAJOR}.${Python_VERSION_MINOR}.${Python_VERSION_PATCH})
message(STATUS "    Site-packages:        " ${Python_SITELIB})
message(STATUS "  Build wheel           : " ${CAMPO_BUILD_WHEEL} )
message(STATUS "-------------------------------------------------")
