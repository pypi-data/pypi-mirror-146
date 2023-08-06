class POSTMAN:
    schema = "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"


class APP:
    root_dir = "./postmanrenderer/"
    template_dir = "templates/"
    collections_template = "collection.j2"


class HTTP_METHOD:
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    # PATCH = "PATCH"
    # DELETE = "DELETE"
    # COPY = "COPY"
    # HEAD = "HEAD"
    # OPTIONS = "OPTIONS"
    # LINK = "LINK"
    # UNLINK = "UNLINK"


class BODY_MODE:
    formdata = "formdata"
    urlencoded = "urlencoded"
    file = "file"
    raw = "raw"


class Jinja:
    trim_blocks = False
    lstrip_blocks = False


class Script_Type:
    prerequest = "prerequest"
    test = "test"


class Language:
    html = "html"
    javascript = "javascript"
    json = "json"
    text = "text"
