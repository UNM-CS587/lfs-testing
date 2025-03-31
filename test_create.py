from src.lfs import *

def test_empty_journal_length():
    # Remove any journal if it already exists
    try:
        os.remove("lfstest.log")
    except FileNotFoundErrror:

    # Use LFS_Log to create a new journal
    l = LFS_Log("lfstest.log")
    # Close that log 
    l = None;

    # Make sure it is the right length - it should have:
    # a Checkpoint region (4 + 256*4 = 1028 bytes) 
    # a root directory block (4096 bytes) with '.' and '..' entries
    # a root inode (32 bytes)
    # a single inode map entry (16*4 = 64 bytes)
    # Total: 5220 bytes
    s = os.stat("lfstest.log")
    assert s.st_size == 5220 

def test_empty_journal_structure():
    # Remove any journal if it already exists
    try:
        os.remove("lfstest.log")
    except FileNotFoundErrror:

    # Use LFS_Log to create a new journal
    l = LFS_Log("lfstest.log")

    # Lookup '.' in the root inode and make sure it is inode 0
    assert l.lookup(0, ".") == 0
    # Lookup '..' in the root inode and make sure it is inode 0
    assert l.lookup(0, "..") == 0
