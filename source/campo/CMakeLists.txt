set(SOURCES
  __init__.py
  areas.py
  dataframe.py
  dataset.py
  points.py
  utils.py

)


add_custom_target(init_campo_sources ALL
  DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/dataframe.py
)


add_custom_command(
  OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/dataframe.py
  DEPENDS ${SOURCES}
  WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
  COMMAND ${CMAKE_COMMAND} -E copy ${SOURCES} ${CMAKE_CURRENT_BINARY_DIR}
  COMMENT "Copying sources..."
)


install(
  FILES
    ${SOURCES}
  DESTINATION
    ${CMAKE_BINARY_DIR}/package/campo
)
