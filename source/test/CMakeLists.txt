set(SOURCES
  extract_const_diff.py
  extract_const_same.py
  extract_dyn_diff.py
  extract_dyn_same.py
  unit_tests.py
  test_phenomenon.py
  test_propertyset.py
)


add_custom_target(init_test_sources ALL
  DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/unit_tests.py
)


add_custom_command(
  OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/unit_tests.py
  DEPENDS ${SOURCES}
  WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
  COMMENT "Copying sources..."
  COMMAND ${CMAKE_COMMAND} -E copy ${SOURCES} ${CMAKE_CURRENT_BINARY_DIR}
)


add_test(
  NAME
    campo_unit_tests
  COMMAND
    ${Python3_EXECUTABLE} ${CMAKE_CURRENT_BINARY_DIR}/unit_tests.py
)


set_tests_properties(campo_unit_tests PROPERTIES
  DEPENDS
    init_test_sources
  DEPENDS
    init_campo_sources
)

# add path of project's unit test related files to PYTHONPATH
# required to execute this unit test via ctest properly
if(WIN32)
  message(FATAL_ERROR)
else()
  set(ENV_PATH $ENV{PYTHONPATH})
  set_tests_properties(campo_unit_tests PROPERTIES
    ENVIRONMENT "PYTHONPATH=${CMAKE_BINARY_DIR}/source:$ENV{PYTHONPATH}"
  )
endif()
