# pyjiracloudapi

python3 module to call jiracloud apis in command line or inside a module and export result into mysql and later Grafana.

[The source for this project is available here][src].

---

It's a python module that you can include in your python module or can be used in command line.

    usage: pyjiracloudapi.py [-h] [-V] [-U USEREMAIL] [-t TOKEN] [-u URL] [-a API] [-m METHOD] [-J JSONFILE]

    pyjiracloudapi is a python3 program that call jiracloud apis in command line or imported as a module

    optional arguments:
    -h, --help            show this help message and exit
    -V, --version         Display the version of pyjiracloudapi
    -U USEREMAIL, --useremail USEREMAIL
                            jiracloud user email
    -t TOKEN, --token TOKEN
                            jiracloud token
    -u URL, --url URL     jiracloud url
    -a API, --api API     jiracloud api should start by a slash
    -m METHOD, --method METHOD
                            should contain one of the method to use : ['DELETE', 'GET', 'POST', 'PUT']
    -J JSONFILE, --jsonfile JSONFILE
                            json file needed for POST method

---

[packaging guide]: https://packaging.python.org
[distribution tutorial]: https://packaging.python.org/tutorials/packaging-projects/
[src]: https://github.com/stormalf/pyjiracloudapi
[rst]: http://docutils.sourceforge.net/rst.html
[md]: https://tools.ietf.org/html/rfc7764#section-3.5 "CommonMark variant"
[md use]: https://packaging.python.org/specifications/core-metadata/#description-content-type-optional

# release notes

1.0.0 initial version
