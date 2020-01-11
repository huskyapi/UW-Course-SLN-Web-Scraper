

**GOAL**: Have a way to collect useful historical data about courses in the UW Time Schedule.

# Notes
```python
parser.add_argument(arg, type=fn)

def fn(arg):
  if (arg != 'foo'):
    raise argparse.ArgumentTypeError(msg)
```

You can print an custom error message with `argparse` when validating arguments. handy!

                         
# Motivating Questions

* How often is a course offered? With what instructors?

Useful for schedule planning. If a class has always been offered in winter quarter, it is reasonable to plan your schedule with the expectation that you can take it during that quarter.

* How have course times changed over time?

Not intended for being used for registration bots, but for exploratory data analysis and helping people decide on course schedules.
Might be useful for predicting trends in when people tend to register for classes.

* Collecting time series data