# Server Setup

- [Local Setup](#local-setup)
- [PythonAnywhere Setup](#pythonanywhere-setup)

Python 3.6 and above is required to run this server.

## Local Setup

Hosting the serve locally is very basic:

1. Clone the repo: `git clone https://github.com/brentvollebregt/hit-counter.git`
2. cd into the repo: `cd hit-counter`
3. Install requirements: `python -m pip install -r requirements.txt`
4. Run the server: `python server.py`

After step #4, `data.db` will automatically be generated which will hold all the data of 

## PythonAnywhere Setup

This service is publicly hosted at [hitcounter.pythonanywhere.com](https://hitcounter.pythonanywhere.com/), to do this yourself, do the following:

1. Start a new bash console and clone the repo: `git clone https://github.com/brentvollebregt/hit-counter.git`
2. Create a default web app that uses Flask and the highest version of Python 3. Use the default path provided.
3. In the web tab, go down to the "Code" heading and go to the file beside "WSGI configuration file".
    3.1 Make the following changes:
    ```diff
    # add your project directory to the sys.path
    -project_home = '/home/YourUserName/mysite'
    +project_home = '/home/YourUserName/hit-counter'
    if project_home not in sys.path:
        sys.path = [project_home] + sys.path

    # import flask app but need to call it "application" for WSGI to work
    -from flask_app import app as application  # noqa
    +from server import app as application
    ```
    3.2 Save
4. Go back to the web tab and reload your site.

Your database, `data.db` will be located at `/home/YourUserName`.

If you want to enable HTTPS on pythonaywhere, go into [`config.py`](../config.py) and set ENABLE_SSL to `True`.
