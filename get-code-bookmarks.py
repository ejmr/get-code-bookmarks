#!/usr/bin/env python3

"""
get-code-bookmarks <path/to/places.sqlite>

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

Here is a useful diagram for understanding the database structure used
by the browser:

    http://people.mozilla.org/~dietrich/places-erd.png

Author: Eric James Michael Ritz
        Ren@lifesnotsimple.com

This code is Public Domain.
"""

import sys
import sqlite3

# This is a list of terms we search for in bookmark titles and URLs to
# try and find relevant links to share.
search_terms = [
    "program",
    "code",
    "coding",
    "java",
    "perl",
    "python",
    "haskell",
    "erlang",
    "clojure",
    "ruby",
    "javascript",
    "node",
]

def build_search_query():
    """Returns a string which is the search query for finding
    bookmarks.  It incorporates all of the `search_terms` we have
    defined above.  We can give the return value of this function
    directly to the execute() function of the database.  The query
    will select two columns: 'title' and 'url'.
    """
    base_query = "select moz_bookmarks.title, moz_places.url \
                  from moz_bookmarks \
                  join moz_places on moz_bookmarks.fk = moz_places.id"

    where_clauses = ["moz_bookmarks.title like '%{0}%' or moz_places.url like '%{0}%'".format(term)
                     for term in search_terms]

    return base_query + " where " + " or ".join(where_clauses) + ";";

if __name__ == "__main__":

    if len(sys.argv) < 2:
        sys.exit("Missing required argument: Path to places.sqlite file");

    database = sqlite3.connect(sys.argv[1])
    cursor = database.cursor()
    cursor.execute(build_search_query())

    for row in cursor:
        print("{0}\n\t{1}\n".format(row[0], row[1]))
