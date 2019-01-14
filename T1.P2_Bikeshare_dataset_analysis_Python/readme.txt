I have chosen to use the python csv library for this project rather than NumPy/Pandas in order to really understand the benefits of NumPy and Panda later in the course.



I have written and included the following 3 helper functions:
read_file(filename)
filter_for_month(month, row, column)
filter_for_day_in_month(month, day, row, column)

These are in addition to the following 15 functions provided in the template:
get_city()
get_time_period()
get_month()
get_day(month)
popular_month(city_file, time_period='none')
popular_day(city_file, time_period)
popular_hour(city_file, month, day)
trip_duration(city_file, month, day)
popular_stations(city_file, month, day)
popular_trip(city_file, month, day)
users(city_file, month, day)
gender(city_file, month, day)



birth_years(city_file, month, day)



display_data(city_file)
statistics()



I believe that there was some ambiguity in the task. I think the popular_day() function could have been interpreted in 2 ways:

1. Filter the data on a specified day within a specified month, e.g. February 1.
2. Filter on a day of the week, e.g. all the Tuesdays.

I have made the assumption that the requirement was for first version - one day in a month - and have implemented the function in this way.


My code will throw an ValueError Exception if the program cannot interpret the date format.  I have chosen to end the program with a message if this code gets executed.
I have chosen to implement the code like this in case the fact that my settings in the UK cause an issue with a review in the US.




I have used the following resources to help me in my coding.


14.1. csv — CSV File Reading and Writing
https://docs.python.org/3/library/csv.html#id3

8. Data Types
8.1.8. strftime() and strptime() Behavior¶
https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior

Using Counter module for birth year question
https://stackoverflow.com/questions/2600191/how-to-count-the-occurrences-of-a-list-item

Getting greatest count from counter
https://www.robjwells.com/2015/08/python-counter-gotcha-with-max/

help for the display() function
https://stackoverflow.com/questions/21594302/is-there-a-way-to-remember-the-position-in-a-python-iterator

help for the display() function
https://stackoverflow.com/questions/44689546/how-to-print-out-a-dictionary-nicely-in-python

help for the displaying the duration function in hours/mins/secs
https://stackoverflow.com/questions/21520105/how-to-convert-seconds-into-hhmmss-in-python-3-x