from abc import ABC, abstractmethod
import json
from re import T
from constants import APP, HTTP_METHOD, POSTMAN, BODY_MODE, Language, Script_Type
import uuid
from jinja2 import Template, FileSystemLoader, Environment
from typing import List
import jinja_env


class Url:
    '''
    Representation of Request Url
    '''

    def __init__(self, url: str):
        url_split = url.split("://")
        self.protocol: str = url_split[0] if len(url_split) > 1 else None
        self.raw: str = url_split[-1]
        self.host: str = self.raw.split(".")


class RequestBodyData(ABC):
    @abstractmethod
    def to_json(self):
        pass


class KeyValueData():
    def __init__(self, key: str, value: str, description: str = ""):
        self.key: str = key
        self.value: str = value
        self.description: str = description
        self.type = "text"


class KeyValueBody(RequestBodyData):
    def __init__(self, data: List[KeyValueData] = []):
        self.data: List[KeyValueData] = data

    def addKeyValue(self, data: List[KeyValueData]):
        self.data += data

    def to_json(self):
        return json.dumps(self.data, default=vars)


class RawBody(RequestBodyData):
    def __init__(self, data: str, language: Language = Language.text):
        self.data: str = data
        self.language: Language = language

    def to_json(self):
        return self.data


class ProtocolProfileBehaviour:
    '''
    Used to change Protocol Behavior for Requests
    See docs:
    https://github.com/postmanlabs/postman-runtime/blob/develop/docs/protocol-profile-behavior.md
    '''

    def __init__(self):
        pass


class RequestBody:
    '''
    Adds body to a Request, body can be None, Raw, formdata, urlEncoded
    '''

    def __init__(self, mode: BODY_MODE):
        self.mode: BODY_MODE = mode
        self.require_options: bool = False

    def addRawBody(self, content: RawBody):
        if self.mode != BODY_MODE.raw:
            raise("Mode incorrect")
        self.content = content
        if self.content.language != None:
            self.require_options = True

    def addurlEncodedBody(self, content: KeyValueBody):
        if self.mode != BODY_MODE.urlencoded:
            raise("Mode incorrect")
        self.content = content

    def addFormData(self, content: KeyValueBody):
        if self.mode != BODY_MODE.formdata:
            raise("Mode incorrect")
        self.content = content
        self.require_options = True

    def addFileData(self):
        pass


class Script:
    def __init__(self, script_type: Script_Type, filename):
        self.script_type = script_type
        self.script = []
        with open(filename, "r") as f:
            self.script = f.readlines()
        self.script = [s.strip() for s in self.script]


# Representation of Request in a Collection

class Request:
    '''
    Representation of Request in a Collection
    '''

    def __init__(self, name: str, method: HTTP_METHOD, description: str, url: Url) -> None:
        self.name: str = name
        self.method: HTTP_METHOD = method
        self.description = description
        self.headers: dict = dict()
        self.url: Url = url
        self.body: RequestBody = None
        self.ProtocolProfileBehaviour = None
        self.events = {}

    def add_script(self, script: Script):
        self.events[script.script_type] = script

    def add_header(self, key: str, value: str):
        self.headers[key] = value

    def add_body(self, body: RequestBody):
        self.body = body

    def add_profile_protocol_behaviour(self, ppb: ProtocolProfileBehaviour):
        self.ProtocolProfileBehaviour = ppb


class Collection:
    '''
    Representation of Postman Collection
    '''

    def __init__(self, name: str, id=None) -> None:
        self.id = uuid.uuid4() if id == None else id
        self.name: str = name
        self.schema = POSTMAN.schema
        self.requests: List[Request] = []

    def add_request(self, request: Request):
        self.requests.append(request)

    def get_template_object(self) -> Template:
        file_loader = FileSystemLoader(APP.root_dir + APP.template_dir)
        env = Environment(loader=file_loader)
        jinja_env.init(env)
        template = env.get_template(APP.collections_template)
        return template

    def render(self, template: Template) -> str:
        rendered_template = template.render(collection=self)
        return rendered_template

    def write_to_file(self, rendered_collection, filename):
        with open(filename, "w") as f:
            f.write(rendered_collection)


if __name__ == "__main__":
    collection = Collection("sample_collection")
    # request = Request("Yahoo request", HTTP_METHOD.GET,
    #                   "", Url("https://www.yahoo.com"))
    # collection.add_request(request)

    request = Request("Google request", HTTP_METHOD.GET,
                      "", Url("https://www.google.com"))
    request.add_header("Content-Type", "Application/json")
    pre_script = Script(Script_Type.prerequest, "tests/data/pre-request.js")
    request.add_script(pre_script)
    request.add_script(Script(Script_Type.test,
                       "tests/data/post-request.js"))

    # body = RequestBody(BODY_MODE.raw)
    # rawBodyData = RawBody("x = hello test")
    # body.addRawBody(rawBodyData)

    body = RequestBody(BODY_MODE.formdata)
    formDataBody = KeyValueBody(
        [KeyValueData("hello", "world"), KeyValueData("test", "one")])
    body.addFormData(formDataBody)
    request.add_body(body)
    collection.add_request(request)

    template = collection.get_template_object()
    render = collection.render(template)
    collection.write_to_file(render, "out.collection")
    print(render)
