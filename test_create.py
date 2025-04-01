from lfs import *

def test_create_empty_file():
    # Remove any journal if it already exists
    try:
        os.remove("lfstest.log")
    except FileNotFoundErrror:
        pass

    # Use LFS_Log to create a new journal
    l = LFS_Log("lfstest.log")

    # Create an empty regular file in the root directory
    fnum1 = l.creat(0, LFS_REGULAR_FILE, "empty.txt")
    assert fnum1 > 0

    # Look it up and make sure inode numbers match
    fnum2 = l.lookup(0, "empty.txt")
    assert fnum1 == fnum2
 
    # release the log object 
    l = None

def test_stat_empty_file():
    # Open the existing log
    l = LFS_Log("lfstest.log")

    # Look it the still existing empty file
    fnum = l.lookup(0, "empty.txt")
    assert fnum > 0

    # Stat the file and see if its type and size are right
    type, size = l.stat(fnum)
    assert type == LFS_REGULAR_FILE
    assert size == 0

    # Release the log
    l = None

def test_directory_size():
    # Open the existing log
    l = LFS_Log("lfstest.log")
    
    # Stat the root directory
    type, size = l.stat(0)

    # It should be a directory
    assert type == LFS_DIRECTORY

    # Still with one block of data
    assert size == 4096

    # Release the log
    l = None
