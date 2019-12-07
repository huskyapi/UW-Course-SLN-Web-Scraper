# Notes
```python
`parser.add_argument(arg, type=fn)

def fn(arg):
  if (arg != 'foo'):
    raise argparse.ArgumentTypeError(msg)
``` 

 you can print an custom error message with `argparse` when validating arguments. handy!

