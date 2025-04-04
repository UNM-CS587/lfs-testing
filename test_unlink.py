from lfs import *
import os

def test_unlink_empty_file():
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
 
    # Now unlink the file in the root dirctory
    l.unlink(0, "empty.txt")

    # Make sure we can look it up
    try:
        fnum = l.lookup(0, "empty.txt")
    except: 
        pass
    else:
        raise AssertionError("Was able to lookup unlinked file.")

    # release the log object 
    l = None

def test_unlink_empty_directory():
    l = LFS_Log("lfstest.log")

    # Create an empty directory in the root directory
    l.creat(0, LFS_DIRECTORY, "emptydir")

    # Make sure we can look it up
    fnum = l.lookup(0, "emptydir")
    assert fnum > 0
 
    # Now unlink the directory in the root dirctory
    l.unlink(0, "emptydir")

    # Make sure we cannot look it up
    try:
        fnum = l.lookup(0, "emptydir")
    except: 
        pass
    else:
        raise AssertionError("Was able to lookup unlinked directory.")

    # release the log object 
    l = None

def test_unlink_nonempty_directory():
    l = LFS_Log("lfstest.log")

    # Create an empty directory in the root directory
    l.creat(0, LFS_DIRECTORY, "emptydir")

    # Make sure we can look it up
    fnum = l.lookup(0, "emptydir")
    assert fnum > 0
 
    # Now make a file in the empty directory
    l.creat(fnum, LFS_REGULAR_FILE, "empty.txt")

    # Now try to unlink the directory in the root dirctory
    try:
        l.unlink(0, "emptydir")
    except: 
        pass
    else:
        raise AssertionError("Was able to unlink non-empty directory.")

def test_unlink_nonexistent_file():
    l = LFS_Log("lfstest.log")
    l.creat(0, LFS_REGULAR_FILE, "empty.txt")
    l.unlink(0, "empty.txt")
    l.unlink(0, "empty.txt") # This should succeed to ensure idempotency
