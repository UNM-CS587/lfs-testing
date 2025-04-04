from lfs import *
import os

def test_create_empty_file():
    # Remove any journal if it already exists
    try:
        os.remove("lfstest.log")
    except FileNotFoundError:
        pass

    # Use LFS_Log to create a new journal
    l = LFS_Log("lfstest.log")

    # Create an empty regular file in the root directory
    l.creat(0, LFS_REGULAR_FILE, "empty.txt")

    # Make sure we can look it up
    fnum = l.lookup(0, "empty.txt")
    assert fnum > 0
 
    # Stat the file and see if its type and size are right
    type, size = l.stat(fnum)
    assert type == LFS_REGULAR_FILE
    assert size == 0

    # release the log object 
    l = None

def test_create_directory()
    # Open the existing log
    l = LFS_Log("lfstest.log")

    # Create an empty directory in the root directory
    l.creat(0, LFS_DIRECTORY, "testdir")
    
    # Look up the empty directory
    fnum = l.lookup(0, "testdir")
    assert fnum > 0

    # Check the inodes in the empty directory
    fnum1 = l.lookup(fnum, ".")
    assert fnum1 == fnum

    # Check the inodes in the empty directory
    fnum2 = l.lookup(fnum, "..")
    assert fnum2 == 0

    # Stat the root directory
    type, size = l.stat(fnum)

    # It should be a directory
    assert type == LFS_DIRECTORY

    # Still with one block of entries
    assert size == 4096

def test_create_long_name():
    # Open the existing log
    l = LFS_Log("lfstest.log")

    # Create a file with a long name
    try: 
        l.creat(0, LFS_REGULAR_FILE, "thisnameistoolongforcreatetosucceedwithitshouldfail.txt")
    except:
        pass
    else:
        raise AssertionError("LFS_Creat did not fail with a name that was too long.");

def test_create_duplicate_name():
    # Open the existing log
    l = LFS_Log("lfstest.log")

    # Try to create a duplicate ".". THIS SHOULD SUCCEED but not actually 
    # make a duplicate
    l.creat(0, LFS_DIRECTORY, ".")

    # Now read the directory contents directly
    bytes = l.read(0, 0)

    # The returned root directory should have only one '.' in it.
    numdot = 0
    for i in range(0,128):
        str = bytes[i*32:i*32+28].split(b'\x00')[0].decode('utf-8')
        print str
        if str == ".":
            numdot++
    assert numdot == 1
