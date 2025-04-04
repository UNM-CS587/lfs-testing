from lfs import *
import os

# Stress tests on various LFS edge cases. All of these start from an empty log
def test_fill_directory():
    # Remove any journal if it already exists
    try:
        os.remove("lfstest.log")
    except FileNotFoundError:
        pass

    # Use LFS_Log to create a new journal
    l = LFS_Log("lfstest.log")

    # Fill up the root directory with empty files. All of these
    # should succeed.
    for i in range(0, 13*128 - 2):
        l.creat(0, LFS_REGULAR_FILE, "file{0}.txt".format(i))

    # Make sure they were all created.
    fnum_prev = 0
    for i in range(0, 13*128 - 2):
        fnum = l.lookup(0, "file{0}.txt".format(i))
        assert fnum > 0
        assert fnum != fnum_prev
        fnum_prev = fnum

    # Stat the root directory and see its size is right
    type, size = l.stat(0)
    assert size == (4096 * 13)

    # release the log object 
    l = None

def test_directory_tree():
    # Remove any journal if it already exists
    try:
        os.remove("lfstest.log")
    except FileNotFoundError:
        pass

    # Use LFS_Log to create a new journal
    l = LFS_Log("lfstest.log")

    # Start at the root and create a string of nested directories
    pdir = 0
    for i in range(0, 200):
        name = "dir{0}".format(i)
        l.creat(pdir, LFS_DIRECTORY, name)
        dir = l.lookup(pdir, name)
        assert dir > 0
        assert dir != pdir
        pdir = dir

    # Start at bottom and walk back .., making sure we end up at root
    pdir = 0
    for i in range(0, 200):
        name = "dir{0}".format(i)
        pdir = l.lookup(pdir, "..")
    assert pdir == 0
    
    # release the log object 
    l = None
