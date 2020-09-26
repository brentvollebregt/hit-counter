# Server Setup

- [Local Setup](#local-setup)
- [PythonAnywhere Setup](#pythonanywhere-setup)

Python 3.6 and above is required to run this server.

## Local Setup

Hosting the server locally is very basic:

1. Clone the repo: `git clone https://github.com/brentvollebregt/hit-counter.git`
2. cd into the repo: `cd hit-counter`
3. Install requirements: `python -m pip install -r requirements.txt`
4. Generate `cert.pem` and `key.pem` in the root directory using `openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365`.
5. Run the server: `python server.py`
6. Go to the root of the app (try `https://127.0.0.1:8080/`) and you will be initially welcomed with "*Your connection is not private*". Click "Advanced" -> "Proceed to 127.0.0.1 (unsafe)" to tell your browser that this certificate (that you just generated in #4) is ok. 

After step #5, `data.db` will automatically be generated which will hold all the data. 

> `cert.pem` and `key.pem` are required to make requests to the the server using HTTPS. HTTPS is required because we are setting Secure=true on cookies due to having to use SameSite="none".

## PythonAnywhere Setup

This service is publicly hosted at [hitcounter.pythonanywhere.com](https://hitcounter.pythonanywhere.com/), to do this yourself, do the following:

1. Start a new bash console and clone the repo: `git clone https://github.com/brentvollebregt/hit-counter.git`
2. Create a new Python 3.8 virtual environment: `mkvirtualenv venv --python=/usr/bin/python3.8`
    - More details at https://help.pythonanywhere.com/pages/Virtualenvs/
    - Can prove you are using the correct Python by executing `which python` 
3. Go into the project root: `cd hit-counter`
4. Install dependencies: `python -m pip install -r requirements.txt`
5. Create a default web app that uses Flask and the highest version of Python 3. Use the default path provided.
6. In the web tab, go down to the "Code" heading and go to the file beside "WSGI configuration file".
    3.1 Make the following changes:
    ```diff
    # add your project directory to the sys.path
    -project_home = '/home/YOUR_USERNAME/mysite'
    +project_home = '/home/YOUR_USERNAME/hit-counter'
    if project_home not in sys.path:
        sys.path = [project_home] + sys.path

    # import flask app but need to call it "application" for WSGI to work
    -from flask_app import app as application  # noqa
    +from server import app as application
    ```
    3.2 Save
7. Go down to "Virtualenv" and set the virtual environment to the location of the virtual environment you created in step 2.
    - The path will be something like `/home/YOUR_USERNAME/.virtualenvs/venv`
    - You can find this path when executing `which python`, leave off `/bin/python`.
8. Under "Security", enable "Force HTTPS". 
9. Go back to the top of web tab and reload your site.

Your database, `data.db` will be located at `~`.

> A virtual environment is required on pythonanywhere to make sure that required packages and versions exist.
