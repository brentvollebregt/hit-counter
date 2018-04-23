# hit-counter
Easily count hits on a website by requesting a svg displaying hit count

put url in url (&url=...) (use encodeURIComponent in JS)

10min cookie to stop the refresh problem. key is url hashed and then value is a random value

<!-- <img src="http://hits.dwyl.io/dwyl/hits.svg" alt="HitCount" style="max-width:100%;float: left; margin: 2.5px 10px 2.5px 0;"> -->

## testing
```
import requests
r = requests.get('http://127.0.0.1:8080/count', headers={'referer': 'www.example.com'})
r.text # 1
r = requests.get('http://127.0.0.1:8080/count', headers={'referer': 'www.example.com'}, cookies=r.cookies)
r.text # 1
r = requests.get('http://127.0.0.1:8080/count', headers={'referer': 'www.example.com'})
r.text # 2
r = requests.get('http://127.0.0.1:8080/count', headers={'referer': 'www.example.com'})
r.text # 3
```
