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


class Postgres(
    schemas.DictSchema
):
    """
    This class is auto generated by Konfig (https://konfigthis.com)
    """


    class MetaOapg:
        
        class properties:
            
            
            class autovacuum_freeze_max_age(
                schemas.IntSchema
            ):
                pass
            
            
            class autovacuum_max_workers(
                schemas.IntSchema
            ):
                pass
            
            
            class autovacuum_naptime(
                schemas.IntSchema
            ):
                pass
            
            
            class autovacuum_vacuum_threshold(
                schemas.IntSchema
            ):
                pass
            
            
            class autovacuum_analyze_threshold(
                schemas.IntSchema
            ):
                pass
            
            
            class autovacuum_vacuum_scale_factor(
                schemas.NumberSchema
            ):
                pass
            
            
            class autovacuum_analyze_scale_factor(
                schemas.NumberSchema
            ):
                pass
            
            
            class autovacuum_vacuum_cost_delay(
                schemas.IntSchema
            ):
                pass
            
            
            class autovacuum_vacuum_cost_limit(
                schemas.IntSchema
            ):
                pass
            
            
            class backup_hour(
                schemas.IntSchema
            ):
                pass
            
            
            class backup_minute(
                schemas.IntSchema
            ):
                pass
            
            
            class bgwriter_delay(
                schemas.IntSchema
            ):
                pass
            
            
            class bgwriter_flush_after(
                schemas.IntSchema
            ):
                pass
            
            
            class bgwriter_lru_maxpages(
                schemas.IntSchema
            ):
                pass
            
            
            class bgwriter_lru_multiplier(
                schemas.NumberSchema
            ):
                pass
            
            
            class deadlock_timeout(
                schemas.IntSchema
            ):
                pass
            
            
            class default_toast_compression(
                schemas.EnumBase,
                schemas.StrSchema
            ):
                
                @schemas.classproperty
                def LZ4(cls):
                    return cls("lz4")
                
                @schemas.classproperty
                def PGLZ(cls):
                    return cls("pglz")
            
            
            class idle_in_transaction_session_timeout(
                schemas.IntSchema
            ):
                pass
            jit = schemas.BoolSchema
            
            
            class log_autovacuum_min_duration(
                schemas.IntSchema
            ):
                pass
            
            
            class log_error_verbosity(
                schemas.EnumBase,
                schemas.StrSchema
            ):
                
                @schemas.classproperty
                def TERSE(cls):
                    return cls("TERSE")
                
                @schemas.classproperty
                def DEFAULT(cls):
                    return cls("DEFAULT")
                
                @schemas.classproperty
                def VERBOSE(cls):
                    return cls("VERBOSE")
            
            
            class log_line_prefix(
                schemas.EnumBase,
                schemas.StrSchema
            ):
                
                @schemas.classproperty
                def PIDPUSERUDBDAPPACLIENTH(cls):
                    return cls("pid=%p,user=%u,db=%d,app=%a,client=%h")
                
                @schemas.classproperty
                def M_P_QUSERUDBDAPPA(cls):
                    return cls("%m [%p] %q[user=%u,db=%d,app=%a]")
                
                @schemas.classproperty
                def T_P_L1_USERUDBDAPPACLIENTH(cls):
                    return cls("%t [%p]: [%l-1] user=%u,db=%d,app=%a,client=%h")
            
            
            class log_min_duration_statement(
                schemas.IntSchema
            ):
                pass
            
            
            class max_files_per_process(
                schemas.IntSchema
            ):
                pass
            
            
            class max_prepared_transactions(
                schemas.IntSchema
            ):
                pass
            
            
            class max_pred_locks_per_transaction(
                schemas.IntSchema
            ):
                pass
            
            
            class max_locks_per_transaction(
                schemas.IntSchema
            ):
                pass
            
            
            class max_stack_depth(
                schemas.IntSchema
            ):
                pass
            
            
            class max_standby_archive_delay(
                schemas.IntSchema
            ):
                pass
            
            
            class max_standby_streaming_delay(
                schemas.IntSchema
            ):
                pass
            
            
            class max_replication_slots(
                schemas.IntSchema
            ):
                pass
            
            
            class max_logical_replication_workers(
                schemas.IntSchema
            ):
                pass
            
            
            class max_parallel_workers(
                schemas.IntSchema
            ):
                pass
            
            
            class max_parallel_workers_per_gather(
                schemas.IntSchema
            ):
                pass
            
            
            class max_worker_processes(
                schemas.IntSchema
            ):
                pass
            
            
            class pg_partman_bgw_role(
                schemas.StrSchema
            ):
                pass
            
            
            class pg_partman_bgw_interval(
                schemas.IntSchema
            ):
                pass
            
            
            class pg_stat_statements_track(
                schemas.EnumBase,
                schemas.StrSchema
            ):
                
                @schemas.classproperty
                def ALL(cls):
                    return cls("all")
                
                @schemas.classproperty
                def TOP(cls):
                    return cls("top")
                
                @schemas.classproperty
                def NONE(cls):
                    return cls("none")
            
            
            class temp_file_limit(
                schemas.IntSchema
            ):
                pass
            
            
            class timezone(
                schemas.StrSchema
            ):
                pass
            
            
            class track_activity_query_size(
                schemas.IntSchema
            ):
                pass
            
            
            class track_commit_timestamp(
                schemas.EnumBase,
                schemas.StrSchema
            ):
                
                @schemas.classproperty
                def FALSE(cls):
                    return cls("false")
                
                @schemas.classproperty
                def TRUE(cls):
                    return cls("true")
            
            
            class track_functions(
                schemas.EnumBase,
                schemas.StrSchema
            ):
                
                @schemas.classproperty
                def ALL(cls):
                    return cls("all")
                
                @schemas.classproperty
                def PL(cls):
                    return cls("pl")
                
                @schemas.classproperty
                def NONE(cls):
                    return cls("none")
            
            
            class track_io_timing(
                schemas.EnumBase,
                schemas.StrSchema
            ):
                
                @schemas.classproperty
                def FALSE(cls):
                    return cls("false")
                
                @schemas.classproperty
                def TRUE(cls):
                    return cls("true")
            
            
            class max_wal_senders(
                schemas.IntSchema
            ):
                pass
            
            
            class wal_sender_timeout(
                schemas.IntSchema
            ):
                pass
            
            
            class wal_writer_delay(
                schemas.IntSchema
            ):
                pass
            
            
            class shared_buffers_percentage(
                schemas.NumberSchema
            ):
                pass
        
            @staticmethod
            def pgbouncer() -> typing.Type['Pgbouncer']:
                return Pgbouncer
            
            
            class work_mem(
                schemas.IntSchema
            ):
                pass
        
            @staticmethod
            def timescaledb() -> typing.Type['Timescaledb']:
                return Timescaledb
            
            
            class synchronous_replication(
                schemas.EnumBase,
                schemas.StrSchema
            ):
                
                @schemas.classproperty
                def FALSE(cls):
                    return cls("false")
                
                @schemas.classproperty
                def QUORUM(cls):
                    return cls("quorum")
            stat_monitor_enable = schemas.BoolSchema
            __annotations__ = {
                "autovacuum_freeze_max_age": autovacuum_freeze_max_age,
                "autovacuum_max_workers": autovacuum_max_workers,
                "autovacuum_naptime": autovacuum_naptime,
                "autovacuum_vacuum_threshold": autovacuum_vacuum_threshold,
                "autovacuum_analyze_threshold": autovacuum_analyze_threshold,
                "autovacuum_vacuum_scale_factor": autovacuum_vacuum_scale_factor,
                "autovacuum_analyze_scale_factor": autovacuum_analyze_scale_factor,
                "autovacuum_vacuum_cost_delay": autovacuum_vacuum_cost_delay,
                "autovacuum_vacuum_cost_limit": autovacuum_vacuum_cost_limit,
                "backup_hour": backup_hour,
                "backup_minute": backup_minute,
                "bgwriter_delay": bgwriter_delay,
                "bgwriter_flush_after": bgwriter_flush_after,
                "bgwriter_lru_maxpages": bgwriter_lru_maxpages,
                "bgwriter_lru_multiplier": bgwriter_lru_multiplier,
                "deadlock_timeout": deadlock_timeout,
                "default_toast_compression": default_toast_compression,
                "idle_in_transaction_session_timeout": idle_in_transaction_session_timeout,
                "jit": jit,
                "log_autovacuum_min_duration": log_autovacuum_min_duration,
                "log_error_verbosity": log_error_verbosity,
                "log_line_prefix": log_line_prefix,
                "log_min_duration_statement": log_min_duration_statement,
                "max_files_per_process": max_files_per_process,
                "max_prepared_transactions": max_prepared_transactions,
                "max_pred_locks_per_transaction": max_pred_locks_per_transaction,
                "max_locks_per_transaction": max_locks_per_transaction,
                "max_stack_depth": max_stack_depth,
                "max_standby_archive_delay": max_standby_archive_delay,
                "max_standby_streaming_delay": max_standby_streaming_delay,
                "max_replication_slots": max_replication_slots,
                "max_logical_replication_workers": max_logical_replication_workers,
                "max_parallel_workers": max_parallel_workers,
                "max_parallel_workers_per_gather": max_parallel_workers_per_gather,
                "max_worker_processes": max_worker_processes,
                "pg_partman_bgw.role": pg_partman_bgw_role,
                "pg_partman_bgw.interval": pg_partman_bgw_interval,
                "pg_stat_statements.track": pg_stat_statements_track,
                "temp_file_limit": temp_file_limit,
                "timezone": timezone,
                "track_activity_query_size": track_activity_query_size,
                "track_commit_timestamp": track_commit_timestamp,
                "track_functions": track_functions,
                "track_io_timing": track_io_timing,
                "max_wal_senders": max_wal_senders,
                "wal_sender_timeout": wal_sender_timeout,
                "wal_writer_delay": wal_writer_delay,
                "shared_buffers_percentage": shared_buffers_percentage,
                "pgbouncer": pgbouncer,
                "work_mem": work_mem,
                "timescaledb": timescaledb,
                "synchronous_replication": synchronous_replication,
                "stat_monitor_enable": stat_monitor_enable,
            }
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["autovacuum_freeze_max_age"]) -> MetaOapg.properties.autovacuum_freeze_max_age: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["autovacuum_max_workers"]) -> MetaOapg.properties.autovacuum_max_workers: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["autovacuum_naptime"]) -> MetaOapg.properties.autovacuum_naptime: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["autovacuum_vacuum_threshold"]) -> MetaOapg.properties.autovacuum_vacuum_threshold: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["autovacuum_analyze_threshold"]) -> MetaOapg.properties.autovacuum_analyze_threshold: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["autovacuum_vacuum_scale_factor"]) -> MetaOapg.properties.autovacuum_vacuum_scale_factor: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["autovacuum_analyze_scale_factor"]) -> MetaOapg.properties.autovacuum_analyze_scale_factor: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["autovacuum_vacuum_cost_delay"]) -> MetaOapg.properties.autovacuum_vacuum_cost_delay: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["autovacuum_vacuum_cost_limit"]) -> MetaOapg.properties.autovacuum_vacuum_cost_limit: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["backup_hour"]) -> MetaOapg.properties.backup_hour: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["backup_minute"]) -> MetaOapg.properties.backup_minute: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["bgwriter_delay"]) -> MetaOapg.properties.bgwriter_delay: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["bgwriter_flush_after"]) -> MetaOapg.properties.bgwriter_flush_after: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["bgwriter_lru_maxpages"]) -> MetaOapg.properties.bgwriter_lru_maxpages: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["bgwriter_lru_multiplier"]) -> MetaOapg.properties.bgwriter_lru_multiplier: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["deadlock_timeout"]) -> MetaOapg.properties.deadlock_timeout: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["default_toast_compression"]) -> MetaOapg.properties.default_toast_compression: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["idle_in_transaction_session_timeout"]) -> MetaOapg.properties.idle_in_transaction_session_timeout: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["jit"]) -> MetaOapg.properties.jit: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["log_autovacuum_min_duration"]) -> MetaOapg.properties.log_autovacuum_min_duration: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["log_error_verbosity"]) -> MetaOapg.properties.log_error_verbosity: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["log_line_prefix"]) -> MetaOapg.properties.log_line_prefix: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["log_min_duration_statement"]) -> MetaOapg.properties.log_min_duration_statement: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["max_files_per_process"]) -> MetaOapg.properties.max_files_per_process: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["max_prepared_transactions"]) -> MetaOapg.properties.max_prepared_transactions: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["max_pred_locks_per_transaction"]) -> MetaOapg.properties.max_pred_locks_per_transaction: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["max_locks_per_transaction"]) -> MetaOapg.properties.max_locks_per_transaction: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["max_stack_depth"]) -> MetaOapg.properties.max_stack_depth: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["max_standby_archive_delay"]) -> MetaOapg.properties.max_standby_archive_delay: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["max_standby_streaming_delay"]) -> MetaOapg.properties.max_standby_streaming_delay: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["max_replication_slots"]) -> MetaOapg.properties.max_replication_slots: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["max_logical_replication_workers"]) -> MetaOapg.properties.max_logical_replication_workers: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["max_parallel_workers"]) -> MetaOapg.properties.max_parallel_workers: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["max_parallel_workers_per_gather"]) -> MetaOapg.properties.max_parallel_workers_per_gather: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["max_worker_processes"]) -> MetaOapg.properties.max_worker_processes: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["pg_partman_bgw.role"]) -> MetaOapg.properties.pg_partman_bgw_role: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["pg_partman_bgw.interval"]) -> MetaOapg.properties.pg_partman_bgw_interval: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["pg_stat_statements.track"]) -> MetaOapg.properties.pg_stat_statements_track: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["temp_file_limit"]) -> MetaOapg.properties.temp_file_limit: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["timezone"]) -> MetaOapg.properties.timezone: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["track_activity_query_size"]) -> MetaOapg.properties.track_activity_query_size: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["track_commit_timestamp"]) -> MetaOapg.properties.track_commit_timestamp: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["track_functions"]) -> MetaOapg.properties.track_functions: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["track_io_timing"]) -> MetaOapg.properties.track_io_timing: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["max_wal_senders"]) -> MetaOapg.properties.max_wal_senders: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["wal_sender_timeout"]) -> MetaOapg.properties.wal_sender_timeout: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["wal_writer_delay"]) -> MetaOapg.properties.wal_writer_delay: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["shared_buffers_percentage"]) -> MetaOapg.properties.shared_buffers_percentage: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["pgbouncer"]) -> 'Pgbouncer': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["work_mem"]) -> MetaOapg.properties.work_mem: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["timescaledb"]) -> 'Timescaledb': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["synchronous_replication"]) -> MetaOapg.properties.synchronous_replication: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["stat_monitor_enable"]) -> MetaOapg.properties.stat_monitor_enable: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["autovacuum_freeze_max_age", "autovacuum_max_workers", "autovacuum_naptime", "autovacuum_vacuum_threshold", "autovacuum_analyze_threshold", "autovacuum_vacuum_scale_factor", "autovacuum_analyze_scale_factor", "autovacuum_vacuum_cost_delay", "autovacuum_vacuum_cost_limit", "backup_hour", "backup_minute", "bgwriter_delay", "bgwriter_flush_after", "bgwriter_lru_maxpages", "bgwriter_lru_multiplier", "deadlock_timeout", "default_toast_compression", "idle_in_transaction_session_timeout", "jit", "log_autovacuum_min_duration", "log_error_verbosity", "log_line_prefix", "log_min_duration_statement", "max_files_per_process", "max_prepared_transactions", "max_pred_locks_per_transaction", "max_locks_per_transaction", "max_stack_depth", "max_standby_archive_delay", "max_standby_streaming_delay", "max_replication_slots", "max_logical_replication_workers", "max_parallel_workers", "max_parallel_workers_per_gather", "max_worker_processes", "pg_partman_bgw.role", "pg_partman_bgw.interval", "pg_stat_statements.track", "temp_file_limit", "timezone", "track_activity_query_size", "track_commit_timestamp", "track_functions", "track_io_timing", "max_wal_senders", "wal_sender_timeout", "wal_writer_delay", "shared_buffers_percentage", "pgbouncer", "work_mem", "timescaledb", "synchronous_replication", "stat_monitor_enable", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["autovacuum_freeze_max_age"]) -> typing.Union[MetaOapg.properties.autovacuum_freeze_max_age, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["autovacuum_max_workers"]) -> typing.Union[MetaOapg.properties.autovacuum_max_workers, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["autovacuum_naptime"]) -> typing.Union[MetaOapg.properties.autovacuum_naptime, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["autovacuum_vacuum_threshold"]) -> typing.Union[MetaOapg.properties.autovacuum_vacuum_threshold, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["autovacuum_analyze_threshold"]) -> typing.Union[MetaOapg.properties.autovacuum_analyze_threshold, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["autovacuum_vacuum_scale_factor"]) -> typing.Union[MetaOapg.properties.autovacuum_vacuum_scale_factor, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["autovacuum_analyze_scale_factor"]) -> typing.Union[MetaOapg.properties.autovacuum_analyze_scale_factor, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["autovacuum_vacuum_cost_delay"]) -> typing.Union[MetaOapg.properties.autovacuum_vacuum_cost_delay, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["autovacuum_vacuum_cost_limit"]) -> typing.Union[MetaOapg.properties.autovacuum_vacuum_cost_limit, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["backup_hour"]) -> typing.Union[MetaOapg.properties.backup_hour, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["backup_minute"]) -> typing.Union[MetaOapg.properties.backup_minute, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["bgwriter_delay"]) -> typing.Union[MetaOapg.properties.bgwriter_delay, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["bgwriter_flush_after"]) -> typing.Union[MetaOapg.properties.bgwriter_flush_after, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["bgwriter_lru_maxpages"]) -> typing.Union[MetaOapg.properties.bgwriter_lru_maxpages, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["bgwriter_lru_multiplier"]) -> typing.Union[MetaOapg.properties.bgwriter_lru_multiplier, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["deadlock_timeout"]) -> typing.Union[MetaOapg.properties.deadlock_timeout, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["default_toast_compression"]) -> typing.Union[MetaOapg.properties.default_toast_compression, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["idle_in_transaction_session_timeout"]) -> typing.Union[MetaOapg.properties.idle_in_transaction_session_timeout, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["jit"]) -> typing.Union[MetaOapg.properties.jit, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["log_autovacuum_min_duration"]) -> typing.Union[MetaOapg.properties.log_autovacuum_min_duration, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["log_error_verbosity"]) -> typing.Union[MetaOapg.properties.log_error_verbosity, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["log_line_prefix"]) -> typing.Union[MetaOapg.properties.log_line_prefix, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["log_min_duration_statement"]) -> typing.Union[MetaOapg.properties.log_min_duration_statement, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["max_files_per_process"]) -> typing.Union[MetaOapg.properties.max_files_per_process, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["max_prepared_transactions"]) -> typing.Union[MetaOapg.properties.max_prepared_transactions, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["max_pred_locks_per_transaction"]) -> typing.Union[MetaOapg.properties.max_pred_locks_per_transaction, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["max_locks_per_transaction"]) -> typing.Union[MetaOapg.properties.max_locks_per_transaction, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["max_stack_depth"]) -> typing.Union[MetaOapg.properties.max_stack_depth, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["max_standby_archive_delay"]) -> typing.Union[MetaOapg.properties.max_standby_archive_delay, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["max_standby_streaming_delay"]) -> typing.Union[MetaOapg.properties.max_standby_streaming_delay, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["max_replication_slots"]) -> typing.Union[MetaOapg.properties.max_replication_slots, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["max_logical_replication_workers"]) -> typing.Union[MetaOapg.properties.max_logical_replication_workers, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["max_parallel_workers"]) -> typing.Union[MetaOapg.properties.max_parallel_workers, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["max_parallel_workers_per_gather"]) -> typing.Union[MetaOapg.properties.max_parallel_workers_per_gather, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["max_worker_processes"]) -> typing.Union[MetaOapg.properties.max_worker_processes, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["pg_partman_bgw.role"]) -> typing.Union[MetaOapg.properties.pg_partman_bgw_role, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["pg_partman_bgw.interval"]) -> typing.Union[MetaOapg.properties.pg_partman_bgw_interval, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["pg_stat_statements.track"]) -> typing.Union[MetaOapg.properties.pg_stat_statements_track, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["temp_file_limit"]) -> typing.Union[MetaOapg.properties.temp_file_limit, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["timezone"]) -> typing.Union[MetaOapg.properties.timezone, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["track_activity_query_size"]) -> typing.Union[MetaOapg.properties.track_activity_query_size, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["track_commit_timestamp"]) -> typing.Union[MetaOapg.properties.track_commit_timestamp, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["track_functions"]) -> typing.Union[MetaOapg.properties.track_functions, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["track_io_timing"]) -> typing.Union[MetaOapg.properties.track_io_timing, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["max_wal_senders"]) -> typing.Union[MetaOapg.properties.max_wal_senders, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["wal_sender_timeout"]) -> typing.Union[MetaOapg.properties.wal_sender_timeout, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["wal_writer_delay"]) -> typing.Union[MetaOapg.properties.wal_writer_delay, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["shared_buffers_percentage"]) -> typing.Union[MetaOapg.properties.shared_buffers_percentage, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["pgbouncer"]) -> typing.Union['Pgbouncer', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["work_mem"]) -> typing.Union[MetaOapg.properties.work_mem, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["timescaledb"]) -> typing.Union['Timescaledb', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["synchronous_replication"]) -> typing.Union[MetaOapg.properties.synchronous_replication, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["stat_monitor_enable"]) -> typing.Union[MetaOapg.properties.stat_monitor_enable, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["autovacuum_freeze_max_age", "autovacuum_max_workers", "autovacuum_naptime", "autovacuum_vacuum_threshold", "autovacuum_analyze_threshold", "autovacuum_vacuum_scale_factor", "autovacuum_analyze_scale_factor", "autovacuum_vacuum_cost_delay", "autovacuum_vacuum_cost_limit", "backup_hour", "backup_minute", "bgwriter_delay", "bgwriter_flush_after", "bgwriter_lru_maxpages", "bgwriter_lru_multiplier", "deadlock_timeout", "default_toast_compression", "idle_in_transaction_session_timeout", "jit", "log_autovacuum_min_duration", "log_error_verbosity", "log_line_prefix", "log_min_duration_statement", "max_files_per_process", "max_prepared_transactions", "max_pred_locks_per_transaction", "max_locks_per_transaction", "max_stack_depth", "max_standby_archive_delay", "max_standby_streaming_delay", "max_replication_slots", "max_logical_replication_workers", "max_parallel_workers", "max_parallel_workers_per_gather", "max_worker_processes", "pg_partman_bgw.role", "pg_partman_bgw.interval", "pg_stat_statements.track", "temp_file_limit", "timezone", "track_activity_query_size", "track_commit_timestamp", "track_functions", "track_io_timing", "max_wal_senders", "wal_sender_timeout", "wal_writer_delay", "shared_buffers_percentage", "pgbouncer", "work_mem", "timescaledb", "synchronous_replication", "stat_monitor_enable", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *args: typing.Union[dict, frozendict.frozendict, ],
        autovacuum_freeze_max_age: typing.Union[MetaOapg.properties.autovacuum_freeze_max_age, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        autovacuum_max_workers: typing.Union[MetaOapg.properties.autovacuum_max_workers, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        autovacuum_naptime: typing.Union[MetaOapg.properties.autovacuum_naptime, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        autovacuum_vacuum_threshold: typing.Union[MetaOapg.properties.autovacuum_vacuum_threshold, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        autovacuum_analyze_threshold: typing.Union[MetaOapg.properties.autovacuum_analyze_threshold, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        autovacuum_vacuum_scale_factor: typing.Union[MetaOapg.properties.autovacuum_vacuum_scale_factor, decimal.Decimal, int, float, schemas.Unset] = schemas.unset,
        autovacuum_analyze_scale_factor: typing.Union[MetaOapg.properties.autovacuum_analyze_scale_factor, decimal.Decimal, int, float, schemas.Unset] = schemas.unset,
        autovacuum_vacuum_cost_delay: typing.Union[MetaOapg.properties.autovacuum_vacuum_cost_delay, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        autovacuum_vacuum_cost_limit: typing.Union[MetaOapg.properties.autovacuum_vacuum_cost_limit, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        backup_hour: typing.Union[MetaOapg.properties.backup_hour, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        backup_minute: typing.Union[MetaOapg.properties.backup_minute, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        bgwriter_delay: typing.Union[MetaOapg.properties.bgwriter_delay, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        bgwriter_flush_after: typing.Union[MetaOapg.properties.bgwriter_flush_after, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        bgwriter_lru_maxpages: typing.Union[MetaOapg.properties.bgwriter_lru_maxpages, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        bgwriter_lru_multiplier: typing.Union[MetaOapg.properties.bgwriter_lru_multiplier, decimal.Decimal, int, float, schemas.Unset] = schemas.unset,
        deadlock_timeout: typing.Union[MetaOapg.properties.deadlock_timeout, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        default_toast_compression: typing.Union[MetaOapg.properties.default_toast_compression, str, schemas.Unset] = schemas.unset,
        idle_in_transaction_session_timeout: typing.Union[MetaOapg.properties.idle_in_transaction_session_timeout, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        jit: typing.Union[MetaOapg.properties.jit, bool, schemas.Unset] = schemas.unset,
        log_autovacuum_min_duration: typing.Union[MetaOapg.properties.log_autovacuum_min_duration, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        log_error_verbosity: typing.Union[MetaOapg.properties.log_error_verbosity, str, schemas.Unset] = schemas.unset,
        log_line_prefix: typing.Union[MetaOapg.properties.log_line_prefix, str, schemas.Unset] = schemas.unset,
        log_min_duration_statement: typing.Union[MetaOapg.properties.log_min_duration_statement, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        max_files_per_process: typing.Union[MetaOapg.properties.max_files_per_process, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        max_prepared_transactions: typing.Union[MetaOapg.properties.max_prepared_transactions, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        max_pred_locks_per_transaction: typing.Union[MetaOapg.properties.max_pred_locks_per_transaction, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        max_locks_per_transaction: typing.Union[MetaOapg.properties.max_locks_per_transaction, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        max_stack_depth: typing.Union[MetaOapg.properties.max_stack_depth, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        max_standby_archive_delay: typing.Union[MetaOapg.properties.max_standby_archive_delay, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        max_standby_streaming_delay: typing.Union[MetaOapg.properties.max_standby_streaming_delay, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        max_replication_slots: typing.Union[MetaOapg.properties.max_replication_slots, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        max_logical_replication_workers: typing.Union[MetaOapg.properties.max_logical_replication_workers, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        max_parallel_workers: typing.Union[MetaOapg.properties.max_parallel_workers, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        max_parallel_workers_per_gather: typing.Union[MetaOapg.properties.max_parallel_workers_per_gather, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        max_worker_processes: typing.Union[MetaOapg.properties.max_worker_processes, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        temp_file_limit: typing.Union[MetaOapg.properties.temp_file_limit, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        timezone: typing.Union[MetaOapg.properties.timezone, str, schemas.Unset] = schemas.unset,
        track_activity_query_size: typing.Union[MetaOapg.properties.track_activity_query_size, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        track_commit_timestamp: typing.Union[MetaOapg.properties.track_commit_timestamp, str, schemas.Unset] = schemas.unset,
        track_functions: typing.Union[MetaOapg.properties.track_functions, str, schemas.Unset] = schemas.unset,
        track_io_timing: typing.Union[MetaOapg.properties.track_io_timing, str, schemas.Unset] = schemas.unset,
        max_wal_senders: typing.Union[MetaOapg.properties.max_wal_senders, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        wal_sender_timeout: typing.Union[MetaOapg.properties.wal_sender_timeout, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        wal_writer_delay: typing.Union[MetaOapg.properties.wal_writer_delay, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        shared_buffers_percentage: typing.Union[MetaOapg.properties.shared_buffers_percentage, decimal.Decimal, int, float, schemas.Unset] = schemas.unset,
        pgbouncer: typing.Union['Pgbouncer', schemas.Unset] = schemas.unset,
        work_mem: typing.Union[MetaOapg.properties.work_mem, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        timescaledb: typing.Union['Timescaledb', schemas.Unset] = schemas.unset,
        synchronous_replication: typing.Union[MetaOapg.properties.synchronous_replication, str, schemas.Unset] = schemas.unset,
        stat_monitor_enable: typing.Union[MetaOapg.properties.stat_monitor_enable, bool, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'Postgres':
        return super().__new__(
            cls,
            *args,
            autovacuum_freeze_max_age=autovacuum_freeze_max_age,
            autovacuum_max_workers=autovacuum_max_workers,
            autovacuum_naptime=autovacuum_naptime,
            autovacuum_vacuum_threshold=autovacuum_vacuum_threshold,
            autovacuum_analyze_threshold=autovacuum_analyze_threshold,
            autovacuum_vacuum_scale_factor=autovacuum_vacuum_scale_factor,
            autovacuum_analyze_scale_factor=autovacuum_analyze_scale_factor,
            autovacuum_vacuum_cost_delay=autovacuum_vacuum_cost_delay,
            autovacuum_vacuum_cost_limit=autovacuum_vacuum_cost_limit,
            backup_hour=backup_hour,
            backup_minute=backup_minute,
            bgwriter_delay=bgwriter_delay,
            bgwriter_flush_after=bgwriter_flush_after,
            bgwriter_lru_maxpages=bgwriter_lru_maxpages,
            bgwriter_lru_multiplier=bgwriter_lru_multiplier,
            deadlock_timeout=deadlock_timeout,
            default_toast_compression=default_toast_compression,
            idle_in_transaction_session_timeout=idle_in_transaction_session_timeout,
            jit=jit,
            log_autovacuum_min_duration=log_autovacuum_min_duration,
            log_error_verbosity=log_error_verbosity,
            log_line_prefix=log_line_prefix,
            log_min_duration_statement=log_min_duration_statement,
            max_files_per_process=max_files_per_process,
            max_prepared_transactions=max_prepared_transactions,
            max_pred_locks_per_transaction=max_pred_locks_per_transaction,
            max_locks_per_transaction=max_locks_per_transaction,
            max_stack_depth=max_stack_depth,
            max_standby_archive_delay=max_standby_archive_delay,
            max_standby_streaming_delay=max_standby_streaming_delay,
            max_replication_slots=max_replication_slots,
            max_logical_replication_workers=max_logical_replication_workers,
            max_parallel_workers=max_parallel_workers,
            max_parallel_workers_per_gather=max_parallel_workers_per_gather,
            max_worker_processes=max_worker_processes,
            temp_file_limit=temp_file_limit,
            timezone=timezone,
            track_activity_query_size=track_activity_query_size,
            track_commit_timestamp=track_commit_timestamp,
            track_functions=track_functions,
            track_io_timing=track_io_timing,
            max_wal_senders=max_wal_senders,
            wal_sender_timeout=wal_sender_timeout,
            wal_writer_delay=wal_writer_delay,
            shared_buffers_percentage=shared_buffers_percentage,
            pgbouncer=pgbouncer,
            work_mem=work_mem,
            timescaledb=timescaledb,
            synchronous_replication=synchronous_replication,
            stat_monitor_enable=stat_monitor_enable,
            _configuration=_configuration,
            **kwargs,
        )

from digital_ocean_python_sdk.model.pgbouncer import Pgbouncer
from digital_ocean_python_sdk.model.timescaledb import Timescaledb
