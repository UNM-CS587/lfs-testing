from lfs import *
import os

# Basic lookup correctness is tested in test_create. This checks an error
# condition.
def test_lookup_invalid_inode():
    # Remove any journal if it already exists
    try:
        os.remove("lfstest.log")
    except FileNotFoundError:
        pass

    # Use LFS_Log to create a new journal
    l = LFS_Log("lfstest.log")

    try:
        l.lookup(2, ".")
    except:
        pass
    else:
        raise AssertionError("Lookup on an invalid inode did not fail.")

# Basic stat correctness is tested in test_create. This checks an error
# condition.
def test_stat_invalid_inode():
    # Use LFS_Log to open the journal
    l = LFS_Log("lfstest.log")

    try:
        l.stat(2)
    except:
        pass
    else:
        raise AssertionError("Stat on an invalid inode did not fail.")

# Basic read correctness is tested in test_create. This checks an error
# condition.
def test_read_invalid_inode():
    # Use LFS_Log to open the journal
    l = LFS_Log("lfstest.log")

    try:
        l.read(2, 0)
    except:
        pass
    else:
        raise AssertionError("Read on an invalid inode did not fail.")

# Basic read correctness is tested in test_create. This checks an error
# condition.
def test_read_past_file_end():
    # Use LFS_Log to open the journal
    l = LFS_Log("lfstest.log")

    try:
        l.read(0, 4)
    except:
        pass
    else:
        raise AssertionError("Read on a block past end of file did not fail.")

# Basic read correctness is tested in test_create. This checks an error
# condition.
def test_read_before_file_begin():
    # Use LFS_Log to open the journal
    l = LFS_Log("lfstest.log")

    try:
        l.read(0, -1)
    except:
        pass
    else:
        raise AssertionError("Read on a negative block number did not fail.")
