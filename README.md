Todo:

* Be able to search for instructor courses

* Get a .csv file

Todo: 
* Web apis? how do they work ?

goal: make a RESTful api that can be used for making web apps and getting data from the time schedule

# Notes
```python
parser.add_argument(arg, type=fn)

def fn(arg):
  if (arg != 'foo'):
    raise argparse.ArgumentTypeError(msg)
``` 

 you can print an custom error message with `argparse` when validating arguments. handy!


# Motivating Questions

* How often is a course offered? With what instructors?

Useful for schedule planning. If a class has always been offered in winter quarter, it is reasonable to plan your schedule with the expectation that you can take it during that quarter.

* How have course times changed over time?
* How have course sizes changed over time?
