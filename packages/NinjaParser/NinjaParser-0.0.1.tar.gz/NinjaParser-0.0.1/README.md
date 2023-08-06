# NinjaParser
`NinjaParser` is a Python module to parse `.ninja_log` files and print build times.

If you have been complaining about long build times you may have switched to `ninja` from `make`. If not, you should give it a [try](https://ninja-build.org/). 
Along with being faster, `ninja` also provides a log file, `.ninja_log` containing timings for each built object. 
This information can be helpful to understand the bottlenecks in your building process. However, this file needs to be parsed to be comprehensible.
`NinjaParser` prints a sorted list of built times with percentages for the top ten
objects.
