from lfs import *
import os
import pytest

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

    # Lookup on an invalid inode must fail
    with pytest.raises(LFSError):
        l.lookup(2, ".")

# Basic stat correctness is tested in test_create. This checks an error
# condition.
def test_stat_invalid_inode():
    # Use LFS_Log to open the journal
    l = LFS_Log("lfstest.log")

    # Stat on an invalid inode must fail
    with pytest.raises(LFSError):
        l.stat(2)

# Basic read correctness is tested in test_create. This checks an error
# condition.
def test_read_invalid_inode():
    # Use LFS_Log to open the journal
    l = LFS_Log("lfstest.log")

    # Read on an invalid inode must fail
    with pytest.raises(LFSError):
        l.read(2, 0)

# Basic read correctness is tested in test_create. This checks an error
# condition.
def test_read_past_file_end():
    # Use LFS_Log to open the journal
    l = LFS_Log("lfstest.log")

    # Read on a block past the end of the file must fail
    with pytest.raises(LFSError):
        l.read(0, 4)

# Basic read correctness is tested in test_create. This checks an error
# condition.
def test_read_before_file_begin():
    # Use LFS_Log to open the journal
    l = LFS_Log("lfstest.log")

    # Read on a negative block number must fail
    with pytest.raises(LFSError):
        l.read(0, -1)
