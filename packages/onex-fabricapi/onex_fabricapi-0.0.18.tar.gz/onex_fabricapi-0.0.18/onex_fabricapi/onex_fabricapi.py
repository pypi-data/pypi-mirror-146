# ONEx Fabric API 0.0.1
# License: MIT

import importlib
import logging
import json
import yaml
import requests
import urllib3
import io
import sys
import time
import re

try:
    from typing import Union, Dict, List, Any, Literal
except ImportError:
    from typing_extensions import Literal

if sys.version_info[0] == 3:
    unicode = str


def api(location=None, verify=True, logger=None, loglevel=logging.INFO, ext=None):
    """Create an instance of an Api class

    generator.Generator outputs a base Api class with the following:
    - an abstract method for each OpenAPI path item object
    - a concrete properties for each unique OpenAPI path item parameter.

    generator.Generator also outputs an HttpApi class that inherits the base
    Api class, implements the abstract methods and uses the common HttpTransport
    class send_recv method to communicate with a REST based server.

    Args
    ----
    - location (str): The location of an Open Traffic Generator server.
    - verify (bool): Verify the server's TLS certificate, or a string, in which
      case it must be a path to a CA bundle to use. Defaults to `True`.
      When set to `False`, requests will accept any TLS certificate presented by
      the server, and will ignore hostname mismatches and/or expired
      certificates, which will make your application vulnerable to
      man-in-the-middle (MitM) attacks. Setting verify to `False`
      may be useful during local development or testing.
    - logger (logging.Logger): A user defined logging.logger, if none is provided
      then a default logger with a stdout handler will be provided
    - loglevel (logging.loglevel): The logging package log level.
      The default loglevel is logging.INFO
    - ext (str): Name of an extension package
    """
    params = locals()
    if ext is None:
        return HttpApi(**params)
    try:
        lib = importlib.import_module("sanity_{}.onex_fabricapi_api".format(ext))
        return lib.Api(**params)
    except ImportError as err:
        msg = "Extension %s is not installed or invalid: %s"
        raise Exception(msg % (ext, err))


class HttpTransport(object):
    def __init__(self, **kwargs):
        """Use args from api() method to instantiate an HTTP transport"""
        self.location = (
            kwargs["location"]
            if "location" in kwargs and kwargs["location"] is not None
            else "https://localhost:443"
        )
        self.verify = kwargs["verify"] if "verify" in kwargs else False
        self.logger = kwargs["logger"] if "logger" in kwargs else None
        self.loglevel = kwargs["loglevel"] if "loglevel" in kwargs else logging.DEBUG
        if self.logger is None:
            stdout_handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter(fmt="%(asctime)s [%(name)s] [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
            formatter.converter = time.gmtime
            stdout_handler.setFormatter(formatter)
            self.logger = logging.Logger(self.__module__, level=self.loglevel)
            self.logger.addHandler(stdout_handler)
        self.logger.debug("HttpTransport args: {}".format(", ".join(["{}={!r}".format(k, v) for k, v in kwargs.items()])))
        if self.verify is False:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            self.logger.warning("Certificate verification is disabled")
        self._session = requests.Session()

    def send_recv(self, method, relative_url, payload=None, return_object=None, headers=None):
        url = "%s%s" % (self.location, relative_url)
        data = None
        headers = headers or {"Content-Type": "application/json"}
        if payload is not None:
            if isinstance(payload, bytes):
                data = payload
                headers["Content-Type"] = "application/octet-stream"
            elif isinstance(payload, (str, unicode)):
                data = payload
            elif isinstance(payload, OpenApiBase):
                data = payload.serialize()
            else:
                raise Exception("Type of payload provided is unknown")
        response = self._session.request(
            method=method,
            url=url,
            data=data,
            verify=False,
            allow_redirects=True,
            # TODO: add a timeout here
            headers=headers,
        )
        if response.ok:
            if "application/json" in response.headers["content-type"]:
                # TODO: we might want to check for utf-8 charset and decode
                # accordingly, but current impl works for now
                response_dict = yaml.safe_load(response.text)
                if return_object is None:
                    # if response type is not provided, return dictionary
                    # instead of python object
                    return response_dict
                else:
                    return return_object.deserialize(response_dict)
            elif "application/octet-stream" in response.headers["content-type"]:
                return io.BytesIO(response.content)
            else:
                # TODO: for now, return bare response object for unknown
                # content types
                return response
        else:
            raise Exception(response.status_code, yaml.safe_load(response.text))


class OpenApiBase(object):
    """Base class for all generated classes"""

    JSON = "json"
    YAML = "yaml"
    DICT = "dict"

    __slots__ = ()

    def __init__(self):
        pass

    def serialize(self, encoding=JSON):
        """Serialize the current object according to a specified encoding.

        Args
        ----
        - encoding (str[json, yaml, dict]): The object will be recursively
            serialized according to the specified encoding.
            The supported encodings are json, yaml and python dict.

        Returns
        -------
        - obj(Union[str, dict]): A str or dict object depending on the specified
            encoding. The json and yaml encodings will return a str object and
            the dict encoding will return a python dict object.
        """
        if encoding == OpenApiBase.JSON:
            return json.dumps(self._encode(), indent=2, sort_keys=True)
        elif encoding == OpenApiBase.YAML:
            return yaml.safe_dump(self._encode())
        elif encoding == OpenApiBase.DICT:
            return self._encode()
        else:
            raise NotImplementedError("Encoding %s not supported" % encoding)

    def _encode(self):
        raise NotImplementedError()

    def deserialize(self, serialized_object):
        """Deserialize a python object into the current object.

        If the input `serialized_object` does not match the current
        openapi object an exception will be raised.

        Args
        ----
        - serialized_object (Union[str, dict]): The object to deserialize.
            If the serialized_object is of type str then the internal encoding
            of the serialized_object must be json or yaml.

        Returns
        -------
        - obj(OpenApiObject): This object with all the
            serialized_object deserialized within.
        """
        if isinstance(serialized_object, (str, unicode)):
            serialized_object = yaml.safe_load(serialized_object)
        self._decode(serialized_object)
        return self

    def _decode(self, dict_object):
        raise NotImplementedError()


class OpenApiValidator(object):

    __slots__ = ()

    def __init__(self):
        pass

    def validate_mac(self, mac):
        if mac is None or not isinstance(mac, (str, unicode)) or mac.count(" ") != 0:
            return False
        try:
            if len(mac) != 17:
                return False
            return all([0 <= int(oct, 16) <= 255 for oct in mac.split(":")])
        except Exception:
            return False

    def validate_ipv4(self, ip):
        if ip is None or not isinstance(ip, (str, unicode)) or ip.count(" ") != 0:
            return False
        if len(ip.split(".")) != 4:
            return False
        try:
            return all([0 <= int(oct) <= 255 for oct in ip.split(".", 3)])
        except Exception:
            return False

    def validate_ipv6(self, ip):
        if ip is None or not isinstance(ip, (str, unicode)):
            return False
        ip = ip.strip()
        if ip.count(" ") > 0 or ip.count(":") > 7 or ip.count("::") > 1 or ip.count(":::") > 0:
            return False
        if (ip[0] == ":" and ip[:2] != "::") or (ip[-1] == ":" and ip[-2:] != "::"):
            return False
        if ip.count("::") == 0 and ip.count(":") != 7:
            return False
        if ip == "::":
            return True
        if ip[:2] == "::":
            ip = ip.replace("::", "0:")
        elif ip[-2:] == "::":
            ip = ip.replace("::", ":0")
        else:
            ip = ip.replace("::", ":0:")
        try:
            return all([True if (0 <= int(oct, 16) <= 65535) and (1 <= len(oct) <= 4) else False for oct in ip.split(":")])
        except Exception:
            return False

    def validate_hex(self, hex):
        if hex is None or not isinstance(hex, (str, unicode)):
            return False
        try:
            int(hex, 16)
            return True
        except Exception:
            return False

    def validate_integer(self, value, min, max):
        if value is None or not isinstance(value, int):
            return False
        if value < 0:
            return False
        if min is not None and value < min:
            return False
        if max is not None and value > max:
            return False
        return True

    def validate_float(self, value):
        return isinstance(value, (int, float))

    def validate_string(self, value, min_length, max_length):
        if value is None or not isinstance(value, (str, unicode)):
            return False
        if min_length is not None and len(value) < min_length:
            return False
        if max_length is not None and len(value) > max_length:
            return False
        return True

    def validate_bool(self, value):
        return isinstance(value, bool)

    def validate_list(self, value, itemtype, min, max, min_length, max_length):
        if value is None or not isinstance(value, list):
            return False
        v_obj = getattr(self, "validate_{}".format(itemtype), None)
        if v_obj is None:
            raise AttributeError("{} is not a valid attribute".format(itemtype))
        v_obj_lst = []
        for item in value:
            if itemtype == "integer":
                v_obj_lst.append(v_obj(item, min, max))
            elif itemtype == "string":
                v_obj_lst.append(v_obj(item, min_length, max_length))
            else:
                v_obj_lst.append(v_obj(item))
        return v_obj_lst

    def validate_binary(self, value):
        if value is None or not isinstance(value, (str, unicode)):
            return False
        return all([True if int(bin) == 0 or int(bin) == 1 else False for bin in value])

    def types_validation(self, value, type_, err_msg, itemtype=None, min=None, max=None, min_length=None, max_length=None):
        type_map = {int: "integer", str: "string", float: "float", bool: "bool", list: "list", "int64": "integer", "int32": "integer", "double": "float"}
        if type_ in type_map:
            type_ = type_map[type_]
        if itemtype is not None and itemtype in type_map:
            itemtype = type_map[itemtype]
        v_obj = getattr(self, "validate_{}".format(type_), None)
        if v_obj is None:
            msg = "{} is not a valid or unsupported format".format(type_)
            raise TypeError(msg)
        if type_ == "list":
            verdict = v_obj(value, itemtype, min, max, min_length, max_length)
            if all(verdict) is True:
                return
            err_msg = "{} \n {} are not valid".format(err_msg, [value[index] for index, item in enumerate(verdict) if item is False])
            verdict = False
        elif type_ == "integer":
            verdict = v_obj(value, min, max)
            if verdict is True:
                return
            min_max = ""
            if min is not None:
                min_max = ", expected min {}".format(min)
            if max is not None:
                min_max = min_max + ", expected max {}".format(max)
            err_msg = "{} \n got {} of type {} {}".format(err_msg, value, type(value), min_max)
        elif type_ == "string":
            verdict = v_obj(value, min_length, max_length)
            if verdict is True:
                return
            msg = ""
            if min_length is not None:
                msg = ", expected min {}".format(min_length)
            if max_length is not None:
                msg = msg + ", expected max {}".format(max_length)
            err_msg = "{} \n got {} of type {} {}".format(err_msg, value, type(value), msg)
        else:
            verdict = v_obj(value)
        if verdict is False:
            raise TypeError(err_msg)


class OpenApiObject(OpenApiBase, OpenApiValidator):
    """Base class for any /components/schemas object

    Every OpenApiObject is reuseable within the schema so it can
    exist in multiple locations within the hierarchy.
    That means it can exist in multiple locations as a
    leaf, parent/choice or parent.
    """

    __slots__ = ("_properties", "_parent", "_choice")
    _DEFAULTS = {}
    _TYPES = {}
    _REQUIRED = []

    def __init__(self, parent=None, choice=None):
        super(OpenApiObject, self).__init__()
        self._parent = parent
        self._choice = choice
        self._properties = {}

    @property
    def parent(self):
        return self._parent

    def _set_choice(self, name):
        if self._has_choice(name):
            for enum in self._TYPES["choice"]["enum"]:
                if enum in self._properties and name != enum:
                    self._properties.pop(enum)
            self._properties["choice"] = name

    def _has_choice(self, name):
        if "choice" in dir(self) and "_TYPES" in dir(self) and "choice" in self._TYPES and name in self._TYPES["choice"]["enum"]:
            return True
        else:
            return False

    def _get_property(self, name, default_value=None, parent=None, choice=None):
        if name in self._properties and self._properties[name] is not None:
            return self._properties[name]
        if isinstance(default_value, type) is True:
            self._set_choice(name)
            if "_choice" in default_value.__slots__:
                self._properties[name] = default_value(parent=parent, choice=choice)
            else:
                self._properties[name] = default_value(parent=parent)
            if "_DEFAULTS" in dir(self._properties[name]) and "choice" in self._properties[name]._DEFAULTS:
                getattr(self._properties[name], self._properties[name]._DEFAULTS["choice"])
        else:
            if default_value is None and name in self._DEFAULTS:
                self._set_choice(name)
                self._properties[name] = self._DEFAULTS[name]
            else:
                self._properties[name] = default_value
        return self._properties[name]

    def _set_property(self, name, value, choice=None):
        if name in self._DEFAULTS and value is None:
            self._set_choice(name)
            self._properties[name] = self._DEFAULTS[name]
        else:
            self._set_choice(name)
            self._properties[name] = value
        if self._parent is not None and self._choice is not None and value is not None:
            self._parent._set_property("choice", self._choice)

    def _encode(self):
        """Helper method for serialization"""
        output = {}
        self._validate_required()
        for key, value in self._properties.items():
            self._validate_types(key, value)
            if isinstance(value, (OpenApiObject, OpenApiIter)):
                output[key] = value._encode()
            elif value is not None:
                if key in self._TYPES and "format" in self._TYPES[key] and self._TYPES[key]["format"] == "int64":
                    value = str(value)
                output[key] = value
        return output

    def _decode(self, obj):
        dtypes = [list, str, int, float, bool]
        for property_name, property_value in obj.items():
            if property_name in self._TYPES:
                if isinstance(property_value, dict):
                    child = self._get_child_class(property_name)
                    if "choice" in child[1]._TYPES and "_parent" in child[1].__slots__:
                        property_value = child[1](self, property_name)._decode(property_value)
                    elif "_parent" in child[1].__slots__:
                        property_value = child[1](self)._decode(property_value)
                    else:
                        property_value = child[1]()._decode(property_value)
                elif isinstance(property_value, list) and property_name in self._TYPES and self._TYPES[property_name]["type"] not in dtypes:
                    child = self._get_child_class(property_name, True)
                    openapi_list = child[0]()
                    for item in property_value:
                        item = child[1]()._decode(item)
                        openapi_list._items.append(item)
                    property_value = openapi_list
                elif property_name in self._DEFAULTS and property_value is None:
                    if isinstance(self._DEFAULTS[property_name], tuple(dtypes)):
                        property_value = self._DEFAULTS[property_name]
                self._set_choice(property_name)
                if "format" in self._TYPES[property_name] and self._TYPES[property_name]["format"] == "int64":
                    property_value = int(property_value)
                self._properties[property_name] = property_value
            self._validate_types(property_name, property_value)
        self._validate_required()
        return self

    def _get_child_class(self, property_name, is_property_list=False):
        list_class = None
        class_name = self._TYPES[property_name]["type"]
        module = importlib.import_module(self.__module__)
        object_class = getattr(module, class_name)
        if is_property_list is True:
            list_class = object_class
            object_class = getattr(module, class_name[0:-4])
        return (list_class, object_class)

    def __str__(self):
        return self.serialize(encoding=self.YAML)

    def __deepcopy__(self, memo):
        """Creates a deep copy of the current object"""
        return self.__class__().deserialize(self.serialize())

    def __copy__(self):
        """Creates a deep copy of the current object"""
        return self.__deepcopy__(None)

    def __eq__(self, other):
        return self.__str__() == other.__str__()

    def clone(self):
        """Creates a deep copy of the current object"""
        return self.__deepcopy__(None)

    def _validate_required(self):
        """Validates the required properties are set
        Use getattr as it will set any defaults prior to validating
        """
        if getattr(self, "_REQUIRED", None) is None:
            return
        for name in self._REQUIRED:
            if getattr(self, name, None) is None:
                msg = "{} is a mandatory property of {}" " and should not be set to None".format(
                    name,
                    self.__class__,
                )
                raise ValueError(msg)

    def _validate_types(self, property_name, property_value):
        common_data_types = [list, str, int, float, bool]
        if property_name not in self._TYPES:
            # raise ValueError("Invalid Property {}".format(property_name))
            return
        details = self._TYPES[property_name]
        if property_value is None and property_name not in self._DEFAULTS and property_name not in self._REQUIRED:
            return
        if "enum" in details and property_value not in details["enum"]:
            msg = "property {} shall be one of these" " {} enum, but got {} at {}"
            raise TypeError(msg.format(property_name, details["enum"], property_value, self.__class__))
        if details["type"] in common_data_types and "format" not in details:
            msg = "property {} shall be of type {} at {}".format(property_name, details["type"], self.__class__)
            self.types_validation(property_value, details["type"], msg, details.get("itemtype"), details.get("minimum"), details.get("maximum"),
                                  details.get("minLength"), details.get("maxLength"))

        if details["type"] not in common_data_types:
            class_name = details["type"]
            # TODO Need to revisit importlib
            module = importlib.import_module(self.__module__)
            object_class = getattr(module, class_name)
            if not isinstance(property_value, object_class):
                msg = "property {} shall be of type {}," " but got {} at {}"
                raise TypeError(msg.format(property_name, class_name, type(property_value), self.__class__))
        if "format" in details:
            msg = "Invalid {} format, expected {} at {}".format(property_value, details["format"], self.__class__)
            _type = details["type"] if details["type"] is list else details["format"]
            self.types_validation(property_value, _type, msg, details["format"], details.get("minimum"), details.get("maximum"),
                                  details.get("minLength"), details.get("maxLength"))

    def validate(self):
        self._validate_required()
        for key, value in self._properties.items():
            self._validate_types(key, value)

    def get(self, name, with_default=False):
        """
        getattr for openapi object
        """
        if self._properties.get(name) is not None:
            return self._properties[name]
        elif with_default:
            # TODO need to find a way to avoid getattr
            choice = self._properties.get("choice") if "choice" in dir(self) else None
            getattr(self, name)
            if "choice" in dir(self):
                if choice is None and "choice" in self._properties:
                    self._properties.pop("choice")
                else:
                    self._properties["choice"] = choice
            return self._properties.pop(name)
        return None


class OpenApiIter(OpenApiBase):
    """Container class for OpenApiObject

    Inheriting classes contain 0..n instances of an OpenAPI components/schemas
    object.
    - config.flows.flow(name="1").flow(name="2").flow(name="3")

    The __getitem__ method allows getting an instance using ordinal.
    - config.flows[0]
    - config.flows[1:]
    - config.flows[0:1]
    - f1, f2, f3 = config.flows

    The __iter__ method allows for iterating across the encapsulated contents
    - for flow in config.flows:
    """

    __slots__ = ("_index", "_items")
    _GETITEM_RETURNS_CHOICE_OBJECT = False

    def __init__(self):
        super(OpenApiIter, self).__init__()
        self._index = -1
        self._items = []

    def __len__(self):
        return len(self._items)

    def _getitem(self, key):
        found = None
        if isinstance(key, int):
            found = self._items[key]
        elif isinstance(key, slice) is True:
            start, stop, step = key.indices(len(self))
            sliced = self.__class__()
            for i in range(start, stop, step):
                sliced._items.append(self._items[i])
            return sliced
        elif isinstance(key, str):
            for item in self._items:
                if item.name == key:
                    found = item
        if found is None:
            raise IndexError()
        if self._GETITEM_RETURNS_CHOICE_OBJECT is True and found._properties.get("choice") is not None:
            return found._properties[found._properties["choice"]]
        return found

    def _iter(self):
        self._index = -1
        return self

    def _next(self):
        if self._index + 1 >= len(self._items):
            raise StopIteration
        else:
            self._index += 1
        return self.__getitem__(self._index)

    def __getitem__(self, key):
        raise NotImplementedError("This should be overridden by the generator")

    def _add(self, item):
        self._items.append(item)
        self._index = len(self._items) - 1

    def remove(self, index):
        del self._items[index]
        self._index = len(self._items) - 1

    def append(self, item):
        """Append an item to the end of OpenApiIter
        TBD: type check, raise error on mismatch
        """
        if isinstance(item, OpenApiObject) is False:
            raise Exception("Item is not an instance of OpenApiObject")
        self._add(item)
        return self

    def clear(self):
        del self._items[:]
        self._index = -1

    def _encode(self):
        return [item._encode() for item in self._items]

    def _decode(self, encoded_list):
        item_class_name = self.__class__.__name__.replace("Iter", "")
        module = importlib.import_module(self.__module__)
        object_class = getattr(module, item_class_name)
        self.clear()
        for item in encoded_list:
            self._add(object_class()._decode(item))

    def __copy__(self):
        raise NotImplementedError("Shallow copy of OpenApiIter objects is not supported")

    def __deepcopy__(self, memo):
        raise NotImplementedError("Deep copy of OpenApiIter objects is not supported")

    def __str__(self):
        return yaml.safe_dump(self._encode())

    def __eq__(self, other):
        return self.__str__() == other.__str__()


class Config(OpenApiObject):
    __slots__ = ('_parent')

    _TYPES = {
        'hosts': {'type': 'HostIter'},
        'fabric': {'type': 'Fabric'},
    } # type: Dict[str, str]

    _REQUIRED= () # type: tuple(str)

    _DEFAULTS= {} # type: Dict[str, Union(type)]

    def __init__(self, parent=None):
        super(Config, self).__init__()
        self._parent = parent

    @property
    def hosts(self):
        # type: () -> HostIter
        """hosts getter

        TBD

        Returns: HostIter
        """
        return self._get_property('hosts', HostIter, self._parent, self._choice)

    @property
    def fabric(self):
        # type: () -> Fabric
        """fabric getter

        

        Returns: Fabric
        """
        return self._get_property('fabric', Fabric)


class Host(OpenApiObject):
    __slots__ = ('_parent')

    _TYPES = {
        'name': {'type': str},
        'address': {'type': str},
        'prefix': {'type': int},
    } # type: Dict[str, str]

    _REQUIRED = ('address', 'name') # type: tuple(str)

    _DEFAULTS = {
        'prefix': 24,
    } # type: Dict[str, Union(type)]

    def __init__(self, parent=None, name=None, address=None, prefix=24):
        super(Host, self).__init__()
        self._parent = parent
        self._set_property('name', name)
        self._set_property('address', address)
        self._set_property('prefix', prefix)

    @property
    def name(self):
        # type: () -> str
        """name getter

        The name, uniquely identifying the host

        Returns: str
        """
        return self._get_property('name')

    @name.setter
    def name(self, value):
        """name setter

        The name, uniquely identifying the host

        value: str
        """
        self._set_property('name', value)

    @property
    def address(self):
        # type: () -> str
        """address getter

        The test address of the host

        Returns: str
        """
        return self._get_property('address')

    @address.setter
    def address(self, value):
        """address setter

        The test address of the host

        value: str
        """
        self._set_property('address', value)

    @property
    def prefix(self):
        # type: () -> int
        """prefix getter

        The prefix of the host

        Returns: int
        """
        return self._get_property('prefix')

    @prefix.setter
    def prefix(self, value):
        """prefix setter

        The prefix of the host

        value: int
        """
        self._set_property('prefix', value)


class HostIter(OpenApiIter):
    __slots__ = ('_parent', '_choice')

    _GETITEM_RETURNS_CHOICE_OBJECT = False

    def __init__(self, parent=None, choice=None):
        super(HostIter, self).__init__()
        self._parent = parent
        self._choice = choice

    def __getitem__(self, key):
        # type: (str) -> Union[Host]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> HostIter
        return self._iter()

    def __next__(self):
        # type: () -> Host
        return self._next()

    def next(self):
        # type: () -> Host
        return self._next()

    def host(self, name=None, address=None, prefix=24):
        # type: (str,str,int) -> HostIter
        """Factory method that creates an instance of the Host class

        TBD

        Returns: HostIter
        """
        item = Host(parent=self._parent, name=name, address=address, prefix=prefix)
        self._add(item)
        return self

    def add(self, name=None, address=None, prefix=24):
        # type: (str,str,int) -> Host
        """Add method that creates and returns an instance of the Host class

        TBD

        Returns: Host
        """
        item = Host(parent=self._parent, name=name, address=address, prefix=prefix)
        self._add(item)
        return item


class Fabric(OpenApiObject):
    __slots__ = ('_parent','_choice')

    _TYPES = {
        'choice': {
            'type': str,
            'enum': [
                'clos',
            ],
        },
        'clos': {'type': 'FabricClos'},
        'qos_profiles': {'type': 'FabricQosProfileIter'},
        'layer1_profiles': {'type': 'FabricL1SettingsProfileIter'},
    } # type: Dict[str, str]

    _REQUIRED= () # type: tuple(str)

    _DEFAULTS= {} # type: Dict[str, Union(type)]

    CLOS = 'clos' # type: str

    def __init__(self, parent=None, choice=None):
        super(Fabric, self).__init__()
        self._parent = parent
        if 'choice' in self._DEFAULTS and choice is None:
            getattr(self, self._DEFAULTS['choice'])
        else:
            self.choice = choice

    @property
    def clos(self):
        # type: () -> FabricClos
        """Factory property that returns an instance of the FabricClos class

        An emulation of a multistage switch topology. When folded, results in a topology with (up to) 3 tiers identified as . spine, pod and tor tier.

        Returns: FabricClos
        """
        return self._get_property('clos', FabricClos, self, 'clos')

    @property
    def choice(self):
        # type: () -> Union[Literal["clos"]]
        """choice getter

        TBD

        Returns: Union[Literal["clos"]]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[Literal["clos"]]
        """
        self._set_property('choice', value)

    @property
    def qos_profiles(self):
        # type: () -> FabricQosProfileIter
        """qos_profiles getter

        A list of Quality of Service (QoS) profiles

        Returns: FabricQosProfileIter
        """
        return self._get_property('qos_profiles', FabricQosProfileIter, self._parent, self._choice)

    @property
    def layer1_profiles(self):
        # type: () -> FabricL1SettingsProfileIter
        """layer1_profiles getter

        A list of Layer 1 settings profiles

        Returns: FabricL1SettingsProfileIter
        """
        return self._get_property('layer1_profiles', FabricL1SettingsProfileIter, self._parent, self._choice)


class FabricClos(OpenApiObject):
    __slots__ = ('_parent')

    _TYPES = {
        'spine': {'type': 'FabricSpine'},
        'pods': {'type': 'FabricPodIter'},
        'host_links': {'type': 'SwitchHostLinkIter'},
        'pod_profiles': {'type': 'FabricPodProfileIter'},
        'tor_profiles': {'type': 'FabricTorProfileIter'},
        'parallel_fabric_count': {'type': int},
    } # type: Dict[str, str]

    _REQUIRED= () # type: tuple(str)

    _DEFAULTS = {
        'parallel_fabric_count': 1,
    } # type: Dict[str, Union(type)]

    def __init__(self, parent=None, parallel_fabric_count=1):
        super(FabricClos, self).__init__()
        self._parent = parent
        self._set_property('parallel_fabric_count', parallel_fabric_count)

    @property
    def spine(self):
        # type: () -> FabricSpine
        """spine getter

        

        Returns: FabricSpine
        """
        return self._get_property('spine', FabricSpine)

    @property
    def pods(self):
        # type: () -> FabricPodIter
        """pods getter

        The pods in the topology.

        Returns: FabricPodIter
        """
        return self._get_property('pods', FabricPodIter, self._parent, self._choice)

    @property
    def host_links(self):
        # type: () -> SwitchHostLinkIter
        """host_links getter

        TBD

        Returns: SwitchHostLinkIter
        """
        return self._get_property('host_links', SwitchHostLinkIter, self._parent, self._choice)

    @property
    def pod_profiles(self):
        # type: () -> FabricPodProfileIter
        """pod_profiles getter

        A list of pod profiles

        Returns: FabricPodProfileIter
        """
        return self._get_property('pod_profiles', FabricPodProfileIter, self._parent, self._choice)

    @property
    def tor_profiles(self):
        # type: () -> FabricTorProfileIter
        """tor_profiles getter

        A list of ToR switch profiles

        Returns: FabricTorProfileIter
        """
        return self._get_property('tor_profiles', FabricTorProfileIter, self._parent, self._choice)

    @property
    def parallel_fabric_count(self):
        # type: () -> int
        """parallel_fabric_count getter

        Number of parallel fabrics (aka fabric colors). Spine and pod switches . are fully meshed within a fabric

        Returns: int
        """
        return self._get_property('parallel_fabric_count')

    @parallel_fabric_count.setter
    def parallel_fabric_count(self, value):
        """parallel_fabric_count setter

        Number of parallel fabrics (aka fabric colors). Spine and pod switches . are fully meshed within a fabric

        value: int
        """
        self._set_property('parallel_fabric_count', value)


class FabricSpine(OpenApiObject):
    __slots__ = ('_parent')

    _TYPES = {
        'count': {'type': int},
        'downlink_ecmp_mode': {
            'type': str,
            'enum': [
                'random_spray',
                'hash_3_tuple',
                'hash_5_tuple',
            ],
        },
        'qos_profile_name': {'type': str},
    } # type: Dict[str, str]

    _REQUIRED= () # type: tuple(str)

    _DEFAULTS = {
        'count': 1,
    } # type: Dict[str, Union(type)]

    RANDOM_SPRAY = 'random_spray' # type: str
    HASH_3_TUPLE = 'hash_3_tuple' # type: str
    HASH_5_TUPLE = 'hash_5_tuple' # type: str

    def __init__(self, parent=None, count=1, downlink_ecmp_mode=None, qos_profile_name=None):
        super(FabricSpine, self).__init__()
        self._parent = parent
        self._set_property('count', count)
        self._set_property('downlink_ecmp_mode', downlink_ecmp_mode)
        self._set_property('qos_profile_name', qos_profile_name)

    @property
    def count(self):
        # type: () -> int
        """count getter

        The number of spines to be created with each spine sharing the same. downlink_ecmp_mode and qos_profile_name properties.

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        The number of spines to be created with each spine sharing the same. downlink_ecmp_mode and qos_profile_name properties.

        value: int
        """
        self._set_property('count', value)

    @property
    def downlink_ecmp_mode(self):
        # type: () -> Union[Literal["hash_3_tuple"], Literal["hash_5_tuple"], Literal["random_spray"]]
        """downlink_ecmp_mode getter

        The algorithm for packet distribution over ECMP links.. - random_spray randomly puts each packet on an ECMP member links . - hash_3_tuple is a 3 tuple hash of ipv4 src, dst, protocol. - hash_5_tuple is static_hash_ipv4_l4 but a different resulting RTAG7 hash mode

        Returns: Union[Literal["hash_3_tuple"], Literal["hash_5_tuple"], Literal["random_spray"]]
        """
        return self._get_property('downlink_ecmp_mode')

    @downlink_ecmp_mode.setter
    def downlink_ecmp_mode(self, value):
        """downlink_ecmp_mode setter

        The algorithm for packet distribution over ECMP links.. - random_spray randomly puts each packet on an ECMP member links . - hash_3_tuple is a 3 tuple hash of ipv4 src, dst, protocol. - hash_5_tuple is static_hash_ipv4_l4 but a different resulting RTAG7 hash mode

        value: Union[Literal["hash_3_tuple"], Literal["hash_5_tuple"], Literal["random_spray"]]
        """
        self._set_property('downlink_ecmp_mode', value)

    @property
    def qos_profile_name(self):
        # type: () -> str
        """qos_profile_name getter

        The name of a qos profile shared by the spines.. . x-constraint:. - #/components/schemas/QosProfile/properties/name. 

        Returns: str
        """
        return self._get_property('qos_profile_name')

    @qos_profile_name.setter
    def qos_profile_name(self, value):
        """qos_profile_name setter

        The name of a qos profile shared by the spines.. . x-constraint:. - #/components/schemas/QosProfile/properties/name. 

        value: str
        """
        self._set_property('qos_profile_name', value)


class FabricPod(OpenApiObject):
    __slots__ = ('_parent')

    _TYPES = {
        'count': {'type': int},
        'pod_profile_name': {'type': str},
    } # type: Dict[str, str]

    _REQUIRED= () # type: tuple(str)

    _DEFAULTS = {
        'count': 1,
    } # type: Dict[str, Union(type)]

    def __init__(self, parent=None, count=1, pod_profile_name=None):
        super(FabricPod, self).__init__()
        self._parent = parent
        self._set_property('count', count)
        self._set_property('pod_profile_name', pod_profile_name)

    @property
    def count(self):
        # type: () -> int
        """count getter

        The number of pods that will share the same profile

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        The number of pods that will share the same profile

        value: int
        """
        self._set_property('count', value)

    @property
    def pod_profile_name(self):
        # type: () -> str
        """pod_profile_name getter

        The pod profile associated with the pod(s).. . x-constraint:. - #/components/schemas/PodProfile/properties/name. 

        Returns: str
        """
        return self._get_property('pod_profile_name')

    @pod_profile_name.setter
    def pod_profile_name(self, value):
        """pod_profile_name setter

        The pod profile associated with the pod(s).. . x-constraint:. - #/components/schemas/PodProfile/properties/name. 

        value: str
        """
        self._set_property('pod_profile_name', value)


class FabricPodIter(OpenApiIter):
    __slots__ = ('_parent', '_choice')

    _GETITEM_RETURNS_CHOICE_OBJECT = False

    def __init__(self, parent=None, choice=None):
        super(FabricPodIter, self).__init__()
        self._parent = parent
        self._choice = choice

    def __getitem__(self, key):
        # type: (str) -> Union[FabricPod]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> FabricPodIter
        return self._iter()

    def __next__(self):
        # type: () -> FabricPod
        return self._next()

    def next(self):
        # type: () -> FabricPod
        return self._next()

    def pod(self, count=1, pod_profile_name=None):
        # type: (int,str) -> FabricPodIter
        """Factory method that creates an instance of the FabricPod class

        TBD

        Returns: FabricPodIter
        """
        item = FabricPod(parent=self._parent, count=count, pod_profile_name=pod_profile_name)
        self._add(item)
        return self

    def add(self, count=1, pod_profile_name=None):
        # type: (int,str) -> FabricPod
        """Add method that creates and returns an instance of the FabricPod class

        TBD

        Returns: FabricPod
        """
        item = FabricPod(parent=self._parent, count=count, pod_profile_name=pod_profile_name)
        self._add(item)
        return item


class SwitchHostLink(OpenApiObject):
    __slots__ = ('_parent','_choice')

    _TYPES = {
        'host_name': {'type': str},
        'host_type': {
            'type': str,
            'enum': [
                'external',
                'internal_traffic_sink',
            ],
        },
        'front_panel_port': {'type': int},
        'l1_profile_name': {'type': str},
        'choice': {
            'type': str,
            'enum': [
                'spine',
                'pod',
                'tor',
            ],
        },
        'spine': {
            'type': int,
            'minimum': 1,
        },
        'pod': {'type': 'SwitchHostLinkSwitchRef'},
        'tor': {'type': 'SwitchHostLinkSwitchRef'},
    } # type: Dict[str, str]

    _REQUIRED = ('host_name',) # type: tuple(str)

    _DEFAULTS = {
        'host_type': 'external',
        'choice': 'tor',
    } # type: Dict[str, Union(type)]

    EXTERNAL = 'external' # type: str
    INTERNAL_TRAFFIC_SINK = 'internal_traffic_sink' # type: str

    SPINE = 'spine' # type: str
    POD = 'pod' # type: str
    TOR = 'tor' # type: str

    def __init__(self, parent=None, choice=None, host_name=None, host_type='external', front_panel_port=None, l1_profile_name=None, spine=None):
        super(SwitchHostLink, self).__init__()
        self._parent = parent
        self._set_property('host_name', host_name)
        self._set_property('host_type', host_type)
        self._set_property('front_panel_port', front_panel_port)
        self._set_property('l1_profile_name', l1_profile_name)
        self._set_property('spine', spine)
        if 'choice' in self._DEFAULTS and choice is None:
            getattr(self, self._DEFAULTS['choice'])
        else:
            self.choice = choice

    @property
    def pod(self):
        # type: () -> SwitchHostLinkSwitchRef
        """Factory property that returns an instance of the SwitchHostLinkSwitchRef class

        Location of the switch based on pod and switch index

        Returns: SwitchHostLinkSwitchRef
        """
        return self._get_property('pod', SwitchHostLinkSwitchRef, self, 'pod')

    @property
    def tor(self):
        # type: () -> SwitchHostLinkSwitchRef
        """Factory property that returns an instance of the SwitchHostLinkSwitchRef class

        Location of the switch based on pod and switch index

        Returns: SwitchHostLinkSwitchRef
        """
        return self._get_property('tor', SwitchHostLinkSwitchRef, self, 'tor')

    @property
    def host_name(self):
        # type: () -> str
        """host_name getter

        TBD. . x-constraint:. - #components/schemas/Host/properties/name. 

        Returns: str
        """
        return self._get_property('host_name')

    @host_name.setter
    def host_name(self, value):
        """host_name setter

        TBD. . x-constraint:. - #components/schemas/Host/properties/name. 

        value: str
        """
        self._set_property('host_name', value)

    @property
    def host_type(self):
        # type: () -> Union[Literal["external"], Literal["internal_traffic_sink"]]
        """host_type getter

        Optional host type, if fabric is rendered on physical box.. - external for hosts/servers physically connected to front panel ports. - internal_traffic_sink for an emulated server that acts as a traffic sink (i.e. packets sent to its IP address will be routed through the emulated fabric)

        Returns: Union[Literal["external"], Literal["internal_traffic_sink"]]
        """
        return self._get_property('host_type')

    @host_type.setter
    def host_type(self, value):
        """host_type setter

        Optional host type, if fabric is rendered on physical box.. - external for hosts/servers physically connected to front panel ports. - internal_traffic_sink for an emulated server that acts as a traffic sink (i.e. packets sent to its IP address will be routed through the emulated fabric)

        value: Union[Literal["external"], Literal["internal_traffic_sink"]]
        """
        self._set_property('host_type', value)

    @property
    def front_panel_port(self):
        # type: () -> int
        """front_panel_port getter

        Optional front panel port number, if fabric is rendered on physical box

        Returns: int
        """
        return self._get_property('front_panel_port')

    @front_panel_port.setter
    def front_panel_port(self, value):
        """front_panel_port setter

        Optional front panel port number, if fabric is rendered on physical box

        value: int
        """
        self._set_property('front_panel_port', value)

    @property
    def l1_profile_name(self):
        # type: () -> str
        """l1_profile_name getter

        The layer 1 settings profile associated with the host/front panel port.. . x-constraint:. - #/components/schemas/Fabric.L1SettingsProfile/properties/name. 

        Returns: str
        """
        return self._get_property('l1_profile_name')

    @l1_profile_name.setter
    def l1_profile_name(self, value):
        """l1_profile_name setter

        The layer 1 settings profile associated with the host/front panel port.. . x-constraint:. - #/components/schemas/Fabric.L1SettingsProfile/properties/name. 

        value: str
        """
        self._set_property('l1_profile_name', value)

    @property
    def choice(self):
        # type: () -> Union[Literal["pod"], Literal["spine"], Literal["tor"]]
        """choice getter

        TBD

        Returns: Union[Literal["pod"], Literal["spine"], Literal["tor"]]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[Literal["pod"], Literal["spine"], Literal["tor"]]
        """
        self._set_property('choice', value)

    @property
    def spine(self):
        # type: () -> int
        """spine getter

        One based index of the spine switch based on the number of spines . configured in the clos topology.

        Returns: int
        """
        return self._get_property('spine')

    @spine.setter
    def spine(self, value):
        """spine setter

        One based index of the spine switch based on the number of spines . configured in the clos topology.

        value: int
        """
        self._set_property('spine', value, 'spine')


class SwitchHostLinkSwitchRef(OpenApiObject):
    __slots__ = ('_parent')

    _TYPES = {
        'pod_index': {
            'type': int,
            'minimum': 1,
        },
        'switch_index': {
            'type': int,
            'minimum': 1,
        },
    } # type: Dict[str, str]

    _REQUIRED= () # type: tuple(str)

    _DEFAULTS = {
        'pod_index': 1,
        'switch_index': 1,
    } # type: Dict[str, Union(type)]

    def __init__(self, parent=None, pod_index=1, switch_index=1):
        super(SwitchHostLinkSwitchRef, self).__init__()
        self._parent = parent
        self._set_property('pod_index', pod_index)
        self._set_property('switch_index', switch_index)

    @property
    def pod_index(self):
        # type: () -> int
        """pod_index getter

        One-based index of the pod based on the number of pods in the fabric

        Returns: int
        """
        return self._get_property('pod_index')

    @pod_index.setter
    def pod_index(self, value):
        """pod_index setter

        One-based index of the pod based on the number of pods in the fabric

        value: int
        """
        self._set_property('pod_index', value)

    @property
    def switch_index(self):
        # type: () -> int
        """switch_index getter

        One-based index of the pod or ToR switch in the indicated pod

        Returns: int
        """
        return self._get_property('switch_index')

    @switch_index.setter
    def switch_index(self, value):
        """switch_index setter

        One-based index of the pod or ToR switch in the indicated pod

        value: int
        """
        self._set_property('switch_index', value)


class SwitchHostLinkIter(OpenApiIter):
    __slots__ = ('_parent', '_choice')

    _GETITEM_RETURNS_CHOICE_OBJECT = False

    def __init__(self, parent=None, choice=None):
        super(SwitchHostLinkIter, self).__init__()
        self._parent = parent
        self._choice = choice

    def __getitem__(self, key):
        # type: (str) -> Union[SwitchHostLink, SwitchHostLinkSwitchRef]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> SwitchHostLinkIter
        return self._iter()

    def __next__(self):
        # type: () -> SwitchHostLink
        return self._next()

    def next(self):
        # type: () -> SwitchHostLink
        return self._next()

    def switchhostlink(self, host_name=None, host_type='external', front_panel_port=None, l1_profile_name=None, spine=None):
        # type: (str,Union[Literal["external"], Literal["internal_traffic_sink"]],int,str,int) -> SwitchHostLinkIter
        """Factory method that creates an instance of the SwitchHostLink class

        The ingress point of a host which is the index of a spine, pod or tor switch.

        Returns: SwitchHostLinkIter
        """
        item = SwitchHostLink(parent=self._parent, choice=self._choice, host_name=host_name, host_type=host_type, front_panel_port=front_panel_port, l1_profile_name=l1_profile_name, spine=spine)
        self._add(item)
        return self

    def add(self, host_name=None, host_type='external', front_panel_port=None, l1_profile_name=None, spine=None):
        # type: (str,Union[Literal["external"], Literal["internal_traffic_sink"]],int,str,int) -> SwitchHostLink
        """Add method that creates and returns an instance of the SwitchHostLink class

        The ingress point of a host which is the index of a spine, pod or tor switch.

        Returns: SwitchHostLink
        """
        item = SwitchHostLink(parent=self._parent, choice=self._choice, host_name=host_name, host_type=host_type, front_panel_port=front_panel_port, l1_profile_name=l1_profile_name, spine=spine)
        self._add(item)
        return item


class FabricPodProfile(OpenApiObject):
    __slots__ = ('_parent')

    _TYPES = {
        'name': {'type': str},
        'pod_switch': {'type': 'FabricPodSwitch'},
        'tors': {'type': 'FabricTorIter'},
        'pod_to_spine_oversubscription': {'type': str},
    } # type: Dict[str, str]

    _REQUIRED= () # type: tuple(str)

    _DEFAULTS= {} # type: Dict[str, Union(type)]

    def __init__(self, parent=None, name=None, pod_to_spine_oversubscription=None):
        super(FabricPodProfile, self).__init__()
        self._parent = parent
        self._set_property('name', name)
        self._set_property('pod_to_spine_oversubscription', pod_to_spine_oversubscription)

    @property
    def name(self):
        # type: () -> str
        """name getter

        Uniquely identifies a pod profile

        Returns: str
        """
        return self._get_property('name')

    @name.setter
    def name(self, value):
        """name setter

        Uniquely identifies a pod profile

        value: str
        """
        self._set_property('name', value)

    @property
    def pod_switch(self):
        # type: () -> FabricPodSwitch
        """pod_switch getter

        

        Returns: FabricPodSwitch
        """
        return self._get_property('pod_switch', FabricPodSwitch)

    @property
    def tors(self):
        # type: () -> FabricTorIter
        """tors getter

        The ToRs in the pod

        Returns: FabricTorIter
        """
        return self._get_property('tors', FabricTorIter, self._parent, self._choice)

    @property
    def pod_to_spine_oversubscription(self):
        # type: () -> str
        """pod_to_spine_oversubscription getter

        Oversubscription ratio of the pod switches

        Returns: str
        """
        return self._get_property('pod_to_spine_oversubscription')

    @pod_to_spine_oversubscription.setter
    def pod_to_spine_oversubscription(self, value):
        """pod_to_spine_oversubscription setter

        Oversubscription ratio of the pod switches

        value: str
        """
        self._set_property('pod_to_spine_oversubscription', value)


class FabricPodSwitch(OpenApiObject):
    __slots__ = ('_parent')

    _TYPES = {
        'count': {'type': int},
        'uplink_ecmp_mode': {
            'type': str,
            'enum': [
                'random_spray',
                'hash_3_tuple',
                'hash_5_tuple',
            ],
        },
        'downlink_ecmp_mode': {
            'type': str,
            'enum': [
                'random_spray',
                'hash_3_tuple',
                'hash_5_tuple',
            ],
        },
        'qos_profile_name': {'type': str},
    } # type: Dict[str, str]

    _REQUIRED= () # type: tuple(str)

    _DEFAULTS = {
        'count': 1,
    } # type: Dict[str, Union(type)]

    RANDOM_SPRAY = 'random_spray' # type: str
    HASH_3_TUPLE = 'hash_3_tuple' # type: str
    HASH_5_TUPLE = 'hash_5_tuple' # type: str

    RANDOM_SPRAY = 'random_spray' # type: str
    HASH_3_TUPLE = 'hash_3_tuple' # type: str
    HASH_5_TUPLE = 'hash_5_tuple' # type: str

    def __init__(self, parent=None, count=1, uplink_ecmp_mode=None, downlink_ecmp_mode=None, qos_profile_name=None):
        super(FabricPodSwitch, self).__init__()
        self._parent = parent
        self._set_property('count', count)
        self._set_property('uplink_ecmp_mode', uplink_ecmp_mode)
        self._set_property('downlink_ecmp_mode', downlink_ecmp_mode)
        self._set_property('qos_profile_name', qos_profile_name)

    @property
    def count(self):
        # type: () -> int
        """count getter

        TBD

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        TBD

        value: int
        """
        self._set_property('count', value)

    @property
    def uplink_ecmp_mode(self):
        # type: () -> Union[Literal["hash_3_tuple"], Literal["hash_5_tuple"], Literal["random_spray"]]
        """uplink_ecmp_mode getter

        The algorithm for packet distribution over ECMP links.. - random_spray randomly puts each packet on an ECMP member links . - hash_3_tuple is a 3 tuple hash of ipv4 src, dst, protocol. - hash_5_tuple is static_hash_ipv4_l4 but a different resulting RTAG7 hash mode

        Returns: Union[Literal["hash_3_tuple"], Literal["hash_5_tuple"], Literal["random_spray"]]
        """
        return self._get_property('uplink_ecmp_mode')

    @uplink_ecmp_mode.setter
    def uplink_ecmp_mode(self, value):
        """uplink_ecmp_mode setter

        The algorithm for packet distribution over ECMP links.. - random_spray randomly puts each packet on an ECMP member links . - hash_3_tuple is a 3 tuple hash of ipv4 src, dst, protocol. - hash_5_tuple is static_hash_ipv4_l4 but a different resulting RTAG7 hash mode

        value: Union[Literal["hash_3_tuple"], Literal["hash_5_tuple"], Literal["random_spray"]]
        """
        self._set_property('uplink_ecmp_mode', value)

    @property
    def downlink_ecmp_mode(self):
        # type: () -> Union[Literal["hash_3_tuple"], Literal["hash_5_tuple"], Literal["random_spray"]]
        """downlink_ecmp_mode getter

        The algorithm for packet distribution over ECMP links.. - random_spray randomly puts each packet on an ECMP member links . - hash_3_tuple is a 3 tuple hash of ipv4 src, dst, protocol. - hash_5_tuple is static_hash_ipv4_l4 but a different resulting RTAG7 hash mode

        Returns: Union[Literal["hash_3_tuple"], Literal["hash_5_tuple"], Literal["random_spray"]]
        """
        return self._get_property('downlink_ecmp_mode')

    @downlink_ecmp_mode.setter
    def downlink_ecmp_mode(self, value):
        """downlink_ecmp_mode setter

        The algorithm for packet distribution over ECMP links.. - random_spray randomly puts each packet on an ECMP member links . - hash_3_tuple is a 3 tuple hash of ipv4 src, dst, protocol. - hash_5_tuple is static_hash_ipv4_l4 but a different resulting RTAG7 hash mode

        value: Union[Literal["hash_3_tuple"], Literal["hash_5_tuple"], Literal["random_spray"]]
        """
        self._set_property('downlink_ecmp_mode', value)

    @property
    def qos_profile_name(self):
        # type: () -> str
        """qos_profile_name getter

        The name of a qos profile associated with the switches in this pod.. . x-constraint:. - #/components/schemas/QosProfile/properties/name. 

        Returns: str
        """
        return self._get_property('qos_profile_name')

    @qos_profile_name.setter
    def qos_profile_name(self, value):
        """qos_profile_name setter

        The name of a qos profile associated with the switches in this pod.. . x-constraint:. - #/components/schemas/QosProfile/properties/name. 

        value: str
        """
        self._set_property('qos_profile_name', value)


class FabricTor(OpenApiObject):
    __slots__ = ('_parent')

    _TYPES = {
        'count': {'type': int},
        'tor_profile_name': {'type': str},
    } # type: Dict[str, str]

    _REQUIRED= () # type: tuple(str)

    _DEFAULTS = {
        'count': 1,
    } # type: Dict[str, Union(type)]

    def __init__(self, parent=None, count=1, tor_profile_name=None):
        super(FabricTor, self).__init__()
        self._parent = parent
        self._set_property('count', count)
        self._set_property('tor_profile_name', tor_profile_name)

    @property
    def count(self):
        # type: () -> int
        """count getter

        number of ToR switches that will share the same profile

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        number of ToR switches that will share the same profile

        value: int
        """
        self._set_property('count', value)

    @property
    def tor_profile_name(self):
        # type: () -> str
        """tor_profile_name getter

        The names of ToR profiles associated with the ToR switch(es). . x-constraint:. - #/components/schemas/TorProfile/properties/name. 

        Returns: str
        """
        return self._get_property('tor_profile_name')

    @tor_profile_name.setter
    def tor_profile_name(self, value):
        """tor_profile_name setter

        The names of ToR profiles associated with the ToR switch(es). . x-constraint:. - #/components/schemas/TorProfile/properties/name. 

        value: str
        """
        self._set_property('tor_profile_name', value)


class FabricTorIter(OpenApiIter):
    __slots__ = ('_parent', '_choice')

    _GETITEM_RETURNS_CHOICE_OBJECT = False

    def __init__(self, parent=None, choice=None):
        super(FabricTorIter, self).__init__()
        self._parent = parent
        self._choice = choice

    def __getitem__(self, key):
        # type: (str) -> Union[FabricTor]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> FabricTorIter
        return self._iter()

    def __next__(self):
        # type: () -> FabricTor
        return self._next()

    def next(self):
        # type: () -> FabricTor
        return self._next()

    def tor(self, count=1, tor_profile_name=None):
        # type: (int,str) -> FabricTorIter
        """Factory method that creates an instance of the FabricTor class

        TBD

        Returns: FabricTorIter
        """
        item = FabricTor(parent=self._parent, count=count, tor_profile_name=tor_profile_name)
        self._add(item)
        return self

    def add(self, count=1, tor_profile_name=None):
        # type: (int,str) -> FabricTor
        """Add method that creates and returns an instance of the FabricTor class

        TBD

        Returns: FabricTor
        """
        item = FabricTor(parent=self._parent, count=count, tor_profile_name=tor_profile_name)
        self._add(item)
        return item


class FabricPodProfileIter(OpenApiIter):
    __slots__ = ('_parent', '_choice')

    _GETITEM_RETURNS_CHOICE_OBJECT = False

    def __init__(self, parent=None, choice=None):
        super(FabricPodProfileIter, self).__init__()
        self._parent = parent
        self._choice = choice

    def __getitem__(self, key):
        # type: (str) -> Union[FabricPodProfile]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> FabricPodProfileIter
        return self._iter()

    def __next__(self):
        # type: () -> FabricPodProfile
        return self._next()

    def next(self):
        # type: () -> FabricPodProfile
        return self._next()

    def podprofile(self, name=None, pod_to_spine_oversubscription=None):
        # type: (str,str) -> FabricPodProfileIter
        """Factory method that creates an instance of the FabricPodProfile class

        TBD

        Returns: FabricPodProfileIter
        """
        item = FabricPodProfile(parent=self._parent, name=name, pod_to_spine_oversubscription=pod_to_spine_oversubscription)
        self._add(item)
        return self

    def add(self, name=None, pod_to_spine_oversubscription=None):
        # type: (str,str) -> FabricPodProfile
        """Add method that creates and returns an instance of the FabricPodProfile class

        TBD

        Returns: FabricPodProfile
        """
        item = FabricPodProfile(parent=self._parent, name=name, pod_to_spine_oversubscription=pod_to_spine_oversubscription)
        self._add(item)
        return item


class FabricTorProfile(OpenApiObject):
    __slots__ = ('_parent')

    _TYPES = {
        'name': {'type': str},
        'tor_mode': {
            'type': str,
            'enum': [
                'layer2',
                'layer3',
            ],
        },
        'uplink_ecmp_mode': {
            'type': str,
            'enum': [
                'random_spray',
                'hash_3_tuple',
                'hash_5_tuple',
            ],
        },
        'qos_profile_name': {'type': str},
        'tor_to_pod_oversubscription': {'type': str},
    } # type: Dict[str, str]

    _REQUIRED= () # type: tuple(str)

    _DEFAULTS= {} # type: Dict[str, Union(type)]

    LAYER2 = 'layer2' # type: str
    LAYER3 = 'layer3' # type: str

    RANDOM_SPRAY = 'random_spray' # type: str
    HASH_3_TUPLE = 'hash_3_tuple' # type: str
    HASH_5_TUPLE = 'hash_5_tuple' # type: str

    def __init__(self, parent=None, name=None, tor_mode=None, uplink_ecmp_mode=None, qos_profile_name=None, tor_to_pod_oversubscription=None):
        super(FabricTorProfile, self).__init__()
        self._parent = parent
        self._set_property('name', name)
        self._set_property('tor_mode', tor_mode)
        self._set_property('uplink_ecmp_mode', uplink_ecmp_mode)
        self._set_property('qos_profile_name', qos_profile_name)
        self._set_property('tor_to_pod_oversubscription', tor_to_pod_oversubscription)

    @property
    def name(self):
        # type: () -> str
        """name getter

        TBD

        Returns: str
        """
        return self._get_property('name')

    @name.setter
    def name(self, value):
        """name setter

        TBD

        value: str
        """
        self._set_property('name', value)

    @property
    def tor_mode(self):
        # type: () -> Union[Literal["layer2"], Literal["layer3"]]
        """tor_mode getter

        ToR switch mode

        Returns: Union[Literal["layer2"], Literal["layer3"]]
        """
        return self._get_property('tor_mode')

    @tor_mode.setter
    def tor_mode(self, value):
        """tor_mode setter

        ToR switch mode

        value: Union[Literal["layer2"], Literal["layer3"]]
        """
        self._set_property('tor_mode', value)

    @property
    def uplink_ecmp_mode(self):
        # type: () -> Union[Literal["hash_3_tuple"], Literal["hash_5_tuple"], Literal["random_spray"]]
        """uplink_ecmp_mode getter

        The algorithm for packet distribution over ECMP links.. - random_spray randomly puts each packet on an ECMP member links . - hash_3_tuple is a 3 tuple hash of ipv4 src, dst, protocol. - hash_5_tuple is static_hash_ipv4_l4 but a different resulting RTAG7 hash mode

        Returns: Union[Literal["hash_3_tuple"], Literal["hash_5_tuple"], Literal["random_spray"]]
        """
        return self._get_property('uplink_ecmp_mode')

    @uplink_ecmp_mode.setter
    def uplink_ecmp_mode(self, value):
        """uplink_ecmp_mode setter

        The algorithm for packet distribution over ECMP links.. - random_spray randomly puts each packet on an ECMP member links . - hash_3_tuple is a 3 tuple hash of ipv4 src, dst, protocol. - hash_5_tuple is static_hash_ipv4_l4 but a different resulting RTAG7 hash mode

        value: Union[Literal["hash_3_tuple"], Literal["hash_5_tuple"], Literal["random_spray"]]
        """
        self._set_property('uplink_ecmp_mode', value)

    @property
    def qos_profile_name(self):
        # type: () -> str
        """qos_profile_name getter

        The name of a qos profile associated with the ToR switch(es). . x-constraint:. - #/components/schemas/QosProfile/properties/name. 

        Returns: str
        """
        return self._get_property('qos_profile_name')

    @qos_profile_name.setter
    def qos_profile_name(self, value):
        """qos_profile_name setter

        The name of a qos profile associated with the ToR switch(es). . x-constraint:. - #/components/schemas/QosProfile/properties/name. 

        value: str
        """
        self._set_property('qos_profile_name', value)

    @property
    def tor_to_pod_oversubscription(self):
        # type: () -> str
        """tor_to_pod_oversubscription getter

        The oversubscription ratio of the ToR switch(es)

        Returns: str
        """
        return self._get_property('tor_to_pod_oversubscription')

    @tor_to_pod_oversubscription.setter
    def tor_to_pod_oversubscription(self, value):
        """tor_to_pod_oversubscription setter

        The oversubscription ratio of the ToR switch(es)

        value: str
        """
        self._set_property('tor_to_pod_oversubscription', value)


class FabricTorProfileIter(OpenApiIter):
    __slots__ = ('_parent', '_choice')

    _GETITEM_RETURNS_CHOICE_OBJECT = False

    def __init__(self, parent=None, choice=None):
        super(FabricTorProfileIter, self).__init__()
        self._parent = parent
        self._choice = choice

    def __getitem__(self, key):
        # type: (str) -> Union[FabricTorProfile]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> FabricTorProfileIter
        return self._iter()

    def __next__(self):
        # type: () -> FabricTorProfile
        return self._next()

    def next(self):
        # type: () -> FabricTorProfile
        return self._next()

    def torprofile(self, name=None, tor_mode=None, uplink_ecmp_mode=None, qos_profile_name=None, tor_to_pod_oversubscription=None):
        # type: (str,Union[Literal["layer2"], Literal["layer3"]],Union[Literal["hash_3_tuple"], Literal["hash_5_tuple"], Literal["random_spray"]],str,str) -> FabricTorProfileIter
        """Factory method that creates an instance of the FabricTorProfile class

        TBD

        Returns: FabricTorProfileIter
        """
        item = FabricTorProfile(parent=self._parent, name=name, tor_mode=tor_mode, uplink_ecmp_mode=uplink_ecmp_mode, qos_profile_name=qos_profile_name, tor_to_pod_oversubscription=tor_to_pod_oversubscription)
        self._add(item)
        return self

    def add(self, name=None, tor_mode=None, uplink_ecmp_mode=None, qos_profile_name=None, tor_to_pod_oversubscription=None):
        # type: (str,Union[Literal["layer2"], Literal["layer3"]],Union[Literal["hash_3_tuple"], Literal["hash_5_tuple"], Literal["random_spray"]],str,str) -> FabricTorProfile
        """Add method that creates and returns an instance of the FabricTorProfile class

        TBD

        Returns: FabricTorProfile
        """
        item = FabricTorProfile(parent=self._parent, name=name, tor_mode=tor_mode, uplink_ecmp_mode=uplink_ecmp_mode, qos_profile_name=qos_profile_name, tor_to_pod_oversubscription=tor_to_pod_oversubscription)
        self._add(item)
        return item


class FabricQosProfile(OpenApiObject):
    __slots__ = ('_parent')

    _TYPES = {
        'name': {'type': str},
        'ingress_admission': {'type': 'FabricQosProfileIngressAdmission'},
        'scheduler': {'type': 'FabricQosProfileScheduler'},
        'packet_classification': {'type': 'FabricQosProfilePacketClassification'},
        'wred': {'type': 'FabricQosProfileWred'},
    } # type: Dict[str, str]

    _REQUIRED = ('name',) # type: tuple(str)

    _DEFAULTS= {} # type: Dict[str, Union(type)]

    def __init__(self, parent=None, name=None):
        super(FabricQosProfile, self).__init__()
        self._parent = parent
        self._set_property('name', name)

    @property
    def name(self):
        # type: () -> str
        """name getter

        TBD

        Returns: str
        """
        return self._get_property('name')

    @name.setter
    def name(self, value):
        """name setter

        TBD

        value: str
        """
        self._set_property('name', value)

    @property
    def ingress_admission(self):
        # type: () -> FabricQosProfileIngressAdmission
        """ingress_admission getter

        

        Returns: FabricQosProfileIngressAdmission
        """
        return self._get_property('ingress_admission', FabricQosProfileIngressAdmission)

    @property
    def scheduler(self):
        # type: () -> FabricQosProfileScheduler
        """scheduler getter

        

        Returns: FabricQosProfileScheduler
        """
        return self._get_property('scheduler', FabricQosProfileScheduler)

    @property
    def packet_classification(self):
        # type: () -> FabricQosProfilePacketClassification
        """packet_classification getter

        

        Returns: FabricQosProfilePacketClassification
        """
        return self._get_property('packet_classification', FabricQosProfilePacketClassification)

    @property
    def wred(self):
        # type: () -> FabricQosProfileWred
        """wred getter

        WRED (weighted random early detection) configurationWRED (weighted random early detection) configuration

        Returns: FabricQosProfileWred
        """
        return self._get_property('wred', FabricQosProfileWred)


class FabricQosProfileIngressAdmission(OpenApiObject):
    __slots__ = ('_parent')

    _TYPES = {
        'reserved_buffer_bytes': {'type': int},
        'shared_buffer_bytes': {'type': int},
        'priority_list': {
            'type': list,
            'itemtype': str,
        },
    } # type: Dict[str, str]

    _REQUIRED= () # type: tuple(str)

    _DEFAULTS = {
        'reserved_buffer_bytes': 0,
        'shared_buffer_bytes': 0,
    } # type: Dict[str, Union(type)]

    def __init__(self, parent=None, reserved_buffer_bytes=0, shared_buffer_bytes=0, priority_list=None):
        super(FabricQosProfileIngressAdmission, self).__init__()
        self._parent = parent
        self._set_property('reserved_buffer_bytes', reserved_buffer_bytes)
        self._set_property('shared_buffer_bytes', shared_buffer_bytes)
        self._set_property('priority_list', priority_list)

    @property
    def reserved_buffer_bytes(self):
        # type: () -> int
        """reserved_buffer_bytes getter

        Buffer space (in bytes) reserved for each port that this Qos profile applies to

        Returns: int
        """
        return self._get_property('reserved_buffer_bytes')

    @reserved_buffer_bytes.setter
    def reserved_buffer_bytes(self, value):
        """reserved_buffer_bytes setter

        Buffer space (in bytes) reserved for each port that this Qos profile applies to

        value: int
        """
        self._set_property('reserved_buffer_bytes', value)

    @property
    def shared_buffer_bytes(self):
        # type: () -> int
        """shared_buffer_bytes getter

        Amount of shared buffer space (in bytes) available

        Returns: int
        """
        return self._get_property('shared_buffer_bytes')

    @shared_buffer_bytes.setter
    def shared_buffer_bytes(self, value):
        """shared_buffer_bytes setter

        Amount of shared buffer space (in bytes) available

        value: int
        """
        self._set_property('shared_buffer_bytes', value)

    @property
    def priority_list(self):
        # type: () -> List[str]
        """priority_list getter

        List of priorities for which the buffer sizes should be applied

        Returns: List[str]
        """
        return self._get_property('priority_list')

    @priority_list.setter
    def priority_list(self, value):
        """priority_list setter

        List of priorities for which the buffer sizes should be applied

        value: List[str]
        """
        self._set_property('priority_list', value)


class FabricQosProfileScheduler(OpenApiObject):
    __slots__ = ('_parent')

    _TYPES = {
        'scheduler_mode': {
            'type': str,
            'enum': [
                'strict_priority',
                'weighted_round_robin',
            ],
        },
        'weight_list': {
            'type': list,
            'itemtype': int,
        },
    } # type: Dict[str, str]

    _REQUIRED= () # type: tuple(str)

    _DEFAULTS= {} # type: Dict[str, Union(type)]

    STRICT_PRIORITY = 'strict_priority' # type: str
    WEIGHTED_ROUND_ROBIN = 'weighted_round_robin' # type: str

    def __init__(self, parent=None, scheduler_mode=None, weight_list=None):
        super(FabricQosProfileScheduler, self).__init__()
        self._parent = parent
        self._set_property('scheduler_mode', scheduler_mode)
        self._set_property('weight_list', weight_list)

    @property
    def scheduler_mode(self):
        # type: () -> Union[Literal["strict_priority"], Literal["weighted_round_robin"]]
        """scheduler_mode getter

        The queue scheduling discipline 

        Returns: Union[Literal["strict_priority"], Literal["weighted_round_robin"]]
        """
        return self._get_property('scheduler_mode')

    @scheduler_mode.setter
    def scheduler_mode(self, value):
        """scheduler_mode setter

        The queue scheduling discipline 

        value: Union[Literal["strict_priority"], Literal["weighted_round_robin"]]
        """
        self._set_property('scheduler_mode', value)

    @property
    def weight_list(self):
        # type: () -> List[int]
        """weight_list getter

        A list of egress queue weights for weighted round robin scheduler mode

        Returns: List[int]
        """
        return self._get_property('weight_list')

    @weight_list.setter
    def weight_list(self, value):
        """weight_list setter

        A list of egress queue weights for weighted round robin scheduler mode

        value: List[int]
        """
        self._set_property('weight_list', value)


class FabricQosProfilePacketClassification(OpenApiObject):
    __slots__ = ('_parent')

    _TYPES = {
        'map_dscp_to_traffic_class': {'type': 'FabricQosProfilePacketClassificationMap'},
        'map_traffic_class_to_queue': {'type': 'FabricQosProfilePacketClassificationMap'},
    } # type: Dict[str, str]

    _REQUIRED= () # type: tuple(str)

    _DEFAULTS= {} # type: Dict[str, Union(type)]

    def __init__(self, parent=None):
        super(FabricQosProfilePacketClassification, self).__init__()
        self._parent = parent

    @property
    def map_dscp_to_traffic_class(self):
        # type: () -> FabricQosProfilePacketClassificationMap
        """map_dscp_to_traffic_class getter

        

        Returns: FabricQosProfilePacketClassificationMap
        """
        return self._get_property('map_dscp_to_traffic_class', FabricQosProfilePacketClassificationMap)

    @property
    def map_traffic_class_to_queue(self):
        # type: () -> FabricQosProfilePacketClassificationMap
        """map_traffic_class_to_queue getter

        

        Returns: FabricQosProfilePacketClassificationMap
        """
        return self._get_property('map_traffic_class_to_queue', FabricQosProfilePacketClassificationMap)


class FabricQosProfilePacketClassificationMap(OpenApiObject):
    __slots__ = ('_parent')

    _TYPES = {} # type: Dict[str, str]

    _REQUIRED= () # type: tuple(str)

    _DEFAULTS= {} # type: Dict[str, Union(type)]

    def __init__(self, parent=None):
        super(FabricQosProfilePacketClassificationMap, self).__init__()
        self._parent = parent


class FabricQosProfileWred(OpenApiObject):
    __slots__ = ('_parent')

    _TYPES = {
        'queue_list': {
            'type': list,
            'itemtype': str,
        },
        'ecn_marking_enabled': {'type': bool},
        'min_threshold_bytes': {'type': int},
        'max_threshold_bytes': {'type': int},
        'max_probability_percent': {'type': int},
    } # type: Dict[str, str]

    _REQUIRED= () # type: tuple(str)

    _DEFAULTS = {
        'ecn_marking_enabled': False,
        'min_threshold_bytes': 1,
        'max_threshold_bytes': 2,
        'max_probability_percent': 100,
    } # type: Dict[str, Union(type)]

    def __init__(self, parent=None, queue_list=None, ecn_marking_enabled=False, min_threshold_bytes=1, max_threshold_bytes=2, max_probability_percent=100):
        super(FabricQosProfileWred, self).__init__()
        self._parent = parent
        self._set_property('queue_list', queue_list)
        self._set_property('ecn_marking_enabled', ecn_marking_enabled)
        self._set_property('min_threshold_bytes', min_threshold_bytes)
        self._set_property('max_threshold_bytes', max_threshold_bytes)
        self._set_property('max_probability_percent', max_probability_percent)

    @property
    def queue_list(self):
        # type: () -> List[str]
        """queue_list getter

        List of queues for which WRED is enabled

        Returns: List[str]
        """
        return self._get_property('queue_list')

    @queue_list.setter
    def queue_list(self, value):
        """queue_list setter

        List of queues for which WRED is enabled

        value: List[str]
        """
        self._set_property('queue_list', value)

    @property
    def ecn_marking_enabled(self):
        # type: () -> bool
        """ecn_marking_enabled getter

        TBD

        Returns: bool
        """
        return self._get_property('ecn_marking_enabled')

    @ecn_marking_enabled.setter
    def ecn_marking_enabled(self, value):
        """ecn_marking_enabled setter

        TBD

        value: bool
        """
        self._set_property('ecn_marking_enabled', value)

    @property
    def min_threshold_bytes(self):
        # type: () -> int
        """min_threshold_bytes getter

        Egress queue threshold beyond which packets will be droppes or marked

        Returns: int
        """
        return self._get_property('min_threshold_bytes')

    @min_threshold_bytes.setter
    def min_threshold_bytes(self, value):
        """min_threshold_bytes setter

        Egress queue threshold beyond which packets will be droppes or marked

        value: int
        """
        self._set_property('min_threshold_bytes', value)

    @property
    def max_threshold_bytes(self):
        # type: () -> int
        """max_threshold_bytes getter

        Egress queue threshold beyond which packets will be droppes or marked

        Returns: int
        """
        return self._get_property('max_threshold_bytes')

    @max_threshold_bytes.setter
    def max_threshold_bytes(self, value):
        """max_threshold_bytes setter

        Egress queue threshold beyond which packets will be droppes or marked

        value: int
        """
        self._set_property('max_threshold_bytes', value)

    @property
    def max_probability_percent(self):
        # type: () -> int
        """max_probability_percent getter

        Probability of dropping/marking packets at max threshold

        Returns: int
        """
        return self._get_property('max_probability_percent')

    @max_probability_percent.setter
    def max_probability_percent(self, value):
        """max_probability_percent setter

        Probability of dropping/marking packets at max threshold

        value: int
        """
        self._set_property('max_probability_percent', value)


class FabricQosProfileIter(OpenApiIter):
    __slots__ = ('_parent', '_choice')

    _GETITEM_RETURNS_CHOICE_OBJECT = False

    def __init__(self, parent=None, choice=None):
        super(FabricQosProfileIter, self).__init__()
        self._parent = parent
        self._choice = choice

    def __getitem__(self, key):
        # type: (str) -> Union[FabricQosProfile]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> FabricQosProfileIter
        return self._iter()

    def __next__(self):
        # type: () -> FabricQosProfile
        return self._next()

    def next(self):
        # type: () -> FabricQosProfile
        return self._next()

    def qosprofile(self, name=None):
        # type: (str) -> FabricQosProfileIter
        """Factory method that creates an instance of the FabricQosProfile class

        TBD

        Returns: FabricQosProfileIter
        """
        item = FabricQosProfile(parent=self._parent, name=name)
        self._add(item)
        return self

    def add(self, name=None):
        # type: (str) -> FabricQosProfile
        """Add method that creates and returns an instance of the FabricQosProfile class

        TBD

        Returns: FabricQosProfile
        """
        item = FabricQosProfile(parent=self._parent, name=name)
        self._add(item)
        return item


class FabricL1SettingsProfile(OpenApiObject):
    __slots__ = ('_parent')

    _TYPES = {
        'name': {'type': str},
        'link_speed': {
            'type': str,
            'enum': [
                'speed_100_gbps',
                'speed_200_gbps',
                'speed_50_gbps',
            ],
        },
        'autonegotiation': {'type': 'FabricL1SettingsProfileAutonegotiation'},
    } # type: Dict[str, str]

    _REQUIRED= () # type: tuple(str)

    _DEFAULTS = {
        'link_speed': 'speed_100_gbps',
    } # type: Dict[str, Union(type)]

    SPEED_100_GBPS = 'speed_100_gbps' # type: str
    SPEED_200_GBPS = 'speed_200_gbps' # type: str
    SPEED_50_GBPS = 'speed_50_gbps' # type: str

    def __init__(self, parent=None, name=None, link_speed='speed_100_gbps'):
        super(FabricL1SettingsProfile, self).__init__()
        self._parent = parent
        self._set_property('name', name)
        self._set_property('link_speed', link_speed)

    @property
    def name(self):
        # type: () -> str
        """name getter

        Uniquely identifies a layer 1 settings profile

        Returns: str
        """
        return self._get_property('name')

    @name.setter
    def name(self, value):
        """name setter

        Uniquely identifies a layer 1 settings profile

        value: str
        """
        self._set_property('name', value)

    @property
    def link_speed(self):
        # type: () -> Union[Literal["speed_100_gbps"], Literal["speed_200_gbps"], Literal["speed_50_gbps"]]
        """link_speed getter

        Link speed

        Returns: Union[Literal["speed_100_gbps"], Literal["speed_200_gbps"], Literal["speed_50_gbps"]]
        """
        return self._get_property('link_speed')

    @link_speed.setter
    def link_speed(self, value):
        """link_speed setter

        Link speed

        value: Union[Literal["speed_100_gbps"], Literal["speed_200_gbps"], Literal["speed_50_gbps"]]
        """
        self._set_property('link_speed', value)

    @property
    def autonegotiation(self):
        # type: () -> FabricL1SettingsProfileAutonegotiation
        """autonegotiation getter

        

        Returns: FabricL1SettingsProfileAutonegotiation
        """
        return self._get_property('autonegotiation', FabricL1SettingsProfileAutonegotiation)


class FabricL1SettingsProfileAutonegotiation(OpenApiObject):
    __slots__ = ('_parent','_choice')

    _TYPES = {
        'choice': {
            'type': str,
            'enum': [
                'enabled',
                'disabled',
            ],
        },
        'enabled': {'type': 'FabricL1SettingsProfileAutonegotiationEnabled'},
        'disabled': {'type': 'FabricL1SettingsProfileAutonegotiationDisabled'},
    } # type: Dict[str, str]

    _REQUIRED= () # type: tuple(str)

    _DEFAULTS = {
        'choice': 'enabled',
    } # type: Dict[str, Union(type)]

    ENABLED = 'enabled' # type: str
    DISABLED = 'disabled' # type: str

    def __init__(self, parent=None, choice=None):
        super(FabricL1SettingsProfileAutonegotiation, self).__init__()
        self._parent = parent
        if 'choice' in self._DEFAULTS and choice is None:
            getattr(self, self._DEFAULTS['choice'])
        else:
            self.choice = choice

    @property
    def enabled(self):
        # type: () -> FabricL1SettingsProfileAutonegotiationEnabled
        """Factory property that returns an instance of the FabricL1SettingsProfileAutonegotiationEnabled class

        TBD

        Returns: FabricL1SettingsProfileAutonegotiationEnabled
        """
        return self._get_property('enabled', FabricL1SettingsProfileAutonegotiationEnabled, self, 'enabled')

    @property
    def disabled(self):
        # type: () -> FabricL1SettingsProfileAutonegotiationDisabled
        """Factory property that returns an instance of the FabricL1SettingsProfileAutonegotiationDisabled class

        TBD

        Returns: FabricL1SettingsProfileAutonegotiationDisabled
        """
        return self._get_property('disabled', FabricL1SettingsProfileAutonegotiationDisabled, self, 'disabled')

    @property
    def choice(self):
        # type: () -> Union[Literal["disabled"], Literal["enabled"]]
        """choice getter

        TBD

        Returns: Union[Literal["disabled"], Literal["enabled"]]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[Literal["disabled"], Literal["enabled"]]
        """
        self._set_property('choice', value)


class FabricL1SettingsProfileAutonegotiationEnabled(OpenApiObject):
    __slots__ = ('_parent')

    _TYPES = {
        'advertise_fec': {'type': bool},
    } # type: Dict[str, str]

    _REQUIRED= () # type: tuple(str)

    _DEFAULTS = {
        'advertise_fec': True,
    } # type: Dict[str, Union(type)]

    def __init__(self, parent=None, advertise_fec=True):
        super(FabricL1SettingsProfileAutonegotiationEnabled, self).__init__()
        self._parent = parent
        self._set_property('advertise_fec', advertise_fec)

    @property
    def advertise_fec(self):
        # type: () -> bool
        """advertise_fec getter

        TBD

        Returns: bool
        """
        return self._get_property('advertise_fec')

    @advertise_fec.setter
    def advertise_fec(self, value):
        """advertise_fec setter

        TBD

        value: bool
        """
        self._set_property('advertise_fec', value)


class FabricL1SettingsProfileAutonegotiationDisabled(OpenApiObject):
    __slots__ = ('_parent')

    _TYPES = {
        'fec_mode': {
            'type': str,
            'enum': [
                'firecode',
                'kp4',
                'reed_solomon',
            ],
        },
    } # type: Dict[str, str]

    _REQUIRED= () # type: tuple(str)

    _DEFAULTS = {
        'fec_mode': 'reed_solomon',
    } # type: Dict[str, Union(type)]

    FIRECODE = 'firecode' # type: str
    KP4 = 'kp4' # type: str
    REED_SOLOMON = 'reed_solomon' # type: str

    def __init__(self, parent=None, fec_mode='reed_solomon'):
        super(FabricL1SettingsProfileAutonegotiationDisabled, self).__init__()
        self._parent = parent
        self._set_property('fec_mode', fec_mode)

    @property
    def fec_mode(self):
        # type: () -> Union[Literal["firecode"], Literal["kp4"], Literal["reed_solomon"]]
        """fec_mode getter

        TBD

        Returns: Union[Literal["firecode"], Literal["kp4"], Literal["reed_solomon"]]
        """
        return self._get_property('fec_mode')

    @fec_mode.setter
    def fec_mode(self, value):
        """fec_mode setter

        TBD

        value: Union[Literal["firecode"], Literal["kp4"], Literal["reed_solomon"]]
        """
        self._set_property('fec_mode', value)


class FabricL1SettingsProfileIter(OpenApiIter):
    __slots__ = ('_parent', '_choice')

    _GETITEM_RETURNS_CHOICE_OBJECT = False

    def __init__(self, parent=None, choice=None):
        super(FabricL1SettingsProfileIter, self).__init__()
        self._parent = parent
        self._choice = choice

    def __getitem__(self, key):
        # type: (str) -> Union[FabricL1SettingsProfile]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> FabricL1SettingsProfileIter
        return self._iter()

    def __next__(self):
        # type: () -> FabricL1SettingsProfile
        return self._next()

    def next(self):
        # type: () -> FabricL1SettingsProfile
        return self._next()

    def l1settingsprofile(self, name=None, link_speed='speed_100_gbps'):
        # type: (str,Union[Literal["speed_100_gbps"], Literal["speed_200_gbps"], Literal["speed_50_gbps"]]) -> FabricL1SettingsProfileIter
        """Factory method that creates an instance of the FabricL1SettingsProfile class

        TBD

        Returns: FabricL1SettingsProfileIter
        """
        item = FabricL1SettingsProfile(parent=self._parent, name=name, link_speed=link_speed)
        self._add(item)
        return self

    def add(self, name=None, link_speed='speed_100_gbps'):
        # type: (str,Union[Literal["speed_100_gbps"], Literal["speed_200_gbps"], Literal["speed_50_gbps"]]) -> FabricL1SettingsProfile
        """Add method that creates and returns an instance of the FabricL1SettingsProfile class

        TBD

        Returns: FabricL1SettingsProfile
        """
        item = FabricL1SettingsProfile(parent=self._parent, name=name, link_speed=link_speed)
        self._add(item)
        return item


class ErrorDetails(OpenApiObject):
    __slots__ = ('_parent')

    _TYPES = {
        'errors': {'type': 'ErrorItemIter'},
    } # type: Dict[str, str]

    _REQUIRED= () # type: tuple(str)

    _DEFAULTS= {} # type: Dict[str, Union(type)]

    def __init__(self, parent=None):
        super(ErrorDetails, self).__init__()
        self._parent = parent

    @property
    def errors(self):
        # type: () -> ErrorItemIter
        """errors getter

        TBD

        Returns: ErrorItemIter
        """
        return self._get_property('errors', ErrorItemIter, self._parent, self._choice)


class ErrorItem(OpenApiObject):
    __slots__ = ('_parent')

    _TYPES = {
        'message': {'type': str},
        'code': {'type': int},
        'detail': {'type': str},
    } # type: Dict[str, str]

    _REQUIRED= () # type: tuple(str)

    _DEFAULTS= {} # type: Dict[str, Union(type)]

    def __init__(self, parent=None, message=None, code=None, detail=None):
        super(ErrorItem, self).__init__()
        self._parent = parent
        self._set_property('message', message)
        self._set_property('code', code)
        self._set_property('detail', detail)

    @property
    def message(self):
        # type: () -> str
        """message getter

        TBD

        Returns: str
        """
        return self._get_property('message')

    @message.setter
    def message(self, value):
        """message setter

        TBD

        value: str
        """
        self._set_property('message', value)

    @property
    def code(self):
        # type: () -> int
        """code getter

        TBD

        Returns: int
        """
        return self._get_property('code')

    @code.setter
    def code(self, value):
        """code setter

        TBD

        value: int
        """
        self._set_property('code', value)

    @property
    def detail(self):
        # type: () -> str
        """detail getter

        TBD

        Returns: str
        """
        return self._get_property('detail')

    @detail.setter
    def detail(self, value):
        """detail setter

        TBD

        value: str
        """
        self._set_property('detail', value)


class ErrorItemIter(OpenApiIter):
    __slots__ = ('_parent', '_choice')

    _GETITEM_RETURNS_CHOICE_OBJECT = False

    def __init__(self, parent=None, choice=None):
        super(ErrorItemIter, self).__init__()
        self._parent = parent
        self._choice = choice

    def __getitem__(self, key):
        # type: (str) -> Union[ErrorItem]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> ErrorItemIter
        return self._iter()

    def __next__(self):
        # type: () -> ErrorItem
        return self._next()

    def next(self):
        # type: () -> ErrorItem
        return self._next()

    def item(self, message=None, code=None, detail=None):
        # type: (str,int,str) -> ErrorItemIter
        """Factory method that creates an instance of the ErrorItem class

        TBD

        Returns: ErrorItemIter
        """
        item = ErrorItem(parent=self._parent, message=message, code=code, detail=detail)
        self._add(item)
        return self

    def add(self, message=None, code=None, detail=None):
        # type: (str,int,str) -> ErrorItem
        """Add method that creates and returns an instance of the ErrorItem class

        TBD

        Returns: ErrorItem
        """
        item = ErrorItem(parent=self._parent, message=message, code=code, detail=detail)
        self._add(item)
        return item


class Api(object):
    """OpenApi Abstract API
    """

    def __init__(self, **kwargs):
        pass

    def set_config(self, payload):
        """POST /onex/api/v1/fabric/config

        Sets the fabric configuration.

        Return: error_details
        """
        raise NotImplementedError("set_config")

    def get_config(self):
        """GET /onex/api/v1/fabric/config

        Gets the fabric configuration.

        Return: config
        """
        raise NotImplementedError("get_config")

    def config(self):
        """Factory method that creates an instance of Config

        Return: Config
        """
        return Config()

    def error_details(self):
        """Factory method that creates an instance of ErrorDetails

        Return: ErrorDetails
        """
        return ErrorDetails()


class HttpApi(Api):
    """OpenAPI HTTP Api
    """
    def __init__(self, **kwargs):
        super(HttpApi, self).__init__(**kwargs)
        self._transport = HttpTransport(**kwargs)

    def set_config(self, payload):
        """POST /onex/api/v1/fabric/config

        Sets the fabric configuration.

        Return: error_details
        """
        return self._transport.send_recv(
            "post",
            "/onex/api/v1/fabric/config",
            payload=payload,
            return_object=self.error_details(),
        )

    def get_config(self):
        """GET /onex/api/v1/fabric/config

        Gets the fabric configuration.

        Return: config
        """
        return self._transport.send_recv(
            "get",
            "/onex/api/v1/fabric/config",
            payload=None,
            return_object=self.config(),
        )
