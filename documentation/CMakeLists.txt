if(EXISTS "sphinx_rtd_theme")
  set(sphinx_rtd_theme_repository "sphinx_rtd_theme")
else()
  set(sphinx_rtd_theme_repository "https://github.com/computationalgeography/sphinx_rtd_theme")
endif()

FetchContent_Declare(sphinx_lue_theme
  GIT_REPOSITORY ${sphinx_rtd_theme_repository}
  GIT_TAG 3ecd7ff
)

FetchContent_MakeAvailable(sphinx_lue_theme)

configure_file(conf.py.in
  conf.py
)

configure_file(pip.rst.in
  pip.rst
)


# Hack to mimic Python modules
# this way we don't need to install the packages for documentation building
# similar with PCRaster, maks empty dir to allow for module import
file(WRITE ${CMAKE_BINARY_DIR}/source/lue/data_model/__init__.py
"class Unit(object):
  day,month,year=1,1,1
"
)
file(WRITE ${CMAKE_BINARY_DIR}/source/pcraster/__init__.py "")
file(WRITE ${CMAKE_BINARY_DIR}/source/xarray/__init__.py "")
file(WRITE ${CMAKE_BINARY_DIR}/source/pandas/__init__.py "")
file(WRITE ${CMAKE_BINARY_DIR}/source/networkx/__init__.py "")
file(WRITE ${CMAKE_BINARY_DIR}/source/osgeo/__init__.py "")
file(WRITE ${CMAKE_BINARY_DIR}/source/osgeo/gdal/__init__.py "")
file(WRITE ${CMAKE_BINARY_DIR}/source/osgeo/osr/__init__.py "")
file(WRITE ${CMAKE_BINARY_DIR}/source/osgeo/ogr/__init__.py "")

set(SOURCES
  index.rst
  general/introduction.rst
  general/concepts.rst
  general/install.rst
  general/sourcecode.rst
  general/indices.rst
  operations/index.rst
  operations/dataframe.rst
)


add_custom_target(init_doc_sources ALL
  DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/index.rst
)


add_custom_command(
  OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/index.rst
  DEPENDS
    ${SOURCES}
    ${CMAKE_CURRENT_BINARY_DIR}/conf.py
  WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
  COMMAND ${CMAKE_COMMAND} -E copy_directory _static ${CMAKE_CURRENT_BINARY_DIR}/_static
  COMMAND ${CMAKE_COMMAND} -E copy_directory _templates ${CMAKE_CURRENT_BINARY_DIR}/_templates
  COMMAND ${CMAKE_COMMAND} -E copy_directory general ${CMAKE_CURRENT_BINARY_DIR}/general
  COMMAND ${CMAKE_COMMAND} -E copy_directory operations ${CMAKE_CURRENT_BINARY_DIR}/operations
  COMMAND ${CMAKE_COMMAND} -E copy index.rst ${CMAKE_CURRENT_BINARY_DIR}
)


add_custom_target(documentation
  DEPENDS init_campo_sources
  DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/_build/html/index.html
)


add_custom_command(
  OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/_build/html/index.html
  DEPENDS init_doc_sources
  WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
  VERBATIM
  COMMAND ${CMAKE_COMMAND} -E remove_directory _build
  COMMAND ${CMAKE_COMMAND} -E make_directory _build
  COMMAND sphinx-build -q -W -b html ${CMAKE_CURRENT_BINARY_DIR} _build
)
