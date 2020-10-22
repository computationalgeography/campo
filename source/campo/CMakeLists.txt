configure_file(
    __about__.py.in
    __about__.py
)

set(SOURCES
  __init__.py
  areas.py
  dataframe.py
  dataset.py
  phenomenon.py
  points.py
  property.py
  propertyset.py
  utils.py
  values.py
)

set(FIELD_SOURCES
  op_fields/__init__.py
  op_fields/operations.py
)

set(FIELDAGENT_SOURCES
  op_fieldagents/__init__.py
  op_fieldagents/operations.py
  op_fieldagents/operators.py
)

set(EXPERIMENTAL_SOURCES
  op_experimental/__init__.py
  op_experimental/rasterize.py
  op_experimental/focal.py
  op_experimental/network.py
)


add_custom_target(init_campo_sources ALL
  DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/dataframe.py
  DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/op_fields/operations.py
  DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/op_fieldagents/operations.py
  DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/op_experimental/__init__.py
)

add_custom_command(
  OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/dataframe.py
  DEPENDS ${SOURCES}
  WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
  COMMAND ${CMAKE_COMMAND} -E copy ${SOURCES} ${CMAKE_CURRENT_BINARY_DIR}
)

add_custom_command(
  OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/op_fields/operations.py
  DEPENDS ${FIELD_SOURCES}
  WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
  COMMAND ${CMAKE_COMMAND} -E copy_directory op_fields ${CMAKE_CURRENT_BINARY_DIR}/op_fields
)

add_custom_command(
  OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/op_fieldagents/operations.py
  DEPENDS ${FIELDAGENT_SOURCES}
  WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
  COMMAND ${CMAKE_COMMAND} -E copy_directory op_fieldagents ${CMAKE_CURRENT_BINARY_DIR}/op_fieldagents
)

add_custom_command(
  OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/op_experimental/__init__.py
  DEPENDS ${EXPERIMENTAL_SOURCES}
  WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
  COMMAND ${CMAKE_COMMAND} -E copy_directory op_experimental ${CMAKE_CURRENT_BINARY_DIR}/op_experimental
)

install(
  FILES
    ${SOURCES}
    ${CMAKE_CURRENT_BINARY_DIR}/__about__.py
  DESTINATION
    ${CMAKE_BINARY_DIR}/package/campo
)

install(
  FILES
    ${FIELD_SOURCES}
  DESTINATION
    ${CMAKE_BINARY_DIR}/package/campo/op_fields
)

install(
  FILES
    ${FIELDAGENT_SOURCES}
  DESTINATION
    ${CMAKE_BINARY_DIR}/package/campo/op_fieldagents
)

install(
  FILES
    ${EXPERIMENTAL_SOURCES}
  DESTINATION
    ${CMAKE_BINARY_DIR}/package/campo/op_experimental
)
