# coding: utf-8
"""
    DigitalOcean API

    # Introduction  The DigitalOcean API allows you to manage Droplets and resources within the DigitalOcean cloud in a simple, programmatic way using conventional HTTP requests.  All of the functionality that you are familiar with in the DigitalOcean control panel is also available through the API, allowing you to script the complex actions that your situation requires.  The API documentation will start with a general overview about the design and technology that has been implemented, followed by reference information about specific endpoints.  ## Requests  Any tool that is fluent in HTTP can communicate with the API simply by requesting the correct URI. Requests should be made using the HTTPS protocol so that traffic is encrypted. The interface responds to different methods depending on the action required.  |Method|Usage| |--- |--- | |GET|For simple retrieval of information about your account, Droplets, or environment, you should use the GET method.  The information you request will be returned to you as a JSON object. The attributes defined by the JSON object can be used to form additional requests.  Any request using the GET method is read-only and will not affect any of the objects you are querying.| |DELETE|To destroy a resource and remove it from your account and environment, the DELETE method should be used.  This will remove the specified object if it is found.  If it is not found, the operation will return a response indicating that the object was not found. This idempotency means that you do not have to check for a resource's availability prior to issuing a delete command, the final state will be the same regardless of its existence.| |PUT|To update the information about a resource in your account, the PUT method is available. Like the DELETE Method, the PUT method is idempotent.  It sets the state of the target using the provided values, regardless of their current values. Requests using the PUT method do not need to check the current attributes of the object.| |PATCH|Some resources support partial modification. In these cases, the PATCH method is available. Unlike PUT which generally requires a complete representation of a resource, a PATCH request is is a set of instructions on how to modify a resource updating only specific attributes.| |POST|To create a new object, your request should specify the POST method. The POST request includes all of the attributes necessary to create a new object.  When you wish to create a new object, send a POST request to the target endpoint.| |HEAD|Finally, to retrieve metadata information, you should use the HEAD method to get the headers.  This returns only the header of what would be returned with an associated GET request. Response headers contain some useful information about your API access and the results that are available for your request. For instance, the headers contain your current rate-limit value and the amount of time available until the limit resets. It also contains metrics about the total number of objects found, pagination information, and the total content length.|   ## HTTP Statuses  Along with the HTTP methods that the API responds to, it will also return standard HTTP statuses, including error codes.  In the event of a problem, the status will contain the error code, while the body of the response will usually contain additional information about the problem that was encountered.  In general, if the status returned is in the 200 range, it indicates that the request was fulfilled successfully and that no error was encountered.  Return codes in the 400 range typically indicate that there was an issue with the request that was sent. Among other things, this could mean that you did not authenticate correctly, that you are requesting an action that you do not have authorization for, that the object you are requesting does not exist, or that your request is malformed.  If you receive a status in the 500 range, this generally indicates a server-side problem. This means that we are having an issue on our end and cannot fulfill your request currently.  400 and 500 level error responses will include a JSON object in their body, including the following attributes:  |Name|Type|Description| |--- |--- |--- | |id|string|A short identifier corresponding to the HTTP status code returned. For example, the ID for a response returning a 404 status code would be \"not_found.\"| |message|string|A message providing additional information about the error, including details to help resolve it when possible.| |request_id|string|Optionally, some endpoints may include a request ID that should be provided when reporting bugs or opening support tickets to help identify the issue.|  ### Example Error Response  ```     HTTP/1.1 403 Forbidden     {       \"id\":       \"forbidden\",       \"message\":  \"You do not have access for the attempted action.\"     } ```  ## Responses  When a request is successful, a response body will typically be sent back in the form of a JSON object. An exception to this is when a DELETE request is processed, which will result in a successful HTTP 204 status and an empty response body.  Inside of this JSON object, the resource root that was the target of the request will be set as the key. This will be the singular form of the word if the request operated on a single object, and the plural form of the word if a collection was processed.  For example, if you send a GET request to `/v2/droplets/$DROPLET_ID` you will get back an object with a key called \"`droplet`\". However, if you send the GET request to the general collection at `/v2/droplets`, you will get back an object with a key called \"`droplets`\".  The value of these keys will generally be a JSON object for a request on a single object and an array of objects for a request on a collection of objects.  ### Response for a Single Object  ```     {         \"droplet\": {             \"name\": \"example.com\"             . . .         }     } ```  ### Response for an Object Collection  ```     {         \"droplets\": [             {                 \"name\": \"example.com\"                 . . .             },             {                 \"name\": \"second.com\"                 . . .             }         ]     } ```  ## Meta  In addition to the main resource root, the response may also contain a `meta` object. This object contains information about the response itself.  The `meta` object contains a `total` key that is set to the total number of objects returned by the request. This has implications on the `links` object and pagination.  The `meta` object will only be displayed when it has a value. Currently, the `meta` object will have a value when a request is made on a collection (like `droplets` or `domains`).   ### Sample Meta Object  ```     {         . . .         \"meta\": {             \"total\": 43         }         . . .     } ```  ## Links & Pagination  The `links` object is returned as part of the response body when pagination is enabled. By default, 20 objects are returned per page. If the response contains 20 objects or fewer, no `links` object will be returned. If the response contains more than 20 objects, the first 20 will be returned along with the `links` object.  You can request a different pagination limit or force pagination by appending `?per_page=` to the request with the number of items you would like per page. For instance, to show only two results per page, you could add `?per_page=2` to the end of your query. The maximum number of results per page is 200.  The `links` object contains a `pages` object. The `pages` object, in turn, contains keys indicating the relationship of additional pages. The values of these are the URLs of the associated pages. The keys will be one of the following:  *   **first**: The URI of the first page of results. *   **prev**: The URI of the previous sequential page of results. *   **next**: The URI of the next sequential page of results. *   **last**: The URI of the last page of results.  The `pages` object will only include the links that make sense. So for the first page of results, no `first` or `prev` links will ever be set. This convention holds true in other situations where a link would not make sense.  ### Sample Links Object  ```     {         . . .         \"links\": {             \"pages\": {                 \"last\": \"https://api.digitalocean.com/v2/images?page=2\",                 \"next\": \"https://api.digitalocean.com/v2/images?page=2\"             }         }         . . .     } ```  ## Rate Limit  Requests through the API are rate limited per OAuth token. Current rate limits:  *   5,000 requests per hour *   250 requests per minute (5% of the hourly total)  Once you exceed either limit, you will be rate limited until the next cycle starts. Space out any requests that you would otherwise issue in bursts for the best results.  The rate limiting information is contained within the response headers of each request. The relevant headers are:  *   **ratelimit-limit**: The number of requests that can be made per hour. *   **ratelimit-remaining**: The number of requests that remain before you hit your request limit. See the information below for how the request limits expire. *   **ratelimit-reset**: This represents the time when the oldest request will expire. The value is given in [Unix epoch time](http://en.wikipedia.org/wiki/Unix_time). See below for more information about how request limits expire.  More rate limiting information is returned only within burst limit error response headers: *   **retry-after**: The number of seconds to wait before making another request when rate limited.  As long as the `ratelimit-remaining` count is above zero, you will be able to make additional requests.  The way that a request expires and is removed from the current limit count is important to understand. Rather than counting all of the requests for an hour and resetting the `ratelimit-remaining` value at the end of the hour, each request instead has its own timer.  This means that each request contributes toward the `ratelimit-remaining` count for one complete hour after the request is made. When that request's timer runs out, it is no longer counted towards the request limit.  This has implications on the meaning of the `ratelimit-reset` header as well. Because the entire rate limit is not reset at one time, the value of this header is set to the time when the _oldest_ request will expire.  Keep this in mind if you see your `ratelimit-reset` value change, but not move an entire hour into the future.  If the `ratelimit-remaining` reaches zero, subsequent requests will receive a 429 error code until the request reset has been reached.   `ratelimit-remaining` reaching zero can also indicate that the \"burst limit\" of 250  requests per minute limit was met, even if the 5,000 requests per hour limit was not.  In this case, the 429 error response will include a retry-after header to indicate how  long to wait (in seconds) until the request may be retried.  You can see the format of the response in the examples.   **Note:** The following endpoints have special rate limit requirements that are independent of the limits defined above.  *   Only 12 `POST` requests to the `/v2/floating_ips` endpoint to create Floating IPs can be made per 60 seconds. *   Only 10 `GET` requests to the `/v2/account/keys` endpoint to list SSH keys can be made per 60 seconds. *   Only 5 requests to any and all `v2/cdn/endpoints` can be made per 10 seconds. This includes `v2/cdn/endpoints`,      `v2/cdn/endpoints/$ENDPOINT_ID`, and `v2/cdn/endpoints/$ENDPOINT_ID/cache`. *   Only 50 strings within the `files` json struct in the `v2/cdn/endpoints/$ENDPOINT_ID/cache` [payload](https://docs.digitalocean.com/reference/api/api-reference/#operation/cdn_purge_cache)      can be requested every 20 seconds.  ### Sample Rate Limit Headers  ```     . . .     ratelimit-limit: 1200     ratelimit-remaining: 1193     rateLimit-reset: 1402425459     . . . ```    ### Sample Rate Limit Headers When Burst Limit is Reached:  ```     . . .     ratelimit-limit: 5000     ratelimit-remaining: 0     rateLimit-reset: 1402425459     retry-after: 29     . . . ```  ### Sample Rate Exceeded Response  ```     429 Too Many Requests     {             id: \"too_many_requests\",             message: \"API Rate limit exceeded.\"     } ```  ## Curl Examples  Throughout this document, some example API requests will be given using the `curl` command. This will allow us to demonstrate the various endpoints in a simple, textual format.      These examples assume that you are using a Linux or macOS command line. To run these commands on a Windows machine, you can either use cmd.exe, PowerShell, or WSL:  * For cmd.exe, use the `set VAR=VALUE` [syntax](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/set_1) to define environment variables, call them with `%VAR%`, then replace all backslashes (`\\`) in the examples with carets (`^`).  * For PowerShell, use the `$Env:VAR = \"VALUE\"` [syntax](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_environment_variables?view=powershell-7.2) to define environment variables, call them with `$Env:VAR`, then replace `curl` with `curl.exe` and all backslashes (`\\`) in the examples with backticks (`` ` ``).  * WSL is a compatibility layer that allows you to emulate a Linux terminal on a Windows machine. Install WSL with our [community tutorial](https://www.digitalocean.com/community/tutorials/how-to-install-the-windows-subsystem-for-linux-2-on-microsoft-windows-10),  then follow this API documentation normally.  The names of account-specific references (like Droplet IDs, for instance) will be represented by variables. For instance, a Droplet ID may be represented by a variable called `$DROPLET_ID`. You can set the associated variables in your environment if you wish to use the examples without modification.  The first variable that you should set to get started is your OAuth authorization token. The next section will go over the details of this, but you can set an environmental variable for it now.  Generate a token by going to the [Apps & API](https://cloud.digitalocean.com/settings/applications) section of the DigitalOcean control panel. Use an existing token if you have saved one, or generate a new token with the \"Generate new token\" button. Copy the generated token and use it to set and export the TOKEN variable in your environment as the example shows.  You may also wish to set some other variables now or as you go along. For example, you may wish to set the `DROPLET_ID` variable to one of your Droplet IDs since this will be used frequently in the API.  If you are following along, make sure you use a Droplet ID that you control so that your commands will execute correctly.  If you need access to the headers of a response through `curl`, you can pass the `-i` flag to display the header information along with the body. If you are only interested in the header, you can instead pass the `-I` flag, which will exclude the response body entirely.   ### Set and Export your OAuth Token  ``` export DIGITALOCEAN_TOKEN=your_token_here ```  ### Set and Export a Variable  ``` export DROPLET_ID=1111111 ```  ## Parameters  There are two different ways to pass parameters in a request with the API.  When passing parameters to create or update an object, parameters should be passed as a JSON object containing the appropriate attribute names and values as key-value pairs. When you use this format, you should specify that you are sending a JSON object in the header. This is done by setting the `Content-Type` header to `application/json`. This ensures that your request is interpreted correctly.  When passing parameters to filter a response on GET requests, parameters can be passed using standard query attributes. In this case, the parameters would be embedded into the URI itself by appending a `?` to the end of the URI and then setting each attribute with an equal sign. Attributes can be separated with a `&`. Tools like `curl` can create the appropriate URI when given parameters and values; this can also be done using the `-F` flag and then passing the key and value as an argument. The argument should take the form of a quoted string with the attribute being set to a value with an equal sign.  ### Pass Parameters as a JSON Object  ```     curl -H \"Authorization: Bearer $DIGITALOCEAN_TOKEN\" \\         -H \"Content-Type: application/json\" \\         -d '{\"name\": \"example.com\", \"ip_address\": \"127.0.0.1\"}' \\         -X POST \"https://api.digitalocean.com/v2/domains\" ```  ### Pass Filter Parameters as a Query String  ```      curl -H \"Authorization: Bearer $DIGITALOCEAN_TOKEN\" \\          -X GET \\          \"https://api.digitalocean.com/v2/images?private=true\" ```  ## Cross Origin Resource Sharing  In order to make requests to the API from other domains, the API implements Cross Origin Resource Sharing (CORS) support.  CORS support is generally used to create AJAX requests outside of the domain that the request originated from. This is necessary to implement projects like control panels utilizing the API. This tells the browser that it can send requests to an outside domain.  The procedure that the browser initiates in order to perform these actions (other than GET requests) begins by sending a \"preflight\" request. This sets the `Origin` header and uses the `OPTIONS` method. The server will reply back with the methods it allows and some of the limits it imposes. The client then sends the actual request if it falls within the allowed constraints.  This process is usually done in the background by the browser, but you can use curl to emulate this process using the example provided. The headers that will be set to show the constraints are:  *   **Access-Control-Allow-Origin**: This is the domain that is sent by the client or browser as the origin of the request. It is set through an `Origin` header. *   **Access-Control-Allow-Methods**: This specifies the allowed options for requests from that domain. This will generally be all available methods. *   **Access-Control-Expose-Headers**: This will contain the headers that will be available to requests from the origin domain. *   **Access-Control-Max-Age**: This is the length of time that the access is considered valid. After this expires, a new preflight should be sent. *   **Access-Control-Allow-Credentials**: This will be set to `true`. It basically allows you to send your OAuth token for authentication.  You should not need to be concerned with the details of these headers, because the browser will typically do all of the work for you. 

    The version of the OpenAPI document: 2.0
    Contact: api-engineering@digitalocean.com
    Generated by: https://konfigthis.com
"""

from dataclasses import dataclass
from decimal import Decimal
import enum
import email
import json
import os
import io
import atexit
from multiprocessing.pool import ThreadPool
import re
import tempfile
import time
import typing
import typing_extensions
import aiohttp
import urllib3
from pydantic import BaseModel, RootModel, ValidationError
from urllib3._collections import HTTPHeaderDict
from urllib.parse import urlparse, quote
from urllib3.fields import RequestField as RequestFieldBase
from urllib3.fields import guess_content_type

import frozendict

from digital_ocean_python_sdk import rest
from digital_ocean_python_sdk.api_response import ApiResponse, AsyncApiResponse
from digital_ocean_python_sdk.rest import AsyncResponseWrapper, ResponseWrapper
from digital_ocean_python_sdk.configuration import Configuration
from digital_ocean_python_sdk.exceptions import ApiTypeError, ApiValueError, MissingRequiredParametersError
from digital_ocean_python_sdk.request_after_hook import request_after_hook
from digital_ocean_python_sdk.request_before_url_hook import request_before_url_hook
from digital_ocean_python_sdk.schemas import (
    NoneClass,
    BoolClass,
    Schema,
    FileIO,
    BinarySchema,
    date,
    datetime,
    none_type,
    Unset,
    unset,
)

@dataclass
class MappedArgs:
    body: typing.Any = None
    query: typing.Optional[dict] = None
    path: typing.Optional[dict] = None
    header: typing.Optional[dict] = None
    cookie: typing.Optional[dict] = None

class RequestField(RequestFieldBase):
    def __eq__(self, other):
        if not isinstance(other, RequestField):
            return False
        return self.__dict__ == other.__dict__


T = typing.TypeVar('T')


def closest_type_match(value: typing.Any, types: typing.List[typing.Type]) -> typing.Type:
    best_match = None

    for t in types:
        # Check for generic types
        origin = typing_extensions.get_origin(t)
        args = typing_extensions.get_args(t)

        # Check for Literal types
        if origin == typing_extensions.Literal:
            if value in args:
                best_match = t
                continue

        # Check for Pydantic models and non-generic types
        if isinstance(t, type):  # Ensure t is a class
            if issubclass(t, BaseModel):
                if isinstance(value, dict):
                    try:
                        t(**value)
                        best_match = t
                    except ValidationError:
                        continue
            else:  # This is a non-generic type
                if isinstance(value, t):
                    if best_match is None or (isinstance(value, type) and issubclass(best_match, t)):
                        best_match = t
                continue

        # Check for generic list type
        if origin == list and isinstance(value, list):
            best_match = t

    return best_match


def construct_model_instance(model: typing.Type[T], data: typing.Any) -> T:
    """
    Recursively construct an instance of a Pydantic model along with its nested models.
    """

    # if model is Union,
    if typing_extensions.get_origin(model) is typing.Union:
        best_type = closest_type_match(data, model.__args__)
        return construct_model_instance(best_type, data)
    elif model is None or model is type(None):
        return data
    # if model is scalar value like str, number, etc. just return the value
    elif isinstance(data, (str, float, int, bytes, bool)):
        return data
    elif data is None:
        return data
    # if model is list, iterate over list and recursively call
    elif typing_extensions.get_origin(model) is list:
        item_model = typing_extensions.get_args(model)[0]
        return [construct_model_instance(item_model, item) for item in data]
    # if model is free form object, just return the value
    elif typing_extensions.get_origin(model) is dict:
        return data
    elif model is dict:
        return data
    elif model is object:
        return data
    # if model is BaseModel, iterate over fields and recursively call
    elif issubclass(model, BaseModel):
        new_data = {}
        for field_name, field_type in model.__annotations__.items():
            # get alias
            alias = model.model_fields[field_name].alias
            if alias in data:
                new_data[alias] = construct_model_instance(field_type, data[alias])
        return model.model_construct(**new_data)
    raise ApiTypeError(f"Unable to construct model instance of type {model}")


class Dictionary(BaseModel):
    """
    For free-form objects that can have any keys and values
    (i.e. "type: object" with no properties)
    """
    class Config:
        extra = 'allow'


def DeprecationWarningOnce(func=None, *, prefix=None):
    def decorator(func):
        warned = False
        def wrapper(instance, *args, **kwargs):
            nonlocal warned
            if not warned:
                msg = f"{func.__name__} is deprecated"
                if prefix:
                    msg = f"{prefix}.{msg}"
                instance.api_client.configuration.logger.warning(msg)
                warned = True
            return func(instance, *args, **kwargs)
        return wrapper
    if func is None:
        return decorator
    else:
        return decorator(func)

class JSONEncoder(json.JSONEncoder):
    compact_separators = (',', ':')

    def default(self, obj):
        if isinstance(obj, str):
            return str(obj)
        elif isinstance(obj, float):
            return float(obj)
        elif isinstance(obj, int):
            return int(obj)
        elif isinstance(obj, Decimal):
            if obj.as_tuple().exponent >= 0:
                return int(obj)
            return float(obj)
        elif isinstance(obj, NoneClass):
            return None
        elif isinstance(obj, BoolClass):
            return bool(obj)
        elif isinstance(obj, (dict, frozendict.frozendict)):
            return {key: self.default(val) for key, val in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [self.default(item) for item in obj]
        raise ApiValueError('Unable to prepare type {} for serialization'.format(obj.__class__.__name__))


class ParameterInType(enum.Enum):
    QUERY = 'query'
    HEADER = 'header'
    PATH = 'path'
    COOKIE = 'cookie'


class ParameterStyle(enum.Enum):
    MATRIX = 'matrix'
    LABEL = 'label'
    FORM = 'form'
    SIMPLE = 'simple'
    SPACE_DELIMITED = 'spaceDelimited'
    PIPE_DELIMITED = 'pipeDelimited'
    DEEP_OBJECT = 'deepObject'


class PrefixSeparatorIterator:
    # A class to store prefixes and separators for rfc6570 expansions

    def __init__(self, prefix: str, separator: str):
        self.prefix = prefix
        self.separator = separator
        self.first = True
        if separator in {'.', '|', '%20'}:
            item_separator = separator
        else:
            item_separator = ','
        self.item_separator = item_separator

    def __iter__(self):
        return self

    def __next__(self):
        if self.first:
            self.first = False
            return self.prefix
        return self.separator


class ParameterSerializerBase:
    @classmethod
    def _get_default_explode(cls, style: ParameterStyle) -> bool:
        return False

    @staticmethod
    def __ref6570_item_value(in_data: typing.Any, percent_encode: bool):
        """
        Get representation if str/float/int/None/items in list/ values in dict
        None is returned if an item is undefined, use cases are value=
        - None
        - []
        - {}
        - [None, None None]
        - {'a': None, 'b': None}
        """
        if type(in_data) in {str, float, int}:
            if percent_encode:
                return quote(str(in_data))
            return str(in_data)
        elif isinstance(in_data, none_type):
            # ignored by the expansion process https://datatracker.ietf.org/doc/html/rfc6570#section-3.2.1
            return None
        elif isinstance(in_data, list) and not in_data:
            # ignored by the expansion process https://datatracker.ietf.org/doc/html/rfc6570#section-3.2.1
            return None
        elif isinstance(in_data, dict) and not in_data:
            # ignored by the expansion process https://datatracker.ietf.org/doc/html/rfc6570#section-3.2.1
            return None
        raise ApiValueError('Unable to generate a ref6570 item representation of {}'.format(in_data))

    @staticmethod
    def _to_dict(name: str, value: str):
        return {name: value}

    """
    rfc6570 does not specify how boolean values are serialized so we use lowercase "true" and "false
    """
    @classmethod
    def __konfig_bool_expansion(
        cls,
        in_data: typing.Any,
        prefix_separator_iterator: PrefixSeparatorIterator,
        var_name_piece: str,
        named_parameter_expansion: bool
    ) -> str:
        item_value = "true" if in_data is True else "false"
        if item_value is None or (item_value == '' and prefix_separator_iterator.separator == ';'):
            return next(prefix_separator_iterator) + var_name_piece
        value_pair_equals = '=' if named_parameter_expansion else ''
        return next(prefix_separator_iterator) + var_name_piece + value_pair_equals + item_value

    @classmethod
    def __ref6570_str_float_int_expansion(
        cls,
        variable_name: str,
        in_data: typing.Any,
        explode: bool,
        percent_encode: bool,
        prefix_separator_iterator: PrefixSeparatorIterator,
        var_name_piece: str,
        named_parameter_expansion: bool
    ) -> str:
        item_value = cls.__ref6570_item_value(in_data, percent_encode)
        if item_value is None or (item_value == '' and prefix_separator_iterator.separator == ';'):
            return next(prefix_separator_iterator) + var_name_piece
        value_pair_equals = '=' if named_parameter_expansion else ''
        return next(prefix_separator_iterator) + var_name_piece + value_pair_equals + item_value

    @classmethod
    def __ref6570_list_expansion(
        cls,
        variable_name: str,
        in_data: typing.Any,
        explode: bool,
        percent_encode: bool,
        prefix_separator_iterator: PrefixSeparatorIterator,
        var_name_piece: str,
        named_parameter_expansion: bool
    ) -> str:
        item_values = [cls.__ref6570_item_value(v, percent_encode) for v in in_data]
        item_values = [v for v in item_values if v is not None]
        if not item_values:
            # ignored by the expansion process https://datatracker.ietf.org/doc/html/rfc6570#section-3.2.1
            return ""
        value_pair_equals = '=' if named_parameter_expansion else ''
        if not explode:
            return (
                next(prefix_separator_iterator) +
                var_name_piece +
                value_pair_equals +
                prefix_separator_iterator.item_separator.join(item_values)
            )
        # exploded
        return next(prefix_separator_iterator) + next(prefix_separator_iterator).join(
            [var_name_piece + value_pair_equals + val for val in item_values]
        )

    @classmethod
    def __ref6570_dict_expansion(
        cls,
        variable_name: str,
        in_data: typing.Any,
        explode: bool,
        percent_encode: bool,
        prefix_separator_iterator: PrefixSeparatorIterator,
        var_name_piece: str,
        named_parameter_expansion: bool
    ) -> str:
        in_data_transformed = {key: cls.__ref6570_item_value(val, percent_encode) for key, val in in_data.items()}
        in_data_transformed = {key: val for key, val in in_data_transformed.items() if val is not None}
        if not in_data_transformed:
            # ignored by the expansion process https://datatracker.ietf.org/doc/html/rfc6570#section-3.2.1
            return ""
        value_pair_equals = '=' if named_parameter_expansion else ''
        if not explode:
            return (
                next(prefix_separator_iterator) +
                var_name_piece + value_pair_equals +
                prefix_separator_iterator.item_separator.join(
                    prefix_separator_iterator.item_separator.join(
                        item_pair
                    ) for item_pair in in_data_transformed.items()
                )
            )
        # exploded
        return next(prefix_separator_iterator) + next(prefix_separator_iterator).join(
            [key + '=' + val for key, val in in_data_transformed.items()]
        )

    @classmethod
    def _ref6570_expansion(
        cls,
        variable_name: str,
        in_data: typing.Any,
        explode: bool,
        percent_encode: bool,
        prefix_separator_iterator: PrefixSeparatorIterator
    ) -> str:
        """
        Separator is for separate variables like dict with explode true, not for array item separation
        """
        named_parameter_expansion = prefix_separator_iterator.separator in {'&', ';'}
        var_name_piece = variable_name if named_parameter_expansion else ''
        if type(in_data) in {str, float, int}:
            return cls.__ref6570_str_float_int_expansion(
                variable_name,
                in_data,
                explode,
                percent_encode,
                prefix_separator_iterator,
                var_name_piece,
                named_parameter_expansion
            )
        elif isinstance(in_data, none_type):
            # ignored by the expansion process https://datatracker.ietf.org/doc/html/rfc6570#section-3.2.1
            return ""
        elif isinstance(in_data, list):
            return cls.__ref6570_list_expansion(
                variable_name,
                in_data,
                explode,
                percent_encode,
                prefix_separator_iterator,
                var_name_piece,
                named_parameter_expansion
            )
        elif isinstance(in_data, dict):
            return cls.__ref6570_dict_expansion(
                variable_name,
                in_data,
                explode,
                percent_encode,
                prefix_separator_iterator,
                var_name_piece,
                named_parameter_expansion
            )
        elif isinstance(in_data, bool):
            return cls.__konfig_bool_expansion(
                in_data,
                prefix_separator_iterator,
                var_name_piece,
                named_parameter_expansion
            )
        # bytes, etc
        raise ApiValueError('Unable to generate a ref6570 representation of {}'.format(in_data))


class StyleFormSerializer(ParameterSerializerBase):
    @classmethod
    def _get_default_explode(cls, style: ParameterStyle) -> bool:
        if style is ParameterStyle.FORM:
            return True
        return super()._get_default_explode(style)

    def _serialize_form(
        self,
        in_data: typing.Union[None, int, float, str, bool, dict, list],
        name: str,
        explode: bool,
        percent_encode: bool,
        prefix_separator_iterator: typing.Optional[PrefixSeparatorIterator] = None
    ) -> str:
        if prefix_separator_iterator is None:
            prefix_separator_iterator = PrefixSeparatorIterator('', '&')
        return self._ref6570_expansion(
            variable_name=name,
            in_data=in_data,
            explode=explode,
            percent_encode=percent_encode,
            prefix_separator_iterator=prefix_separator_iterator
        )


class StyleSimpleSerializer(ParameterSerializerBase):

    def _serialize_simple(
        self,
        in_data: typing.Union[None, int, float, str, bool, dict, list],
        name: str,
        explode: bool,
        percent_encode: bool
    ) -> str:
        prefix_separator_iterator = PrefixSeparatorIterator('', ',')
        return self._ref6570_expansion(
            variable_name=name,
            in_data=in_data,
            explode=explode,
            percent_encode=percent_encode,
            prefix_separator_iterator=prefix_separator_iterator
        )


class JSONDetector:
    """
    Works for:
    application/json
    application/json; charset=UTF-8
    application/json-patch+json
    application/geo+json
    """
    __json_content_type_pattern = re.compile("application/[^+]*[+]?(json);?.*")

    @classmethod
    def _content_type_is_json(cls, content_type: str) -> bool:
        if cls.__json_content_type_pattern.match(content_type):
            return True
        return False


@dataclass
class ParameterBase(JSONDetector):
    name: str
    in_type: ParameterInType
    required: bool
    style: typing.Optional[ParameterStyle]
    explode: typing.Optional[bool]
    allow_reserved: typing.Optional[bool]
    schema: typing.Optional[typing.Type[Schema]]
    content: typing.Optional[typing.Dict[str, typing.Type[Schema]]]

    __style_to_in_type = {
        ParameterStyle.MATRIX: {ParameterInType.PATH},
        ParameterStyle.LABEL: {ParameterInType.PATH},
        ParameterStyle.FORM: {ParameterInType.QUERY, ParameterInType.COOKIE},
        ParameterStyle.SIMPLE: {ParameterInType.PATH, ParameterInType.HEADER},
        ParameterStyle.SPACE_DELIMITED: {ParameterInType.QUERY},
        ParameterStyle.PIPE_DELIMITED: {ParameterInType.QUERY},
        ParameterStyle.DEEP_OBJECT: {ParameterInType.QUERY},
    }
    __in_type_to_default_style = {
        ParameterInType.QUERY: ParameterStyle.FORM,
        ParameterInType.PATH: ParameterStyle.SIMPLE,
        ParameterInType.HEADER: ParameterStyle.SIMPLE,
        ParameterInType.COOKIE: ParameterStyle.FORM,
    }
    __disallowed_header_names = {'Accept', 'Content-Type', 'Authorization'}
    _json_encoder = JSONEncoder()

    @classmethod
    def __verify_style_to_in_type(cls, style: typing.Optional[ParameterStyle], in_type: ParameterInType):
        if style is None:
            return
        in_type_set = cls.__style_to_in_type[style]
        if in_type not in in_type_set:
            raise ValueError(
                'Invalid style and in_type combination. For style={} only in_type={} are allowed'.format(
                    style, in_type_set
                )
            )

    def __init__(
        self,
        name: str,
        in_type: ParameterInType,
        required: bool = False,
        style: typing.Optional[ParameterStyle] = None,
        explode: bool = False,
        allow_reserved: typing.Optional[bool] = None,
        schema: typing.Optional[typing.Type[Schema]] = None,
        content: typing.Optional[typing.Dict[str, typing.Type[Schema]]] = None
    ):
        if schema is None and content is None:
            raise ValueError('Value missing; Pass in either schema or content')
        if schema and content:
            raise ValueError('Too many values provided. Both schema and content were provided. Only one may be input')
        if name in self.__disallowed_header_names and in_type is ParameterInType.HEADER:
            raise ValueError('Invalid name, name may not be one of {}'.format(self.__disallowed_header_names))
        self.__verify_style_to_in_type(style, in_type)
        if content is None and style is None:
            style = self.__in_type_to_default_style[in_type]
        if content is not None and in_type in self.__in_type_to_default_style and len(content) != 1:
            raise ValueError('Invalid content length, content length must equal 1')
        self.in_type = in_type
        self.name = name
        self.required = required
        self.style = style
        self.explode = explode
        self.allow_reserved = allow_reserved
        self.schema = schema
        self.content = content

    def _serialize_json(
        self,
        in_data: typing.Union[None, int, float, str, bool, dict, list],
        eliminate_whitespace: bool = False
    ) -> str:
        if eliminate_whitespace:
            return json.dumps(in_data, separators=self._json_encoder.compact_separators)
        return json.dumps(in_data)


class PathParameter(ParameterBase, StyleSimpleSerializer):

    def __init__(
        self,
        name: str,
        required: bool = False,
        style: typing.Optional[ParameterStyle] = None,
        explode: bool = False,
        allow_reserved: typing.Optional[bool] = None,
        schema: typing.Optional[typing.Type[Schema]] = None,
        content: typing.Optional[typing.Dict[str, typing.Type[Schema]]] = None
    ):
        super().__init__(
            name,
            in_type=ParameterInType.PATH,
            required=required,
            style=style,
            explode=explode,
            allow_reserved=allow_reserved,
            schema=schema,
            content=content
        )

    def __serialize_label(
        self,
        in_data: typing.Union[None, int, float, str, bool, dict, list]
    ) -> typing.Dict[str, str]:
        prefix_separator_iterator = PrefixSeparatorIterator('.', '.')
        value = self._ref6570_expansion(
            variable_name=self.name,
            in_data=in_data,
            explode=self.explode,
            percent_encode=True,
            prefix_separator_iterator=prefix_separator_iterator
        )
        return self._to_dict(self.name, value)

    def __serialize_matrix(
        self,
        in_data: typing.Union[None, int, float, str, bool, dict, list]
    ) -> typing.Dict[str, str]:
        prefix_separator_iterator = PrefixSeparatorIterator(';', ';')
        value = self._ref6570_expansion(
            variable_name=self.name,
            in_data=in_data,
            explode=self.explode,
            percent_encode=True,
            prefix_separator_iterator=prefix_separator_iterator
        )
        return self._to_dict(self.name, value)

    def __serialize_simple(
        self,
        in_data: typing.Union[None, int, float, str, bool, dict, list],
    ) -> typing.Dict[str, str]:
        value = self._serialize_simple(
            in_data=in_data,
            name=self.name,
            explode=self.explode,
            percent_encode=True
        )
        return self._to_dict(self.name, value)

    def serialize(
        self,
        in_data: typing.Union[
            Schema, Decimal, int, float, str, date, datetime, None, bool, list, tuple, dict, frozendict.frozendict]
    ) -> typing.Dict[str, str]:
        if self.schema:
            cast_in_data = self.schema(in_data)
            cast_in_data = self._json_encoder.default(cast_in_data)
            """
            simple -> path
                path:
                    returns path_params: dict
            label -> path
                returns path_params
            matrix -> path
                returns path_params
            """
            if self.style:
                if self.style is ParameterStyle.SIMPLE:
                    return self.__serialize_simple(cast_in_data)
                elif self.style is ParameterStyle.LABEL:
                    return self.__serialize_label(cast_in_data)
                elif self.style is ParameterStyle.MATRIX:
                    return self.__serialize_matrix(cast_in_data)
        # self.content will be length one
        for content_type, schema in self.content.items():
            cast_in_data = schema(in_data)
            cast_in_data = self._json_encoder.default(cast_in_data)
            if self._content_type_is_json(content_type):
                value = self._serialize_json(cast_in_data)
                return self._to_dict(self.name, value)
            raise NotImplementedError('Serialization of {} has not yet been implemented'.format(content_type))


class QueryParameter(ParameterBase, StyleFormSerializer):

    def __init__(
        self,
        name: str,
        required: bool = False,
        style: typing.Optional[ParameterStyle] = None,
        explode: typing.Optional[bool] = None,
        allow_reserved: typing.Optional[bool] = None,
        schema: typing.Optional[typing.Type[Schema]] = None,
        content: typing.Optional[typing.Dict[str, typing.Type[Schema]]] = None
    ):
        used_style = ParameterStyle.FORM if style is None else style
        used_explode = self._get_default_explode(used_style) if explode is None else explode

        super().__init__(
            name,
            in_type=ParameterInType.QUERY,
            required=required,
            style=used_style,
            explode=used_explode,
            allow_reserved=allow_reserved,
            schema=schema,
            content=content
        )

    def __serialize_space_delimited(
        self,
        in_data: typing.Union[None, int, float, str, bool, dict, list],
        prefix_separator_iterator: typing.Optional[PrefixSeparatorIterator]
    ) -> typing.Dict[str, str]:
        if prefix_separator_iterator is None:
            prefix_separator_iterator = self.get_prefix_separator_iterator()
        value = self._ref6570_expansion(
            variable_name=self.name,
            in_data=in_data,
            explode=self.explode,
            percent_encode=True,
            prefix_separator_iterator=prefix_separator_iterator
        )
        return self._to_dict(self.name, value)

    def __serialize_pipe_delimited(
        self,
        in_data: typing.Union[None, int, float, str, bool, dict, list],
        prefix_separator_iterator: typing.Optional[PrefixSeparatorIterator]
    ) -> typing.Dict[str, str]:
        if prefix_separator_iterator is None:
            prefix_separator_iterator = self.get_prefix_separator_iterator()
        value = self._ref6570_expansion(
            variable_name=self.name,
            in_data=in_data,
            explode=self.explode,
            percent_encode=True,
            prefix_separator_iterator=prefix_separator_iterator
        )
        return self._to_dict(self.name, value)

    def __serialize_form(
        self,
        in_data: typing.Union[None, int, float, str, bool, dict, list],
        prefix_separator_iterator: typing.Optional[PrefixSeparatorIterator]
    ) -> typing.Dict[str, str]:
        if prefix_separator_iterator is None:
            prefix_separator_iterator = self.get_prefix_separator_iterator()
        value = self._serialize_form(
            in_data,
            name=self.name,
            explode=self.explode,
            percent_encode=True,
            prefix_separator_iterator=prefix_separator_iterator
        )
        return self._to_dict(self.name, value)

    def get_prefix_separator_iterator(self) -> typing.Optional[PrefixSeparatorIterator]:
        if self.style is ParameterStyle.FORM:
            return PrefixSeparatorIterator('?', '&')
        elif self.style is ParameterStyle.SPACE_DELIMITED:
            return PrefixSeparatorIterator('', '%20')
        elif self.style is ParameterStyle.PIPE_DELIMITED:
            return PrefixSeparatorIterator('', '|')

    def serialize(
        self,
        in_data: typing.Union[
            Schema, Decimal, int, float, str, date, datetime, None, bool, list, tuple, dict, frozendict.frozendict],
        prefix_separator_iterator: typing.Optional[PrefixSeparatorIterator] = None
    ) -> typing.Dict[str, str]:
        if self.schema:
            cast_in_data = self.schema(in_data)
            cast_in_data = self._json_encoder.default(cast_in_data)
            """
            form -> query
                query:
                    - GET/HEAD/DELETE: could use fields
                    - PUT/POST: must use urlencode to send parameters
                    returns fields: tuple
            spaceDelimited -> query
                returns fields
            pipeDelimited -> query
                returns fields
            deepObject -> query, https://github.com/OAI/OpenAPI-Specification/issues/1706
                returns fields
            """
            if self.style:
                # TODO update query ones to omit setting values when [] {} or None is input
                if self.style is ParameterStyle.FORM:
                    return self.__serialize_form(cast_in_data, prefix_separator_iterator)
                elif self.style is ParameterStyle.SPACE_DELIMITED:
                    return self.__serialize_space_delimited(cast_in_data, prefix_separator_iterator)
                elif self.style is ParameterStyle.PIPE_DELIMITED:
                    return self.__serialize_pipe_delimited(cast_in_data, prefix_separator_iterator)
        # self.content will be length one
        if prefix_separator_iterator is None:
            prefix_separator_iterator = self.get_prefix_separator_iterator()
        for content_type, schema in self.content.items():
            cast_in_data = schema(in_data)
            cast_in_data = self._json_encoder.default(cast_in_data)
            if self._content_type_is_json(content_type):
                value = self._serialize_json(cast_in_data, eliminate_whitespace=True)
                return self._to_dict(
                    self.name,
                    next(prefix_separator_iterator) + self.name + '=' + quote(value)
                )
            raise NotImplementedError('Serialization of {} has not yet been implemented'.format(content_type))


class CookieParameter(ParameterBase, StyleFormSerializer):

    def __init__(
        self,
        name: str,
        required: bool = False,
        style: typing.Optional[ParameterStyle] = None,
        explode: typing.Optional[bool] = None,
        allow_reserved: typing.Optional[bool] = None,
        schema: typing.Optional[typing.Type[Schema]] = None,
        content: typing.Optional[typing.Dict[str, typing.Type[Schema]]] = None
    ):
        used_style = ParameterStyle.FORM if style is None and content is None and schema else style
        used_explode = self._get_default_explode(used_style) if explode is None else explode

        super().__init__(
            name,
            in_type=ParameterInType.COOKIE,
            required=required,
            style=used_style,
            explode=used_explode,
            allow_reserved=allow_reserved,
            schema=schema,
            content=content
        )

    def serialize(
        self,
        in_data: typing.Union[
            Schema, Decimal, int, float, str, date, datetime, None, bool, list, tuple, dict, frozendict.frozendict]
    ) -> typing.Dict[str, str]:
        if self.schema:
            cast_in_data = self.schema(in_data)
            cast_in_data = self._json_encoder.default(cast_in_data)
            """
            form -> cookie
                returns fields: tuple
            """
            if self.style:
                """
                TODO add escaping of comma, space, equals
                or turn encoding on
                """
                value = self._serialize_form(
                    cast_in_data,
                    explode=self.explode,
                    name=self.name,
                    percent_encode=False,
                    prefix_separator_iterator=PrefixSeparatorIterator('', '&')
                )
                return self._to_dict(self.name, value)
        # self.content will be length one
        for content_type, schema in self.content.items():
            cast_in_data = schema(in_data)
            cast_in_data = self._json_encoder.default(cast_in_data)
            if self._content_type_is_json(content_type):
                value = self._serialize_json(cast_in_data)
                return self._to_dict(self.name, value)
            raise NotImplementedError('Serialization of {} has not yet been implemented'.format(content_type))


class HeaderParameter(ParameterBase, StyleSimpleSerializer):
    def __init__(
        self,
        name: str,
        required: bool = False,
        style: typing.Optional[ParameterStyle] = None,
        explode: bool = False,
        allow_reserved: typing.Optional[bool] = None,
        schema: typing.Optional[typing.Type[Schema]] = None,
        content: typing.Optional[typing.Dict[str, typing.Type[Schema]]] = None
    ):
        super().__init__(
            name,
            in_type=ParameterInType.HEADER,
            required=required,
            style=style,
            explode=explode,
            allow_reserved=allow_reserved,
            schema=schema,
            content=content
        )

    @staticmethod
    def __to_headers(in_data: typing.Tuple[typing.Tuple[str, str], ...]) -> HTTPHeaderDict:
        data = tuple(t for t in in_data if t)
        headers = HTTPHeaderDict()
        if not data:
            return headers
        headers.extend(data)
        return headers

    def serialize(
        self,
        in_data: typing.Union[
            Schema, Decimal, int, float, str, date, datetime, None, bool, list, tuple, dict, frozendict.frozendict]
    ) -> HTTPHeaderDict:
        if self.schema:
            cast_in_data = self.schema(in_data)
            cast_in_data = self._json_encoder.default(cast_in_data)
            """
            simple -> header
                headers: PoolManager needs a mapping, tuple is close
                    returns headers: dict
            """
            if self.style:
                value = self._serialize_simple(cast_in_data, self.name, self.explode, False)
                return self.__to_headers(((self.name, value),))
        # self.content will be length one
        for content_type, schema in self.content.items():
            cast_in_data = schema(in_data)
            cast_in_data = self._json_encoder.default(cast_in_data)
            if self._content_type_is_json(content_type):
                value = self._serialize_json(cast_in_data)
                return self.__to_headers(((self.name, value),))
            raise NotImplementedError('Serialization of {} has not yet been implemented'.format(content_type))


class Encoding:
    def __init__(
        self,
        content_type: str,
        headers: typing.Optional[typing.Dict[str, HeaderParameter]] = None,
        style: typing.Optional[ParameterStyle] = None,
        explode: bool = False,
        allow_reserved: bool = False,
    ):
        self.content_type = content_type
        self.headers = headers
        self.style = style
        self.explode = explode
        self.allow_reserved = allow_reserved


@dataclass
class MediaType:
    """
    Used to store request and response body schema information
    encoding:
        A map between a property name and its encoding information.
        The key, being the property name, MUST exist in the schema as a property.
        The encoding object SHALL only apply to requestBody objects when the media type is
        multipart or application/x-www-form-urlencoded.
    """
    schema: typing.Optional[typing.Type[Schema]] = None
    encoding: typing.Optional[typing.Dict[str, Encoding]] = None


@dataclass
class ApiResponseWithoutDeserialization(ApiResponse):
    pass

@dataclass
class ApiResponseWithoutDeserializationAsync(AsyncApiResponse):
    pass


class OpenApiResponse(JSONDetector):
    __filename_content_disposition_pattern = re.compile('filename="(.+?)"')

    def __init__(
        self,
        response_cls: typing.Type[ApiResponse] = ApiResponse,
        response_cls_async: typing.Type[AsyncApiResponse] = AsyncApiResponse,
        content: typing.Optional[typing.Dict[str, MediaType]] = None,
        headers: typing.Optional[typing.List[HeaderParameter]] = None,
    ):
        self.headers = headers
        if content is not None and len(content) == 0:
            raise ValueError('Invalid value for content, the content dict must have >= 1 entry')
        self.content = content
        self.response_cls = response_cls
        self.response_cls_async = response_cls_async

    @staticmethod
    def __deserialize_json(response: bytes) -> typing.Any:
        # python must be >= 3.9 so we can pass in bytes into json.loads
        return json.loads(response)

    @staticmethod
    def __file_name_from_response_url(response_url: typing.Optional[str]) -> typing.Optional[str]:
        if response_url is None:
            return None
        url_path = urlparse(response_url).path
        if url_path:
            path_basename = os.path.basename(url_path)
            if path_basename:
                _filename, ext = os.path.splitext(path_basename)
                if ext:
                    return path_basename
        return None

    @classmethod
    def __file_name_from_content_disposition(cls, content_disposition: typing.Optional[str]) -> typing.Optional[str]:
        if content_disposition is None:
            return None
        match = cls.__filename_content_disposition_pattern.search(content_disposition)
        if not match:
            return None
        return match.group(1)

    def __deserialize_application_octet_stream(
        self, response: urllib3.HTTPResponse
    ) -> typing.Union[bytes, io.BufferedReader]:
        """
        urllib3 use cases:
        1. when preload_content=True (stream=False) then supports_chunked_reads is False and bytes are returned
        2. when preload_content=False (stream=True) then supports_chunked_reads is True and
            a file will be written and returned
        """
        if response.supports_chunked_reads():
            file_name = (
                self.__file_name_from_content_disposition(response.headers.get('content-disposition'))
                or self.__file_name_from_response_url(response.geturl())
            )

            if file_name is None:
                _fd, path = tempfile.mkstemp()
            else:
                path = os.path.join(tempfile.gettempdir(), file_name)

            with open(path, 'wb') as new_file:
                chunk_size = 1024
                while True:
                    data = response.read(chunk_size)
                    if not data:
                        break
                    new_file.write(data)
            # release_conn is needed for streaming connections only
            response.release_conn()
            new_file = open(path, 'rb')
            return new_file
        else:
            return response.data

    @staticmethod
    def __deserialize_multipart_form_data(
        response: bytes
    ) -> typing.Dict[str, typing.Any]:
        msg = email.message_from_bytes(response)
        return {
            part.get_param("name", header="Content-Disposition"): part.get_payload(
                decode=True
            ).decode(part.get_content_charset())
            if part.get_content_charset()
            else part.get_payload()
            for part in msg.get_payload()
        }

    def __get_schema_for_content_type(
        self,
        content_type
    ) -> typing.Optional[typing.Type[Schema]]:
        """
        Finds the correct SchemaObject for a particular content type. Handles
        the asterisk "*" character that is used to group media types into ranges
        (https://www.rfc-editor.org/rfc/rfc7231#section-5.3.2). Also handles
        parameters in the form of name=value pairs.
        """
        media_types = self.content.keys()
        matched_media_type = OpenApiResponse.match_content_type(
            content_type=content_type,
            media_types=media_types
        )
        if matched_media_type is None:
            return None
        return self.content[matched_media_type].schema

    @staticmethod
    def match_content_type(content_type: str, media_types: typing.List[str]) -> typing.Optional[str]:
        """
        Matches a content type to a media type in a list of media types, handling media type ranges as defined in RFC7231.

        Parameters:
        content_type (str): The content type to match.
        media_types (list): The list of media types to search.

        Returns:
        str: The first media type that matches the content type, or None if no match is found.
        """
        for media_type in media_types:
            if media_type == '*/*' or media_type == content_type:
                return media_type
            elif '/' in media_type:
                type_, subtype = media_type.split('/')
                if (type_ == '*' or type_ == content_type.split('/')[0]) and \
                (subtype == '*' or subtype == content_type.split('/')[1].split(';')[0]):
                    return media_type

        return None

    async def deserialize_async(self, response: AsyncResponseWrapper, configuration: Configuration, skip_deserialization = False) -> AsyncApiResponse:
        """
        Deserializes an HTTP response body into an object.
        """
        content_type = response.http_response.content_type
        deserialized_body = unset
        if self.content is not None:
            if len(self.content) == 0:
                # some specs do not define response content media type schemas
                return self.response_cls_async(
                    round_trip_time=response.round_trip_time,
                    response=response.http_response,
                    body=unset,
                    headers=response.http_response.headers,
                    status=response.http_response.status
                )
            body_schema = self.__get_schema_for_content_type(content_type)
            if body_schema is None:
                raise ApiValueError(
                    f"Invalid content_type returned. Content_type='{content_type}' was returned "
                    f"when only {str(set(self.content))} are defined for status_code={str(response.http_response.status)}"
                )
            if self._content_type_is_json(content_type):
                body_data = self.__deserialize_json(await response.http_response.read())
            elif content_type.startswith('multipart/form-data'):
                body_data = self.__deserialize_multipart_form_data(await response.http_response.read())
            else:
                raise NotImplementedError('Deserialization of {} has not yet been implemented'.format(content_type))
            if skip_deserialization:
                return self.response_cls_async(
                    round_trip_time=response.round_trip_time,
                    response=response.http_response,
                    body=body_data,
                    headers=response.http_response.headers,
                    status=response.http_response.status
                )
            # Execute validation and throw as a side effect if validation fails
            body_schema.from_openapi_data_oapg(
                body_data,
                _configuration=configuration
            )
            # Validation passed, set deserialized_body to plain old deserialized data
            deserialized_body = body_data

        return self.response_cls_async(
            round_trip_time=response.round_trip_time,
            response=response.http_response,
            body=deserialized_body,
            headers=response.http_response.headers,
            status=response.http_response.status
        )

    def deserialize_body(self, response: ResponseWrapper, content_type: str) -> (any, str):
        if self._content_type_is_json(content_type):
            deserialized_body = self.__deserialize_json(response.http_response.data)
        elif content_type == 'application/octet-stream':
            deserialized_body = self.__deserialize_application_octet_stream(response.http_response)
        elif content_type.startswith('multipart/form-data'):
            deserialized_body = self.__deserialize_multipart_form_data(response.http_response.data)
            content_type = 'multipart/form-data'
        else: # If we don't know how to deserialize, use raw body string
            deserialized_body = response.http_response.data.decode()
        return deserialized_body, content_type

    def deserialize(self, response: ResponseWrapper, configuration: Configuration, skip_deserialization = False) -> ApiResponse:
        content_type = response.http_response.headers.get('content-type')
        streamed = response.http_response.supports_chunked_reads()

        deserialized_headers = unset
        if self.headers is not None:
            # TODO add header deserialization here
            pass

        if self.content is not None and len(self.content) == 0:
            # some specs do not define response content media type schemas
            return self.response_cls(
                round_trip_time=response.round_trip_time,
                response=response.http_response,
                body=unset,
                headers=response.http_response.headers,
                status=response.http_response.status
            )

        try:
            deserialized_body, content_type = self.deserialize_body(response, content_type)
        except Exception:
            # Most likely content-type did not match actual body
            deserialized_body = unset

        if not skip_deserialization:
            body_schema = self.__get_schema_for_content_type(content_type)
            if body_schema is None:
                raise ApiValueError(
                    f"Invalid content_type returned. Content_type='{content_type}' was returned "
                    f"when only {str(set(self.content))} are defined for status_code={str(response.http_response.status)}"
                )
            # Execute validation and throw as a side effect if validation fails
            body_schema.from_openapi_data_oapg(
                body_data,
                _configuration=configuration
            )

        if streamed:
            response.http_response.release_conn()

        return self.response_cls(
            round_trip_time=response.round_trip_time,
            response=response.http_response,
            body=deserialized_body,
            headers=response.http_response.headers,
            status=response.http_response.status
        )


class ApiClient:
    """Generic API client for OpenAPI client library builds.

    OpenAPI generic API client. This client handles the client-
    server communication, and is invariant across implementations. Specifics of
    the methods and models for each application are generated from the OpenAPI
    templates.

    This class is auto generated by Konfig (https://konfigthis.com)

    :param configuration: .Configuration object for this client
    :param header_name: a header to pass when making calls to the API.
    :param header_value: a header value to pass when making calls to
        the API.
    :param cookie: a cookie to include in the header when making calls
        to the API
    :param pool_threads: The number of threads to use for async requests
        to the API. More threads means more concurrent API requests.
    """

    _pool = None

    def __init__(
        self,
        configuration: typing.Optional[Configuration] = None,
        header_name: typing.Optional[str] = None,
        header_value: typing.Optional[str] = None,
        cookie: typing.Optional[str] = None,
        pool_threads: int = 1
    ):
        if configuration is None:
            configuration = Configuration()
        self.configuration = configuration
        self.pool_threads = pool_threads

        self.rest_client = rest.RESTClientObject(configuration)
        self.default_headers = HTTPHeaderDict()
        if header_name is not None:
            self.default_headers[header_name] = header_value
        self.cookie = cookie
        # Set default User-Agent.
        self.user_agent = 'Konfig/2.0/python'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        if self._pool:
            self._pool.close()
            self._pool.join()
            self._pool = None
            if hasattr(atexit, 'unregister'):
                atexit.unregister(self.close)

    @property
    def pool(self):
        """Create thread pool on first request
         avoids instantiating unused threadpool for blocking clients.
        """
        if self._pool is None:
            atexit.register(self.close)
            self._pool = ThreadPool(self.pool_threads)
        return self._pool

    @property
    def user_agent(self):
        """User agent for this API client"""
        return self.default_headers['User-Agent']

    @user_agent.setter
    def user_agent(self, value):
        self.default_headers['User-Agent'] = value

    def set_default_header(self, header_name, header_value):
        self.default_headers[header_name] = header_value

    async def __async_call_api(
        self,
        resource_path: str,
        method: str,
        headers: typing.Optional[HTTPHeaderDict] = None,
        serialized_body: typing.Optional[typing.Union[str, bytes]] = None,
        body: typing.Any = None,
        fields: typing.Optional[typing.Tuple[typing.Tuple[str, str], ...]] = None,
        auth_settings: typing.Optional[typing.List[str]] = None,
        stream: bool = False,
        timeout: typing.Optional[typing.Union[float, typing.Tuple]] = None,
        host: typing.Optional[str] = None,
        prefix_separator_iterator: PrefixSeparatorIterator = None,
        **kwargs
    ) -> AsyncResponseWrapper:

        # header parameters
        used_headers = HTTPHeaderDict(self.default_headers)
        if self.cookie:
            headers['Cookie'] = self.cookie

        # auth setting
        resource_path_ref = [self.update_params_for_auth(
            used_headers,
            auth_settings,
            resource_path,
            method,
            body,
            prefix_separator_iterator
        )]

        # must happen after cookie setting and auth setting in case user is overriding those
        if headers:
            used_headers.update(headers)

        request_before_url_hook(
            resource_path_ref=resource_path_ref,
            method=method,
            configuration=self.configuration,
            body=body,
            fields=fields,
            auth_settings=auth_settings,
            headers=used_headers,
        )

        # request url
        if host is None:
            url = self.configuration.host + resource_path_ref[0]
        else:
            # use server/host defined in path or operation instead
            url = host + resource_path_ref[0]

        request_after_hook(
            resource_path=resource_path_ref[0],
            method=method,
            configuration=self.configuration,
            body=body,
            fields=fields,
            auth_settings=auth_settings,
            headers=used_headers,
        )

        # perform request and return response
        response = await self.async_request(
            method,
            url,
            headers=used_headers,
            fields=fields,
            body=serialized_body,
            stream=stream,
            timeout=timeout,
            **kwargs
        )


        return response

    def __call_api(
        self,
        resource_path: str,
        method: str,
        headers: typing.Optional[HTTPHeaderDict] = None,
        serialized_body: typing.Optional[typing.Union[str, bytes]] = None,
        body: typing.Any = None,
        fields: typing.Optional[typing.Tuple[typing.Tuple[str, str], ...]] = None,
        auth_settings: typing.Optional[typing.List[str]] = None,
        stream: bool = False,
        timeout: typing.Optional[typing.Union[float, typing.Tuple]] = None,
        host: typing.Optional[str] = None,
        prefix_separator_iterator: PrefixSeparatorIterator = None,
    ) -> ResponseWrapper:

        # header parameters
        used_headers = HTTPHeaderDict(self.default_headers)
        if self.cookie:
            headers['Cookie'] = self.cookie

        # auth setting
        resource_path_ref = [self.update_params_for_auth(
            used_headers,
            auth_settings,
            resource_path,
            method,
            body,
            prefix_separator_iterator
        )]

        # must happen after cookie setting and auth setting in case user is overriding those
        if headers:
            used_headers.update(headers)

        request_before_url_hook(
            resource_path_ref=resource_path_ref,
            method=method,
            configuration=self.configuration,
            body=body,
            fields=fields,
            auth_settings=auth_settings,
            headers=used_headers,
        )

        # request url
        if host is None:
            url = self.configuration.host + resource_path_ref[0]
        else:
            # use server/host defined in path or operation instead
            url = host + resource_path_ref[0]

        request_after_hook(
            resource_path=resource_path_ref[0],
            method=method,
            configuration=self.configuration,
            body=body,
            fields=fields,
            auth_settings=auth_settings,
            headers=used_headers,
        )

        # perform request and return response
        response = self.request(
            method,
            url,
            headers=used_headers,
            fields=fields,
            body=serialized_body,
            stream=stream,
            timeout=timeout,
        )


        return response

    async def async_call_api(
        self,
        resource_path: str,
        method: str,
        headers: typing.Optional[HTTPHeaderDict] = None,
        serialized_body: typing.Optional[typing.Union[str, bytes]] = None,
        body: typing.Any = None,
        fields: typing.Optional[typing.Tuple[typing.Tuple[str, str], ...]] = None,
        auth_settings: typing.Optional[typing.List[str]] = None,
        stream: bool = False,
        timeout: typing.Optional[typing.Union[float, typing.Tuple]] = None,
        host: typing.Optional[str] = None,
        prefix_separator_iterator: PrefixSeparatorIterator = None,
        **kwargs
    ) -> AsyncResponseWrapper:
        """Makes the HTTP request (synchronous) and returns deserialized data.

        :param resource_path: Path to method endpoint.
        :param method: Method to call.
        :param headers: Header parameters to be
            placed in the request header.
        :param body: Request body.
        :param fields: Request post form parameters,
            for `application/x-www-form-urlencoded`, `multipart/form-data`.
        :param auth_settings: Auth Settings names for the request.
        :param stream: if True, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Also when True, if the openapi spec describes a file download,
                                 the data will be written to a local filesystme file and the BinarySchema
                                 instance will also inherit from FileSchema and FileIO
                                 Default is False.
        :type stream: bool, optional
        :param timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param host: api endpoint host
        :return: response
        """
        return await self.__async_call_api(
            resource_path,
            method,
            headers,
            serialized_body,
            body,
            fields,
            auth_settings,
            stream,
            timeout,
            host,
            prefix_separator_iterator,
            **kwargs
        )

    def call_api(
        self,
        resource_path: str,
        method: str,
        headers: typing.Optional[HTTPHeaderDict] = None,
        serialized_body: typing.Optional[typing.Union[str, bytes]] = None,
        body: typing.Any = None,
        fields: typing.Optional[typing.Tuple[typing.Tuple[str, str], ...]] = None,
        auth_settings: typing.Optional[typing.List[str]] = None,
        stream: bool = False,
        timeout: typing.Optional[typing.Union[float, typing.Tuple]] = None,
        host: typing.Optional[str] = None,
        prefix_separator_iterator: PrefixSeparatorIterator = None,
    ) -> ResponseWrapper:
        """Makes the HTTP request (synchronous) and returns deserialized data.

        :param resource_path: Path to method endpoint.
        :param method: Method to call.
        :param headers: Header parameters to be
            placed in the request header.
        :param body: Request body.
        :param fields: Request post form parameters,
            for `application/x-www-form-urlencoded`, `multipart/form-data`.
        :param auth_settings: Auth Settings names for the request.
        :param stream: if True, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Also when True, if the openapi spec describes a file download,
                                 the data will be written to a local filesystme file and the BinarySchema
                                 instance will also inherit from FileSchema and FileIO
                                 Default is False.
        :type stream: bool, optional
        :param timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param host: api endpoint host
        :return: response
        """
        return self.__call_api(
            resource_path,
            method,
            headers,
            serialized_body,
            body,
            fields,
            auth_settings,
            stream,
            timeout,
            host,
            prefix_separator_iterator,
        )

    def fields_to_dict(self, fields: typing.Optional[typing.Tuple[typing.Tuple[str, str], ...]]):
        """Converts fields to dict.

        :param fields: fields
        :return: dict
        """
        if fields is None:
            return None
        return {k: v for k, v in fields}

    async def async_request(
        self,
        method: str,
        url: str,
        headers: typing.Optional[HTTPHeaderDict] = None,
        fields: typing.Optional[typing.Tuple[typing.Tuple[str, str], ...]] = None,
        body: typing.Optional[typing.Union[str, bytes]] = None,
        stream: bool = False,
        timeout: typing.Optional[typing.Union[float, typing.Tuple]] = None,
        **kwargs
    ) -> AsyncResponseWrapper:
        if body and fields:
            raise ApiValueError("body parameter cannot be used with fields parameter")
        data = None
        if body:
            data=body
        if fields:
            data=self.fields_to_dict(fields)
        session = aiohttp.ClientSession()
        t1 = time.time()
        if method == "GET":
            response = await session.get(url, headers=headers, timeout=timeout, **kwargs)
            return AsyncResponseWrapper(response, time.time() - t1, session)
        elif method == "HEAD":
            response = await session.head(url, headers=headers, timeout=timeout, **kwargs)
            return AsyncResponseWrapper(response, time.time() - t1, session)
        elif method == "OPTIONS":
            response = await session.options(url, data=data, headers=headers, timeout=timeout, **kwargs)
            return AsyncResponseWrapper(response, time.time() - t1, session)
        elif method == "POST":
            response = await session.post(url, data=data, headers=headers, timeout=timeout, **kwargs)
            return AsyncResponseWrapper(response, time.time() - t1, session)
        elif method == "PUT":
            response = await session.put(url, data=data, headers=headers, timeout=timeout, **kwargs)
            return AsyncResponseWrapper(response, time.time() - t1, session)
        elif method == "PATCH":
            response = await session.patch(url, data=data, headers=headers, timeout=timeout, **kwargs)
            return AsyncResponseWrapper(response, time.time() - t1, session)
        elif method == "DELETE":
            response = await session.delete(url, data=data, headers=headers, timeout=timeout, **kwargs)
            return AsyncResponseWrapper(response, time.time() - t1, session)
        raise ApiValueError(
            "http method must be `GET`, `HEAD`, `OPTIONS`,"
            " `POST`, `PATCH`, `PUT` or `DELETE`."
        )

    def request(
        self,
        method: str,
        url: str,
        headers: typing.Optional[HTTPHeaderDict] = None,
        fields: typing.Optional[typing.Tuple[typing.Tuple[str, str], ...]] = None,
        body: typing.Optional[typing.Union[str, bytes]] = None,
        stream: bool = False,
        timeout: typing.Optional[typing.Union[float, typing.Tuple]] = None,
    ) -> ResponseWrapper:
        """Makes the HTTP request using RESTClient."""
        if method == "GET":
            return self.rest_client.GET(url,
                                        stream=stream,
                                        timeout=timeout,
                                        headers=headers)
        elif method == "HEAD":
            return self.rest_client.HEAD(url,
                                         stream=stream,
                                         timeout=timeout,
                                         headers=headers)
        elif method == "OPTIONS":
            return self.rest_client.OPTIONS(url,
                                            headers=headers,
                                            fields=fields,
                                            stream=stream,
                                            timeout=timeout,
                                            body=body)
        elif method == "POST":
            return self.rest_client.POST(url,
                                         headers=headers,
                                         fields=fields,
                                         stream=stream,
                                         timeout=timeout,
                                         body=body)
        elif method == "PUT":
            return self.rest_client.PUT(url,
                                        headers=headers,
                                        fields=fields,
                                        stream=stream,
                                        timeout=timeout,
                                        body=body)
        elif method == "PATCH":
            return self.rest_client.PATCH(url,
                                          headers=headers,
                                          fields=fields,
                                          stream=stream,
                                          timeout=timeout,
                                          body=body)
        elif method == "DELETE":
            return self.rest_client.DELETE(url,
                                           headers=headers,
                                           stream=stream,
                                           timeout=timeout,
                                           body=body)
        else:
            raise ApiValueError(
                "http method must be `GET`, `HEAD`, `OPTIONS`,"
                " `POST`, `PATCH`, `PUT` or `DELETE`."
            )

    def update_params_for_auth(
            self,
            headers,
            auth_settings,
            resource_path,
            method,
            body,
            prefix_separator_iterator: PrefixSeparatorIterator = None
        ) -> str:
        """Updates header and query params based on authentication setting.

        :param headers: Header parameters dict to be updated.
        :param auth_settings: Authentication setting identifiers list.
        :param resource_path: A string representation of the HTTP request resource path.
        :param method: A string representation of the HTTP request method.
        :param body: A object representing the body of the HTTP request.
            The object type is the return value of _encoder.default().
        """
        if not auth_settings:
            return resource_path
        if prefix_separator_iterator is None:
            prefix_separator_iterator = PrefixSeparatorIterator("?", "&")

        for auth in auth_settings:
            auth_setting = self.configuration.auth_settings().get(auth)
            if not auth_setting:
                continue
            if auth_setting['in'] == 'cookie':
                headers.add('Cookie', auth_setting['value'])
            elif auth_setting['in'] == 'header':
                if auth_setting['type'] != 'http-signature':
                    headers.add(auth_setting['key'], auth_setting['value'])
            elif auth_setting['in'] == 'query':
                """ TODO implement auth in query
                need to pass in prefix_separator_iterator
                and need to output resource_path with query params added
                """
                resource_path += ParameterSerializerBase._ref6570_expansion(
                    variable_name=auth_setting['key'],
                    in_data=auth_setting['value'],
                    explode=False,
                    percent_encode=False,
                    prefix_separator_iterator=prefix_separator_iterator
                )
            else:
                raise ApiValueError(
                    'Authentication token must be in `query` or `header`'
                )
        return resource_path


class Api:
    """NOTE:
    This class is auto generated by Konfig (https://konfigthis.com)
    """

    def __init__(self, api_client: typing.Optional[ApiClient] = None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    @staticmethod
    def _verify_typed_dict_inputs_oapg(cls: typing.Type[typing_extensions.TypedDict], data: typing.Dict[str, typing.Any]):
        """
        Ensures that:
        - required keys are present
        - additional properties are not input
        - value stored under required keys do not have the value unset
        Note: detailed value checking is done in schema classes
        """
        missing_required_keys = []
        required_keys_with_unset_values = []
        for required_key in cls.__required_keys__:
            if required_key not in data:
                missing_required_keys.append(required_key)
                continue
            value = data[required_key]
            if value is unset:
                required_keys_with_unset_values.append(required_key)
        if missing_required_keys:
            raise ApiTypeError(
                '{} missing {} required arguments: {}'.format(
                    cls.__name__, len(missing_required_keys), missing_required_keys
                 )
             )
        if required_keys_with_unset_values:
            raise ApiValueError(
                '{} contains invalid unset values for {} required keys: {}'.format(
                    cls.__name__, len(required_keys_with_unset_values), required_keys_with_unset_values
                )
            )

        disallowed_additional_keys = []
        for key in data:
            if key in cls.__required_keys__ or key in cls.__optional_keys__:
                continue
            disallowed_additional_keys.append(key)
        if disallowed_additional_keys:
            raise ApiTypeError(
                '{} got {} unexpected keyword arguments: {}'.format(
                    cls.__name__, len(disallowed_additional_keys), disallowed_additional_keys
                )
            )

    def _get_host_oapg(
        self,
        operation_id: str,
        servers: typing.Tuple[typing.Dict[str, str], ...] = tuple(),
        host_index: typing.Optional[int] = None
    ) -> typing.Optional[str]:
        configuration = self.api_client.configuration
        try:
            if host_index is None:
                index = configuration.server_operation_index.get(
                    operation_id, configuration.server_index
                )
            else:
                index = host_index
            server_variables = configuration.server_operation_variables.get(
                operation_id, configuration.server_variables
            )
            host = configuration.get_host_from_settings(
                index, variables=server_variables, servers=servers
            )
        except IndexError:
            if servers:
                raise ApiValueError(
                    "Invalid host index. Must be 0 <= index < %s" %
                    len(servers)
                )
            host = None
        return host


class SerializedRequestBody(typing_extensions.TypedDict, total=False):
    body: typing.Union[str, bytes]
    fields: typing.Tuple[typing.Union[RequestField, typing.Tuple[str, str]], ...]


class RequestBody(StyleFormSerializer, JSONDetector):
    """
    A request body parameter
    content: content_type to MediaType Schema info
    """
    __json_encoder = JSONEncoder()

    def __init__(
        self,
        content: typing.Dict[str, MediaType],
        required: bool = False,
    ):
        self.required = required
        if len(content) == 0:
            raise ValueError('Invalid value for content, the content dict must have >= 1 entry')
        self.content = content

    def __serialize_json(
        self,
        in_data: typing.Any
    ) -> typing.Dict[str, bytes]:
        in_data = self.__json_encoder.default(in_data)
        json_str = json.dumps(in_data, separators=(",", ":"), ensure_ascii=False).encode(
            "utf-8"
        )
        return dict(body=json_str)

    @staticmethod
    def __serialize_text_plain(in_data: typing.Any) -> typing.Dict[str, str]:
        if isinstance(in_data, frozendict.frozendict):
            raise ValueError('Unable to serialize type frozendict.frozendict to text/plain')
        elif isinstance(in_data, tuple):
            raise ValueError('Unable to serialize type tuple to text/plain')
        elif isinstance(in_data, NoneClass):
            raise ValueError('Unable to serialize type NoneClass to text/plain')
        elif isinstance(in_data, BoolClass):
            raise ValueError('Unable to serialize type BoolClass to text/plain')
        return dict(body=str(in_data))

    def __multipart_json_item(self, key: str, value: Schema) -> RequestField:
        json_value = self.__json_encoder.default(value)
        return RequestField(name=key, data=json.dumps(json_value), headers={'Content-Type': 'application/json'})

    def __multipart_form_item(self, key: str, value: Schema) -> RequestField:
        if isinstance(value, str):
            return RequestField(name=key, data=str(value), headers={'Content-Type': 'text/plain'})
        elif isinstance(value, bytes):
            return RequestField(name=key, data=value, headers={'Content-Type': 'application/octet-stream'})
        elif isinstance(value, FileIO):
            filename = os.path.basename(value.name)
            request_field = RequestField(
                name=key,
                data=value.read(),
                filename=filename,
                headers={'Content-Type': guess_content_type(filename)}
            )
            value.close()
            return request_field
        else:
            return self.__multipart_json_item(key=key, value=value)

    def __serialize_multipart_form_data(
        self, in_data: Schema
    ) -> typing.Dict[str, typing.Tuple[RequestField, ...]]:
        if not isinstance(in_data, frozendict.frozendict) and not isinstance(in_data, list) and not isinstance(in_data, tuple):
            raise ValueError(f'Unable to serialize {in_data} to multipart/form-data because it is not a dict of data or a list of data')
        """
        In a multipart/form-data request body, each schema property, or each element of a schema array property,
        takes a section in the payload with an internal header as defined by RFC7578. The serialization strategy
        for each property of a multipart/form-data request body can be specified in an associated Encoding Object.

        When passing in multipart types, boundaries MAY be used to separate sections of the content being
        transferred – thus, the following default Content-Types are defined for multipart:

        If the (object) property is a primitive, or an array of primitive values, the default Content-Type is text/plain
        If the property is complex, or an array of complex values, the default Content-Type is application/json
            Question: how is the array of primitives encoded?
        If the property is a type: string with a contentEncoding, the default Content-Type is application/octet-stream
        """
        fields: typing.List[RequestField] = []

        def add_field(data):
            for key, value in data.items():
                if isinstance(value, tuple):
                    if value:
                        # values use explode = True, so the code makes a RequestField for each item with name=key
                        for item in value:
                            request_field = self.__multipart_form_item(key=key, value=item)
                            fields.append(request_field)
                    else:
                        # send an empty array as json because exploding will not send it
                        request_field = self.__multipart_json_item(key=key, value=value)
                        fields.append(request_field)
                else:
                    request_field = self.__multipart_form_item(key=key, value=value)
                    fields.append(request_field)

        if isinstance(in_data, list) or isinstance(in_data, tuple):
            for item in in_data:
                add_field(item)
        else:
            add_field(in_data)

        # This is necessary to fill the "Content-Disposition" header needed for naming fields in multipart
        for field in fields:
            field.make_multipart(content_type=field.headers["Content-Type"])

        return dict(fields=tuple(fields))

    def __serialize_application_octet_stream(self, in_data: BinarySchema) -> typing.Dict[str, bytes]:
        if isinstance(in_data, bytes):
            return dict(body=in_data)
        # FileIO type
        result = dict(body=in_data.read())
        in_data.close()
        return result

    def __serialize_application_x_www_form_data(
        self, in_data: typing.Any
    ) -> SerializedRequestBody:
        """
        POST submission of form data in body
        """
        if not isinstance(in_data, frozendict.frozendict):
            raise ValueError(
                f'Unable to serialize {in_data} to application/x-www-form-urlencoded because it is not a dict of data')
        cast_in_data = self.__json_encoder.default(in_data)
        value = self._serialize_form(cast_in_data, name='', explode=True, percent_encode=True)
        return dict(body=value)

    def serialize(
        self, in_data: typing.Any, content_type: str
    ) -> SerializedRequestBody:
        """
        If a str is returned then the result will be assigned to data when making the request
        If a tuple is returned then the result will be used as fields input in encode_multipart_formdata
        Return a tuple of

        The key of the return dict is
        - body for application/json
        - encode_multipart and fields for multipart/form-data
        """
        media_type = self.content[content_type]
        if isinstance(in_data, media_type.schema):
            cast_in_data = in_data
        elif isinstance(in_data, (dict, frozendict.frozendict)) and in_data:
            try:
                cast_in_data = media_type.schema(**in_data)
            except TypeError as e:
                raise MissingRequiredParametersError(e)
        else:
            cast_in_data = media_type.schema(in_data)
        # TODO check for and use encoding if it exists
        # and content_type is multipart or application/x-www-form-urlencoded
        if self._content_type_is_json(content_type):
            return self.__serialize_json(cast_in_data)
        elif content_type == 'text/plain':
            return self.__serialize_text_plain(cast_in_data)
        elif content_type == 'multipart/form-data':
            return self.__serialize_multipart_form_data(cast_in_data)
        elif content_type == 'application/x-www-form-urlencoded':
            return self.__serialize_application_x_www_form_data(cast_in_data)
        elif content_type == 'application/octet-stream':
            return self.__serialize_application_octet_stream(cast_in_data)
        raise NotImplementedError('Serialization has not yet been implemented for {}'.format(content_type))
