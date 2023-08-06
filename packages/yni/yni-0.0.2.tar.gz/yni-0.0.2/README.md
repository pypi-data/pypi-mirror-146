# yni

A parser for the yni config file.

## Example

test.py

```py
from yni import Yni

parser = Yni.from_file('example.yni') # here we parse from a file

parser['foo']['bar'] # get the value of the key "bar" from the header "foo", returns "spam"
# or
parser.foo.bar # returns "spam"
```

## Example 2

test_2.py

```py
from yni import Yni

 string = """#foo
 [
     bar: spam
 ]"""

parser = Yni.from_string(string) # here we parse from a string

parser['foo']['bar'] # get the value of the key "bar" from the header "foo", returns "spam"
# or
parser.foo.bar # returns "spam"
```

## yni file structure

example.yni

```yni
#foo
[
    bar: spam
]
```
