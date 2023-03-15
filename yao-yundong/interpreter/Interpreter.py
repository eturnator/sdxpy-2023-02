import json
import sys
from collections import ChainMap

def do_add(env, args):
    """Add two values.
    ["add" A B] => A + B
    """
    assert len(args) == 2
    left = do(env, args[0])
    right = do(env, args[1])
    return left + right

# [call]
def do_call(env, args):
    """Call a function.
    ["call" name ...expr...] => env[name](*expr)
    """
    # Set up the call.
    assert len(args) >= 1
    name = args[0]
    values = [do(env, a) for a in args[1:]]

    # Find the function.
    func = env_get(env, name)
    assert isinstance(func, list) and (func[0] == "func")
    params, body = func[1], func[2]
    assert len(values) == len(params)

    # Run in new environment.
    env.append(dict(zip(params, values)))
    result = do(env, body)
    env.pop()

    # Report.
    return result
# [/call]

def do_comment(env, args):
    """Ignore instructions.
    ["comment" "text"] => None
    """
    return None

# [def]
def do_def(env, args):
    """Define a new function.
    ["def" name [...params...] body] => None # and define function
    """
    assert len(args) == 3
    name = args[0]
    params = args[1]
    body = args[2]
    env_set(env, name, ["func", params, body])
    return None
# [/def]

def do_get(env, args):
    """Get the value of a variable from the most recent environment
    or the global environment.
    ["get" name] => env{name}
    """
    assert len(args) == 1 or len(args) == 2
    if len(args) == 1:
        return env_get(env, args[0])
    else:
        index = args[0]
        return env_get(env, args[1][index])

def do_gt(env, args):
    """Strictly greater than.
    ["gt" A B] => A > B
    """
    assert len(args) == 2
    return do(env, args[0]) > do(env, args[1])

def do_if(env, args):
    """Make a choice: only one sub-expression is evaluated.
    ["if" C A B] => A if C else B
    """
    assert len(args) == 3
    cond = do(env, args[0])
    choice = args[1] if cond else args[2]
    return do(env, choice)

def do_leq(env, args):
    """Less than or equal.
    ["leq" A B] => A <= B
    """
    assert len(args) == 2
    return do(env, args[0]) <= do(env, args[1])

def do_neg(env, args):
    """Arithmetic negation.
    ["neq" A] => -A
    """
    assert len(args) == 1
    return -do(env, args[0])

def do_not(env, args):
    """Logical negation.
    ["not" A] => not A
    """
    assert len(args) == 1
    return not do(env, args[0])

def do_or(env, args):
    """Logical or.
    The second sub-expression is only evaluated if the first is false.
    ["or" A B] => A or B
    """
    assert len(args) == 2
    if temp := do(env, args[0]):
        return temp
    return do(env, args[1])

def do_print(env, args):
    """Print values.
    ["print" ...values...] => None # print each value
    """
    args = [do(env, a) for a in args]
    print(*args)
    return None

def do_repeat(env, args):
    """Repeat instructions some number of times.
    ["repeat" N expr] => expr # last one of N
    """
    assert len(args) == 2
    count = do(env, args[0])
    for i in range(count):
        result = do(env, args[1])
    return result

def do_seq(env, args):
    """Do a sequence of operations.
    ["seq" A B...] => last expr # execute in order
    """
    for a in args:
        result = do(env, a)
    return result

def do_set(env, args):
    """Assign to a variable.
    ["seq" name expr] => expr # and env{name} = expr
    """
    assert len(args) == 2 or len(args) == 3
    
    name = args[0]
    
    if len(args) == 2:       
        value = do(env, args[1])
        env_set(env, name, value)
    else:
        assert name in env
        index = args[1]
        value = do(env, args[2])
        env_set(env, name, value, index)
            
    return value

def do_array(env, args):
    """Create fixed-size array.
    ["array", 3] => [None, None, None]
    """
    assert len(args) == 1
    assert isinstance(args[0], int)
    return [None] * args[0]

def do_while(env, args):
    """While loop.
    ["while", A, B] => while A then B
    """   
    assert len(args) == 2
    cond = args[0]
    loop = args[1]
    while do(env, cond):        
        value = do(env, loop)
        
    return value

# Lookup table of operations.
OPERATIONS = {
    name.replace("do_", ""): func
    for (name, func) in globals().items()
    if name.startswith("do_")
}

def do(env, instruction):
    if not isinstance(instruction, list):
        return instruction
    op, args = instruction[0], instruction[1:]
    assert op in OPERATIONS
    return OPERATIONS[op](env, args)

def env_get(env, name, index=None):
    assert isinstance(name, str)
    if name in env:
        if not index:
            return env[name]
        else:
            assert isinstance(index, int)
            assert name in env
            assert 0 < index < len(env[name])
            return env[name][index]
    assert False, f"Unknown variable {name}"
    
def env_set(env, name, value, index=None):
    assert isinstance(name, str)
    if not index:
        env[name] = value
    else:
        assert isinstance(index, int)
        assert name in env
        assert 0 < index < len(env[name])
        env[name][index] = value


ops = ["seq",
["set", "var", ["array", 10]], 
["get", "var"],
["set", "var", 3, 2], 
["get", "var"],
["set", "var", 10, 6]
             ]

def main():
    chain = ChainMap()
    result = do(chain, ops)
    print(f"=> {result}")


if __name__ == "__main__":
    main()
