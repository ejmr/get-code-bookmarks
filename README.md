get-code-bookmarks
==================

This is a simple [Python](http://python.org) script for extracting
programming-related bookmarks from [Firefox](http://firefox.com/), or
browsers based on the same engine, such as my preferred browser
[Conkeror](http://conkeror.org/).  Run `./get-code-bookmarks.py
--help` to see the command-line options (described below).  And see
the comment at the beginning of the script for a more detailed
explanation of the program.


Usage
-----

The simple way to run the program is

    ./get-code-bookmarks.py database

where `database` is the path to the `places.sqlite` file for your
browser.  Firefox places this file in your ‘profile’ directory, as do
other browsers based on Firefox.  For example, mine is in the
directory `~/.conkeror.mozdev.org/conkeror/k12o14s2.default/`.
So you will want to search for something like that.

Running the program like so will print out all of the bookmarks where
either the title or the URL match any words inside of the
`search_terms` list in the code.  So if you want to add extra search
terms to the program, that is where you can put them.

You can also specify search terms on the command-line.  This is useful
if you want to restrict your search to a certain set of terms, or
search for a term that is not part of the built-in list.  You can do
this with the `--terms` option like so:

    ./get-code-bookmarks.py database --terms lua game 2d

This will limit the results to only those links containing any of
those three terms.  You should place `--terms` *after* the path to
your `places.sqlite` file, otherwise the program will try to treat the
SQLite file as a search term and then give you an error about failing
to provide the required database.

The default output format looks like this:

    Bookmark Title
        <URL for the Bookmark>

If you provide the `--markdown` option the output will look like this
instead:

    [Bookmark Title](URL for the Bookmark)

Or you can use the `--bbcode` option  to get output like:

    [url=Bookmar Title]URL for the Bookmark[/url]

The `--normal` option produces the default output, but it is not
necessary to use that argument except when you need to be explicit.
The three output options are mutually exclusive.


License
-------

Public Domain
