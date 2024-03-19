# coding: utf-8

"""
    DigitalOcean API

    # Introduction  The DigitalOcean API allows you to manage Droplets and resources within the DigitalOcean cloud in a simple, programmatic way using conventional HTTP requests.  All of the functionality that you are familiar with in the DigitalOcean control panel is also available through the API, allowing you to script the complex actions that your situation requires.  The API documentation will start with a general overview about the design and technology that has been implemented, followed by reference information about specific endpoints.  ## Requests  Any tool that is fluent in HTTP can communicate with the API simply by requesting the correct URI. Requests should be made using the HTTPS protocol so that traffic is encrypted. The interface responds to different methods depending on the action required.  |Method|Usage| |--- |--- | |GET|For simple retrieval of information about your account, Droplets, or environment, you should use the GET method.  The information you request will be returned to you as a JSON object. The attributes defined by the JSON object can be used to form additional requests.  Any request using the GET method is read-only and will not affect any of the objects you are querying.| |DELETE|To destroy a resource and remove it from your account and environment, the DELETE method should be used.  This will remove the specified object if it is found.  If it is not found, the operation will return a response indicating that the object was not found. This idempotency means that you do not have to check for a resource's availability prior to issuing a delete command, the final state will be the same regardless of its existence.| |PUT|To update the information about a resource in your account, the PUT method is available. Like the DELETE Method, the PUT method is idempotent.  It sets the state of the target using the provided values, regardless of their current values. Requests using the PUT method do not need to check the current attributes of the object.| |PATCH|Some resources support partial modification. In these cases, the PATCH method is available. Unlike PUT which generally requires a complete representation of a resource, a PATCH request is is a set of instructions on how to modify a resource updating only specific attributes.| |POST|To create a new object, your request should specify the POST method. The POST request includes all of the attributes necessary to create a new object.  When you wish to create a new object, send a POST request to the target endpoint.| |HEAD|Finally, to retrieve metadata information, you should use the HEAD method to get the headers.  This returns only the header of what would be returned with an associated GET request. Response headers contain some useful information about your API access and the results that are available for your request. For instance, the headers contain your current rate-limit value and the amount of time available until the limit resets. It also contains metrics about the total number of objects found, pagination information, and the total content length.|   ## HTTP Statuses  Along with the HTTP methods that the API responds to, it will also return standard HTTP statuses, including error codes.  In the event of a problem, the status will contain the error code, while the body of the response will usually contain additional information about the problem that was encountered.  In general, if the status returned is in the 200 range, it indicates that the request was fulfilled successfully and that no error was encountered.  Return codes in the 400 range typically indicate that there was an issue with the request that was sent. Among other things, this could mean that you did not authenticate correctly, that you are requesting an action that you do not have authorization for, that the object you are requesting does not exist, or that your request is malformed.  If you receive a status in the 500 range, this generally indicates a server-side problem. This means that we are having an issue on our end and cannot fulfill your request currently.  400 and 500 level error responses will include a JSON object in their body, including the following attributes:  |Name|Type|Description| |--- |--- |--- | |id|string|A short identifier corresponding to the HTTP status code returned. For example, the ID for a response returning a 404 status code would be \"not_found.\"| |message|string|A message providing additional information about the error, including details to help resolve it when possible.| |request_id|string|Optionally, some endpoints may include a request ID that should be provided when reporting bugs or opening support tickets to help identify the issue.|  ### Example Error Response  ```     HTTP/1.1 403 Forbidden     {       \"id\":       \"forbidden\",       \"message\":  \"You do not have access for the attempted action.\"     } ```  ## Responses  When a request is successful, a response body will typically be sent back in the form of a JSON object. An exception to this is when a DELETE request is processed, which will result in a successful HTTP 204 status and an empty response body.  Inside of this JSON object, the resource root that was the target of the request will be set as the key. This will be the singular form of the word if the request operated on a single object, and the plural form of the word if a collection was processed.  For example, if you send a GET request to `/v2/droplets/$DROPLET_ID` you will get back an object with a key called \"`droplet`\". However, if you send the GET request to the general collection at `/v2/droplets`, you will get back an object with a key called \"`droplets`\".  The value of these keys will generally be a JSON object for a request on a single object and an array of objects for a request on a collection of objects.  ### Response for a Single Object  ```     {         \"droplet\": {             \"name\": \"example.com\"             . . .         }     } ```  ### Response for an Object Collection  ```     {         \"droplets\": [             {                 \"name\": \"example.com\"                 . . .             },             {                 \"name\": \"second.com\"                 . . .             }         ]     } ```  ## Meta  In addition to the main resource root, the response may also contain a `meta` object. This object contains information about the response itself.  The `meta` object contains a `total` key that is set to the total number of objects returned by the request. This has implications on the `links` object and pagination.  The `meta` object will only be displayed when it has a value. Currently, the `meta` object will have a value when a request is made on a collection (like `droplets` or `domains`).   ### Sample Meta Object  ```     {         . . .         \"meta\": {             \"total\": 43         }         . . .     } ```  ## Links & Pagination  The `links` object is returned as part of the response body when pagination is enabled. By default, 20 objects are returned per page. If the response contains 20 objects or fewer, no `links` object will be returned. If the response contains more than 20 objects, the first 20 will be returned along with the `links` object.  You can request a different pagination limit or force pagination by appending `?per_page=` to the request with the number of items you would like per page. For instance, to show only two results per page, you could add `?per_page=2` to the end of your query. The maximum number of results per page is 200.  The `links` object contains a `pages` object. The `pages` object, in turn, contains keys indicating the relationship of additional pages. The values of these are the URLs of the associated pages. The keys will be one of the following:  *   **first**: The URI of the first page of results. *   **prev**: The URI of the previous sequential page of results. *   **next**: The URI of the next sequential page of results. *   **last**: The URI of the last page of results.  The `pages` object will only include the links that make sense. So for the first page of results, no `first` or `prev` links will ever be set. This convention holds true in other situations where a link would not make sense.  ### Sample Links Object  ```     {         . . .         \"links\": {             \"pages\": {                 \"last\": \"https://api.digitalocean.com/v2/images?page=2\",                 \"next\": \"https://api.digitalocean.com/v2/images?page=2\"             }         }         . . .     } ```  ## Rate Limit  Requests through the API are rate limited per OAuth token. Current rate limits:  *   5,000 requests per hour *   250 requests per minute (5% of the hourly total)  Once you exceed either limit, you will be rate limited until the next cycle starts. Space out any requests that you would otherwise issue in bursts for the best results.  The rate limiting information is contained within the response headers of each request. The relevant headers are:  *   **ratelimit-limit**: The number of requests that can be made per hour. *   **ratelimit-remaining**: The number of requests that remain before you hit your request limit. See the information below for how the request limits expire. *   **ratelimit-reset**: This represents the time when the oldest request will expire. The value is given in [Unix epoch time](http://en.wikipedia.org/wiki/Unix_time). See below for more information about how request limits expire.  More rate limiting information is returned only within burst limit error response headers: *   **retry-after**: The number of seconds to wait before making another request when rate limited.  As long as the `ratelimit-remaining` count is above zero, you will be able to make additional requests.  The way that a request expires and is removed from the current limit count is important to understand. Rather than counting all of the requests for an hour and resetting the `ratelimit-remaining` value at the end of the hour, each request instead has its own timer.  This means that each request contributes toward the `ratelimit-remaining` count for one complete hour after the request is made. When that request's timer runs out, it is no longer counted towards the request limit.  This has implications on the meaning of the `ratelimit-reset` header as well. Because the entire rate limit is not reset at one time, the value of this header is set to the time when the _oldest_ request will expire.  Keep this in mind if you see your `ratelimit-reset` value change, but not move an entire hour into the future.  If the `ratelimit-remaining` reaches zero, subsequent requests will receive a 429 error code until the request reset has been reached.   `ratelimit-remaining` reaching zero can also indicate that the \"burst limit\" of 250  requests per minute limit was met, even if the 5,000 requests per hour limit was not.  In this case, the 429 error response will include a retry-after header to indicate how  long to wait (in seconds) until the request may be retried.  You can see the format of the response in the examples.   **Note:** The following endpoints have special rate limit requirements that are independent of the limits defined above.  *   Only 12 `POST` requests to the `/v2/floating_ips` endpoint to create Floating IPs can be made per 60 seconds. *   Only 10 `GET` requests to the `/v2/account/keys` endpoint to list SSH keys can be made per 60 seconds. *   Only 5 requests to any and all `v2/cdn/endpoints` can be made per 10 seconds. This includes `v2/cdn/endpoints`,      `v2/cdn/endpoints/$ENDPOINT_ID`, and `v2/cdn/endpoints/$ENDPOINT_ID/cache`. *   Only 50 strings within the `files` json struct in the `v2/cdn/endpoints/$ENDPOINT_ID/cache` [payload](https://docs.digitalocean.com/reference/api/api-reference/#operation/cdn_purge_cache)      can be requested every 20 seconds.  ### Sample Rate Limit Headers  ```     . . .     ratelimit-limit: 1200     ratelimit-remaining: 1193     rateLimit-reset: 1402425459     . . . ```    ### Sample Rate Limit Headers When Burst Limit is Reached:  ```     . . .     ratelimit-limit: 5000     ratelimit-remaining: 0     rateLimit-reset: 1402425459     retry-after: 29     . . . ```  ### Sample Rate Exceeded Response  ```     429 Too Many Requests     {             id: \"too_many_requests\",             message: \"API Rate limit exceeded.\"     } ```  ## Curl Examples  Throughout this document, some example API requests will be given using the `curl` command. This will allow us to demonstrate the various endpoints in a simple, textual format.      These examples assume that you are using a Linux or macOS command line. To run these commands on a Windows machine, you can either use cmd.exe, PowerShell, or WSL:  * For cmd.exe, use the `set VAR=VALUE` [syntax](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/set_1) to define environment variables, call them with `%VAR%`, then replace all backslashes (`\\`) in the examples with carets (`^`).  * For PowerShell, use the `$Env:VAR = \"VALUE\"` [syntax](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_environment_variables?view=powershell-7.2) to define environment variables, call them with `$Env:VAR`, then replace `curl` with `curl.exe` and all backslashes (`\\`) in the examples with backticks (`` ` ``).  * WSL is a compatibility layer that allows you to emulate a Linux terminal on a Windows machine. Install WSL with our [community tutorial](https://www.digitalocean.com/community/tutorials/how-to-install-the-windows-subsystem-for-linux-2-on-microsoft-windows-10),  then follow this API documentation normally.  The names of account-specific references (like Droplet IDs, for instance) will be represented by variables. For instance, a Droplet ID may be represented by a variable called `$DROPLET_ID`. You can set the associated variables in your environment if you wish to use the examples without modification.  The first variable that you should set to get started is your OAuth authorization token. The next section will go over the details of this, but you can set an environmental variable for it now.  Generate a token by going to the [Apps & API](https://cloud.digitalocean.com/settings/applications) section of the DigitalOcean control panel. Use an existing token if you have saved one, or generate a new token with the \"Generate new token\" button. Copy the generated token and use it to set and export the TOKEN variable in your environment as the example shows.  You may also wish to set some other variables now or as you go along. For example, you may wish to set the `DROPLET_ID` variable to one of your Droplet IDs since this will be used frequently in the API.  If you are following along, make sure you use a Droplet ID that you control so that your commands will execute correctly.  If you need access to the headers of a response through `curl`, you can pass the `-i` flag to display the header information along with the body. If you are only interested in the header, you can instead pass the `-I` flag, which will exclude the response body entirely.   ### Set and Export your OAuth Token  ``` export DIGITALOCEAN_TOKEN=your_token_here ```  ### Set and Export a Variable  ``` export DROPLET_ID=1111111 ```  ## Parameters  There are two different ways to pass parameters in a request with the API.  When passing parameters to create or update an object, parameters should be passed as a JSON object containing the appropriate attribute names and values as key-value pairs. When you use this format, you should specify that you are sending a JSON object in the header. This is done by setting the `Content-Type` header to `application/json`. This ensures that your request is interpreted correctly.  When passing parameters to filter a response on GET requests, parameters can be passed using standard query attributes. In this case, the parameters would be embedded into the URI itself by appending a `?` to the end of the URI and then setting each attribute with an equal sign. Attributes can be separated with a `&`. Tools like `curl` can create the appropriate URI when given parameters and values; this can also be done using the `-F` flag and then passing the key and value as an argument. The argument should take the form of a quoted string with the attribute being set to a value with an equal sign.  ### Pass Parameters as a JSON Object  ```     curl -H \"Authorization: Bearer $DIGITALOCEAN_TOKEN\" \\         -H \"Content-Type: application/json\" \\         -d '{\"name\": \"example.com\", \"ip_address\": \"127.0.0.1\"}' \\         -X POST \"https://api.digitalocean.com/v2/domains\" ```  ### Pass Filter Parameters as a Query String  ```      curl -H \"Authorization: Bearer $DIGITALOCEAN_TOKEN\" \\          -X GET \\          \"https://api.digitalocean.com/v2/images?private=true\" ```  ## Cross Origin Resource Sharing  In order to make requests to the API from other domains, the API implements Cross Origin Resource Sharing (CORS) support.  CORS support is generally used to create AJAX requests outside of the domain that the request originated from. This is necessary to implement projects like control panels utilizing the API. This tells the browser that it can send requests to an outside domain.  The procedure that the browser initiates in order to perform these actions (other than GET requests) begins by sending a \"preflight\" request. This sets the `Origin` header and uses the `OPTIONS` method. The server will reply back with the methods it allows and some of the limits it imposes. The client then sends the actual request if it falls within the allowed constraints.  This process is usually done in the background by the browser, but you can use curl to emulate this process using the example provided. The headers that will be set to show the constraints are:  *   **Access-Control-Allow-Origin**: This is the domain that is sent by the client or browser as the origin of the request. It is set through an `Origin` header. *   **Access-Control-Allow-Methods**: This specifies the allowed options for requests from that domain. This will generally be all available methods. *   **Access-Control-Expose-Headers**: This will contain the headers that will be available to requests from the origin domain. *   **Access-Control-Max-Age**: This is the length of time that the access is considered valid. After this expires, a new preflight should be sent. *   **Access-Control-Allow-Credentials**: This will be set to `true`. It basically allows you to send your OAuth token for authentication.  You should not need to be concerned with the details of these headers, because the browser will typically do all of the work for you. 

    The version of the OpenAPI document: 2.0
    Contact: api-engineering@digitalocean.com
    Generated by: https://konfigthis.com
"""

from datetime import date, datetime  # noqa: F401
import decimal  # noqa: F401
import functools  # noqa: F401
import io  # noqa: F401
import re  # noqa: F401
import typing  # noqa: F401
import typing_extensions  # noqa: F401
import uuid  # noqa: F401

import frozendict  # noqa: F401

from digital_ocean_python_sdk import schemas  # noqa: F401


class Mysql(
    schemas.DictSchema
):
    """
    This class is auto generated by Konfig (https://konfigthis.com)
    """


    class MetaOapg:
        
        class properties:
            
            
            class backup_hour(
                schemas.IntSchema
            ):
            
            
                class MetaOapg:
                    inclusive_maximum = 23
                    inclusive_minimum = 0
            
            
            class backup_minute(
                schemas.IntSchema
            ):
            
            
                class MetaOapg:
                    inclusive_maximum = 59
                    inclusive_minimum = 0
            
            
            class sql_mode(
                schemas.StrSchema
            ):
            
            
                class MetaOapg:
                    max_length = 1024
                    regex=[{
                        'pattern': r'^[A-Z_]*(,[A-Z_]+)*$',
                    }]
            
            
            class connect_timeout(
                schemas.IntSchema
            ):
            
            
                class MetaOapg:
                    inclusive_maximum = 3600
                    inclusive_minimum = 2
            
            
            class default_time_zone(
                schemas.StrSchema
            ):
            
            
                class MetaOapg:
                    max_length = 100
                    min_length = 2
            
            
            class group_concat_max_len(
                schemas.IntSchema
            ):
            
            
                class MetaOapg:
                    inclusive_maximum = 384
                    inclusive_minimum = 4
            
            
            class information_schema_stats_expiry(
                schemas.IntSchema
            ):
            
            
                class MetaOapg:
                    inclusive_maximum = 31536000
                    inclusive_minimum = 900
            
            
            class innodb_ft_min_token_size(
                schemas.IntSchema
            ):
            
            
                class MetaOapg:
                    inclusive_maximum = 16
                    inclusive_minimum = 0
            
            
            class innodb_ft_server_stopword_table(
                schemas.StrSchema
            ):
            
            
                class MetaOapg:
                    max_length = 1024
                    regex=[{
                        'pattern': r'^.+/.+$',
                    }]
            
            
            class innodb_lock_wait_timeout(
                schemas.IntSchema
            ):
            
            
                class MetaOapg:
                    inclusive_maximum = 3600
                    inclusive_minimum = 1
            
            
            class innodb_log_buffer_size(
                schemas.IntSchema
            ):
            
            
                class MetaOapg:
                    inclusive_maximum = 4294967295
                    inclusive_minimum = 1048576
            
            
            class innodb_online_alter_log_max_size(
                schemas.IntSchema
            ):
            
            
                class MetaOapg:
                    inclusive_maximum = 1099511627776
                    inclusive_minimum = 65536
            innodb_print_all_deadlocks = schemas.BoolSchema
            innodb_rollback_on_timeout = schemas.BoolSchema
            
            
            class interactive_timeout(
                schemas.IntSchema
            ):
            
            
                class MetaOapg:
                    inclusive_maximum = 604800
                    inclusive_minimum = 30
            
            
            class internal_tmp_mem_storage_engine(
                schemas.EnumBase,
                schemas.StrSchema
            ):
            
            
                class MetaOapg:
                    enum_value_to_name = {
                        "TempTable": "TEMP_TABLE",
                        "MEMORY": "MEMORY",
                    }
                
                @schemas.classproperty
                def TEMP_TABLE(cls):
                    return cls("TempTable")
                
                @schemas.classproperty
                def MEMORY(cls):
                    return cls("MEMORY")
            
            
            class net_read_timeout(
                schemas.IntSchema
            ):
            
            
                class MetaOapg:
                    inclusive_maximum = 3600
                    inclusive_minimum = 1
            
            
            class net_write_timeout(
                schemas.IntSchema
            ):
            
            
                class MetaOapg:
                    inclusive_maximum = 3600
                    inclusive_minimum = 1
            sql_require_primary_key = schemas.BoolSchema
            
            
            class wait_timeout(
                schemas.IntSchema
            ):
            
            
                class MetaOapg:
                    inclusive_maximum = 2147483
                    inclusive_minimum = 1
            
            
            class max_allowed_packet(
                schemas.IntSchema
            ):
            
            
                class MetaOapg:
                    inclusive_maximum = 1073741824
                    inclusive_minimum = 102400
            
            
            class max_heap_table_size(
                schemas.IntSchema
            ):
            
            
                class MetaOapg:
                    inclusive_maximum = 1073741824
                    inclusive_minimum = 1048576
            
            
            class sort_buffer_size(
                schemas.IntSchema
            ):
            
            
                class MetaOapg:
                    inclusive_maximum = 1073741824
                    inclusive_minimum = 32768
            
            
            class tmp_table_size(
                schemas.IntSchema
            ):
            
            
                class MetaOapg:
                    inclusive_maximum = 1073741824
                    inclusive_minimum = 1048576
            slow_query_log = schemas.BoolSchema
            
            
            class long_query_time(
                schemas.NumberSchema
            ):
            
            
                class MetaOapg:
                    inclusive_maximum = 3600
                    inclusive_minimum = 0
            
            
            class binlog_retention_period(
                schemas.NumberSchema
            ):
            
            
                class MetaOapg:
                    inclusive_maximum = 86400
                    inclusive_minimum = 600
            
            
            class innodb_change_buffer_max_size(
                schemas.IntSchema
            ):
            
            
                class MetaOapg:
                    inclusive_maximum = 50
                    inclusive_minimum = 0
            
            
            class innodb_flush_neighbors(
                schemas.EnumBase,
                schemas.IntSchema
            ):
            
            
                class MetaOapg:
                    enum_value_to_name = {
                        0: "POSITIVE_0",
                        1: "POSITIVE_1",
                        2: "POSITIVE_2",
                    }
                
                @schemas.classproperty
                def POSITIVE_0(cls):
                    return cls(0)
                
                @schemas.classproperty
                def POSITIVE_1(cls):
                    return cls(1)
                
                @schemas.classproperty
                def POSITIVE_2(cls):
                    return cls(2)
            
            
            class innodb_read_io_threads(
                schemas.IntSchema
            ):
            
            
                class MetaOapg:
                    inclusive_maximum = 64
                    inclusive_minimum = 1
            
            
            class innodb_write_io_threads(
                schemas.IntSchema
            ):
            
            
                class MetaOapg:
                    inclusive_maximum = 64
                    inclusive_minimum = 1
            
            
            class innodb_thread_concurrency(
                schemas.IntSchema
            ):
            
            
                class MetaOapg:
                    inclusive_maximum = 1000
                    inclusive_minimum = 0
            
            
            class net_buffer_length(
                schemas.IntSchema
            ):
            
            
                class MetaOapg:
                    inclusive_maximum = 1048576
                    inclusive_minimum = 1024
            __annotations__ = {
                "backup_hour": backup_hour,
                "backup_minute": backup_minute,
                "sql_mode": sql_mode,
                "connect_timeout": connect_timeout,
                "default_time_zone": default_time_zone,
                "group_concat_max_len": group_concat_max_len,
                "information_schema_stats_expiry": information_schema_stats_expiry,
                "innodb_ft_min_token_size": innodb_ft_min_token_size,
                "innodb_ft_server_stopword_table": innodb_ft_server_stopword_table,
                "innodb_lock_wait_timeout": innodb_lock_wait_timeout,
                "innodb_log_buffer_size": innodb_log_buffer_size,
                "innodb_online_alter_log_max_size": innodb_online_alter_log_max_size,
                "innodb_print_all_deadlocks": innodb_print_all_deadlocks,
                "innodb_rollback_on_timeout": innodb_rollback_on_timeout,
                "interactive_timeout": interactive_timeout,
                "internal_tmp_mem_storage_engine": internal_tmp_mem_storage_engine,
                "net_read_timeout": net_read_timeout,
                "net_write_timeout": net_write_timeout,
                "sql_require_primary_key": sql_require_primary_key,
                "wait_timeout": wait_timeout,
                "max_allowed_packet": max_allowed_packet,
                "max_heap_table_size": max_heap_table_size,
                "sort_buffer_size": sort_buffer_size,
                "tmp_table_size": tmp_table_size,
                "slow_query_log": slow_query_log,
                "long_query_time": long_query_time,
                "binlog_retention_period": binlog_retention_period,
                "innodb_change_buffer_max_size": innodb_change_buffer_max_size,
                "innodb_flush_neighbors": innodb_flush_neighbors,
                "innodb_read_io_threads": innodb_read_io_threads,
                "innodb_write_io_threads": innodb_write_io_threads,
                "innodb_thread_concurrency": innodb_thread_concurrency,
                "net_buffer_length": net_buffer_length,
            }
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["backup_hour"]) -> MetaOapg.properties.backup_hour: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["backup_minute"]) -> MetaOapg.properties.backup_minute: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["sql_mode"]) -> MetaOapg.properties.sql_mode: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["connect_timeout"]) -> MetaOapg.properties.connect_timeout: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["default_time_zone"]) -> MetaOapg.properties.default_time_zone: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["group_concat_max_len"]) -> MetaOapg.properties.group_concat_max_len: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["information_schema_stats_expiry"]) -> MetaOapg.properties.information_schema_stats_expiry: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["innodb_ft_min_token_size"]) -> MetaOapg.properties.innodb_ft_min_token_size: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["innodb_ft_server_stopword_table"]) -> MetaOapg.properties.innodb_ft_server_stopword_table: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["innodb_lock_wait_timeout"]) -> MetaOapg.properties.innodb_lock_wait_timeout: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["innodb_log_buffer_size"]) -> MetaOapg.properties.innodb_log_buffer_size: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["innodb_online_alter_log_max_size"]) -> MetaOapg.properties.innodb_online_alter_log_max_size: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["innodb_print_all_deadlocks"]) -> MetaOapg.properties.innodb_print_all_deadlocks: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["innodb_rollback_on_timeout"]) -> MetaOapg.properties.innodb_rollback_on_timeout: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["interactive_timeout"]) -> MetaOapg.properties.interactive_timeout: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["internal_tmp_mem_storage_engine"]) -> MetaOapg.properties.internal_tmp_mem_storage_engine: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["net_read_timeout"]) -> MetaOapg.properties.net_read_timeout: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["net_write_timeout"]) -> MetaOapg.properties.net_write_timeout: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["sql_require_primary_key"]) -> MetaOapg.properties.sql_require_primary_key: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["wait_timeout"]) -> MetaOapg.properties.wait_timeout: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["max_allowed_packet"]) -> MetaOapg.properties.max_allowed_packet: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["max_heap_table_size"]) -> MetaOapg.properties.max_heap_table_size: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["sort_buffer_size"]) -> MetaOapg.properties.sort_buffer_size: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["tmp_table_size"]) -> MetaOapg.properties.tmp_table_size: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["slow_query_log"]) -> MetaOapg.properties.slow_query_log: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["long_query_time"]) -> MetaOapg.properties.long_query_time: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["binlog_retention_period"]) -> MetaOapg.properties.binlog_retention_period: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["innodb_change_buffer_max_size"]) -> MetaOapg.properties.innodb_change_buffer_max_size: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["innodb_flush_neighbors"]) -> MetaOapg.properties.innodb_flush_neighbors: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["innodb_read_io_threads"]) -> MetaOapg.properties.innodb_read_io_threads: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["innodb_write_io_threads"]) -> MetaOapg.properties.innodb_write_io_threads: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["innodb_thread_concurrency"]) -> MetaOapg.properties.innodb_thread_concurrency: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["net_buffer_length"]) -> MetaOapg.properties.net_buffer_length: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["backup_hour", "backup_minute", "sql_mode", "connect_timeout", "default_time_zone", "group_concat_max_len", "information_schema_stats_expiry", "innodb_ft_min_token_size", "innodb_ft_server_stopword_table", "innodb_lock_wait_timeout", "innodb_log_buffer_size", "innodb_online_alter_log_max_size", "innodb_print_all_deadlocks", "innodb_rollback_on_timeout", "interactive_timeout", "internal_tmp_mem_storage_engine", "net_read_timeout", "net_write_timeout", "sql_require_primary_key", "wait_timeout", "max_allowed_packet", "max_heap_table_size", "sort_buffer_size", "tmp_table_size", "slow_query_log", "long_query_time", "binlog_retention_period", "innodb_change_buffer_max_size", "innodb_flush_neighbors", "innodb_read_io_threads", "innodb_write_io_threads", "innodb_thread_concurrency", "net_buffer_length", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["backup_hour"]) -> typing.Union[MetaOapg.properties.backup_hour, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["backup_minute"]) -> typing.Union[MetaOapg.properties.backup_minute, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["sql_mode"]) -> typing.Union[MetaOapg.properties.sql_mode, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["connect_timeout"]) -> typing.Union[MetaOapg.properties.connect_timeout, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["default_time_zone"]) -> typing.Union[MetaOapg.properties.default_time_zone, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["group_concat_max_len"]) -> typing.Union[MetaOapg.properties.group_concat_max_len, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["information_schema_stats_expiry"]) -> typing.Union[MetaOapg.properties.information_schema_stats_expiry, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["innodb_ft_min_token_size"]) -> typing.Union[MetaOapg.properties.innodb_ft_min_token_size, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["innodb_ft_server_stopword_table"]) -> typing.Union[MetaOapg.properties.innodb_ft_server_stopword_table, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["innodb_lock_wait_timeout"]) -> typing.Union[MetaOapg.properties.innodb_lock_wait_timeout, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["innodb_log_buffer_size"]) -> typing.Union[MetaOapg.properties.innodb_log_buffer_size, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["innodb_online_alter_log_max_size"]) -> typing.Union[MetaOapg.properties.innodb_online_alter_log_max_size, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["innodb_print_all_deadlocks"]) -> typing.Union[MetaOapg.properties.innodb_print_all_deadlocks, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["innodb_rollback_on_timeout"]) -> typing.Union[MetaOapg.properties.innodb_rollback_on_timeout, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["interactive_timeout"]) -> typing.Union[MetaOapg.properties.interactive_timeout, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["internal_tmp_mem_storage_engine"]) -> typing.Union[MetaOapg.properties.internal_tmp_mem_storage_engine, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["net_read_timeout"]) -> typing.Union[MetaOapg.properties.net_read_timeout, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["net_write_timeout"]) -> typing.Union[MetaOapg.properties.net_write_timeout, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["sql_require_primary_key"]) -> typing.Union[MetaOapg.properties.sql_require_primary_key, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["wait_timeout"]) -> typing.Union[MetaOapg.properties.wait_timeout, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["max_allowed_packet"]) -> typing.Union[MetaOapg.properties.max_allowed_packet, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["max_heap_table_size"]) -> typing.Union[MetaOapg.properties.max_heap_table_size, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["sort_buffer_size"]) -> typing.Union[MetaOapg.properties.sort_buffer_size, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["tmp_table_size"]) -> typing.Union[MetaOapg.properties.tmp_table_size, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["slow_query_log"]) -> typing.Union[MetaOapg.properties.slow_query_log, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["long_query_time"]) -> typing.Union[MetaOapg.properties.long_query_time, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["binlog_retention_period"]) -> typing.Union[MetaOapg.properties.binlog_retention_period, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["innodb_change_buffer_max_size"]) -> typing.Union[MetaOapg.properties.innodb_change_buffer_max_size, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["innodb_flush_neighbors"]) -> typing.Union[MetaOapg.properties.innodb_flush_neighbors, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["innodb_read_io_threads"]) -> typing.Union[MetaOapg.properties.innodb_read_io_threads, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["innodb_write_io_threads"]) -> typing.Union[MetaOapg.properties.innodb_write_io_threads, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["innodb_thread_concurrency"]) -> typing.Union[MetaOapg.properties.innodb_thread_concurrency, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["net_buffer_length"]) -> typing.Union[MetaOapg.properties.net_buffer_length, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["backup_hour", "backup_minute", "sql_mode", "connect_timeout", "default_time_zone", "group_concat_max_len", "information_schema_stats_expiry", "innodb_ft_min_token_size", "innodb_ft_server_stopword_table", "innodb_lock_wait_timeout", "innodb_log_buffer_size", "innodb_online_alter_log_max_size", "innodb_print_all_deadlocks", "innodb_rollback_on_timeout", "interactive_timeout", "internal_tmp_mem_storage_engine", "net_read_timeout", "net_write_timeout", "sql_require_primary_key", "wait_timeout", "max_allowed_packet", "max_heap_table_size", "sort_buffer_size", "tmp_table_size", "slow_query_log", "long_query_time", "binlog_retention_period", "innodb_change_buffer_max_size", "innodb_flush_neighbors", "innodb_read_io_threads", "innodb_write_io_threads", "innodb_thread_concurrency", "net_buffer_length", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *args: typing.Union[dict, frozendict.frozendict, ],
        backup_hour: typing.Union[MetaOapg.properties.backup_hour, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        backup_minute: typing.Union[MetaOapg.properties.backup_minute, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        sql_mode: typing.Union[MetaOapg.properties.sql_mode, str, schemas.Unset] = schemas.unset,
        connect_timeout: typing.Union[MetaOapg.properties.connect_timeout, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        default_time_zone: typing.Union[MetaOapg.properties.default_time_zone, str, schemas.Unset] = schemas.unset,
        group_concat_max_len: typing.Union[MetaOapg.properties.group_concat_max_len, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        information_schema_stats_expiry: typing.Union[MetaOapg.properties.information_schema_stats_expiry, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        innodb_ft_min_token_size: typing.Union[MetaOapg.properties.innodb_ft_min_token_size, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        innodb_ft_server_stopword_table: typing.Union[MetaOapg.properties.innodb_ft_server_stopword_table, str, schemas.Unset] = schemas.unset,
        innodb_lock_wait_timeout: typing.Union[MetaOapg.properties.innodb_lock_wait_timeout, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        innodb_log_buffer_size: typing.Union[MetaOapg.properties.innodb_log_buffer_size, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        innodb_online_alter_log_max_size: typing.Union[MetaOapg.properties.innodb_online_alter_log_max_size, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        innodb_print_all_deadlocks: typing.Union[MetaOapg.properties.innodb_print_all_deadlocks, bool, schemas.Unset] = schemas.unset,
        innodb_rollback_on_timeout: typing.Union[MetaOapg.properties.innodb_rollback_on_timeout, bool, schemas.Unset] = schemas.unset,
        interactive_timeout: typing.Union[MetaOapg.properties.interactive_timeout, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        internal_tmp_mem_storage_engine: typing.Union[MetaOapg.properties.internal_tmp_mem_storage_engine, str, schemas.Unset] = schemas.unset,
        net_read_timeout: typing.Union[MetaOapg.properties.net_read_timeout, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        net_write_timeout: typing.Union[MetaOapg.properties.net_write_timeout, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        sql_require_primary_key: typing.Union[MetaOapg.properties.sql_require_primary_key, bool, schemas.Unset] = schemas.unset,
        wait_timeout: typing.Union[MetaOapg.properties.wait_timeout, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        max_allowed_packet: typing.Union[MetaOapg.properties.max_allowed_packet, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        max_heap_table_size: typing.Union[MetaOapg.properties.max_heap_table_size, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        sort_buffer_size: typing.Union[MetaOapg.properties.sort_buffer_size, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        tmp_table_size: typing.Union[MetaOapg.properties.tmp_table_size, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        slow_query_log: typing.Union[MetaOapg.properties.slow_query_log, bool, schemas.Unset] = schemas.unset,
        long_query_time: typing.Union[MetaOapg.properties.long_query_time, decimal.Decimal, int, float, schemas.Unset] = schemas.unset,
        binlog_retention_period: typing.Union[MetaOapg.properties.binlog_retention_period, decimal.Decimal, int, float, schemas.Unset] = schemas.unset,
        innodb_change_buffer_max_size: typing.Union[MetaOapg.properties.innodb_change_buffer_max_size, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        innodb_flush_neighbors: typing.Union[MetaOapg.properties.innodb_flush_neighbors, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        innodb_read_io_threads: typing.Union[MetaOapg.properties.innodb_read_io_threads, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        innodb_write_io_threads: typing.Union[MetaOapg.properties.innodb_write_io_threads, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        innodb_thread_concurrency: typing.Union[MetaOapg.properties.innodb_thread_concurrency, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        net_buffer_length: typing.Union[MetaOapg.properties.net_buffer_length, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'Mysql':
        return super().__new__(
            cls,
            *args,
            backup_hour=backup_hour,
            backup_minute=backup_minute,
            sql_mode=sql_mode,
            connect_timeout=connect_timeout,
            default_time_zone=default_time_zone,
            group_concat_max_len=group_concat_max_len,
            information_schema_stats_expiry=information_schema_stats_expiry,
            innodb_ft_min_token_size=innodb_ft_min_token_size,
            innodb_ft_server_stopword_table=innodb_ft_server_stopword_table,
            innodb_lock_wait_timeout=innodb_lock_wait_timeout,
            innodb_log_buffer_size=innodb_log_buffer_size,
            innodb_online_alter_log_max_size=innodb_online_alter_log_max_size,
            innodb_print_all_deadlocks=innodb_print_all_deadlocks,
            innodb_rollback_on_timeout=innodb_rollback_on_timeout,
            interactive_timeout=interactive_timeout,
            internal_tmp_mem_storage_engine=internal_tmp_mem_storage_engine,
            net_read_timeout=net_read_timeout,
            net_write_timeout=net_write_timeout,
            sql_require_primary_key=sql_require_primary_key,
            wait_timeout=wait_timeout,
            max_allowed_packet=max_allowed_packet,
            max_heap_table_size=max_heap_table_size,
            sort_buffer_size=sort_buffer_size,
            tmp_table_size=tmp_table_size,
            slow_query_log=slow_query_log,
            long_query_time=long_query_time,
            binlog_retention_period=binlog_retention_period,
            innodb_change_buffer_max_size=innodb_change_buffer_max_size,
            innodb_flush_neighbors=innodb_flush_neighbors,
            innodb_read_io_threads=innodb_read_io_threads,
            innodb_write_io_threads=innodb_write_io_threads,
            innodb_thread_concurrency=innodb_thread_concurrency,
            net_buffer_length=net_buffer_length,
            _configuration=_configuration,
            **kwargs,
        )
