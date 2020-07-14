# Background

- [Anti-Refresh Counting System](#anti-refresh-counting-system)

## Anti-Refresh Counting System
A weak attempt a to stop hits increasing by people spamming F5 is a cookie. This cookie remembers when you increase the count for a URL and will wait [COOKIE_TIMEOUT](./config#cookie_timeout) seconds before the user can count as another hit.

On sites like github.com, images are cached. Even though I declare no-cache in the header, GitHub will load the image on their side first which will cause an increase in the count no matter what as it isn't passing back the cookie it got previously (and if it did there would be a timeout for everyone).

The cookie system implemented to help reduce count increases after consecutive requests will only work if the cookies that were received are sent back to the server in the consecutive requests. No cookie means this no longer works.
