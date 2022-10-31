cmake_minimum_required(VERSION 3.18)

project(campo
  VERSION 0.3.2
  DESCRIPTION "Modelling framework for fields and agents"
  HOMEPAGE_URL "https://campo.computationalgeography.org/"
  LANGUAGES NONE
)

set(CMAKE_MODULE_PATH
    $ENV{CMAKE_MODULE_PATH}
    ${CMAKE_CURRENT_SOURCE_DIR}/environment/cmake
)


set(DEV_CURRENT_YEAR "2022")

set(${PROJECT_NAME}_ORGANISATION_NAME "Computational Geography group, Dept of Physical Geography, Utrecht University")
set(${PROJECT_NAME}_COPYRIGHT
     "2020, ${DEV_CURRENT_YEAR}, ${${PROJECT_NAME}_ORGANISATION_NAME}")


find_package (Python3 COMPONENTS Interpreter NumPy)
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
message(STATUS "    Python interpreter:   " ${Python3_EXECUTABLE})
message(STATUS "    Python version:       " ${Python3_VERSION_MAJOR}.${Python3_VERSION_MINOR}.${Python3_VERSION_PATCH})
message(STATUS "    Site-packages:        " ${Python3_SITELIB})
message(STATUS "  Build wheel           : " ${CAMPO_BUILD_WHEEL} )
message(STATUS "-------------------------------------------------")


# Only configured for packaging source code required to build a package!
# include(CampoPackaging)
