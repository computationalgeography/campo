add_subdirectory(campo)
add_subdirectory(test)



configure_file(setup.py.in
  setup.py
)

configure_file(campo.yaml.in
  ${CMAKE_SOURCE_DIR}/environment/conda/campo.yaml
)

configure_file(campo.yaml.in
  ${CMAKE_BINARY_DIR}/documentation/campo.yaml
)


if(CAMPO_BUILD_WHEEL)

  install(
    FILES
      ${CMAKE_CURRENT_BINARY_DIR}/setup.py
      ${CMAKE_SOURCE_DIR}/README.md
    DESTINATION
      ${CAMPO_INSTALL_DIR}
  )

  install(CODE "execute_process(COMMAND ${Python3_EXECUTABLE} setup.py sdist bdist_wheel
                                WORKING_DIRECTORY ${CAMPO_INSTALL_DIR}")
endif()
