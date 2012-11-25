#!/usr/bin/env python3

"""get-code-bookmarks.py [-h] [--terms TERMS ...] [--markdown] database

This program tries to extract all of the programming-related bookmarks
from Firefox, or browsers based on the same platform (e.g. Conkeror).
It requires one argument, which is the path to your `places.sqlite`
file, as that is where the browser stores bookmarks.  Linux users will
find this file in their home directory, most likely under a
`.mozilla/` directory.  For Windows users it is probably in the
`Program Files` directory for the browser, but I am unsure.  In either
case a simple use of a utility like `find` should help you get the
file.

The program will print out all of the bookmarks in a format suitable
for pasting into an email.  That is the reason I wrote this program,
to easily share all of my programming-related bookmarks with friends
and fellow coders on a mailing list.

The other command-line options are described in the `README.md` file
that should accompany this program.  If you do not have it then you
may find the README at the website for the program, listed below.

Here is a useful diagram for understanding the database structure used
by the browser:

    http://people.mozilla.org/~dietrich/places-erd.png

Author: Eric James Michael Ritz
        lobbyjones@gmail.com
        https://github.com/ejmr/get-code-bookmarks

This code is Public Domain.

"""

import argparse
import sys
import sqlite3

from operator import itemgetter

# This is a list of terms we search for in bookmark titles and URLs to
# try and find relevant links to share.
search_terms = [
    "6502",
    "algebra",
    "algorithm",
    "api",
    "arm",
    "assembly",
    "c++",
    "calculus",
    "clang",
    "clojure",
    "code",
    "coding",
    "coffeescript",
    "database",
    "directx",
    "erlang",
    "factor",
    "forth",
    "framework",
    "geometry",
    "glsl",
    "gnu",
    "haskell",
    "http",
    "java",
    "javascript",
    "jdk",
    "jvm",
    "llvm",
    "lua",
    "math",
    "mvc",
    "node",
    "ocaml",
    "objective-c",
    "opengl",
    "perl",
    "program",
    "python",
    "ruby",
    "sdl",
    "shader",
    "smalltalk",
    "standardml",
    "sql",
    "trigonometry",
    "x86",
    "xul",
]

def build_search_query(terms):
    """Returns a string which is the search query for finding bookmarks.
    The function searches through the list of `terms` that we pass to
    it.  We can give the return value of this function directly to the
    execute() function of the database.  The query will select two
    columns: 'title' and 'url'.
    """
    base_query = "select moz_bookmarks.title, moz_places.url \
                  from moz_bookmarks \
                  join moz_places on moz_bookmarks.fk = moz_places.id"

    where_clauses = ["moz_bookmarks.title like '%{0}%' or moz_places.url like '%{0}%'".format(term)
                     for term in terms]

    return base_query + " where " + " or ".join(where_clauses) + ";";

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lists programming bookmarks.")
    parser.add_argument("database", type=str, help="Location of places.sqlite file")
    parser.add_argument("--terms", nargs="*", type=str, default=[], help="Specific terms to search for in bookmarks")
    parser.add_argument("--markdown", default=False, action="store_true", help="Format the output in Markdown")
    arguments = parser.parse_args()

    database = sqlite3.connect(arguments.database)

    if len(arguments.terms) > 0:
        terms = arguments.terms
    else:
        terms = search_terms

    try:
        results = database.cursor().execute(build_search_query(terms))
    except sqlite3.OperationalError:
        sys.exit("Error: {0} does not look like a valid places.sqlite file".format(arguments.database))

    for row in sorted(results, key=itemgetter(0)):
        if arguments.markdown is True:
            print("[{0}]({1})\n".format(row[0], row[1]))
        else:
            print("{0}\n\t{1}\n".format(row[0], row[1]))
