# Flask-babel walk-trough

### 1. Install the requirements

```
pip install flask-babel
pip install pybabel
```

or

```
conda install -c conda-forge flask-babel
```

### 2. Write the text in the templates or the code

python:

``` .py
from flask import Flask, redirect, session, request, render_template
from flask_babel import gettext

app = Flask(__name__)
app.config["BABEL_DEFAULT_LOCALE"] = "en"

babel = Babel(app)

text = gettext("strings.hello_world")
```

jinja:

``` .html
<p>{{ _("strings.hello_world") }}</p>
```

Currently, this code will return "strings.hello_world" or any other string, that it is given.  
Now we will set up the translations

### 3. Setup a .cfg file

Create a ./babel/babel.cfg file with the following information

``` .cfg
[python: webapp/**.py]
[jinja2: webapp/templates/**.html]
encoding = utf-8
extensions=jinja.2.ext.autoescape,jinja2.ext.with_
```

### 4. Create a messages.pot file

This file will contain all the strings in your app

```
pybabel extract -F ./babel/babel.cfg -o ./babel/messages.pot . 
```

To update this file with new strings from the files, run this command

```
pybabel update -F ./babel/babel.cfg -o ./babel/messages.pot . 
```

### 5. Create .po files for translation

Run this command:  

```
pybabel init -i ./babel/messages.pot -d translations -l en
```

This will create a new file at ./translations/en/LC_MESSAGES/messages.po  
The file will look somewhat like this

``` .po
# English translations for PROJECT.
# Copyright (C) 2022 ORGANIZATION
# This file is distributed under the same license as the PROJECT project.
# FIRST AUTHOR <EMAIL@ADDRESS>, 2022.

#: templates/components/side_panel.html:20 templates/discover_page.html:7
msgid "strings.discover_page"
msgstr ""

#: templates/discover_page.html:12 templates/discover_page.html:57
msgid "strings.upload_song"
msgstr ""
```

Write the translations in the msgstr, like this

``` .po
#: templates/discover_page.html:12 templates/discover_page.html:57
msgid "strings.upload_song"
msgstr "Upload song"
```

If the files is very big, it might be more handy to use a .po file editor. Some editors like [the localise poeditor](https://localise.biz/free/poeditor).

### 6. Compile the .po files to binary

Run this command:  

```
pybabel compile -d translations
```

This will create a new .mo file next to each .po file in the translations directory.

### 7. Get the users' locale

If your app contains multiple languages, select the language with the babel.localeselector

``` .py
@babel.localeselector
def get_locale() -> str:
    """
    Used for determining the language of the website
    If the locale is in the session it returns the local
    If the locale is not in the session it returns the best local according to the users browser
    :return: the locale as "lv" or "en"
    """
    locale = request.accept_languages.best_match(["lv", "en"])
    if "locale" in session:
        locale = session.get("locale")

    session["locale"] = locale
    return locale
```