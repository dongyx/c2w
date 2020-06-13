# c2w

The c2w utility converts a CLI program to a Web service.

## Installation

```
% pip install c2w
```

## Getting Startted

We convert [kramdown](https://kramdown.gettalong.org) to a web service to get an online Markdown renderer.

```
% c2w --mime text/html kramdown
```

`c2w` is serving on `127.0.0.1:8000` now.

```
% curl http://localhost:8000 -X POST --data-binary @- << __EOF__
heredoc> # TITLE
heredoc>
heredoc> This is **strong**.
heredoc> __EOF__
```

We could get the following.

```
<h1 id="title">TITLE</h1>

<p>This is <strong>strong</strong>.</p>
```

The query string will be split by `&`, decoded and sent to `kramdown` as arguments.
The request body will be sent to the `stdin` of `kramdown` and the `stdout` of `kramdown` will be sent to the browser.

`kramdown` can translate Mardown to LaTex with the option `-o latex`.
If we want to get the LaTex output, we could put `-o&latex` in the query string.

```
% curl 'http://localhost:8000?-o&latex' --data-binary @- << __EOF__
heredoc> # TITLE
heredoc>
heredoc> This is **strong**.
heredoc> __EOF__
```

We got the following.

```
\section{TITLE}\hypertarget{title}{}\label{title}

This is \textbf{strong}.
```

## Serving as a CGI program with an HTTP Server

The HTTP server provided by `c2w` is not mature enough.
You may want to use Apache HTTPd or Nginx.
To achieve this you can run `c2w` in CGI mode.

Create a simple Shell script named `netmark`.

```
#!/bin/bash

c2w --cgi --mime text/html kramdown
```

Give it the execution permission and put it in the `cgi-bin` directory of your HTTP server.
Now you get an online Markdown renderer at `..../cgi-bin/netmark`.

## Detailed Usage

Run `c2w --help`.

## Why I Wrote It

[c2w: Convert Any CLI Program to a Web Service](http://dongyuxuan.me/posts/c2w.html)
