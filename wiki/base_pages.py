base_home_page = """# HomePage

Welcome to **wiki.py**, a simple, pythonic wiki engine.
You can access [help](/WikiHelp/) anytime by pressing '**h**' on your keyboard.
"""

base_help_page = """# WikiHelp

## Syntax

The syntax is derived from [Markdown](http://daringfireball.net/projects/markdown/syntax).

A title level X is made by typing X*#, followed by the title.

e.g.:

    # Title1

    ## Title2

    ## Title2

    ### Title3

As **wiki.py** uses the [markdown python library](http://pythonhosted.org/Markdown/). The following extensions are available:

"""

from wiki import app

exts = []

for elem in app.config['MARKDOWN_EXTS']:
    exts.append("* [{0}](http://pythonhosted.org/Markdown/extensions/{0}.html)\n".format(elem))

base_help_page = base_help_page + "".join(exts)

base_help_page = base_help_page + """

For more explanations on the syntax, please refer to the corresponding extensions.


## **wiki.py**-specific, markdown-related settings

In order for a web page to be valid, the following constraints must be respected:

The first line of the document should be the page's name. For instance, for the page HomePage, the first line is `# HomePage`.

In order to link to an other webpage, use double square brackets, like so: [[HomePage]]

    [[HomePage]]

## Edit a page

When viewing a page, press '**e**' to edit.

If you want to edit a page not yet created, please visit the URL `/PageName/edit`.

"""
