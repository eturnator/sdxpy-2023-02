# A Testing Framework: Exercises

## Looping Over `globals`

What happens if you run:

```python
for name in globals():
    print(name)
```

## Ece Answer: Prints global functions

What happens if you run:

```python
name = None
for name in globals():
    print(name)
```

## Ece answer: Prints same, does not alter names of functions in globals() dict.

Why?

## Ece answer: Copy because we want to separate the value in memory of the copy of globals() from the actual dicionary so we can add to it but not alter the existing dict.

## Counting Results

1.  Modify the test framework so that it reports which tests passed, failed, or had errors
    and also reports a summary of how many tests produced each result.
    
    ##Ece Answer:
    
    def run_tests(all_tests):
    results = {"pass": 0, "fail": 0, "error": 0}
    for test in all_tests:
        try:
            test()
            results["pass"] += 1
        except AssertionError:
            results["fail"] += 1
        except Exception:
            results["error"] += 1
    print(f"pass {results['pass']}")
    print(f"fail {results['fail']}")
    print(f"error {results['error']}")

    run_tests(TESTS)

2.  Write unit tests to check that your answer to part 1 works correctly.

    TESTS = [
   "pass",
    "fail",
    "error",
    ]

3.  Think of another plausible way to interpret part 1
    that *wouldn't* pass the tests you wrote for part 2.
    
  Ece answer: The tests above need to be placed in a list and so they don't run independently of the list. If the AssertionError is called when the result key is "fail" or "error".

## Failing on Purpose

Putting assertions into code to check that it is behaving correctly
is called __defensive programming__.
It's a good practice,
but we should make sure those assertions are failing when they're supposed to,
just as we should test our smoke detectors every once in a while.

Modify the tester so that
if a test function's docstring is `"test:assert"`,
the test passes if it raises an `AssertionError`
and fails if it does not.
Tests whose docstring don't contain `"test:assert"`
should behave as before.

---

class: exercise

## Setup and Teardown

Testing frameworks often allow programmers to specify a `setup` function
that is to be run before each test
and a corresponding `teardown` function
that is to be run after each test.
(`setup` usually re-creates complicated test fixtures,
while `teardown` functions are sometimes needed to clean up after tests,
e.g., to close database connections or delete temporary files.)

Modify the testing tool in this chapter so that
if a file of tests contains a function called `setup`
then the tool calls it exactly once before running each test in the file.
Add a similar way to register a `teardown` function.
