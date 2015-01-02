#!/usr/bin/env python
"""This program offers the user random articles from Wikipedia to read. On
selection of an articles, the program opens the article in a new browser tab.
The user can set how many articles to show at a time (from 1 article to 10).

This program only runs on Python v3.0 or higher.
"""
from getopt import getopt, error
from json import loads
from webbrowser import open_new_tab
import sys

__author__ = "Jeffrey Chan"
__version__ = "1.0.0"

if sys.version_info[0] >= 3:
    from urllib.request import urlopen

"""This is the URL to the Wikipedia API to get 10 random articles."""
wikipedia_random_url = ("http://en.wikipedia.org/w/api.php?action=query&"
                        "list=random&rnnamespace=0&format=json&rawcontinue&"
                        "rnlimit=10")

"""This is the URL to any article on Wikipedia - once the ID is added on."""
wikipedia_article_url = "http://en.wikipedia.org/wiki?curid="

"""Help message for the user."""
help_message = ("This program offers the user random articles from Wikipedia "
                "to read. Articles will be opened in a new browser tab.\n"
                "Use -n or --number= to set the number of articles to display "
                "at any one time (from 1 to 10).")

"""A queue of dictionaries representing Wikipedia articles to eventually
display to the user.
"""
queue = []

"""Current amount of articles to show to the user."""
articles_to_show = 5

def call_Wikipedia():
    """Gets random articles from Wikipedia (10 at a time) and stores them in queue.
    """
    global queue
    try:
        data = urlopen(wikipedia_random_url)
        data_dict = loads(data.read().decode("utf-8"))
        data.close()
        articles = data_dict["query"]["random"]
        queue += articles
        return True
    except Exception as e:
        print(e)
        return False

def offerArticles():
    """Displays articles to the user. Calls call_Wikipedia to fill up queue when
    necessary. Offers user option to select an article by number (will open
    article in new browser tab), get new articles choices, or exit the program.

    This is the main function of the program and is constantly running once the
    program is started waiting for the user to give commands - hence the while True
    loop.
    """
    global queue
    while True:
        try:
            if not queue or len(queue) < articles_to_show:
                if not call_Wikipedia():
                    print("Unable to fetch Articles now")
                    return 1
            current =  queue[:articles_to_show]
            queue = queue[articles_to_show:]
            for i in range(articles_to_show):
                print("[{:d}] {:s}".format(i, current[i]["title"]))
            user_input = input("Select an article by number, press enter to "
                               "get new articles, or type exit.\n")
            while user_input:
                if appropriate_number(user_input, 0, articles_to_show):
                    user_choice = int(user_input)
                    open_new_tab(wikipedia_article_url +
                                 str(current[user_choice]["id"]))
                elif user_input == "exit":
                    return 0
                else:
                    print("That's not a valid option.")
                user_input = input("Select another article by number, "
                                   "press enter to get new articles, or "
                                   "type exit.\n")
        except KeyboardInterrupt:
            print("\n")
            return 0

def appropriate_number(user_input, lower_limit=1, upper_limit=10):
    """Returns true if user input is a number that is bigger than or equal to
    the lower limit and smaller than the upper limit. Returns false otherwise.
    """
    try:
        a = int(user_input)
        if a < lower_limit:
            return False
        elif a >= upper_limit:
            return False
        else:
            return True
    except ValueError:
        return False

def main(*argv):
    """This function starts the program. Provides help messages when the user asks
    for one as well as when user uses program inappropriately. Allows user to
    set the amount of articles to display at one time.
    """
    global articles_to_show
    try:
        if sys.version_info[0] < 3:
            print("Please use Python 3.0 or above.")
            return 1
        opts, args = getopt(argv[0][1:],"hn:",["help", "number="])
    except error as msg:
        print(msg)
        print("for help use --help")
        return 2
    if args and not opts:
        print(help_message)
        return 2
    else:
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                print(help_message)
                return 2
            elif opt in ("-n", "--number"):
                if appropriate_number(arg, upper_limit=11):
                    articles_to_show = int(arg)
                else:
                    print("Please enter a number between 1-10.")
                    return 2
            else:
                print(help_message)
                return 2
    return offerArticles()

"""Calls the function to start the program on run. Exits the program after
running is complete either due to user exiting or an error.
"""
if __name__ == "__main__":
    sys.exit(main(sys.argv))