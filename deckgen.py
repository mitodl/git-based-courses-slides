#!/usr/bin/env python
# Author: Brandon DeRosier <bdero@mit.edu>

"""Standalone slide deck collection builder.

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

"""

import logging
import os
import re
import time

from docopt import docopt
from watchdog.observers import Observer
from watchdog.events import RegexMatchingEventHandler


def src_path(path, deckname):
    """
    Get source file name for a given deck name and path.
    """
    return "{0}.md".format(
        os.path.join(path, deckname)
    )


def dest_path(path, deckname):
    """
    Get destination file name for a given deck name and path.
    """
    return "{0}.html".format(
        os.path.join(path, deckname)
    )


def convert(source, destination, template, decks):
    """
    Convert slide deck markdown files to HTML by passing them through a given
    template.
    """
    # Read template file
    try:
        with open(template) as template_file:
            template_html = template_file.read()
    except IOError:
        logging.critical(
            "Couldn't read template file \"{0}\".. "
            "Are you sure it exists?".format(template)
        )
        exit(1)

    # Convert and save slide decks
    for deck in decks:
        deck_source = src_path(source, deck)
        deck_destination = dest_path(destination, deck)

        try:
            with open(deck_source) as source_file:
                markdown = source_file.read()
        except IOError:
            logging.error(
                "Couldn't read source markdown file \"{0}\".. "
                "Are you sure it exists?".format(deck_source)
            )
            continue

        deck_html = re.sub(
            "\s*{{\s*deck_markdown\s*}}",
            "\n{0}".format(markdown),
            template_html
        )

        try:
            with open(deck_destination, "w") as destination_file:
                destination_file.write(deck_html)
        except IOError:
            logging.error(
                "Couldn't write to destination HTML file \"{0}\".. "
                "Are you sure I have permission to write to it?"
                .format(deck_destination)
            )
            continue

        logging.info(
            "Success:  {0} -> {1}".format(deck_source, deck_destination)
        )


class DeckConversionEventHandler(RegexMatchingEventHandler):
    """
    Match markdown files in the source directory and convert them to HTML files
    in the destination directory by passing them through the template.
    """
    def __init__(self, source, destination, template):
        super(DeckConversionEventHandler, self).__init__(
            regexes=["^{0}/[^\.]*.md$".format(source)],
            ignore_directories=True,
            case_sensitive=True
        )

        self._source = source
        self._destination = destination
        self._template = template

    def do_conversion(self, event):
        """
        Convert the markdown to HTML by passing it through the template.
        """
        deck = event.src_path[len(self._source) + 1:-3]
        convert(self._source, self._destination, self._template, [deck])

    def on_modified(self, event):
        """
        Process modified markdown files.
        """
        self.do_conversion(event)

    def on_created(self, event):
        """
        Process newly created markdown files.
        """
        self.do_conversion(event)


def watch(source, destination, template):
    """
    Watch the source directory for changes until a KeyboardInterrupt is
    encountered.
    """
    observer = Observer()
    event_handler = DeckConversionEventHandler(source, destination, template)
    observer.schedule(event_handler, source, recursive=False)

    logging.info("Starting watcher..")

    try:
        observer.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Keyboard interrupt received; stopping watcher..")
        observer.stop()

    observer.join()


if __name__ == "__main__":
    args = docopt(__doc__)

    destination = args["--destination"]
    source = args["--source"]
    template = args["--template"]
    decknames = args["NAME"]

    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    for path in [source, destination]:
        if not os.path.exists(path):
            os.mkdir(path)

    if args['build']:
        if not decknames:
            decknames = [
                deckname[:-3] for deckname in os.listdir(source)
                if deckname[-3:] == ".md"
            ]

            if not decknames:
                logging.info(
                    "No .md files in source directory; nothing to do."
                )
                exit(0)

        convert(source, destination, template, decknames)
    elif args['watch']:
        watch(source, destination, template)
