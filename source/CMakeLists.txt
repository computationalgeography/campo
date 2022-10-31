add_subdirectory(campo)
add_subdirectory(test)



configure_file(setup.py.in
  setup.py
)

install(
  FILES
    ${CMAKE_CURRENT_BINARY_DIR}/setup.py
    ${CMAKE_SOURCE_DIR}/README.md
    ${CMAKE_SOURCE_DIR}/LICENSE.txt
  DESTINATION
    ${CAMPO_INSTALL_DIR}
)

if(CAMPO_BUILD_WHEEL)

  install(CODE "execute_process(COMMAND ${Python3_EXECUTABLE} setup.py sdist bdist_wheel
                                WORKING_DIRECTORY ${CAMPO_INSTALL_DIR})")
endif()

# workaround fttb
add_custom_target(tar_bz2
    COMMAND
        ${CMAKE_COMMAND} -E tar "cjfv" "${CMAKE_BINARY_DIR}/campo-${${PROJECT_NAME}_VERSION}.tar.bz2"
        ${CAMPO_INSTALL_DIR}/campo
        ${CAMPO_INSTALL_DIR}/README.md
        ${CAMPO_INSTALL_DIR}/LICENSE.txt
        ${CAMPO_INSTALL_DIR}/setup.py

    WORKING_DIRECTORY ${CAMPO_INSTALL_DIR}
)
