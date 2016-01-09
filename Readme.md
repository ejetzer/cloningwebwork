# Exercise generator

This is a complete recode of something I've already done.
The original (somewhat working) code can be found in the
[original repository][github].
This version will be using a lot more of Python's builtin modules,
keeping me from making overcomplicated things.

[github]: http://github.com/ejetzer/cloningwebwork-old

# Error propagation

* Rounding errors
* Sign errors
* Exercise specific errors

## Specific problems

* Large size of the list of wrong answers

# Exercise templates

* Markdown base, based on the Python [Markdown module][md].
* Python functions
* Template configuration, using the Python [builtin class][temp].

[md]: https://pypi.python.org/pypi/Markdown
[temp]: https://docs.python.org/2/library/string.html#template-strings

# AJAX client

* Page templates? Gonna use [Django][django]
* Javascript library, based on [JQuery][jq]

[django]: https://www.djangoproject.com/
[jq]: http://jquery.org

# Exercise server

Probably based on one of Python's numerous asynchronous server libraries.

* Login?
* Caching
