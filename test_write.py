from lfs import *
import os

def test_single_write():
    # Remove any journal if it already exists
    try:
        os.remove("lfstest.log")
    except FileNotFoundError:
        pass

    # Use LFS_Log to create a new journal
    l = LFS_Log("lfstest.log")

    # Create an empty file in the root directory and look it up
    l.creat(0, LFS_REGULAR_FILE, "testfile.bin")
    fnum = l.lookup(0, "testfile.bin")
    assert fnum > 0

    # Stat the file and check its length
    type, size = l.stat(fnum)
    assert type == LFS_REGULAR_FILE
    assert size == 0

    # Create a 4k byte array to write to the file
    b = bytearray(4096)
    for i in range(4096):
        b[i] = (4096 - i) & 0xff

    # Write it to the file
    l.write(fnum, 0, b)

    # Stat the file and check its length
    type, size = l.stat(fnum)
    assert type == LFS_REGULAR_FILE
    assert size == 4096

    # Close the log
    l = None

def test_invalid_write():
    # Use LFS_Log to open the existing log
    l = LFS_Log("lfstest.log")

    fnum = l.lookup(0, "testfile.bin")
    assert fnum > 0
    
    # Create a 4k byte array to write to the file
    b = bytearray(4096)
    for i in range(4096):
        b[i] = (4096 - i) & 0xff

    # Write to invalid inode number
    try:
        l.write(514, 0, b)
    except:
        pass
    else:
        raise AssertionError("Write to invalid inode number did not throw an exception")

    # Write to invalid block number
    try:
        l.write(fnum, 15, b)
    except:
        pass
    else:
        raise AssertionError("Write to invalid inode number did not throw an exception")

def test_single_read():
    # Use LFS_Log to open the existing log
    l = LFS_Log("lfstest.log")

    # Read back the written block
    fnum = l.lookup(0, "testfile.bin")
    assert fnum > 0
    b = l.read(fnum, 0)

    # Check its length and contents
    assert len(b) == 4096
    for i in range(4096):
        assert b[i] == (4096 - i) & 0xff

    # Close the log 
    l = None;

def test_second_write():
    # Use LFS_Log to open the existing log
    l = LFS_Log("lfstest.log")

    # Write a second block to the file
    fnum = l.lookup(0, "testfile.bin")
    assert fnum > 0
    
    # Create a 4k byte array to write to the file
    b = bytearray(4096)

    for i in range(4096):
        b[i] = (4096 - i) & 0xff
    # Write it to the file
    l.write(fnum, 1, b)

    # Stat the file and check its length
    type, size = l.stat(fnum)
    assert type == LFS_REGULAR_FILE
    assert size == 8192

    # Close the log 
    l = None;

# Now write to the *fourth* block of the file, skipping the third
def test_skip_write():
    # Use LFS_Log to open the existing log
    l = LFS_Log("lfstest.log")

    # Write a second block to the file
    fnum = l.lookup(0, "testfile.bin")
    assert fnum > 0
    
    # Create a 4k byte array to write to the file
    b = bytearray(4096)

    for i in range(4096):
        b[i] = (4096 - i) & 0xff
    # Write it to the file
    l.write(fnum, 3, b)

    # Stat the file and check its length. It should be 
    # *4* blocks long
    type, size = l.stat(fnum)
    assert type == LFS_REGULAR_FILE
    assert size == 16384

    # Close the log 
    l = None;


# Test skip read - see what happens if we read from a skipped interior
# block in a file. 
def test_skip_read():
    # Use LFS_Log to open the existing log
    l = LFS_Log("lfstest.log")

    fnum = l.lookup(0, "testfile.bin")
    assert fnum > 0
    
    # Block 2 hasn't been written but should still be in the file
    # since its inside the length. Read should return 4096 bytes of 0
    b = l.read(fnum, 2, b)
    assert len(b) == 4096
    for i in range(4096):
        assert b[i] == 0 

    # Close the log 
    l = None;
