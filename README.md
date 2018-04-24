# Hit Counter
Easily count hits on a website by requesting a svg that displays a hit count.

Live demo hosted at:

# What is This?
This is a server that allows a client to request for a svg file that displays views for a url. This url can either be passed as a query parameter or the referrer (or referer) value in the header will be used.

These is also a small method to prevent the refresh count increase issue (if you want to call it an issue, I see it as annoying) which uses cookies.

**This makes is very easy too keep track of views on static sites like Github Pages.** (can also be uses on non-static sites as a general counter)

# How Can I Use it?
## Getting an SVG
To get an image for the current url (for example is image is being requested by www.example.com), simply get the image as you normally would:

```<img src="http://livedemo.com/count/tag.svg" alt="Hits">```

In this example a hit would be added to the websites count on the server. To stop this form occurring but still get the svg file, use:

```<img src="http://livedemo.com/nocount/tag.svg" alt="Hits">```

## Getting the Count Raw
If you don't want the SVG file but still want the count to use in something else, you can do a GET request to ```/count``` or as before ```/nocount``` to not add a count. For Example:

```javascript
let xmlHttp = new XMLHttpRequest();
xmlHttp.open('GET', 'http://livedemo.com/count', false);
xmlHttp.send(null);
count = xmlHttp.responseText;
```

## Getting a Count For a Site That Isn't Me
There may be circumstances that the referrer may not be sent or you may want to request a SVG or count for another site. To do this, add a query with ```url``` as the name and the url you want to get (encoded obviously).

For example, getting an svg:

```<img src="http://livedemo.com/count/tag.svg?url=www.example.com" alt="Hits">```

And if you want to get the count:

```javascript
let targetUrl = 'www.example.com';
let query = '?url=' + encodeURIComponent(targetUrl);
let xmlHttp = new XMLHttpRequest();
xmlHttp.open('GET', 'http://livedemo.com/count', false);
xmlHttp.send(null);
count = xmlHttp.responseText;
```

# Hosting Your Own Server
Running this server is very easy, simple clone the repo (or download the files) and run ```server.py```

I host this on pythonaywhere.com; to do this make sure you have cloned the repo into the filesystem and then create a new project. Modify the "WSGI configuration file" under the code header in the web tab. Change line 16 to import your script and restart the application using the green button at the top.

```from server import app as application```

# How it Works
This server has been built with Flask. Calling one of the ```/count``` or ```/nocount``` methods will interact with the local sqlite3 database (file) and keep track of urls, views and the counts for urls. Data will be returned based off what is in the database at the current time.

Cookies are used to prevent multiple counts for the same client in a specified period of time. These are simply the url as the key and a random string generated server side as the value.

# Configuration
In config.py there are a few configurations that can be made
### DATABASE_FILENAME
This is the name of the sqlite3 database to be used, if it doesn't exist it will be created so you don't really need to worry about this unless you have a conflict.

### COOKIE_TIMEOUT
This is the amount of time for a cline to count as a view again. When a view is counted, the SVG/count is returned with a cookie for that site. Currently that is set at 10mins (600 seconds) but can be changed.

To disable this feature simply set this to 0; the cookies stored on the server will be flushed from the database each new view.

### SVG_TEMPLATE
This is the template of the SVG returned. ```{count}``` must always be in this string so that python can add the count before giving it as a response.

### RANDOM_VALUE_LENGTH
This is the length of the value of the cookie stored both server and client side. Making this longer will stop collisions from occurring but will increase storage. Each value generated is completely random from the characters [0-9][a-z][A-Z].

