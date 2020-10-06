add_subdirectory(campo)
add_subdirectory(test)



configure_file(setup.py.in
  setup.py
)

configure_file(environment.yaml.in
  ${CMAKE_SOURCE_DIR}/environment/conda/environment.yaml
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

