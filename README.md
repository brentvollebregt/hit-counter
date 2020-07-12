# Hit Counter
Easily count hits on a website by requesting a SVG that displays a hit count.

<div style="text-align: center">
    <img src="https://hitcounter.pythonanywhere.com/count/tag.svg?url=https%3A%2F%2Fgithub.com%2Fbrentvollebregt%2Fhit-counter" alt="Hits">
</div>

Live demo hosted at: [hitcounter.pythonanywhere.com](https://hitcounter.pythonanywhere.com/)

## What is This?
This is a server that allows a client to request for an SVG file that displays views for a URL. This URL can either be passed as a query parameter or the referrer (or referer) value in the header will be used.

A small method to help prevent the count increasing after short consecutive page loads is included which uses cookies to check if the user has made the request recently.

**This makes it very easy to keep track of views on static sites like Github Pages.** *It can also be used on non-static sites as a general counter.*

## How Can I Use it?
### Getting an SVG
To get an image for the current URL (for example is image is being requested by www.example.com), simply get the image as you normally would:

```html
<img src="https://hitcounter.pythonanywhere.com/count/tag.svg" alt="Hits">
```

In this example, a hit would be added to the websites count on the server. To stop this from occurring but still get the SVG file, use:

```html
<img src="https://hitcounter.pythonanywhere.com/nocount/tag.svg" alt="Hits">
```

### Getting the Count Raw
If you don't want the SVG file but still want the count to use in something else, you can do a GET request to ```/count``` or as before, ```/nocount``` to not add a count. For Example:

```javascript
let xmlHttp = new XMLHttpRequest();
xmlHttp.open('GET', 'https://hitcounter.pythonanywhere.com/count', false);
xmlHttp.send(null);
count = xmlHttp.responseText;
```

#### Using Ajax

```javascript
let targetUrl = window.location.href;
$.ajax('https://hitcounter.pythonanywhere.com/count',{
    data:{url: targetUrl},
}).then(count => console.log('Count:' + count));
```

> Do not use `data: {url: encodeURIComponent(targetUrl)}` as Ajax will encode the string (url) for you. Doing this will encode the url twice which will then only be decoded on the server once (this can lead to broken tags in the future).

### Getting a Count For a Site That Isn't Me
There may be circumstances that the referrer may not be sent or you may want to request an SVG or count for another site. To do this, set `url` to the URL you want to get (make sure to encoded the value).

For example, getting an SVG:

```html
<img src="https://hitcounter.pythonanywhere.com/nocount/tag.svg?url=www.example.com" alt="Hits">
```

And if you want to get the count:

```javascript
let targetUrl = 'www.example.com';
let query = '?url=' + encodeURIComponent(targetUrl);
let xmlHttp = new XMLHttpRequest();
xmlHttp.open('GET', 'https://hitcounter.pythonanywhere.com/nocount' + query, false);
xmlHttp.send(null);
count = xmlHttp.responseText;
```

> There are also some situations where a client will not send the Referer in the header. This is a simple solution to the server not being able to find where the request came from.

## Generating Links With A Tool Hosted By The Server
Going to the location `/` on the server, you will be served with an HTML page that contains a tool to create the image tag or markdown element and search up a websites count.

![Interface](https://nitratine.net/posts/hit-counter/interface.png)

## Hosting Your Own Server
- Clone the repo: `git clone https://github.com/brentvollebregt/hit-counter.git`
- cd into the repo: `cd hit-counter`
- Install requirements: `python -m pip install -r requirements.txt`
- Run the server: `python server.py`

I host this on [pythonanywhere.com](https://hitcounter.pythonanywhere.com/); to do this make sure you have cloned the repo into the filesystem and then create a new project. Modify the "WSGI configuration file" under the "Code" header in the "Web" tab. Change line 16 to import your script and restart the application using the green button at the top.

```python
from server import app as application
```

> If you want to enable HTTPS on pythonaywhere, set config.ENABLE_SSL in `config.py` to True.

## Server Configuration
- Enable SSL: Set an environment variable `ENABLE_SSL` to `true`.
- Change Database location: Set an environment variable `DATABASE_FILE_PATH` to the file path of the database. 

> Alternatively these config values can be manually set in `config.py`.

### Domain whitelisting
You can configure the server to only count hits to domains matching a certain pattern. To do so, add regular expression entries to `URL_WHITELIST_RE` in `config.py`, e.g. `r'github\.com'`.

## Inspiration
This project was inspired by [github.com/dwyl/hits](https://github.com/dwyl/hits) which is a "General purpose hits (page views) counter" which unfortunately will count GitHub repo views. This was my idea to expand on this and add some features with also making it compatible with any site.

## Why Does The Anti-Refresh System Not Work?
On sites like github.com, images are cached. Even though I declare no-cache in the header, GitHub will load the image on their side first which will cause an increase in the count no matter what as it isn't passing back the cookie it got previously (and if it did there would be a timeout for everyone).

The cookie system implemented to help reduce count increases after consecutive requests will only work if the cookies that were received are sent back to the server in the consecutive requests. No cookie means this no longer works.
