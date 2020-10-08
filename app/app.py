import json
import os
from http import HTTPStatus

from flask import Flask, request, Response, render_template
from marko.ext.gfm import gfm
from uuid import uuid4
from yaml import Dumper, dump as ydump
import sqlite3

from markupsafe import escape

app = Flask(__name__)


@app.route('/')
def hello_world():
    motdl = []
    client_ip = request.remote_addr
    md = render_template("index.md", client_ip=client_ip)
    rendered_md = gfm(md)
    html = render_template("index.html", markdown_rendered=rendered_md,
                           request_id=uuid4().hex, motdl=motdl)
    return Response(content_type="text/html", response=html)


@app.route('/address.<string:ext>')
def return_rendered(ext):
    ext = escape(ext)
    rid = uuid4().hex
    headers = {
        "x-request-id": rid
    }
    res = {
        "ip": request.remote_addr,
        "request_id": rid
    }
    if ext == "txt":
        if request.args.get("plain", None) is not None:
            resp = "{ip},{request_id}".format(**res)
            return Response(content_type="text/plain", response=resp, headers=headers)
        else:
            resp = "ip={ip}\nrequest_id={request_id}".format(**res)
            return Response(content_type="text/plain", response=resp, headers=headers)
    elif ext == "json":
        return Response(content_type="application/json", response=json.dumps(res), headers=headers)
    elif ext == "yaml" or ext == "yml":
        return Response(content_type="application/x-yaml", response=ydump(res, Dumper=Dumper), headers=headers)
    else:
        return Response(status=HTTPStatus.NOT_FOUND,
                        response=gfm(render_template("404.md", url=request.url, request_id=rid))
                        )


if __name__ == '__main__':
    app.run(host="127.0.0.1")
