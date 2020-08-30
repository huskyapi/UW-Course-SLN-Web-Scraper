from utils import validate_campus_name, validate_course_name, validate_quarter_name

print(validate_quarter_name('autumn 2019'))
print(validate_quarter_name('spring 2018'))
print(validate_quarter_name('SPR2019'))

print(validate_course_name('B PHYS121'))
print(validate_course_name('INFO200'))

print(validate_course_name('INFO200')[1])
