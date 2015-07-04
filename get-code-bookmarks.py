#!/usr/bin/env python3

"""
get-code-bookmarks.py

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
        ejmr@plutono.com
        https://github.com/ejmr/get-code-bookmarks

License: GPLv3

"""

import argparse
import sys
import sqlite3

from operator import itemgetter

VERSION = "2.3.0"

# This is set in the main logic.
arguments = None

# This is a list of terms we search for in bookmark titles and URLs to
# try and find relevant links to share.
search_terms = [
    "6502",
    "ada",
    "algebra",
    "algorithm",
    "amiga",
    "android",
    "api",
    "arm",
    "assembly",
    "bazaar",
    "beos",
    "bitbucket",
    "bsd",
    "c++",
    "calculus",
    "clang",
    "clojure",
    "code",
    "coding",
    "coffeescript",
    "commodore 64",
    "cpu",
    "darcs",
    "database",
    "directx",
    "dos",
    "emacs",
    "erlang",
    "factor",
    "forth",
    "framework",
    "geometry",
    "git",
    "glsl",
    "gnome",
    "gnu",
    "golang",
    "gpu",
    "guile",
    "haskell",
    "html",
    "http",
    "java",
    "javascript",
    "jdk",
    "jvm",
    "kde",
    "linux",
    "lisp",
    "llvm",
    "lua",
    "macro",
    "math",
    "mercurial",
    "micro",
    "mips",
    "mozilla",
    "mssp",
    "mud",
    "mush",
    "mvc",
    "node",
    "objective-c",
    "ocaml",
    "opengl",
    "perl",
    "program",
    "python",
    "qt",
    "racket",
    "redis",
    "rfc"
    "ruby",
    "rust",
    "scheme",
    "sdl",
    "shader",
    "shell",
    "smalltalk",
    "sourceforge",
    "sql",
    "standardml",
    "subversion",
    "svn",
    "swift",
    "tex",
    "trigonometry",
    "unix",
    "vim",
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

    if arguments.title_only == True:
        where_clauses = ["moz_bookmarks.title like '%{0}%'".format(term)
                         for term in terms]
    else:
        where_clauses = ["moz_bookmarks.title like '%{0}%' or moz_places.url like '%{0}%'".format(term)
                         for term in terms]

    return base_query + " where " + " or ".join(where_clauses) + ";"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lists programming bookmarks.")
    parser.add_argument("database", type=str, help="Location of places.sqlite file")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s {0}".format(VERSION))
    parser.add_argument("--terms", nargs="*", type=str, default=[], help="Specific terms to search for in bookmarks")
    parser.add_argument("-o", "--output", type=str, default="normal",
                        choices=["normal", "markdown", "bbcode", "html"],
                        help="The output format for the links")
    parser.add_argument("-c", "--count", action="store_true", help="Prints a count of the bookmarks")
    parser.add_argument("--title-only", action="store_true", help="Search only bookmark titles, not URLs")

    arguments = parser.parse_args()
    database = sqlite3.connect(arguments.database)
    bookmark_count = 0

    if len(arguments.terms) > 0:
        terms = arguments.terms
    else:
        terms = search_terms

    try:
        query = database.cursor()
    except sqlite3.OperationalError:
        sys.exit("Error: {0} does not look like a valid places.sqlite file".format(arguments.database))

    if arguments.output == "html":
        print("<ul>")

    for row in sorted(query.execute(build_search_query(terms)), key=itemgetter(0)):
        bookmark_count = bookmark_count + 1
        if arguments.output == "markdown":
            print("[{0}]({1})\n".format(row[0], row[1]))
        elif arguments.output == "bbcode":
            print("[url={1}]{0}[/url]\n".format(row[0], row[1]))
        elif arguments.output == "html":
            print("<li><a href=\"{1}\">{0}</a></li>".format(row[0], row[1]))
        elif arguments.output == "normal":
            print("{0}\n\t{1}\n".format(row[0], row[1]))

    if arguments.output == "html":
        print("</ul>")

    if arguments.count == True:
        print("Total Bookmarks: {0}".format(bookmark_count), file=sys.stderr)
