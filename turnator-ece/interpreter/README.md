## Defining and Calling Functions

1.  Work through the explanation in the slides (and chapter)
    of how to define a function in our little language
    and then how to call one.
    
    DONE
    
2.  Look at the documentation for Python's `ChainMap` class
    and modify the implementation from the slides to use that
    to manage environments.
    
    NOT DONE

## Arrays

Implement fixed-size one-dimensional arrays:

1.  `["array", 10]` creates an array of 10 elements.
    (If you want to assign it to a variable you could use `["set", "var", ["array", 10]]`.)
    
    def do_get (array, index):
        assert len(index)==0
        assert isinstance(array[0], str)
        return ???
        
    def do_set(array, index):
        assert len(index)==1
        assert isinstance(index
        
        SORRY -- will look at what others have done
        
        
2.  Other instructions that you design get and set array elements by index.

## While Loops

Implement a `while` loop instruction.
Your implementation can use either a Python `while` loop or recursion.
