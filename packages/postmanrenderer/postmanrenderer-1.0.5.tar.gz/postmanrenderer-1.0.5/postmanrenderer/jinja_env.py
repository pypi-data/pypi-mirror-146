import json
from constants import Jinja
import jinja2

# Initializes custom filters
def init(env: jinja2.Environment):
    env.filters["to_json"] = to_json
    env.trim_blocks = Jinja.trim_blocks
    env.lstrip_blocks = Jinja.lstrip_blocks
    # env.keep_trailing_newline = True
    
# Accepts python list and returns json compatible list in string type
def to_json(ele: list) -> str:
    ele_json = json.dumps(ele)
    return ele_json