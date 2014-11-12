Git-based Courses talk slides
=============================
This project is intended to supply a convenient development environment for the
"Git-based Courses" talk which will be presented at the 2014 Open edX conference
by Carson Gee and Peter Pinch.


How to build
------------
1. Install the requirements: `pip install -r requirements.txt`
2. Run the build script: `python deckgen.py build`
3. To view the slide decks, navigate to the **decks** directory using a modern
   browser.


How it works
------------
There are three important directories: **markdown**, **decks**, and **assets**.

- **markdown** contains the source markdown files.
- **decks** contains the resulting HTML slide decks.
- **assets** contains assets used by the slide decks.

When building a slide deck, the build script just takes the markdown file from
the **source** directory, inserts it into the **template.html** file, and saves
the result in the **decks** directory. That is all.


Using the watcher
-----------------
There is a filesystem watcher utility included in **deckgen.py** that can listen
for changes to markdown files and convert them on the fly. *This is convenient
when editing slide decks.*

It can be started by running `deckgen.py watch`.


deckgen.py --help
-----------------
```
Standalone slide deck collection builder.

Usage:
  deckgen.py build [-s SRC] [-d DEST] [-t TEMP] [NAME...]
  deckgen.py watch [-s SRC] [-d DEST] [-t TEMP]
  deckgen.py -h | --help

Arguments:
  name   The name of a slide deck to generate. Accompanying markdown should be
  located in the source directory. For example, if the markdown file is
  named "slides.md", the name "slides" should be passed.
  If no names are passed, the default behavior is to run against ALL
  markdown files in the source directory

Options:
  -h --help               Show this help screen.
  -s --source=SRC         Source markdown directory [default: markdown].
  -d --destination=DEST   Destination HTML directory [default: decks].
  -t --template=TEMP      HTML template to use [default: template.html].
```
