# coding: utf-8

"""
    DigitalOcean API

    # Introduction  The DigitalOcean API allows you to manage Droplets and resources within the DigitalOcean cloud in a simple, programmatic way using conventional HTTP requests.  All of the functionality that you are familiar with in the DigitalOcean control panel is also available through the API, allowing you to script the complex actions that your situation requires.  The API documentation will start with a general overview about the design and technology that has been implemented, followed by reference information about specific endpoints.  ## Requests  Any tool that is fluent in HTTP can communicate with the API simply by requesting the correct URI. Requests should be made using the HTTPS protocol so that traffic is encrypted. The interface responds to different methods depending on the action required.  |Method|Usage| |--- |--- | |GET|For simple retrieval of information about your account, Droplets, or environment, you should use the GET method.  The information you request will be returned to you as a JSON object. The attributes defined by the JSON object can be used to form additional requests.  Any request using the GET method is read-only and will not affect any of the objects you are querying.| |DELETE|To destroy a resource and remove it from your account and environment, the DELETE method should be used.  This will remove the specified object if it is found.  If it is not found, the operation will return a response indicating that the object was not found. This idempotency means that you do not have to check for a resource's availability prior to issuing a delete command, the final state will be the same regardless of its existence.| |PUT|To update the information about a resource in your account, the PUT method is available. Like the DELETE Method, the PUT method is idempotent.  It sets the state of the target using the provided values, regardless of their current values. Requests using the PUT method do not need to check the current attributes of the object.| |PATCH|Some resources support partial modification. In these cases, the PATCH method is available. Unlike PUT which generally requires a complete representation of a resource, a PATCH request is is a set of instructions on how to modify a resource updating only specific attributes.| |POST|To create a new object, your request should specify the POST method. The POST request includes all of the attributes necessary to create a new object.  When you wish to create a new object, send a POST request to the target endpoint.| |HEAD|Finally, to retrieve metadata information, you should use the HEAD method to get the headers.  This returns only the header of what would be returned with an associated GET request. Response headers contain some useful information about your API access and the results that are available for your request. For instance, the headers contain your current rate-limit value and the amount of time available until the limit resets. It also contains metrics about the total number of objects found, pagination information, and the total content length.|   ## HTTP Statuses  Along with the HTTP methods that the API responds to, it will also return standard HTTP statuses, including error codes.  In the event of a problem, the status will contain the error code, while the body of the response will usually contain additional information about the problem that was encountered.  In general, if the status returned is in the 200 range, it indicates that the request was fulfilled successfully and that no error was encountered.  Return codes in the 400 range typically indicate that there was an issue with the request that was sent. Among other things, this could mean that you did not authenticate correctly, that you are requesting an action that you do not have authorization for, that the object you are requesting does not exist, or that your request is malformed.  If you receive a status in the 500 range, this generally indicates a server-side problem. This means that we are having an issue on our end and cannot fulfill your request currently.  400 and 500 level error responses will include a JSON object in their body, including the following attributes:  |Name|Type|Description| |--- |--- |--- | |id|string|A short identifier corresponding to the HTTP status code returned. For example, the ID for a response returning a 404 status code would be \"not_found.\"| |message|string|A message providing additional information about the error, including details to help resolve it when possible.| |request_id|string|Optionally, some endpoints may include a request ID that should be provided when reporting bugs or opening support tickets to help identify the issue.|  ### Example Error Response  ```     HTTP/1.1 403 Forbidden     {       \"id\":       \"forbidden\",       \"message\":  \"You do not have access for the attempted action.\"     } ```  ## Responses  When a request is successful, a response body will typically be sent back in the form of a JSON object. An exception to this is when a DELETE request is processed, which will result in a successful HTTP 204 status and an empty response body.  Inside of this JSON object, the resource root that was the target of the request will be set as the key. This will be the singular form of the word if the request operated on a single object, and the plural form of the word if a collection was processed.  For example, if you send a GET request to `/v2/droplets/$DROPLET_ID` you will get back an object with a key called \"`droplet`\". However, if you send the GET request to the general collection at `/v2/droplets`, you will get back an object with a key called \"`droplets`\".  The value of these keys will generally be a JSON object for a request on a single object and an array of objects for a request on a collection of objects.  ### Response for a Single Object  ```     {         \"droplet\": {             \"name\": \"example.com\"             . . .         }     } ```  ### Response for an Object Collection  ```     {         \"droplets\": [             {                 \"name\": \"example.com\"                 . . .             },             {                 \"name\": \"second.com\"                 . . .             }         ]     } ```  ## Meta  In addition to the main resource root, the response may also contain a `meta` object. This object contains information about the response itself.  The `meta` object contains a `total` key that is set to the total number of objects returned by the request. This has implications on the `links` object and pagination.  The `meta` object will only be displayed when it has a value. Currently, the `meta` object will have a value when a request is made on a collection (like `droplets` or `domains`).   ### Sample Meta Object  ```     {         . . .         \"meta\": {             \"total\": 43         }         . . .     } ```  ## Links & Pagination  The `links` object is returned as part of the response body when pagination is enabled. By default, 20 objects are returned per page. If the response contains 20 objects or fewer, no `links` object will be returned. If the response contains more than 20 objects, the first 20 will be returned along with the `links` object.  You can request a different pagination limit or force pagination by appending `?per_page=` to the request with the number of items you would like per page. For instance, to show only two results per page, you could add `?per_page=2` to the end of your query. The maximum number of results per page is 200.  The `links` object contains a `pages` object. The `pages` object, in turn, contains keys indicating the relationship of additional pages. The values of these are the URLs of the associated pages. The keys will be one of the following:  *   **first**: The URI of the first page of results. *   **prev**: The URI of the previous sequential page of results. *   **next**: The URI of the next sequential page of results. *   **last**: The URI of the last page of results.  The `pages` object will only include the links that make sense. So for the first page of results, no `first` or `prev` links will ever be set. This convention holds true in other situations where a link would not make sense.  ### Sample Links Object  ```     {         . . .         \"links\": {             \"pages\": {                 \"last\": \"https://api.digitalocean.com/v2/images?page=2\",                 \"next\": \"https://api.digitalocean.com/v2/images?page=2\"             }         }         . . .     } ```  ## Rate Limit  Requests through the API are rate limited per OAuth token. Current rate limits:  *   5,000 requests per hour *   250 requests per minute (5% of the hourly total)  Once you exceed either limit, you will be rate limited until the next cycle starts. Space out any requests that you would otherwise issue in bursts for the best results.  The rate limiting information is contained within the response headers of each request. The relevant headers are:  *   **ratelimit-limit**: The number of requests that can be made per hour. *   **ratelimit-remaining**: The number of requests that remain before you hit your request limit. See the information below for how the request limits expire. *   **ratelimit-reset**: This represents the time when the oldest request will expire. The value is given in [Unix epoch time](http://en.wikipedia.org/wiki/Unix_time). See below for more information about how request limits expire.  More rate limiting information is returned only within burst limit error response headers: *   **retry-after**: The number of seconds to wait before making another request when rate limited.  As long as the `ratelimit-remaining` count is above zero, you will be able to make additional requests.  The way that a request expires and is removed from the current limit count is important to understand. Rather than counting all of the requests for an hour and resetting the `ratelimit-remaining` value at the end of the hour, each request instead has its own timer.  This means that each request contributes toward the `ratelimit-remaining` count for one complete hour after the request is made. When that request's timer runs out, it is no longer counted towards the request limit.  This has implications on the meaning of the `ratelimit-reset` header as well. Because the entire rate limit is not reset at one time, the value of this header is set to the time when the _oldest_ request will expire.  Keep this in mind if you see your `ratelimit-reset` value change, but not move an entire hour into the future.  If the `ratelimit-remaining` reaches zero, subsequent requests will receive a 429 error code until the request reset has been reached.   `ratelimit-remaining` reaching zero can also indicate that the \"burst limit\" of 250  requests per minute limit was met, even if the 5,000 requests per hour limit was not.  In this case, the 429 error response will include a retry-after header to indicate how  long to wait (in seconds) until the request may be retried.  You can see the format of the response in the examples.   **Note:** The following endpoints have special rate limit requirements that are independent of the limits defined above.  *   Only 12 `POST` requests to the `/v2/floating_ips` endpoint to create Floating IPs can be made per 60 seconds. *   Only 10 `GET` requests to the `/v2/account/keys` endpoint to list SSH keys can be made per 60 seconds. *   Only 5 requests to any and all `v2/cdn/endpoints` can be made per 10 seconds. This includes `v2/cdn/endpoints`,      `v2/cdn/endpoints/$ENDPOINT_ID`, and `v2/cdn/endpoints/$ENDPOINT_ID/cache`. *   Only 50 strings within the `files` json struct in the `v2/cdn/endpoints/$ENDPOINT_ID/cache` [payload](https://docs.digitalocean.com/reference/api/api-reference/#operation/cdn_purge_cache)      can be requested every 20 seconds.  ### Sample Rate Limit Headers  ```     . . .     ratelimit-limit: 1200     ratelimit-remaining: 1193     rateLimit-reset: 1402425459     . . . ```    ### Sample Rate Limit Headers When Burst Limit is Reached:  ```     . . .     ratelimit-limit: 5000     ratelimit-remaining: 0     rateLimit-reset: 1402425459     retry-after: 29     . . . ```  ### Sample Rate Exceeded Response  ```     429 Too Many Requests     {             id: \"too_many_requests\",             message: \"API Rate limit exceeded.\"     } ```  ## Curl Examples  Throughout this document, some example API requests will be given using the `curl` command. This will allow us to demonstrate the various endpoints in a simple, textual format.      These examples assume that you are using a Linux or macOS command line. To run these commands on a Windows machine, you can either use cmd.exe, PowerShell, or WSL:  * For cmd.exe, use the `set VAR=VALUE` [syntax](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/set_1) to define environment variables, call them with `%VAR%`, then replace all backslashes (`\\`) in the examples with carets (`^`).  * For PowerShell, use the `$Env:VAR = \"VALUE\"` [syntax](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_environment_variables?view=powershell-7.2) to define environment variables, call them with `$Env:VAR`, then replace `curl` with `curl.exe` and all backslashes (`\\`) in the examples with backticks (`` ` ``).  * WSL is a compatibility layer that allows you to emulate a Linux terminal on a Windows machine. Install WSL with our [community tutorial](https://www.digitalocean.com/community/tutorials/how-to-install-the-windows-subsystem-for-linux-2-on-microsoft-windows-10),  then follow this API documentation normally.  The names of account-specific references (like Droplet IDs, for instance) will be represented by variables. For instance, a Droplet ID may be represented by a variable called `$DROPLET_ID`. You can set the associated variables in your environment if you wish to use the examples without modification.  The first variable that you should set to get started is your OAuth authorization token. The next section will go over the details of this, but you can set an environmental variable for it now.  Generate a token by going to the [Apps & API](https://cloud.digitalocean.com/settings/applications) section of the DigitalOcean control panel. Use an existing token if you have saved one, or generate a new token with the \"Generate new token\" button. Copy the generated token and use it to set and export the TOKEN variable in your environment as the example shows.  You may also wish to set some other variables now or as you go along. For example, you may wish to set the `DROPLET_ID` variable to one of your Droplet IDs since this will be used frequently in the API.  If you are following along, make sure you use a Droplet ID that you control so that your commands will execute correctly.  If you need access to the headers of a response through `curl`, you can pass the `-i` flag to display the header information along with the body. If you are only interested in the header, you can instead pass the `-I` flag, which will exclude the response body entirely.   ### Set and Export your OAuth Token  ``` export DIGITALOCEAN_TOKEN=your_token_here ```  ### Set and Export a Variable  ``` export DROPLET_ID=1111111 ```  ## Parameters  There are two different ways to pass parameters in a request with the API.  When passing parameters to create or update an object, parameters should be passed as a JSON object containing the appropriate attribute names and values as key-value pairs. When you use this format, you should specify that you are sending a JSON object in the header. This is done by setting the `Content-Type` header to `application/json`. This ensures that your request is interpreted correctly.  When passing parameters to filter a response on GET requests, parameters can be passed using standard query attributes. In this case, the parameters would be embedded into the URI itself by appending a `?` to the end of the URI and then setting each attribute with an equal sign. Attributes can be separated with a `&`. Tools like `curl` can create the appropriate URI when given parameters and values; this can also be done using the `-F` flag and then passing the key and value as an argument. The argument should take the form of a quoted string with the attribute being set to a value with an equal sign.  ### Pass Parameters as a JSON Object  ```     curl -H \"Authorization: Bearer $DIGITALOCEAN_TOKEN\" \\         -H \"Content-Type: application/json\" \\         -d '{\"name\": \"example.com\", \"ip_address\": \"127.0.0.1\"}' \\         -X POST \"https://api.digitalocean.com/v2/domains\" ```  ### Pass Filter Parameters as a Query String  ```      curl -H \"Authorization: Bearer $DIGITALOCEAN_TOKEN\" \\          -X GET \\          \"https://api.digitalocean.com/v2/images?private=true\" ```  ## Cross Origin Resource Sharing  In order to make requests to the API from other domains, the API implements Cross Origin Resource Sharing (CORS) support.  CORS support is generally used to create AJAX requests outside of the domain that the request originated from. This is necessary to implement projects like control panels utilizing the API. This tells the browser that it can send requests to an outside domain.  The procedure that the browser initiates in order to perform these actions (other than GET requests) begins by sending a \"preflight\" request. This sets the `Origin` header and uses the `OPTIONS` method. The server will reply back with the methods it allows and some of the limits it imposes. The client then sends the actual request if it falls within the allowed constraints.  This process is usually done in the background by the browser, but you can use curl to emulate this process using the example provided. The headers that will be set to show the constraints are:  *   **Access-Control-Allow-Origin**: This is the domain that is sent by the client or browser as the origin of the request. It is set through an `Origin` header. *   **Access-Control-Allow-Methods**: This specifies the allowed options for requests from that domain. This will generally be all available methods. *   **Access-Control-Expose-Headers**: This will contain the headers that will be available to requests from the origin domain. *   **Access-Control-Max-Age**: This is the length of time that the access is considered valid. After this expires, a new preflight should be sent. *   **Access-Control-Allow-Credentials**: This will be set to `true`. It basically allows you to send your OAuth token for authentication.  You should not need to be concerned with the details of these headers, because the browser will typically do all of the work for you. 

    The version of the OpenAPI document: 2.0
    Contact: api-engineering@digitalocean.com
    Generated by: https://konfigthis.com
"""

from datetime import datetime, date
import typing
from enum import Enum
from typing_extensions import TypedDict, Literal, TYPE_CHECKING
from pydantic import BaseModel, Field, RootModel

from digital_ocean_python_sdk.pydantic.pgbouncer import Pgbouncer
from digital_ocean_python_sdk.pydantic.timescaledb import Timescaledb

class Postgres(BaseModel):
    # Specifies the maximum age (in transactions) that a table's pg_class.relfrozenxid field can attain before a VACUUM operation is forced to prevent transaction ID wraparound within the table. Note that the system will launch autovacuum processes to prevent wraparound even when autovacuum is otherwise disabled. This parameter will cause the server to be restarted.
    autovacuum_freeze_max_age: typing.Optional[int] = Field(None, alias='autovacuum_freeze_max_age')

    # Specifies the maximum number of autovacuum processes (other than the autovacuum launcher) that may be running at any one time. The default is three. This parameter can only be set at server start.
    autovacuum_max_workers: typing.Optional[int] = Field(None, alias='autovacuum_max_workers')

    # Specifies the minimum delay, in seconds, between autovacuum runs on any given database. The default is one minute.
    autovacuum_naptime: typing.Optional[int] = Field(None, alias='autovacuum_naptime')

    # Specifies the minimum number of updated or deleted tuples needed to trigger a VACUUM in any one table. The default is 50 tuples.
    autovacuum_vacuum_threshold: typing.Optional[int] = Field(None, alias='autovacuum_vacuum_threshold')

    # Specifies the minimum number of inserted, updated, or deleted tuples needed to trigger an ANALYZE in any one table. The default is 50 tuples.
    autovacuum_analyze_threshold: typing.Optional[int] = Field(None, alias='autovacuum_analyze_threshold')

    # Specifies a fraction, in a decimal value, of the table size to add to autovacuum_vacuum_threshold when deciding whether to trigger a VACUUM. The default is 0.2 (20% of table size).
    autovacuum_vacuum_scale_factor: typing.Optional[typing.Union[int, float]] = Field(None, alias='autovacuum_vacuum_scale_factor')

    # Specifies a fraction, in a decimal value, of the table size to add to autovacuum_analyze_threshold when deciding whether to trigger an ANALYZE. The default is 0.2 (20% of table size).
    autovacuum_analyze_scale_factor: typing.Optional[typing.Union[int, float]] = Field(None, alias='autovacuum_analyze_scale_factor')

    # Specifies the cost delay value, in milliseconds, that will be used in automatic VACUUM operations. If -1, uses the regular vacuum_cost_delay value, which is 20 milliseconds.
    autovacuum_vacuum_cost_delay: typing.Optional[int] = Field(None, alias='autovacuum_vacuum_cost_delay')

    # Specifies the cost limit value that will be used in automatic VACUUM operations. If -1 is specified (which is the default), the regular vacuum_cost_limit value will be used.
    autovacuum_vacuum_cost_limit: typing.Optional[int] = Field(None, alias='autovacuum_vacuum_cost_limit')

    # The hour of day (in UTC) when backup for the service starts. New backup only starts if previous backup has already completed.
    backup_hour: typing.Optional[int] = Field(None, alias='backup_hour')

    # The minute of the backup hour when backup for the service starts. New backup is only started if previous backup has already completed.
    backup_minute: typing.Optional[int] = Field(None, alias='backup_minute')

    # Specifies the delay, in milliseconds, between activity rounds for the background writer. Default is 200 ms.
    bgwriter_delay: typing.Optional[int] = Field(None, alias='bgwriter_delay')

    # The amount of kilobytes that need to be written by the background writer before attempting to force the OS to issue these writes to underlying storage. Specified in kilobytes, default is 512.  Setting of 0 disables forced writeback.
    bgwriter_flush_after: typing.Optional[int] = Field(None, alias='bgwriter_flush_after')

    # The maximum number of buffers that the background writer can write. Setting this to zero disables background writing. Default is 100.
    bgwriter_lru_maxpages: typing.Optional[int] = Field(None, alias='bgwriter_lru_maxpages')

    # The average recent need for new buffers is multiplied by bgwriter_lru_multiplier to arrive at an estimate of the number that will be needed during the next round, (up to bgwriter_lru_maxpages). 1.0 represents a “just in time” policy of writing exactly the number of buffers predicted to be needed. Larger values provide some cushion against spikes in demand, while smaller values intentionally leave writes to be done by server processes. The default is 2.0.
    bgwriter_lru_multiplier: typing.Optional[typing.Union[int, float]] = Field(None, alias='bgwriter_lru_multiplier')

    # The amount of time, in milliseconds, to wait on a lock before checking to see if there is a deadlock condition.
    deadlock_timeout: typing.Optional[int] = Field(None, alias='deadlock_timeout')

    # Specifies the default TOAST compression method for values of compressible columns (the default is lz4).
    default_toast_compression: typing.Optional[Literal["lz4", "pglz"]] = Field(None, alias='default_toast_compression')

    # Time out sessions with open transactions after this number of milliseconds
    idle_in_transaction_session_timeout: typing.Optional[int] = Field(None, alias='idle_in_transaction_session_timeout')

    # Activates, in a boolean, the system-wide use of Just-in-Time Compilation (JIT).
    jit: typing.Optional[bool] = Field(None, alias='jit')

    # Causes each action executed by autovacuum to be logged if it ran for at least the specified number of milliseconds. Setting this to zero logs all autovacuum actions. Minus-one (the default) disables logging autovacuum actions.
    log_autovacuum_min_duration: typing.Optional[int] = Field(None, alias='log_autovacuum_min_duration')

    # Controls the amount of detail written in the server log for each message that is logged.
    log_error_verbosity: typing.Optional[Literal["TERSE", "DEFAULT", "VERBOSE"]] = Field(None, alias='log_error_verbosity')

    # Selects one of the available log-formats. These can support popular log analyzers like pgbadger, pganalyze, etc.
    log_line_prefix: typing.Optional[Literal["pid=%p,user=%u,db=%d,app=%a,client=%h", "%m [%p] %q[user=%u,db=%d,app=%a]", "%t [%p]: [%l-1] user=%u,db=%d,app=%a,client=%h"]] = Field(None, alias='log_line_prefix')

    # Log statements that take more than this number of milliseconds to run. If -1, disables.
    log_min_duration_statement: typing.Optional[int] = Field(None, alias='log_min_duration_statement')

    # PostgreSQL maximum number of files that can be open per process.
    max_files_per_process: typing.Optional[int] = Field(None, alias='max_files_per_process')

    # PostgreSQL maximum prepared transactions. Once increased, this parameter cannot be lowered from its set value.
    max_prepared_transactions: typing.Optional[int] = Field(None, alias='max_prepared_transactions')

    # PostgreSQL maximum predicate locks per transaction.
    max_pred_locks_per_transaction: typing.Optional[int] = Field(None, alias='max_pred_locks_per_transaction')

    # PostgreSQL maximum locks per transaction. Once increased, this parameter cannot be lowered from its set value.
    max_locks_per_transaction: typing.Optional[int] = Field(None, alias='max_locks_per_transaction')

    # Maximum depth of the stack in bytes.
    max_stack_depth: typing.Optional[int] = Field(None, alias='max_stack_depth')

    # Max standby archive delay in milliseconds.
    max_standby_archive_delay: typing.Optional[int] = Field(None, alias='max_standby_archive_delay')

    # Max standby streaming delay in milliseconds.
    max_standby_streaming_delay: typing.Optional[int] = Field(None, alias='max_standby_streaming_delay')

    # PostgreSQL maximum replication slots.
    max_replication_slots: typing.Optional[int] = Field(None, alias='max_replication_slots')

    # PostgreSQL maximum logical replication workers (taken from the pool of max_parallel_workers).
    max_logical_replication_workers: typing.Optional[int] = Field(None, alias='max_logical_replication_workers')

    # Sets the maximum number of workers that the system can support for parallel queries.
    max_parallel_workers: typing.Optional[int] = Field(None, alias='max_parallel_workers')

    # Sets the maximum number of workers that can be started by a single Gather or Gather Merge node.
    max_parallel_workers_per_gather: typing.Optional[int] = Field(None, alias='max_parallel_workers_per_gather')

    # Sets the maximum number of background processes that the system can support. Once increased, this parameter cannot be lowered from its set value.
    max_worker_processes: typing.Optional[int] = Field(None, alias='max_worker_processes')

    # Controls which role to use for pg_partman's scheduled background tasks. Must consist of alpha-numeric characters, dots, underscores, or dashes. May not start with dash or dot. Maximum of 64 characters.
    pg_partman_bgw.role_: typing.Optional[str] = Field(None, alias='pg_partman_bgw.role')

    # Sets the time interval to run pg_partman's scheduled tasks.
    pg_partman_bgw.interval_: typing.Optional[int] = Field(None, alias='pg_partman_bgw.interval')

    # Controls which statements are counted. Specify 'top' to track top-level statements (those issued directly by clients), 'all' to also track nested statements (such as statements invoked within functions), or 'none' to disable statement statistics collection. The default value is top.
    pg_stat_statements.track_: typing.Optional[Literal["all", "top", "none"]] = Field(None, alias='pg_stat_statements.track')

    # PostgreSQL temporary file limit in KiB. If -1, sets to unlimited.
    temp_file_limit: typing.Optional[int] = Field(None, alias='temp_file_limit')

    # PostgreSQL service timezone
    timezone: typing.Optional[str] = Field(None, alias='timezone')

    # Specifies the number of bytes reserved to track the currently executing command for each active session.
    track_activity_query_size: typing.Optional[int] = Field(None, alias='track_activity_query_size')

    # Record commit time of transactions.
    track_commit_timestamp: typing.Optional[Literal["false", "true"]] = Field(None, alias='track_commit_timestamp')

    # Enables tracking of function call counts and time used.
    track_functions: typing.Optional[Literal["all", "pl", "none"]] = Field(None, alias='track_functions')

    # Enables timing of database I/O calls. This parameter is off by default, because it will repeatedly query the operating system for the current time, which may cause significant overhead on some platforms.
    track_io_timing: typing.Optional[Literal["false", "true"]] = Field(None, alias='track_io_timing')

    # PostgreSQL maximum WAL senders. Once increased, this parameter cannot be lowered from its set value.
    max_wal_senders: typing.Optional[int] = Field(None, alias='max_wal_senders')

    # Terminate replication connections that are inactive for longer than this amount of time, in milliseconds. Setting this value to zero disables the timeout. Must be either 0 or between 5000 and 10800000.
    wal_sender_timeout: typing.Optional[int] = Field(None, alias='wal_sender_timeout')

    # WAL flush interval in milliseconds. Note that setting this value to lower than the default 200ms may negatively impact performance
    wal_writer_delay: typing.Optional[int] = Field(None, alias='wal_writer_delay')

    # Percentage of total RAM that the database server uses for shared memory buffers.  Valid range is 20-60 (float), which corresponds to 20% - 60%.  This setting adjusts the shared_buffers configuration value.
    shared_buffers_percentage: typing.Optional[typing.Union[int, float]] = Field(None, alias='shared_buffers_percentage')

    pgbouncer: typing.Optional[Pgbouncer] = Field(None, alias='pgbouncer')

    # The maximum amount of memory, in MB, used by a query operation (such as a sort or hash table) before writing to temporary disk files. Default is 1MB + 0.075% of total RAM (up to 32MB).
    work_mem: typing.Optional[int] = Field(None, alias='work_mem')

    timescaledb: typing.Optional[Timescaledb] = Field(None, alias='timescaledb')

    # Synchronous replication type. Note that the service plan also needs to support synchronous replication.
    synchronous_replication: typing.Optional[Literal["false", "quorum"]] = Field(None, alias='synchronous_replication')

    # Enable the pg_stat_monitor extension. <b>Enabling this extension will cause the cluster to be restarted.</b> When this extension is enabled, pg_stat_statements results for utility commands are unreliable.
    stat_monitor_enable: typing.Optional[bool] = Field(None, alias='stat_monitor_enable')
    class Config:
        arbitrary_types_allowed = True
