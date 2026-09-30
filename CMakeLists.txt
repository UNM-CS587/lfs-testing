# We actually implement all tests in Python, and so use pytest

# Relies on the pytest-cmake package being installed in python
# typically via `pip install pytest-cmake --user`

# Use the Pytest Cmake package to handle discovering and running python tests
# REQUIRED because without it a missing pytest-cmake configures cleanly and
# `make test` then reports success having run no tests at all.
find_package(Pytest REQUIRED)

if (ENABLE_LFS_C_LIBRARY)
    pytest_discover_tests(
        LFSTest
        LIBRARY_PATH_PREPEND
            $<TARGET_FILE_DIR:lfs>
        PYTHON_PATH_PREPEND
            $<TARGET_FILE_DIR:lfs>
        TRIM_FROM_NAME "^test_"
        DEPENDS lfs
    )
else (ENABLE_LFS_C_LIBRARY)
    pytest_discover_tests(
        LFSTest
        PYTHON_PATH_PREPEND
            ${CMAKE_CURRENT_BINARY_DIR}/../src
        TRIM_FROM_NAME "^test_"
    )
endif (ENABLE_LFS_C_LIBRARY)
