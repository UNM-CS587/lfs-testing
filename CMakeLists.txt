# We actually implemenet all test in Python, and so use pytest 

# Relies on the pytest-cmake package being installed in python
# typically via `pip install pytest-cmake --user`


# Use the Pytest Cmake package to handle discocering and running python tests
find_package(Pytest)

if (ENABLE_LFS_C_LIBRARY)
    pytest_discover_tests(
        LFSTest
        LIBRARY_PATH_PREPEND
            $<TARGET_FILE_DIR:liblfs>
        PYTHON_PATH_PREPEND
            $<TARGET_FILE_DIR:liblfs>
        TRIM_FROM_NAME "^test_"
        DEPENDS liblfs
    )
else (ENABLE_LFS_C_LIBRARY)
    pytest_discover_tests(
        LFSTest
        TRIM_FROM_NAME "^test_"
    )
endif (LFS_C_LIBRARY)
