import json
import requests
import socket

HOST = "127.0.0.1"
PORT = 2000
PANEL_URL = f"http://{HOST}:{PORT}"

class PydobeBaseObject(object):
    """Base object for every mirror object from ExtendScript"""

    def __init__(self, pydobe_id: str):
        self.pydobe_id = pydobe_id

    def _eval_on_this_object(self, extend_property: str = "", index: int = None):
        """Query property or execute function on ExtendScript object"""

        if extend_property:
            extend_property = f".{extend_property}"
        if index:
            index = f"[{index}]"
        else:
            index = ""
        line = f"$._pydobe['{self.pydobe_id}']{index}{extend_property};"
        result = eval_script_returning_object(line)
        return result


class PydobeBaseCollection(PydobeBaseObject):
    def __init__(self, pydobe_id: str, len_property: str):
        """Base Object for collections"""

        if pydobe_id is None:
            raise ValueError("Creating a collection from scratch is not supported")
        self.len_property = len_property
        super(PydobeBaseCollection, self).__init__(pydobe_id)

    def __getitem__(self, index: int) -> dict:
        """Builtin method for getting the value at the specific index, redirect to ExtendScript similar query"""

        if index < 0:
            index = str(self.__len__() + index)
        # return self._eval_on_this_object(es_property="typeName", index=index)
        return self._eval_on_this_object(index=index)

    def __len__(self) -> int:
        """Builtin method for length, we ask premiere using the 'num...' property of the object"""

        return int(self._eval_on_this_object(self.len_property))

def is_port_open():
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    location = (HOST, PORT)
    result_of_check = a_socket.connect_ex(location)
    message = f"Connection to port {PORT} could not be established. Please ensure After Effects is running."
    if result_of_check != 0:
        raise ConnectionError(message)

def eval_script_returning_object(line: str):
    """Eval the line as ExtendScript code.
    If the code returns an object, it will be stored with an id for pydobe to handle """

    # Create ExtendScript to send
    script = "var tmp = {}".format(line)
    script += """\nif(typeof tmp === 'object' && tmp !== null){
            var newPydobeId = $._pydobe.generateId();
            $._pydobe[newPydobeId] = tmp;
            tmp = ExtendJSON.stringify({"isObject": true, "objectType": tmp.reflect.name, "pydobeId": newPydobeId}, internal_variables_replacer, 0, 1);
        }
        tmp"""
    # Get the resulting data
    result = eval_script(script)
    # Extract pydobe ID if object is returned
    if isinstance(result, dict) and result.get("isObject"):
        kwargs = dict(pydobe_id=result["pydobeId"])
        return kwargs
    return result


def eval_script(code: str):
    """Send ExtendScript code to adobe software, retrieve and decode the response"""

    # send code to adobe software (adding try statement to prevent error popup message locking UI)
    response = requests.post(PANEL_URL,
                             json={"to_eval": "try{\n" + code + "\n}catch(e){e.error=true;ExtendJSON.stringify(e)}"})

    # handle response
    data = response.text

    # Check if the data is an object. If it is - decode it. If not - return data as text
    try:
        decoded_data = json.loads(data)
    except json.decoder.JSONDecodeError:
        return data
    return decoded_data


def format_to_extend(obj):
    """Format the argument to ExtendScript"""

    if isinstance(obj, PydobeBaseObject):
        return "$._pydobe['{}']".format(obj.pydobe_id)
    elif isinstance(obj, bool):
        return str(obj).lower()
