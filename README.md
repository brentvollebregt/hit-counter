# Hit Counter
Easily count hits on a website by requesting a SVG that displays a hit count.

<!-- <div style="text-align: center">
    <img src="https://hitcounter.pythonanywhere.com/count/tag.svg?url=https%3A%2F%2Fgithub.com%2Fbrentvollebregt%2Fhit-counter" alt="Hits">
</div> -->

~~Live demo hosted at: [hitcounter.pythonanywhere.com](https://hitcounter.pythonanywhere.com/)~~

> ~~Please note this is only a demo instance and any traffic that causes harm to the server will be blocked.~~
> ~~Also due to how this demo instance is being hosted and the large amount of traffic it gets, the server does fall over some times.~~

> PythonAnywhere has understandably disabled the demo instance due to heavy disk usage.

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

> Warning: ["*Chrome plans to radually enable strict-origin-when-cross-origin as the default policy in 85; this may impact use cases relying on the referrer value from another origin*"](https://developers.google.com/web/updates/2020/07/referrer-policy-new-chrome-default). To get around this, you'll want to put the URL in the query string as outlined under [Getting a Count For a Site That Isn't Me](#getting-a-count-for-a-site-that-isnt-me).

### Getting the Count Raw
If you don't want the SVG file but still want the count to use in something else, you can do a GET request to ```/count``` or as before, ```/nocount``` to not add a count. For Example:

```javascript
fetch('https://hitcounter.pythonanywhere.com/count', {
    credentials: 'include'
})
    .then(res => res.text())
    .then(count => console.log('Count: ' + count))
```

#### Using XMLHttpRequest

```javascript
let xmlHttp = new XMLHttpRequest();
xmlHttp.withCredentials = true;
xmlHttp.onload = function() {
    console.log('Count: ' + this.responseText);
};
xmlHttp.open('GET', 'https://hitcounter.pythonanywhere.com/count', true);
xmlHttp.send(null);
```

#### Using Ajax

```javascript
let targetUrl = window.location.href;
$.ajax('https://hitcounter.pythonanywhere.com/count', {
    data: { url: targetUrl },
    xhrFields: { withCredentials: true }
}).then(count => console.log('Count: ' + count));
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
fetch(`https://hitcounter.pythonanywhere.com/count?url=${encodeURIComponent(targetUrl)}`, {
    credentials: 'include'
})
    .then(res => res.text())
    .then(count => console.log('Count: ' + count))
```

> There are also some situations where a client will not send the Referer in the header. This is a simple solution to the server not being able to find where the request came from.

## Generating Links With A Tool Hosted By The Server
Going to the location `/` on the server, you will be served with an HTML page that contains a tool to create the image tag or markdown element and search up a websites count.

![Interface](https://nitratine.net/posts/hit-counter/interface.png)

## Documentation
- [Server Setup](./docs/setup.md)
    - [Local Setup](./docs/setup.md#local-setup)
    - [PythonAnywhere Setup](./docs/setup.md#pythonanywhere-setup)
- [Server Configuration](./docs/config.md)
- [Usage](./docs/usage.md)
    - [Getting an SVG](./docs/usage.md#getting-an-svg)
    - [Getting the Count Raw](./docs/usage.md#getting-the-count-raw)
    - [Getting a Count For a Site That Isn't Me](./docs/usage.md#getting-a-count-for-a-site-that-isnt-me)
    - [Generating Links With A Tool Hosted By The Server](./docs/usage.md#generating-links-with-a-tool-hosted-by-the-server)
- [Background](./docs/background.md)
    - [Anti-Refresh Counting System](./docs/background.md#anti-refresh-counting-system)

## Inspiration
This project was inspired by [github.com/dwyl/hits](https://github.com/dwyl/hits) which is a _"General purpose hits (page views) counter"_ which unfortunately will only count GitHub repo views. This was my idea to expand on this and add some features with also making it compatible with any site.
