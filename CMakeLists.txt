cmake_minimum_required(VERSION 3.18)

project(campo
  VERSION 0.0.23
  DESCRIPTION "Modelling framework for fields and agents"
  HOMEPAGE_URL "https://campo.computationalgeography.org/"
  LANGUAGES NONE
)

set(DEV_CURRENT_YEAR "2020")

set(${PROJECT_NAME}_ORGANISATION_NAME "Computational Geography group, Dept of Physical Geography, Utrecht University")
set(${PROJECT_NAME}_COPYRIGHT
     "${DEV_CURRENT_YEAR}, ${${PROJECT_NAME}_ORGANISATION_NAME}")


find_package (Python3 COMPONENTS Interpreter NumPy)
include(FetchContent)

enable_testing()


add_subdirectory(source)
add_subdirectory(documentation)
