from lfs import *
import os

def test_empty_journal_length():
    # Remove any journal if it already exists
    try:
        os.remove("lfstest.log")
    except FileNotFoundError:
        pass

    # Use LFS_Log to create a new journal
    l = LFS_Log("lfstest.log")
    # Close that log 
    l = None;

    # Make sure it is the right length - it should have:
    # a Checkpoint region (4 + 256*4 = 1028 bytes) 
    # a root directory block (4096 bytes) with '.' and '..' entries
    # a root inode (64 bytes)
    # a single inode map entry (16*4 = 64 bytes)
    # Total: 5252 bytes
    s = os.stat("lfstest.log")
    assert s.st_size == 5252 

def test_root_directory_contents():
    # Use LFS_Log to open existing journal
    l = LFS_Log("lfstest.log")

    # Lookup '.' in the root inode and make sure it is inode 0
    assert l.lookup(0, ".") == 0

    # Lookup '..' in the root inode and make sure it is inode 0
    assert l.lookup(0, "..") == 0

def test_root_directory_stat():
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
