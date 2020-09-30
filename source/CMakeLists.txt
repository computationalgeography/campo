add_subdirectory(campo)
add_subdirectory(test)



configure_file(setup.py.in
  setup.py
)

install(
  FILES
    ${CMAKE_CURRENT_BINARY_DIR}/setup.py
    ${CMAKE_SOURCE_DIR}/README.md
  DESTINATION
    ${CMAKE_BINARY_DIR}/package
)

install(CODE "execute_process(COMMAND ${Python3_EXECUTABLE} setup.py sdist bdist_wheel
                              WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/package)")








#
#
# message(STATUS "))))))))))))))))0" ${CMAKE_CURRENT_SOURCE_DIR}/campo)
# message(STATUS "))))))))))))))))0" ${CMAKE_CURRENT_BINARY_DIR}/campo)


# add_custom_command(
#   TARGET init_sources
#   ALL #POST_BUILD
#   COMMAND ${CMAKE_COMMAND} -E copy_directory
#     ${CMAKE_CURRENT_SOURCE_DIR}/campo
#     ${CMAKE_CURRENT_BINARY_DIR}/campo
# )

# add_custom_target(
#   init_source
#   ALL
#   COMMAND ${CMAKE_COMMAND} -E copy_directory
#     ${CMAKE_CURRENT_SOURCE_DIR}/campo
#     ${CMAKE_CURRENT_BINARY_DIR}/campo
# )
