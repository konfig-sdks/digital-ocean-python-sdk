<div align="left">

[![Visit Digitalocean](./header.png)](https://digitalocean.com)

# Digitalocean<a id="digitalocean"></a>

# Introduction<a id="introduction"></a>

The DigitalOcean API allows you to manage Droplets and resources within the
DigitalOcean cloud in a simple, programmatic way using conventional HTTP requests.

All of the functionality that you are familiar with in the DigitalOcean
control panel is also available through the API, allowing you to script the
complex actions that your situation requires.

The API documentation will start with a general overview about the design
and technology that has been implemented, followed by reference information
about specific endpoints.

## Requests<a id="requests"></a>

Any tool that is fluent in HTTP can communicate with the API simply by
requesting the correct URI. Requests should be made using the HTTPS protocol
so that traffic is encrypted. The interface responds to different methods
depending on the action required.

|Method|Usage|
|--- |--- |
|GET|For simple retrieval of information about your account, Droplets, or environment, you should use the GET method.  The information you request will be returned to you as a JSON object. The attributes defined by the JSON object can be used to form additional requests.  Any request using the GET method is read-only and will not affect any of the objects you are querying.|
|DELETE|To destroy a resource and remove it from your account and environment, the DELETE method should be used.  This will remove the specified object if it is found.  If it is not found, the operation will return a response indicating that the object was not found. This idempotency means that you do not have to check for a resource's availability prior to issuing a delete command, the final state will be the same regardless of its existence.|
|PUT|To update the information about a resource in your account, the PUT method is available. Like the DELETE Method, the PUT method is idempotent.  It sets the state of the target using the provided values, regardless of their current values. Requests using the PUT method do not need to check the current attributes of the object.|
|PATCH|Some resources support partial modification. In these cases, the PATCH method is available. Unlike PUT which generally requires a complete representation of a resource, a PATCH request is is a set of instructions on how to modify a resource updating only specific attributes.|
|POST|To create a new object, your request should specify the POST method. The POST request includes all of the attributes necessary to create a new object.  When you wish to create a new object, send a POST request to the target endpoint.|
|HEAD|Finally, to retrieve metadata information, you should use the HEAD method to get the headers.  This returns only the header of what would be returned with an associated GET request. Response headers contain some useful information about your API access and the results that are available for your request. For instance, the headers contain your current rate-limit value and the amount of time available until the limit resets. It also contains metrics about the total number of objects found, pagination information, and the total content length.|


## HTTP Statuses<a id="http-statuses"></a>

Along with the HTTP methods that the API responds to, it will also return
standard HTTP statuses, including error codes.

In the event of a problem, the status will contain the error code, while the
body of the response will usually contain additional information about the
problem that was encountered.

In general, if the status returned is in the 200 range, it indicates that
the request was fulfilled successfully and that no error was encountered.

Return codes in the 400 range typically indicate that there was an issue
with the request that was sent. Among other things, this could mean that you
did not authenticate correctly, that you are requesting an action that you
do not have authorization for, that the object you are requesting does not
exist, or that your request is malformed.

If you receive a status in the 500 range, this generally indicates a
server-side problem. This means that we are having an issue on our end and
cannot fulfill your request currently.

400 and 500 level error responses will include a JSON object in their body,
including the following attributes:

|Name|Type|Description|
|--- |--- |--- |
|id|string|A short identifier corresponding to the HTTP status code returned. For example, the ID for a response returning a 404 status code would be \"not_found.\"|
|message|string|A message providing additional information about the error, including details to help resolve it when possible.|
|request_id|string|Optionally, some endpoints may include a request ID that should be provided when reporting bugs or opening support tickets to help identify the issue.|

### Example Error Response<a id="example-error-response"></a>

```
    HTTP/1.1 403 Forbidden
    {
      \"id\":       \"forbidden\",
      \"message\":  \"You do not have access for the attempted action.\"
    }
```

## Responses<a id="responses"></a>

When a request is successful, a response body will typically be sent back in
the form of a JSON object. An exception to this is when a DELETE request is
processed, which will result in a successful HTTP 204 status and an empty
response body.

Inside of this JSON object, the resource root that was the target of the
request will be set as the key. This will be the singular form of the word
if the request operated on a single object, and the plural form of the word
if a collection was processed.

For example, if you send a GET request to `/v2/droplets/$DROPLET_ID` you
will get back an object with a key called \"`droplet`\". However, if you send
the GET request to the general collection at `/v2/droplets`, you will get
back an object with a key called \"`droplets`\".

The value of these keys will generally be a JSON object for a request on a
single object and an array of objects for a request on a collection of
objects.

### Response for a Single Object<a id="response-for-a-single-object"></a>

```
    {
        \"droplet\": {
            \"name\": \"example.com\"
            . . .
        }
    }
```

### Response for an Object Collection<a id="response-for-an-object-collection"></a>

```
    {
        \"droplets\": [
            {
                \"name\": \"example.com\"
                . . .
            },
            {
                \"name\": \"second.com\"
                . . .
            }
        ]
    }
```

## Meta<a id="meta"></a>

In addition to the main resource root, the response may also contain a
`meta` object. This object contains information about the response itself.

The `meta` object contains a `total` key that is set to the total number of
objects returned by the request. This has implications on the `links` object
and pagination.

The `meta` object will only be displayed when it has a value. Currently, the
`meta` object will have a value when a request is made on a collection (like
`droplets` or `domains`).


### Sample Meta Object<a id="sample-meta-object"></a>

```
    {
        . . .
        \"meta\": {
            \"total\": 43
        }
        . . .
    }
```

## Links & Pagination<a id="links--pagination"></a>

The `links` object is returned as part of the response body when pagination
is enabled. By default, 20 objects are returned per page. If the response
contains 20 objects or fewer, no `links` object will be returned. If the
response contains more than 20 objects, the first 20 will be returned along
with the `links` object.

You can request a different pagination limit or force pagination by
appending `?per_page=` to the request with the number of items you would
like per page. For instance, to show only two results per page, you could
add `?per_page=2` to the end of your query. The maximum number of results
per page is 200.

The `links` object contains a `pages` object. The `pages` object, in turn,
contains keys indicating the relationship of additional pages. The values of
these are the URLs of the associated pages. The keys will be one of the
following:

*   **first**: The URI of the first page of results.
*   **prev**: The URI of the previous sequential page of results.
*   **next**: The URI of the next sequential page of results.
*   **last**: The URI of the last page of results.

The `pages` object will only include the links that make sense. So for the
first page of results, no `first` or `prev` links will ever be set. This
convention holds true in other situations where a link would not make sense.

### Sample Links Object<a id="sample-links-object"></a>

```
    {
        . . .
        \"links\": {
            \"pages\": {
                \"last\": \"https://api.digitalocean.com/v2/images?page=2\",
                \"next\": \"https://api.digitalocean.com/v2/images?page=2\"
            }
        }
        . . .
    }
```

## Rate Limit<a id="rate-limit"></a>

Requests through the API are rate limited per OAuth token. Current rate limits:

*   5,000 requests per hour
*   250 requests per minute (5% of the hourly total)

Once you exceed either limit, you will be rate limited until the next cycle
starts. Space out any requests that you would otherwise issue in bursts for
the best results.

The rate limiting information is contained within the response headers of
each request. The relevant headers are:

*   **ratelimit-limit**: The number of requests that can be made per hour.
*   **ratelimit-remaining**: The number of requests that remain before you hit your request limit. See the information below for how the request limits expire.
*   **ratelimit-reset**: This represents the time when the oldest request will expire. The value is given in [Unix epoch time](http://en.wikipedia.org/wiki/Unix_time). See below for more information about how request limits expire.

More rate limiting information is returned only within burst limit error response headers:
*   **retry-after**: The number of seconds to wait before making another request when rate limited.

As long as the `ratelimit-remaining` count is above zero, you will be able
to make additional requests.

The way that a request expires and is removed from the current limit count
is important to understand. Rather than counting all of the requests for an
hour and resetting the `ratelimit-remaining` value at the end of the hour,
each request instead has its own timer.

This means that each request contributes toward the `ratelimit-remaining`
count for one complete hour after the request is made. When that request's
timer runs out, it is no longer counted towards the request limit.

This has implications on the meaning of the `ratelimit-reset` header as
well. Because the entire rate limit is not reset at one time, the value of
this header is set to the time when the _oldest_ request will expire.

Keep this in mind if you see your `ratelimit-reset` value change, but not
move an entire hour into the future.

If the `ratelimit-remaining` reaches zero, subsequent requests will receive
a 429 error code until the request reset has been reached. 

`ratelimit-remaining` reaching zero can also indicate that the \"burst limit\" of 250 
requests per minute limit was met, even if the 5,000 requests per hour limit was not. 
In this case, the 429 error response will include a retry-after header to indicate how 
long to wait (in seconds) until the request may be retried.

You can see the format of the response in the examples. 

**Note:** The following endpoints have special rate limit requirements that
are independent of the limits defined above.

*   Only 12 `POST` requests to the `/v2/floating_ips` endpoint to create Floating IPs can be made per 60 seconds.
*   Only 10 `GET` requests to the `/v2/account/keys` endpoint to list SSH keys can be made per 60 seconds.
*   Only 5 requests to any and all `v2/cdn/endpoints` can be made per 10 seconds. This includes `v2/cdn/endpoints`, 
    `v2/cdn/endpoints/$ENDPOINT_ID`, and `v2/cdn/endpoints/$ENDPOINT_ID/cache`.
*   Only 50 strings within the `files` json struct in the `v2/cdn/endpoints/$ENDPOINT_ID/cache` [payload](https://docs.digitalocean.com/reference/api/api-reference/#operation/cdn_purge_cache) 
    can be requested every 20 seconds.

### Sample Rate Limit Headers<a id="sample-rate-limit-headers"></a>

```
    . . .
    ratelimit-limit: 1200
    ratelimit-remaining: 1193
    rateLimit-reset: 1402425459
    . . .
```

  ### Sample Rate Limit Headers When Burst Limit is Reached:

```
    . . .
    ratelimit-limit: 5000
    ratelimit-remaining: 0
    rateLimit-reset: 1402425459
    retry-after: 29
    . . .
```

### Sample Rate Exceeded Response<a id="sample-rate-exceeded-response"></a>

```
    429 Too Many Requests
    {
            id: \"too_many_requests\",
            message: \"API Rate limit exceeded.\"
    }
```

## Curl Examples<a id="curl-examples"></a>

Throughout this document, some example API requests will be given using the
`curl` command. This will allow us to demonstrate the various endpoints in a
simple, textual format.
  
  These examples assume that you are using a Linux or macOS command line. To run
these commands on a Windows machine, you can either use cmd.exe, PowerShell, or WSL:

* For cmd.exe, use the `set VAR=VALUE` [syntax](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/set_1)
to define environment variables, call them with `%VAR%`, then replace all backslashes (`\\`) in the examples with carets (`^`).

* For PowerShell, use the `$Env:VAR = \"VALUE\"` [syntax](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_environment_variables?view=powershell-7.2)
to define environment variables, call them with `$Env:VAR`, then replace `curl` with `curl.exe` and all backslashes (`\\`) in the examples with backticks (`` ` ``).

* WSL is a compatibility layer that allows you to emulate a Linux terminal on a Windows machine.
Install WSL with our [community tutorial](https://www.digitalocean.com/community/tutorials/how-to-install-the-windows-subsystem-for-linux-2-on-microsoft-windows-10), 
then follow this API documentation normally.

The names of account-specific references (like Droplet IDs, for instance)
will be represented by variables. For instance, a Droplet ID may be
represented by a variable called `$DROPLET_ID`. You can set the associated
variables in your environment if you wish to use the examples without
modification.

The first variable that you should set to get started is your OAuth
authorization token. The next section will go over the details of this, but
you can set an environmental variable for it now.

Generate a token by going to the [Apps & API](https://cloud.digitalocean.com/settings/applications)
section of the DigitalOcean control panel. Use an existing token if you have
saved one, or generate a new token with the \"Generate new token\" button.
Copy the generated token and use it to set and export the TOKEN variable in
your environment as the example shows.

You may also wish to set some other variables now or as you go along. For
example, you may wish to set the `DROPLET_ID` variable to one of your
Droplet IDs since this will be used frequently in the API.

If you are following along, make sure you use a Droplet ID that you control
so that your commands will execute correctly.

If you need access to the headers of a response through `curl`, you can pass
the `-i` flag to display the header information along with the body. If you
are only interested in the header, you can instead pass the `-I` flag, which
will exclude the response body entirely.


### Set and Export your OAuth Token<a id="set-and-export-your-oauth-token"></a>

```
export DIGITALOCEAN_TOKEN=your_token_here
```

### Set and Export a Variable<a id="set-and-export-a-variable"></a>

```
export DROPLET_ID=1111111
```

## Parameters<a id="parameters"></a>

There are two different ways to pass parameters in a request with the API.

When passing parameters to create or update an object, parameters should be
passed as a JSON object containing the appropriate attribute names and
values as key-value pairs. When you use this format, you should specify that
you are sending a JSON object in the header. This is done by setting the
`Content-Type` header to `application/json`. This ensures that your request
is interpreted correctly.

When passing parameters to filter a response on GET requests, parameters can
be passed using standard query attributes. In this case, the parameters
would be embedded into the URI itself by appending a `?` to the end of the
URI and then setting each attribute with an equal sign. Attributes can be
separated with a `&`. Tools like `curl` can create the appropriate URI when
given parameters and values; this can also be done using the `-F` flag and
then passing the key and value as an argument. The argument should take the
form of a quoted string with the attribute being set to a value with an
equal sign.

### Pass Parameters as a JSON Object<a id="pass-parameters-as-a-json-object"></a>

```
    curl -H \"Authorization: Bearer $DIGITALOCEAN_TOKEN\" \\
        -H \"Content-Type: application/json\" \\
        -d '{\"name\": \"example.com\", \"ip_address\": \"127.0.0.1\"}' \\
        -X POST \"https://api.digitalocean.com/v2/domains\"
```

### Pass Filter Parameters as a Query String<a id="pass-filter-parameters-as-a-query-string"></a>

```
     curl -H \"Authorization: Bearer $DIGITALOCEAN_TOKEN\" \\
         -X GET \\
         \"https://api.digitalocean.com/v2/images?private=true\"
```

## Cross Origin Resource Sharing<a id="cross-origin-resource-sharing"></a>

In order to make requests to the API from other domains, the API implements
Cross Origin Resource Sharing (CORS) support.

CORS support is generally used to create AJAX requests outside of the domain
that the request originated from. This is necessary to implement projects
like control panels utilizing the API. This tells the browser that it can
send requests to an outside domain.

The procedure that the browser initiates in order to perform these actions
(other than GET requests) begins by sending a \"preflight\" request. This sets
the `Origin` header and uses the `OPTIONS` method. The server will reply
back with the methods it allows and some of the limits it imposes. The
client then sends the actual request if it falls within the allowed
constraints.

This process is usually done in the background by the browser, but you can
use curl to emulate this process using the example provided. The headers
that will be set to show the constraints are:

*   **Access-Control-Allow-Origin**: This is the domain that is sent by the client or browser as the origin of the request. It is set through an `Origin` header.
*   **Access-Control-Allow-Methods**: This specifies the allowed options for requests from that domain. This will generally be all available methods.
*   **Access-Control-Expose-Headers**: This will contain the headers that will be available to requests from the origin domain.
*   **Access-Control-Max-Age**: This is the length of time that the access is considered valid. After this expires, a new preflight should be sent.
*   **Access-Control-Allow-Credentials**: This will be set to `true`. It basically allows you to send your OAuth token for authentication.

You should not need to be concerned with the details of these headers,
because the browser will typically do all of the work for you.



</div>

## Table of Contents<a id="table-of-contents"></a>

<!-- toc -->

- [Requirements](#requirements)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Async](#async)
- [Raw HTTP Response](#raw-http-response)
- [Reference](#reference)
  * [`digitalocean.1_click_applications.install_kubernetes_application`](#digitalocean1_click_applicationsinstall_kubernetes_application)
  * [`digitalocean.1_click_applications.list`](#digitalocean1_click_applicationslist)
  * [`digitalocean.account.get`](#digitaloceanaccountget)
  * [`digitalocean.actions.get`](#digitaloceanactionsget)
  * [`digitalocean.actions.list`](#digitaloceanactionslist)
  * [`digitalocean.apps.cancel_deployment`](#digitaloceanappscancel_deployment)
  * [`digitalocean.apps.commit_rollback`](#digitaloceanappscommit_rollback)
  * [`digitalocean.apps.create`](#digitaloceanappscreate)
  * [`digitalocean.apps.create_deployment`](#digitaloceanappscreate_deployment)
  * [`digitalocean.apps.delete`](#digitaloceanappsdelete)
  * [`digitalocean.apps.get`](#digitaloceanappsget)
  * [`digitalocean.apps.get_active_deployment_logs`](#digitaloceanappsget_active_deployment_logs)
  * [`digitalocean.apps.get_active_deployment_logs_0`](#digitaloceanappsget_active_deployment_logs_0)
  * [`digitalocean.apps.get_aggregate_deployment_logs`](#digitaloceanappsget_aggregate_deployment_logs)
  * [`digitalocean.apps.get_app_daily_bandwidth_metrics`](#digitaloceanappsget_app_daily_bandwidth_metrics)
  * [`digitalocean.apps.get_deployment_info`](#digitaloceanappsget_deployment_info)
  * [`digitalocean.apps.get_deployment_logs`](#digitaloceanappsget_deployment_logs)
  * [`digitalocean.apps.get_instance_size`](#digitaloceanappsget_instance_size)
  * [`digitalocean.apps.get_multiple_daily_metrics`](#digitaloceanappsget_multiple_daily_metrics)
  * [`digitalocean.apps.get_tier_info`](#digitaloceanappsget_tier_info)
  * [`digitalocean.apps.list`](#digitaloceanappslist)
  * [`digitalocean.apps.list_alerts`](#digitaloceanappslist_alerts)
  * [`digitalocean.apps.list_deployments`](#digitaloceanappslist_deployments)
  * [`digitalocean.apps.list_instance_sizes`](#digitaloceanappslist_instance_sizes)
  * [`digitalocean.apps.list_regions`](#digitaloceanappslist_regions)
  * [`digitalocean.apps.list_tiers`](#digitaloceanappslist_tiers)
  * [`digitalocean.apps.propose_app_spec`](#digitaloceanappspropose_app_spec)
  * [`digitalocean.apps.revert_rollback`](#digitaloceanappsrevert_rollback)
  * [`digitalocean.apps.rollback_deployment`](#digitaloceanappsrollback_deployment)
  * [`digitalocean.apps.update`](#digitaloceanappsupdate)
  * [`digitalocean.apps.update_destinations_for_alerts`](#digitaloceanappsupdate_destinations_for_alerts)
  * [`digitalocean.apps.validate_rollback`](#digitaloceanappsvalidate_rollback)
  * [`digitalocean.billing.get`](#digitaloceanbillingget)
  * [`digitalocean.billing.get_invoice_by_uuid`](#digitaloceanbillingget_invoice_by_uuid)
  * [`digitalocean.billing.get_invoice_csv_by_uuid`](#digitaloceanbillingget_invoice_csv_by_uuid)
  * [`digitalocean.billing.get_invoice_summary_by_uuid`](#digitaloceanbillingget_invoice_summary_by_uuid)
  * [`digitalocean.billing.get_pdf_by_uuid`](#digitaloceanbillingget_pdf_by_uuid)
  * [`digitalocean.billing.list`](#digitaloceanbillinglist)
  * [`digitalocean.billing.list_0`](#digitaloceanbillinglist_0)
  * [`digitalocean.block_storage.create`](#digitaloceanblock_storagecreate)
  * [`digitalocean.block_storage.create_0`](#digitaloceanblock_storagecreate_0)
  * [`digitalocean.block_storage.delete`](#digitaloceanblock_storagedelete)
  * [`digitalocean.block_storage.delete_by_region_and_name`](#digitaloceanblock_storagedelete_by_region_and_name)
  * [`digitalocean.block_storage.delete_volume_snapshot`](#digitaloceanblock_storagedelete_volume_snapshot)
  * [`digitalocean.block_storage.get`](#digitaloceanblock_storageget)
  * [`digitalocean.block_storage.get_snapshot_details`](#digitaloceanblock_storageget_snapshot_details)
  * [`digitalocean.block_storage.list`](#digitaloceanblock_storagelist)
- [Filtering Results](#filtering-results)
  * [By Region](#by-region)
  * [By Name](#by-name)
  * [By Name and Region](#by-name-and-region)
  * [`digitalocean.block_storage.list_0`](#digitaloceanblock_storagelist_0)
  * [`digitalocean.block_storage_actions.get`](#digitaloceanblock_storage_actionsget)
  * [`digitalocean.block_storage_actions.initiate_attach_action`](#digitaloceanblock_storage_actionsinitiate_attach_action)
- [Attach a Block Storage Volume to a Droplet](#attach-a-block-storage-volume-to-a-droplet)
- [Remove a Block Storage Volume from a Droplet](#remove-a-block-storage-volume-from-a-droplet)
- [Resize a Volume](#resize-a-volume)
  * [`digitalocean.block_storage_actions.list`](#digitaloceanblock_storage_actionslist)
  * [`digitalocean.block_storage_actions.post`](#digitaloceanblock_storage_actionspost)
- [Attach a Block Storage Volume to a Droplet](#attach-a-block-storage-volume-to-a-droplet-1)
- [Remove a Block Storage Volume from a Droplet](#remove-a-block-storage-volume-from-a-droplet-1)
  * [`digitalocean.cdn_endpoints.create_new_endpoint`](#digitaloceancdn_endpointscreate_new_endpoint)
  * [`digitalocean.cdn_endpoints.delete_endpoint`](#digitaloceancdn_endpointsdelete_endpoint)
  * [`digitalocean.cdn_endpoints.get_existing_endpoint`](#digitaloceancdn_endpointsget_existing_endpoint)
  * [`digitalocean.cdn_endpoints.list_all`](#digitaloceancdn_endpointslist_all)
  * [`digitalocean.cdn_endpoints.purge_cache`](#digitaloceancdn_endpointspurge_cache)
  * [`digitalocean.cdn_endpoints.update_endpoint`](#digitaloceancdn_endpointsupdate_endpoint)
  * [`digitalocean.certificates.create`](#digitaloceancertificatescreate)
  * [`digitalocean.certificates.delete`](#digitaloceancertificatesdelete)
  * [`digitalocean.certificates.get`](#digitaloceancertificatesget)
  * [`digitalocean.certificates.list`](#digitaloceancertificateslist)
  * [`digitalocean.container_registry.cancel_garbage_collection`](#digitaloceancontainer_registrycancel_garbage_collection)
  * [`digitalocean.container_registry.create`](#digitaloceancontainer_registrycreate)
  * [`digitalocean.container_registry.delete`](#digitaloceancontainer_registrydelete)
  * [`digitalocean.container_registry.delete_repository_manifest_by_digest`](#digitaloceancontainer_registrydelete_repository_manifest_by_digest)
  * [`digitalocean.container_registry.delete_repository_tag`](#digitaloceancontainer_registrydelete_repository_tag)
  * [`digitalocean.container_registry.get`](#digitaloceancontainer_registryget)
  * [`digitalocean.container_registry.get_active_garbage_collection`](#digitaloceancontainer_registryget_active_garbage_collection)
  * [`digitalocean.container_registry.get_docker_credentials`](#digitaloceancontainer_registryget_docker_credentials)
  * [`digitalocean.container_registry.get_subscription_info`](#digitaloceancontainer_registryget_subscription_info)
  * [`digitalocean.container_registry.list_garbage_collections`](#digitaloceancontainer_registrylist_garbage_collections)
  * [`digitalocean.container_registry.list_options`](#digitaloceancontainer_registrylist_options)
  * [`digitalocean.container_registry.list_repositories`](#digitaloceancontainer_registrylist_repositories)
  * [`digitalocean.container_registry.list_repositories_v2`](#digitaloceancontainer_registrylist_repositories_v2)
  * [`digitalocean.container_registry.list_repository_manifests`](#digitaloceancontainer_registrylist_repository_manifests)
  * [`digitalocean.container_registry.list_repository_tags`](#digitaloceancontainer_registrylist_repository_tags)
  * [`digitalocean.container_registry.start_garbage_collection`](#digitaloceancontainer_registrystart_garbage_collection)
  * [`digitalocean.container_registry.update_subscription_tier`](#digitaloceancontainer_registryupdate_subscription_tier)
  * [`digitalocean.container_registry.validate_name`](#digitaloceancontainer_registryvalidate_name)
  * [`digitalocean.databases.add`](#digitaloceandatabasesadd)
  * [`digitalocean.databases.add_new_connection_pool`](#digitaloceandatabasesadd_new_connection_pool)
  * [`digitalocean.databases.add_user`](#digitaloceandatabasesadd_user)
  * [`digitalocean.databases.configure_eviction_policy`](#digitaloceandatabasesconfigure_eviction_policy)
  * [`digitalocean.databases.configure_maintenance_window`](#digitaloceandatabasesconfigure_maintenance_window)
  * [`digitalocean.databases.create_cluster`](#digitaloceandatabasescreate_cluster)
  * [`digitalocean.databases.create_read_only_replica`](#digitaloceandatabasescreate_read_only_replica)
  * [`digitalocean.databases.create_topic_kafka_cluster`](#digitaloceandatabasescreate_topic_kafka_cluster)
  * [`digitalocean.databases.delete`](#digitaloceandatabasesdelete)
  * [`digitalocean.databases.delete_connection_pool`](#digitaloceandatabasesdelete_connection_pool)
  * [`digitalocean.databases.delete_topic_kafka_cluster`](#digitaloceandatabasesdelete_topic_kafka_cluster)
  * [`digitalocean.databases.destroy_cluster`](#digitaloceandatabasesdestroy_cluster)
  * [`digitalocean.databases.destroy_readonly_replica`](#digitaloceandatabasesdestroy_readonly_replica)
  * [`digitalocean.databases.get`](#digitaloceandatabasesget)
  * [`digitalocean.databases.get_cluster_config`](#digitaloceandatabasesget_cluster_config)
  * [`digitalocean.databases.get_cluster_info`](#digitaloceandatabasesget_cluster_info)
  * [`digitalocean.databases.get_clusters_metrics_credentials`](#digitaloceandatabasesget_clusters_metrics_credentials)
  * [`digitalocean.databases.get_connection_pool`](#digitaloceandatabasesget_connection_pool)
  * [`digitalocean.databases.get_eviction_policy`](#digitaloceandatabasesget_eviction_policy)
  * [`digitalocean.databases.get_existing_read_only_replica`](#digitaloceandatabasesget_existing_read_only_replica)
  * [`digitalocean.databases.get_migration_status`](#digitaloceandatabasesget_migration_status)
  * [`digitalocean.databases.get_public_certificate`](#digitaloceandatabasesget_public_certificate)
  * [`digitalocean.databases.get_sql_mode`](#digitaloceandatabasesget_sql_mode)
  * [`digitalocean.databases.get_topic_kafka_cluster`](#digitaloceandatabasesget_topic_kafka_cluster)
  * [`digitalocean.databases.get_user`](#digitaloceandatabasesget_user)
  * [`digitalocean.databases.list`](#digitaloceandatabaseslist)
  * [`digitalocean.databases.list_backups`](#digitaloceandatabaseslist_backups)
  * [`digitalocean.databases.list_clusters`](#digitaloceandatabaseslist_clusters)
  * [`digitalocean.databases.list_connection_pools`](#digitaloceandatabaseslist_connection_pools)
  * [`digitalocean.databases.list_events_logs`](#digitaloceandatabaseslist_events_logs)
  * [`digitalocean.databases.list_firewall_rules`](#digitaloceandatabaseslist_firewall_rules)
  * [`digitalocean.databases.list_options`](#digitaloceandatabaseslist_options)
  * [`digitalocean.databases.list_read_only_replicas`](#digitaloceandatabaseslist_read_only_replicas)
  * [`digitalocean.databases.list_topics_kafka_cluster`](#digitaloceandatabaseslist_topics_kafka_cluster)
  * [`digitalocean.databases.list_users`](#digitaloceandatabaseslist_users)
  * [`digitalocean.databases.migrate_cluster_to_new_region`](#digitaloceandatabasesmigrate_cluster_to_new_region)
  * [`digitalocean.databases.promote_readonly_replica_to_primary`](#digitaloceandatabasespromote_readonly_replica_to_primary)
  * [`digitalocean.databases.remove_user`](#digitaloceandatabasesremove_user)
  * [`digitalocean.databases.reset_user_auth`](#digitaloceandatabasesreset_user_auth)
  * [`digitalocean.databases.resize_cluster`](#digitaloceandatabasesresize_cluster)
  * [`digitalocean.databases.start_online_migration`](#digitaloceandatabasesstart_online_migration)
  * [`digitalocean.databases.stop_online_migration`](#digitaloceandatabasesstop_online_migration)
  * [`digitalocean.databases.update_config_cluster`](#digitaloceandatabasesupdate_config_cluster)
  * [`digitalocean.databases.update_connection_pool_postgresql`](#digitaloceandatabasesupdate_connection_pool_postgresql)
  * [`digitalocean.databases.update_firewall_rules`](#digitaloceandatabasesupdate_firewall_rules)
  * [`digitalocean.databases.update_metrics_credentials`](#digitaloceandatabasesupdate_metrics_credentials)
  * [`digitalocean.databases.update_settings`](#digitaloceandatabasesupdate_settings)
  * [`digitalocean.databases.update_sql_mode`](#digitaloceandatabasesupdate_sql_mode)
  * [`digitalocean.databases.update_topic_kafka_cluster`](#digitaloceandatabasesupdate_topic_kafka_cluster)
  * [`digitalocean.databases.upgrade_major_version`](#digitaloceandatabasesupgrade_major_version)
  * [`digitalocean.domain_records.create_new_record`](#digitaloceandomain_recordscreate_new_record)
  * [`digitalocean.domain_records.delete_by_id`](#digitaloceandomain_recordsdelete_by_id)
  * [`digitalocean.domain_records.get_existing_record`](#digitaloceandomain_recordsget_existing_record)
  * [`digitalocean.domain_records.list_all_records`](#digitaloceandomain_recordslist_all_records)
  * [`digitalocean.domain_records.update_record_by_id`](#digitaloceandomain_recordsupdate_record_by_id)
  * [`digitalocean.domain_records.update_record_by_id_0`](#digitaloceandomain_recordsupdate_record_by_id_0)
  * [`digitalocean.domains.create`](#digitaloceandomainscreate)
  * [`digitalocean.domains.delete`](#digitaloceandomainsdelete)
  * [`digitalocean.domains.get`](#digitaloceandomainsget)
  * [`digitalocean.domains.list`](#digitaloceandomainslist)
  * [`digitalocean.droplet_actions.act_on_tagged_droplets`](#digitaloceandroplet_actionsact_on_tagged_droplets)
  * [`digitalocean.droplet_actions.get`](#digitaloceandroplet_actionsget)
  * [`digitalocean.droplet_actions.list`](#digitaloceandroplet_actionslist)
  * [`digitalocean.droplet_actions.post`](#digitaloceandroplet_actionspost)
  * [`digitalocean.droplets.check_destroy_status`](#digitaloceandropletscheck_destroy_status)
  * [`digitalocean.droplets.create`](#digitaloceandropletscreate)
  * [Create Multiple Droplets](#create-multiple-droplets)
  * [`digitalocean.droplets.delete_by_tag`](#digitaloceandropletsdelete_by_tag)
  * [`digitalocean.droplets.delete_dangerous`](#digitaloceandropletsdelete_dangerous)
  * [`digitalocean.droplets.destroy`](#digitaloceandropletsdestroy)
  * [`digitalocean.droplets.destroy_associated_resources_selective`](#digitaloceandropletsdestroy_associated_resources_selective)
  * [`digitalocean.droplets.get`](#digitaloceandropletsget)
  * [`digitalocean.droplets.list`](#digitaloceandropletslist)
  * [Filtering Results by Tag](#filtering-results-by-tag)
  * [`digitalocean.droplets.list_associated_resources`](#digitaloceandropletslist_associated_resources)
  * [`digitalocean.droplets.list_backups`](#digitaloceandropletslist_backups)
  * [`digitalocean.droplets.list_droplet_neighbors`](#digitaloceandropletslist_droplet_neighbors)
  * [`digitalocean.droplets.list_firewalls`](#digitaloceandropletslist_firewalls)
  * [`digitalocean.droplets.list_kernels`](#digitaloceandropletslist_kernels)
  * [`digitalocean.droplets.list_neighbors`](#digitaloceandropletslist_neighbors)
  * [`digitalocean.droplets.list_snapshots`](#digitaloceandropletslist_snapshots)
  * [`digitalocean.droplets.retry_destroy_with_associated_resources`](#digitaloceandropletsretry_destroy_with_associated_resources)
  * [`digitalocean.firewalls.add_droplets`](#digitaloceanfirewallsadd_droplets)
  * [`digitalocean.firewalls.add_rules`](#digitaloceanfirewallsadd_rules)
  * [`digitalocean.firewalls.add_tags`](#digitaloceanfirewallsadd_tags)
  * [`digitalocean.firewalls.create`](#digitaloceanfirewallscreate)
  * [`digitalocean.firewalls.delete`](#digitaloceanfirewallsdelete)
  * [`digitalocean.firewalls.get`](#digitaloceanfirewallsget)
  * [`digitalocean.firewalls.list`](#digitaloceanfirewallslist)
  * [`digitalocean.firewalls.remove_droplets`](#digitaloceanfirewallsremove_droplets)
  * [`digitalocean.firewalls.remove_rules`](#digitaloceanfirewallsremove_rules)
  * [`digitalocean.firewalls.remove_tags`](#digitaloceanfirewallsremove_tags)
  * [`digitalocean.firewalls.update`](#digitaloceanfirewallsupdate)
  * [`digitalocean.floating_ip_actions.get`](#digitaloceanfloating_ip_actionsget)
  * [`digitalocean.floating_ip_actions.list`](#digitaloceanfloating_ip_actionslist)
  * [`digitalocean.floating_ip_actions.post`](#digitaloceanfloating_ip_actionspost)
  * [`digitalocean.floating_ips.create`](#digitaloceanfloating_ipscreate)
  * [`digitalocean.floating_ips.delete`](#digitaloceanfloating_ipsdelete)
  * [`digitalocean.floating_ips.get`](#digitaloceanfloating_ipsget)
  * [`digitalocean.floating_ips.list`](#digitaloceanfloating_ipslist)
  * [`digitalocean.functions.create_namespace`](#digitaloceanfunctionscreate_namespace)
  * [`digitalocean.functions.create_trigger_in_namespace`](#digitaloceanfunctionscreate_trigger_in_namespace)
  * [`digitalocean.functions.delete_namespace`](#digitaloceanfunctionsdelete_namespace)
  * [`digitalocean.functions.delete_trigger`](#digitaloceanfunctionsdelete_trigger)
  * [`digitalocean.functions.get_namespace_details`](#digitaloceanfunctionsget_namespace_details)
  * [`digitalocean.functions.get_trigger_details`](#digitaloceanfunctionsget_trigger_details)
  * [`digitalocean.functions.list_namespaces`](#digitaloceanfunctionslist_namespaces)
  * [`digitalocean.functions.list_triggers`](#digitaloceanfunctionslist_triggers)
  * [`digitalocean.functions.update_trigger_details`](#digitaloceanfunctionsupdate_trigger_details)
  * [`digitalocean.image_actions.get`](#digitaloceanimage_actionsget)
  * [`digitalocean.image_actions.list`](#digitaloceanimage_actionslist)
  * [`digitalocean.image_actions.post`](#digitaloceanimage_actionspost)
- [Convert an Image to a Snapshot](#convert-an-image-to-a-snapshot)
- [Transfer an Image](#transfer-an-image)
  * [`digitalocean.images.delete`](#digitaloceanimagesdelete)
  * [`digitalocean.images.get`](#digitaloceanimagesget)
  * [`digitalocean.images.import_custom_image_from_url`](#digitaloceanimagesimport_custom_image_from_url)
  * [`digitalocean.images.list`](#digitaloceanimageslist)
- [Filtering Results](#filtering-results-1)
  * [`digitalocean.images.update`](#digitaloceanimagesupdate)
  * [`digitalocean.kubernetes.add_container_registry_to_clusters`](#digitaloceankubernetesadd_container_registry_to_clusters)
  * [`digitalocean.kubernetes.add_node_pool`](#digitaloceankubernetesadd_node_pool)
  * [`digitalocean.kubernetes.create_new_cluster`](#digitaloceankubernetescreate_new_cluster)
  * [`digitalocean.kubernetes.delete_cluster`](#digitaloceankubernetesdelete_cluster)
  * [`digitalocean.kubernetes.delete_cluster_associated_resources_dangerous`](#digitaloceankubernetesdelete_cluster_associated_resources_dangerous)
  * [`digitalocean.kubernetes.delete_node_in_node_pool`](#digitaloceankubernetesdelete_node_in_node_pool)
  * [`digitalocean.kubernetes.delete_node_pool`](#digitaloceankubernetesdelete_node_pool)
  * [`digitalocean.kubernetes.get_available_upgrades`](#digitaloceankubernetesget_available_upgrades)
  * [`digitalocean.kubernetes.get_cluster_info`](#digitaloceankubernetesget_cluster_info)
  * [`digitalocean.kubernetes.get_cluster_lint_diagnostics`](#digitaloceankubernetesget_cluster_lint_diagnostics)
  * [`digitalocean.kubernetes.get_credentials_by_cluster_id`](#digitaloceankubernetesget_credentials_by_cluster_id)
  * [`digitalocean.kubernetes.get_kubeconfig`](#digitaloceankubernetesget_kubeconfig)
  * [`digitalocean.kubernetes.get_node_pool`](#digitaloceankubernetesget_node_pool)
  * [`digitalocean.kubernetes.get_user_information`](#digitaloceankubernetesget_user_information)
  * [`digitalocean.kubernetes.list_associated_resources`](#digitaloceankuberneteslist_associated_resources)
  * [`digitalocean.kubernetes.list_clusters`](#digitaloceankuberneteslist_clusters)
  * [`digitalocean.kubernetes.list_node_pools`](#digitaloceankuberneteslist_node_pools)
  * [`digitalocean.kubernetes.list_options`](#digitaloceankuberneteslist_options)
  * [`digitalocean.kubernetes.recycle_node_pool`](#digitaloceankubernetesrecycle_node_pool)
  * [`digitalocean.kubernetes.remove_registry`](#digitaloceankubernetesremove_registry)
  * [`digitalocean.kubernetes.run_clusterlint_checks`](#digitaloceankubernetesrun_clusterlint_checks)
  * [`digitalocean.kubernetes.selective_cluster_destroy`](#digitaloceankubernetesselective_cluster_destroy)
  * [`digitalocean.kubernetes.update_cluster`](#digitaloceankubernetesupdate_cluster)
  * [`digitalocean.kubernetes.update_node_pool`](#digitaloceankubernetesupdate_node_pool)
  * [`digitalocean.kubernetes.upgrade_cluster`](#digitaloceankubernetesupgrade_cluster)
  * [`digitalocean.load_balancers.add_forwarding_rules`](#digitaloceanload_balancersadd_forwarding_rules)
  * [`digitalocean.load_balancers.assign_droplets`](#digitaloceanload_balancersassign_droplets)
  * [`digitalocean.load_balancers.create`](#digitaloceanload_balancerscreate)
  * [`digitalocean.load_balancers.delete`](#digitaloceanload_balancersdelete)
  * [`digitalocean.load_balancers.get`](#digitaloceanload_balancersget)
  * [`digitalocean.load_balancers.list`](#digitaloceanload_balancerslist)
  * [`digitalocean.load_balancers.remove_droplets`](#digitaloceanload_balancersremove_droplets)
  * [`digitalocean.load_balancers.remove_forwarding_rules`](#digitaloceanload_balancersremove_forwarding_rules)
  * [`digitalocean.load_balancers.update`](#digitaloceanload_balancersupdate)
  * [`digitalocean.monitoring.create_alert_policy`](#digitaloceanmonitoringcreate_alert_policy)
  * [`digitalocean.monitoring.delete_alert_policy`](#digitaloceanmonitoringdelete_alert_policy)
  * [`digitalocean.monitoring.droplet_cpu_metricsget`](#digitaloceanmonitoringdroplet_cpu_metricsget)
  * [`digitalocean.monitoring.droplet_load5_metrics_get`](#digitaloceanmonitoringdroplet_load5_metrics_get)
  * [`digitalocean.monitoring.droplet_memory_cached_metrics`](#digitaloceanmonitoringdroplet_memory_cached_metrics)
  * [`digitalocean.monitoring.get_app_cpu_percentage_metrics`](#digitaloceanmonitoringget_app_cpu_percentage_metrics)
  * [`digitalocean.monitoring.get_app_memory_percentage_metrics`](#digitaloceanmonitoringget_app_memory_percentage_metrics)
  * [`digitalocean.monitoring.get_app_restart_count_metrics`](#digitaloceanmonitoringget_app_restart_count_metrics)
  * [`digitalocean.monitoring.get_droplet_bandwidth_metrics`](#digitaloceanmonitoringget_droplet_bandwidth_metrics)
  * [`digitalocean.monitoring.get_droplet_filesystem_free_metrics`](#digitaloceanmonitoringget_droplet_filesystem_free_metrics)
  * [`digitalocean.monitoring.get_droplet_filesystem_size_metrics`](#digitaloceanmonitoringget_droplet_filesystem_size_metrics)
  * [`digitalocean.monitoring.get_droplet_load15_metrics`](#digitaloceanmonitoringget_droplet_load15_metrics)
  * [`digitalocean.monitoring.get_droplet_load1_metrics`](#digitaloceanmonitoringget_droplet_load1_metrics)
  * [`digitalocean.monitoring.get_droplet_memory_available_metrics`](#digitaloceanmonitoringget_droplet_memory_available_metrics)
  * [`digitalocean.monitoring.get_droplet_memory_free_metrics`](#digitaloceanmonitoringget_droplet_memory_free_metrics)
  * [`digitalocean.monitoring.get_droplet_memory_total_metrics`](#digitaloceanmonitoringget_droplet_memory_total_metrics)
  * [`digitalocean.monitoring.get_existing_alert_policy`](#digitaloceanmonitoringget_existing_alert_policy)
  * [`digitalocean.monitoring.list_alert_policies`](#digitaloceanmonitoringlist_alert_policies)
  * [`digitalocean.monitoring.update_alert_policy`](#digitaloceanmonitoringupdate_alert_policy)
  * [`digitalocean.project_resources.assign_resources_to_default`](#digitaloceanproject_resourcesassign_resources_to_default)
  * [`digitalocean.project_resources.assign_to_project`](#digitaloceanproject_resourcesassign_to_project)
  * [`digitalocean.project_resources.list`](#digitaloceanproject_resourceslist)
  * [`digitalocean.project_resources.list_default`](#digitaloceanproject_resourceslist_default)
  * [`digitalocean.projects.create`](#digitaloceanprojectscreate)
  * [`digitalocean.projects.delete`](#digitaloceanprojectsdelete)
  * [`digitalocean.projects.get`](#digitaloceanprojectsget)
  * [`digitalocean.projects.get_default_project`](#digitaloceanprojectsget_default_project)
  * [`digitalocean.projects.list`](#digitaloceanprojectslist)
  * [`digitalocean.projects.patch`](#digitaloceanprojectspatch)
  * [`digitalocean.projects.update`](#digitaloceanprojectsupdate)
  * [`digitalocean.projects.update_default_project`](#digitaloceanprojectsupdate_default_project)
  * [`digitalocean.projects.update_default_project_attributes`](#digitaloceanprojectsupdate_default_project_attributes)
  * [`digitalocean.regions.list`](#digitaloceanregionslist)
  * [`digitalocean.reserved_ip_actions.get`](#digitaloceanreserved_ip_actionsget)
  * [`digitalocean.reserved_ip_actions.list`](#digitaloceanreserved_ip_actionslist)
  * [`digitalocean.reserved_ip_actions.post`](#digitaloceanreserved_ip_actionspost)
  * [`digitalocean.reserved_ips.create`](#digitaloceanreserved_ipscreate)
  * [`digitalocean.reserved_ips.delete`](#digitaloceanreserved_ipsdelete)
  * [`digitalocean.reserved_ips.get`](#digitaloceanreserved_ipsget)
  * [`digitalocean.reserved_ips.list`](#digitaloceanreserved_ipslist)
  * [`digitalocean.ssh_keys.create`](#digitaloceanssh_keyscreate)
  * [`digitalocean.ssh_keys.delete`](#digitaloceanssh_keysdelete)
  * [`digitalocean.ssh_keys.get`](#digitaloceanssh_keysget)
  * [`digitalocean.ssh_keys.list`](#digitaloceanssh_keyslist)
  * [`digitalocean.ssh_keys.update`](#digitaloceanssh_keysupdate)
  * [`digitalocean.sizes.list`](#digitaloceansizeslist)
  * [`digitalocean.snapshots.delete`](#digitaloceansnapshotsdelete)
  * [`digitalocean.snapshots.get`](#digitaloceansnapshotsget)
  * [`digitalocean.snapshots.list`](#digitaloceansnapshotslist)
  * [Filtering Results by Resource Type](#filtering-results-by-resource-type)
  * [`digitalocean.tags.create`](#digitaloceantagscreate)
  * [`digitalocean.tags.delete`](#digitaloceantagsdelete)
  * [`digitalocean.tags.get`](#digitaloceantagsget)
  * [`digitalocean.tags.list`](#digitaloceantagslist)
  * [`digitalocean.tags.tag_resource`](#digitaloceantagstag_resource)
  * [`digitalocean.tags.untag_resource`](#digitaloceantagsuntag_resource)
  * [`digitalocean.uptime.create_check`](#digitaloceanuptimecreate_check)
  * [`digitalocean.uptime.create_new_alert`](#digitaloceanuptimecreate_new_alert)
  * [`digitalocean.uptime.delete_alert`](#digitaloceanuptimedelete_alert)
  * [`digitalocean.uptime.delete_check`](#digitaloceanuptimedelete_check)
  * [`digitalocean.uptime.get_check_by_id`](#digitaloceanuptimeget_check_by_id)
  * [`digitalocean.uptime.get_check_state`](#digitaloceanuptimeget_check_state)
  * [`digitalocean.uptime.get_existing_alert`](#digitaloceanuptimeget_existing_alert)
  * [`digitalocean.uptime.list_all_alerts`](#digitaloceanuptimelist_all_alerts)
  * [`digitalocean.uptime.list_checks`](#digitaloceanuptimelist_checks)
  * [`digitalocean.uptime.update_alert_settings`](#digitaloceanuptimeupdate_alert_settings)
  * [`digitalocean.uptime.update_check_settings`](#digitaloceanuptimeupdate_check_settings)
  * [`digitalocean.vpcs.create`](#digitaloceanvpcscreate)
  * [`digitalocean.vpcs.delete`](#digitaloceanvpcsdelete)
  * [`digitalocean.vpcs.get`](#digitaloceanvpcsget)
  * [`digitalocean.vpcs.list`](#digitaloceanvpcslist)
  * [`digitalocean.vpcs.list_members`](#digitaloceanvpcslist_members)
  * [`digitalocean.vpcs.patch`](#digitaloceanvpcspatch)
  * [`digitalocean.vpcs.update`](#digitaloceanvpcsupdate)

<!-- tocstop -->

## Requirements<a id="requirements"></a>

Python >=3.7

## Installation<a id="installation"></a>
<div align="center">
  <a href="https://konfigthis.com/sdk-sign-up?company=DigitalOcean&language=Python">
    <img src="https://raw.githubusercontent.com/konfig-dev/brand-assets/HEAD/cta-images/python-cta.png" width="70%">
  </a>
</div>

## Getting Started<a id="getting-started"></a>

```python
from pprint import pprint
from digital_ocean_python_sdk import DigitalOcean, ApiException

digitalocean = DigitalOcean(

    access_token = 'YOUR_BEARER_TOKEN'
)

try:
    # Install Kubernetes 1-Click Applications
    install_kubernetes_application_response = digitalocean.1_click_applications.install_kubernetes_application(
        addon_slugs=["kube-state-metrics", "loki"],
        cluster_uuid="50a994b6-c303-438f-9495-7e896cfe6b08",
    )
    print(install_kubernetes_application_response)
except ApiException as e:
    print("Exception when calling Model1ClickApplicationsApi.install_kubernetes_application: %s\n" % e)
    pprint(e.body)
    pprint(e.headers)
    pprint(e.status)
    pprint(e.reason)
    pprint(e.round_trip_time)
```

## Async<a id="async"></a>

`async` support is available by prepending `a` to any method.

```python

import asyncio
from pprint import pprint
from digital_ocean_python_sdk import DigitalOcean, ApiException

digitalocean = DigitalOcean(

    access_token = 'YOUR_BEARER_TOKEN'
)

async def main():
    try:
        # Install Kubernetes 1-Click Applications
        install_kubernetes_application_response = await digitalocean.1_click_applications.ainstall_kubernetes_application(
            addon_slugs=["kube-state-metrics", "loki"],
            cluster_uuid="50a994b6-c303-438f-9495-7e896cfe6b08",
        )
        print(install_kubernetes_application_response)
    except ApiException as e:
        print("Exception when calling Model1ClickApplicationsApi.install_kubernetes_application: %s\n" % e)
        pprint(e.body)
        pprint(e.headers)
        pprint(e.status)
        pprint(e.reason)
        pprint(e.round_trip_time)

asyncio.run(main())
```

## Raw HTTP Response<a id="raw-http-response"></a>

To access raw HTTP response values, use the `.raw` namespace.

```python
from pprint import pprint
from digital_ocean_python_sdk import DigitalOcean, ApiException

digitalocean = DigitalOcean(

    access_token = 'YOUR_BEARER_TOKEN'
)

try:
    # Install Kubernetes 1-Click Applications
    install_kubernetes_application_response = digitalocean.1_click_applications.raw.install_kubernetes_application(
        addon_slugs=["kube-state-metrics", "loki"],
        cluster_uuid="50a994b6-c303-438f-9495-7e896cfe6b08",
    )
    pprint(install_kubernetes_application_response.body)
    pprint(install_kubernetes_application_response.body["message"])
    pprint(install_kubernetes_application_response.headers)
    pprint(install_kubernetes_application_response.status)
    pprint(install_kubernetes_application_response.round_trip_time)
except ApiException as e:
    print("Exception when calling Model1ClickApplicationsApi.install_kubernetes_application: %s\n" % e)
    pprint(e.body)
    pprint(e.headers)
    pprint(e.status)
    pprint(e.reason)
    pprint(e.round_trip_time)
```


## Reference<a id="reference"></a>
### `digitalocean.1_click_applications.install_kubernetes_application`<a id="digitalocean1_click_applicationsinstall_kubernetes_application"></a>

To install a Kubernetes 1-Click application on a cluster, send a POST request to
`/v2/1-clicks/kubernetes`. The `addon_slugs` and `cluster_uuid` must be provided as body
parameter in order to specify which 1-Click application(s) to install. To list all available
1-Click Kubernetes applications, send a request to `/v2/1-clicks?type=kubernetes`.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
install_kubernetes_application_response = digitalocean.1_click_applications.install_kubernetes_application(
    addon_slugs=["kube-state-metrics", "loki"],
    cluster_uuid="50a994b6-c303-438f-9495-7e896cfe6b08",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### addon_slugs: [`OneClicksCreateAddonSlugs`](./digital_ocean_python_sdk/type/one_clicks_create_addon_slugs.py)<a id="addon_slugs-oneclickscreateaddonslugsdigital_ocean_python_sdktypeone_clicks_create_addon_slugspy"></a>

##### cluster_uuid: `str`<a id="cluster_uuid-str"></a>

A unique ID for the Kubernetes cluster to which the 1-Click Applications will be installed.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`OneClicksCreate`](./digital_ocean_python_sdk/type/one_clicks_create.py)
#### 🔄 Return<a id="🔄-return"></a>

[`Model1ClickApplicationsInstallKubernetesApplicationResponse`](./digital_ocean_python_sdk/pydantic/model1_click_applications_install_kubernetes_application_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/1-clicks/kubernetes` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.1_click_applications.list`<a id="digitalocean1_click_applicationslist"></a>

To list all available 1-Click applications, send a GET request to `/v2/1-clicks`. The `type` may
be provided as query paramater in order to restrict results to a certain type of 1-Click, for
example: `/v2/1-clicks?type=droplet`. Current supported types are `kubernetes` and `droplet`.

The response will be a JSON object with a key called `1_clicks`. This will be set to an array of
1-Click application data, each of which will contain the the slug and type for the 1-Click.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = digitalocean.1_click_applications.list(
    type="kubernetes",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### type: `str`<a id="type-str"></a>

Restrict results to a certain type of 1-Click.

#### 🔄 Return<a id="🔄-return"></a>

[`OneClicksListResponse`](./digital_ocean_python_sdk/pydantic/one_clicks_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/1-clicks` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.account.get`<a id="digitaloceanaccountget"></a>

To show information about the current user account, send a GET request to `/v2/account`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_response = digitalocean.account.get()
```

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/account` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.actions.get`<a id="digitaloceanactionsget"></a>

To retrieve a specific action object, send a GET request to `/v2/actions/$ACTION_ID`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_response = digitalocean.actions.get(
    action_id=36804636,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### action_id: `int`<a id="action_id-int"></a>

A unique numeric ID that can be used to identify and reference an action.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/actions/{action_id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.actions.list`<a id="digitaloceanactionslist"></a>

This will be the entire list of actions taken on your account, so it will be quite large. As with any large collection returned by the API, the results will be paginated with only 20 on each page by default.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = digitalocean.actions.list(
    per_page=2,
    page=1,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### per_page: `int`<a id="per_page-int"></a>

Number of items returned per page

##### page: `int`<a id="page-int"></a>

Which 'page' of paginated results to return.

#### 🔄 Return<a id="🔄-return"></a>

[`ActionsListResponse`](./digital_ocean_python_sdk/pydantic/actions_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/actions` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.apps.cancel_deployment`<a id="digitaloceanappscancel_deployment"></a>

Immediately cancel an in-progress deployment.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
cancel_deployment_response = digitalocean.apps.cancel_deployment(
    app_id="4f6c71e2-1e90-4762-9fee-6cc4a0a9f2cf",
    deployment_id="3aa4d20e-5527-4c00-b496-601fbd22520a",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### app_id: `str`<a id="app_id-str"></a>

The app ID

##### deployment_id: `str`<a id="deployment_id-str"></a>

The deployment ID

#### 🔄 Return<a id="🔄-return"></a>

[`AppsDeploymentResponse`](./digital_ocean_python_sdk/pydantic/apps_deployment_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/apps/{app_id}/deployments/{deployment_id}/cancel` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.apps.commit_rollback`<a id="digitaloceanappscommit_rollback"></a>

Commit an app rollback. This action permanently applies the rollback and unpins the app to resume new deployments.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.apps.commit_rollback(
    app_id="4f6c71e2-1e90-4762-9fee-6cc4a0a9f2cf",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### app_id: `str`<a id="app_id-str"></a>

The app ID

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/apps/{app_id}/rollback/commit` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.apps.create`<a id="digitaloceanappscreate"></a>

Create a new app by submitting an app specification. For documentation on app specifications (`AppSpec` objects), please refer to [the product documentation](https://docs.digitalocean.com/products/app-platform/reference/app-spec/).

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_response = digitalocean.apps.create(
    spec={
        "name": "web-app-01",
        "region": "nyc",
    },
    project_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### spec: [`AppSpec`](./digital_ocean_python_sdk/type/app_spec.py)<a id="spec-appspecdigital_ocean_python_sdktypeapp_specpy"></a>


##### project_id: `str`<a id="project_id-str"></a>

The ID of the project the app should be assigned to. If omitted, it will be assigned to your default project.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`AppsCreateAppRequest`](./digital_ocean_python_sdk/type/apps_create_app_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`AppResponse`](./digital_ocean_python_sdk/pydantic/app_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/apps` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.apps.create_deployment`<a id="digitaloceanappscreate_deployment"></a>

Creating an app deployment will pull the latest changes from your repository and schedule a new deployment for your app.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_deployment_response = digitalocean.apps.create_deployment(
    app_id="4f6c71e2-1e90-4762-9fee-6cc4a0a9f2cf",
    force_build=True,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### app_id: `str`<a id="app_id-str"></a>

The app ID

##### force_build: `bool`<a id="force_build-bool"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`AppsCreateDeploymentRequest`](./digital_ocean_python_sdk/type/apps_create_deployment_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`AppsDeploymentResponse`](./digital_ocean_python_sdk/pydantic/apps_deployment_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/apps/{app_id}/deployments` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.apps.delete`<a id="digitaloceanappsdelete"></a>

Delete an existing app. Once deleted, all active deployments will be permanently shut down and the app deleted. If needed, be sure to back up your app specification so that you may re-create it at a later time.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
delete_response = digitalocean.apps.delete(
    id="4f6c71e2-1e90-4762-9fee-6cc4a0a9f2cf",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

The ID of the app

#### 🔄 Return<a id="🔄-return"></a>

[`AppsDeleteAppResponse`](./digital_ocean_python_sdk/pydantic/apps_delete_app_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/apps/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.apps.get`<a id="digitaloceanappsget"></a>

Retrieve details about an existing app by either its ID or name. To retrieve an app by its name, do not include an ID in the request path. Information about the current active deployment as well as any in progress ones will also be included in the response.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_response = digitalocean.apps.get(
    id="4f6c71e2-1e90-4762-9fee-6cc4a0a9f2cf",
    name="myApp",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

The ID of the app

##### name: `str`<a id="name-str"></a>

The name of the app to retrieve.

#### 🔄 Return<a id="🔄-return"></a>

[`AppResponse`](./digital_ocean_python_sdk/pydantic/app_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/apps/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.apps.get_active_deployment_logs`<a id="digitaloceanappsget_active_deployment_logs"></a>

Retrieve the logs of the active deployment if one exists. The response will include links to either real-time logs of an in-progress or active deployment or archived logs of a past deployment. Note log_type=BUILD logs will return logs associated with the current active deployment (being served). To view build logs associated with in-progress build, the query must explicitly reference the deployment id.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_active_deployment_logs_response = digitalocean.apps.get_active_deployment_logs(
    app_id="4f6c71e2-1e90-4762-9fee-6cc4a0a9f2cf",
    component_name="component",
    type="BUILD",
    follow=True,
    pod_connection_timeout="3m",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### app_id: `str`<a id="app_id-str"></a>

The app ID

##### component_name: `str`<a id="component_name-str"></a>

An optional component name. If set, logs will be limited to this component only.

##### type: `str`<a id="type-str"></a>

The type of logs to retrieve - BUILD: Build-time logs - DEPLOY: Deploy-time logs - RUN: Live run-time logs - RUN_RESTARTED: Logs of crashed/restarted instances during runtime

##### follow: `bool`<a id="follow-bool"></a>

Whether the logs should follow live updates.

##### pod_connection_timeout: `str`<a id="pod_connection_timeout-str"></a>

An optional time duration to wait if the underlying component instance is not immediately available. Default: `3m`.

#### 🔄 Return<a id="🔄-return"></a>

[`AppsGetLogsResponse`](./digital_ocean_python_sdk/pydantic/apps_get_logs_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/apps/{app_id}/components/{component_name}/logs` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.apps.get_active_deployment_logs_0`<a id="digitaloceanappsget_active_deployment_logs_0"></a>

Retrieve the logs of the active deployment if one exists. The response will include links to either real-time logs of an in-progress or active deployment or archived logs of a past deployment. Note log_type=BUILD logs will return logs associated with the current active deployment (being served). To view build logs associated with in-progress build, the query must explicitly reference the deployment id.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_active_deployment_logs_0_response = digitalocean.apps.get_active_deployment_logs_0(
    app_id="4f6c71e2-1e90-4762-9fee-6cc4a0a9f2cf",
    type="BUILD",
    follow=True,
    pod_connection_timeout="3m",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### app_id: `str`<a id="app_id-str"></a>

The app ID

##### type: `str`<a id="type-str"></a>

The type of logs to retrieve - BUILD: Build-time logs - DEPLOY: Deploy-time logs - RUN: Live run-time logs - RUN_RESTARTED: Logs of crashed/restarted instances during runtime

##### follow: `bool`<a id="follow-bool"></a>

Whether the logs should follow live updates.

##### pod_connection_timeout: `str`<a id="pod_connection_timeout-str"></a>

An optional time duration to wait if the underlying component instance is not immediately available. Default: `3m`.

#### 🔄 Return<a id="🔄-return"></a>

[`AppsGetLogsResponse`](./digital_ocean_python_sdk/pydantic/apps_get_logs_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/apps/{app_id}/logs` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.apps.get_aggregate_deployment_logs`<a id="digitaloceanappsget_aggregate_deployment_logs"></a>

Retrieve the logs of a past, in-progress, or active deployment. If a component name is specified, the logs will be limited to only that component. The response will include links to either real-time logs of an in-progress or active deployment or archived logs of a past deployment.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_aggregate_deployment_logs_response = digitalocean.apps.get_aggregate_deployment_logs(
    app_id="4f6c71e2-1e90-4762-9fee-6cc4a0a9f2cf",
    deployment_id="3aa4d20e-5527-4c00-b496-601fbd22520a",
    type="BUILD",
    follow=True,
    pod_connection_timeout="3m",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### app_id: `str`<a id="app_id-str"></a>

The app ID

##### deployment_id: `str`<a id="deployment_id-str"></a>

The deployment ID

##### type: `str`<a id="type-str"></a>

The type of logs to retrieve - BUILD: Build-time logs - DEPLOY: Deploy-time logs - RUN: Live run-time logs - RUN_RESTARTED: Logs of crashed/restarted instances during runtime

##### follow: `bool`<a id="follow-bool"></a>

Whether the logs should follow live updates.

##### pod_connection_timeout: `str`<a id="pod_connection_timeout-str"></a>

An optional time duration to wait if the underlying component instance is not immediately available. Default: `3m`.

#### 🔄 Return<a id="🔄-return"></a>

[`AppsGetLogsResponse`](./digital_ocean_python_sdk/pydantic/apps_get_logs_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/apps/{app_id}/deployments/{deployment_id}/logs` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.apps.get_app_daily_bandwidth_metrics`<a id="digitaloceanappsget_app_daily_bandwidth_metrics"></a>

Retrieve daily bandwidth usage metrics for a single app.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_app_daily_bandwidth_metrics_response = digitalocean.apps.get_app_daily_bandwidth_metrics(
    app_id="4f6c71e2-1e90-4762-9fee-6cc4a0a9f2cf",
    date="2023-01-17T00:00:00Z",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### app_id: `str`<a id="app_id-str"></a>

The app ID

##### date: `datetime`<a id="date-datetime"></a>

Optional day to query. Only the date component of the timestamp will be considered. Default: yesterday.

#### 🔄 Return<a id="🔄-return"></a>

[`AppMetricsBandwidthUsage`](./digital_ocean_python_sdk/pydantic/app_metrics_bandwidth_usage.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/apps/{app_id}/metrics/bandwidth_daily` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.apps.get_deployment_info`<a id="digitaloceanappsget_deployment_info"></a>

Retrieve information about an app deployment.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_deployment_info_response = digitalocean.apps.get_deployment_info(
    app_id="4f6c71e2-1e90-4762-9fee-6cc4a0a9f2cf",
    deployment_id="3aa4d20e-5527-4c00-b496-601fbd22520a",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### app_id: `str`<a id="app_id-str"></a>

The app ID

##### deployment_id: `str`<a id="deployment_id-str"></a>

The deployment ID

#### 🔄 Return<a id="🔄-return"></a>

[`AppsDeploymentResponse`](./digital_ocean_python_sdk/pydantic/apps_deployment_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/apps/{app_id}/deployments/{deployment_id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.apps.get_deployment_logs`<a id="digitaloceanappsget_deployment_logs"></a>

Retrieve the logs of a past, in-progress, or active deployment. The response will include links to either real-time logs of an in-progress or active deployment or archived logs of a past deployment.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_deployment_logs_response = digitalocean.apps.get_deployment_logs(
    app_id="4f6c71e2-1e90-4762-9fee-6cc4a0a9f2cf",
    deployment_id="3aa4d20e-5527-4c00-b496-601fbd22520a",
    component_name="component",
    type="BUILD",
    follow=True,
    pod_connection_timeout="3m",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### app_id: `str`<a id="app_id-str"></a>

The app ID

##### deployment_id: `str`<a id="deployment_id-str"></a>

The deployment ID

##### component_name: `str`<a id="component_name-str"></a>

An optional component name. If set, logs will be limited to this component only.

##### type: `str`<a id="type-str"></a>

The type of logs to retrieve - BUILD: Build-time logs - DEPLOY: Deploy-time logs - RUN: Live run-time logs - RUN_RESTARTED: Logs of crashed/restarted instances during runtime

##### follow: `bool`<a id="follow-bool"></a>

Whether the logs should follow live updates.

##### pod_connection_timeout: `str`<a id="pod_connection_timeout-str"></a>

An optional time duration to wait if the underlying component instance is not immediately available. Default: `3m`.

#### 🔄 Return<a id="🔄-return"></a>

[`AppsGetLogsResponse`](./digital_ocean_python_sdk/pydantic/apps_get_logs_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/apps/{app_id}/deployments/{deployment_id}/components/{component_name}/logs` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.apps.get_instance_size`<a id="digitaloceanappsget_instance_size"></a>

Retrieve information about a specific instance size for `service`, `worker`, and `job` components.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_instance_size_response = digitalocean.apps.get_instance_size(
    slug="basic-xxs",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### slug: `str`<a id="slug-str"></a>

The slug of the instance size

#### 🔄 Return<a id="🔄-return"></a>

[`AppsGetInstanceSizeResponse`](./digital_ocean_python_sdk/pydantic/apps_get_instance_size_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/apps/tiers/instance_sizes/{slug}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.apps.get_multiple_daily_metrics`<a id="digitaloceanappsget_multiple_daily_metrics"></a>

Retrieve daily bandwidth usage metrics for multiple apps.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_multiple_daily_metrics_response = digitalocean.apps.get_multiple_daily_metrics(
    app_ids=["4f6c71e2-1e90-4762-9fee-6cc4a0a9f2cf", "c2a93513-8d9b-4223-9d61-5e7272c81cf5"],
    date="2023-01-17T00:00:00Z",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### app_ids: [`AppMetricsBandwidthUsageRequestAppIds`](./digital_ocean_python_sdk/type/app_metrics_bandwidth_usage_request_app_ids.py)<a id="app_ids-appmetricsbandwidthusagerequestappidsdigital_ocean_python_sdktypeapp_metrics_bandwidth_usage_request_app_idspy"></a>

##### date: `datetime`<a id="date-datetime"></a>

Optional day to query. Only the date component of the timestamp will be considered. Default: yesterday.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`AppMetricsBandwidthUsageRequest`](./digital_ocean_python_sdk/type/app_metrics_bandwidth_usage_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`AppMetricsBandwidthUsage`](./digital_ocean_python_sdk/pydantic/app_metrics_bandwidth_usage.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/apps/metrics/bandwidth_daily` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.apps.get_tier_info`<a id="digitaloceanappsget_tier_info"></a>

Retrieve information about a specific app tier.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_tier_info_response = digitalocean.apps.get_tier_info(
    slug="basic",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### slug: `str`<a id="slug-str"></a>

The slug of the tier

#### 🔄 Return<a id="🔄-return"></a>

[`AppsGetTierResponse`](./digital_ocean_python_sdk/pydantic/apps_get_tier_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/apps/tiers/{slug}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.apps.list`<a id="digitaloceanappslist"></a>

List all apps on your account. Information about the current active deployment as well as any in progress ones will also be included for each app.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = digitalocean.apps.list(
    page=1,
    per_page=2,
    with_projects=True,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### page: `int`<a id="page-int"></a>

Which 'page' of paginated results to return.

##### per_page: `int`<a id="per_page-int"></a>

Number of items returned per page

##### with_projects: `bool`<a id="with_projects-bool"></a>

Whether the project_id of listed apps should be fetched and included.

#### 🔄 Return<a id="🔄-return"></a>

[`AppsResponse`](./digital_ocean_python_sdk/pydantic/apps_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/apps` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.apps.list_alerts`<a id="digitaloceanappslist_alerts"></a>

List alerts associated to the app and any components. This includes configuration information about the alerts including emails, slack webhooks, and triggering events or conditions.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_alerts_response = digitalocean.apps.list_alerts(
    app_id="4f6c71e2-1e90-4762-9fee-6cc4a0a9f2cf",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### app_id: `str`<a id="app_id-str"></a>

The app ID

#### 🔄 Return<a id="🔄-return"></a>

[`AppsListAlertsResponse`](./digital_ocean_python_sdk/pydantic/apps_list_alerts_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/apps/{app_id}/alerts` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.apps.list_deployments`<a id="digitaloceanappslist_deployments"></a>

List all deployments of an app.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_deployments_response = digitalocean.apps.list_deployments(
    app_id="4f6c71e2-1e90-4762-9fee-6cc4a0a9f2cf",
    page=1,
    per_page=2,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### app_id: `str`<a id="app_id-str"></a>

The app ID

##### page: `int`<a id="page-int"></a>

Which 'page' of paginated results to return.

##### per_page: `int`<a id="per_page-int"></a>

Number of items returned per page

#### 🔄 Return<a id="🔄-return"></a>

[`AppsDeploymentsResponse`](./digital_ocean_python_sdk/pydantic/apps_deployments_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/apps/{app_id}/deployments` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.apps.list_instance_sizes`<a id="digitaloceanappslist_instance_sizes"></a>

List all instance sizes for `service`, `worker`, and `job` components.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_instance_sizes_response = digitalocean.apps.list_instance_sizes()
```

#### 🔄 Return<a id="🔄-return"></a>

[`AppsListInstanceSizesResponse`](./digital_ocean_python_sdk/pydantic/apps_list_instance_sizes_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/apps/tiers/instance_sizes` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.apps.list_regions`<a id="digitaloceanappslist_regions"></a>

List all regions supported by App Platform.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_regions_response = digitalocean.apps.list_regions()
```

#### 🔄 Return<a id="🔄-return"></a>

[`AppsListRegionsResponse`](./digital_ocean_python_sdk/pydantic/apps_list_regions_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/apps/regions` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.apps.list_tiers`<a id="digitaloceanappslist_tiers"></a>

List all app tiers.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_tiers_response = digitalocean.apps.list_tiers()
```

#### 🔄 Return<a id="🔄-return"></a>

[`AppsListTiersResponse`](./digital_ocean_python_sdk/pydantic/apps_list_tiers_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/apps/tiers` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.apps.propose_app_spec`<a id="digitaloceanappspropose_app_spec"></a>

To propose and validate a spec for a new or existing app, send a POST request to the `/v2/apps/propose` endpoint. The request returns some information about the proposed app, including app cost and upgrade cost. If an existing app ID is specified, the app spec is treated as a proposed update to the existing app.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
propose_app_spec_response = digitalocean.apps.propose_app_spec(
    spec={
        "name": "web-app-01",
        "region": "nyc",
    },
    app_id="b6bdf840-2854-4f87-a36c-5f231c617c84",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### spec: [`AppSpec`](./digital_ocean_python_sdk/type/app_spec.py)<a id="spec-appspecdigital_ocean_python_sdktypeapp_specpy"></a>


##### app_id: `str`<a id="app_id-str"></a>

An optional ID of an existing app. If set, the spec will be treated as a proposed update to the specified app. The existing app is not modified using this method.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`AppPropose`](./digital_ocean_python_sdk/type/app_propose.py)
#### 🔄 Return<a id="🔄-return"></a>

[`AppProposeResponse`](./digital_ocean_python_sdk/pydantic/app_propose_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/apps/propose` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.apps.revert_rollback`<a id="digitaloceanappsrevert_rollback"></a>

Revert an app rollback. This action reverts the active rollback by creating a new deployment from the
latest app spec prior to the rollback and unpins the app to resume new deployments.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
revert_rollback_response = digitalocean.apps.revert_rollback(
    app_id="4f6c71e2-1e90-4762-9fee-6cc4a0a9f2cf",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### app_id: `str`<a id="app_id-str"></a>

The app ID

#### 🔄 Return<a id="🔄-return"></a>

[`AppsDeploymentResponse`](./digital_ocean_python_sdk/pydantic/apps_deployment_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/apps/{app_id}/rollback/revert` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.apps.rollback_deployment`<a id="digitaloceanappsrollback_deployment"></a>

Rollback an app to a previous deployment. A new deployment will be created to perform the rollback.
The app will be pinned to the rollback deployment preventing any new deployments from being created,
either manually or through Auto Deploy on Push webhooks. To resume deployments, the rollback must be
either committed or reverted.

It is recommended to use the Validate App Rollback endpoint to double check if the rollback is
valid and if there are any warnings.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
rollback_deployment_response = digitalocean.apps.rollback_deployment(
    app_id="4f6c71e2-1e90-4762-9fee-6cc4a0a9f2cf",
    deployment_id="3aa4d20e-5527-4c00-b496-601fbd22520a",
    skip_pin=False,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### app_id: `str`<a id="app_id-str"></a>

The app ID

##### deployment_id: `str`<a id="deployment_id-str"></a>

The ID of the deployment to rollback to.

##### skip_pin: `bool`<a id="skip_pin-bool"></a>

Whether to skip pinning the rollback deployment. If false, the rollback deployment will be pinned and any new deployments including Auto Deploy on Push hooks will be disabled until the rollback is either manually committed or reverted via the CommitAppRollback or RevertAppRollback endpoints respectively. If true, the rollback will be immediately committed and the app will remain unpinned.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`AppsRollbackAppRequest`](./digital_ocean_python_sdk/type/apps_rollback_app_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`AppsDeploymentResponse`](./digital_ocean_python_sdk/pydantic/apps_deployment_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/apps/{app_id}/rollback` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.apps.update`<a id="digitaloceanappsupdate"></a>

Update an existing app by submitting a new app specification. For documentation on app specifications (`AppSpec` objects), please refer to [the product documentation](https://docs.digitalocean.com/products/app-platform/reference/app-spec/).

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_response = digitalocean.apps.update(
    spec={
        "name": "web-app-01",
        "region": "nyc",
    },
    id="4f6c71e2-1e90-4762-9fee-6cc4a0a9f2cf",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### spec: [`AppSpec`](./digital_ocean_python_sdk/type/app_spec.py)<a id="spec-appspecdigital_ocean_python_sdktypeapp_specpy"></a>


##### id: `str`<a id="id-str"></a>

The ID of the app

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`AppsUpdateAppRequest`](./digital_ocean_python_sdk/type/apps_update_app_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`AppResponse`](./digital_ocean_python_sdk/pydantic/app_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/apps/{id}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.apps.update_destinations_for_alerts`<a id="digitaloceanappsupdate_destinations_for_alerts"></a>

Updates the emails and slack webhook destinations for app alerts. Emails must be associated to a user with access to the app.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_destinations_for_alerts_response = digitalocean.apps.update_destinations_for_alerts(
    app_id="4f6c71e2-1e90-4762-9fee-6cc4a0a9f2cf",
    alert_id="5a624ab5-dd58-4b39-b7dd-8b7c36e8a91d",
    emails=["sammy@digitalocean.com"],
    slack_webhooks=[
        {
            "url": "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX",
            "channel": "Channel Name",
        }
    ],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### app_id: `str`<a id="app_id-str"></a>

The app ID

##### alert_id: `str`<a id="alert_id-str"></a>

The alert ID

##### emails: List[`str`]<a id="emails-liststr"></a>

##### slack_webhooks: List[`AppAlertSlackWebhook`]<a id="slack_webhooks-listappalertslackwebhook"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`AppsAssignAppAlertDestinationsRequest`](./digital_ocean_python_sdk/type/apps_assign_app_alert_destinations_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`AppsAlertResponse`](./digital_ocean_python_sdk/pydantic/apps_alert_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/apps/{app_id}/alerts/{alert_id}/destinations` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.apps.validate_rollback`<a id="digitaloceanappsvalidate_rollback"></a>

Check whether an app can be rolled back to a specific deployment. This endpoint can also be used
to check if there are any warnings or validation conditions that will cause the rollback to proceed
under unideal circumstances. For example, if a component must be rebuilt as part of the rollback
causing it to take longer than usual.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
validate_rollback_response = digitalocean.apps.validate_rollback(
    app_id="4f6c71e2-1e90-4762-9fee-6cc4a0a9f2cf",
    deployment_id="3aa4d20e-5527-4c00-b496-601fbd22520a",
    skip_pin=False,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### app_id: `str`<a id="app_id-str"></a>

The app ID

##### deployment_id: `str`<a id="deployment_id-str"></a>

The ID of the deployment to rollback to.

##### skip_pin: `bool`<a id="skip_pin-bool"></a>

Whether to skip pinning the rollback deployment. If false, the rollback deployment will be pinned and any new deployments including Auto Deploy on Push hooks will be disabled until the rollback is either manually committed or reverted via the CommitAppRollback or RevertAppRollback endpoints respectively. If true, the rollback will be immediately committed and the app will remain unpinned.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`AppsRollbackAppRequest`](./digital_ocean_python_sdk/type/apps_rollback_app_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`AppsValidateRollbackResponse`](./digital_ocean_python_sdk/pydantic/apps_validate_rollback_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/apps/{app_id}/rollback/validate` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.billing.get`<a id="digitaloceanbillingget"></a>

To retrieve the balances on a customer's account, send a GET request to `/v2/customers/my/balance`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_response = digitalocean.billing.get()
```

#### 🔄 Return<a id="🔄-return"></a>

[`Balance`](./digital_ocean_python_sdk/pydantic/balance.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/customers/my/balance` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.billing.get_invoice_by_uuid`<a id="digitaloceanbillingget_invoice_by_uuid"></a>

To retrieve the invoice items for an invoice, send a GET request to `/v2/customers/my/invoices/$INVOICE_UUID`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_invoice_by_uuid_response = digitalocean.billing.get_invoice_by_uuid(
    invoice_uuid="22737513-0ea7-4206-8ceb-98a575af7681",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### invoice_uuid: `str`<a id="invoice_uuid-str"></a>

UUID of the invoice

#### 🔄 Return<a id="🔄-return"></a>

[`BillingGetInvoiceByUuidResponse`](./digital_ocean_python_sdk/pydantic/billing_get_invoice_by_uuid_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/customers/my/invoices/{invoice_uuid}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.billing.get_invoice_csv_by_uuid`<a id="digitaloceanbillingget_invoice_csv_by_uuid"></a>

To retrieve a CSV for an invoice, send a GET request to `/v2/customers/my/invoices/$INVOICE_UUID/csv`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_invoice_csv_by_uuid_response = digitalocean.billing.get_invoice_csv_by_uuid(
    invoice_uuid="22737513-0ea7-4206-8ceb-98a575af7681",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### invoice_uuid: `str`<a id="invoice_uuid-str"></a>

UUID of the invoice

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/customers/my/invoices/{invoice_uuid}/csv` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.billing.get_invoice_summary_by_uuid`<a id="digitaloceanbillingget_invoice_summary_by_uuid"></a>

To retrieve a summary for an invoice, send a GET request to `/v2/customers/my/invoices/$INVOICE_UUID/summary`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_invoice_summary_by_uuid_response = digitalocean.billing.get_invoice_summary_by_uuid(
    invoice_uuid="22737513-0ea7-4206-8ceb-98a575af7681",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### invoice_uuid: `str`<a id="invoice_uuid-str"></a>

UUID of the invoice

#### 🔄 Return<a id="🔄-return"></a>

[`InvoiceSummary`](./digital_ocean_python_sdk/pydantic/invoice_summary.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/customers/my/invoices/{invoice_uuid}/summary` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.billing.get_pdf_by_uuid`<a id="digitaloceanbillingget_pdf_by_uuid"></a>

To retrieve a PDF for an invoice, send a GET request to `/v2/customers/my/invoices/$INVOICE_UUID/pdf`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_pdf_by_uuid_response = digitalocean.billing.get_pdf_by_uuid(
    invoice_uuid="22737513-0ea7-4206-8ceb-98a575af7681",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### invoice_uuid: `str`<a id="invoice_uuid-str"></a>

UUID of the invoice

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/customers/my/invoices/{invoice_uuid}/pdf` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.billing.list`<a id="digitaloceanbillinglist"></a>

To retrieve a list of all billing history entries, send a GET request to `/v2/customers/my/billing_history`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = digitalocean.billing.list()
```

#### 🔄 Return<a id="🔄-return"></a>

[`BillingHistoryListResponse`](./digital_ocean_python_sdk/pydantic/billing_history_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/customers/my/billing_history` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.billing.list_0`<a id="digitaloceanbillinglist_0"></a>

To retrieve a list of all invoices, send a GET request to `/v2/customers/my/invoices`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_0_response = digitalocean.billing.list_0(
    per_page=2,
    page=1,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### per_page: `int`<a id="per_page-int"></a>

Number of items returned per page

##### page: `int`<a id="page-int"></a>

Which 'page' of paginated results to return.

#### 🔄 Return<a id="🔄-return"></a>

[`InvoicesListResponse`](./digital_ocean_python_sdk/pydantic/invoices_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/customers/my/invoices` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.block_storage.create`<a id="digitaloceanblock_storagecreate"></a>

To create a new volume, send a POST request to `/v2/volumes`. Optionally, a `filesystem_type` attribute may be provided in order to automatically format the volume's filesystem. Pre-formatted volumes are automatically mounted when attached to Ubuntu, Debian, Fedora, Fedora Atomic, and CentOS Droplets created on or after April 26, 2018. Attaching pre-formatted volumes to Droplets without support for auto-mounting is not recommended.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_response = digitalocean.block_storage.create(
    body={},
    tags=["base-image", "prod"],
    description="Block store for examples",
    id="506f78a4-e098-11e5-ad9f-000f53306ae1",
    droplet_ids=[],
    name="example",
    size_gigabytes=10,
    created_at="2020-03-02T17:00:49Z",
    snapshot_id="b0798135-fb76-11eb-946a-0a58ac146f33",
    filesystem_type="ext4",
    region="nyc3",
    filesystem_label=None,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### tags: [`TagsArray`](./digital_ocean_python_sdk/type/tags_array.py)<a id="tags-tagsarraydigital_ocean_python_sdktypetags_arraypy"></a>

##### description: `str`<a id="description-str"></a>

An optional free-form text field to describe a block storage volume.

##### id: `str`<a id="id-str"></a>

The unique identifier for the block storage volume.

##### droplet_ids: [`VolumeBaseDropletIds`](./digital_ocean_python_sdk/type/volume_base_droplet_ids.py)<a id="droplet_ids-volumebasedropletidsdigital_ocean_python_sdktypevolume_base_droplet_idspy"></a>

##### name: `str`<a id="name-str"></a>

A human-readable name for the block storage volume. Must be lowercase and be composed only of numbers, letters and \\\"-\\\", up to a limit of 64 characters. The name must begin with a letter.

##### size_gigabytes: `int`<a id="size_gigabytes-int"></a>

The size of the block storage volume in GiB (1024^3). This field does not apply  when creating a volume from a snapshot.

##### created_at: `str`<a id="created_at-str"></a>

A time value given in ISO8601 combined date and time format that represents when the block storage volume was created.

##### snapshot_id: `str`<a id="snapshot_id-str"></a>

The unique identifier for the volume snapshot from which to create the volume.

##### filesystem_type: `str`<a id="filesystem_type-str"></a>

The name of the filesystem type to be used on the volume. When provided, the volume will automatically be formatted to the specified filesystem type. Currently, the available options are `ext4` and `xfs`. Pre-formatted volumes are automatically mounted when attached to Ubuntu, Debian, Fedora, Fedora Atomic, and CentOS Droplets created on or after April 26, 2018. Attaching pre-formatted volumes to other Droplets is not recommended.

##### region: [`RegionSlug`](./digital_ocean_python_sdk/type/region_slug.py)<a id="region-regionslugdigital_ocean_python_sdktyperegion_slugpy"></a>

##### filesystem_label: Union[`str`, [`Union[bool, date, datetime, dict, float, int, list, str, None]`](./digital_ocean_python_sdk/type/typing_union_bool_date_datetime_dict_float_int_list_str_none.py)]<a id="filesystem_label-unionstr-unionbool-date-datetime-dict-float-int-list-str-nonedigital_ocean_python_sdktypetyping_union_bool_date_datetime_dict_float_int_list_str_nonepy"></a>


#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`VolumesCreateRequest`](./digital_ocean_python_sdk/type/volumes_create_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`VolumesCreateResponse`](./digital_ocean_python_sdk/pydantic/volumes_create_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/volumes` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.block_storage.create_0`<a id="digitaloceanblock_storagecreate_0"></a>

To create a snapshot from a volume, sent a POST request to `/v2/volumes/$VOLUME_ID/snapshots`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_0_response = digitalocean.block_storage.create_0(
    body=None,
    name="big-data-snapshot1475261774",
    volume_id="7724db7c-e098-11e5-b522-000f53304e51",
    tags=["base-image", "prod"],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### name: `str`<a id="name-str"></a>

A human-readable name for the volume snapshot.

##### volume_id: `str`<a id="volume_id-str"></a>

The ID of the block storage volume.

##### tags: [`TagsArray`](./digital_ocean_python_sdk/type/tags_array.py)<a id="tags-tagsarraydigital_ocean_python_sdktypetags_arraypy"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`VolumeSnapshotsCreateRequest`](./digital_ocean_python_sdk/type/volume_snapshots_create_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`BlockStorageGetSnapshotDetailsResponse`](./digital_ocean_python_sdk/pydantic/block_storage_get_snapshot_details_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/volumes/{volume_id}/snapshots` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.block_storage.delete`<a id="digitaloceanblock_storagedelete"></a>

To delete a block storage volume, destroying all data and removing it from your account, send a DELETE request to `/v2/volumes/$VOLUME_ID`.
No response body will be sent back, but the response code will indicate success. Specifically, the response code will be a 204, which means that the action was successful with no returned body data.



#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.block_storage.delete(
    volume_id="7724db7c-e098-11e5-b522-000f53304e51",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### volume_id: `str`<a id="volume_id-str"></a>

The ID of the block storage volume.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/volumes/{volume_id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.block_storage.delete_by_region_and_name`<a id="digitaloceanblock_storagedelete_by_region_and_name"></a>

Block storage volumes may also be deleted by name by sending a DELETE request with the volume's **name** and the **region slug** for the region it is located in as query parameters to `/v2/volumes?name=$VOLUME_NAME&region=nyc1`.
No response body will be sent back, but the response code will indicate success. Specifically, the response code will be a 204, which means that the action was successful with no returned body data.



#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.block_storage.delete_by_region_and_name(
    name="example",
    region="nyc3",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### name: `str`<a id="name-str"></a>

The block storage volume's name.

##### region: [`RegionSlug`](./digital_ocean_python_sdk/type/.py)<a id="region-regionslugdigital_ocean_python_sdktypepy"></a>

The slug identifier for the region where the resource is available.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/volumes` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.block_storage.delete_volume_snapshot`<a id="digitaloceanblock_storagedelete_volume_snapshot"></a>

To delete a volume snapshot, send a DELETE request to
`/v2/snapshots/$SNAPSHOT_ID`.

A status of 204 will be given. This indicates that the request was processed
successfully, but that no response body is needed.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.block_storage.delete_volume_snapshot(
    snapshot_id=6372321,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### snapshot_id: Union[`int`, `str`]<a id="snapshot_id-unionint-str"></a>


Either the ID of an existing snapshot. This will be an integer for a Droplet snapshot or a string for a volume snapshot.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/volumes/snapshots/{snapshot_id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.block_storage.get`<a id="digitaloceanblock_storageget"></a>

To show information about a block storage volume, send a GET request to `/v2/volumes/$VOLUME_ID`.



#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_response = digitalocean.block_storage.get(
    volume_id="7724db7c-e098-11e5-b522-000f53304e51",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### volume_id: `str`<a id="volume_id-str"></a>

The ID of the block storage volume.

#### 🔄 Return<a id="🔄-return"></a>

[`VolumesCreateResponse`](./digital_ocean_python_sdk/pydantic/volumes_create_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/volumes/{volume_id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.block_storage.get_snapshot_details`<a id="digitaloceanblock_storageget_snapshot_details"></a>

To retrieve the details of a snapshot that has been created from a volume, send a GET request to `/v2/volumes/snapshots/$SNAPSHOT_ID`.



#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_snapshot_details_response = digitalocean.block_storage.get_snapshot_details(
    snapshot_id=6372321,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### snapshot_id: Union[`int`, `str`]<a id="snapshot_id-unionint-str"></a>


Either the ID of an existing snapshot. This will be an integer for a Droplet snapshot or a string for a volume snapshot.

#### 🔄 Return<a id="🔄-return"></a>

[`BlockStorageGetSnapshotDetailsResponse`](./digital_ocean_python_sdk/pydantic/block_storage_get_snapshot_details_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/volumes/snapshots/{snapshot_id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.block_storage.list`<a id="digitaloceanblock_storagelist"></a>

To list all of the block storage volumes available on your account, send a GET request to `/v2/volumes`.
## Filtering Results<a id="filtering-results"></a>
### By Region<a id="by-region"></a>
The `region` may be provided as query parameter in order to restrict results to volumes available in a specific region. For example: `/v2/volumes?region=nyc1`
### By Name<a id="by-name"></a>
It is also possible to list volumes on your account that match a specified name. To do so, send a GET request with the volume's name as a query parameter to `/v2/volumes?name=$VOLUME_NAME`.
**Note:** You can only create one volume per region with the same name.
### By Name and Region<a id="by-name-and-region"></a>
It is also possible to retrieve information about a block storage volume by name. To do so, send a GET request with the volume's name and the region slug for the region it is located in as query parameters to `/v2/volumes?name=$VOLUME_NAME&region=nyc1`.




#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = digitalocean.block_storage.list(
    name="example",
    region="nyc3",
    per_page=2,
    page=1,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### name: `str`<a id="name-str"></a>

The block storage volume's name.

##### region: [`RegionSlug`](./digital_ocean_python_sdk/type/.py)<a id="region-regionslugdigital_ocean_python_sdktypepy"></a>

The slug identifier for the region where the resource is available.

##### per_page: `int`<a id="per_page-int"></a>

Number of items returned per page

##### page: `int`<a id="page-int"></a>

Which 'page' of paginated results to return.

#### 🔄 Return<a id="🔄-return"></a>

[`VolumesListResponse`](./digital_ocean_python_sdk/pydantic/volumes_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/volumes` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.block_storage.list_0`<a id="digitaloceanblock_storagelist_0"></a>

To retrieve the snapshots that have been created from a volume, send a GET request to `/v2/volumes/$VOLUME_ID/snapshots`.



#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_0_response = digitalocean.block_storage.list_0(
    volume_id="7724db7c-e098-11e5-b522-000f53304e51",
    per_page=2,
    page=1,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### volume_id: `str`<a id="volume_id-str"></a>

The ID of the block storage volume.

##### per_page: `int`<a id="per_page-int"></a>

Number of items returned per page

##### page: `int`<a id="page-int"></a>

Which 'page' of paginated results to return.

#### 🔄 Return<a id="🔄-return"></a>

[`VolumeSnapshotsListResponse`](./digital_ocean_python_sdk/pydantic/volume_snapshots_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/volumes/{volume_id}/snapshots` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.block_storage_actions.get`<a id="digitaloceanblock_storage_actionsget"></a>

To retrieve the status of a volume action, send a GET request to `/v2/volumes/$VOLUME_ID/actions/$ACTION_ID`.



#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_response = digitalocean.block_storage_actions.get(
    volume_id="7724db7c-e098-11e5-b522-000f53304e51",
    action_id=36804636,
    per_page=2,
    page=1,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### volume_id: `str`<a id="volume_id-str"></a>

The ID of the block storage volume.

##### action_id: `int`<a id="action_id-int"></a>

A unique numeric ID that can be used to identify and reference an action.

##### per_page: `int`<a id="per_page-int"></a>

Number of items returned per page

##### page: `int`<a id="page-int"></a>

Which 'page' of paginated results to return.

#### 🔄 Return<a id="🔄-return"></a>

[`VolumeActionsPostResponse`](./digital_ocean_python_sdk/pydantic/volume_actions_post_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/volumes/{volume_id}/actions/{action_id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.block_storage_actions.initiate_attach_action`<a id="digitaloceanblock_storage_actionsinitiate_attach_action"></a>

To initiate an action on a block storage volume by Id, send a POST request to
`~/v2/volumes/$VOLUME_ID/actions`. The body should contain the appropriate
attributes for the respective action.

## Attach a Block Storage Volume to a Droplet<a id="attach-a-block-storage-volume-to-a-droplet"></a>

| Attribute  | Details                                                             |
| ---------- | ------------------------------------------------------------------- |
| type       | This must be `attach`                                               |
| droplet_id | Set to the Droplet's ID                                             |
| region     | Set to the slug representing the region where the volume is located |

Each volume may only be attached to a single Droplet. However, up to seven
volumes may be attached to a Droplet at a time. Pre-formatted volumes will be
automatically mounted to Ubuntu, Debian, Fedora, Fedora Atomic, and CentOS
Droplets created on or after April 26, 2018 when attached. On older Droplets,
[additional configuration](https://www.digitalocean.com/community/tutorials/how-to-partition-and-format-digitalocean-block-storage-volumes-in-linux#mounting-the-filesystems)
is required.

## Remove a Block Storage Volume from a Droplet<a id="remove-a-block-storage-volume-from-a-droplet"></a>

| Attribute  | Details                                                             |
| ---------- | ------------------------------------------------------------------- |
| type       | This must be `detach`                                               |
| droplet_id | Set to the Droplet's ID                                             |
| region     | Set to the slug representing the region where the volume is located |

## Resize a Volume<a id="resize-a-volume"></a>

| Attribute      | Details                                                             |
| -------------- | ------------------------------------------------------------------- |
| type           | This must be `resize`                                               |
| size_gigabytes | The new size of the block storage volume in GiB (1024^3)            |
| region         | Set to the slug representing the region where the volume is located |

Volumes may only be resized upwards. The maximum size for a volume is 16TiB.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
initiate_attach_action_response = digitalocean.block_storage_actions.initiate_attach_action(
    body={},
    volume_id="7724db7c-e098-11e5-b522-000f53304e51",
    type="attach",
    region="nyc3",
    tags=["base-image", "prod"],
    droplet_id=11612190,
    size_gigabytes=1,
    per_page=2,
    page=1,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### volume_id: `str`<a id="volume_id-str"></a>

The ID of the block storage volume.

##### type: `str`<a id="type-str"></a>

The volume action to initiate.

##### region: [`RegionSlug`](./digital_ocean_python_sdk/type/region_slug.py)<a id="region-regionslugdigital_ocean_python_sdktyperegion_slugpy"></a>

##### tags: [`TagsArray`](./digital_ocean_python_sdk/type/tags_array.py)<a id="tags-tagsarraydigital_ocean_python_sdktypetags_arraypy"></a>

##### droplet_id: `int`<a id="droplet_id-int"></a>

The unique identifier for the Droplet the volume will be attached or detached from.

##### size_gigabytes: `int`<a id="size_gigabytes-int"></a>

The new size of the block storage volume in GiB (1024^3).

##### per_page: `int`<a id="per_page-int"></a>

Number of items returned per page

##### page: `int`<a id="page-int"></a>

Which 'page' of paginated results to return.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`BlockStorageActionsInitiateAttachActionRequest`](./digital_ocean_python_sdk/type/block_storage_actions_initiate_attach_action_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`VolumeActionsPostResponse`](./digital_ocean_python_sdk/pydantic/volume_actions_post_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/volumes/{volume_id}/actions` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.block_storage_actions.list`<a id="digitaloceanblock_storage_actionslist"></a>

To retrieve all actions that have been executed on a volume, send a GET request to `/v2/volumes/$VOLUME_ID/actions`.



#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = digitalocean.block_storage_actions.list(
    volume_id="7724db7c-e098-11e5-b522-000f53304e51",
    per_page=2,
    page=1,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### volume_id: `str`<a id="volume_id-str"></a>

The ID of the block storage volume.

##### per_page: `int`<a id="per_page-int"></a>

Number of items returned per page

##### page: `int`<a id="page-int"></a>

Which 'page' of paginated results to return.

#### 🔄 Return<a id="🔄-return"></a>

[`VolumeActionsListResponse`](./digital_ocean_python_sdk/pydantic/volume_actions_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/volumes/{volume_id}/actions` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.block_storage_actions.post`<a id="digitaloceanblock_storage_actionspost"></a>

To initiate an action on a block storage volume by Name, send a POST request to
`~/v2/volumes/actions`. The body should contain the appropriate
attributes for the respective action.

## Attach a Block Storage Volume to a Droplet<a id="attach-a-block-storage-volume-to-a-droplet"></a>

| Attribute   | Details                                                             |
| ----------- | ------------------------------------------------------------------- |
| type        | This must be `attach`                                               |
| volume_name | The name of the block storage volume                                |
| droplet_id  | Set to the Droplet's ID                                             |
| region      | Set to the slug representing the region where the volume is located |

Each volume may only be attached to a single Droplet. However, up to five
volumes may be attached to a Droplet at a time. Pre-formatted volumes will be
automatically mounted to Ubuntu, Debian, Fedora, Fedora Atomic, and CentOS
Droplets created on or after April 26, 2018 when attached. On older Droplets,
[additional configuration](https://www.digitalocean.com/community/tutorials/how-to-partition-and-format-digitalocean-block-storage-volumes-in-linux#mounting-the-filesystems)
is required.

## Remove a Block Storage Volume from a Droplet<a id="remove-a-block-storage-volume-from-a-droplet"></a>

| Attribute   | Details                                                             |
| ----------- | ------------------------------------------------------------------- |
| type        | This must be `detach`                                               |
| volume_name | The name of the block storage volume                                |
| droplet_id  | Set to the Droplet's ID                                             |
| region      | Set to the slug representing the region where the volume is located |


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
post_response = digitalocean.block_storage_actions.post(
    body={},
    type="attach",
    region="nyc3",
    tags=["base-image", "prod"],
    droplet_id=11612190,
    per_page=2,
    page=1,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### type: `str`<a id="type-str"></a>

The volume action to initiate.

##### region: [`RegionSlug`](./digital_ocean_python_sdk/type/region_slug.py)<a id="region-regionslugdigital_ocean_python_sdktyperegion_slugpy"></a>

##### tags: [`TagsArray`](./digital_ocean_python_sdk/type/tags_array.py)<a id="tags-tagsarraydigital_ocean_python_sdktypetags_arraypy"></a>

##### droplet_id: `int`<a id="droplet_id-int"></a>

The unique identifier for the Droplet the volume will be attached or detached from.

##### per_page: `int`<a id="per_page-int"></a>

Number of items returned per page

##### page: `int`<a id="page-int"></a>

Which 'page' of paginated results to return.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`VolumeActionsPostRequest`](./digital_ocean_python_sdk/type/volume_actions_post_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`VolumeActionsPostResponse`](./digital_ocean_python_sdk/pydantic/volume_actions_post_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/volumes/actions` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.cdn_endpoints.create_new_endpoint`<a id="digitaloceancdn_endpointscreate_new_endpoint"></a>

To create a new CDN endpoint, send a POST request to `/v2/cdn/endpoints`. The
origin attribute must be set to the fully qualified domain name (FQDN) of a
DigitalOcean Space. Optionally, the TTL may be configured by setting the `ttl`
attribute.

A custom subdomain may be configured by specifying the `custom_domain` and
`certificate_id` attributes.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_new_endpoint_response = digitalocean.cdn_endpoints.create_new_endpoint(
    origin="static-images.nyc3.digitaloceanspaces.com",
    id="892071a0-bb95-49bc-8021-3afd67a210bf",
    endpoint="static-images.nyc3.cdn.digitaloceanspaces.com",
    ttl=3600,
    certificate_id="892071a0-bb95-49bc-8021-3afd67a210bf",
    custom_domain="static.example.com",
    created_at="2018-03-21T16:02:37Z",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### origin: `str`<a id="origin-str"></a>

The fully qualified domain name (FQDN) for the origin server which provides the content for the CDN. This is currently restricted to a Space.

##### id: `str`<a id="id-str"></a>

A unique ID that can be used to identify and reference a CDN endpoint.

##### endpoint: `str`<a id="endpoint-str"></a>

The fully qualified domain name (FQDN) from which the CDN-backed content is served.

##### ttl: `int`<a id="ttl-int"></a>

The amount of time the content is cached by the CDN's edge servers in seconds. TTL must be one of 60, 600, 3600, 86400, or 604800. Defaults to 3600 (one hour) when excluded.

##### certificate_id: `str`<a id="certificate_id-str"></a>

The ID of a DigitalOcean managed TLS certificate used for SSL when a custom subdomain is provided.

##### custom_domain: `str`<a id="custom_domain-str"></a>

The fully qualified domain name (FQDN) of the custom subdomain used with the CDN endpoint.

##### created_at: `datetime`<a id="created_at-datetime"></a>

A time value given in ISO8601 combined date and time format that represents when the CDN endpoint was created.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`CdnEndpoint`](./digital_ocean_python_sdk/type/cdn_endpoint.py)
#### 🔄 Return<a id="🔄-return"></a>

[`CdnEndpointsCreateNewEndpointResponse`](./digital_ocean_python_sdk/pydantic/cdn_endpoints_create_new_endpoint_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/cdn/endpoints` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.cdn_endpoints.delete_endpoint`<a id="digitaloceancdn_endpointsdelete_endpoint"></a>

To delete a specific CDN endpoint, send a DELETE request to
`/v2/cdn/endpoints/$ENDPOINT_ID`.

A status of 204 will be given. This indicates that the request was processed
successfully, but that no response body is needed.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.cdn_endpoints.delete_endpoint(
    cdn_id="19f06b6a-3ace-4315-b086-499a0e521b76",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### cdn_id: `str`<a id="cdn_id-str"></a>

A unique identifier for a CDN endpoint.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/cdn/endpoints/{cdn_id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.cdn_endpoints.get_existing_endpoint`<a id="digitaloceancdn_endpointsget_existing_endpoint"></a>

To show information about an existing CDN endpoint, send a GET request to `/v2/cdn/endpoints/$ENDPOINT_ID`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_existing_endpoint_response = digitalocean.cdn_endpoints.get_existing_endpoint(
    cdn_id="19f06b6a-3ace-4315-b086-499a0e521b76",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### cdn_id: `str`<a id="cdn_id-str"></a>

A unique identifier for a CDN endpoint.

#### 🔄 Return<a id="🔄-return"></a>

[`CdnEndpointsCreateNewEndpointResponse`](./digital_ocean_python_sdk/pydantic/cdn_endpoints_create_new_endpoint_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/cdn/endpoints/{cdn_id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.cdn_endpoints.list_all`<a id="digitaloceancdn_endpointslist_all"></a>

To list all of the CDN endpoints available on your account, send a GET request to `/v2/cdn/endpoints`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_all_response = digitalocean.cdn_endpoints.list_all(
    per_page=2,
    page=1,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### per_page: `int`<a id="per_page-int"></a>

Number of items returned per page

##### page: `int`<a id="page-int"></a>

Which 'page' of paginated results to return.

#### 🔄 Return<a id="🔄-return"></a>

[`CdnEndpointsListAllResponse`](./digital_ocean_python_sdk/pydantic/cdn_endpoints_list_all_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/cdn/endpoints` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.cdn_endpoints.purge_cache`<a id="digitaloceancdn_endpointspurge_cache"></a>

To purge cached content from a CDN endpoint, send a DELETE request to
`/v2/cdn/endpoints/$ENDPOINT_ID/cache`. The body of the request should include
a `files` attribute containing a list of cached file paths to be purged. A
path may be for a single file or may contain a wildcard (`*`) to recursively
purge all files under a directory. When only a wildcard is provided, all
cached files will be purged. There is a rate limit of 50 files per 20 seconds 
that can be purged.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.cdn_endpoints.purge_cache(
    files=["path/to/image.png", "path/to/css/*"],
    cdn_id="19f06b6a-3ace-4315-b086-499a0e521b76",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### files: [`PurgeCacheFiles`](./digital_ocean_python_sdk/type/purge_cache_files.py)<a id="files-purgecachefilesdigital_ocean_python_sdktypepurge_cache_filespy"></a>

##### cdn_id: `str`<a id="cdn_id-str"></a>

A unique identifier for a CDN endpoint.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`PurgeCache`](./digital_ocean_python_sdk/type/purge_cache.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/cdn/endpoints/{cdn_id}/cache` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.cdn_endpoints.update_endpoint`<a id="digitaloceancdn_endpointsupdate_endpoint"></a>

To update the TTL, certificate ID, or the FQDN of the custom subdomain for
an existing CDN endpoint, send a PUT request to
`/v2/cdn/endpoints/$ENDPOINT_ID`.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_endpoint_response = digitalocean.cdn_endpoints.update_endpoint(
    cdn_id="19f06b6a-3ace-4315-b086-499a0e521b76",
    ttl=3600,
    certificate_id="892071a0-bb95-49bc-8021-3afd67a210bf",
    custom_domain="static.example.com",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### cdn_id: `str`<a id="cdn_id-str"></a>

A unique identifier for a CDN endpoint.

##### ttl: `int`<a id="ttl-int"></a>

The amount of time the content is cached by the CDN's edge servers in seconds. TTL must be one of 60, 600, 3600, 86400, or 604800. Defaults to 3600 (one hour) when excluded.

##### certificate_id: `str`<a id="certificate_id-str"></a>

The ID of a DigitalOcean managed TLS certificate used for SSL when a custom subdomain is provided.

##### custom_domain: `str`<a id="custom_domain-str"></a>

The fully qualified domain name (FQDN) of the custom subdomain used with the CDN endpoint.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`UpdateEndpoint`](./digital_ocean_python_sdk/type/update_endpoint.py)
#### 🔄 Return<a id="🔄-return"></a>

[`CdnEndpointsCreateNewEndpointResponse`](./digital_ocean_python_sdk/pydantic/cdn_endpoints_create_new_endpoint_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/cdn/endpoints/{cdn_id}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.certificates.create`<a id="digitaloceancertificatescreate"></a>

To upload new SSL certificate which you have previously generated, send a POST
request to `/v2/certificates`.

When uploading a user-generated certificate, the `private_key`,
`leaf_certificate`, and optionally the `certificate_chain` attributes should
be provided. The type must be set to `custom`.

When using Let's Encrypt to create a certificate, the `dns_names` attribute
must be provided, and the type must be set to `lets_encrypt`.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_response = digitalocean.certificates.create(
    body=None,
    name="web-cert-01",
    type="lets_encrypt",
    dns_names=["www.example.com", "example.com"],
    private_key="-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDBIZMz8pnK6V52\nSVf+CYssOfCQHAx5f0Ou5rYbq3xNh8VHAIYJCQ1QxQIxKSP6+uODSYrb2KWyurP1\nDwGb8OYm0J3syEDtCUQik1cpCzpeNlAZ2f8FzXyYQAqPopxdRpsFz8DtZnVvu86X\nwrE4oFPl9MReICmZfBNWylpV5qgFPoXyJ70ZAsTm3cEe3n+LBXEnY4YrVDRWxA3w\nZ2mzZ03HZ1hHrxK9CMnS829U+8sK+UneZpCO7yLRPuxwhmps0wpK/YuZZfRAKF1F\nZRnak/SIQ28rnWufmdg16YqqHgl5JOgnb3aslKRvL4dI2Gwnkd2IHtpZnTR0gxFX\nfqqbQwuRAgMBAAECggEBAILLmkW0JzOkmLTDNzR0giyRkLoIROqDpfLtjKdwm95l\n9NUBJcU4vCvXQITKt/NhtnNTexcowg8pInb0ksJpg3UGE+4oMNBXVi2UW5MQZ5cm\ncVkQqgXkBF2YAY8FMaB6EML+0En2+dGR/3gIAr221xsFiXe1kHbB8Nb2c/d5HpFt\neRpLVJnK+TxSr78PcZA8DDGlSgwvgimdAaFUNO2OqB9/0E9UPyKk2ycdff/Z6ldF\n0hkCLtdYTTl8Kf/OwjcuTgmA2O3Y8/CoQX/L+oP9Rvt9pWCEfuebiOmHJVPO6Y6x\ngtQVEXwmF1pDHH4Qtz/e6UZTdYeMl9G4aNO2CawwcaYECgYEA57imgSOG4XsJLRh\nGGncV9R/xhy4AbDWLtAMzQRX4ktvKCaHWyQV2XK2we/cu29NLv2Y89WmerTNPOU+\nP8+pB31uty2ELySVn15QhKpQClVEAlxCnnNjXYrii5LOM80+lVmxvQwxVd8Yz8nj\nIntyioXNBEnYS7V2RxxFGgFun1cCgYEA1V3W+Uyamhq8JS5EY0FhyGcXdHd70K49\nW1ou7McIpncf9tM9acLS1hkI98rd2T69Zo8mKoV1V2hjFaKUYfNys6tTkYWeZCcJ\n3rW44j9DTD+FmmjcX6b8DzfybGLehfNbCw6n67/r45DXIV/fk6XZfkx6IEGO4ODt\nNfnvx4TuI1cCgYBACDiKqwSUvmkUuweOo4IuCxyb5Ee8v98P5JIE/VRDxlCbKbpx\npxEam6aBBQVcDi+n8o0H3WjjlKc6UqbW/01YMoMrvzotxNBLz8Y0QtQHZvR6KoCG\nRKCKstxTcWflzKuknbqN4RapAhNbKBDJ8PMSWfyDWNyaXzSmBdvaidbF1QKBgDI0\no4oD0Xkjg1QIYAUu9FBQmb9JAjRnW36saNBEQS/SZg4RRKknM683MtoDvVIKJk0E\nsAlfX+4SXQZRPDMUMtA+Jyrd0xhj6zmhbwClvDMr20crF3fWdgcqtft1BEFmsuyW\nJUMe5OWmRkjPI2+9ncDPRAllA7a8lnSV/Crph5N/AoGBAIK249temKrGe9pmsmAo\nQbNuYSmwpnMoAqdHTrl70HEmK7ob6SIVmsR8QFAkH7xkYZc4Bxbx4h1bdpozGB+/\nAangbiaYJcAOD1QyfiFbflvI1RFeHgrk7VIafeSeQv6qu0LLMi2zUbpgVzxt78Wg\neTuK2xNR0PIM8OI7pRpgyj1I\n-----END PRIVATE KEY-----",
    leaf_certificate="-----BEGIN CERTIFICATE-----\nMIIFFjCCA/6gAwIBAgISA0AznUJmXhu08/89ZuSPC/kRMA0GCSqGSIb3DQEBCwUA\nMEoxCzAJBgNVBAYTAlVTMRYwFAYDVQQKEw1MZXQncyBFbmNyeXB0MSMwIQYDVQQD\nExpMZXQncyBFbmNyeXB0IEF1dGhvcml0eSBYMzAeFw0xNjExMjQwMDIzMDBaFw0x\nNzAyMjIwMDIzMDBaMCQxIjAgBgNVBAMTGWNsb3VkLmFuZHJld3NvbWV0aGluZy5j\nb20wggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDBIZMz8pnK6V52SVf+\nCYssOfCQHAx5f0Ou5rYbq3xNh8VWHIYJCQ1QxQIxKSP6+uODSYrb2KWyurP1DwGb\n8OYm0J3syEDtCUQik1cpCzpeNlAZ2f8FzXyYQAqPopxdRpsFz8DtZnVvu86XwrE4\noFPl9MReICmZfBNWylpV5qgFPoXyJ70ZAsTm3cEe3n+LBXEnY4YrVDRWxA3wZ2mz\nZ03HZ1hHrxK9CMnS829U+8sK+UneZpCO7yLRPuxwhmps0wpK/YuZZfRAKF1FZRna\nk/SIQ28rnWufmdg16YqqHgl5JOgnb3aslKRvL4dI2Gwnkd2IHtpZnTR0gxFXfqqb\nQwuRAgMBAAGjggIaMIICFjAOBgNVHQ8BAf8EBAMCBaAwHQYDVR0lBBYwFAYIKwYB\nBQUHAwEGCCsGAQUFBwMCMAwGA1UdEwEB/wQCMAAwHQYDVR0OBBYEFLsAFcxAhFX1\nMbCnzr9hEO5rL4jqMB8GA1UdIwQYMBaAFKhKamMEfd265tE5t6ZFZe/zqOyhMHAG\nCCsGAQUFBwEBBGQwYjAvBggrBgEFBQcwAYYjaHR0cDovL29jc3AuaW50LXgzLmxl\ndHNlbmNyeXB0Lm9yZy8wLwYIKwYBBQUHMAKGI2h0dHA6Ly9jZXJ0LmludC14My5s\nZXRzZW5jcnlwdC5vcmcvMCQGA1UdEQQdMBuCGWNsb3VkLmFuZHJld3NvbWV0aGlu\nZy5jb20wgf4GA1UdIASB9jCB8zAIBgZngQwBAgWrgeYGCysGAQQBgt8TAQEBMIHW\nMCYGCCsGAQUFBwIBFhpodHRwOi8vY3BzLmxldHNlbmNyeXB0Lm9yZzCBqwYIKwYB\nBQUHAgIwgZ4MgZtUaGlzIENlcnRpZmljYXRlIG1heSBvbmx5IGJlIHJlbGllZCB1\ncG9uIGJ5IFJlbHlpbmcgUGFydGllcyBhbmQgb25seSQ2ziBhY2NvcmRhbmNlIHdp\ndGggdGhlIENlcnRpZmljYXRlIFBvbGljeSBmb3VuZCBhdCBodHRwczovL2xldHNl\nbmNyeXB0Lm9yZy9yZXBvc2l0b3J5LzANBgkqhkiG9w0BAQsFAAOCAQEAOZVQvrjM\nPKXLARTjB5XsgfyDN3/qwLl7SmwGkPe+B+9FJpfScYG1JzVuCj/SoaPaK34G4x/e\niXwlwOXtMOtqjQYzNu2Pr2C+I+rVmaxIrCUXFmC205IMuUBEeWXG9Y/HvXQLPabD\nD3Gdl5+Feink9SDRP7G0HaAwq13hI7ARxkL9p+UIY39X0dV3WOboW2Re8nrkFXJ7\nq9Z6shK5QgpBfsLjtjNsQzaGV3ve1gOg25aTJGearBWOvEjJNA1wGMoKVXOtYwm/\nWyWoVdCQ8HmconcbJB6xc0UZ1EjvzRr5ZIvSa5uHZD0L3m7/kpPWlAlFJ7hHASPu\nUlF1zblDmg2Iaw==\n-----END CERTIFICATE-----",
    certificate_chain="-----BEGIN CERTIFICATE-----\nMIIFFjCCA/6gAwIBAgISA0AznUJmXhu08/89ZuSPC/kRMA0GCSqGSIb3DQEBCwUA\nMEoxCzAJBgNVBAYTAlVTMRYwFAYDVQQKEw1MZXQncyBFbmNyeXB0MSMwIQYDVQQD\nExpMZXQncyBFbmNyeXB0IEF1dGhvcml0eSBYMzAeFw0xNjExMjQwMDIzMDBaFw0x\nNzAyMjIwMDIzMDBaMCQxIjAgBgNVBAMTGWNsb3VkLmFuZHJld3NvbWV0aGluZy5j\nb20wggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDBIZMz7tnK6V52SVf+\nCYssOfCQHAx5f0Ou5rYbq3xNh8VHAIYJCQ1QxQIxKSP6+uODSYrb2KWyurP1DwGb\n8OYm0J3syEDtCUQik1cpCzpeNlAZ2f8FzXyYQAqPopxdRpsFz8DtZnVvu86XwrE4\noFPl9MReICmZfBNWylpV5qgFPoXyJ70ZAsTm3cEe3n+LBXEnY4YrVDRWxA3wZ2mz\nZ03HZ1hHrxK9CMnS829U+8sK+UneZpCO7yLRPuxwhmps0wpK/YuZZfRAKF1FZRna\nk/SIQ28rnWufmdg16YqqHgl5JOgnb3aslKRvL4dI2Gwnkd2IHtpZnTR0gxFXfqqb\nQwuRAgMBAAGjggIaMIICFjAOBgNVHQ8BAf8EBAMCBaAwHQYDVR0lBBYwFAYIKwYB\nBQUHAwEGCCsGAQUFBwMCMAwGA1UdEwEB/wQCMAAwHQYDVR0OBBYEFLsAFcxAhFX1\nMbCnzr9hEO5rL4jqMB8GA1UdIwQYMBaAFKhKamMEfd265tE5t6ZFZe/zqOyhMHAG\nCCsGAQUFBwEBBGQwYjAvBggrBgEFBQcwAYYjaHR0cDovL29jc3AuaW50LXgzLmxl\ndHNlbmNyeXB0Lm9yZy8wLwYIKwYBBQUHMAKGI2h0dHA6Ly9jZXJ0LmludC14My5s\nZXRzZW5jcnlwdC5vcmcvMCQGA1UdEQQdMBuCGWNsb3VkLmFuZHJld3NvbWV0aGlu\nZy5jb20wgf4GA1UdIASB9jCB8zAIBgZngQwBAgEwgeWECysGAQQBgt8TAQEBMIHW\nMCYGCCsGAQUFBwIBFhpodHRwOi8vY3BzLmxldHNlbmNyeXB0Lm9yZzCBqwYIKwYB\nBQUHAgIwgZ4MgZtUaGlzIENlcnRpZmljYXRlIG1heSBvbmx5IGJlIHJlbGllZCB1\ncG9uIGJ5IFJlbHlpbmcgUGFydGllcyBhbmQgb25seSQ2ziBhY2NvcmRhbmNlIHdp\ndGggdGhlIENlcnRpZmljYXRlIFBvbGljeSBmb3VuZCBhdCBsdHRwczovL2xldHNl\nbmNyeXB0Lm9yZy9yZXBvc2l0b3J5LzANBgkqhkiG9w0BAQsFAAOCAQEAOZVQvrjM\nPKXLARTjB5XsgfyDN3/qwLl7SmwGkPe+B+9FJpfScYG1JzVuCj/SoaPaK34G4x/e\niXwlwOXtMOtqjQYzNu2Pr2C+I+rVmaxIrCUXFmC205IMuUBEeWXG9Y/HvXQLPabD\nD3Gdl5+Feink9SDRP7G0HaAwq13hI7ARxkL3o+UIY39X0dV3WOboW2Re8nrkFXJ7\nq9Z6shK5QgpBfsLjtjNsQzaGV3ve1gOg25aTJGearBWOvEjJNA1wGMoKVXOtYwm/\nWyWoVdCQ8HmconcbJB6xc0UZ1EjvzRr5ZIvSa5uHZD0L3m7/kpPWlAlFJ7hHASPu\nUlF1zblDmg2Iaw==\n-----END CERTIFICATE-----\n-----BEGIN CERTIFICATE-----\nMIIEkjCCA3qgAwIBAgIQCgFBQgAAAVOFc2oLheynCDANBgkqhkiG9w0BAQsFADA/\nMSQwIgYDVQQKExtEaWdpdGFsIFNpZ25hdHVyZSBUcnVzdCBDby4xFzAVBgNVBAMT\nDkRTVCBSb290IENBIFgzMB4XDTE2MDMxNzE2NDA0NloXDTIxMDMxNzE2NDA0Nlow\nSjELMAkGA1UEBhMCVVMxFjAUBgNVBAoTDUxldCdzIEVuY3J5cHQxIzAhBgNVBAMT\nGkxldCdzIEVuY3J5cHQgQXV0aG9yaXR5IFgzMIIBIjANBgkqhkiG9w0BAQEFAAOC\nAQ8AMIIBCgKCAQEAnNMM8FrlLsd3cl03g7NoYzDq1zUmGSXhvb418XCSL7e4S0EF\nq6meNQhY7LEqxGiHC6PjdeTm86dicbp5gWAf15Gan/PQeGdxyGkOlZHP/uaZ6WA8\nSMx+yk13EiSdRxta67nsHjcAHJyse6cF6s5K671B5TaYucv9bTyWaN8jKkKQDIZ0\nZ8h/pZq4UmEUEz9l6YKHy9v6Dlb2honzhT+Xhq+w3Brvaw2VFn3EK6BlspkENnWA\na6xK8xuQSXgvopZPKiAlKQTGdMDQMc2PMTiVFrqoM7hD8bEfwzB/onkxEz0tNvjj\n/PIzark5McWvxI0NHWQWM6r6hCm21AvA2H3DkwIPOIUo4IBfTCCAXkwEgYDVR0T\nAQH/BAgwBgEB/wIBADAOBgNVHQ8BAf8EBAMCAYYwfwYIKwYBBQUHAQEEczBxMDIG\nCCsGAQUFBzABhiZodHRwOi8vaXNyZy50cnVzdGlkLm9jc3AuaWRlbnRydXN0LmNv\nbTA7BggrBgEFBQcwAoYvaHR0cDovL2FwcHMuaWRlbnRydXN0LmNvbS9yb290cy9k\nc3Ryb290Y2F4My5wN2MwHwYDVR0jBBgwFoAUxKexpHsscfrb4UuQdf/EFWCFiRAw\nVAYDVR0gBE0wSzAIBgZngQwBAgEwPwYLKwYBBAGC3xMBAQEwMDAuBggrBgEFBQcC\nARYiaHR0cDovL2Nwcy5yb290LXgxLmxldHNlbmNyeXB0Lm9yZzA8BgNVHR8ENTAz\nMDGgL6AthitodHRwOi8vY3JsLmlkZW50cnVzdC5jb20vRFNUUk9PVENBWDNDUkwu\nY3JsMB0GA1UdDgQWBBSoSmpjBH3duubRObemRWXv86jsoTANBgkqhkiG9w0BAQsF\nAAOCAQEA3TPXEfNjWDjdGBX7CVW+dla5cEilaUcne8IkCJLxWh9KEik3JHRRHGJo\nuM2VcGfl96S8TihRzZvoroed6ti6WqEBmtzw3Wodatg+VyOeph4EYpr/1wXKtx8/\nwApIvJSwtmVi4MFU5aMqrSDE6ea73Mj2tcMyo5jMd6jmeWUHK8so/joWUoHOUgwu\nX4Po1QYz+3dszkDqMp4fklxBwXRsW10KXzPMTZ+sOPAveyxindmjkW8lGy+QsRlG\nPfZ+G6Z6h7mjem0Y+iWlkYcV4PIWL1iwBi8saCbGS5jN2p8M+X+Q7UNKEkROb3N6\nKOqkqm57TH2H3eDJAkSnh6/DNFu0Qg==\n-----END CERTIFICATE-----",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### name: `str`<a id="name-str"></a>

A unique human-readable name referring to a certificate.

##### type: `str`<a id="type-str"></a>

A string representing the type of the certificate. The value will be `custom` for a user-uploaded certificate or `lets_encrypt` for one automatically generated with Let's Encrypt.

##### dns_names: List[`str`]<a id="dns_names-liststr"></a>

An array of fully qualified domain names (FQDNs) for which the certificate was issued. A certificate covering all subdomains can be issued using a wildcard (e.g. `*.example.com`).

##### private_key: `str`<a id="private_key-str"></a>

The contents of a PEM-formatted private-key corresponding to the SSL certificate.

##### leaf_certificate: `str`<a id="leaf_certificate-str"></a>

The contents of a PEM-formatted public SSL certificate.

##### certificate_chain: `str`<a id="certificate_chain-str"></a>

The full PEM-formatted trust chain between the certificate authority's certificate and your domain's SSL certificate.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`CertificatesCreateRequest`](./digital_ocean_python_sdk/type/certificates_create_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`CertificatesCreateResponse`](./digital_ocean_python_sdk/pydantic/certificates_create_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/certificates` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.certificates.delete`<a id="digitaloceancertificatesdelete"></a>

To delete a specific certificate, send a DELETE request to
`/v2/certificates/$CERTIFICATE_ID`.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.certificates.delete(
    certificate_id="4de7ac8b-495b-4884-9a69-1050c6793cd6",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### certificate_id: `str`<a id="certificate_id-str"></a>

A unique identifier for a certificate.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/certificates/{certificate_id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.certificates.get`<a id="digitaloceancertificatesget"></a>

To show information about an existing certificate, send a GET request to `/v2/certificates/$CERTIFICATE_ID`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_response = digitalocean.certificates.get(
    certificate_id="4de7ac8b-495b-4884-9a69-1050c6793cd6",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### certificate_id: `str`<a id="certificate_id-str"></a>

A unique identifier for a certificate.

#### 🔄 Return<a id="🔄-return"></a>

[`CertificatesGetResponse`](./digital_ocean_python_sdk/pydantic/certificates_get_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/certificates/{certificate_id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.certificates.list`<a id="digitaloceancertificateslist"></a>

To list all of the certificates available on your account, send a GET request to `/v2/certificates`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = digitalocean.certificates.list(
    per_page=2,
    page=1,
    name="certificate-name",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### per_page: `int`<a id="per_page-int"></a>

Number of items returned per page

##### page: `int`<a id="page-int"></a>

Which 'page' of paginated results to return.

##### name: `str`<a id="name-str"></a>

Name of expected certificate

#### 🔄 Return<a id="🔄-return"></a>

[`CertificatesListResponse`](./digital_ocean_python_sdk/pydantic/certificates_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/certificates` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.container_registry.cancel_garbage_collection`<a id="digitaloceancontainer_registrycancel_garbage_collection"></a>

To cancel the currently-active garbage collection for a registry, send a PUT request to `/v2/registry/$REGISTRY_NAME/garbage-collection/$GC_UUID` and specify one or more of the attributes below.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
cancel_garbage_collection_response = digitalocean.container_registry.cancel_garbage_collection(
    registry_name="example",
    garbage_collection_uuid="eff0feee-49c7-4e8f-ba5c-a320c109c8a8",
    cancel=True,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### registry_name: `str`<a id="registry_name-str"></a>

The name of a container registry.

##### garbage_collection_uuid: `str`<a id="garbage_collection_uuid-str"></a>

The UUID of a garbage collection run.

##### cancel: `bool`<a id="cancel-bool"></a>

A boolean value indicating that the garbage collection should be cancelled.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`UpdateRegistry`](./digital_ocean_python_sdk/type/update_registry.py)
#### 🔄 Return<a id="🔄-return"></a>

[`ContainerRegistryGetActiveGarbageCollectionResponse`](./digital_ocean_python_sdk/pydantic/container_registry_get_active_garbage_collection_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/registry/{registry_name}/garbage-collection/{garbage_collection_uuid}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.container_registry.create`<a id="digitaloceancontainer_registrycreate"></a>

To create your container registry, send a POST request to `/v2/registry`.

The `name` becomes part of the URL for images stored in the registry. For
example, if your registry is called `example`, an image in it will have the
URL `registry.digitalocean.com/example/image:tag`.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_response = digitalocean.container_registry.create(
    name="example",
    subscription_tier_slug="basic",
    region="fra1",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### name: `str`<a id="name-str"></a>

A globally unique name for the container registry. Must be lowercase and be composed only of numbers, letters and `-`, up to a limit of 63 characters.

##### subscription_tier_slug: `str`<a id="subscription_tier_slug-str"></a>

The slug of the subscription tier to sign up for. Valid values can be retrieved using the options endpoint.

##### region: `str`<a id="region-str"></a>

Slug of the region where registry data is stored. When not provided, a region will be selected.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`RegistryCreate`](./digital_ocean_python_sdk/type/registry_create.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/registry` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.container_registry.delete`<a id="digitaloceancontainer_registrydelete"></a>

To delete your container registry, destroying all container image data stored in it, send a DELETE request to `/v2/registry`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.container_registry.delete()
```

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/registry` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.container_registry.delete_repository_manifest_by_digest`<a id="digitaloceancontainer_registrydelete_repository_manifest_by_digest"></a>

To delete a container repository manifest by digest, send a DELETE request to
`/v2/registry/$REGISTRY_NAME/repositories/$REPOSITORY_NAME/digests/$MANIFEST_DIGEST`.

Note that if your repository name contains `/` characters, it must be
URL-encoded in the request URL. For example, to delete
`registry.digitalocean.com/example/my/repo@sha256:abcd`, the path would be
`/v2/registry/example/repositories/my%2Frepo/digests/sha256:abcd`.

A successful request will receive a 204 status code with no body in response.
This indicates that the request was processed successfully.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.container_registry.delete_repository_manifest_by_digest(
    registry_name="example",
    repository_name="repo-1",
    manifest_digest="sha256:cb8a924afdf0229ef7515d9e5b3024e23b3eb03ddbba287f4a19c6ac90b8d221",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### registry_name: `str`<a id="registry_name-str"></a>

The name of a container registry.

##### repository_name: `str`<a id="repository_name-str"></a>

The name of a container registry repository. If the name contains `/` characters, they must be URL-encoded, e.g. `%2F`.

##### manifest_digest: `str`<a id="manifest_digest-str"></a>

The manifest digest of a container registry repository tag.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/registry/{registry_name}/repositories/{repository_name}/digests/{manifest_digest}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.container_registry.delete_repository_tag`<a id="digitaloceancontainer_registrydelete_repository_tag"></a>

To delete a container repository tag, send a DELETE request to
`/v2/registry/$REGISTRY_NAME/repositories/$REPOSITORY_NAME/tags/$TAG`.

Note that if your repository name contains `/` characters, it must be
URL-encoded in the request URL. For example, to delete
`registry.digitalocean.com/example/my/repo:mytag`, the path would be
`/v2/registry/example/repositories/my%2Frepo/tags/mytag`.

A successful request will receive a 204 status code with no body in response.
This indicates that the request was processed successfully.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.container_registry.delete_repository_tag(
    registry_name="example",
    repository_name="repo-1",
    repository_tag="06a447a",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### registry_name: `str`<a id="registry_name-str"></a>

The name of a container registry.

##### repository_name: `str`<a id="repository_name-str"></a>

The name of a container registry repository. If the name contains `/` characters, they must be URL-encoded, e.g. `%2F`.

##### repository_tag: `str`<a id="repository_tag-str"></a>

The name of a container registry repository tag.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/registry/{registry_name}/repositories/{repository_name}/tags/{repository_tag}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.container_registry.get`<a id="digitaloceancontainer_registryget"></a>

To get information about your container registry, send a GET request to `/v2/registry`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_response = digitalocean.container_registry.get()
```

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/registry` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.container_registry.get_active_garbage_collection`<a id="digitaloceancontainer_registryget_active_garbage_collection"></a>

To get information about the currently-active garbage collection for a registry, send a GET request to `/v2/registry/$REGISTRY_NAME/garbage-collection`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_active_garbage_collection_response = digitalocean.container_registry.get_active_garbage_collection(
    registry_name="example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### registry_name: `str`<a id="registry_name-str"></a>

The name of a container registry.

#### 🔄 Return<a id="🔄-return"></a>

[`ContainerRegistryGetActiveGarbageCollectionResponse`](./digital_ocean_python_sdk/pydantic/container_registry_get_active_garbage_collection_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/registry/{registry_name}/garbage-collection` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.container_registry.get_docker_credentials`<a id="digitaloceancontainer_registryget_docker_credentials"></a>

In order to access your container registry with the Docker client or from a
Kubernetes cluster, you will need to configure authentication. The necessary
JSON configuration can be retrieved by sending a GET request to
`/v2/registry/docker-credentials`.

The response will be in the format of a Docker `config.json` file. To use the
config in your Kubernetes cluster, create a Secret with:

    kubectl create secret generic docr \
      --from-file=.dockerconfigjson=config.json \
      --type=kubernetes.io/dockerconfigjson

By default, the returned credentials have read-only access to your registry
and cannot be used to push images. This is appropriate for most Kubernetes
clusters. To retrieve read/write credentials, suitable for use with the Docker
client or in a CI system, read_write may be provided as query parameter. For
example: `/v2/registry/docker-credentials?read_write=true`

By default, the returned credentials will not expire. To retrieve credentials
with an expiry set, expiry_seconds may be provided as a query parameter. For
example: `/v2/registry/docker-credentials?expiry_seconds=3600` will return
credentials that expire after one hour.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_docker_credentials_response = digitalocean.container_registry.get_docker_credentials(
    expiry_seconds=3600,
    read_write=True,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### expiry_seconds: `int`<a id="expiry_seconds-int"></a>

The duration in seconds that the returned registry credentials will be valid. If not set or 0, the credentials will not expire.

##### read_write: `bool`<a id="read_write-bool"></a>

By default, the registry credentials allow for read-only access. Set this query parameter to `true` to obtain read-write credentials.

#### 🔄 Return<a id="🔄-return"></a>

[`DockerCredentials`](./digital_ocean_python_sdk/pydantic/docker_credentials.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/registry/docker-credentials` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.container_registry.get_subscription_info`<a id="digitaloceancontainer_registryget_subscription_info"></a>

A subscription is automatically created when you configure your container registry. To get information about your subscription, send a GET request to `/v2/registry/subscription`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_subscription_info_response = digitalocean.container_registry.get_subscription_info()
```

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/registry/subscription` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.container_registry.list_garbage_collections`<a id="digitaloceancontainer_registrylist_garbage_collections"></a>

To get information about past garbage collections for a registry, send a GET request to `/v2/registry/$REGISTRY_NAME/garbage-collections`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_garbage_collections_response = digitalocean.container_registry.list_garbage_collections(
    registry_name="example",
    per_page=2,
    page=1,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### registry_name: `str`<a id="registry_name-str"></a>

The name of a container registry.

##### per_page: `int`<a id="per_page-int"></a>

Number of items returned per page

##### page: `int`<a id="page-int"></a>

Which 'page' of paginated results to return.

#### 🔄 Return<a id="🔄-return"></a>

[`ContainerRegistryListGarbageCollectionsResponse`](./digital_ocean_python_sdk/pydantic/container_registry_list_garbage_collections_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/registry/{registry_name}/garbage-collections` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.container_registry.list_options`<a id="digitaloceancontainer_registrylist_options"></a>

This endpoint serves to provide additional information as to which option values are available when creating a container registry.
There are multiple subscription tiers available for container registry. Each tier allows a different number of image repositories to be created in your registry, and has a different amount of storage and transfer included.
There are multiple regions available for container registry and controls where your data is stored.
To list the available options, send a GET request to `/v2/registry/options`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_options_response = digitalocean.container_registry.list_options()
```

#### 🔄 Return<a id="🔄-return"></a>

[`ContainerRegistryListOptionsResponse`](./digital_ocean_python_sdk/pydantic/container_registry_list_options_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/registry/options` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.container_registry.list_repositories`<a id="digitaloceancontainer_registrylist_repositories"></a>

This endpoint has been deprecated in favor of the _List All Container Registry Repositories [V2]_ endpoint.

To list all repositories in your container registry, send a GET
request to `/v2/registry/$REGISTRY_NAME/repositories`.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_repositories_response = digitalocean.container_registry.list_repositories(
    registry_name="example",
    per_page=2,
    page=1,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### registry_name: `str`<a id="registry_name-str"></a>

The name of a container registry.

##### per_page: `int`<a id="per_page-int"></a>

Number of items returned per page

##### page: `int`<a id="page-int"></a>

Which 'page' of paginated results to return.

#### 🔄 Return<a id="🔄-return"></a>

[`ContainerRegistryListRepositoriesResponse`](./digital_ocean_python_sdk/pydantic/container_registry_list_repositories_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/registry/{registry_name}/repositories` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.container_registry.list_repositories_v2`<a id="digitaloceancontainer_registrylist_repositories_v2"></a>

To list all repositories in your container registry, send a GET request to `/v2/registry/$REGISTRY_NAME/repositoriesV2`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_repositories_v2_response = digitalocean.container_registry.list_repositories_v2(
    registry_name="example",
    per_page=2,
    page=1,
    page_token="eyJUb2tlbiI6IkNnZGpiMjlz",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### registry_name: `str`<a id="registry_name-str"></a>

The name of a container registry.

##### per_page: `int`<a id="per_page-int"></a>

Number of items returned per page

##### page: `int`<a id="page-int"></a>

Which 'page' of paginated results to return. Ignored when 'page_token' is provided.

##### page_token: `str`<a id="page_token-str"></a>

Token to retrieve of the next or previous set of results more quickly than using 'page'.

#### 🔄 Return<a id="🔄-return"></a>

[`ContainerRegistryListRepositoriesV2Response`](./digital_ocean_python_sdk/pydantic/container_registry_list_repositories_v2_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/registry/{registry_name}/repositoriesV2` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.container_registry.list_repository_manifests`<a id="digitaloceancontainer_registrylist_repository_manifests"></a>

To list all manifests in your container registry repository, send a GET
request to `/v2/registry/$REGISTRY_NAME/repositories/$REPOSITORY_NAME/digests`.

Note that if your repository name contains `/` characters, it must be
URL-encoded in the request URL. For example, to list manifests for
`registry.digitalocean.com/example/my/repo`, the path would be
`/v2/registry/example/repositories/my%2Frepo/digests`.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_repository_manifests_response = digitalocean.container_registry.list_repository_manifests(
    registry_name="example",
    repository_name="repo-1",
    per_page=2,
    page=1,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### registry_name: `str`<a id="registry_name-str"></a>

The name of a container registry.

##### repository_name: `str`<a id="repository_name-str"></a>

The name of a container registry repository. If the name contains `/` characters, they must be URL-encoded, e.g. `%2F`.

##### per_page: `int`<a id="per_page-int"></a>

Number of items returned per page

##### page: `int`<a id="page-int"></a>

Which 'page' of paginated results to return.

#### 🔄 Return<a id="🔄-return"></a>

[`ContainerRegistryListRepositoryManifestsResponse`](./digital_ocean_python_sdk/pydantic/container_registry_list_repository_manifests_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/registry/{registry_name}/repositories/{repository_name}/digests` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.container_registry.list_repository_tags`<a id="digitaloceancontainer_registrylist_repository_tags"></a>

To list all tags in your container registry repository, send a GET
request to `/v2/registry/$REGISTRY_NAME/repositories/$REPOSITORY_NAME/tags`.

Note that if your repository name contains `/` characters, it must be
URL-encoded in the request URL. For example, to list tags for
`registry.digitalocean.com/example/my/repo`, the path would be
`/v2/registry/example/repositories/my%2Frepo/tags`.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_repository_tags_response = digitalocean.container_registry.list_repository_tags(
    registry_name="example",
    repository_name="repo-1",
    per_page=2,
    page=1,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### registry_name: `str`<a id="registry_name-str"></a>

The name of a container registry.

##### repository_name: `str`<a id="repository_name-str"></a>

The name of a container registry repository. If the name contains `/` characters, they must be URL-encoded, e.g. `%2F`.

##### per_page: `int`<a id="per_page-int"></a>

Number of items returned per page

##### page: `int`<a id="page-int"></a>

Which 'page' of paginated results to return.

#### 🔄 Return<a id="🔄-return"></a>

[`ContainerRegistryListRepositoryTagsResponse`](./digital_ocean_python_sdk/pydantic/container_registry_list_repository_tags_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/registry/{registry_name}/repositories/{repository_name}/tags` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.container_registry.start_garbage_collection`<a id="digitaloceancontainer_registrystart_garbage_collection"></a>

Garbage collection enables users to clear out unreferenced blobs (layer &
manifest data) after deleting one or more manifests from a repository. If
there are no unreferenced blobs resulting from the deletion of one or more
manifests, garbage collection is effectively a noop.
[See here for more information](https://www.digitalocean.com/docs/container-registry/how-to/clean-up-container-registry/)
about how and why you should clean up your container registry periodically.

To request a garbage collection run on your registry, send a POST request to
`/v2/registry/$REGISTRY_NAME/garbage-collection`. This will initiate the
following sequence of events on your registry.

* Set the registry to read-only mode, meaning no further write-scoped
  JWTs will be issued to registry clients. Existing write-scoped JWTs will
  continue to work until they expire which can take up to 15 minutes.
* Wait until all existing write-scoped JWTs have expired.
* Scan all registry manifests to determine which blobs are unreferenced.
* Delete all unreferenced blobs from the registry.
* Record the number of blobs deleted and bytes freed, mark the garbage
  collection status as `success`.
* Remove the read-only mode restriction from the registry, meaning write-scoped
  JWTs will once again be issued to registry clients.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
start_garbage_collection_response = digitalocean.container_registry.start_garbage_collection(
    registry_name="example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### registry_name: `str`<a id="registry_name-str"></a>

The name of a container registry.

#### 🔄 Return<a id="🔄-return"></a>

[`ContainerRegistryGetActiveGarbageCollectionResponse`](./digital_ocean_python_sdk/pydantic/container_registry_get_active_garbage_collection_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/registry/{registry_name}/garbage-collection` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.container_registry.update_subscription_tier`<a id="digitaloceancontainer_registryupdate_subscription_tier"></a>

After creating your registry, you can switch to a different subscription tier to better suit your needs. To do this, send a POST request to `/v2/registry/subscription`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_subscription_tier_response = digitalocean.container_registry.update_subscription_tier(
    tier_slug="basic",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### tier_slug: `str`<a id="tier_slug-str"></a>

The slug of the subscription tier to sign up for.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ContainerRegistryUpdateSubscriptionTierRequest`](./digital_ocean_python_sdk/type/container_registry_update_subscription_tier_request.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/registry/subscription` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.container_registry.validate_name`<a id="digitaloceancontainer_registryvalidate_name"></a>

To validate that a container registry name is available for use, send a POST
request to `/v2/registry/validate-name`.

If the name is both formatted correctly and available, the response code will
be 204 and contain no body. If the name is already in use, the response will
be a 409 Conflict.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.container_registry.validate_name(
    name="example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### name: `str`<a id="name-str"></a>

A globally unique name for the container registry. Must be lowercase and be composed only of numbers, letters and `-`, up to a limit of 63 characters.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ValidateRegistry`](./digital_ocean_python_sdk/type/validate_registry.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/registry/validate-name` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.databases.add`<a id="digitaloceandatabasesadd"></a>

To add a new database to an existing cluster, send a POST request to
`/v2/databases/$DATABASE_ID/dbs`.

Note: Database management is not supported for Redis clusters.

The response will be a JSON object with a key called `db`. The value of this will be
an object that contains the standard attributes associated with a database.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
add_response = digitalocean.databases.add(
    name="alpha",
    database_cluster_uuid="9cc10173-e9ea-4176-9dbc-a4cee4c4ff30",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### name: `str`<a id="name-str"></a>

The name of the database.

##### database_cluster_uuid: `str`<a id="database_cluster_uuid-str"></a>

A unique identifier for a database cluster.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`Database`](./digital_ocean_python_sdk/type/database.py)
#### 🔄 Return<a id="🔄-return"></a>

[`DatabasesAddResponse`](./digital_ocean_python_sdk/pydantic/databases_add_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/databases/{database_cluster_uuid}/dbs` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.databases.add_new_connection_pool`<a id="digitaloceandatabasesadd_new_connection_pool"></a>

For PostgreSQL database clusters, connection pools can be used to allow a
database to share its idle connections. The popular PostgreSQL connection
pooling utility PgBouncer is used to provide this service. [See here for more information](https://www.digitalocean.com/docs/databases/postgresql/how-to/manage-connection-pools/)
about how and why to use PgBouncer connection pooling including
details about the available transaction modes.

To add a new connection pool to a PostgreSQL database cluster, send a POST
request to `/v2/databases/$DATABASE_ID/pools` specifying a name for the pool,
the user to connect with, the database to connect to, as well as its desired
size and transaction mode.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
add_new_connection_pool_response = digitalocean.databases.add_new_connection_pool(
    name="backend-pool",
    mode="transaction",
    size=10,
    db="defaultdb",
    database_cluster_uuid="9cc10173-e9ea-4176-9dbc-a4cee4c4ff30",
    user="doadmin",
    connection=None,
    private_connection=None,
    standby_connection=None,
    standby_private_connection=None,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### name: `str`<a id="name-str"></a>

A unique name for the connection pool. Must be between 3 and 60 characters.

##### mode: `str`<a id="mode-str"></a>

The PGBouncer transaction mode for the connection pool. The allowed values are session, transaction, and statement.

##### size: `int`<a id="size-int"></a>

The desired size of the PGBouncer connection pool. The maximum allowed size is determined by the size of the cluster's primary node. 25 backend server connections are allowed for every 1GB of RAM. Three are reserved for maintenance. For example, a primary node with 1 GB of RAM allows for a maximum of 22 backend server connections while one with 4 GB would allow for 97. Note that these are shared across all connection pools in a cluster.

##### db: `str`<a id="db-str"></a>

The database for use with the connection pool.

##### database_cluster_uuid: `str`<a id="database_cluster_uuid-str"></a>

A unique identifier for a database cluster.

##### user: `str`<a id="user-str"></a>

The name of the user for use with the connection pool. When excluded, all sessions connect to the database as the inbound user.

##### connection: Union[`DatabaseConnection`, [`Union[bool, date, datetime, dict, float, int, list, str, None]`](./digital_ocean_python_sdk/type/typing_union_bool_date_datetime_dict_float_int_list_str_none.py)]<a id="connection-uniondatabaseconnection-unionbool-date-datetime-dict-float-int-list-str-nonedigital_ocean_python_sdktypetyping_union_bool_date_datetime_dict_float_int_list_str_nonepy"></a>


##### private_connection: Union[`DatabaseConnection`, [`Union[bool, date, datetime, dict, float, int, list, str, None]`](./digital_ocean_python_sdk/type/typing_union_bool_date_datetime_dict_float_int_list_str_none.py)]<a id="private_connection-uniondatabaseconnection-unionbool-date-datetime-dict-float-int-list-str-nonedigital_ocean_python_sdktypetyping_union_bool_date_datetime_dict_float_int_list_str_nonepy"></a>


##### standby_connection: Union[`DatabaseConnection`, [`Union[bool, date, datetime, dict, float, int, list, str, None]`](./digital_ocean_python_sdk/type/typing_union_bool_date_datetime_dict_float_int_list_str_none.py)]<a id="standby_connection-uniondatabaseconnection-unionbool-date-datetime-dict-float-int-list-str-nonedigital_ocean_python_sdktypetyping_union_bool_date_datetime_dict_float_int_list_str_nonepy"></a>


##### standby_private_connection: Union[`DatabaseConnection`, [`Union[bool, date, datetime, dict, float, int, list, str, None]`](./digital_ocean_python_sdk/type/typing_union_bool_date_datetime_dict_float_int_list_str_none.py)]<a id="standby_private_connection-uniondatabaseconnection-unionbool-date-datetime-dict-float-int-list-str-nonedigital_ocean_python_sdktypetyping_union_bool_date_datetime_dict_float_int_list_str_nonepy"></a>


#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ConnectionPool`](./digital_ocean_python_sdk/type/connection_pool.py)
#### 🔄 Return<a id="🔄-return"></a>

[`DatabasesAddNewConnectionPoolResponse`](./digital_ocean_python_sdk/pydantic/databases_add_new_connection_pool_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/databases/{database_cluster_uuid}/pools` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.databases.add_user`<a id="digitaloceandatabasesadd_user"></a>

To add a new database user, send a POST request to `/v2/databases/$DATABASE_ID/users`
with the desired username.

Note: User management is not supported for Redis clusters.

When adding a user to a MySQL cluster, additional options can be configured in the
`mysql_settings` object.

When adding a user to a Kafka cluster, additional options can be configured in
the `settings` object.

The response will be a JSON object with a key called `user`. The value of this will be an
object that contains the standard attributes associated with a database user including
its randomly generated password.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
add_user_response = digitalocean.databases.add_user(
    body=None,
    database_cluster_uuid="9cc10173-e9ea-4176-9dbc-a4cee4c4ff30",
    name="app-01",
    role="normal",
    password="jge5lfxtzhx42iff",
    access_cert="-----BEGIN CERTIFICATE-----\nMIIFFjCCA/6gAwIBAgISA0AznUJmXhu08/89ZuSPC/kRMA0GCSqGSIb3DQEBCwUA\nMEoxCzAJBgNVBAYTAlVTMRYwFAYDVQQKEw1MZXQncyBFbmNyeXB0MSMwIQYDVQQD\nExpMZXQncyBFbmNyeXB0IEF1dGhvcml0eSBYMzAeFw0xNjExMjQwMDIzMDBaFw0x\nNzAyMjIwMDIzMDBaMCQxIjAgBgNVBAMTGWNsb3VkLmFuZHJld3NvbWV0aGluZy5j\nb20wggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDBIZMz8pnK6V52SVf+\nCYssOfCQHAx5f0Ou5rYbq3xNh8VWHIYJCQ1QxQIxKSP6+uODSYrb2KWyurP1DwGb\n8OYm0J3syEDtCUQik1cpCzpeNlAZ2f8FzXyYQAqPopxdRpsFz8DtZnVvu86XwrE4\noFPl9MReICmZfBNWylpV5qgFPoXyJ70ZAsTm3cEe3n+LBXEnY4YrVDRWxA3wZ2mz\nZ03HZ1hHrxK9CMnS829U+8sK+UneZpCO7yLRPuxwhmps0wpK/YuZZfRAKF1FZRna\nk/SIQ28rnWufmdg16YqqHgl5JOgnb3aslKRvL4dI2Gwnkd2IHtpZnTR0gxFXfqqb\nQwuRAgMBAAGjggIaMIICFjAOBgNVHQ8BAf8EBAMCBaAwHQYDVR0lBBYwFAYIKwYB\nBQUHAwEGCCsGAQUFBwMCMAwGA1UdEwEB/wQCMAAwHQYDVR0OBBYEFLsAFcxAhFX1\nMbCnzr9hEO5rL4jqMB8GA1UdIwQYMBaAFKhKamMEfd265tE5t6ZFZe/zqOyhMHAG\nCCsGAQUFBwEBBGQwYjAvBggrBgEFBQcwAYYjaHR0cDovL29jc3AuaW50LXgzLmxl\ndHNlbmNyeXB0Lm9yZy8wLwYIKwYBBQUHMAKGI2h0dHA6Ly9jZXJ0LmludC14My5s\nZXRzZW5jcnlwdC5vcmcvMCQGA1UdEQQdMBuCGWNsb3VkLmFuZHJld3NvbWV0aGlu\nZy5jb20wgf4GA1UdIASB9jCB8zAIBgZngQwBAgWrgeYGCysGAQQBgt8TAQEBMIHW\nMCYGCCsGAQUFBwIBFhpodHRwOi8vY3BzLmxldHNlbmNyeXB0Lm9yZzCBqwYIKwYB\nBQUHAgIwgZ4MgZtUaGlzIENlcnRpZmljYXRlIG1heSBvbmx5IGJlIHJlbGllZCB1\ncG9uIGJ5IFJlbHlpbmcgUGFydGllcyBhbmQgb25seSQ2ziBhY2NvcmRhbmNlIHdp\ndGggdGhlIENlcnRpZmljYXRlIFBvbGljeSBmb3VuZCBhdCBodHRwczovL2xldHNl\nbmNyeXB0Lm9yZy9yZXBvc2l0b3J5LzANBgkqhkiG9w0BAQsFAAOCAQEAOZVQvrjM\nPKXLARTjB5XsgfyDN3/qwLl7SmwGkPe+B+9FJpfScYG1JzVuCj/SoaPaK34G4x/e\niXwlwOXtMOtqjQYzNu2Pr2C+I+rVmaxIrCUXFmC205IMuUBEeWXG9Y/HvXQLPabD\nD3Gdl5+Feink9SDRP7G0HaAwq13hI7ARxkL9p+UIY39X0dV3WOboW2Re8nrkFXJ7\nq9Z6shK5QgpBfsLjtjNsQzaGV3ve1gOg25aTJGearBWOvEjJNA1wGMoKVXOtYwm/\nWyWoVdCQ8HmconcbJB6xc0UZ1EjvzRr5ZIvSa5uHZD0L3m7/kpPWlAlFJ7hHASPu\nUlF1zblDmg2Iaw==\n-----END CERTIFICATE-----",
    access_key="-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDBIZMz8pnK6V52\nSVf+CYssOfCQHAx5f0Ou5rYbq3xNh8VHAIYJCQ1QxQIxKSP6+uODSYrb2KWyurP1\nDwGb8OYm0J3syEDtCUQik1cpCzpeNlAZ2f8FzXyYQAqPopxdRpsFz8DtZnVvu86X\nwrE4oFPl9MReICmZfBNWylpV5qgFPoXyJ70ZAsTm3cEe3n+LBXEnY4YrVDRWxA3w\nZ2mzZ03HZ1hHrxK9CMnS829U+8sK+UneZpCO7yLRPuxwhmps0wpK/YuZZfRAKF1F\nZRnak/SIQ28rnWufmdg16YqqHgl5JOgnb3aslKRvL4dI2Gwnkd2IHtpZnTR0gxFX\nfqqbQwuRAgMBAAECggEBAILLmkW0JzOkmLTDNzR0giyRkLoIROqDpfLtjKdwm95l\n9NUBJcU4vCvXQITKt/NhtnNTexcowg8pInb0ksJpg3UGE+4oMNBXVi2UW5MQZ5cm\ncVkQqgXkBF2YAY8FMaB6EML+0En2+dGR/3gIAr221xsFiXe1kHbB8Nb2c/d5HpFt\neRpLVJnK+TxSr78PcZA8DDGlSgwvgimdAaFUNO2OqB9/0E9UPyKk2ycdff/Z6ldF\n0hkCLtdYTTl8Kf/OwjcuTgmA2O3Y8/CoQX/L+oP9Rvt9pWCEfuebiOmHJVPO6Y6x\ngtQVEXwmF1pDHH4Qtz/e6UZTdYeMl9G4aNO2CawwcaYECgYEA57imgSOG4XsJLRh\nGGncV9R/xhy4AbDWLtAMzQRX4ktvKCaHWyQV2XK2we/cu29NLv2Y89WmerTNPOU+\nP8+pB31uty2ELySVn15QhKpQClVEAlxCnnNjXYrii5LOM80+lVmxvQwxVd8Yz8nj\nIntyioXNBEnYS7V2RxxFGgFun1cCgYEA1V3W+Uyamhq8JS5EY0FhyGcXdHd70K49\nW1ou7McIpncf9tM9acLS1hkI98rd2T69Zo8mKoV1V2hjFaKUYfNys6tTkYWeZCcJ\n3rW44j9DTD+FmmjcX6b8DzfybGLehfNbCw6n67/r45DXIV/fk6XZfkx6IEGO4ODt\nNfnvx4TuI1cCgYBACDiKqwSUvmkUuweOo4IuCxyb5Ee8v98P5JIE/VRDxlCbKbpx\npxEam6aBBQVcDi+n8o0H3WjjlKc6UqbW/01YMoMrvzotxNBLz8Y0QtQHZvR6KoCG\nRKCKstxTcWflzKuknbqN4RapAhNbKBDJ8PMSWfyDWNyaXzSmBdvaidbF1QKBgDI0\no4oD0Xkjg1QIYAUu9FBQmb9JAjRnW36saNBEQS/SZg4RRKknM683MtoDvVIKJk0E\nsAlfX+4SXQZRPDMUMtA+Jyrd0xhj6zmhbwClvDMr20crF3fWdgcqtft1BEFmsuyW\nJUMe5OWmRkjPI2+9ncDPRAllA7a8lnSV/Crph5N/AoGBAIK249temKrGe9pmsmAo\nQbNuYSmwpnMoAqdHTrl70HEmK7ob6SIVmsR8QFAkH7xkYZc4Bxbx4h1bdpozGB+/\nAangbiaYJcAOD1QyfiFbflvI1RFeHgrk7VIafeSeQv6qu0LLMi2zUbpgVzxt78Wg\neTuK2xNR0PIM8OI7pRpgyj1I\n-----END PRIVATE KEY-----",
    mysql_settings={
        "auth_plugin": "mysql_native_password",
    },
    settings={
        "pg_allow_replication": True,
    },
    readonly=True,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### database_cluster_uuid: `str`<a id="database_cluster_uuid-str"></a>

A unique identifier for a database cluster.

##### name: `str`<a id="name-str"></a>

The name of a database user.

##### role: `str`<a id="role-str"></a>

A string representing the database user's role. The value will be either \\\"primary\\\" or \\\"normal\\\". 

##### password: `str`<a id="password-str"></a>

A randomly generated password for the database user.

##### access_cert: `str`<a id="access_cert-str"></a>

Access certificate for TLS client authentication. (Kafka only)

##### access_key: `str`<a id="access_key-str"></a>

Access key for TLS client authentication. (Kafka only)

##### mysql_settings: [`MysqlSettings`](./digital_ocean_python_sdk/type/mysql_settings.py)<a id="mysql_settings-mysqlsettingsdigital_ocean_python_sdktypemysql_settingspy"></a>


##### settings: [`UserSettings`](./digital_ocean_python_sdk/type/user_settings.py)<a id="settings-usersettingsdigital_ocean_python_sdktypeuser_settingspy"></a>


##### readonly: `bool`<a id="readonly-bool"></a>

For MongoDB clusters, set to `true` to create a read-only user. This option is not currently supported for other database engines.              

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`DatabasesAddUserRequest`](./digital_ocean_python_sdk/type/databases_add_user_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`DatabasesAddUserResponse`](./digital_ocean_python_sdk/pydantic/databases_add_user_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/databases/{database_cluster_uuid}/users` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.databases.configure_eviction_policy`<a id="digitaloceandatabasesconfigure_eviction_policy"></a>

To configure an eviction policy for an existing Redis cluster, send a PUT request to `/v2/databases/$DATABASE_ID/eviction_policy` specifying the desired policy.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.databases.configure_eviction_policy(
    eviction_policy="allkeys_lru",
    database_cluster_uuid="9cc10173-e9ea-4176-9dbc-a4cee4c4ff30",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### eviction_policy: [`EvictionPolicyModel`](./digital_ocean_python_sdk/type/eviction_policy_model.py)<a id="eviction_policy-evictionpolicymodeldigital_ocean_python_sdktypeeviction_policy_modelpy"></a>

##### database_cluster_uuid: `str`<a id="database_cluster_uuid-str"></a>

A unique identifier for a database cluster.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`DatabasesConfigureEvictionPolicyRequest`](./digital_ocean_python_sdk/type/databases_configure_eviction_policy_request.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/databases/{database_cluster_uuid}/eviction_policy` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.databases.configure_maintenance_window`<a id="digitaloceandatabasesconfigure_maintenance_window"></a>

To configure the window when automatic maintenance should be performed for a database cluster, send a PUT request to `/v2/databases/$DATABASE_ID/maintenance`.
A successful request will receive a 204 No Content status code with no body in response.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.databases.configure_maintenance_window(
    day="tuesday",
    hour="840",
    database_cluster_uuid="9cc10173-e9ea-4176-9dbc-a4cee4c4ff30",
    description=["Update TimescaleDB to version 1.2.1", "Upgrade to PostgreSQL 11.2 and 10.7 bugfix releases"],
    pending=True,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### day: `str`<a id="day-str"></a>

The day of the week on which to apply maintenance updates.

##### hour: `str`<a id="hour-str"></a>

The hour in UTC at which maintenance updates will be applied in 24 hour format.

##### database_cluster_uuid: `str`<a id="database_cluster_uuid-str"></a>

A unique identifier for a database cluster.

##### description: [`DatabaseMaintenanceWindowDescription`](./digital_ocean_python_sdk/type/database_maintenance_window_description.py)<a id="description-databasemaintenancewindowdescriptiondigital_ocean_python_sdktypedatabase_maintenance_window_descriptionpy"></a>

##### pending: `bool`<a id="pending-bool"></a>

A boolean value indicating whether any maintenance is scheduled to be performed in the next window.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`DatabaseMaintenanceWindow`](./digital_ocean_python_sdk/type/database_maintenance_window.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/databases/{database_cluster_uuid}/maintenance` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.databases.create_cluster`<a id="digitaloceandatabasescreate_cluster"></a>

To create a database cluster, send a POST request to `/v2/databases`.
The response will be a JSON object with a key called `database`. The value of this will be an object that contains the standard attributes associated with a database cluster. The initial value of the database cluster's `status` attribute will be `creating`. When the cluster is ready to receive traffic, this will transition to `online`.

The embedded `connection` and `private_connection` objects will contain the information needed to access the database cluster. For multi-node clusters, the `standby_connection` and `standby_private_connection` objects will contain the information needed to connect to the cluster's standby node(s).

DigitalOcean managed PostgreSQL and MySQL database clusters take automated daily backups. To create a new database cluster based on a backup of an existing cluster, send a POST request to `/v2/databases`. In addition to the standard database cluster attributes, the JSON body must include a key named `backup_restore` with the name of the original database cluster and the timestamp of the backup to be restored. Creating a database from a backup is the same as forking a database in the control panel.
Note: Backups are not supported for Redis clusters.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_cluster_response = digitalocean.databases.create_cluster(
    body=None,
    tags=["production"],
    version="8",
    id="9cc10173-e9ea-4176-9dbc-a4cee4c4ff30",
    name="backend",
    engine="mysql",
    semantic_version="8.0.28",
    num_nodes=2,
    size="db-s-2vcpu-4gb",
    region="nyc3",
    status="creating",
    created_at="2019-01-11T18:37:36Z",
    private_network_uuid="d455e75d-4858-4eec-8c95-da2f0a5f93a7",
    db_names=["doadmin"],
    connection=None,
    private_connection=None,
    standby_connection=None,
    standby_private_connection=None,
    users=[
        {
            "name": "app-01",
            "role": "normal",
            "password": "jge5lfxtzhx42iff",
            "access_cert": "-----BEGIN CERTIFICATE-----\nMIIFFjCCA/6gAwIBAgISA0AznUJmXhu08/89ZuSPC/kRMA0GCSqGSIb3DQEBCwUA\nMEoxCzAJBgNVBAYTAlVTMRYwFAYDVQQKEw1MZXQncyBFbmNyeXB0MSMwIQYDVQQD\nExpMZXQncyBFbmNyeXB0IEF1dGhvcml0eSBYMzAeFw0xNjExMjQwMDIzMDBaFw0x\nNzAyMjIwMDIzMDBaMCQxIjAgBgNVBAMTGWNsb3VkLmFuZHJld3NvbWV0aGluZy5j\nb20wggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDBIZMz8pnK6V52SVf+\nCYssOfCQHAx5f0Ou5rYbq3xNh8VWHIYJCQ1QxQIxKSP6+uODSYrb2KWyurP1DwGb\n8OYm0J3syEDtCUQik1cpCzpeNlAZ2f8FzXyYQAqPopxdRpsFz8DtZnVvu86XwrE4\noFPl9MReICmZfBNWylpV5qgFPoXyJ70ZAsTm3cEe3n+LBXEnY4YrVDRWxA3wZ2mz\nZ03HZ1hHrxK9CMnS829U+8sK+UneZpCO7yLRPuxwhmps0wpK/YuZZfRAKF1FZRna\nk/SIQ28rnWufmdg16YqqHgl5JOgnb3aslKRvL4dI2Gwnkd2IHtpZnTR0gxFXfqqb\nQwuRAgMBAAGjggIaMIICFjAOBgNVHQ8BAf8EBAMCBaAwHQYDVR0lBBYwFAYIKwYB\nBQUHAwEGCCsGAQUFBwMCMAwGA1UdEwEB/wQCMAAwHQYDVR0OBBYEFLsAFcxAhFX1\nMbCnzr9hEO5rL4jqMB8GA1UdIwQYMBaAFKhKamMEfd265tE5t6ZFZe/zqOyhMHAG\nCCsGAQUFBwEBBGQwYjAvBggrBgEFBQcwAYYjaHR0cDovL29jc3AuaW50LXgzLmxl\ndHNlbmNyeXB0Lm9yZy8wLwYIKwYBBQUHMAKGI2h0dHA6Ly9jZXJ0LmludC14My5s\nZXRzZW5jcnlwdC5vcmcvMCQGA1UdEQQdMBuCGWNsb3VkLmFuZHJld3NvbWV0aGlu\nZy5jb20wgf4GA1UdIASB9jCB8zAIBgZngQwBAgWrgeYGCysGAQQBgt8TAQEBMIHW\nMCYGCCsGAQUFBwIBFhpodHRwOi8vY3BzLmxldHNlbmNyeXB0Lm9yZzCBqwYIKwYB\nBQUHAgIwgZ4MgZtUaGlzIENlcnRpZmljYXRlIG1heSBvbmx5IGJlIHJlbGllZCB1\ncG9uIGJ5IFJlbHlpbmcgUGFydGllcyBhbmQgb25seSQ2ziBhY2NvcmRhbmNlIHdp\ndGggdGhlIENlcnRpZmljYXRlIFBvbGljeSBmb3VuZCBhdCBodHRwczovL2xldHNl\nbmNyeXB0Lm9yZy9yZXBvc2l0b3J5LzANBgkqhkiG9w0BAQsFAAOCAQEAOZVQvrjM\nPKXLARTjB5XsgfyDN3/qwLl7SmwGkPe+B+9FJpfScYG1JzVuCj/SoaPaK34G4x/e\niXwlwOXtMOtqjQYzNu2Pr2C+I+rVmaxIrCUXFmC205IMuUBEeWXG9Y/HvXQLPabD\nD3Gdl5+Feink9SDRP7G0HaAwq13hI7ARxkL9p+UIY39X0dV3WOboW2Re8nrkFXJ7\nq9Z6shK5QgpBfsLjtjNsQzaGV3ve1gOg25aTJGearBWOvEjJNA1wGMoKVXOtYwm/\nWyWoVdCQ8HmconcbJB6xc0UZ1EjvzRr5ZIvSa5uHZD0L3m7/kpPWlAlFJ7hHASPu\nUlF1zblDmg2Iaw==\n-----END CERTIFICATE-----",
            "access_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDBIZMz8pnK6V52\nSVf+CYssOfCQHAx5f0Ou5rYbq3xNh8VHAIYJCQ1QxQIxKSP6+uODSYrb2KWyurP1\nDwGb8OYm0J3syEDtCUQik1cpCzpeNlAZ2f8FzXyYQAqPopxdRpsFz8DtZnVvu86X\nwrE4oFPl9MReICmZfBNWylpV5qgFPoXyJ70ZAsTm3cEe3n+LBXEnY4YrVDRWxA3w\nZ2mzZ03HZ1hHrxK9CMnS829U+8sK+UneZpCO7yLRPuxwhmps0wpK/YuZZfRAKF1F\nZRnak/SIQ28rnWufmdg16YqqHgl5JOgnb3aslKRvL4dI2Gwnkd2IHtpZnTR0gxFX\nfqqbQwuRAgMBAAECggEBAILLmkW0JzOkmLTDNzR0giyRkLoIROqDpfLtjKdwm95l\n9NUBJcU4vCvXQITKt/NhtnNTexcowg8pInb0ksJpg3UGE+4oMNBXVi2UW5MQZ5cm\ncVkQqgXkBF2YAY8FMaB6EML+0En2+dGR/3gIAr221xsFiXe1kHbB8Nb2c/d5HpFt\neRpLVJnK+TxSr78PcZA8DDGlSgwvgimdAaFUNO2OqB9/0E9UPyKk2ycdff/Z6ldF\n0hkCLtdYTTl8Kf/OwjcuTgmA2O3Y8/CoQX/L+oP9Rvt9pWCEfuebiOmHJVPO6Y6x\ngtQVEXwmF1pDHH4Qtz/e6UZTdYeMl9G4aNO2CawwcaYECgYEA57imgSOG4XsJLRh\nGGncV9R/xhy4AbDWLtAMzQRX4ktvKCaHWyQV2XK2we/cu29NLv2Y89WmerTNPOU+\nP8+pB31uty2ELySVn15QhKpQClVEAlxCnnNjXYrii5LOM80+lVmxvQwxVd8Yz8nj\nIntyioXNBEnYS7V2RxxFGgFun1cCgYEA1V3W+Uyamhq8JS5EY0FhyGcXdHd70K49\nW1ou7McIpncf9tM9acLS1hkI98rd2T69Zo8mKoV1V2hjFaKUYfNys6tTkYWeZCcJ\n3rW44j9DTD+FmmjcX6b8DzfybGLehfNbCw6n67/r45DXIV/fk6XZfkx6IEGO4ODt\nNfnvx4TuI1cCgYBACDiKqwSUvmkUuweOo4IuCxyb5Ee8v98P5JIE/VRDxlCbKbpx\npxEam6aBBQVcDi+n8o0H3WjjlKc6UqbW/01YMoMrvzotxNBLz8Y0QtQHZvR6KoCG\nRKCKstxTcWflzKuknbqN4RapAhNbKBDJ8PMSWfyDWNyaXzSmBdvaidbF1QKBgDI0\no4oD0Xkjg1QIYAUu9FBQmb9JAjRnW36saNBEQS/SZg4RRKknM683MtoDvVIKJk0E\nsAlfX+4SXQZRPDMUMtA+Jyrd0xhj6zmhbwClvDMr20crF3fWdgcqtft1BEFmsuyW\nJUMe5OWmRkjPI2+9ncDPRAllA7a8lnSV/Crph5N/AoGBAIK249temKrGe9pmsmAo\nQbNuYSmwpnMoAqdHTrl70HEmK7ob6SIVmsR8QFAkH7xkYZc4Bxbx4h1bdpozGB+/\nAangbiaYJcAOD1QyfiFbflvI1RFeHgrk7VIafeSeQv6qu0LLMi2zUbpgVzxt78Wg\neTuK2xNR0PIM8OI7pRpgyj1I\n-----END PRIVATE KEY-----",
        }
    ],
    maintenance_window=None,
    project_id="9cc10173-e9ea-4176-9dbc-a4cee4c4ff30",
    rules=[
        {
            "uuid": "79f26d28-ea8a-41f2-8ad8-8cfcdd020095",
            "cluster_uuid": "9cc10173-e9ea-4176-9dbc-a4cee4c4ff30",
            "type": "droplet",
            "value": "ff2a6c52-5a44-4b63-b99c-0e98e7a63d61",
            "created_at": "2019-01-11T18:37:36Z",
        }
    ],
    version_end_of_life="2023-11-09T00:00:00Z",
    version_end_of_availability="2023-05-09T00:00:00Z",
    storage_size_mib=61440,
    metrics_endpoints=[
        {
            "host": "backend-do-user-19081923-0.db.ondigitalocean.com",
            "port": 9273,
        }
    ],
    backup_restore={
        "database_name": "backend",
        "backup_created_at": "2019-01-31T19:25:22Z",
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### tags: [`DatabaseClusterTags`](./digital_ocean_python_sdk/type/database_cluster_tags.py)<a id="tags-databaseclustertagsdigital_ocean_python_sdktypedatabase_cluster_tagspy"></a>

##### version: `str`<a id="version-str"></a>

A string representing the version of the database engine in use for the cluster.

##### id: `str`<a id="id-str"></a>

A unique ID that can be used to identify and reference a database cluster.

##### name: `str`<a id="name-str"></a>

A unique, human-readable name referring to a database cluster.

##### engine: `str`<a id="engine-str"></a>

A slug representing the database engine used for the cluster. The possible values are: \\\"pg\\\" for PostgreSQL, \\\"mysql\\\" for MySQL, \\\"redis\\\" for Redis, \\\"mongodb\\\" for MongoDB, and \\\"kafka\\\" for Kafka.

##### semantic_version: `str`<a id="semantic_version-str"></a>

A string representing the semantic version of the database engine in use for the cluster.

##### num_nodes: `int`<a id="num_nodes-int"></a>

The number of nodes in the database cluster.

##### size: `str`<a id="size-str"></a>

The slug identifier representing the size of the nodes in the database cluster.

##### region: `str`<a id="region-str"></a>

The slug identifier for the region where the database cluster is located.

##### status: `str`<a id="status-str"></a>

A string representing the current status of the database cluster.

##### created_at: `datetime`<a id="created_at-datetime"></a>

A time value given in ISO8601 combined date and time format that represents when the database cluster was created.

##### private_network_uuid: `str`<a id="private_network_uuid-str"></a>

A string specifying the UUID of the VPC to which the database cluster will be assigned. If excluded, the cluster when creating a new database cluster, it will be assigned to your account's default VPC for the region.

##### db_names: [`DatabaseClusterDbNames`](./digital_ocean_python_sdk/type/database_cluster_db_names.py)<a id="db_names-databaseclusterdbnamesdigital_ocean_python_sdktypedatabase_cluster_db_namespy"></a>

##### connection: Union[`DatabaseConnection`, [`Union[bool, date, datetime, dict, float, int, list, str, None]`](./digital_ocean_python_sdk/type/typing_union_bool_date_datetime_dict_float_int_list_str_none.py)]<a id="connection-uniondatabaseconnection-unionbool-date-datetime-dict-float-int-list-str-nonedigital_ocean_python_sdktypetyping_union_bool_date_datetime_dict_float_int_list_str_nonepy"></a>


##### private_connection: Union[`DatabaseConnection`, [`Union[bool, date, datetime, dict, float, int, list, str, None]`](./digital_ocean_python_sdk/type/typing_union_bool_date_datetime_dict_float_int_list_str_none.py)]<a id="private_connection-uniondatabaseconnection-unionbool-date-datetime-dict-float-int-list-str-nonedigital_ocean_python_sdktypetyping_union_bool_date_datetime_dict_float_int_list_str_nonepy"></a>


##### standby_connection: Union[`DatabaseConnection`, [`Union[bool, date, datetime, dict, float, int, list, str, None]`](./digital_ocean_python_sdk/type/typing_union_bool_date_datetime_dict_float_int_list_str_none.py)]<a id="standby_connection-uniondatabaseconnection-unionbool-date-datetime-dict-float-int-list-str-nonedigital_ocean_python_sdktypetyping_union_bool_date_datetime_dict_float_int_list_str_nonepy"></a>


##### standby_private_connection: Union[`DatabaseConnection`, [`Union[bool, date, datetime, dict, float, int, list, str, None]`](./digital_ocean_python_sdk/type/typing_union_bool_date_datetime_dict_float_int_list_str_none.py)]<a id="standby_private_connection-uniondatabaseconnection-unionbool-date-datetime-dict-float-int-list-str-nonedigital_ocean_python_sdktypetyping_union_bool_date_datetime_dict_float_int_list_str_nonepy"></a>


##### users: List[`DatabaseUser`]<a id="users-listdatabaseuser"></a>

##### maintenance_window: Union[`DatabaseMaintenanceWindow`, [`Union[bool, date, datetime, dict, float, int, list, str, None]`](./digital_ocean_python_sdk/type/typing_union_bool_date_datetime_dict_float_int_list_str_none.py)]<a id="maintenance_window-uniondatabasemaintenancewindow-unionbool-date-datetime-dict-float-int-list-str-nonedigital_ocean_python_sdktypetyping_union_bool_date_datetime_dict_float_int_list_str_nonepy"></a>


##### project_id: `str`<a id="project_id-str"></a>

The ID of the project that the database cluster is assigned to. If excluded when creating a new database cluster, it will be assigned to your default project.

##### rules: List[`FirewallRule`]<a id="rules-listfirewallrule"></a>

##### version_end_of_life: `str`<a id="version_end_of_life-str"></a>

A timestamp referring to the date when the particular version will no longer be supported. If null, the version does not have an end of life timeline.

##### version_end_of_availability: `str`<a id="version_end_of_availability-str"></a>

A timestamp referring to the date when the particular version will no longer be available for creating new clusters. If null, the version does not have an end of availability timeline.

##### storage_size_mib: `int`<a id="storage_size_mib-int"></a>

Additional storage added to the cluster, in MiB. If null, no additional storage is added to the cluster, beyond what is provided as a base amount from the 'size' and any previously added additional storage.

##### metrics_endpoints: List[`DatabaseServiceEndpoint`]<a id="metrics_endpoints-listdatabaseserviceendpoint"></a>

Public hostname and port of the cluster's metrics endpoint(s). Includes one record for the cluster's primary node and a second entry for the cluster's standby node(s).

##### backup_restore: [`DatabaseBackup`](./digital_ocean_python_sdk/type/database_backup.py)<a id="backup_restore-databasebackupdigital_ocean_python_sdktypedatabase_backuppy"></a>


#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`DatabasesCreateClusterRequest`](./digital_ocean_python_sdk/type/databases_create_cluster_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`DatabasesCreateClusterResponse`](./digital_ocean_python_sdk/pydantic/databases_create_cluster_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/databases` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.databases.create_read_only_replica`<a id="digitaloceandatabasescreate_read_only_replica"></a>

To create a read-only replica for a PostgreSQL or MySQL database cluster, send a POST request to `/v2/databases/$DATABASE_ID/replicas` specifying the name it should be given, the size of the node to be used, and the region where it will be located.

**Note**: Read-only replicas are not supported for Redis clusters.

The response will be a JSON object with a key called `replica`. The value of this will be an object that contains the standard attributes associated with a database replica. The initial value of the read-only replica's `status` attribute will be `forking`. When the replica is ready to receive traffic, this will transition to `active`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_read_only_replica_response = digitalocean.databases.create_read_only_replica(
    name="read-nyc3-01",
    database_cluster_uuid="9cc10173-e9ea-4176-9dbc-a4cee4c4ff30",
    tags=["production"],
    id="9cc10173-e9ea-4176-9dbc-a4cee4c4ff30",
    region="nyc3",
    size="db-s-2vcpu-4gb",
    status="creating",
    created_at="2019-01-11T18:37:36Z",
    private_network_uuid="9423cbad-9211-442f-820b-ef6915e99b5f",
    connection=None,
    private_connection=None,
    storage_size_mib=61440,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### name: `str`<a id="name-str"></a>

The name to give the read-only replicating

##### database_cluster_uuid: `str`<a id="database_cluster_uuid-str"></a>

A unique identifier for a database cluster.

##### tags: [`DatabaseReplicaTags`](./digital_ocean_python_sdk/type/database_replica_tags.py)<a id="tags-databasereplicatagsdigital_ocean_python_sdktypedatabase_replica_tagspy"></a>

##### id: `str`<a id="id-str"></a>

A unique ID that can be used to identify and reference a database replica.

##### region: `str`<a id="region-str"></a>

A slug identifier for the region where the read-only replica will be located. If excluded, the replica will be placed in the same region as the cluster.

##### size: `str`<a id="size-str"></a>

A slug identifier representing the size of the node for the read-only replica. The size of the replica must be at least as large as the node size for the database cluster from which it is replicating.

##### status: `str`<a id="status-str"></a>

A string representing the current status of the database cluster.

##### created_at: `datetime`<a id="created_at-datetime"></a>

A time value given in ISO8601 combined date and time format that represents when the database cluster was created.

##### private_network_uuid: `str`<a id="private_network_uuid-str"></a>

A string specifying the UUID of the VPC to which the read-only replica will be assigned. If excluded, the replica will be assigned to your account's default VPC for the region.

##### connection: Union[[`Union[bool, date, datetime, dict, float, int, list, str, None]`](./digital_ocean_python_sdk/type/typing_union_bool_date_datetime_dict_float_int_list_str_none.py), `DatabaseConnection`]<a id="connection-unionunionbool-date-datetime-dict-float-int-list-str-nonedigital_ocean_python_sdktypetyping_union_bool_date_datetime_dict_float_int_list_str_nonepy-databaseconnection"></a>


##### private_connection: Union[[`Union[bool, date, datetime, dict, float, int, list, str, None]`](./digital_ocean_python_sdk/type/typing_union_bool_date_datetime_dict_float_int_list_str_none.py), `DatabaseConnection`]<a id="private_connection-unionunionbool-date-datetime-dict-float-int-list-str-nonedigital_ocean_python_sdktypetyping_union_bool_date_datetime_dict_float_int_list_str_nonepy-databaseconnection"></a>


##### storage_size_mib: `int`<a id="storage_size_mib-int"></a>

Additional storage added to the cluster, in MiB. If null, no additional storage is added to the cluster, beyond what is provided as a base amount from the 'size' and any previously added additional storage.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`DatabaseReplica`](./digital_ocean_python_sdk/type/database_replica.py)
#### 🔄 Return<a id="🔄-return"></a>

[`DatabasesCreateReadOnlyReplicaResponse`](./digital_ocean_python_sdk/pydantic/databases_create_read_only_replica_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/databases/{database_cluster_uuid}/replicas` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.databases.create_topic_kafka_cluster`<a id="digitaloceandatabasescreate_topic_kafka_cluster"></a>

To create a topic attached to a Kafka cluster, send a POST request to
`/v2/databases/$DATABASE_ID/topics`.

The result will be a JSON object with a `topic` key.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_topic_kafka_cluster_response = digitalocean.databases.create_topic_kafka_cluster(
    database_cluster_uuid="9cc10173-e9ea-4176-9dbc-a4cee4c4ff30",
    name="events",
    replication_factor=2,
    partition_count=3,
    config={
        "cleanup_policy": "delete",
        "compression_type": "producer",
        "delete_retention_ms": 86400000,
        "file_delete_delay_ms": 60000,
        "flush_messages": 9223372036854776000,
        "flush_ms": 9223372036854776000,
        "index_interval_bytes": 4096,
        "max_compaction_lag_ms": 9223372036854776000,
        "max_message_bytes": 1048588,
        "message_down_conversion_enable": True,
        "message_format_version": "3.0-IV1",
        "message_timestamp_type": "create_time",
        "min_cleanable_dirty_ratio": 0.5,
        "min_compaction_lag_ms": 0,
        "min_insync_replicas": 1,
        "preallocate": False,
        "retention_bytes": 1000000,
        "retention_ms": 604800000,
        "segment_bytes": 209715200,
        "segment_jitter_ms": 0,
        "segment_ms": 604800000,
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### database_cluster_uuid: `str`<a id="database_cluster_uuid-str"></a>

A unique identifier for a database cluster.

##### name: `str`<a id="name-str"></a>

The name of the Kafka topic.

##### replication_factor: `int`<a id="replication_factor-int"></a>

The number of nodes to replicate data across the cluster.

##### partition_count: `int`<a id="partition_count-int"></a>

The number of partitions available for the topic. On update, this value can only be increased.

##### config: [`KafkaTopicConfig`](./digital_ocean_python_sdk/type/kafka_topic_config.py)<a id="config-kafkatopicconfigdigital_ocean_python_sdktypekafka_topic_configpy"></a>


#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`KafkaTopicCreate`](./digital_ocean_python_sdk/type/kafka_topic_create.py)
#### 🔄 Return<a id="🔄-return"></a>

[`DatabasesCreateTopicKafkaClusterResponse`](./digital_ocean_python_sdk/pydantic/databases_create_topic_kafka_cluster_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/databases/{database_cluster_uuid}/topics` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.databases.delete`<a id="digitaloceandatabasesdelete"></a>

To delete a specific database, send a DELETE request to
`/v2/databases/$DATABASE_ID/dbs/$DB_NAME`.

A status of 204 will be given. This indicates that the request was processed
successfully, but that no response body is needed.

Note: Database management is not supported for Redis clusters.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.databases.delete(
    database_cluster_uuid="9cc10173-e9ea-4176-9dbc-a4cee4c4ff30",
    database_name="alpha",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### database_cluster_uuid: `str`<a id="database_cluster_uuid-str"></a>

A unique identifier for a database cluster.

##### database_name: `str`<a id="database_name-str"></a>

The name of the database.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/databases/{database_cluster_uuid}/dbs/{database_name}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.databases.delete_connection_pool`<a id="digitaloceandatabasesdelete_connection_pool"></a>

To delete a specific connection pool for a PostgreSQL database cluster, send
a DELETE request to `/v2/databases/$DATABASE_ID/pools/$POOL_NAME`.

A status of 204 will be given. This indicates that the request was processed
successfully, but that no response body is needed.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.databases.delete_connection_pool(
    database_cluster_uuid="9cc10173-e9ea-4176-9dbc-a4cee4c4ff30",
    pool_name="backend-pool",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### database_cluster_uuid: `str`<a id="database_cluster_uuid-str"></a>

A unique identifier for a database cluster.

##### pool_name: `str`<a id="pool_name-str"></a>

The name used to identify the connection pool.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/databases/{database_cluster_uuid}/pools/{pool_name}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.databases.delete_topic_kafka_cluster`<a id="digitaloceandatabasesdelete_topic_kafka_cluster"></a>

To delete a single topic within a Kafka cluster, send a DELETE request
to `/v2/databases/$DATABASE_ID/topics/$TOPIC_NAME`.

A status of 204 will be given. This indicates that the request was
processed successfully, but that no response body is needed.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.databases.delete_topic_kafka_cluster(
    database_cluster_uuid="9cc10173-e9ea-4176-9dbc-a4cee4c4ff30",
    topic_name="customer-events",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### database_cluster_uuid: `str`<a id="database_cluster_uuid-str"></a>

A unique identifier for a database cluster.

##### topic_name: `str`<a id="topic_name-str"></a>

The name used to identify the Kafka topic.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/databases/{database_cluster_uuid}/topics/{topic_name}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.databases.destroy_cluster`<a id="digitaloceandatabasesdestroy_cluster"></a>

To destroy a specific database, send a DELETE request to `/v2/databases/$DATABASE_ID`.
A status of 204 will be given. This indicates that the request was processed successfully, but that no response body is needed.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.databases.destroy_cluster(
    database_cluster_uuid="9cc10173-e9ea-4176-9dbc-a4cee4c4ff30",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### database_cluster_uuid: `str`<a id="database_cluster_uuid-str"></a>

A unique identifier for a database cluster.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/databases/{database_cluster_uuid}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.databases.destroy_readonly_replica`<a id="digitaloceandatabasesdestroy_readonly_replica"></a>

To destroy a specific read-only replica, send a DELETE request to `/v2/databases/$DATABASE_ID/replicas/$REPLICA_NAME`.

**Note**: Read-only replicas are not supported for Redis clusters.

A status of 204 will be given. This indicates that the request was processed successfully, but that no response body is needed.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.databases.destroy_readonly_replica(
    database_cluster_uuid="9cc10173-e9ea-4176-9dbc-a4cee4c4ff30",
    replica_name="read-nyc3-01",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### database_cluster_uuid: `str`<a id="database_cluster_uuid-str"></a>

A unique identifier for a database cluster.

##### replica_name: `str`<a id="replica_name-str"></a>

The name of the database replica.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/databases/{database_cluster_uuid}/replicas/{replica_name}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.databases.get`<a id="digitaloceandatabasesget"></a>

To show information about an existing database cluster, send a GET request to
`/v2/databases/$DATABASE_ID/dbs/$DB_NAME`.

Note: Database management is not supported for Redis clusters.

The response will be a JSON object with a `db` key. This will be set to an object
containing the standard database attributes.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_response = digitalocean.databases.get(
    database_cluster_uuid="9cc10173-e9ea-4176-9dbc-a4cee4c4ff30",
    database_name="alpha",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### database_cluster_uuid: `str`<a id="database_cluster_uuid-str"></a>

A unique identifier for a database cluster.

##### database_name: `str`<a id="database_name-str"></a>

The name of the database.

#### 🔄 Return<a id="🔄-return"></a>

[`DatabasesAddResponse`](./digital_ocean_python_sdk/pydantic/databases_add_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/databases/{database_cluster_uuid}/dbs/{database_name}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.databases.get_cluster_config`<a id="digitaloceandatabasesget_cluster_config"></a>

Shows configuration parameters for an existing database cluster by sending a GET request to
`/v2/databases/$DATABASE_ID/config`.
The response is a JSON object with a `config` key, which is set to an object
containing any database configuration parameters.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_cluster_config_response = digitalocean.databases.get_cluster_config(
    database_cluster_uuid="9cc10173-e9ea-4176-9dbc-a4cee4c4ff30",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### database_cluster_uuid: `str`<a id="database_cluster_uuid-str"></a>

A unique identifier for a database cluster.

#### 🔄 Return<a id="🔄-return"></a>

[`DatabasesGetClusterConfigResponse`](./digital_ocean_python_sdk/pydantic/databases_get_cluster_config_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/databases/{database_cluster_uuid}/config` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.databases.get_cluster_info`<a id="digitaloceandatabasesget_cluster_info"></a>

To show information about an existing database cluster, send a GET request to `/v2/databases/$DATABASE_ID`.

The response will be a JSON object with a database key. This will be set to an object containing the standard database cluster attributes.

The embedded `connection` and `private_connection` objects will contain the information needed to access the database cluster. For multi-node clusters, the `standby_connection` and `standby_private_connection` objects contain the information needed to connect to the cluster's standby node(s).

The embedded maintenance_window object will contain information about any scheduled maintenance for the database cluster.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_cluster_info_response = digitalocean.databases.get_cluster_info(
    database_cluster_uuid="9cc10173-e9ea-4176-9dbc-a4cee4c4ff30",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### database_cluster_uuid: `str`<a id="database_cluster_uuid-str"></a>

A unique identifier for a database cluster.

#### 🔄 Return<a id="🔄-return"></a>

[`DatabasesCreateClusterResponse`](./digital_ocean_python_sdk/pydantic/databases_create_cluster_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/databases/{database_cluster_uuid}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.databases.get_clusters_metrics_credentials`<a id="digitaloceandatabasesget_clusters_metrics_credentials"></a>

To show the credentials for all database clusters' metrics endpoints, send a GET request to `/v2/databases/metrics/credentials`. The result will be a JSON object with a `credentials` key.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_clusters_metrics_credentials_response = digitalocean.databases.get_clusters_metrics_credentials()
```

#### 🔄 Return<a id="🔄-return"></a>

[`DatabasesGetClustersMetricsCredentialsResponse`](./digital_ocean_python_sdk/pydantic/databases_get_clusters_metrics_credentials_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/databases/metrics/credentials` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.databases.get_connection_pool`<a id="digitaloceandatabasesget_connection_pool"></a>

To show information about an existing connection pool for a PostgreSQL database cluster, send a GET request to `/v2/databases/$DATABASE_ID/pools/$POOL_NAME`.
The response will be a JSON object with a `pool` key.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_connection_pool_response = digitalocean.databases.get_connection_pool(
    database_cluster_uuid="9cc10173-e9ea-4176-9dbc-a4cee4c4ff30",
    pool_name="backend-pool",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### database_cluster_uuid: `str`<a id="database_cluster_uuid-str"></a>

A unique identifier for a database cluster.

##### pool_name: `str`<a id="pool_name-str"></a>

The name used to identify the connection pool.

#### 🔄 Return<a id="🔄-return"></a>

[`DatabasesAddNewConnectionPoolResponse`](./digital_ocean_python_sdk/pydantic/databases_add_new_connection_pool_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/databases/{database_cluster_uuid}/pools/{pool_name}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.databases.get_eviction_policy`<a id="digitaloceandatabasesget_eviction_policy"></a>

To retrieve the configured eviction policy for an existing Redis cluster, send a GET request to `/v2/databases/$DATABASE_ID/eviction_policy`.
The response will be a JSON object with an `eviction_policy` key. This will be set to a string representing the eviction policy.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_eviction_policy_response = digitalocean.databases.get_eviction_policy(
    database_cluster_uuid="9cc10173-e9ea-4176-9dbc-a4cee4c4ff30",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### database_cluster_uuid: `str`<a id="database_cluster_uuid-str"></a>

A unique identifier for a database cluster.

#### 🔄 Return<a id="🔄-return"></a>

[`DatabasesGetEvictionPolicyResponse`](./digital_ocean_python_sdk/pydantic/databases_get_eviction_policy_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/databases/{database_cluster_uuid}/eviction_policy` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.databases.get_existing_read_only_replica`<a id="digitaloceandatabasesget_existing_read_only_replica"></a>

To show information about an existing database replica, send a GET request to `/v2/databases/$DATABASE_ID/replicas/$REPLICA_NAME`.

**Note**: Read-only replicas are not supported for Redis clusters.

The response will be a JSON object with a `replica key`. This will be set to an object containing the standard database replica attributes.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_existing_read_only_replica_response = digitalocean.databases.get_existing_read_only_replica(
    database_cluster_uuid="9cc10173-e9ea-4176-9dbc-a4cee4c4ff30",
    replica_name="read-nyc3-01",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### database_cluster_uuid: `str`<a id="database_cluster_uuid-str"></a>

A unique identifier for a database cluster.

##### replica_name: `str`<a id="replica_name-str"></a>

The name of the database replica.

#### 🔄 Return<a id="🔄-return"></a>

[`DatabasesCreateReadOnlyReplicaResponse`](./digital_ocean_python_sdk/pydantic/databases_create_read_only_replica_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/databases/{database_cluster_uuid}/replicas/{replica_name}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.databases.get_migration_status`<a id="digitaloceandatabasesget_migration_status"></a>

To retrieve the status of the most recent online migration, send a GET request to `/v2/databases/$DATABASE_ID/online-migration`. 

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_migration_status_response = digitalocean.databases.get_migration_status(
    database_cluster_uuid="9cc10173-e9ea-4176-9dbc-a4cee4c4ff30",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### database_cluster_uuid: `str`<a id="database_cluster_uuid-str"></a>

A unique identifier for a database cluster.

#### 🔄 Return<a id="🔄-return"></a>

[`OnlineMigration`](./digital_ocean_python_sdk/pydantic/online_migration.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/databases/{database_cluster_uuid}/online-migration` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.databases.get_public_certificate`<a id="digitaloceandatabasesget_public_certificate"></a>

To retrieve the public certificate used to secure the connection to the database cluster send a GET request to
`/v2/databases/$DATABASE_ID/ca`.

The response will be a JSON object with a `ca` key. This will be set to an object
containing the base64 encoding of the public key certificate.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_public_certificate_response = digitalocean.databases.get_public_certificate(
    database_cluster_uuid="9cc10173-e9ea-4176-9dbc-a4cee4c4ff30",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### database_cluster_uuid: `str`<a id="database_cluster_uuid-str"></a>

A unique identifier for a database cluster.

#### 🔄 Return<a id="🔄-return"></a>

[`DatabasesGetPublicCertificateResponse`](./digital_ocean_python_sdk/pydantic/databases_get_public_certificate_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/databases/{database_cluster_uuid}/ca` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.databases.get_sql_mode`<a id="digitaloceandatabasesget_sql_mode"></a>

To retrieve the configured SQL modes for an existing MySQL cluster, send a GET request to `/v2/databases/$DATABASE_ID/sql_mode`.
The response will be a JSON object with a `sql_mode` key. This will be set to a string representing the configured SQL modes.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_sql_mode_response = digitalocean.databases.get_sql_mode(
    database_cluster_uuid="9cc10173-e9ea-4176-9dbc-a4cee4c4ff30",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### database_cluster_uuid: `str`<a id="database_cluster_uuid-str"></a>

A unique identifier for a database cluster.

#### 🔄 Return<a id="🔄-return"></a>

[`SqlMode`](./digital_ocean_python_sdk/pydantic/sql_mode.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/databases/{database_cluster_uuid}/sql_mode` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.databases.get_topic_kafka_cluster`<a id="digitaloceandatabasesget_topic_kafka_cluster"></a>

To retrieve a given topic by name from the set of a Kafka cluster's topics,
send a GET request to `/v2/databases/$DATABASE_ID/topics/$TOPIC_NAME`.

The result will be a JSON object with a `topic` key.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_topic_kafka_cluster_response = digitalocean.databases.get_topic_kafka_cluster(
    database_cluster_uuid="9cc10173-e9ea-4176-9dbc-a4cee4c4ff30",
    topic_name="customer-events",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### database_cluster_uuid: `str`<a id="database_cluster_uuid-str"></a>

A unique identifier for a database cluster.

##### topic_name: `str`<a id="topic_name-str"></a>

The name used to identify the Kafka topic.

#### 🔄 Return<a id="🔄-return"></a>

[`DatabasesCreateTopicKafkaClusterResponse`](./digital_ocean_python_sdk/pydantic/databases_create_topic_kafka_cluster_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/databases/{database_cluster_uuid}/topics/{topic_name}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.databases.get_user`<a id="digitaloceandatabasesget_user"></a>

To show information about an existing database user, send a GET request to
`/v2/databases/$DATABASE_ID/users/$USERNAME`.

Note: User management is not supported for Redis clusters.

The response will be a JSON object with a `user` key. This will be set to an object
containing the standard database user attributes.

For MySQL clusters, additional options will be contained in the `mysql_settings`
object.

For Kafka clusters, additional options will be contained in the `settings` object.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_user_response = digitalocean.databases.get_user(
    database_cluster_uuid="9cc10173-e9ea-4176-9dbc-a4cee4c4ff30",
    username="app-01",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### database_cluster_uuid: `str`<a id="database_cluster_uuid-str"></a>

A unique identifier for a database cluster.

##### username: `str`<a id="username-str"></a>

The name of the database user.

#### 🔄 Return<a id="🔄-return"></a>

[`DatabasesAddUserResponse`](./digital_ocean_python_sdk/pydantic/databases_add_user_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/databases/{database_cluster_uuid}/users/{username}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.databases.list`<a id="digitaloceandatabaseslist"></a>

To list all of the databases in a clusters, send a GET request to
`/v2/databases/$DATABASE_ID/dbs`.

The result will be a JSON object with a `dbs` key. This will be set to an array
of database objects, each of which will contain the standard database attributes.

Note: Database management is not supported for Redis clusters.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = digitalocean.databases.list(
    database_cluster_uuid="9cc10173-e9ea-4176-9dbc-a4cee4c4ff30",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### database_cluster_uuid: `str`<a id="database_cluster_uuid-str"></a>

A unique identifier for a database cluster.

#### 🔄 Return<a id="🔄-return"></a>

[`DatabasesListResponse`](./digital_ocean_python_sdk/pydantic/databases_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/databases/{database_cluster_uuid}/dbs` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.databases.list_backups`<a id="digitaloceandatabaseslist_backups"></a>

To list all of the available backups of a PostgreSQL or MySQL database cluster, send a GET request to `/v2/databases/$DATABASE_ID/backups`.
**Note**: Backups are not supported for Redis clusters.
The result will be a JSON object with a `backups key`. This will be set to an array of backup objects, each of which will contain the size of the backup and the timestamp at which it was created.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_backups_response = digitalocean.databases.list_backups(
    database_cluster_uuid="9cc10173-e9ea-4176-9dbc-a4cee4c4ff30",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### database_cluster_uuid: `str`<a id="database_cluster_uuid-str"></a>

A unique identifier for a database cluster.

#### 🔄 Return<a id="🔄-return"></a>

[`DatabasesListBackupsResponse`](./digital_ocean_python_sdk/pydantic/databases_list_backups_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/databases/{database_cluster_uuid}/backups` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.databases.list_clusters`<a id="digitaloceandatabaseslist_clusters"></a>

To list all of the database clusters available on your account, send a GET request to `/v2/databases`. To limit the results to database clusters with a specific tag, include the `tag_name` query parameter set to the name of the tag. For example, `/v2/databases?tag_name=$TAG_NAME`.

The result will be a JSON object with a `databases` key. This will be set to an array of database objects, each of which will contain the standard database attributes.

The embedded `connection` and `private_connection` objects will contain the information needed to access the database cluster. For multi-node clusters, the `standby_connection` and `standby_private_connection` objects will contain the information needed to connect to the cluster's standby node(s).

The embedded `maintenance_window` object will contain information about any scheduled maintenance for the database cluster.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_clusters_response = digitalocean.databases.list_clusters(
    tag_name="production",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### tag_name: `str`<a id="tag_name-str"></a>

Limits the results to database clusters with a specific tag.

#### 🔄 Return<a id="🔄-return"></a>

[`DatabasesListClustersResponse`](./digital_ocean_python_sdk/pydantic/databases_list_clusters_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/databases` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.databases.list_connection_pools`<a id="digitaloceandatabaseslist_connection_pools"></a>

To list all of the connection pools available to a PostgreSQL database cluster, send a GET request to `/v2/databases/$DATABASE_ID/pools`.
The result will be a JSON object with a `pools` key. This will be set to an array of connection pool objects.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_connection_pools_response = digitalocean.databases.list_connection_pools(
    database_cluster_uuid="9cc10173-e9ea-4176-9dbc-a4cee4c4ff30",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### database_cluster_uuid: `str`<a id="database_cluster_uuid-str"></a>

A unique identifier for a database cluster.

#### 🔄 Return<a id="🔄-return"></a>

[`ConnectionPools`](./digital_ocean_python_sdk/pydantic/connection_pools.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/databases/{database_cluster_uuid}/pools` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.databases.list_events_logs`<a id="digitaloceandatabaseslist_events_logs"></a>

To list all of the cluster events, send a GET request to
`/v2/databases/$DATABASE_ID/events`.

The result will be a JSON object with a `events` key.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_events_logs_response = digitalocean.databases.list_events_logs(
    database_cluster_uuid="9cc10173-e9ea-4176-9dbc-a4cee4c4ff30",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### database_cluster_uuid: `str`<a id="database_cluster_uuid-str"></a>

A unique identifier for a database cluster.

#### 🔄 Return<a id="🔄-return"></a>

[`DatabasesListEventsLogsResponse`](./digital_ocean_python_sdk/pydantic/databases_list_events_logs_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/databases/{database_cluster_uuid}/events` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.databases.list_firewall_rules`<a id="digitaloceandatabaseslist_firewall_rules"></a>

To list all of a database cluster's firewall rules (known as "trusted sources" in the control panel), send a GET request to `/v2/databases/$DATABASE_ID/firewall`.
The result will be a JSON object with a `rules` key.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_firewall_rules_response = digitalocean.databases.list_firewall_rules(
    database_cluster_uuid="9cc10173-e9ea-4176-9dbc-a4cee4c4ff30",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### database_cluster_uuid: `str`<a id="database_cluster_uuid-str"></a>

A unique identifier for a database cluster.

#### 🔄 Return<a id="🔄-return"></a>

[`DatabasesListFirewallRulesResponse`](./digital_ocean_python_sdk/pydantic/databases_list_firewall_rules_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/databases/{database_cluster_uuid}/firewall` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.databases.list_options`<a id="digitaloceandatabaseslist_options"></a>

To list all of the options available for the offered database engines, send a GET request to `/v2/databases/options`.
The result will be a JSON object with an `options` key.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_options_response = digitalocean.databases.list_options()
```

#### 🔄 Return<a id="🔄-return"></a>

[`Options`](./digital_ocean_python_sdk/pydantic/options.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/databases/options` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.databases.list_read_only_replicas`<a id="digitaloceandatabaseslist_read_only_replicas"></a>

To list all of the read-only replicas associated with a database cluster, send a GET request to `/v2/databases/$DATABASE_ID/replicas`.

**Note**: Read-only replicas are not supported for Redis clusters.

The result will be a JSON object with a `replicas` key. This will be set to an array of database replica objects, each of which will contain the standard database replica attributes.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_read_only_replicas_response = digitalocean.databases.list_read_only_replicas(
    database_cluster_uuid="9cc10173-e9ea-4176-9dbc-a4cee4c4ff30",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### database_cluster_uuid: `str`<a id="database_cluster_uuid-str"></a>

A unique identifier for a database cluster.

#### 🔄 Return<a id="🔄-return"></a>

[`DatabasesListReadOnlyReplicasResponse`](./digital_ocean_python_sdk/pydantic/databases_list_read_only_replicas_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/databases/{database_cluster_uuid}/replicas` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.databases.list_topics_kafka_cluster`<a id="digitaloceandatabaseslist_topics_kafka_cluster"></a>

To list all of a Kafka cluster's topics, send a GET request to
`/v2/databases/$DATABASE_ID/topics`.

The result will be a JSON object with a `topics` key.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_topics_kafka_cluster_response = digitalocean.databases.list_topics_kafka_cluster(
    database_cluster_uuid="9cc10173-e9ea-4176-9dbc-a4cee4c4ff30",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### database_cluster_uuid: `str`<a id="database_cluster_uuid-str"></a>

A unique identifier for a database cluster.

#### 🔄 Return<a id="🔄-return"></a>

[`DatabasesListTopicsKafkaClusterResponse`](./digital_ocean_python_sdk/pydantic/databases_list_topics_kafka_cluster_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/databases/{database_cluster_uuid}/topics` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.databases.list_users`<a id="digitaloceandatabaseslist_users"></a>

To list all of the users for your database cluster, send a GET request to
`/v2/databases/$DATABASE_ID/users`.

Note: User management is not supported for Redis clusters.

The result will be a JSON object with a `users` key. This will be set to an array
of database user objects, each of which will contain the standard database user attributes.

For MySQL clusters, additional options will be contained in the mysql_settings object.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_users_response = digitalocean.databases.list_users(
    database_cluster_uuid="9cc10173-e9ea-4176-9dbc-a4cee4c4ff30",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### database_cluster_uuid: `str`<a id="database_cluster_uuid-str"></a>

A unique identifier for a database cluster.

#### 🔄 Return<a id="🔄-return"></a>

[`DatabasesListUsersResponse`](./digital_ocean_python_sdk/pydantic/databases_list_users_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/databases/{database_cluster_uuid}/users` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.databases.migrate_cluster_to_new_region`<a id="digitaloceandatabasesmigrate_cluster_to_new_region"></a>

To migrate a database cluster to a new region, send a `PUT` request to
`/v2/databases/$DATABASE_ID/migrate`. The body of the request must specify a
`region` attribute.

A successful request will receive a 202 Accepted status code with no body in
response. Querying the database cluster will show that its `status` attribute
will now be set to `migrating`. This will transition back to `online` when the
migration has completed.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.databases.migrate_cluster_to_new_region(
    region="lon1",
    database_cluster_uuid="9cc10173-e9ea-4176-9dbc-a4cee4c4ff30",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### region: `str`<a id="region-str"></a>

A slug identifier for the region to which the database cluster will be migrated.

##### database_cluster_uuid: `str`<a id="database_cluster_uuid-str"></a>

A unique identifier for a database cluster.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`DatabasesMigrateClusterToNewRegionRequest`](./digital_ocean_python_sdk/type/databases_migrate_cluster_to_new_region_request.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/databases/{database_cluster_uuid}/migrate` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.databases.promote_readonly_replica_to_primary`<a id="digitaloceandatabasespromote_readonly_replica_to_primary"></a>

To promote a specific read-only replica, send a PUT request to `/v2/databases/$DATABASE_ID/replicas/$REPLICA_NAME/promote`.

**Note**: Read-only replicas are not supported for Redis clusters.

A status of 204 will be given. This indicates that the request was processed successfully, but that no response body is needed.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.databases.promote_readonly_replica_to_primary(
    database_cluster_uuid="9cc10173-e9ea-4176-9dbc-a4cee4c4ff30",
    replica_name="read-nyc3-01",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### database_cluster_uuid: `str`<a id="database_cluster_uuid-str"></a>

A unique identifier for a database cluster.

##### replica_name: `str`<a id="replica_name-str"></a>

The name of the database replica.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/databases/{database_cluster_uuid}/replicas/{replica_name}/promote` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.databases.remove_user`<a id="digitaloceandatabasesremove_user"></a>

To remove a specific database user, send a DELETE request to
`/v2/databases/$DATABASE_ID/users/$USERNAME`.

A status of 204 will be given. This indicates that the request was processed
successfully, but that no response body is needed.

Note: User management is not supported for Redis clusters.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.databases.remove_user(
    database_cluster_uuid="9cc10173-e9ea-4176-9dbc-a4cee4c4ff30",
    username="app-01",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### database_cluster_uuid: `str`<a id="database_cluster_uuid-str"></a>

A unique identifier for a database cluster.

##### username: `str`<a id="username-str"></a>

The name of the database user.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/databases/{database_cluster_uuid}/users/{username}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.databases.reset_user_auth`<a id="digitaloceandatabasesreset_user_auth"></a>

To reset the password for a database user, send a POST request to
`/v2/databases/$DATABASE_ID/users/$USERNAME/reset_auth`.

For `mysql` databases, the authentication method can be specifying by
including a key in the JSON body called `mysql_settings` with the `auth_plugin`
value specified.

The response will be a JSON object with a `user` key. This will be set to an
object containing the standard database user attributes.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
reset_user_auth_response = digitalocean.databases.reset_user_auth(
    database_cluster_uuid="9cc10173-e9ea-4176-9dbc-a4cee4c4ff30",
    username="app-01",
    mysql_settings={
        "auth_plugin": "mysql_native_password",
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### database_cluster_uuid: `str`<a id="database_cluster_uuid-str"></a>

A unique identifier for a database cluster.

##### username: `str`<a id="username-str"></a>

The name of the database user.

##### mysql_settings: [`MysqlSettings`](./digital_ocean_python_sdk/type/mysql_settings.py)<a id="mysql_settings-mysqlsettingsdigital_ocean_python_sdktypemysql_settingspy"></a>


#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`DatabasesResetUserAuthRequest`](./digital_ocean_python_sdk/type/databases_reset_user_auth_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`DatabasesAddUserResponse`](./digital_ocean_python_sdk/pydantic/databases_add_user_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/databases/{database_cluster_uuid}/users/{username}/reset_auth` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.databases.resize_cluster`<a id="digitaloceandatabasesresize_cluster"></a>

To resize a database cluster, send a PUT request to `/v2/databases/$DATABASE_ID/resize`. The body of the request must specify both the size and num_nodes attributes.
A successful request will receive a 202 Accepted status code with no body in response. Querying the database cluster will show that its status attribute will now be set to resizing. This will transition back to online when the resize operation has completed.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.databases.resize_cluster(
    size="db-s-4vcpu-8gb",
    num_nodes=3,
    database_cluster_uuid="9cc10173-e9ea-4176-9dbc-a4cee4c4ff30",
    storage_size_mib=61440,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### size: `str`<a id="size-str"></a>

A slug identifier representing desired the size of the nodes in the database cluster.

##### num_nodes: `int`<a id="num_nodes-int"></a>

The number of nodes in the database cluster. Valid values are are 1-3. In addition to the primary node, up to two standby nodes may be added for highly available configurations.

##### database_cluster_uuid: `str`<a id="database_cluster_uuid-str"></a>

A unique identifier for a database cluster.

##### storage_size_mib: `int`<a id="storage_size_mib-int"></a>

Additional storage added to the cluster, in MiB. If null, no additional storage is added to the cluster, beyond what is provided as a base amount from the 'size' and any previously added additional storage.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`DatabaseClusterResize`](./digital_ocean_python_sdk/type/database_cluster_resize.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/databases/{database_cluster_uuid}/resize` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.databases.start_online_migration`<a id="digitaloceandatabasesstart_online_migration"></a>

To start an online migration, send a PUT request to `/v2/databases/$DATABASE_ID/online-migration` endpoint. Migrating a cluster establishes a connection with an existing cluster and replicates its contents to the target cluster. Online migration is only available for MySQL, PostgreSQL, and Redis clusters.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
start_online_migration_response = digitalocean.databases.start_online_migration(
    database_cluster_uuid="9cc10173-e9ea-4176-9dbc-a4cee4c4ff30",
    source={
        "host": "backend-do-user-19081923-0.db.ondigitalocean.com",
        "port": 25060,
        "dbname": "defaultdb",
        "username": "doadmin",
        "password": "wv78n3zpz42xezdk",
    },
    disable_ssl=False,
    ignore_dbs=["db0", "db1"],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### database_cluster_uuid: `str`<a id="database_cluster_uuid-str"></a>

A unique identifier for a database cluster.

##### source: [`SourceDatabaseSource`](./digital_ocean_python_sdk/type/source_database_source.py)<a id="source-sourcedatabasesourcedigital_ocean_python_sdktypesource_database_sourcepy"></a>


##### disable_ssl: `bool`<a id="disable_ssl-bool"></a>

Enables SSL encryption when connecting to the source database.

##### ignore_dbs: [`SourceDatabaseIgnoreDbs`](./digital_ocean_python_sdk/type/source_database_ignore_dbs.py)<a id="ignore_dbs-sourcedatabaseignoredbsdigital_ocean_python_sdktypesource_database_ignore_dbspy"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`SourceDatabase`](./digital_ocean_python_sdk/type/source_database.py)
#### 🔄 Return<a id="🔄-return"></a>

[`OnlineMigration`](./digital_ocean_python_sdk/pydantic/online_migration.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/databases/{database_cluster_uuid}/online-migration` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.databases.stop_online_migration`<a id="digitaloceandatabasesstop_online_migration"></a>

To stop an online migration, send a DELETE request to `/v2/databases/$DATABASE_ID/online-migration/$MIGRATION_ID`.

A status of 204 will be given. This indicates that the request was processed successfully, but that no response body is needed.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.databases.stop_online_migration(
    database_cluster_uuid="9cc10173-e9ea-4176-9dbc-a4cee4c4ff30",
    migration_id="77b28fc8-19ff-11eb-8c9c-c68e24557488",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### database_cluster_uuid: `str`<a id="database_cluster_uuid-str"></a>

A unique identifier for a database cluster.

##### migration_id: `str`<a id="migration_id-str"></a>

A unique identifier assigned to the online migration.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/databases/{database_cluster_uuid}/online-migration/{migration_id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.databases.update_config_cluster`<a id="digitaloceandatabasesupdate_config_cluster"></a>

To update the configuration for an existing database cluster, send a PATCH request to
`/v2/databases/$DATABASE_ID/config`.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.databases.update_config_cluster(
    database_cluster_uuid="9cc10173-e9ea-4176-9dbc-a4cee4c4ff30",
    config={
        "backup_hour": 3,
        "backup_minute": 30,
        "sql_mode": "ANSI,TRADITIONAL",
        "connect_timeout": 10,
        "default_time_zone": "+03:00",
        "group_concat_max_len": 1024,
        "information_schema_stats_expiry": 86400,
        "innodb_ft_min_token_size": 3,
        "innodb_ft_server_stopword_table": "db_name/table_name",
        "innodb_lock_wait_timeout": 50,
        "innodb_log_buffer_size": 16777216,
        "innodb_online_alter_log_max_size": 134217728,
        "innodb_print_all_deadlocks": True,
        "innodb_rollback_on_timeout": True,
        "interactive_timeout": 3600,
        "internal_tmp_mem_storage_engine": "TempTable",
        "net_read_timeout": 30,
        "net_write_timeout": 30,
        "sql_require_primary_key": True,
        "wait_timeout": 28800,
        "max_allowed_packet": 67108864,
        "max_heap_table_size": 16777216,
        "sort_buffer_size": 262144,
        "tmp_table_size": 16777216,
        "slow_query_log": True,
        "long_query_time": 10,
        "binlog_retention_period": 600,
        "innodb_change_buffer_max_size": 25,
        "innodb_flush_neighbors": 0,
        "innodb_read_io_threads": 16,
        "innodb_write_io_threads": 16,
        "innodb_thread_concurrency": 0,
        "net_buffer_length": 4096,
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### database_cluster_uuid: `str`<a id="database_cluster_uuid-str"></a>

A unique identifier for a database cluster.

##### config: Union[`Mysql`, `Postgres`, `Redis`]<a id="config-unionmysql-postgres-redis"></a>


#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`DatabaseConfig`](./digital_ocean_python_sdk/type/database_config.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/databases/{database_cluster_uuid}/config` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.databases.update_connection_pool_postgresql`<a id="digitaloceandatabasesupdate_connection_pool_postgresql"></a>

To update a connection pool for a PostgreSQL database cluster, send a PUT request to  `/v2/databases/$DATABASE_ID/pools/$POOL_NAME`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.databases.update_connection_pool_postgresql(
    mode="transaction",
    size=10,
    db="defaultdb",
    database_cluster_uuid="9cc10173-e9ea-4176-9dbc-a4cee4c4ff30",
    pool_name="backend-pool",
    user="doadmin",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### mode: `str`<a id="mode-str"></a>

The PGBouncer transaction mode for the connection pool. The allowed values are session, transaction, and statement.

##### size: `int`<a id="size-int"></a>

The desired size of the PGBouncer connection pool. The maximum allowed size is determined by the size of the cluster's primary node. 25 backend server connections are allowed for every 1GB of RAM. Three are reserved for maintenance. For example, a primary node with 1 GB of RAM allows for a maximum of 22 backend server connections while one with 4 GB would allow for 97. Note that these are shared across all connection pools in a cluster.

##### db: `str`<a id="db-str"></a>

The database for use with the connection pool.

##### database_cluster_uuid: `str`<a id="database_cluster_uuid-str"></a>

A unique identifier for a database cluster.

##### pool_name: `str`<a id="pool_name-str"></a>

The name used to identify the connection pool.

##### user: `str`<a id="user-str"></a>

The name of the user for use with the connection pool. When excluded, all sessions connect to the database as the inbound user.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ConnectionPoolUpdate`](./digital_ocean_python_sdk/type/connection_pool_update.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/databases/{database_cluster_uuid}/pools/{pool_name}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.databases.update_firewall_rules`<a id="digitaloceandatabasesupdate_firewall_rules"></a>

To update a database cluster's firewall rules (known as "trusted sources" in the control panel), send a PUT request to `/v2/databases/$DATABASE_ID/firewall` specifying which resources should be able to open connections to the database. You may limit connections to specific Droplets, Kubernetes clusters, or IP addresses. When a tag is provided, any Droplet or Kubernetes node with that tag applied to it will have access. The firewall is limited to 100 rules (or trusted sources). When possible, we recommend [placing your databases into a VPC network](https://www.digitalocean.com/docs/networking/vpc/) to limit access to them instead of using a firewall.
A successful

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.databases.update_firewall_rules(
    database_cluster_uuid="9cc10173-e9ea-4176-9dbc-a4cee4c4ff30",
    rules=[
        {
            "uuid": "79f26d28-ea8a-41f2-8ad8-8cfcdd020095",
            "cluster_uuid": "9cc10173-e9ea-4176-9dbc-a4cee4c4ff30",
            "type": "droplet",
            "value": "ff2a6c52-5a44-4b63-b99c-0e98e7a63d61",
            "created_at": "2019-01-11T18:37:36Z",
        }
    ],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### database_cluster_uuid: `str`<a id="database_cluster_uuid-str"></a>

A unique identifier for a database cluster.

##### rules: List[`FirewallRule`]<a id="rules-listfirewallrule"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`DatabasesUpdateFirewallRulesRequest`](./digital_ocean_python_sdk/type/databases_update_firewall_rules_request.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/databases/{database_cluster_uuid}/firewall` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.databases.update_metrics_credentials`<a id="digitaloceandatabasesupdate_metrics_credentials"></a>

To update the credentials for all database clusters' metrics endpoints, send a PUT request to `/v2/databases/metrics/credentials`. A successful request will receive a 204 No Content status code  with no body in response.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.databases.update_metrics_credentials(
    credentials={
        "basic_auth_username": "username",
        "basic_auth_password": "password",
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### credentials: [`DatabasesBasicAuthCredentials`](./digital_ocean_python_sdk/type/databases_basic_auth_credentials.py)<a id="credentials-databasesbasicauthcredentialsdigital_ocean_python_sdktypedatabases_basic_auth_credentialspy"></a>


#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`DatabaseMetricsCredentials`](./digital_ocean_python_sdk/type/database_metrics_credentials.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/databases/metrics/credentials` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.databases.update_settings`<a id="digitaloceandatabasesupdate_settings"></a>

To update an existing database user, send a PUT request to `/v2/databases/$DATABASE_ID/users/$USERNAME`
with the desired settings.

**Note**: only `settings` can be updated via this type of request. If you wish to change the name of a user,
you must recreate a new user.

The response will be a JSON object with a key called `user`. The value of this will be an
object that contains the name of the update database user, along with the `settings` object that
has been updated.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_settings_response = digitalocean.databases.update_settings(
    body={
    },
    settings={
        "pg_allow_replication": True,
    },
    database_cluster_uuid="9cc10173-e9ea-4176-9dbc-a4cee4c4ff30",
    username="app-01",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### settings: [`UserSettings`](./digital_ocean_python_sdk/type/user_settings.py)<a id="settings-usersettingsdigital_ocean_python_sdktypeuser_settingspy"></a>


##### database_cluster_uuid: `str`<a id="database_cluster_uuid-str"></a>

A unique identifier for a database cluster.

##### username: `str`<a id="username-str"></a>

The name of the database user.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`DatabasesUpdateSettingsRequest`](./digital_ocean_python_sdk/type/databases_update_settings_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`DatabasesAddUserResponse`](./digital_ocean_python_sdk/pydantic/databases_add_user_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/databases/{database_cluster_uuid}/users/{username}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.databases.update_sql_mode`<a id="digitaloceandatabasesupdate_sql_mode"></a>

To configure the SQL modes for an existing MySQL cluster, send a PUT request to `/v2/databases/$DATABASE_ID/sql_mode` specifying the desired modes. See the official MySQL 8 documentation for a [full list of supported SQL modes](https://dev.mysql.com/doc/refman/8.0/en/sql-mode.html#sql-mode-full).
A successful request will receive a 204 No Content status code with no body in response.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.databases.update_sql_mode(
    sql_mode="ANSI,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION,NO_ZERO_DATE,NO_ZERO_IN_DATE,STRICT_ALL_TABLES",
    database_cluster_uuid="9cc10173-e9ea-4176-9dbc-a4cee4c4ff30",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### sql_mode: `str`<a id="sql_mode-str"></a>

A string specifying the configured SQL modes for the MySQL cluster.

##### database_cluster_uuid: `str`<a id="database_cluster_uuid-str"></a>

A unique identifier for a database cluster.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`SqlMode`](./digital_ocean_python_sdk/type/sql_mode.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/databases/{database_cluster_uuid}/sql_mode` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.databases.update_topic_kafka_cluster`<a id="digitaloceandatabasesupdate_topic_kafka_cluster"></a>

To update a topic attached to a Kafka cluster, send a PUT request to
`/v2/databases/$DATABASE_ID/topics/$TOPIC_NAME`.

The result will be a JSON object with a `topic` key.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_topic_kafka_cluster_response = digitalocean.databases.update_topic_kafka_cluster(
    database_cluster_uuid="9cc10173-e9ea-4176-9dbc-a4cee4c4ff30",
    topic_name="customer-events",
    replication_factor=2,
    partition_count=3,
    config={
        "cleanup_policy": "delete",
        "compression_type": "producer",
        "delete_retention_ms": 86400000,
        "file_delete_delay_ms": 60000,
        "flush_messages": 9223372036854776000,
        "flush_ms": 9223372036854776000,
        "index_interval_bytes": 4096,
        "max_compaction_lag_ms": 9223372036854776000,
        "max_message_bytes": 1048588,
        "message_down_conversion_enable": True,
        "message_format_version": "3.0-IV1",
        "message_timestamp_type": "create_time",
        "min_cleanable_dirty_ratio": 0.5,
        "min_compaction_lag_ms": 0,
        "min_insync_replicas": 1,
        "preallocate": False,
        "retention_bytes": 1000000,
        "retention_ms": 604800000,
        "segment_bytes": 209715200,
        "segment_jitter_ms": 0,
        "segment_ms": 604800000,
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### database_cluster_uuid: `str`<a id="database_cluster_uuid-str"></a>

A unique identifier for a database cluster.

##### topic_name: `str`<a id="topic_name-str"></a>

The name used to identify the Kafka topic.

##### replication_factor: `int`<a id="replication_factor-int"></a>

The number of nodes to replicate data across the cluster.

##### partition_count: `int`<a id="partition_count-int"></a>

The number of partitions available for the topic. On update, this value can only be increased.

##### config: [`KafkaTopicConfig`](./digital_ocean_python_sdk/type/kafka_topic_config.py)<a id="config-kafkatopicconfigdigital_ocean_python_sdktypekafka_topic_configpy"></a>


#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`KafkaTopicUpdate`](./digital_ocean_python_sdk/type/kafka_topic_update.py)
#### 🔄 Return<a id="🔄-return"></a>

[`DatabasesCreateTopicKafkaClusterResponse`](./digital_ocean_python_sdk/pydantic/databases_create_topic_kafka_cluster_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/databases/{database_cluster_uuid}/topics/{topic_name}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.databases.upgrade_major_version`<a id="digitaloceandatabasesupgrade_major_version"></a>

To upgrade the major version of a database, send a PUT request to `/v2/databases/$DATABASE_ID/upgrade`, specifying the target version.
A successful request will receive a 204 No Content status code with no body in response.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.databases.upgrade_major_version(
    database_cluster_uuid="9cc10173-e9ea-4176-9dbc-a4cee4c4ff30",
    version="8",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### database_cluster_uuid: `str`<a id="database_cluster_uuid-str"></a>

A unique identifier for a database cluster.

##### version: `str`<a id="version-str"></a>

A string representing the version of the database engine in use for the cluster.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`Version2`](./digital_ocean_python_sdk/type/version2.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/databases/{database_cluster_uuid}/upgrade` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.domain_records.create_new_record`<a id="digitaloceandomain_recordscreate_new_record"></a>

To create a new record to a domain, send a POST request to
`/v2/domains/$DOMAIN_NAME/records`.

The request must include all of the required fields for the domain record type
being added.

See the [attribute table](https://api-engineering.nyc3.cdn.digitaloceanspaces.com) for details regarding record
types and their respective required attributes.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_new_record_response = digitalocean.domain_records.create_new_record(
    body=None,
    domain_name="example.com",
    id=28448429,
    type="NS",
    name="@",
    data="ns1.digitalocean.com",
    priority=1,
    port=1,
    ttl=1800,
    weight=1,
    flags=1,
    tag="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### domain_name: `str`<a id="domain_name-str"></a>

The name of the domain itself.

##### id: `int`<a id="id-int"></a>

A unique identifier for each domain record.

##### type: `str`<a id="type-str"></a>

The type of the DNS record. For example: A, CNAME, TXT, ...

##### name: `str`<a id="name-str"></a>

The host name, alias, or service being defined by the record.

##### data: `str`<a id="data-str"></a>

Variable data depending on record type. For example, the \\\"data\\\" value for an A record would be the IPv4 address to which the domain will be mapped. For a CAA record, it would contain the domain name of the CA being granted permission to issue certificates.

##### priority: `Optional[int]`<a id="priority-optionalint"></a>

The priority for SRV and MX records.

##### port: `Optional[int]`<a id="port-optionalint"></a>

The port for SRV records.

##### ttl: `int`<a id="ttl-int"></a>

This value is the time to live for the record, in seconds. This defines the time frame that clients can cache queried information before a refresh should be requested.

##### weight: `Optional[int]`<a id="weight-optionalint"></a>

The weight for SRV records.

##### flags: `Optional[int]`<a id="flags-optionalint"></a>

An unsigned integer between 0-255 used for CAA records.

##### tag: `Optional[str]`<a id="tag-optionalstr"></a>

The parameter tag for CAA records. Valid values are \\\"issue\\\", \\\"issuewild\\\", or \\\"iodef\\\"

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`DomainRecordsCreateNewRecordRequest`](./digital_ocean_python_sdk/type/domain_records_create_new_record_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`DomainRecordsCreateNewRecordResponse`](./digital_ocean_python_sdk/pydantic/domain_records_create_new_record_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/domains/{domain_name}/records` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.domain_records.delete_by_id`<a id="digitaloceandomain_recordsdelete_by_id"></a>

To delete a record for a domain, send a DELETE request to
`/v2/domains/$DOMAIN_NAME/records/$DOMAIN_RECORD_ID`.

The record will be deleted and the response status will be a 204. This
indicates a successful request with no body returned.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.domain_records.delete_by_id(
    domain_name="example.com",
    domain_record_id=3352896,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### domain_name: `str`<a id="domain_name-str"></a>

The name of the domain itself.

##### domain_record_id: `int`<a id="domain_record_id-int"></a>

The unique identifier of the domain record.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/domains/{domain_name}/records/{domain_record_id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.domain_records.get_existing_record`<a id="digitaloceandomain_recordsget_existing_record"></a>

To retrieve a specific domain record, send a GET request to `/v2/domains/$DOMAIN_NAME/records/$RECORD_ID`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_existing_record_response = digitalocean.domain_records.get_existing_record(
    domain_name="example.com",
    domain_record_id=3352896,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### domain_name: `str`<a id="domain_name-str"></a>

The name of the domain itself.

##### domain_record_id: `int`<a id="domain_record_id-int"></a>

The unique identifier of the domain record.

#### 🔄 Return<a id="🔄-return"></a>

[`DomainRecordsGetExistingRecordResponse`](./digital_ocean_python_sdk/pydantic/domain_records_get_existing_record_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/domains/{domain_name}/records/{domain_record_id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.domain_records.list_all_records`<a id="digitaloceandomain_recordslist_all_records"></a>

To get a listing of all records configured for a domain, send a GET request to `/v2/domains/$DOMAIN_NAME/records`.
The list of records returned can be filtered by using the `name` and `type` query parameters. For example, to only include A records for a domain, send a GET request to `/v2/domains/$DOMAIN_NAME/records?type=A`. `name` must be a fully qualified record name. For example, to only include records matching `sub.example.com`, send a GET request to `/v2/domains/$DOMAIN_NAME/records?name=sub.example.com`. Both name and type may be used together.



#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_all_records_response = digitalocean.domain_records.list_all_records(
    domain_name="example.com",
    name="sub.example.com",
    type="A",
    per_page=2,
    page=1,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### domain_name: `str`<a id="domain_name-str"></a>

The name of the domain itself.

##### name: `str`<a id="name-str"></a>

A fully qualified record name. For example, to only include records matching sub.example.com, send a GET request to `/v2/domains/$DOMAIN_NAME/records?name=sub.example.com`.

##### type: `str`<a id="type-str"></a>

The type of the DNS record. For example: A, CNAME, TXT, ...

##### per_page: `int`<a id="per_page-int"></a>

Number of items returned per page

##### page: `int`<a id="page-int"></a>

Which 'page' of paginated results to return.

#### 🔄 Return<a id="🔄-return"></a>

[`DomainRecordsListAllRecordsResponse`](./digital_ocean_python_sdk/pydantic/domain_records_list_all_records_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/domains/{domain_name}/records` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.domain_records.update_record_by_id`<a id="digitaloceandomain_recordsupdate_record_by_id"></a>

To update an existing record, send a PUT request to
`/v2/domains/$DOMAIN_NAME/records/$DOMAIN_RECORD_ID`. Any attribute valid for
the record type can be set to a new value for the record.

See the [attribute table](https://api-engineering.nyc3.cdn.digitaloceanspaces.com) for details regarding record
types and their respective attributes.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_record_by_id_response = digitalocean.domain_records.update_record_by_id(
    type="NS",
    domain_name="example.com",
    domain_record_id=3352896,
    id=28448429,
    name="@",
    data="ns1.digitalocean.com",
    priority=1,
    port=1,
    ttl=1800,
    weight=1,
    flags=1,
    tag="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### type: `str`<a id="type-str"></a>

The type of the DNS record. For example: A, CNAME, TXT, ...

##### domain_name: `str`<a id="domain_name-str"></a>

The name of the domain itself.

##### domain_record_id: `int`<a id="domain_record_id-int"></a>

The unique identifier of the domain record.

##### id: `int`<a id="id-int"></a>

A unique identifier for each domain record.

##### name: `str`<a id="name-str"></a>

The host name, alias, or service being defined by the record.

##### data: `str`<a id="data-str"></a>

Variable data depending on record type. For example, the \\\"data\\\" value for an A record would be the IPv4 address to which the domain will be mapped. For a CAA record, it would contain the domain name of the CA being granted permission to issue certificates.

##### priority: `Optional[int]`<a id="priority-optionalint"></a>

The priority for SRV and MX records.

##### port: `Optional[int]`<a id="port-optionalint"></a>

The port for SRV records.

##### ttl: `int`<a id="ttl-int"></a>

This value is the time to live for the record, in seconds. This defines the time frame that clients can cache queried information before a refresh should be requested.

##### weight: `Optional[int]`<a id="weight-optionalint"></a>

The weight for SRV records.

##### flags: `Optional[int]`<a id="flags-optionalint"></a>

An unsigned integer between 0-255 used for CAA records.

##### tag: `Optional[str]`<a id="tag-optionalstr"></a>

The parameter tag for CAA records. Valid values are \\\"issue\\\", \\\"issuewild\\\", or \\\"iodef\\\"

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`DomainRecord`](./digital_ocean_python_sdk/type/domain_record.py)
#### 🔄 Return<a id="🔄-return"></a>

[`DomainRecordsGetExistingRecordResponse`](./digital_ocean_python_sdk/pydantic/domain_records_get_existing_record_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/domains/{domain_name}/records/{domain_record_id}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.domain_records.update_record_by_id_0`<a id="digitaloceandomain_recordsupdate_record_by_id_0"></a>

To update an existing record, send a PATCH request to
`/v2/domains/$DOMAIN_NAME/records/$DOMAIN_RECORD_ID`. Any attribute valid for
the record type can be set to a new value for the record.

See the [attribute table](https://api-engineering.nyc3.cdn.digitaloceanspaces.com) for details regarding record
types and their respective attributes.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_record_by_id_0_response = digitalocean.domain_records.update_record_by_id_0(
    type="NS",
    domain_name="example.com",
    domain_record_id=3352896,
    id=28448429,
    name="@",
    data="ns1.digitalocean.com",
    priority=1,
    port=1,
    ttl=1800,
    weight=1,
    flags=1,
    tag="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### type: `str`<a id="type-str"></a>

The type of the DNS record. For example: A, CNAME, TXT, ...

##### domain_name: `str`<a id="domain_name-str"></a>

The name of the domain itself.

##### domain_record_id: `int`<a id="domain_record_id-int"></a>

The unique identifier of the domain record.

##### id: `int`<a id="id-int"></a>

A unique identifier for each domain record.

##### name: `str`<a id="name-str"></a>

The host name, alias, or service being defined by the record.

##### data: `str`<a id="data-str"></a>

Variable data depending on record type. For example, the \\\"data\\\" value for an A record would be the IPv4 address to which the domain will be mapped. For a CAA record, it would contain the domain name of the CA being granted permission to issue certificates.

##### priority: `Optional[int]`<a id="priority-optionalint"></a>

The priority for SRV and MX records.

##### port: `Optional[int]`<a id="port-optionalint"></a>

The port for SRV records.

##### ttl: `int`<a id="ttl-int"></a>

This value is the time to live for the record, in seconds. This defines the time frame that clients can cache queried information before a refresh should be requested.

##### weight: `Optional[int]`<a id="weight-optionalint"></a>

The weight for SRV records.

##### flags: `Optional[int]`<a id="flags-optionalint"></a>

An unsigned integer between 0-255 used for CAA records.

##### tag: `Optional[str]`<a id="tag-optionalstr"></a>

The parameter tag for CAA records. Valid values are \\\"issue\\\", \\\"issuewild\\\", or \\\"iodef\\\"

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`DomainRecord`](./digital_ocean_python_sdk/type/domain_record.py)
#### 🔄 Return<a id="🔄-return"></a>

[`DomainRecordsGetExistingRecordResponse`](./digital_ocean_python_sdk/pydantic/domain_records_get_existing_record_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/domains/{domain_name}/records/{domain_record_id}` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.domains.create`<a id="digitaloceandomainscreate"></a>

To create a new domain, send a POST request to `/v2/domains`. Set the "name"
attribute to the domain name you are adding. Optionally, you may set the
"ip_address" attribute, and an A record will be automatically created pointing
to the apex domain.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_response = digitalocean.domains.create(
    name="example.com",
    ip_address="192.0.2.1",
    ttl=1800,
    zone_file="$ORIGIN example.com.\n$TTL 1800\nexample.com. IN SOA ns1.digitalocean.com. hostmaster.example.com. 1415982609 10800 3600 604800 1800\nexample.com. 1800 IN NS ns1.digitalocean.com.\nexample.com. 1800 IN NS ns2.digitalocean.com.\nexample.com. 1800 IN NS ns3.digitalocean.com.\nexample.com. 1800 IN A 1.2.3.4\n",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### name: `str`<a id="name-str"></a>

The name of the domain itself. This should follow the standard domain format of domain.TLD. For instance, `example.com` is a valid domain name.

##### ip_address: `str`<a id="ip_address-str"></a>

This optional attribute may contain an IP address. When provided, an A record will be automatically created pointing to the apex domain.

##### ttl: `Optional[int]`<a id="ttl-optionalint"></a>

This value is the time to live for the records on this domain, in seconds. This defines the time frame that clients can cache queried information before a refresh should be requested.

##### zone_file: `Optional[str]`<a id="zone_file-optionalstr"></a>

This attribute contains the complete contents of the zone file for the selected domain. Individual domain record resources should be used to get more granular control over records. However, this attribute can also be used to get information about the SOA record, which is created automatically and is not accessible as an individual record resource.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`Domain`](./digital_ocean_python_sdk/type/domain.py)
#### 🔄 Return<a id="🔄-return"></a>

[`DomainsCreateResponse`](./digital_ocean_python_sdk/pydantic/domains_create_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/domains` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.domains.delete`<a id="digitaloceandomainsdelete"></a>

To delete a domain, send a DELETE request to `/v2/domains/$DOMAIN_NAME`.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.domains.delete(
    domain_name="example.com",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### domain_name: `str`<a id="domain_name-str"></a>

The name of the domain itself.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/domains/{domain_name}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.domains.get`<a id="digitaloceandomainsget"></a>

To get details about a specific domain, send a GET request to `/v2/domains/$DOMAIN_NAME`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_response = digitalocean.domains.get(
    domain_name="example.com",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### domain_name: `str`<a id="domain_name-str"></a>

The name of the domain itself.

#### 🔄 Return<a id="🔄-return"></a>

[`DomainsGetResponse`](./digital_ocean_python_sdk/pydantic/domains_get_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/domains/{domain_name}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.domains.list`<a id="digitaloceandomainslist"></a>

To retrieve a list of all of the domains in your account, send a GET request to `/v2/domains`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = digitalocean.domains.list(
    per_page=2,
    page=1,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### per_page: `int`<a id="per_page-int"></a>

Number of items returned per page

##### page: `int`<a id="page-int"></a>

Which 'page' of paginated results to return.

#### 🔄 Return<a id="🔄-return"></a>

[`DomainsListResponse`](./digital_ocean_python_sdk/pydantic/domains_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/domains` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.droplet_actions.act_on_tagged_droplets`<a id="digitaloceandroplet_actionsact_on_tagged_droplets"></a>

Some actions can be performed in bulk on tagged Droplets. The actions can be
initiated by sending a POST to `/v2/droplets/actions?tag_name=$TAG_NAME` with
the action arguments.

Only a sub-set of action types are supported:

- `power_cycle`
- `power_on`
- `power_off`
- `shutdown`
- `enable_ipv6`
- `enable_backups`
- `disable_backups`
- `snapshot`


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
act_on_tagged_droplets_response = digitalocean.droplet_actions.act_on_tagged_droplets(
    body={
        "type": "disable_backups",
    },
    type="reboot",
    name="Nifty New Snapshot",
    tag_name="env:prod",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### type: `str`<a id="type-str"></a>

The type of action to initiate for the Droplet.

##### name: `str`<a id="name-str"></a>

The name to give the new snapshot of the Droplet.

##### tag_name: `str`<a id="tag_name-str"></a>

Used to filter Droplets by a specific tag. Can not be combined with `name`.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`DropletActionsActOnTaggedDropletsRequest`](./digital_ocean_python_sdk/type/droplet_actions_act_on_tagged_droplets_request.py)
The `type` attribute set in the request body will specify the  action that will be taken on the Droplet. Some actions will require additional attributes to be set as well. 

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/droplets/actions` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.droplet_actions.get`<a id="digitaloceandroplet_actionsget"></a>

To retrieve a Droplet action, send a GET request to
`/v2/droplets/$DROPLET_ID/actions/$ACTION_ID`.

The response will be a JSON object with a key called `action`. The value will
be a Droplet action object.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_response = digitalocean.droplet_actions.get(
    droplet_id=3164444,
    action_id=36804636,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### droplet_id: `int`<a id="droplet_id-int"></a>

A unique identifier for a Droplet instance.

##### action_id: `int`<a id="action_id-int"></a>

A unique numeric ID that can be used to identify and reference an action.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/droplets/{droplet_id}/actions/{action_id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.droplet_actions.list`<a id="digitaloceandroplet_actionslist"></a>

To retrieve a list of all actions that have been executed for a Droplet, send
a GET request to `/v2/droplets/$DROPLET_ID/actions`.

The results will be returned as a JSON object with an `actions` key. This will
be set to an array filled with `action` objects containing the standard
`action` attributes.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = digitalocean.droplet_actions.list(
    droplet_id=3164444,
    per_page=2,
    page=1,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### droplet_id: `int`<a id="droplet_id-int"></a>

A unique identifier for a Droplet instance.

##### per_page: `int`<a id="per_page-int"></a>

Number of items returned per page

##### page: `int`<a id="page-int"></a>

Which 'page' of paginated results to return.

#### 🔄 Return<a id="🔄-return"></a>

[`DropletActionsListResponse`](./digital_ocean_python_sdk/pydantic/droplet_actions_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/droplets/{droplet_id}/actions` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.droplet_actions.post`<a id="digitaloceandroplet_actionspost"></a>

To initiate an action on a Droplet send a POST request to
`/v2/droplets/$DROPLET_ID/actions`. In the JSON body to the request,
set the `type` attribute to on of the supported action types:

| Action                                   | Details |
| ---------------------------------------- | ----------- |
| <nobr>`enable_backups`</nobr>            | Enables backups for a Droplet |
| <nobr>`disable_backups`</nobr>           | Disables backups for a Droplet |
| <nobr>`reboot`</nobr>                    | Reboots a Droplet. A `reboot` action is an attempt to reboot the Droplet in a graceful way, similar to using the `reboot` command from the console. |
| <nobr>`power_cycle`</nobr>               | Power cycles a Droplet. A `powercycle` action is similar to pushing the reset button on a physical machine, it's similar to booting from scratch. |
| <nobr>`shutdown`</nobr>                  | Shutsdown a Droplet. A shutdown action is an attempt to shutdown the Droplet in a graceful way, similar to using the `shutdown` command from the console. Since a `shutdown` command can fail, this action guarantees that the command is issued, not that it succeeds. The preferred way to turn off a Droplet is to attempt a shutdown, with a reasonable timeout, followed by a `power_off` action to ensure the Droplet is off. |
| <nobr>`power_off`</nobr>                 | Powers off a Droplet. A `power_off` event is a hard shutdown and should only be used if the `shutdown` action is not successful. It is similar to cutting the power on a server and could lead to complications. |
| <nobr>`power_on`</nobr>                  | Powers on a Droplet. |
| <nobr>`restore`</nobr>                   | Restore a Droplet using a backup image. The image ID that is passed in must be a backup of the current Droplet instance. The operation will leave any embedded SSH keys intact. |
| <nobr>`password_reset`</nobr>            | Resets the root password for a Droplet. A new password will be provided via email. It must be changed after first use. |
| <nobr>`resize`</nobr>                    | Resizes a Droplet. Set the `size` attribute to a size slug. If a permanent resize with disk changes included is desired, set the `disk` attribute to `true`. |
| <nobr>`rebuild`</nobr>                   | Rebuilds a Droplet from a new base image. Set the `image` attribute to an image ID or slug. |
| <nobr>`rename`</nobr>                    | Renames a Droplet. |
| <nobr>`change_kernel`</nobr>             | Changes a Droplet's kernel. Only applies to Droplets with externally managed kernels. All Droplets created after March 2017 use internal kernels by default. |
| <nobr>`enable_ipv6`</nobr>               | Enables IPv6 for a Droplet. Once enabled for a Droplet, IPv6 can not be disabled. When enabling IPv6 on an existing Droplet, [additional OS-level configuration](https://docs.digitalocean.com/products/networking/ipv6/how-to/enable/#on-existing-droplets) is required. |
| <nobr>`snapshot`</nobr>                  | Takes a snapshot of a Droplet. |


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
post_response = digitalocean.droplet_actions.post(
    body={
        "type": "reboot",
    },
    droplet_id=3164444,
    type="reboot",
    image=None,
    disk=True,
    size="s-2vcpu-2gb",
    name="Nifty New Snapshot",
    kernel=12389723,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### droplet_id: `int`<a id="droplet_id-int"></a>

A unique identifier for a Droplet instance.

##### type: `str`<a id="type-str"></a>

The type of action to initiate for the Droplet.

##### image: Union[`str`, `int`]<a id="image-unionstr-int"></a>


The image ID of a public or private image or the slug identifier for a public image. The Droplet will be rebuilt using this image as its base.

##### disk: `bool`<a id="disk-bool"></a>

When `true`, the Droplet's disk will be resized in addition to its RAM and CPU. This is a permanent change and cannot be reversed as a Droplet's disk size cannot be decreased.

##### size: `str`<a id="size-str"></a>

The slug identifier for the size to which you wish to resize the Droplet.

##### name: `str`<a id="name-str"></a>

The name to give the new snapshot of the Droplet.

##### kernel: `int`<a id="kernel-int"></a>

A unique number used to identify and reference a specific kernel.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`DropletActionsPostRequest`](./digital_ocean_python_sdk/type/droplet_actions_post_request.py)
The `type` attribute set in the request body will specify the  action that will be taken on the Droplet. Some actions will require additional attributes to be set as well. 

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/droplets/{droplet_id}/actions` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.droplets.check_destroy_status`<a id="digitaloceandropletscheck_destroy_status"></a>

To check on the status of a request to destroy a Droplet with its associated
resources, send a GET request to the
`/v2/droplets/$DROPLET_ID/destroy_with_associated_resources/status` endpoint.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
check_destroy_status_response = digitalocean.droplets.check_destroy_status(
    droplet_id=3164444,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### droplet_id: `int`<a id="droplet_id-int"></a>

A unique identifier for a Droplet instance.

#### 🔄 Return<a id="🔄-return"></a>

[`AssociatedResourceStatus`](./digital_ocean_python_sdk/pydantic/associated_resource_status.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/droplets/{droplet_id}/destroy_with_associated_resources/status` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.droplets.create`<a id="digitaloceandropletscreate"></a>

To create a new Droplet, send a POST request to `/v2/droplets` setting the
required attributes.

A Droplet will be created using the provided information. The response body
will contain a JSON object with a key called `droplet`. The value will be an
object containing the standard attributes for your new Droplet. The response
code, 202 Accepted, does not indicate the success or failure of the operation,
just that the request has been accepted for processing. The `actions` returned
as part of the response's `links` object can be used to check the status
of the Droplet create event.

### Create Multiple Droplets<a id="create-multiple-droplets"></a>

Creating multiple Droplets is very similar to creating a single Droplet.
Instead of sending `name` as a string, send `names` as an array of strings. A
Droplet will be created for each name you send using the associated
information. Up to ten Droplets may be created this way at a time.

Rather than returning a single Droplet, the response body will contain a JSON
array with a key called `droplets`. This will be set to an array of JSON
objects, each of which will contain the standard Droplet attributes. The
response code, 202 Accepted, does not indicate the success or failure of any
operation, just that the request has been accepted for processing. The array
of `actions` returned as part of the response's `links` object can be used to
check the status of each individual Droplet create event.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_response = digitalocean.droplets.create(
    body=None,
    name="example.com",
    tags=["env:prod", "web"],
    region="nyc3",
    size="s-1vcpu-1gb",
    image=None,
    ssh_keys=[289794, "3b:16:e4:bf:8b:00:8b:b8:59:8c:a9:d3:f0:19:fa:45"],
    backups=True,
    ipv6=True,
    monitoring=True,
    user_data="#cloud-config\nruncmd:\n  - touch /test.txt\n",
    private_networking=True,
    volumes=["12e97116-7280-11ed-b3d0-0a58ac146812"],
    vpc_uuid="760e09ef-dc84-11e8-981e-3cfdfeaae000",
    with_droplet_agent=True,
    names=["sub-01.example.com", "sub-02.example.com"],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### name: `str`<a id="name-str"></a>

The human-readable string you wish to use when displaying the Droplet name. The name, if set to a domain name managed in the DigitalOcean DNS management system, will configure a PTR record for the Droplet. The name set during creation will also determine the hostname for the Droplet in its internal configuration.

##### tags: [`DropletCreateTags`](./digital_ocean_python_sdk/type/droplet_create_tags.py)<a id="tags-dropletcreatetagsdigital_ocean_python_sdktypedroplet_create_tagspy"></a>

##### region: `str`<a id="region-str"></a>

The slug identifier for the region that you wish to deploy the Droplet in. If the specific datacenter is not not important, a slug prefix (e.g. `nyc`) can be used to deploy the Droplet in any of the that region's locations (`nyc1`, `nyc2`, or `nyc3`). If the region is omitted from the create request completely, the Droplet may deploy in any region.

##### size: `str`<a id="size-str"></a>

The slug identifier for the size that you wish to select for this Droplet.

##### image: Union[`str`, `int`]<a id="image-unionstr-int"></a>


The image ID of a public or private image or the slug identifier for a public image. This image will be the base image for your Droplet.

##### ssh_keys: [`DropletCreateSshKeys`](./digital_ocean_python_sdk/type/droplet_create_ssh_keys.py)<a id="ssh_keys-dropletcreatesshkeysdigital_ocean_python_sdktypedroplet_create_ssh_keyspy"></a>

##### backups: `bool`<a id="backups-bool"></a>

A boolean indicating whether automated backups should be enabled for the Droplet.

##### ipv6: `bool`<a id="ipv6-bool"></a>

A boolean indicating whether to enable IPv6 on the Droplet.

##### monitoring: `bool`<a id="monitoring-bool"></a>

A boolean indicating whether to install the DigitalOcean agent for monitoring.

##### user_data: `str`<a id="user_data-str"></a>

A string containing 'user data' which may be used to configure the Droplet on first boot, often a 'cloud-config' file or Bash script. It must be plain text and may not exceed 64 KiB in size.

##### private_networking: `bool`<a id="private_networking-bool"></a>

This parameter has been deprecated. Use `vpc_uuid` instead to specify a VPC network for the Droplet. If no `vpc_uuid` is provided, the Droplet will be placed in your account's default VPC for the region.

##### volumes: [`DropletCreateVolumes`](./digital_ocean_python_sdk/type/droplet_create_volumes.py)<a id="volumes-dropletcreatevolumesdigital_ocean_python_sdktypedroplet_create_volumespy"></a>

##### vpc_uuid: `str`<a id="vpc_uuid-str"></a>

A string specifying the UUID of the VPC to which the Droplet will be assigned. If excluded, the Droplet will be assigned to your account's default VPC for the region.

##### with_droplet_agent: `bool`<a id="with_droplet_agent-bool"></a>

A boolean indicating whether to install the DigitalOcean agent used for providing access to the Droplet web console in the control panel. By default, the agent is installed on new Droplets but installation errors (i.e. OS not supported) are ignored. To prevent it from being installed, set to `false`. To make installation errors fatal, explicitly set it to `true`.

##### names: List[`str`]<a id="names-liststr"></a>

An array of human human-readable strings you wish to use when displaying the Droplet name. Each name, if set to a domain name managed in the DigitalOcean DNS management system, will configure a PTR record for the Droplet. Each name set during creation will also determine the hostname for the Droplet in its internal configuration.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`DropletsCreateRequest`](./digital_ocean_python_sdk/type/droplets_create_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`DropletsCreateResponse`](./digital_ocean_python_sdk/pydantic/droplets_create_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/droplets` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.droplets.delete_by_tag`<a id="digitaloceandropletsdelete_by_tag"></a>

To delete **all** Droplets assigned to a specific tag, include the `tag_name`
query parameter set to the name of the tag in your DELETE request. For
example,  `/v2/droplets?tag_name=$TAG_NAME`.

A successful request will receive a 204 status code with no body in response.
This indicates that the request was processed successfully.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.droplets.delete_by_tag(
    tag_name="env:test",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### tag_name: `str`<a id="tag_name-str"></a>

Specifies Droplets to be deleted by tag.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/droplets` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.droplets.delete_dangerous`<a id="digitaloceandropletsdelete_dangerous"></a>

To destroy a Droplet along with all of its associated resources, send a DELETE
request to the `/v2/droplets/$DROPLET_ID/destroy_with_associated_resources/dangerous`
endpoint. The headers of this request must include an `X-Dangerous` key set to
`true`. To preview which resources will be destroyed, first query the
Droplet's associated resources. This operation _can not_ be reverse and should
be used with caution.

A successful response will include a 202 response code and no content. Use the
status endpoint to check on the success or failure of the destruction of the
individual resources.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.droplets.delete_dangerous(
    droplet_id=3164444,
    x_dangerous=True,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### droplet_id: `int`<a id="droplet_id-int"></a>

A unique identifier for a Droplet instance.

##### x_dangerous: `bool`<a id="x_dangerous-bool"></a>

Acknowledge this action will destroy the Droplet and all associated resources and _can not_ be reversed.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/droplets/{droplet_id}/destroy_with_associated_resources/dangerous` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.droplets.destroy`<a id="digitaloceandropletsdestroy"></a>

To delete a Droplet, send a DELETE request to `/v2/droplets/$DROPLET_ID`.

A successful request will receive a 204 status code with no body in response.
This indicates that the request was processed successfully.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.droplets.destroy(
    droplet_id=3164444,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### droplet_id: `int`<a id="droplet_id-int"></a>

A unique identifier for a Droplet instance.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/droplets/{droplet_id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.droplets.destroy_associated_resources_selective`<a id="digitaloceandropletsdestroy_associated_resources_selective"></a>

To destroy a Droplet along with a sub-set of its associated resources, send a
DELETE request to the `/v2/droplets/$DROPLET_ID/destroy_with_associated_resources/selective`
endpoint. The JSON body of the request should include `reserved_ips`, `snapshots`, `volumes`,
or `volume_snapshots` keys each set to an array of IDs for the associated
resources to be destroyed. The IDs can be found by querying the Droplet's
associated resources. Any associated resource not included in the request
will remain and continue to accrue changes on your account.

A successful response will include a 202 response code and no content. Use
the status endpoint to check on the success or failure of the destruction of
the individual resources.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.droplets.destroy_associated_resources_selective(
    droplet_id=3164444,
    floating_ips=["6186916"],
    reserved_ips=["6186916"],
    snapshots=["61486916"],
    volumes=["ba49449a-7435-11ea-b89e-0a58ac14480f"],
    volume_snapshots=["edb0478d-7436-11ea-86e6-0a58ac144b91"],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### droplet_id: `int`<a id="droplet_id-int"></a>

A unique identifier for a Droplet instance.

##### floating_ips: [`SelectiveDestroyAssociatedResourceFloatingIps`](./digital_ocean_python_sdk/type/selective_destroy_associated_resource_floating_ips.py)<a id="floating_ips-selectivedestroyassociatedresourcefloatingipsdigital_ocean_python_sdktypeselective_destroy_associated_resource_floating_ipspy"></a>

##### reserved_ips: [`SelectiveDestroyAssociatedResourceReservedIps`](./digital_ocean_python_sdk/type/selective_destroy_associated_resource_reserved_ips.py)<a id="reserved_ips-selectivedestroyassociatedresourcereservedipsdigital_ocean_python_sdktypeselective_destroy_associated_resource_reserved_ipspy"></a>

##### snapshots: [`SelectiveDestroyAssociatedResourceSnapshots`](./digital_ocean_python_sdk/type/selective_destroy_associated_resource_snapshots.py)<a id="snapshots-selectivedestroyassociatedresourcesnapshotsdigital_ocean_python_sdktypeselective_destroy_associated_resource_snapshotspy"></a>

##### volumes: [`SelectiveDestroyAssociatedResourceVolumes`](./digital_ocean_python_sdk/type/selective_destroy_associated_resource_volumes.py)<a id="volumes-selectivedestroyassociatedresourcevolumesdigital_ocean_python_sdktypeselective_destroy_associated_resource_volumespy"></a>

##### volume_snapshots: [`SelectiveDestroyAssociatedResourceVolumeSnapshots`](./digital_ocean_python_sdk/type/selective_destroy_associated_resource_volume_snapshots.py)<a id="volume_snapshots-selectivedestroyassociatedresourcevolumesnapshotsdigital_ocean_python_sdktypeselective_destroy_associated_resource_volume_snapshotspy"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`SelectiveDestroyAssociatedResource`](./digital_ocean_python_sdk/type/selective_destroy_associated_resource.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/droplets/{droplet_id}/destroy_with_associated_resources/selective` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.droplets.get`<a id="digitaloceandropletsget"></a>

To show information about an individual Droplet, send a GET request to
`/v2/droplets/$DROPLET_ID`.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_response = digitalocean.droplets.get(
    droplet_id=3164444,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### droplet_id: `int`<a id="droplet_id-int"></a>

A unique identifier for a Droplet instance.

#### 🔄 Return<a id="🔄-return"></a>

[`DropletsGetResponse`](./digital_ocean_python_sdk/pydantic/droplets_get_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/droplets/{droplet_id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.droplets.list`<a id="digitaloceandropletslist"></a>

To list all Droplets in your account, send a GET request to `/v2/droplets`.

The response body will be a JSON object with a key of `droplets`. This will be
set to an array containing objects each representing a Droplet. These will
contain the standard Droplet attributes.

### Filtering Results by Tag<a id="filtering-results-by-tag"></a>

It's possible to request filtered results by including certain query parameters.
To only list Droplets assigned to a specific tag, include the `tag_name` query
parameter set to the name of the tag in your GET request. For example,
`/v2/droplets?tag_name=$TAG_NAME`.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = digitalocean.droplets.list(
    per_page=2,
    page=1,
    tag_name="env:prod",
    name="web-01",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### per_page: `int`<a id="per_page-int"></a>

Number of items returned per page

##### page: `int`<a id="page-int"></a>

Which 'page' of paginated results to return.

##### tag_name: `str`<a id="tag_name-str"></a>

Used to filter Droplets by a specific tag. Can not be combined with `name`.

##### name: `str`<a id="name-str"></a>

Used to filter list response by Droplet name returning only exact matches. It is case-insensitive and can not be combined with `tag_name`.

#### 🔄 Return<a id="🔄-return"></a>

[`DropletsListResponse`](./digital_ocean_python_sdk/pydantic/droplets_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/droplets` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.droplets.list_associated_resources`<a id="digitaloceandropletslist_associated_resources"></a>

To list the associated billable resources that can be destroyed along with a
Droplet, send a GET request to the
`/v2/droplets/$DROPLET_ID/destroy_with_associated_resources` endpoint.

The response will be a JSON object containing `snapshots`, `volumes`, and
`volume_snapshots` keys. Each will be set to an array of objects containing
information about the associated resources.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_associated_resources_response = digitalocean.droplets.list_associated_resources(
    droplet_id=3164444,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### droplet_id: `int`<a id="droplet_id-int"></a>

A unique identifier for a Droplet instance.

#### 🔄 Return<a id="🔄-return"></a>

[`DropletsListAssociatedResourcesResponse`](./digital_ocean_python_sdk/pydantic/droplets_list_associated_resources_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/droplets/{droplet_id}/destroy_with_associated_resources` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.droplets.list_backups`<a id="digitaloceandropletslist_backups"></a>

To retrieve any backups associated with a Droplet, send a GET request to
`/v2/droplets/$DROPLET_ID/backups`.

You will get back a JSON object that has a `backups` key. This will be set to
an array of backup objects, each of which contain the standard
Droplet backup attributes.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_backups_response = digitalocean.droplets.list_backups(
    droplet_id=3164444,
    per_page=2,
    page=1,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### droplet_id: `int`<a id="droplet_id-int"></a>

A unique identifier for a Droplet instance.

##### per_page: `int`<a id="per_page-int"></a>

Number of items returned per page

##### page: `int`<a id="page-int"></a>

Which 'page' of paginated results to return.

#### 🔄 Return<a id="🔄-return"></a>

[`DropletsListBackupsResponse`](./digital_ocean_python_sdk/pydantic/droplets_list_backups_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/droplets/{droplet_id}/backups` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.droplets.list_droplet_neighbors`<a id="digitaloceandropletslist_droplet_neighbors"></a>

To retrieve a list of all Droplets that are co-located on the same physical
hardware, send a GET request to `/v2/reports/droplet_neighbors_ids`.

The results will be returned as a JSON object with a key of `neighbor_ids`.
This will be set to an array of arrays. Each array will contain a set of
Droplet IDs for Droplets that share a physical server. An empty array
indicates that all Droplets associated with your account are located on
separate physical hardware.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_droplet_neighbors_response = digitalocean.droplets.list_droplet_neighbors()
```

#### 🔄 Return<a id="🔄-return"></a>

[`NeighborIds`](./digital_ocean_python_sdk/pydantic/neighbor_ids.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/reports/droplet_neighbors_ids` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.droplets.list_firewalls`<a id="digitaloceandropletslist_firewalls"></a>

To retrieve a list of all firewalls available to a Droplet, send a GET request
to `/v2/droplets/$DROPLET_ID/firewalls`

The response will be a JSON object that has a key called `firewalls`. This will
be set to an array of `firewall` objects, each of which contain the standard
`firewall` attributes.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_firewalls_response = digitalocean.droplets.list_firewalls(
    droplet_id=3164444,
    per_page=2,
    page=1,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### droplet_id: `int`<a id="droplet_id-int"></a>

A unique identifier for a Droplet instance.

##### per_page: `int`<a id="per_page-int"></a>

Number of items returned per page

##### page: `int`<a id="page-int"></a>

Which 'page' of paginated results to return.

#### 🔄 Return<a id="🔄-return"></a>

[`DropletsListFirewallsResponse`](./digital_ocean_python_sdk/pydantic/droplets_list_firewalls_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/droplets/{droplet_id}/firewalls` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.droplets.list_kernels`<a id="digitaloceandropletslist_kernels"></a>

To retrieve a list of all kernels available to a Droplet, send a GET request
to `/v2/droplets/$DROPLET_ID/kernels`

The response will be a JSON object that has a key called `kernels`. This will
be set to an array of `kernel` objects, each of which contain the standard
`kernel` attributes.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_kernels_response = digitalocean.droplets.list_kernels(
    droplet_id=3164444,
    per_page=2,
    page=1,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### droplet_id: `int`<a id="droplet_id-int"></a>

A unique identifier for a Droplet instance.

##### per_page: `int`<a id="per_page-int"></a>

Number of items returned per page

##### page: `int`<a id="page-int"></a>

Which 'page' of paginated results to return.

#### 🔄 Return<a id="🔄-return"></a>

[`DropletsListKernelsResponse`](./digital_ocean_python_sdk/pydantic/droplets_list_kernels_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/droplets/{droplet_id}/kernels` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.droplets.list_neighbors`<a id="digitaloceandropletslist_neighbors"></a>

To retrieve a list of any "neighbors" (i.e. Droplets that are co-located on
the same physical hardware) for a specific Droplet, send a GET request to
`/v2/droplets/$DROPLET_ID/neighbors`.

The results will be returned as a JSON object with a key of `droplets`. This
will be set to an array containing objects representing any other Droplets
that share the same physical hardware. An empty array indicates that the
Droplet is not co-located any other Droplets associated with your account.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_neighbors_response = digitalocean.droplets.list_neighbors(
    droplet_id=3164444,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### droplet_id: `int`<a id="droplet_id-int"></a>

A unique identifier for a Droplet instance.

#### 🔄 Return<a id="🔄-return"></a>

[`DropletsListNeighborsResponse`](./digital_ocean_python_sdk/pydantic/droplets_list_neighbors_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/droplets/{droplet_id}/neighbors` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.droplets.list_snapshots`<a id="digitaloceandropletslist_snapshots"></a>

To retrieve the snapshots that have been created from a Droplet, send a GET
request to `/v2/droplets/$DROPLET_ID/snapshots`.

You will get back a JSON object that has a `snapshots` key. This will be set
to an array of snapshot objects, each of which contain the standard Droplet
snapshot attributes.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_snapshots_response = digitalocean.droplets.list_snapshots(
    droplet_id=3164444,
    per_page=2,
    page=1,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### droplet_id: `int`<a id="droplet_id-int"></a>

A unique identifier for a Droplet instance.

##### per_page: `int`<a id="per_page-int"></a>

Number of items returned per page

##### page: `int`<a id="page-int"></a>

Which 'page' of paginated results to return.

#### 🔄 Return<a id="🔄-return"></a>

[`DropletsListSnapshotsResponse`](./digital_ocean_python_sdk/pydantic/droplets_list_snapshots_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/droplets/{droplet_id}/snapshots` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.droplets.retry_destroy_with_associated_resources`<a id="digitaloceandropletsretry_destroy_with_associated_resources"></a>

If the status of a request to destroy a Droplet with its associated resources
reported any errors, it can be retried by sending a POST request to the
`/v2/droplets/$DROPLET_ID/destroy_with_associated_resources/retry` endpoint.

Only one destroy can be active at a time per Droplet. If a retry is issued
while another destroy is in progress for the Droplet a 409 status code will
be returned. A successful response will include a 202 response code and no
content.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.droplets.retry_destroy_with_associated_resources(
    droplet_id=3164444,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### droplet_id: `int`<a id="droplet_id-int"></a>

A unique identifier for a Droplet instance.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/droplets/{droplet_id}/destroy_with_associated_resources/retry` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.firewalls.add_droplets`<a id="digitaloceanfirewallsadd_droplets"></a>

To assign a Droplet to a firewall, send a POST request to
`/v2/firewalls/$FIREWALL_ID/droplets`. In the body of the request, there
should be a `droplet_ids` attribute containing a list of Droplet IDs.

No response body will be sent back, but the response code will indicate
success. Specifically, the response code will be a 204, which means that the
action was successful with no returned body data.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.firewalls.add_droplets(
    body=None,
    droplet_ids=[49696269],
    firewall_id="bb4b2611-3d72-467b-8602-280330ecd65c",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### droplet_ids: List[`int`]<a id="droplet_ids-listint"></a>

An array containing the IDs of the Droplets to be assigned to the firewall.

##### firewall_id: `str`<a id="firewall_id-str"></a>

A unique ID that can be used to identify and reference a firewall.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`FirewallsAddDropletsRequest`](./digital_ocean_python_sdk/type/firewalls_add_droplets_request.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/firewalls/{firewall_id}/droplets` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.firewalls.add_rules`<a id="digitaloceanfirewallsadd_rules"></a>

To add additional access rules to a firewall, send a POST request to
`/v2/firewalls/$FIREWALL_ID/rules`. The body of the request may include an
inbound_rules and/or outbound_rules attribute containing an array of rules to
be added.

No response body will be sent back, but the response code will indicate
success. Specifically, the response code will be a 204, which means that the
action was successful with no returned body data.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.firewalls.add_rules(
    body=None,
    firewall_id="bb4b2611-3d72-467b-8602-280330ecd65c",
    inbound_rules=[
        None
    ],
    outbound_rules=[
        None
    ],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### firewall_id: `str`<a id="firewall_id-str"></a>

A unique ID that can be used to identify and reference a firewall.

##### inbound_rules: [`FirewallRulesInboundRules`](./digital_ocean_python_sdk/type/firewall_rules_inbound_rules.py)<a id="inbound_rules-firewallrulesinboundrulesdigital_ocean_python_sdktypefirewall_rules_inbound_rulespy"></a>

##### outbound_rules: [`FirewallRulesOutboundRules`](./digital_ocean_python_sdk/type/firewall_rules_outbound_rules.py)<a id="outbound_rules-firewallrulesoutboundrulesdigital_ocean_python_sdktypefirewall_rules_outbound_rulespy"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`FirewallsAddRulesRequest`](./digital_ocean_python_sdk/type/firewalls_add_rules_request.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/firewalls/{firewall_id}/rules` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.firewalls.add_tags`<a id="digitaloceanfirewallsadd_tags"></a>

To assign a tag representing a group of Droplets to a firewall, send a POST
request to `/v2/firewalls/$FIREWALL_ID/tags`. In the body of the request,
there should be a `tags` attribute containing a list of tag names.

No response body will be sent back, but the response code will indicate
success. Specifically, the response code will be a 204, which means that the
action was successful with no returned body data.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.firewalls.add_tags(
    body=None,
    tags=None,
    firewall_id="bb4b2611-3d72-467b-8602-280330ecd65c",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### tags: Union[[`TagsArray`](./digital_ocean_python_sdk/type/tags_array.py), [`Union[bool, date, datetime, dict, float, int, list, str, None]`](./digital_ocean_python_sdk/type/typing_union_bool_date_datetime_dict_float_int_list_str_none.py)]<a id="tags-uniontagsarraydigital_ocean_python_sdktypetags_arraypy-unionbool-date-datetime-dict-float-int-list-str-nonedigital_ocean_python_sdktypetyping_union_bool_date_datetime_dict_float_int_list_str_nonepy"></a>


##### firewall_id: `str`<a id="firewall_id-str"></a>

A unique ID that can be used to identify and reference a firewall.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`FirewallsAddTagsRequest`](./digital_ocean_python_sdk/type/firewalls_add_tags_request.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/firewalls/{firewall_id}/tags` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.firewalls.create`<a id="digitaloceanfirewallscreate"></a>

To create a new firewall, send a POST request to `/v2/firewalls`. The request
must contain at least one inbound or outbound access rule.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_response = digitalocean.firewalls.create(
    body=None,
    tags=None,
    id="bb4b2611-3d72-467b-8602-280330ecd65c",
    status="waiting",
    created_at="2020-05-23T21:24:00Z",
    pending_changes=[{
    "droplet_id": 8043964,
    "removing": False,
    "status": "waiting",
}],
    name="firewall",
    droplet_ids=[8043964],
    inbound_rules=[
        None
    ],
    outbound_rules=[
        None
    ],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### tags: Union[[`TagsArray`](./digital_ocean_python_sdk/type/tags_array.py), [`Union[bool, date, datetime, dict, float, int, list, str, None]`](./digital_ocean_python_sdk/type/typing_union_bool_date_datetime_dict_float_int_list_str_none.py)]<a id="tags-uniontagsarraydigital_ocean_python_sdktypetags_arraypy-unionbool-date-datetime-dict-float-int-list-str-nonedigital_ocean_python_sdktypetyping_union_bool_date_datetime_dict_float_int_list_str_nonepy"></a>


##### id: `str`<a id="id-str"></a>

A unique ID that can be used to identify and reference a firewall.

##### status: `str`<a id="status-str"></a>

A status string indicating the current state of the firewall. This can be \\\"waiting\\\", \\\"succeeded\\\", or \\\"failed\\\".

##### created_at: `datetime`<a id="created_at-datetime"></a>

A time value given in ISO8601 combined date and time format that represents when the firewall was created.

##### pending_changes: List[`Dict[str, Union[bool, date, datetime, dict, float, int, list, str, None]]`]<a id="pending_changes-listdictstr-unionbool-date-datetime-dict-float-int-list-str-none"></a>

An array of objects each containing the fields \\\"droplet_id\\\", \\\"removing\\\", and \\\"status\\\". It is provided to detail exactly which Droplets are having their security policies updated. When empty, all changes have been successfully applied.

##### name: `str`<a id="name-str"></a>

A human-readable name for a firewall. The name must begin with an alphanumeric character. Subsequent characters must either be alphanumeric characters, a period (.), or a dash (-).

##### droplet_ids: List[`int`]<a id="droplet_ids-listint"></a>

An array containing the IDs of the Droplets assigned to the firewall.

##### inbound_rules: [`FirewallRulesInboundRules`](./digital_ocean_python_sdk/type/firewall_rules_inbound_rules.py)<a id="inbound_rules-firewallrulesinboundrulesdigital_ocean_python_sdktypefirewall_rules_inbound_rulespy"></a>

##### outbound_rules: [`FirewallRulesOutboundRules`](./digital_ocean_python_sdk/type/firewall_rules_outbound_rules.py)<a id="outbound_rules-firewallrulesoutboundrulesdigital_ocean_python_sdktypefirewall_rules_outbound_rulespy"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`FirewallsCreateRequest`](./digital_ocean_python_sdk/type/firewalls_create_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`FirewallsCreateResponse`](./digital_ocean_python_sdk/pydantic/firewalls_create_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/firewalls` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.firewalls.delete`<a id="digitaloceanfirewallsdelete"></a>

To delete a firewall send a DELETE request to `/v2/firewalls/$FIREWALL_ID`.

No response body will be sent back, but the response code will indicate
success. Specifically, the response code will be a 204, which means that the
action was successful with no returned body data.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.firewalls.delete(
    firewall_id="bb4b2611-3d72-467b-8602-280330ecd65c",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### firewall_id: `str`<a id="firewall_id-str"></a>

A unique ID that can be used to identify and reference a firewall.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/firewalls/{firewall_id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.firewalls.get`<a id="digitaloceanfirewallsget"></a>

To show information about an existing firewall, send a GET request to `/v2/firewalls/$FIREWALL_ID`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_response = digitalocean.firewalls.get(
    firewall_id="bb4b2611-3d72-467b-8602-280330ecd65c",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### firewall_id: `str`<a id="firewall_id-str"></a>

A unique ID that can be used to identify and reference a firewall.

#### 🔄 Return<a id="🔄-return"></a>

[`FirewallsGetResponse`](./digital_ocean_python_sdk/pydantic/firewalls_get_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/firewalls/{firewall_id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.firewalls.list`<a id="digitaloceanfirewallslist"></a>

To list all of the firewalls available on your account, send a GET request to `/v2/firewalls`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = digitalocean.firewalls.list(
    per_page=2,
    page=1,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### per_page: `int`<a id="per_page-int"></a>

Number of items returned per page

##### page: `int`<a id="page-int"></a>

Which 'page' of paginated results to return.

#### 🔄 Return<a id="🔄-return"></a>

[`FirewallsListResponse`](./digital_ocean_python_sdk/pydantic/firewalls_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/firewalls` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.firewalls.remove_droplets`<a id="digitaloceanfirewallsremove_droplets"></a>

To remove a Droplet from a firewall, send a DELETE request to
`/v2/firewalls/$FIREWALL_ID/droplets`. In the body of the request, there should
be a `droplet_ids` attribute containing a list of Droplet IDs.

No response body will be sent back, but the response code will indicate
success. Specifically, the response code will be a 204, which means that the
action was successful with no returned body data.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.firewalls.remove_droplets(
    body=None,
    droplet_ids=[49696269],
    firewall_id="bb4b2611-3d72-467b-8602-280330ecd65c",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### droplet_ids: List[`int`]<a id="droplet_ids-listint"></a>

An array containing the IDs of the Droplets to be removed from the firewall.

##### firewall_id: `str`<a id="firewall_id-str"></a>

A unique ID that can be used to identify and reference a firewall.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`FirewallsRemoveDropletsRequest`](./digital_ocean_python_sdk/type/firewalls_remove_droplets_request.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/firewalls/{firewall_id}/droplets` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.firewalls.remove_rules`<a id="digitaloceanfirewallsremove_rules"></a>

To remove access rules from a firewall, send a DELETE request to
`/v2/firewalls/$FIREWALL_ID/rules`. The body of the request may include an
`inbound_rules` and/or `outbound_rules` attribute containing an array of rules
to be removed.

No response body will be sent back, but the response code will indicate
success. Specifically, the response code will be a 204, which means that the
action was successful with no returned body data.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.firewalls.remove_rules(
    body=None,
    firewall_id="bb4b2611-3d72-467b-8602-280330ecd65c",
    inbound_rules=[
        None
    ],
    outbound_rules=[
        None
    ],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### firewall_id: `str`<a id="firewall_id-str"></a>

A unique ID that can be used to identify and reference a firewall.

##### inbound_rules: [`FirewallRulesInboundRules`](./digital_ocean_python_sdk/type/firewall_rules_inbound_rules.py)<a id="inbound_rules-firewallrulesinboundrulesdigital_ocean_python_sdktypefirewall_rules_inbound_rulespy"></a>

##### outbound_rules: [`FirewallRulesOutboundRules`](./digital_ocean_python_sdk/type/firewall_rules_outbound_rules.py)<a id="outbound_rules-firewallrulesoutboundrulesdigital_ocean_python_sdktypefirewall_rules_outbound_rulespy"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`FirewallsRemoveRulesRequest`](./digital_ocean_python_sdk/type/firewalls_remove_rules_request.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/firewalls/{firewall_id}/rules` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.firewalls.remove_tags`<a id="digitaloceanfirewallsremove_tags"></a>

To remove a tag representing a group of Droplets from a firewall, send a
DELETE request to `/v2/firewalls/$FIREWALL_ID/tags`. In the body of the
request, there should be a `tags` attribute containing a list of tag names.

No response body will be sent back, but the response code will indicate
success. Specifically, the response code will be a 204, which means that the
action was successful with no returned body data.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.firewalls.remove_tags(
    body=None,
    tags=None,
    firewall_id="bb4b2611-3d72-467b-8602-280330ecd65c",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### tags: Union[[`TagsArray`](./digital_ocean_python_sdk/type/tags_array.py), [`Union[bool, date, datetime, dict, float, int, list, str, None]`](./digital_ocean_python_sdk/type/typing_union_bool_date_datetime_dict_float_int_list_str_none.py)]<a id="tags-uniontagsarraydigital_ocean_python_sdktypetags_arraypy-unionbool-date-datetime-dict-float-int-list-str-nonedigital_ocean_python_sdktypetyping_union_bool_date_datetime_dict_float_int_list_str_nonepy"></a>


##### firewall_id: `str`<a id="firewall_id-str"></a>

A unique ID that can be used to identify and reference a firewall.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`FirewallsRemoveTagsRequest`](./digital_ocean_python_sdk/type/firewalls_remove_tags_request.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/firewalls/{firewall_id}/tags` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.firewalls.update`<a id="digitaloceanfirewallsupdate"></a>

To update the configuration of an existing firewall, send a PUT request to
`/v2/firewalls/$FIREWALL_ID`. The request should contain a full representation
of the firewall including existing attributes. **Note that any attributes that
are not provided will be reset to their default values.**


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_response = digitalocean.firewalls.update(
    body=None,
    name="firewall",
    firewall_id="bb4b2611-3d72-467b-8602-280330ecd65c",
    tags=None,
    id="bb4b2611-3d72-467b-8602-280330ecd65c",
    status="waiting",
    created_at="2020-05-23T21:24:00Z",
    pending_changes=[{
    "droplet_id": 8043964,
    "removing": False,
    "status": "waiting",
}],
    droplet_ids=[8043964],
    inbound_rules=[
        None
    ],
    outbound_rules=[
        None
    ],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### name: `str`<a id="name-str"></a>

A human-readable name for a firewall. The name must begin with an alphanumeric character. Subsequent characters must either be alphanumeric characters, a period (.), or a dash (-).

##### firewall_id: `str`<a id="firewall_id-str"></a>

A unique ID that can be used to identify and reference a firewall.

##### tags: Union[[`TagsArray`](./digital_ocean_python_sdk/type/tags_array.py), [`Union[bool, date, datetime, dict, float, int, list, str, None]`](./digital_ocean_python_sdk/type/typing_union_bool_date_datetime_dict_float_int_list_str_none.py)]<a id="tags-uniontagsarraydigital_ocean_python_sdktypetags_arraypy-unionbool-date-datetime-dict-float-int-list-str-nonedigital_ocean_python_sdktypetyping_union_bool_date_datetime_dict_float_int_list_str_nonepy"></a>


##### id: `str`<a id="id-str"></a>

A unique ID that can be used to identify and reference a firewall.

##### status: `str`<a id="status-str"></a>

A status string indicating the current state of the firewall. This can be \\\"waiting\\\", \\\"succeeded\\\", or \\\"failed\\\".

##### created_at: `datetime`<a id="created_at-datetime"></a>

A time value given in ISO8601 combined date and time format that represents when the firewall was created.

##### pending_changes: List[`Dict[str, Union[bool, date, datetime, dict, float, int, list, str, None]]`]<a id="pending_changes-listdictstr-unionbool-date-datetime-dict-float-int-list-str-none"></a>

An array of objects each containing the fields \\\"droplet_id\\\", \\\"removing\\\", and \\\"status\\\". It is provided to detail exactly which Droplets are having their security policies updated. When empty, all changes have been successfully applied.

##### droplet_ids: List[`int`]<a id="droplet_ids-listint"></a>

An array containing the IDs of the Droplets assigned to the firewall.

##### inbound_rules: [`FirewallRulesInboundRules`](./digital_ocean_python_sdk/type/firewall_rules_inbound_rules.py)<a id="inbound_rules-firewallrulesinboundrulesdigital_ocean_python_sdktypefirewall_rules_inbound_rulespy"></a>

##### outbound_rules: [`FirewallRulesOutboundRules`](./digital_ocean_python_sdk/type/firewall_rules_outbound_rules.py)<a id="outbound_rules-firewallrulesoutboundrulesdigital_ocean_python_sdktypefirewall_rules_outbound_rulespy"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`FirewallsUpdateRequest`](./digital_ocean_python_sdk/type/firewalls_update_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`FirewallsUpdateResponse`](./digital_ocean_python_sdk/pydantic/firewalls_update_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/firewalls/{firewall_id}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.floating_ip_actions.get`<a id="digitaloceanfloating_ip_actionsget"></a>

To retrieve the status of a floating IP action, send a GET request to `/v2/floating_ips/$FLOATING_IP/actions/$ACTION_ID`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_response = digitalocean.floating_ip_actions.get(
    floating_ip="45.55.96.47",
    action_id=36804636,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### floating_ip: `str`<a id="floating_ip-str"></a>

A floating IP address.

##### action_id: `int`<a id="action_id-int"></a>

A unique numeric ID that can be used to identify and reference an action.

#### 🔄 Return<a id="🔄-return"></a>

[`FloatingIPsActionPostResponse`](./digital_ocean_python_sdk/pydantic/floating_ips_action_post_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/floating_ips/{floating_ip}/actions/{action_id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.floating_ip_actions.list`<a id="digitaloceanfloating_ip_actionslist"></a>

To retrieve all actions that have been executed on a floating IP, send a GET request to `/v2/floating_ips/$FLOATING_IP/actions`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = digitalocean.floating_ip_actions.list(
    floating_ip="45.55.96.47",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### floating_ip: `str`<a id="floating_ip-str"></a>

A floating IP address.

#### 🔄 Return<a id="🔄-return"></a>

[`FloatingIPsActionListResponse`](./digital_ocean_python_sdk/pydantic/floating_ips_action_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/floating_ips/{floating_ip}/actions` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.floating_ip_actions.post`<a id="digitaloceanfloating_ip_actionspost"></a>

To initiate an action on a floating IP send a POST request to
`/v2/floating_ips/$FLOATING_IP/actions`. In the JSON body to the request,
set the `type` attribute to on of the supported action types:

| Action     | Details
|------------|--------
| `assign`   | Assigns a floating IP to a Droplet
| `unassign` | Unassign a floating IP from a Droplet


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
post_response = digitalocean.floating_ip_actions.post(
    body=None,
    floating_ip="45.55.96.47",
    type="assign",
    droplet_id=758604968,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### floating_ip: `str`<a id="floating_ip-str"></a>

A floating IP address.

##### type: `str`<a id="type-str"></a>

The type of action to initiate for the floating IP.

##### droplet_id: `int`<a id="droplet_id-int"></a>

The ID of the Droplet that the floating IP will be assigned to.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`FloatingIPsActionPostRequest`](./digital_ocean_python_sdk/type/floating_ips_action_post_request.py)
The `type` attribute set in the request body will specify the action that will be taken on the floating IP. 

#### 🔄 Return<a id="🔄-return"></a>

[`FloatingIPsActionPostResponse`](./digital_ocean_python_sdk/pydantic/floating_ips_action_post_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/floating_ips/{floating_ip}/actions` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.floating_ips.create`<a id="digitaloceanfloating_ipscreate"></a>

On creation, a floating IP must be either assigned to a Droplet or reserved to a region.
* To create a new floating IP assigned to a Droplet, send a POST
  request to `/v2/floating_ips` with the `droplet_id` attribute.

* To create a new floating IP reserved to a region, send a POST request to
  `/v2/floating_ips` with the `region` attribute.

**Note**:  In addition to the standard rate limiting, only 12 floating IPs may be created per 60 seconds.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_response = digitalocean.floating_ips.create(
    body=None,
    droplet_id=2457247,
    region="nyc3",
    project_id="746c6152-2fa2-11ed-92d3-27aaa54e4988",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### droplet_id: `int`<a id="droplet_id-int"></a>

The ID of the Droplet that the floating IP will be assigned to.

##### region: `str`<a id="region-str"></a>

The slug identifier for the region the floating IP will be reserved to.

##### project_id: `str`<a id="project_id-str"></a>

The UUID of the project to which the floating IP will be assigned.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`FloatingIpCreate`](./digital_ocean_python_sdk/type/floating_ip_create.py)
#### 🔄 Return<a id="🔄-return"></a>

[`FloatingIPsCreateResponse`](./digital_ocean_python_sdk/pydantic/floating_ips_create_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/floating_ips` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.floating_ips.delete`<a id="digitaloceanfloating_ipsdelete"></a>

To delete a floating IP and remove it from your account, send a DELETE request
to `/v2/floating_ips/$FLOATING_IP_ADDR`.

A successful request will receive a 204 status code with no body in response.
This indicates that the request was processed successfully.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.floating_ips.delete(
    floating_ip="45.55.96.47",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### floating_ip: `str`<a id="floating_ip-str"></a>

A floating IP address.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/floating_ips/{floating_ip}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.floating_ips.get`<a id="digitaloceanfloating_ipsget"></a>

To show information about a floating IP, send a GET request to `/v2/floating_ips/$FLOATING_IP_ADDR`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_response = digitalocean.floating_ips.get(
    floating_ip="45.55.96.47",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### floating_ip: `str`<a id="floating_ip-str"></a>

A floating IP address.

#### 🔄 Return<a id="🔄-return"></a>

[`FloatingIPsGetResponse`](./digital_ocean_python_sdk/pydantic/floating_ips_get_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/floating_ips/{floating_ip}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.floating_ips.list`<a id="digitaloceanfloating_ipslist"></a>

To list all of the floating IPs available on your account, send a GET request to `/v2/floating_ips`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = digitalocean.floating_ips.list(
    per_page=2,
    page=1,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### per_page: `int`<a id="per_page-int"></a>

Number of items returned per page

##### page: `int`<a id="page-int"></a>

Which 'page' of paginated results to return.

#### 🔄 Return<a id="🔄-return"></a>

[`FloatingIPsListResponse`](./digital_ocean_python_sdk/pydantic/floating_ips_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/floating_ips` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.functions.create_namespace`<a id="digitaloceanfunctionscreate_namespace"></a>

Creates a new serverless functions namespace in the desired region and associates it with the provided label. A namespace is a collection of functions and their associated packages, triggers, and project specifications. To create a namespace, send a POST request to `/v2/functions/namespaces` with the `region` and `label` properties.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_namespace_response = digitalocean.functions.create_namespace(
    region="nyc1",
    label="my namespace",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### region: `str`<a id="region-str"></a>

The [datacenter region](https://docs.digitalocean.com/products/platform/availability-matrix/#available-datacenters) in which to create the namespace.

##### label: `str`<a id="label-str"></a>

The namespace's unique name.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`CreateNamespace`](./digital_ocean_python_sdk/type/create_namespace.py)
#### 🔄 Return<a id="🔄-return"></a>

[`FunctionsCreateNamespaceResponse`](./digital_ocean_python_sdk/pydantic/functions_create_namespace_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/functions/namespaces` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.functions.create_trigger_in_namespace`<a id="digitaloceanfunctionscreate_trigger_in_namespace"></a>

Creates a new trigger for a given function in a namespace. To create a trigger, send a POST request to `/v2/functions/namespaces/$NAMESPACE_ID/triggers` with the `name`, `function`, `type`, `is_enabled` and `scheduled_details` properties.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_trigger_in_namespace_response = digitalocean.functions.create_trigger_in_namespace(
    name="my trigger",
    function="hello",
    type="SCHEDULED",
    is_enabled=True,
    scheduled_details={
        "cron": "* * * * *",
    },
    namespace_id="fn-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### name: `str`<a id="name-str"></a>

The trigger's unique name within the namespace.

##### function: `str`<a id="function-str"></a>

Name of function(action) that exists in the given namespace.

##### type: `str`<a id="type-str"></a>

One of different type of triggers. Currently only SCHEDULED is supported.

##### is_enabled: `bool`<a id="is_enabled-bool"></a>

Indicates weather the trigger is paused or unpaused.

##### scheduled_details: [`ScheduledDetails`](./digital_ocean_python_sdk/type/scheduled_details.py)<a id="scheduled_details-scheduleddetailsdigital_ocean_python_sdktypescheduled_detailspy"></a>


##### namespace_id: `str`<a id="namespace_id-str"></a>

The ID of the namespace to be managed.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`CreateTrigger`](./digital_ocean_python_sdk/type/create_trigger.py)
#### 🔄 Return<a id="🔄-return"></a>

[`FunctionsCreateTriggerInNamespaceResponse`](./digital_ocean_python_sdk/pydantic/functions_create_trigger_in_namespace_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/functions/namespaces/{namespace_id}/triggers` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.functions.delete_namespace`<a id="digitaloceanfunctionsdelete_namespace"></a>

Deletes the given namespace.  When a namespace is deleted all assets, in the namespace are deleted, this includes packages, functions and triggers. Deleting a namespace is a destructive operation and assets in the namespace are not recoverable after deletion. Some metadata is retained, such as activations, or soft deleted for reporting purposes.
To delete namespace, send a DELETE request to `/v2/functions/namespaces/$NAMESPACE_ID`.
A successful deletion returns a 204 response.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.functions.delete_namespace(
    namespace_id="fn-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### namespace_id: `str`<a id="namespace_id-str"></a>

The ID of the namespace to be managed.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/functions/namespaces/{namespace_id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.functions.delete_trigger`<a id="digitaloceanfunctionsdelete_trigger"></a>

Deletes the given trigger.
To delete trigger, send a DELETE request to `/v2/functions/namespaces/$NAMESPACE_ID/triggers/$TRIGGER_NAME`.
A successful deletion returns a 204 response.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.functions.delete_trigger(
    namespace_id="fn-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    trigger_name="my trigger",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### namespace_id: `str`<a id="namespace_id-str"></a>

The ID of the namespace to be managed.

##### trigger_name: `str`<a id="trigger_name-str"></a>

The name of the trigger to be managed.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/functions/namespaces/{namespace_id}/triggers/{trigger_name}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.functions.get_namespace_details`<a id="digitaloceanfunctionsget_namespace_details"></a>

Gets the namespace details for the given namespace UUID. To get namespace details, send a GET request to `/v2/functions/namespaces/$NAMESPACE_ID` with no parameters.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_namespace_details_response = digitalocean.functions.get_namespace_details(
    namespace_id="fn-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### namespace_id: `str`<a id="namespace_id-str"></a>

The ID of the namespace to be managed.

#### 🔄 Return<a id="🔄-return"></a>

[`FunctionsCreateNamespaceResponse`](./digital_ocean_python_sdk/pydantic/functions_create_namespace_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/functions/namespaces/{namespace_id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.functions.get_trigger_details`<a id="digitaloceanfunctionsget_trigger_details"></a>

Gets the trigger details. To get the trigger details, send a GET request to `/v2/functions/namespaces/$NAMESPACE_ID/triggers/$TRIGGER_NAME`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_trigger_details_response = digitalocean.functions.get_trigger_details(
    namespace_id="fn-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    trigger_name="my trigger",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### namespace_id: `str`<a id="namespace_id-str"></a>

The ID of the namespace to be managed.

##### trigger_name: `str`<a id="trigger_name-str"></a>

The name of the trigger to be managed.

#### 🔄 Return<a id="🔄-return"></a>

[`FunctionsCreateTriggerInNamespaceResponse`](./digital_ocean_python_sdk/pydantic/functions_create_trigger_in_namespace_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/functions/namespaces/{namespace_id}/triggers/{trigger_name}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.functions.list_namespaces`<a id="digitaloceanfunctionslist_namespaces"></a>

Returns a list of namespaces associated with the current user. To get all namespaces, send a GET request to `/v2/functions/namespaces`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_namespaces_response = digitalocean.functions.list_namespaces()
```

#### 🔄 Return<a id="🔄-return"></a>

[`FunctionsListNamespacesResponse`](./digital_ocean_python_sdk/pydantic/functions_list_namespaces_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/functions/namespaces` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.functions.list_triggers`<a id="digitaloceanfunctionslist_triggers"></a>

Returns a list of triggers associated with the current user and namespace. To get all triggers, send a GET request to `/v2/functions/namespaces/$NAMESPACE_ID/triggers`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_triggers_response = digitalocean.functions.list_triggers(
    namespace_id="fn-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### namespace_id: `str`<a id="namespace_id-str"></a>

The ID of the namespace to be managed.

#### 🔄 Return<a id="🔄-return"></a>

[`FunctionsListTriggersResponse`](./digital_ocean_python_sdk/pydantic/functions_list_triggers_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/functions/namespaces/{namespace_id}/triggers` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.functions.update_trigger_details`<a id="digitaloceanfunctionsupdate_trigger_details"></a>

Updates the details of the given trigger. To update a trigger, send a PUT request to `/v2/functions/namespaces/$NAMESPACE_ID/triggers/$TRIGGER_NAME` with new values for the `is_enabled ` or `scheduled_details` properties.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_trigger_details_response = digitalocean.functions.update_trigger_details(
    namespace_id="fn-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    trigger_name="my trigger",
    is_enabled=True,
    scheduled_details={
        "cron": "* * * * *",
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### namespace_id: `str`<a id="namespace_id-str"></a>

The ID of the namespace to be managed.

##### trigger_name: `str`<a id="trigger_name-str"></a>

The name of the trigger to be managed.

##### is_enabled: `bool`<a id="is_enabled-bool"></a>

Indicates weather the trigger is paused or unpaused.

##### scheduled_details: [`ScheduledDetails`](./digital_ocean_python_sdk/type/scheduled_details.py)<a id="scheduled_details-scheduleddetailsdigital_ocean_python_sdktypescheduled_detailspy"></a>


#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`UpdateTrigger`](./digital_ocean_python_sdk/type/update_trigger.py)
#### 🔄 Return<a id="🔄-return"></a>

[`FunctionsCreateTriggerInNamespaceResponse`](./digital_ocean_python_sdk/pydantic/functions_create_trigger_in_namespace_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/functions/namespaces/{namespace_id}/triggers/{trigger_name}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.image_actions.get`<a id="digitaloceanimage_actionsget"></a>

To retrieve the status of an image action, send a GET request to `/v2/images/$IMAGE_ID/actions/$IMAGE_ACTION_ID`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_response = digitalocean.image_actions.get(
    image_id=62137902,
    action_id=36804636,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### image_id: `int`<a id="image_id-int"></a>

A unique number that can be used to identify and reference a specific image.

##### action_id: `int`<a id="action_id-int"></a>

A unique numeric ID that can be used to identify and reference an action.

#### 🔄 Return<a id="🔄-return"></a>

[`Action`](./digital_ocean_python_sdk/pydantic/action.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/images/{image_id}/actions/{action_id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.image_actions.list`<a id="digitaloceanimage_actionslist"></a>

To retrieve all actions that have been executed on an image, send a GET request to `/v2/images/$IMAGE_ID/actions`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = digitalocean.image_actions.list(
    image_id=62137902,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### image_id: `int`<a id="image_id-int"></a>

A unique number that can be used to identify and reference a specific image.

#### 🔄 Return<a id="🔄-return"></a>

[`ImageActionsListResponse`](./digital_ocean_python_sdk/pydantic/image_actions_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/images/{image_id}/actions` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.image_actions.post`<a id="digitaloceanimage_actionspost"></a>

The following actions are available on an Image.

## Convert an Image to a Snapshot<a id="convert-an-image-to-a-snapshot"></a>

To convert an image, for example, a backup to a snapshot, send a POST request
to `/v2/images/$IMAGE_ID/actions`. Set the `type` attribute to `convert`.

## Transfer an Image<a id="transfer-an-image"></a>

To transfer an image to another region, send a POST request to
`/v2/images/$IMAGE_ID/actions`. Set the `type` attribute to `transfer` and set
`region` attribute to the slug identifier of the region you wish to transfer
to.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
post_response = digitalocean.image_actions.post(
    body={
        "type": "convert",
    },
    image_id=62137902,
    type="convert",
    region="nyc3",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### image_id: `int`<a id="image_id-int"></a>

A unique number that can be used to identify and reference a specific image.

##### type: `str`<a id="type-str"></a>

The action to be taken on the image. Can be either `convert` or `transfer`.

##### region: [`RegionSlug`](./digital_ocean_python_sdk/type/region_slug.py)<a id="region-regionslugdigital_ocean_python_sdktyperegion_slugpy"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ImageActionsPostRequest`](./digital_ocean_python_sdk/type/image_actions_post_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`Action`](./digital_ocean_python_sdk/pydantic/action.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/images/{image_id}/actions` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.images.delete`<a id="digitaloceanimagesdelete"></a>

To delete a snapshot or custom image, send a `DELETE` request to `/v2/images/$IMAGE_ID`.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.images.delete(
    image_id=62137902,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### image_id: `int`<a id="image_id-int"></a>

A unique number that can be used to identify and reference a specific image.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/images/{image_id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.images.get`<a id="digitaloceanimagesget"></a>

To retrieve information about an image, send a `GET` request to
`/v2/images/$IDENTIFIER`.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_response = digitalocean.images.get(
    image_id=62137902,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### image_id: Union[`int`, `str`]<a id="image_id-unionint-str"></a>


A unique number (id) or string (slug) used to identify and reference a specific image.  **Public** images can be identified by image `id` or `slug`.  **Private** images *must* be identified by image `id`. 

#### 🔄 Return<a id="🔄-return"></a>

[`ImagesGetResponse`](./digital_ocean_python_sdk/pydantic/images_get_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/images/{image_id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.images.import_custom_image_from_url`<a id="digitaloceanimagesimport_custom_image_from_url"></a>

To create a new custom image, send a POST request to /v2/images.
The body must contain a url attribute pointing to a Linux virtual machine
image to be imported into DigitalOcean.
The image must be in the raw, qcow2, vhdx, vdi, or vmdk format.
It may be compressed using gzip or bzip2 and must be smaller than 100 GB after
 being decompressed.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
import_custom_image_from_url_response = digitalocean.images.import_custom_image_from_url(
    name="Nifty New Snapshot",
    url="http://cloud-images.ubuntu.com/minimal/releases/bionic/release/ubuntu-18.04-minimal-cloudimg-amd64.img",
    region="nyc3",
    description=" ",
    distribution="Ubuntu",
    tags=["base-image", "prod"],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### name: `str`<a id="name-str"></a>

The display name that has been given to an image.  This is what is shown in the control panel and is generally a descriptive title for the image in question.

##### url: `str`<a id="url-str"></a>

A URL from which the custom Linux virtual machine image may be retrieved.  The image it points to must be in the raw, qcow2, vhdx, vdi, or vmdk format.  It may be compressed using gzip or bzip2 and must be smaller than 100 GB after being decompressed.

##### region: [`RegionSlug`](./digital_ocean_python_sdk/type/region_slug.py)<a id="region-regionslugdigital_ocean_python_sdktyperegion_slugpy"></a>

##### description: `str`<a id="description-str"></a>

An optional free-form text field to describe an image.

##### distribution: [`Distribution`](./digital_ocean_python_sdk/type/distribution.py)<a id="distribution-distributiondigital_ocean_python_sdktypedistributionpy"></a>

##### tags: [`TagsArray`](./digital_ocean_python_sdk/type/tags_array.py)<a id="tags-tagsarraydigital_ocean_python_sdktypetags_arraypy"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ImageNewCustom`](./digital_ocean_python_sdk/type/image_new_custom.py)
#### 🔄 Return<a id="🔄-return"></a>

[`ImagesImportCustomImageFromUrlResponse`](./digital_ocean_python_sdk/pydantic/images_import_custom_image_from_url_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/images` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.images.list`<a id="digitaloceanimageslist"></a>

To list all of the images available on your account, send a GET request to /v2/images.

## Filtering Results<a id="filtering-results"></a>
-----

It's possible to request filtered results by including certain query parameters.

**Image Type**

Either 1-Click Application or OS Distribution images can be filtered by using the `type` query parameter.

> Important: The `type` query parameter does not directly relate to the `type` attribute.

To retrieve only ***distribution*** images, include the `type` query parameter set to distribution, `/v2/images?type=distribution`.

To retrieve only ***application*** images, include the `type` query parameter set to application, `/v2/images?type=application`.

**User Images**

To retrieve only the private images of a user, include the `private` query parameter set to true, `/v2/images?private=true`.

**Tags**

To list all images assigned to a specific tag, include the `tag_name` query parameter set to the name of the tag in your GET request. For example, `/v2/images?tag_name=$TAG_NAME`.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = digitalocean.images.list(
    type="distribution",
    private=True,
    tag_name="base-image",
    per_page=2,
    page=1,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### type: `str`<a id="type-str"></a>

Filters results based on image type which can be either `application` or `distribution`.

##### private: `bool`<a id="private-bool"></a>

Used to filter only user images.

##### tag_name: `str`<a id="tag_name-str"></a>

Used to filter images by a specific tag.

##### per_page: `int`<a id="per_page-int"></a>

Number of items returned per page

##### page: `int`<a id="page-int"></a>

Which 'page' of paginated results to return.

#### 🔄 Return<a id="🔄-return"></a>

[`ImagesListResponse`](./digital_ocean_python_sdk/pydantic/images_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/images` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.images.update`<a id="digitaloceanimagesupdate"></a>

To update an image, send a `PUT` request to `/v2/images/$IMAGE_ID`.
Set the `name` attribute to the new value you would like to use.
For custom images, the `description` and `distribution` attributes may also be updated.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_response = digitalocean.images.update(
    image_id=62137902,
    description=" ",
    name="Nifty New Snapshot",
    distribution="Ubuntu",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### image_id: `int`<a id="image_id-int"></a>

A unique number that can be used to identify and reference a specific image.

##### description: `str`<a id="description-str"></a>

An optional free-form text field to describe an image.

##### name: `str`<a id="name-str"></a>

The display name that has been given to an image.  This is what is shown in the control panel and is generally a descriptive title for the image in question.

##### distribution: [`Distribution`](./digital_ocean_python_sdk/type/distribution.py)<a id="distribution-distributiondigital_ocean_python_sdktypedistributionpy"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ImageUpdate`](./digital_ocean_python_sdk/type/image_update.py)
#### 🔄 Return<a id="🔄-return"></a>

[`ImagesUpdateResponse`](./digital_ocean_python_sdk/pydantic/images_update_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/images/{image_id}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.kubernetes.add_container_registry_to_clusters`<a id="digitaloceankubernetesadd_container_registry_to_clusters"></a>

To integrate the container registry with Kubernetes clusters, send a POST request to `/v2/kubernetes/registry`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.kubernetes.add_container_registry_to_clusters(
    cluster_uuids=["bd5f5959-5e1e-4205-a714-a914373942af", "50c2f44c-011d-493e-aee5-361a4a0d1844"],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### cluster_uuids: [`ClusterRegistriesClusterUuids`](./digital_ocean_python_sdk/type/cluster_registries_cluster_uuids.py)<a id="cluster_uuids-clusterregistriesclusteruuidsdigital_ocean_python_sdktypecluster_registries_cluster_uuidspy"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ClusterRegistries`](./digital_ocean_python_sdk/type/cluster_registries.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/kubernetes/registry` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.kubernetes.add_node_pool`<a id="digitaloceankubernetesadd_node_pool"></a>

To add an additional node pool to a Kubernetes clusters, send a POST request
to `/v2/kubernetes/clusters/$K8S_CLUSTER_ID/node_pools` with the following
attributes.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
add_node_pool_response = digitalocean.kubernetes.add_node_pool(
    size="s-1vcpu-2gb",
    name="frontend-pool",
    count=3,
    cluster_id="bd5f5959-5e1e-4205-a714-a914373942af",
    tags=["k8s", "k8s:bd5f5959-5e1e-4205-a714-a914373942af", "k8s-worker", "production", "web-team"],
    id="cdda885e-7663-40c8-bc74-3a036c66545d",
    labels={},
    taints=[
        {
            "key": "priority",
            "value": "high",
            "effect": "NoSchedule",
        }
    ],
    auto_scale=True,
    min_nodes=3,
    max_nodes=6,
    nodes=[
        {
            "id": "e78247f8-b1bb-4f7a-8db9-2a5f8d4b8f8f",
            "name": "adoring-newton-3niq",
            "droplet_id": "205545370",
            "created_at": "2018-11-15T16:00:11Z",
            "updated_at": "2018-11-15T16:00:11Z",
        }
    ],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### size: `str`<a id="size-str"></a>

The slug identifier for the type of Droplet used as workers in the node pool.

##### name: `str`<a id="name-str"></a>

A human-readable name for the node pool.

##### count: `int`<a id="count-int"></a>

The number of Droplet instances in the node pool.

##### cluster_id: `str`<a id="cluster_id-str"></a>

A unique ID that can be used to reference a Kubernetes cluster.

##### tags: [`KubernetesNodePoolBaseTags`](./digital_ocean_python_sdk/type/kubernetes_node_pool_base_tags.py)<a id="tags-kubernetesnodepoolbasetagsdigital_ocean_python_sdktypekubernetes_node_pool_base_tagspy"></a>

##### id: `str`<a id="id-str"></a>

A unique ID that can be used to identify and reference a specific node pool.

##### labels: `Optional[Dict[str, Union[bool, date, datetime, dict, float, int, list, str, None]]]`<a id="labels-optionaldictstr-unionbool-date-datetime-dict-float-int-list-str-none"></a>

An object of key/value mappings specifying labels to apply to all nodes in a pool. Labels will automatically be applied to all existing nodes and any subsequent nodes added to the pool. Note that when a label is removed, it is not deleted from the nodes in the pool.

##### taints: List[`KubernetesNodePoolTaint`]<a id="taints-listkubernetesnodepooltaint"></a>

An array of taints to apply to all nodes in a pool. Taints will automatically be applied to all existing nodes and any subsequent nodes added to the pool. When a taint is removed, it is deleted from all nodes in the pool.

##### auto_scale: `bool`<a id="auto_scale-bool"></a>

A boolean value indicating whether auto-scaling is enabled for this node pool.

##### min_nodes: `int`<a id="min_nodes-int"></a>

The minimum number of nodes that this node pool can be auto-scaled to. The value will be `0` if `auto_scale` is set to `false`.

##### max_nodes: `int`<a id="max_nodes-int"></a>

The maximum number of nodes that this node pool can be auto-scaled to. The value will be `0` if `auto_scale` is set to `false`.

##### nodes: List[`Node`]<a id="nodes-listnode"></a>

An object specifying the details of a specific worker node in a node pool.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`KubernetesNodePool`](./digital_ocean_python_sdk/type/kubernetes_node_pool.py)
#### 🔄 Return<a id="🔄-return"></a>

[`KubernetesAddNodePoolResponse`](./digital_ocean_python_sdk/pydantic/kubernetes_add_node_pool_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/kubernetes/clusters/{cluster_id}/node_pools` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.kubernetes.create_new_cluster`<a id="digitaloceankubernetescreate_new_cluster"></a>

To create a new Kubernetes cluster, send a POST request to
`/v2/kubernetes/clusters`. The request must contain at least one node pool
with at least one worker.

The request may contain a maintenance window policy describing a time period
when disruptive maintenance tasks may be carried out. Omitting the policy
implies that a window will be chosen automatically. See
[here](https://www.digitalocean.com/docs/kubernetes/how-to/upgrade-cluster/)
for details.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_new_cluster_response = digitalocean.kubernetes.create_new_cluster(
    version="1.18.6-do.0",
    name="prod-cluster-01",
    region="nyc1",
    node_pools=[
        {}
    ],
    tags=["k8s", "k8s:bd5f5959-5e1e-4205-a714-a914373942af", "production", "web-team"],
    id="bd5f5959-5e1e-4205-a714-a914373942af",
    cluster_subnet="10.244.0.0/16",
    service_subnet="10.245.0.0/16",
    vpc_uuid="c33931f2-a26a-4e61-b85c-4e95a2ec431b",
    ipv4="68.183.121.157",
    endpoint="https://bd5f5959-5e1e-4205-a714-a914373942af.k8s.ondigitalocean.com",
    maintenance_policy={
        "start_time": "720",
        "duration": "4h0m0s",
        "day": "any",
    },
    auto_upgrade=True,
    status={
        "state": "provisioning",
        "message": "provisioning",
    },
    created_at="2018-11-15T16:00:11Z",
    updated_at="2018-11-15T16:00:11Z",
    surge_upgrade=True,
    ha=True,
    registry_enabled=True,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### version: `str`<a id="version-str"></a>

The slug identifier for the version of Kubernetes used for the cluster. If set to a minor version (e.g. \\\"1.14\\\"), the latest version within it will be used (e.g. \\\"1.14.6-do.1\\\"); if set to \\\"latest\\\", the latest published version will be used. See the `/v2/kubernetes/options` endpoint to find all currently available versions.

##### name: `str`<a id="name-str"></a>

A human-readable name for a Kubernetes cluster.

##### region: `str`<a id="region-str"></a>

The slug identifier for the region where the Kubernetes cluster is located.

##### node_pools: List[`KubernetesNodePool`]<a id="node_pools-listkubernetesnodepool"></a>

An object specifying the details of the worker nodes available to the Kubernetes cluster.

##### tags: [`ClusterTags`](./digital_ocean_python_sdk/type/cluster_tags.py)<a id="tags-clustertagsdigital_ocean_python_sdktypecluster_tagspy"></a>

##### id: `str`<a id="id-str"></a>

A unique ID that can be used to identify and reference a Kubernetes cluster.

##### cluster_subnet: `str`<a id="cluster_subnet-str"></a>

The range of IP addresses in the overlay network of the Kubernetes cluster in CIDR notation.

##### service_subnet: `str`<a id="service_subnet-str"></a>

The range of assignable IP addresses for services running in the Kubernetes cluster in CIDR notation.

##### vpc_uuid: `str`<a id="vpc_uuid-str"></a>

A string specifying the UUID of the VPC to which the Kubernetes cluster is assigned.

##### ipv4: `str`<a id="ipv4-str"></a>

The public IPv4 address of the Kubernetes master node. This will not be set if high availability is configured on the cluster (v1.21+)

##### endpoint: `str`<a id="endpoint-str"></a>

The base URL of the API server on the Kubernetes master node.

##### maintenance_policy: [`MaintenancePolicy`](./digital_ocean_python_sdk/type/maintenance_policy.py)<a id="maintenance_policy-maintenancepolicydigital_ocean_python_sdktypemaintenance_policypy"></a>


##### auto_upgrade: `bool`<a id="auto_upgrade-bool"></a>

A boolean value indicating whether the cluster will be automatically upgraded to new patch releases during its maintenance window.

##### status: [`ClusterStatus`](./digital_ocean_python_sdk/type/cluster_status.py)<a id="status-clusterstatusdigital_ocean_python_sdktypecluster_statuspy"></a>


##### created_at: `datetime`<a id="created_at-datetime"></a>

A time value given in ISO8601 combined date and time format that represents when the Kubernetes cluster was created.

##### updated_at: `datetime`<a id="updated_at-datetime"></a>

A time value given in ISO8601 combined date and time format that represents when the Kubernetes cluster was last updated.

##### surge_upgrade: `bool`<a id="surge_upgrade-bool"></a>

A boolean value indicating whether surge upgrade is enabled/disabled for the cluster. Surge upgrade makes cluster upgrades fast and reliable by bringing up new nodes before destroying the outdated nodes.

##### ha: `bool`<a id="ha-bool"></a>

A boolean value indicating whether the control plane is run in a highly available configuration in the cluster. Highly available control planes incur less downtime. The property cannot be disabled.

##### registry_enabled: `bool`<a id="registry_enabled-bool"></a>

A read-only boolean value indicating if a container registry is integrated with the cluster.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`Cluster`](./digital_ocean_python_sdk/type/cluster.py)
#### 🔄 Return<a id="🔄-return"></a>

[`KubernetesCreateNewClusterResponse`](./digital_ocean_python_sdk/pydantic/kubernetes_create_new_cluster_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/kubernetes/clusters` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.kubernetes.delete_cluster`<a id="digitaloceankubernetesdelete_cluster"></a>

To delete a Kubernetes cluster and all services deployed to it, send a DELETE
request to `/v2/kubernetes/clusters/$K8S_CLUSTER_ID`.

A 204 status code with no body will be returned in response to a successful
request.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.kubernetes.delete_cluster(
    cluster_id="bd5f5959-5e1e-4205-a714-a914373942af",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### cluster_id: `str`<a id="cluster_id-str"></a>

A unique ID that can be used to reference a Kubernetes cluster.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/kubernetes/clusters/{cluster_id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.kubernetes.delete_cluster_associated_resources_dangerous`<a id="digitaloceankubernetesdelete_cluster_associated_resources_dangerous"></a>

To delete a Kubernetes cluster with all of its associated resources, send a
DELETE request to `/v2/kubernetes/clusters/$K8S_CLUSTER_ID/destroy_with_associated_resources/dangerous`.
A 204 status code with no body will be returned in response to a successful request.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.kubernetes.delete_cluster_associated_resources_dangerous(
    cluster_id="bd5f5959-5e1e-4205-a714-a914373942af",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### cluster_id: `str`<a id="cluster_id-str"></a>

A unique ID that can be used to reference a Kubernetes cluster.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/kubernetes/clusters/{cluster_id}/destroy_with_associated_resources/dangerous` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.kubernetes.delete_node_in_node_pool`<a id="digitaloceankubernetesdelete_node_in_node_pool"></a>

To delete a single node in a pool, send a DELETE request to
`/v2/kubernetes/clusters/$K8S_CLUSTER_ID/node_pools/$NODE_POOL_ID/nodes/$NODE_ID`.

Appending the `skip_drain=1` query parameter to the request causes node
draining to be skipped. Omitting the query parameter or setting its value to
`0` carries out draining prior to deletion.

Appending the `replace=1` query parameter to the request causes the node to
be replaced by a new one after deletion. Omitting the query parameter or
setting its value to `0` deletes without replacement.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.kubernetes.delete_node_in_node_pool(
    cluster_id="bd5f5959-5e1e-4205-a714-a914373942af",
    node_pool_id="cdda885e-7663-40c8-bc74-3a036c66545d",
    node_id="478247f8-b1bb-4f7a-8db9-2a5f8d4b8f8f",
    skip_drain=1,
    replace=1,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### cluster_id: `str`<a id="cluster_id-str"></a>

A unique ID that can be used to reference a Kubernetes cluster.

##### node_pool_id: `str`<a id="node_pool_id-str"></a>

A unique ID that can be used to reference a Kubernetes node pool.

##### node_id: `str`<a id="node_id-str"></a>

A unique ID that can be used to reference a node in a Kubernetes node pool.

##### skip_drain: `int`<a id="skip_drain-int"></a>

Specifies whether or not to drain workloads from a node before it is deleted. Setting it to `1` causes node draining to be skipped. Omitting the query parameter or setting its value to `0` carries out draining prior to deletion.

##### replace: `int`<a id="replace-int"></a>

Specifies whether or not to replace a node after it has been deleted. Setting it to `1` causes the node to be replaced by a new one after deletion. Omitting the query parameter or setting its value to `0` deletes without replacement.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/kubernetes/clusters/{cluster_id}/node_pools/{node_pool_id}/nodes/{node_id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.kubernetes.delete_node_pool`<a id="digitaloceankubernetesdelete_node_pool"></a>

To delete a node pool, send a DELETE request to
`/v2/kubernetes/clusters/$K8S_CLUSTER_ID/node_pools/$NODE_POOL_ID`.

A 204 status code with no body will be returned in response to a successful
request. Nodes in the pool will subsequently be drained and deleted.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.kubernetes.delete_node_pool(
    cluster_id="bd5f5959-5e1e-4205-a714-a914373942af",
    node_pool_id="cdda885e-7663-40c8-bc74-3a036c66545d",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### cluster_id: `str`<a id="cluster_id-str"></a>

A unique ID that can be used to reference a Kubernetes cluster.

##### node_pool_id: `str`<a id="node_pool_id-str"></a>

A unique ID that can be used to reference a Kubernetes node pool.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/kubernetes/clusters/{cluster_id}/node_pools/{node_pool_id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.kubernetes.get_available_upgrades`<a id="digitaloceankubernetesget_available_upgrades"></a>

To determine whether a cluster can be upgraded, and the versions to which it
can be upgraded, send a GET request to
`/v2/kubernetes/clusters/$K8S_CLUSTER_ID/upgrades`.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_available_upgrades_response = digitalocean.kubernetes.get_available_upgrades(
    cluster_id="bd5f5959-5e1e-4205-a714-a914373942af",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### cluster_id: `str`<a id="cluster_id-str"></a>

A unique ID that can be used to reference a Kubernetes cluster.

#### 🔄 Return<a id="🔄-return"></a>

[`KubernetesGetAvailableUpgradesResponse`](./digital_ocean_python_sdk/pydantic/kubernetes_get_available_upgrades_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/kubernetes/clusters/{cluster_id}/upgrades` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.kubernetes.get_cluster_info`<a id="digitaloceankubernetesget_cluster_info"></a>

To show information about an existing Kubernetes cluster, send a GET request
to `/v2/kubernetes/clusters/$K8S_CLUSTER_ID`.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_cluster_info_response = digitalocean.kubernetes.get_cluster_info(
    cluster_id="bd5f5959-5e1e-4205-a714-a914373942af",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### cluster_id: `str`<a id="cluster_id-str"></a>

A unique ID that can be used to reference a Kubernetes cluster.

#### 🔄 Return<a id="🔄-return"></a>

[`KubernetesGetClusterInfoResponse`](./digital_ocean_python_sdk/pydantic/kubernetes_get_cluster_info_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/kubernetes/clusters/{cluster_id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.kubernetes.get_cluster_lint_diagnostics`<a id="digitaloceankubernetesget_cluster_lint_diagnostics"></a>

To request clusterlint diagnostics for your cluster, send a GET request to
`/v2/kubernetes/clusters/$K8S_CLUSTER_ID/clusterlint`. If the `run_id` query
parameter is provided, then the diagnostics for the specific run is fetched.
By default, the latest results are shown.

To find out how to address clusterlint feedback, please refer to
[the clusterlint check documentation](https://github.com/digitalocean/clusterlint/blob/master/checks.md).


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_cluster_lint_diagnostics_response = digitalocean.kubernetes.get_cluster_lint_diagnostics(
    cluster_id="bd5f5959-5e1e-4205-a714-a914373942af",
    run_id="50c2f44c-011d-493e-aee5-361a4a0d1844",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### cluster_id: `str`<a id="cluster_id-str"></a>

A unique ID that can be used to reference a Kubernetes cluster.

##### run_id: `str`<a id="run_id-str"></a>

Specifies the clusterlint run whose results will be retrieved.

#### 🔄 Return<a id="🔄-return"></a>

[`ClusterlintResults`](./digital_ocean_python_sdk/pydantic/clusterlint_results.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/kubernetes/clusters/{cluster_id}/clusterlint` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.kubernetes.get_credentials_by_cluster_id`<a id="digitaloceankubernetesget_credentials_by_cluster_id"></a>

This endpoint returns a JSON object . It can be used to programmatically
construct Kubernetes clients which cannot parse kubeconfig files.

The resulting JSON object contains token-based authentication for clusters
supporting it, and certificate-based authentication otherwise. For a list of
supported versions and more information, see "[How to Connect to a DigitalOcean
Kubernetes Cluster with kubectl](https://www.digitalocean.com/docs/kubernetes/how-to/connect-with-kubectl/)".

To retrieve credentials for accessing a Kubernetes cluster, send a GET
request to `/v2/kubernetes/clusters/$K8S_CLUSTER_ID/credentials`.

Clusters supporting token-based authentication may define an expiration by
passing a duration in seconds as a query parameter to
`/v2/kubernetes/clusters/$K8S_CLUSTER_ID/credentials?expiry_seconds=$DURATION_IN_SECONDS`.
If not set or 0, then the token will have a 7 day expiry. The query parameter
has no impact in certificate-based authentication.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_credentials_by_cluster_id_response = digitalocean.kubernetes.get_credentials_by_cluster_id(
    cluster_id="bd5f5959-5e1e-4205-a714-a914373942af",
    expiry_seconds=300,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### cluster_id: `str`<a id="cluster_id-str"></a>

A unique ID that can be used to reference a Kubernetes cluster.

##### expiry_seconds: `int`<a id="expiry_seconds-int"></a>

The duration in seconds that the returned Kubernetes credentials will be valid. If not set or 0, the credentials will have a 7 day expiry.

#### 🔄 Return<a id="🔄-return"></a>

[`Credentials`](./digital_ocean_python_sdk/pydantic/credentials.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/kubernetes/clusters/{cluster_id}/credentials` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.kubernetes.get_kubeconfig`<a id="digitaloceankubernetesget_kubeconfig"></a>

This endpoint returns a kubeconfig file in YAML format. It can be used to
connect to and administer the cluster using the Kubernetes command line tool,
`kubectl`, or other programs supporting kubeconfig files (e.g., client libraries).

The resulting kubeconfig file uses token-based authentication for clusters
supporting it, and certificate-based authentication otherwise. For a list of
supported versions and more information, see "[How to Connect to a DigitalOcean
Kubernetes Cluster with kubectl](https://www.digitalocean.com/docs/kubernetes/how-to/connect-with-kubectl/)".

To retrieve a kubeconfig file for use with a Kubernetes cluster, send a GET
request to `/v2/kubernetes/clusters/$K8S_CLUSTER_ID/kubeconfig`.

Clusters supporting token-based authentication may define an expiration by
passing a duration in seconds as a query parameter to
`/v2/kubernetes/clusters/$K8S_CLUSTER_ID/kubeconfig?expiry_seconds=$DURATION_IN_SECONDS`.
If not set or 0, then the token will have a 7 day expiry. The query parameter
has no impact in certificate-based authentication.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.kubernetes.get_kubeconfig(
    cluster_id="bd5f5959-5e1e-4205-a714-a914373942af",
    expiry_seconds=300,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### cluster_id: `str`<a id="cluster_id-str"></a>

A unique ID that can be used to reference a Kubernetes cluster.

##### expiry_seconds: `int`<a id="expiry_seconds-int"></a>

The duration in seconds that the returned Kubernetes credentials will be valid. If not set or 0, the credentials will have a 7 day expiry.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/kubernetes/clusters/{cluster_id}/kubeconfig` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.kubernetes.get_node_pool`<a id="digitaloceankubernetesget_node_pool"></a>

To show information about a specific node pool in a Kubernetes cluster, send
a GET request to `/v2/kubernetes/clusters/$K8S_CLUSTER_ID/node_pools/$NODE_POOL_ID`.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_node_pool_response = digitalocean.kubernetes.get_node_pool(
    cluster_id="bd5f5959-5e1e-4205-a714-a914373942af",
    node_pool_id="cdda885e-7663-40c8-bc74-3a036c66545d",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### cluster_id: `str`<a id="cluster_id-str"></a>

A unique ID that can be used to reference a Kubernetes cluster.

##### node_pool_id: `str`<a id="node_pool_id-str"></a>

A unique ID that can be used to reference a Kubernetes node pool.

#### 🔄 Return<a id="🔄-return"></a>

[`KubernetesGetNodePoolResponse`](./digital_ocean_python_sdk/pydantic/kubernetes_get_node_pool_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/kubernetes/clusters/{cluster_id}/node_pools/{node_pool_id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.kubernetes.get_user_information`<a id="digitaloceankubernetesget_user_information"></a>

To show information the user associated with a Kubernetes cluster, send a GET
request to `/v2/kubernetes/clusters/$K8S_CLUSTER_ID/user`.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_user_information_response = digitalocean.kubernetes.get_user_information(
    cluster_id="bd5f5959-5e1e-4205-a714-a914373942af",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### cluster_id: `str`<a id="cluster_id-str"></a>

A unique ID that can be used to reference a Kubernetes cluster.

#### 🔄 Return<a id="🔄-return"></a>

[`User`](./digital_ocean_python_sdk/pydantic/user.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/kubernetes/clusters/{cluster_id}/user` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.kubernetes.list_associated_resources`<a id="digitaloceankuberneteslist_associated_resources"></a>

To list the associated billable resources that can be destroyed along with a cluster, send a GET request to the `/v2/kubernetes/clusters/$K8S_CLUSTER_ID/destroy_with_associated_resources` endpoint.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_associated_resources_response = digitalocean.kubernetes.list_associated_resources(
    cluster_id="bd5f5959-5e1e-4205-a714-a914373942af",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### cluster_id: `str`<a id="cluster_id-str"></a>

A unique ID that can be used to reference a Kubernetes cluster.

#### 🔄 Return<a id="🔄-return"></a>

[`AssociatedKubernetesResources`](./digital_ocean_python_sdk/pydantic/associated_kubernetes_resources.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/kubernetes/clusters/{cluster_id}/destroy_with_associated_resources` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.kubernetes.list_clusters`<a id="digitaloceankuberneteslist_clusters"></a>

To list all of the Kubernetes clusters on your account, send a GET request
to `/v2/kubernetes/clusters`.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_clusters_response = digitalocean.kubernetes.list_clusters(
    per_page=2,
    page=1,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### per_page: `int`<a id="per_page-int"></a>

Number of items returned per page

##### page: `int`<a id="page-int"></a>

Which 'page' of paginated results to return.

#### 🔄 Return<a id="🔄-return"></a>

[`KubernetesListClustersResponse`](./digital_ocean_python_sdk/pydantic/kubernetes_list_clusters_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/kubernetes/clusters` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.kubernetes.list_node_pools`<a id="digitaloceankuberneteslist_node_pools"></a>

To list all of the node pools in a Kubernetes clusters, send a GET request to
`/v2/kubernetes/clusters/$K8S_CLUSTER_ID/node_pools`.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_node_pools_response = digitalocean.kubernetes.list_node_pools(
    cluster_id="bd5f5959-5e1e-4205-a714-a914373942af",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### cluster_id: `str`<a id="cluster_id-str"></a>

A unique ID that can be used to reference a Kubernetes cluster.

#### 🔄 Return<a id="🔄-return"></a>

[`KubernetesListNodePoolsResponse`](./digital_ocean_python_sdk/pydantic/kubernetes_list_node_pools_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/kubernetes/clusters/{cluster_id}/node_pools` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.kubernetes.list_options`<a id="digitaloceankuberneteslist_options"></a>

To list the versions of Kubernetes available for use, the regions that support Kubernetes, and the available node sizes, send a GET request to `/v2/kubernetes/options`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_options_response = digitalocean.kubernetes.list_options()
```

#### 🔄 Return<a id="🔄-return"></a>

[`KubernetesOptions`](./digital_ocean_python_sdk/pydantic/kubernetes_options.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/kubernetes/options` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.kubernetes.recycle_node_pool`<a id="digitaloceankubernetesrecycle_node_pool"></a>

The endpoint has been deprecated. Please use the DELETE
`/v2/kubernetes/clusters/$K8S_CLUSTER_ID/node_pools/$NODE_POOL_ID/nodes/$NODE_ID`
method instead.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.kubernetes.recycle_node_pool(
    body=None,
    cluster_id="bd5f5959-5e1e-4205-a714-a914373942af",
    node_pool_id="cdda885e-7663-40c8-bc74-3a036c66545d",
    nodes=["d8db5e1a-6103-43b5-a7b3-8a948210a9fc"],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### cluster_id: `str`<a id="cluster_id-str"></a>

A unique ID that can be used to reference a Kubernetes cluster.

##### node_pool_id: `str`<a id="node_pool_id-str"></a>

A unique ID that can be used to reference a Kubernetes node pool.

##### nodes: List[`str`]<a id="nodes-liststr"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`KubernetesRecycleNodePoolRequest`](./digital_ocean_python_sdk/type/kubernetes_recycle_node_pool_request.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/kubernetes/clusters/{cluster_id}/node_pools/{node_pool_id}/recycle` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.kubernetes.remove_registry`<a id="digitaloceankubernetesremove_registry"></a>

To remove the container registry from Kubernetes clusters, send a DELETE request to `/v2/kubernetes/registry`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.kubernetes.remove_registry(
    cluster_uuids=["bd5f5959-5e1e-4205-a714-a914373942af", "50c2f44c-011d-493e-aee5-361a4a0d1844"],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### cluster_uuids: [`ClusterRegistriesClusterUuids`](./digital_ocean_python_sdk/type/cluster_registries_cluster_uuids.py)<a id="cluster_uuids-clusterregistriesclusteruuidsdigital_ocean_python_sdktypecluster_registries_cluster_uuidspy"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ClusterRegistries`](./digital_ocean_python_sdk/type/cluster_registries.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/kubernetes/registry` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.kubernetes.run_clusterlint_checks`<a id="digitaloceankubernetesrun_clusterlint_checks"></a>

Clusterlint helps operators conform to Kubernetes best practices around
resources, security and reliability to avoid common problems while operating
or upgrading the clusters.

To request a clusterlint run on your cluster, send a POST request to
`/v2/kubernetes/clusters/$K8S_CLUSTER_ID/clusterlint`. This will run all
checks present in the `doks` group by default, if a request body is not
specified. Optionally specify the below attributes.

For information about the available checks, please refer to
[the clusterlint check documentation](https://github.com/digitalocean/clusterlint/blob/master/checks.md).


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
run_clusterlint_checks_response = digitalocean.kubernetes.run_clusterlint_checks(
    cluster_id="bd5f5959-5e1e-4205-a714-a914373942af",
    include_groups=["basic", "doks", "security"],
    include_checks=["bare-pods", "resource-requirements"],
    exclude_groups=["workload-health"],
    exclude_checks=["default-namespace"],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### cluster_id: `str`<a id="cluster_id-str"></a>

A unique ID that can be used to reference a Kubernetes cluster.

##### include_groups: [`ClusterlintRequestIncludeGroups`](./digital_ocean_python_sdk/type/clusterlint_request_include_groups.py)<a id="include_groups-clusterlintrequestincludegroupsdigital_ocean_python_sdktypeclusterlint_request_include_groupspy"></a>

##### include_checks: [`ClusterlintRequestIncludeChecks`](./digital_ocean_python_sdk/type/clusterlint_request_include_checks.py)<a id="include_checks-clusterlintrequestincludechecksdigital_ocean_python_sdktypeclusterlint_request_include_checkspy"></a>

##### exclude_groups: [`ClusterlintRequestExcludeGroups`](./digital_ocean_python_sdk/type/clusterlint_request_exclude_groups.py)<a id="exclude_groups-clusterlintrequestexcludegroupsdigital_ocean_python_sdktypeclusterlint_request_exclude_groupspy"></a>

##### exclude_checks: [`ClusterlintRequestExcludeChecks`](./digital_ocean_python_sdk/type/clusterlint_request_exclude_checks.py)<a id="exclude_checks-clusterlintrequestexcludechecksdigital_ocean_python_sdktypeclusterlint_request_exclude_checkspy"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ClusterlintRequest`](./digital_ocean_python_sdk/type/clusterlint_request.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/kubernetes/clusters/{cluster_id}/clusterlint` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.kubernetes.selective_cluster_destroy`<a id="digitaloceankubernetesselective_cluster_destroy"></a>

To delete a Kubernetes cluster along with a subset of its associated resources,
send a DELETE request to `/v2/kubernetes/clusters/$K8S_CLUSTER_ID/destroy_with_associated_resources/selective`.

The JSON body of the request should include `load_balancers`, `volumes`, or
`volume_snapshots` keys each set to an array of IDs for the associated
resources to be destroyed.

The IDs can be found by querying the cluster's associated resources endpoint.
Any associated resource not included in the request will remain and continue
to accrue changes on your account.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.kubernetes.selective_cluster_destroy(
    cluster_id="bd5f5959-5e1e-4205-a714-a914373942af",
    load_balancers=["4de7ac8b-495b-4884-9a69-1050c6793cd6"],
    volumes=["ba49449a-7435-11ea-b89e-0a58ac14480f"],
    volume_snapshots=["edb0478d-7436-11ea-86e6-0a58ac144b91"],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### cluster_id: `str`<a id="cluster_id-str"></a>

A unique ID that can be used to reference a Kubernetes cluster.

##### load_balancers: [`DestroyAssociatedKubernetesResourcesLoadBalancers`](./digital_ocean_python_sdk/type/destroy_associated_kubernetes_resources_load_balancers.py)<a id="load_balancers-destroyassociatedkubernetesresourcesloadbalancersdigital_ocean_python_sdktypedestroy_associated_kubernetes_resources_load_balancerspy"></a>

##### volumes: [`DestroyAssociatedKubernetesResourcesVolumes`](./digital_ocean_python_sdk/type/destroy_associated_kubernetes_resources_volumes.py)<a id="volumes-destroyassociatedkubernetesresourcesvolumesdigital_ocean_python_sdktypedestroy_associated_kubernetes_resources_volumespy"></a>

##### volume_snapshots: [`DestroyAssociatedKubernetesResourcesVolumeSnapshots`](./digital_ocean_python_sdk/type/destroy_associated_kubernetes_resources_volume_snapshots.py)<a id="volume_snapshots-destroyassociatedkubernetesresourcesvolumesnapshotsdigital_ocean_python_sdktypedestroy_associated_kubernetes_resources_volume_snapshotspy"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`DestroyAssociatedKubernetesResources`](./digital_ocean_python_sdk/type/destroy_associated_kubernetes_resources.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/kubernetes/clusters/{cluster_id}/destroy_with_associated_resources/selective` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.kubernetes.update_cluster`<a id="digitaloceankubernetesupdate_cluster"></a>

To update a Kubernetes cluster, send a PUT request to
`/v2/kubernetes/clusters/$K8S_CLUSTER_ID` and specify one or more of the
attributes below.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_cluster_response = digitalocean.kubernetes.update_cluster(
    name="prod-cluster-01",
    cluster_id="bd5f5959-5e1e-4205-a714-a914373942af",
    tags=["k8s", "k8s:bd5f5959-5e1e-4205-a714-a914373942af", "production", "web-team"],
    maintenance_policy={
        "start_time": "720",
        "duration": "4h0m0s",
        "day": "any",
    },
    auto_upgrade=True,
    surge_upgrade=True,
    ha=True,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### name: `str`<a id="name-str"></a>

A human-readable name for a Kubernetes cluster.

##### cluster_id: `str`<a id="cluster_id-str"></a>

A unique ID that can be used to reference a Kubernetes cluster.

##### tags: [`ClusterUpdateTags`](./digital_ocean_python_sdk/type/cluster_update_tags.py)<a id="tags-clusterupdatetagsdigital_ocean_python_sdktypecluster_update_tagspy"></a>

##### maintenance_policy: [`MaintenancePolicy`](./digital_ocean_python_sdk/type/maintenance_policy.py)<a id="maintenance_policy-maintenancepolicydigital_ocean_python_sdktypemaintenance_policypy"></a>


##### auto_upgrade: `bool`<a id="auto_upgrade-bool"></a>

A boolean value indicating whether the cluster will be automatically upgraded to new patch releases during its maintenance window.

##### surge_upgrade: `bool`<a id="surge_upgrade-bool"></a>

A boolean value indicating whether surge upgrade is enabled/disabled for the cluster. Surge upgrade makes cluster upgrades fast and reliable by bringing up new nodes before destroying the outdated nodes.

##### ha: `bool`<a id="ha-bool"></a>

A boolean value indicating whether the control plane is run in a highly available configuration in the cluster. Highly available control planes incur less downtime. The property cannot be disabled.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ClusterUpdate`](./digital_ocean_python_sdk/type/cluster_update.py)
#### 🔄 Return<a id="🔄-return"></a>

[`KubernetesUpdateClusterResponse`](./digital_ocean_python_sdk/pydantic/kubernetes_update_cluster_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/kubernetes/clusters/{cluster_id}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.kubernetes.update_node_pool`<a id="digitaloceankubernetesupdate_node_pool"></a>

To update the name of a node pool, edit the tags applied to it, or adjust its
number of nodes, send a PUT request to
`/v2/kubernetes/clusters/$K8S_CLUSTER_ID/node_pools/$NODE_POOL_ID` with the
following attributes.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_node_pool_response = digitalocean.kubernetes.update_node_pool(
    cluster_id="bd5f5959-5e1e-4205-a714-a914373942af",
    node_pool_id="cdda885e-7663-40c8-bc74-3a036c66545d",
    tags=["k8s", "k8s:bd5f5959-5e1e-4205-a714-a914373942af", "k8s-worker", "production", "web-team"],
    id="cdda885e-7663-40c8-bc74-3a036c66545d",
    name="frontend-pool",
    count=3,
    labels={},
    taints=[
        {
            "key": "priority",
            "value": "high",
            "effect": "NoSchedule",
        }
    ],
    auto_scale=True,
    min_nodes=3,
    max_nodes=6,
    nodes=[
        {
            "id": "e78247f8-b1bb-4f7a-8db9-2a5f8d4b8f8f",
            "name": "adoring-newton-3niq",
            "droplet_id": "205545370",
            "created_at": "2018-11-15T16:00:11Z",
            "updated_at": "2018-11-15T16:00:11Z",
        }
    ],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### cluster_id: `str`<a id="cluster_id-str"></a>

A unique ID that can be used to reference a Kubernetes cluster.

##### node_pool_id: `str`<a id="node_pool_id-str"></a>

A unique ID that can be used to reference a Kubernetes node pool.

##### tags: [`KubernetesNodePoolBaseTags`](./digital_ocean_python_sdk/type/kubernetes_node_pool_base_tags.py)<a id="tags-kubernetesnodepoolbasetagsdigital_ocean_python_sdktypekubernetes_node_pool_base_tagspy"></a>

##### id: `str`<a id="id-str"></a>

A unique ID that can be used to identify and reference a specific node pool.

##### name: `str`<a id="name-str"></a>

A human-readable name for the node pool.

##### count: `int`<a id="count-int"></a>

The number of Droplet instances in the node pool.

##### labels: `Optional[Dict[str, Union[bool, date, datetime, dict, float, int, list, str, None]]]`<a id="labels-optionaldictstr-unionbool-date-datetime-dict-float-int-list-str-none"></a>

An object of key/value mappings specifying labels to apply to all nodes in a pool. Labels will automatically be applied to all existing nodes and any subsequent nodes added to the pool. Note that when a label is removed, it is not deleted from the nodes in the pool.

##### taints: List[`KubernetesNodePoolTaint`]<a id="taints-listkubernetesnodepooltaint"></a>

An array of taints to apply to all nodes in a pool. Taints will automatically be applied to all existing nodes and any subsequent nodes added to the pool. When a taint is removed, it is deleted from all nodes in the pool.

##### auto_scale: `bool`<a id="auto_scale-bool"></a>

A boolean value indicating whether auto-scaling is enabled for this node pool.

##### min_nodes: `int`<a id="min_nodes-int"></a>

The minimum number of nodes that this node pool can be auto-scaled to. The value will be `0` if `auto_scale` is set to `false`.

##### max_nodes: `int`<a id="max_nodes-int"></a>

The maximum number of nodes that this node pool can be auto-scaled to. The value will be `0` if `auto_scale` is set to `false`.

##### nodes: List[`Node`]<a id="nodes-listnode"></a>

An object specifying the details of a specific worker node in a node pool.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`KubernetesNodePoolBase`](./digital_ocean_python_sdk/type/kubernetes_node_pool_base.py)
#### 🔄 Return<a id="🔄-return"></a>

[`KubernetesUpdateNodePoolResponse`](./digital_ocean_python_sdk/pydantic/kubernetes_update_node_pool_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/kubernetes/clusters/{cluster_id}/node_pools/{node_pool_id}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.kubernetes.upgrade_cluster`<a id="digitaloceankubernetesupgrade_cluster"></a>

To immediately upgrade a Kubernetes cluster to a newer patch release of
Kubernetes, send a POST request to `/v2/kubernetes/clusters/$K8S_CLUSTER_ID/upgrade`.
The body of the request must specify a version attribute.

Available upgrade versions for a cluster can be fetched from
`/v2/kubernetes/clusters/$K8S_CLUSTER_ID/upgrades`.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.kubernetes.upgrade_cluster(
    body=None,
    cluster_id="bd5f5959-5e1e-4205-a714-a914373942af",
    version="1.16.13-do.0",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### cluster_id: `str`<a id="cluster_id-str"></a>

A unique ID that can be used to reference a Kubernetes cluster.

##### version: `str`<a id="version-str"></a>

The slug identifier for the version of Kubernetes that the cluster will be upgraded to.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`KubernetesUpgradeClusterRequest`](./digital_ocean_python_sdk/type/kubernetes_upgrade_cluster_request.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/kubernetes/clusters/{cluster_id}/upgrade` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.load_balancers.add_forwarding_rules`<a id="digitaloceanload_balancersadd_forwarding_rules"></a>

To add an additional forwarding rule to a load balancer instance, send a POST
request to `/v2/load_balancers/$LOAD_BALANCER_ID/forwarding_rules`. In the body
of the request, there should be a `forwarding_rules` attribute containing an
array of rules to be added.

No response body will be sent back, but the response code will indicate
success. Specifically, the response code will be a 204, which means that the
action was successful with no returned body data.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.load_balancers.add_forwarding_rules(
    body=None,
    forwarding_rules=[
        {
            "entry_protocol": "https",
            "entry_port": 443,
            "target_protocol": "http",
            "target_port": 80,
            "certificate_id": "892071a0-bb95-49bc-8021-3afd67a210bf",
            "tls_passthrough": False,
        }
    ],
    lb_id="4de7ac8b-495b-4884-9a69-1050c6793cd6",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### forwarding_rules: List[`ForwardingRule`]<a id="forwarding_rules-listforwardingrule"></a>

##### lb_id: `str`<a id="lb_id-str"></a>

A unique identifier for a load balancer.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`LoadBalancersAddForwardingRulesRequest`](./digital_ocean_python_sdk/type/load_balancers_add_forwarding_rules_request.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/load_balancers/{lb_id}/forwarding_rules` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.load_balancers.assign_droplets`<a id="digitaloceanload_balancersassign_droplets"></a>

To assign a Droplet to a load balancer instance, send a POST request to
`/v2/load_balancers/$LOAD_BALANCER_ID/droplets`. In the body of the request,
there should be a `droplet_ids` attribute containing a list of Droplet IDs.
Individual Droplets can not be added to a load balancer configured with a
Droplet tag. Attempting to do so will result in a "422 Unprocessable Entity"
response from the API.

No response body will be sent back, but the response code will indicate
success. Specifically, the response code will be a 204, which means that the
action was successful with no returned body data.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.load_balancers.assign_droplets(
    body=None,
    droplet_ids=[3164444, 3164445],
    lb_id="4de7ac8b-495b-4884-9a69-1050c6793cd6",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### droplet_ids: List[`int`]<a id="droplet_ids-listint"></a>

An array containing the IDs of the Droplets assigned to the load balancer.

##### lb_id: `str`<a id="lb_id-str"></a>

A unique identifier for a load balancer.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`LoadBalancersAssignDropletsRequest`](./digital_ocean_python_sdk/type/load_balancers_assign_droplets_request.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/load_balancers/{lb_id}/droplets` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.load_balancers.create`<a id="digitaloceanload_balancerscreate"></a>

To create a new load balancer instance, send a POST request to
`/v2/load_balancers`.

You can specify the Droplets that will sit behind the load balancer using one
of two methods:

* Set `droplet_ids` to a list of specific Droplet IDs.
* Set `tag` to the name of a tag. All Droplets with this tag applied will be
  assigned to the load balancer. Additional Droplets will be automatically
  assigned as they are tagged.

These methods are mutually exclusive.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_response = digitalocean.load_balancers.create(
    body=None,
    droplet_ids=[3164444, 3164445],
    region="nyc3",
    id="4de7ac8b-495b-4884-9a69-1050c6793cd6",
    name="example-lb-01",
    project_id="4de7ac8b-495b-4884-9a69-1050c6793cd6",
    ip="104.131.186.241",
    size_unit=3,
    size="lb-small",
    algorithm="round_robin",
    status="new",
    created_at="2017-02-01T22:22:58Z",
    forwarding_rules=[
        {
            "entry_protocol": "https",
            "entry_port": 443,
            "target_protocol": "http",
            "target_port": 80,
            "certificate_id": "892071a0-bb95-49bc-8021-3afd67a210bf",
            "tls_passthrough": False,
        }
    ],
    health_check={
        "protocol": "http",
        "port": 80,
        "path": "/",
        "check_interval_seconds": 10,
        "response_timeout_seconds": 5,
        "unhealthy_threshold": 5,
        "healthy_threshold": 3,
    },
    sticky_sessions={
        "type": "cookies",
        "cookie_name": "DO-LB",
        "cookie_ttl_seconds": 300,
    },
    redirect_http_to_https=True,
    enable_proxy_protocol=True,
    enable_backend_keepalive=True,
    http_idle_timeout_seconds=90,
    vpc_uuid="c33931f2-a26a-4e61-b85c-4e95a2ec431b",
    disable_lets_encrypt_dns_records=True,
    firewall={
        "deny": ["ip:1.2.3.4", "cidr:2.3.0.0/16"],
        "allow": ["ip:1.2.3.4", "cidr:2.3.0.0/16"],
    },
    tag="prod:web",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### droplet_ids: List[`int`]<a id="droplet_ids-listint"></a>

An array containing the IDs of the Droplets assigned to the load balancer.

##### region: [`RegionSlug`](./digital_ocean_python_sdk/type/region_slug.py)<a id="region-regionslugdigital_ocean_python_sdktyperegion_slugpy"></a>

##### id: `str`<a id="id-str"></a>

A unique ID that can be used to identify and reference a load balancer.

##### name: `str`<a id="name-str"></a>

A human-readable name for a load balancer instance.

##### project_id: `str`<a id="project_id-str"></a>

The ID of the project that the load balancer is associated with. If no ID is provided at creation, the load balancer associates with the user's default project. If an invalid project ID is provided, the load balancer will not be created.

##### ip: `str`<a id="ip-str"></a>

An attribute containing the public-facing IP address of the load balancer.

##### size_unit: `int`<a id="size_unit-int"></a>

How many nodes the load balancer contains. Each additional node increases the load balancer's ability to manage more connections. Load balancers can be scaled up or down, and you can change the number of nodes after creation up to once per hour. This field is currently not available in the AMS2, NYC2, or SFO1 regions. Use the `size` field to scale load balancers that reside in these regions.

##### size: `str`<a id="size-str"></a>

This field has been replaced by the `size_unit` field for all regions except in AMS2, NYC2, and SFO1. Each available load balancer size now equates to the load balancer having a set number of nodes. * `lb-small` = 1 node * `lb-medium` = 3 nodes * `lb-large` = 6 nodes  You can resize load balancers after creation up to once per hour. You cannot resize a load balancer within the first hour of its creation.

##### algorithm: `str`<a id="algorithm-str"></a>

This field has been deprecated. You can no longer specify an algorithm for load balancers.

##### status: `str`<a id="status-str"></a>

A status string indicating the current state of the load balancer. This can be `new`, `active`, or `errored`.

##### created_at: `datetime`<a id="created_at-datetime"></a>

A time value given in ISO8601 combined date and time format that represents when the load balancer was created.

##### forwarding_rules: List[`ForwardingRule`]<a id="forwarding_rules-listforwardingrule"></a>

An array of objects specifying the forwarding rules for a load balancer.

##### health_check: [`HealthCheck`](./digital_ocean_python_sdk/type/health_check.py)<a id="health_check-healthcheckdigital_ocean_python_sdktypehealth_checkpy"></a>


##### sticky_sessions: [`StickySessions`](./digital_ocean_python_sdk/type/sticky_sessions.py)<a id="sticky_sessions-stickysessionsdigital_ocean_python_sdktypesticky_sessionspy"></a>


##### redirect_http_to_https: `bool`<a id="redirect_http_to_https-bool"></a>

A boolean value indicating whether HTTP requests to the load balancer on port 80 will be redirected to HTTPS on port 443.

##### enable_proxy_protocol: `bool`<a id="enable_proxy_protocol-bool"></a>

A boolean value indicating whether PROXY Protocol is in use.

##### enable_backend_keepalive: `bool`<a id="enable_backend_keepalive-bool"></a>

A boolean value indicating whether HTTP keepalive connections are maintained to target Droplets.

##### http_idle_timeout_seconds: `int`<a id="http_idle_timeout_seconds-int"></a>

An integer value which configures the idle timeout for HTTP requests to the target droplets.

##### vpc_uuid: `str`<a id="vpc_uuid-str"></a>

A string specifying the UUID of the VPC to which the load balancer is assigned.

##### disable_lets_encrypt_dns_records: `bool`<a id="disable_lets_encrypt_dns_records-bool"></a>

A boolean value indicating whether to disable automatic DNS record creation for Let's Encrypt certificates that are added to the load balancer.

##### firewall: [`LbFirewall`](./digital_ocean_python_sdk/type/lb_firewall.py)<a id="firewall-lbfirewalldigital_ocean_python_sdktypelb_firewallpy"></a>


##### tag: `str`<a id="tag-str"></a>

The name of a Droplet tag corresponding to Droplets assigned to the load balancer.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`LoadBalancerCreate`](./digital_ocean_python_sdk/type/load_balancer_create.py)
#### 🔄 Return<a id="🔄-return"></a>

[`LoadBalancersCreateResponse`](./digital_ocean_python_sdk/pydantic/load_balancers_create_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/load_balancers` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.load_balancers.delete`<a id="digitaloceanload_balancersdelete"></a>

To delete a load balancer instance, disassociating any Droplets assigned to it
and removing it from your account, send a DELETE request to
`/v2/load_balancers/$LOAD_BALANCER_ID`.

A successful request will receive a 204 status code with no body in response.
This indicates that the request was processed successfully.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.load_balancers.delete(
    lb_id="4de7ac8b-495b-4884-9a69-1050c6793cd6",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### lb_id: `str`<a id="lb_id-str"></a>

A unique identifier for a load balancer.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/load_balancers/{lb_id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.load_balancers.get`<a id="digitaloceanload_balancersget"></a>

To show information about a load balancer instance, send a GET request to
`/v2/load_balancers/$LOAD_BALANCER_ID`.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_response = digitalocean.load_balancers.get(
    lb_id="4de7ac8b-495b-4884-9a69-1050c6793cd6",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### lb_id: `str`<a id="lb_id-str"></a>

A unique identifier for a load balancer.

#### 🔄 Return<a id="🔄-return"></a>

[`LoadBalancersGetResponse`](./digital_ocean_python_sdk/pydantic/load_balancers_get_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/load_balancers/{lb_id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.load_balancers.list`<a id="digitaloceanload_balancerslist"></a>

To list all of the load balancer instances on your account, send a GET request
to `/v2/load_balancers`.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = digitalocean.load_balancers.list(
    per_page=2,
    page=1,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### per_page: `int`<a id="per_page-int"></a>

Number of items returned per page

##### page: `int`<a id="page-int"></a>

Which 'page' of paginated results to return.

#### 🔄 Return<a id="🔄-return"></a>

[`LoadBalancersListResponse`](./digital_ocean_python_sdk/pydantic/load_balancers_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/load_balancers` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.load_balancers.remove_droplets`<a id="digitaloceanload_balancersremove_droplets"></a>

To remove a Droplet from a load balancer instance, send a DELETE request to
`/v2/load_balancers/$LOAD_BALANCER_ID/droplets`. In the body of the request,
there should be a `droplet_ids` attribute containing a list of Droplet IDs.

No response body will be sent back, but the response code will indicate
success. Specifically, the response code will be a 204, which means that the
action was successful with no returned body data.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.load_balancers.remove_droplets(
    body=None,
    droplet_ids=[3164444, 3164445],
    lb_id="4de7ac8b-495b-4884-9a69-1050c6793cd6",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### droplet_ids: List[`int`]<a id="droplet_ids-listint"></a>

An array containing the IDs of the Droplets assigned to the load balancer.

##### lb_id: `str`<a id="lb_id-str"></a>

A unique identifier for a load balancer.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`LoadBalancersRemoveDropletsRequest`](./digital_ocean_python_sdk/type/load_balancers_remove_droplets_request.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/load_balancers/{lb_id}/droplets` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.load_balancers.remove_forwarding_rules`<a id="digitaloceanload_balancersremove_forwarding_rules"></a>

To remove forwarding rules from a load balancer instance, send a DELETE
request to `/v2/load_balancers/$LOAD_BALANCER_ID/forwarding_rules`. In the
body of the request, there should be a `forwarding_rules` attribute containing
an array of rules to be removed.

No response body will be sent back, but the response code will indicate
success. Specifically, the response code will be a 204, which means that the
action was successful with no returned body data.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.load_balancers.remove_forwarding_rules(
    body=None,
    forwarding_rules=[
        {
            "entry_protocol": "https",
            "entry_port": 443,
            "target_protocol": "http",
            "target_port": 80,
            "certificate_id": "892071a0-bb95-49bc-8021-3afd67a210bf",
            "tls_passthrough": False,
        }
    ],
    lb_id="4de7ac8b-495b-4884-9a69-1050c6793cd6",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### forwarding_rules: List[`ForwardingRule`]<a id="forwarding_rules-listforwardingrule"></a>

##### lb_id: `str`<a id="lb_id-str"></a>

A unique identifier for a load balancer.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`LoadBalancersRemoveForwardingRulesRequest`](./digital_ocean_python_sdk/type/load_balancers_remove_forwarding_rules_request.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/load_balancers/{lb_id}/forwarding_rules` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.load_balancers.update`<a id="digitaloceanload_balancersupdate"></a>

To update a load balancer's settings, send a PUT request to
`/v2/load_balancers/$LOAD_BALANCER_ID`. The request should contain a full
representation of the load balancer including existing attributes. It may
contain _one of_ the `droplets_ids` or `tag` attributes as they are mutually
exclusive. **Note that any attribute that is not provided will be reset to its
default value.**


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_response = digitalocean.load_balancers.update(
    body=None,
    lb_id="4de7ac8b-495b-4884-9a69-1050c6793cd6",
    droplet_ids=[3164444, 3164445],
    region="nyc3",
    id="4de7ac8b-495b-4884-9a69-1050c6793cd6",
    name="example-lb-01",
    project_id="4de7ac8b-495b-4884-9a69-1050c6793cd6",
    ip="104.131.186.241",
    size_unit=3,
    size="lb-small",
    algorithm="round_robin",
    status="new",
    created_at="2017-02-01T22:22:58Z",
    forwarding_rules=[
        {
            "entry_protocol": "https",
            "entry_port": 443,
            "target_protocol": "http",
            "target_port": 80,
            "certificate_id": "892071a0-bb95-49bc-8021-3afd67a210bf",
            "tls_passthrough": False,
        }
    ],
    health_check={
        "protocol": "http",
        "port": 80,
        "path": "/",
        "check_interval_seconds": 10,
        "response_timeout_seconds": 5,
        "unhealthy_threshold": 5,
        "healthy_threshold": 3,
    },
    sticky_sessions={
        "type": "cookies",
        "cookie_name": "DO-LB",
        "cookie_ttl_seconds": 300,
    },
    redirect_http_to_https=True,
    enable_proxy_protocol=True,
    enable_backend_keepalive=True,
    http_idle_timeout_seconds=90,
    vpc_uuid="c33931f2-a26a-4e61-b85c-4e95a2ec431b",
    disable_lets_encrypt_dns_records=True,
    firewall={
        "deny": ["ip:1.2.3.4", "cidr:2.3.0.0/16"],
        "allow": ["ip:1.2.3.4", "cidr:2.3.0.0/16"],
    },
    tag="prod:web",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### lb_id: `str`<a id="lb_id-str"></a>

A unique identifier for a load balancer.

##### droplet_ids: List[`int`]<a id="droplet_ids-listint"></a>

An array containing the IDs of the Droplets assigned to the load balancer.

##### region: [`RegionSlug`](./digital_ocean_python_sdk/type/region_slug.py)<a id="region-regionslugdigital_ocean_python_sdktyperegion_slugpy"></a>

##### id: `str`<a id="id-str"></a>

A unique ID that can be used to identify and reference a load balancer.

##### name: `str`<a id="name-str"></a>

A human-readable name for a load balancer instance.

##### project_id: `str`<a id="project_id-str"></a>

The ID of the project that the load balancer is associated with. If no ID is provided at creation, the load balancer associates with the user's default project. If an invalid project ID is provided, the load balancer will not be created.

##### ip: `str`<a id="ip-str"></a>

An attribute containing the public-facing IP address of the load balancer.

##### size_unit: `int`<a id="size_unit-int"></a>

How many nodes the load balancer contains. Each additional node increases the load balancer's ability to manage more connections. Load balancers can be scaled up or down, and you can change the number of nodes after creation up to once per hour. This field is currently not available in the AMS2, NYC2, or SFO1 regions. Use the `size` field to scale load balancers that reside in these regions.

##### size: `str`<a id="size-str"></a>

This field has been replaced by the `size_unit` field for all regions except in AMS2, NYC2, and SFO1. Each available load balancer size now equates to the load balancer having a set number of nodes. * `lb-small` = 1 node * `lb-medium` = 3 nodes * `lb-large` = 6 nodes  You can resize load balancers after creation up to once per hour. You cannot resize a load balancer within the first hour of its creation.

##### algorithm: `str`<a id="algorithm-str"></a>

This field has been deprecated. You can no longer specify an algorithm for load balancers.

##### status: `str`<a id="status-str"></a>

A status string indicating the current state of the load balancer. This can be `new`, `active`, or `errored`.

##### created_at: `datetime`<a id="created_at-datetime"></a>

A time value given in ISO8601 combined date and time format that represents when the load balancer was created.

##### forwarding_rules: List[`ForwardingRule`]<a id="forwarding_rules-listforwardingrule"></a>

An array of objects specifying the forwarding rules for a load balancer.

##### health_check: [`HealthCheck`](./digital_ocean_python_sdk/type/health_check.py)<a id="health_check-healthcheckdigital_ocean_python_sdktypehealth_checkpy"></a>


##### sticky_sessions: [`StickySessions`](./digital_ocean_python_sdk/type/sticky_sessions.py)<a id="sticky_sessions-stickysessionsdigital_ocean_python_sdktypesticky_sessionspy"></a>


##### redirect_http_to_https: `bool`<a id="redirect_http_to_https-bool"></a>

A boolean value indicating whether HTTP requests to the load balancer on port 80 will be redirected to HTTPS on port 443.

##### enable_proxy_protocol: `bool`<a id="enable_proxy_protocol-bool"></a>

A boolean value indicating whether PROXY Protocol is in use.

##### enable_backend_keepalive: `bool`<a id="enable_backend_keepalive-bool"></a>

A boolean value indicating whether HTTP keepalive connections are maintained to target Droplets.

##### http_idle_timeout_seconds: `int`<a id="http_idle_timeout_seconds-int"></a>

An integer value which configures the idle timeout for HTTP requests to the target droplets.

##### vpc_uuid: `str`<a id="vpc_uuid-str"></a>

A string specifying the UUID of the VPC to which the load balancer is assigned.

##### disable_lets_encrypt_dns_records: `bool`<a id="disable_lets_encrypt_dns_records-bool"></a>

A boolean value indicating whether to disable automatic DNS record creation for Let's Encrypt certificates that are added to the load balancer.

##### firewall: [`LbFirewall`](./digital_ocean_python_sdk/type/lb_firewall.py)<a id="firewall-lbfirewalldigital_ocean_python_sdktypelb_firewallpy"></a>


##### tag: `str`<a id="tag-str"></a>

The name of a Droplet tag corresponding to Droplets assigned to the load balancer.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`LoadBalancerCreate`](./digital_ocean_python_sdk/type/load_balancer_create.py)
#### 🔄 Return<a id="🔄-return"></a>

[`LoadBalancersUpdateResponse`](./digital_ocean_python_sdk/pydantic/load_balancers_update_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/load_balancers/{lb_id}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.monitoring.create_alert_policy`<a id="digitaloceanmonitoringcreate_alert_policy"></a>

To create a new alert, send a POST request to `/v2/monitoring/alerts`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_alert_policy_response = digitalocean.monitoring.create_alert_policy(
    tags=["droplet_tag"],
    description="CPU Alert",
    alerts={
        "email": ["bob@exmaple.com"],
        "slack": [
            {
                "channel": "Production Alerts",
                "url": "https://hooks.slack.com/services/T1234567/AAAAAAAA/ZZZZZZ",
            }
        ],
    },
    compare="GreaterThan",
    enabled=True,
    entities=["192018292"],
    type="v1/insights/droplet/cpu",
    value=80,
    window="5m",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### tags: [`AlertPolicyRequestTags`](./digital_ocean_python_sdk/type/alert_policy_request_tags.py)<a id="tags-alertpolicyrequesttagsdigital_ocean_python_sdktypealert_policy_request_tagspy"></a>

##### description: `str`<a id="description-str"></a>

##### alerts: [`Alerts`](./digital_ocean_python_sdk/type/alerts.py)<a id="alerts-alertsdigital_ocean_python_sdktypealertspy"></a>


##### compare: `str`<a id="compare-str"></a>

##### enabled: `bool`<a id="enabled-bool"></a>

##### entities: [`AlertPolicyRequestEntities`](./digital_ocean_python_sdk/type/alert_policy_request_entities.py)<a id="entities-alertpolicyrequestentitiesdigital_ocean_python_sdktypealert_policy_request_entitiespy"></a>

##### type: `str`<a id="type-str"></a>

##### value: `Union[int, float]`<a id="value-unionint-float"></a>

##### window: `str`<a id="window-str"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`AlertPolicyRequest`](./digital_ocean_python_sdk/type/alert_policy_request.py)
The `type` field dictates what type of entity that the alert policy applies to and hence what type of entity is passed in the `entities` array. If both the `tags` array and `entities` array are empty the alert policy applies to all entities of the relevant type that are owned by the user account. Otherwise the following table shows the valid entity types for each type of alert policy:  Type | Description | Valid Entity Type -----|-------------|-------------------- `v1/insights/droplet/memory_utilization_percent` | alert on the percent of memory utilization | Droplet ID `v1/insights/droplet/disk_read` | alert on the rate of disk read I/O in MBps | Droplet ID `v1/insights/droplet/load_5` | alert on the 5 minute load average | Droplet ID `v1/insights/droplet/load_15` | alert on the 15 minute load average | Droplet ID `v1/insights/droplet/disk_utilization_percent` | alert on the percent of disk utilization | Droplet ID `v1/insights/droplet/cpu` | alert on the percent of CPU utilization | Droplet ID `v1/insights/droplet/disk_write` | alert on the rate of disk write I/O in MBps | Droplet ID `v1/insights/droplet/public_outbound_bandwidth` | alert on the rate of public outbound bandwidth in Mbps | Droplet ID `v1/insights/droplet/public_inbound_bandwidth` | alert on the rate of public inbound bandwidth in Mbps | Droplet ID `v1/insights/droplet/private_outbound_bandwidth` | alert on the rate of private outbound bandwidth in Mbps | Droplet ID `v1/insights/droplet/private_inbound_bandwidth` | alert on the rate of private inbound bandwidth in Mbps | Droplet ID `v1/insights/droplet/load_1` | alert on the 1 minute load average | Droplet ID `v1/insights/lbaas/avg_cpu_utilization_percent`|alert on the percent of CPU utilization|load balancer ID `v1/insights/lbaas/connection_utilization_percent`|alert on the percent of connection utilization|load balancer ID `v1/insights/lbaas/droplet_health`|alert on Droplet health status changes|load balancer ID `v1/insights/lbaas/tls_connections_per_second_utilization_percent`|alert on the percent of TLS connections per second utilization|load balancer ID `v1/insights/lbaas/increase_in_http_error_rate_percentage_5xx`|alert on the percent increase of 5xx level http errors over 5m|load balancer ID `v1/insights/lbaas/increase_in_http_error_rate_percentage_4xx`|alert on the percent increase of 4xx level http errors over 5m|load balancer ID `v1/insights/lbaas/increase_in_http_error_rate_count_5xx`|alert on the count of 5xx level http errors over 5m|load balancer ID `v1/insights/lbaas/increase_in_http_error_rate_count_4xx`|alert on the count of 4xx level http errors over 5m|load balancer ID `v1/insights/lbaas/high_http_request_response_time`|alert on high average http response time|load balancer ID `v1/insights/lbaas/high_http_request_response_time_50p`|alert on high 50th percentile http response time|load balancer ID `v1/insights/lbaas/high_http_request_response_time_95p`|alert on high 95th percentile http response time|load balancer ID `v1/insights/lbaas/high_http_request_response_time_99p`|alert on high 99th percentile http response time|load balancer ID `v1/dbaas/alerts/load_15_alerts` | alert on 15 minute load average across the database cluster | database cluster UUID `v1/dbaas/alerts/memory_utilization_alerts` | alert on the percent memory utilization average across the database cluster | database cluster UUID `v1/dbaas/alerts/disk_utilization_alerts` | alert on the percent disk utilization average across the database cluster | database cluster UUID `v1/dbaas/alerts/cpu_alerts` | alert on the percent CPU usage average across the database cluster | database cluster UUID 

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/monitoring/alerts` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.monitoring.delete_alert_policy`<a id="digitaloceanmonitoringdelete_alert_policy"></a>

To delete an alert policy, send a DELETE request to `/v2/monitoring/alerts/{alert_uuid}`

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.monitoring.delete_alert_policy(
    alert_uuid="4de7ac8b-495b-4884-9a69-1050c6793cd6",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### alert_uuid: `str`<a id="alert_uuid-str"></a>

A unique identifier for an alert policy.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/monitoring/alerts/{alert_uuid}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.monitoring.droplet_cpu_metricsget`<a id="digitaloceanmonitoringdroplet_cpu_metricsget"></a>

To retrieve CPU metrics for a given droplet, send a GET request to `/v2/monitoring/metrics/droplet/cpu`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
droplet_cpu_metricsget_response = digitalocean.monitoring.droplet_cpu_metricsget(
    host_id="17209102",
    start="1620683817",
    end="1620705417",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### host_id: `str`<a id="host_id-str"></a>

The droplet ID.

##### start: `str`<a id="start-str"></a>

Timestamp to start metric window.

##### end: `str`<a id="end-str"></a>

Timestamp to end metric window.

#### 🔄 Return<a id="🔄-return"></a>

[`Metrics`](./digital_ocean_python_sdk/pydantic/metrics.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/monitoring/metrics/droplet/cpu` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.monitoring.droplet_load5_metrics_get`<a id="digitaloceanmonitoringdroplet_load5_metrics_get"></a>

To retrieve 5 minute load average metrics for a given droplet, send a GET request to `/v2/monitoring/metrics/droplet/load_5`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
droplet_load5_metrics_get_response = digitalocean.monitoring.droplet_load5_metrics_get(
    host_id="17209102",
    start="1620683817",
    end="1620705417",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### host_id: `str`<a id="host_id-str"></a>

The droplet ID.

##### start: `str`<a id="start-str"></a>

Timestamp to start metric window.

##### end: `str`<a id="end-str"></a>

Timestamp to end metric window.

#### 🔄 Return<a id="🔄-return"></a>

[`Metrics`](./digital_ocean_python_sdk/pydantic/metrics.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/monitoring/metrics/droplet/load_5` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.monitoring.droplet_memory_cached_metrics`<a id="digitaloceanmonitoringdroplet_memory_cached_metrics"></a>

To retrieve cached memory metrics for a given droplet, send a GET request to `/v2/monitoring/metrics/droplet/memory_cached`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
droplet_memory_cached_metrics_response = digitalocean.monitoring.droplet_memory_cached_metrics(
    host_id="17209102",
    start="1620683817",
    end="1620705417",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### host_id: `str`<a id="host_id-str"></a>

The droplet ID.

##### start: `str`<a id="start-str"></a>

Timestamp to start metric window.

##### end: `str`<a id="end-str"></a>

Timestamp to end metric window.

#### 🔄 Return<a id="🔄-return"></a>

[`Metrics`](./digital_ocean_python_sdk/pydantic/metrics.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/monitoring/metrics/droplet/memory_cached` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.monitoring.get_app_cpu_percentage_metrics`<a id="digitaloceanmonitoringget_app_cpu_percentage_metrics"></a>

To retrieve cpu percentage metrics for a given app, send a GET request to `/v2/monitoring/metrics/apps/cpu_percentage`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_app_cpu_percentage_metrics_response = digitalocean.monitoring.get_app_cpu_percentage_metrics(
    app_id="2db3c021-15ad-4088-bfe8-99dc972b9cf6",
    start="1620683817",
    end="1620705417",
    app_component="sample-application",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### app_id: `str`<a id="app_id-str"></a>

The app UUID.

##### start: `str`<a id="start-str"></a>

Timestamp to start metric window.

##### end: `str`<a id="end-str"></a>

Timestamp to end metric window.

##### app_component: `str`<a id="app_component-str"></a>

The app component name.

#### 🔄 Return<a id="🔄-return"></a>

[`Metrics`](./digital_ocean_python_sdk/pydantic/metrics.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/monitoring/metrics/apps/cpu_percentage` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.monitoring.get_app_memory_percentage_metrics`<a id="digitaloceanmonitoringget_app_memory_percentage_metrics"></a>

To retrieve memory percentage metrics for a given app, send a GET request to `/v2/monitoring/metrics/apps/memory_percentage`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_app_memory_percentage_metrics_response = digitalocean.monitoring.get_app_memory_percentage_metrics(
    app_id="2db3c021-15ad-4088-bfe8-99dc972b9cf6",
    start="1620683817",
    end="1620705417",
    app_component="sample-application",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### app_id: `str`<a id="app_id-str"></a>

The app UUID.

##### start: `str`<a id="start-str"></a>

Timestamp to start metric window.

##### end: `str`<a id="end-str"></a>

Timestamp to end metric window.

##### app_component: `str`<a id="app_component-str"></a>

The app component name.

#### 🔄 Return<a id="🔄-return"></a>

[`Metrics`](./digital_ocean_python_sdk/pydantic/metrics.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/monitoring/metrics/apps/memory_percentage` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.monitoring.get_app_restart_count_metrics`<a id="digitaloceanmonitoringget_app_restart_count_metrics"></a>

To retrieve restart count metrics for a given app, send a GET request to `/v2/monitoring/metrics/apps/restart_count`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_app_restart_count_metrics_response = digitalocean.monitoring.get_app_restart_count_metrics(
    app_id="2db3c021-15ad-4088-bfe8-99dc972b9cf6",
    start="1620683817",
    end="1620705417",
    app_component="sample-application",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### app_id: `str`<a id="app_id-str"></a>

The app UUID.

##### start: `str`<a id="start-str"></a>

Timestamp to start metric window.

##### end: `str`<a id="end-str"></a>

Timestamp to end metric window.

##### app_component: `str`<a id="app_component-str"></a>

The app component name.

#### 🔄 Return<a id="🔄-return"></a>

[`Metrics`](./digital_ocean_python_sdk/pydantic/metrics.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/monitoring/metrics/apps/restart_count` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.monitoring.get_droplet_bandwidth_metrics`<a id="digitaloceanmonitoringget_droplet_bandwidth_metrics"></a>

To retrieve bandwidth metrics for a given Droplet, send a GET request to `/v2/monitoring/metrics/droplet/bandwidth`. Use the `interface` query parameter to specify if the results should be for the `private` or `public` interface. Use the `direction` query parameter to specify if the results should be for `inbound` or `outbound` traffic.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_droplet_bandwidth_metrics_response = digitalocean.monitoring.get_droplet_bandwidth_metrics(
    host_id="17209102",
    interface="private",
    direction="inbound",
    start="1620683817",
    end="1620705417",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### host_id: `str`<a id="host_id-str"></a>

The droplet ID.

##### interface: `str`<a id="interface-str"></a>

The network interface.

##### direction: `str`<a id="direction-str"></a>

The traffic direction.

##### start: `str`<a id="start-str"></a>

Timestamp to start metric window.

##### end: `str`<a id="end-str"></a>

Timestamp to end metric window.

#### 🔄 Return<a id="🔄-return"></a>

[`Metrics`](./digital_ocean_python_sdk/pydantic/metrics.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/monitoring/metrics/droplet/bandwidth` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.monitoring.get_droplet_filesystem_free_metrics`<a id="digitaloceanmonitoringget_droplet_filesystem_free_metrics"></a>

To retrieve filesystem free metrics for a given droplet, send a GET request to `/v2/monitoring/metrics/droplet/filesystem_free`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_droplet_filesystem_free_metrics_response = digitalocean.monitoring.get_droplet_filesystem_free_metrics(
    host_id="17209102",
    start="1620683817",
    end="1620705417",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### host_id: `str`<a id="host_id-str"></a>

The droplet ID.

##### start: `str`<a id="start-str"></a>

Timestamp to start metric window.

##### end: `str`<a id="end-str"></a>

Timestamp to end metric window.

#### 🔄 Return<a id="🔄-return"></a>

[`Metrics`](./digital_ocean_python_sdk/pydantic/metrics.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/monitoring/metrics/droplet/filesystem_free` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.monitoring.get_droplet_filesystem_size_metrics`<a id="digitaloceanmonitoringget_droplet_filesystem_size_metrics"></a>

To retrieve filesystem size metrics for a given droplet, send a GET request to `/v2/monitoring/metrics/droplet/filesystem_size`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_droplet_filesystem_size_metrics_response = digitalocean.monitoring.get_droplet_filesystem_size_metrics(
    host_id="17209102",
    start="1620683817",
    end="1620705417",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### host_id: `str`<a id="host_id-str"></a>

The droplet ID.

##### start: `str`<a id="start-str"></a>

Timestamp to start metric window.

##### end: `str`<a id="end-str"></a>

Timestamp to end metric window.

#### 🔄 Return<a id="🔄-return"></a>

[`Metrics`](./digital_ocean_python_sdk/pydantic/metrics.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/monitoring/metrics/droplet/filesystem_size` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.monitoring.get_droplet_load15_metrics`<a id="digitaloceanmonitoringget_droplet_load15_metrics"></a>

To retrieve 15 minute load average metrics for a given droplet, send a GET request to `/v2/monitoring/metrics/droplet/load_15`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_droplet_load15_metrics_response = digitalocean.monitoring.get_droplet_load15_metrics(
    host_id="17209102",
    start="1620683817",
    end="1620705417",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### host_id: `str`<a id="host_id-str"></a>

The droplet ID.

##### start: `str`<a id="start-str"></a>

Timestamp to start metric window.

##### end: `str`<a id="end-str"></a>

Timestamp to end metric window.

#### 🔄 Return<a id="🔄-return"></a>

[`Metrics`](./digital_ocean_python_sdk/pydantic/metrics.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/monitoring/metrics/droplet/load_15` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.monitoring.get_droplet_load1_metrics`<a id="digitaloceanmonitoringget_droplet_load1_metrics"></a>

To retrieve 1 minute load average metrics for a given droplet, send a GET request to `/v2/monitoring/metrics/droplet/load_1`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_droplet_load1_metrics_response = digitalocean.monitoring.get_droplet_load1_metrics(
    host_id="17209102",
    start="1620683817",
    end="1620705417",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### host_id: `str`<a id="host_id-str"></a>

The droplet ID.

##### start: `str`<a id="start-str"></a>

Timestamp to start metric window.

##### end: `str`<a id="end-str"></a>

Timestamp to end metric window.

#### 🔄 Return<a id="🔄-return"></a>

[`Metrics`](./digital_ocean_python_sdk/pydantic/metrics.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/monitoring/metrics/droplet/load_1` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.monitoring.get_droplet_memory_available_metrics`<a id="digitaloceanmonitoringget_droplet_memory_available_metrics"></a>

To retrieve available memory metrics for a given droplet, send a GET request to `/v2/monitoring/metrics/droplet/memory_available`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_droplet_memory_available_metrics_response = digitalocean.monitoring.get_droplet_memory_available_metrics(
    host_id="17209102",
    start="1620683817",
    end="1620705417",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### host_id: `str`<a id="host_id-str"></a>

The droplet ID.

##### start: `str`<a id="start-str"></a>

Timestamp to start metric window.

##### end: `str`<a id="end-str"></a>

Timestamp to end metric window.

#### 🔄 Return<a id="🔄-return"></a>

[`Metrics`](./digital_ocean_python_sdk/pydantic/metrics.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/monitoring/metrics/droplet/memory_available` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.monitoring.get_droplet_memory_free_metrics`<a id="digitaloceanmonitoringget_droplet_memory_free_metrics"></a>

To retrieve free memory metrics for a given droplet, send a GET request to `/v2/monitoring/metrics/droplet/memory_free`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_droplet_memory_free_metrics_response = digitalocean.monitoring.get_droplet_memory_free_metrics(
    host_id="17209102",
    start="1620683817",
    end="1620705417",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### host_id: `str`<a id="host_id-str"></a>

The droplet ID.

##### start: `str`<a id="start-str"></a>

Timestamp to start metric window.

##### end: `str`<a id="end-str"></a>

Timestamp to end metric window.

#### 🔄 Return<a id="🔄-return"></a>

[`Metrics`](./digital_ocean_python_sdk/pydantic/metrics.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/monitoring/metrics/droplet/memory_free` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.monitoring.get_droplet_memory_total_metrics`<a id="digitaloceanmonitoringget_droplet_memory_total_metrics"></a>

To retrieve total memory metrics for a given droplet, send a GET request to `/v2/monitoring/metrics/droplet/memory_total`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_droplet_memory_total_metrics_response = digitalocean.monitoring.get_droplet_memory_total_metrics(
    host_id="17209102",
    start="1620683817",
    end="1620705417",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### host_id: `str`<a id="host_id-str"></a>

The droplet ID.

##### start: `str`<a id="start-str"></a>

Timestamp to start metric window.

##### end: `str`<a id="end-str"></a>

Timestamp to end metric window.

#### 🔄 Return<a id="🔄-return"></a>

[`Metrics`](./digital_ocean_python_sdk/pydantic/metrics.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/monitoring/metrics/droplet/memory_total` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.monitoring.get_existing_alert_policy`<a id="digitaloceanmonitoringget_existing_alert_policy"></a>

To retrieve a given alert policy, send a GET request to `/v2/monitoring/alerts/{alert_uuid}`

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_existing_alert_policy_response = digitalocean.monitoring.get_existing_alert_policy(
    alert_uuid="4de7ac8b-495b-4884-9a69-1050c6793cd6",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### alert_uuid: `str`<a id="alert_uuid-str"></a>

A unique identifier for an alert policy.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/monitoring/alerts/{alert_uuid}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.monitoring.list_alert_policies`<a id="digitaloceanmonitoringlist_alert_policies"></a>

Returns all alert policies that are configured for the given account. To List all alert policies, send a GET request to `/v2/monitoring/alerts`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_alert_policies_response = digitalocean.monitoring.list_alert_policies(
    per_page=2,
    page=1,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### per_page: `int`<a id="per_page-int"></a>

Number of items returned per page

##### page: `int`<a id="page-int"></a>

Which 'page' of paginated results to return.

#### 🔄 Return<a id="🔄-return"></a>

[`MonitoringListAlertPoliciesResponse`](./digital_ocean_python_sdk/pydantic/monitoring_list_alert_policies_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/monitoring/alerts` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.monitoring.update_alert_policy`<a id="digitaloceanmonitoringupdate_alert_policy"></a>

To update en existing policy, send a PUT request to `v2/monitoring/alerts/{alert_uuid}`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_alert_policy_response = digitalocean.monitoring.update_alert_policy(
    tags=["droplet_tag"],
    description="CPU Alert",
    alerts={
        "email": ["bob@exmaple.com"],
        "slack": [
            {
                "channel": "Production Alerts",
                "url": "https://hooks.slack.com/services/T1234567/AAAAAAAA/ZZZZZZ",
            }
        ],
    },
    compare="GreaterThan",
    enabled=True,
    entities=["192018292"],
    type="v1/insights/droplet/cpu",
    value=80,
    window="5m",
    alert_uuid="4de7ac8b-495b-4884-9a69-1050c6793cd6",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### tags: [`AlertPolicyRequestTags`](./digital_ocean_python_sdk/type/alert_policy_request_tags.py)<a id="tags-alertpolicyrequesttagsdigital_ocean_python_sdktypealert_policy_request_tagspy"></a>

##### description: `str`<a id="description-str"></a>

##### alerts: [`Alerts`](./digital_ocean_python_sdk/type/alerts.py)<a id="alerts-alertsdigital_ocean_python_sdktypealertspy"></a>


##### compare: `str`<a id="compare-str"></a>

##### enabled: `bool`<a id="enabled-bool"></a>

##### entities: [`AlertPolicyRequestEntities`](./digital_ocean_python_sdk/type/alert_policy_request_entities.py)<a id="entities-alertpolicyrequestentitiesdigital_ocean_python_sdktypealert_policy_request_entitiespy"></a>

##### type: `str`<a id="type-str"></a>

##### value: `Union[int, float]`<a id="value-unionint-float"></a>

##### window: `str`<a id="window-str"></a>

##### alert_uuid: `str`<a id="alert_uuid-str"></a>

A unique identifier for an alert policy.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`AlertPolicyRequest`](./digital_ocean_python_sdk/type/alert_policy_request.py)
The `type` field dictates what type of entity that the alert policy applies to and hence what type of entity is passed in the `entities` array. If both the `tags` array and `entities` array are empty the alert policy applies to all entities of the relevant type that are owned by the user account. Otherwise the following table shows the valid entity types for each type of alert policy:  Type | Description | Valid Entity Type -----|-------------|-------------------- `v1/insights/droplet/memory_utilization_percent` | alert on the percent of memory utilization | Droplet ID `v1/insights/droplet/disk_read` | alert on the rate of disk read I/O in MBps | Droplet ID `v1/insights/droplet/load_5` | alert on the 5 minute load average | Droplet ID `v1/insights/droplet/load_15` | alert on the 15 minute load average | Droplet ID `v1/insights/droplet/disk_utilization_percent` | alert on the percent of disk utilization | Droplet ID `v1/insights/droplet/cpu` | alert on the percent of CPU utilization | Droplet ID `v1/insights/droplet/disk_write` | alert on the rate of disk write I/O in MBps | Droplet ID `v1/insights/droplet/public_outbound_bandwidth` | alert on the rate of public outbound bandwidth in Mbps | Droplet ID `v1/insights/droplet/public_inbound_bandwidth` | alert on the rate of public inbound bandwidth in Mbps | Droplet ID `v1/insights/droplet/private_outbound_bandwidth` | alert on the rate of private outbound bandwidth in Mbps | Droplet ID `v1/insights/droplet/private_inbound_bandwidth` | alert on the rate of private inbound bandwidth in Mbps | Droplet ID `v1/insights/droplet/load_1` | alert on the 1 minute load average | Droplet ID `v1/insights/lbaas/avg_cpu_utilization_percent`|alert on the percent of CPU utilization|load balancer ID `v1/insights/lbaas/connection_utilization_percent`|alert on the percent of connection utilization|load balancer ID `v1/insights/lbaas/droplet_health`|alert on Droplet health status changes|load balancer ID `v1/insights/lbaas/tls_connections_per_second_utilization_percent`|alert on the percent of TLS connections per second utilization|load balancer ID `v1/insights/lbaas/increase_in_http_error_rate_percentage_5xx`|alert on the percent increase of 5xx level http errors over 5m|load balancer ID `v1/insights/lbaas/increase_in_http_error_rate_percentage_4xx`|alert on the percent increase of 4xx level http errors over 5m|load balancer ID `v1/insights/lbaas/increase_in_http_error_rate_count_5xx`|alert on the count of 5xx level http errors over 5m|load balancer ID `v1/insights/lbaas/increase_in_http_error_rate_count_4xx`|alert on the count of 4xx level http errors over 5m|load balancer ID `v1/insights/lbaas/high_http_request_response_time`|alert on high average http response time|load balancer ID `v1/insights/lbaas/high_http_request_response_time_50p`|alert on high 50th percentile http response time|load balancer ID `v1/insights/lbaas/high_http_request_response_time_95p`|alert on high 95th percentile http response time|load balancer ID `v1/insights/lbaas/high_http_request_response_time_99p`|alert on high 99th percentile http response time|load balancer ID `v1/dbaas/alerts/load_15_alerts` | alert on 15 minute load average across the database cluster | database cluster UUID `v1/dbaas/alerts/memory_utilization_alerts` | alert on the percent memory utilization average across the database cluster | database cluster UUID `v1/dbaas/alerts/disk_utilization_alerts` | alert on the percent disk utilization average across the database cluster | database cluster UUID `v1/dbaas/alerts/cpu_alerts` | alert on the percent CPU usage average across the database cluster | database cluster UUID 

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/monitoring/alerts/{alert_uuid}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.project_resources.assign_resources_to_default`<a id="digitaloceanproject_resourcesassign_resources_to_default"></a>

To assign resources to your default project, send a POST request to `/v2/projects/default/resources`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
assign_resources_to_default_response = digitalocean.project_resources.assign_resources_to_default(
    resources=["do:droplet:13457723"],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### resources: List[`Urn`]<a id="resources-listurn"></a>

A list of uniform resource names (URNs) to be added to a project.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ProjectAssignment`](./digital_ocean_python_sdk/type/project_assignment.py)
#### 🔄 Return<a id="🔄-return"></a>

[`ProjectResourcesAssignToProjectResponse`](./digital_ocean_python_sdk/pydantic/project_resources_assign_to_project_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/projects/default/resources` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.project_resources.assign_to_project`<a id="digitaloceanproject_resourcesassign_to_project"></a>

To assign resources to a project, send a POST request to `/v2/projects/$PROJECT_ID/resources`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
assign_to_project_response = digitalocean.project_resources.assign_to_project(
    project_id="4de7ac8b-495b-4884-9a69-1050c6793cd6",
    resources=["do:droplet:13457723"],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_id: `str`<a id="project_id-str"></a>

A unique identifier for a project.

##### resources: List[`Urn`]<a id="resources-listurn"></a>

A list of uniform resource names (URNs) to be added to a project.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ProjectAssignment`](./digital_ocean_python_sdk/type/project_assignment.py)
#### 🔄 Return<a id="🔄-return"></a>

[`ProjectResourcesAssignToProjectResponse`](./digital_ocean_python_sdk/pydantic/project_resources_assign_to_project_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/projects/{project_id}/resources` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.project_resources.list`<a id="digitaloceanproject_resourceslist"></a>

To list all your resources in a project, send a GET request to `/v2/projects/$PROJECT_ID/resources`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = digitalocean.project_resources.list(
    project_id="4de7ac8b-495b-4884-9a69-1050c6793cd6",
    per_page=2,
    page=1,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_id: `str`<a id="project_id-str"></a>

A unique identifier for a project.

##### per_page: `int`<a id="per_page-int"></a>

Number of items returned per page

##### page: `int`<a id="page-int"></a>

Which 'page' of paginated results to return.

#### 🔄 Return<a id="🔄-return"></a>

[`ProjectResourcesListResponse`](./digital_ocean_python_sdk/pydantic/project_resources_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/projects/{project_id}/resources` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.project_resources.list_default`<a id="digitaloceanproject_resourceslist_default"></a>

To list all your resources in your default project, send a GET request to `/v2/projects/default/resources`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_default_response = digitalocean.project_resources.list_default()
```

#### 🔄 Return<a id="🔄-return"></a>

[`ProjectResourcesListResponse`](./digital_ocean_python_sdk/pydantic/project_resources_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/projects/default/resources` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.projects.create`<a id="digitaloceanprojectscreate"></a>

To create a project, send a POST request to `/v2/projects`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_response = digitalocean.projects.create(
    description="My website API",
    id="4e1bfbc3-dc3e-41f2-a18f-1b4d7ba71679",
    owner_uuid="99525febec065ca37b2ffe4f852fd2b2581895e7",
    owner_id=258992,
    name="my-web-api",
    purpose="Service or API",
    environment="Production",
    created_at="2018-09-27T20:10:35Z",
    updated_at="2018-09-27T20:10:35Z",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### description: `str`<a id="description-str"></a>

The description of the project. The maximum length is 255 characters.

##### id: `str`<a id="id-str"></a>

The unique universal identifier of this project.

##### owner_uuid: `str`<a id="owner_uuid-str"></a>

The unique universal identifier of the project owner.

##### owner_id: `int`<a id="owner_id-int"></a>

The integer id of the project owner.

##### name: `str`<a id="name-str"></a>

The human-readable name for the project. The maximum length is 175 characters and the name must be unique.

##### purpose: `str`<a id="purpose-str"></a>

The purpose of the project. The maximum length is 255 characters. It can have one of the following values:  - Just trying out DigitalOcean - Class project / Educational purposes - Website or blog - Web Application - Service or API - Mobile Application - Machine learning / AI / Data processing - IoT - Operational / Developer tooling  If another value for purpose is specified, for example, \\\"your custom purpose\\\", your purpose will be stored as `Other: your custom purpose`. 

##### environment: `str`<a id="environment-str"></a>

The environment of the project's resources.

##### created_at: `datetime`<a id="created_at-datetime"></a>

A time value given in ISO8601 combined date and time format that represents when the project was created.

##### updated_at: `datetime`<a id="updated_at-datetime"></a>

A time value given in ISO8601 combined date and time format that represents when the project was updated.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ProjectBase`](./digital_ocean_python_sdk/type/project_base.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/projects` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.projects.delete`<a id="digitaloceanprojectsdelete"></a>

To delete a project, send a DELETE request to `/v2/projects/$PROJECT_ID`. To
be deleted, a project must not have any resources assigned to it. Any existing
resources must first be reassigned or destroyed, or you will receive a 412 error.

A successful request will receive a 204 status code with no body in response.
This indicates that the request was processed successfully.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.projects.delete(
    project_id="4de7ac8b-495b-4884-9a69-1050c6793cd6",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_id: `str`<a id="project_id-str"></a>

A unique identifier for a project.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/projects/{project_id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.projects.get`<a id="digitaloceanprojectsget"></a>

To get a project, send a GET request to `/v2/projects/$PROJECT_ID`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_response = digitalocean.projects.get(
    project_id="4de7ac8b-495b-4884-9a69-1050c6793cd6",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_id: `str`<a id="project_id-str"></a>

A unique identifier for a project.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/projects/{project_id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.projects.get_default_project`<a id="digitaloceanprojectsget_default_project"></a>

To get your default project, send a GET request to `/v2/projects/default`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_default_project_response = digitalocean.projects.get_default_project()
```

#### 🔄 Return<a id="🔄-return"></a>

[`ProjectsGetDefaultProjectResponse`](./digital_ocean_python_sdk/pydantic/projects_get_default_project_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/projects/default` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.projects.list`<a id="digitaloceanprojectslist"></a>

To list all your projects, send a GET request to `/v2/projects`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = digitalocean.projects.list(
    per_page=2,
    page=1,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### per_page: `int`<a id="per_page-int"></a>

Number of items returned per page

##### page: `int`<a id="page-int"></a>

Which 'page' of paginated results to return.

#### 🔄 Return<a id="🔄-return"></a>

[`ProjectsListResponse`](./digital_ocean_python_sdk/pydantic/projects_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/projects` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.projects.patch`<a id="digitaloceanprojectspatch"></a>

To update only specific attributes of a project, send a PATCH request to `/v2/projects/$PROJECT_ID`. At least one of the following attributes needs to be sent.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
patch_response = digitalocean.projects.patch(
    body=None,
    project_id="4de7ac8b-495b-4884-9a69-1050c6793cd6",
    description="My website API",
    id="4e1bfbc3-dc3e-41f2-a18f-1b4d7ba71679",
    owner_uuid="99525febec065ca37b2ffe4f852fd2b2581895e7",
    owner_id=258992,
    name="my-web-api",
    purpose="Service or API",
    environment="Production",
    created_at="2018-09-27T20:10:35Z",
    updated_at="2018-09-27T20:10:35Z",
    is_default=False,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_id: `str`<a id="project_id-str"></a>

A unique identifier for a project.

##### description: `str`<a id="description-str"></a>

The description of the project. The maximum length is 255 characters.

##### id: `str`<a id="id-str"></a>

The unique universal identifier of this project.

##### owner_uuid: `str`<a id="owner_uuid-str"></a>

The unique universal identifier of the project owner.

##### owner_id: `int`<a id="owner_id-int"></a>

The integer id of the project owner.

##### name: `str`<a id="name-str"></a>

The human-readable name for the project. The maximum length is 175 characters and the name must be unique.

##### purpose: `str`<a id="purpose-str"></a>

The purpose of the project. The maximum length is 255 characters. It can have one of the following values:  - Just trying out DigitalOcean - Class project / Educational purposes - Website or blog - Web Application - Service or API - Mobile Application - Machine learning / AI / Data processing - IoT - Operational / Developer tooling  If another value for purpose is specified, for example, \\\"your custom purpose\\\", your purpose will be stored as `Other: your custom purpose`. 

##### environment: `str`<a id="environment-str"></a>

The environment of the project's resources.

##### created_at: `datetime`<a id="created_at-datetime"></a>

A time value given in ISO8601 combined date and time format that represents when the project was created.

##### updated_at: `datetime`<a id="updated_at-datetime"></a>

A time value given in ISO8601 combined date and time format that represents when the project was updated.

##### is_default: `bool`<a id="is_default-bool"></a>

If true, all resources will be added to this project if no project is specified.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`Project`](./digital_ocean_python_sdk/type/project.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/projects/{project_id}` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.projects.update`<a id="digitaloceanprojectsupdate"></a>

To update a project, send a PUT request to `/v2/projects/$PROJECT_ID`. All of the following attributes must be sent.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_response = digitalocean.projects.update(
    body=None,
    project_id="4de7ac8b-495b-4884-9a69-1050c6793cd6",
    description="My website API",
    id="4e1bfbc3-dc3e-41f2-a18f-1b4d7ba71679",
    owner_uuid="99525febec065ca37b2ffe4f852fd2b2581895e7",
    owner_id=258992,
    name="my-web-api",
    purpose="Service or API",
    environment="Production",
    created_at="2018-09-27T20:10:35Z",
    updated_at="2018-09-27T20:10:35Z",
    is_default=False,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_id: `str`<a id="project_id-str"></a>

A unique identifier for a project.

##### description: `str`<a id="description-str"></a>

The description of the project. The maximum length is 255 characters.

##### id: `str`<a id="id-str"></a>

The unique universal identifier of this project.

##### owner_uuid: `str`<a id="owner_uuid-str"></a>

The unique universal identifier of the project owner.

##### owner_id: `int`<a id="owner_id-int"></a>

The integer id of the project owner.

##### name: `str`<a id="name-str"></a>

The human-readable name for the project. The maximum length is 175 characters and the name must be unique.

##### purpose: `str`<a id="purpose-str"></a>

The purpose of the project. The maximum length is 255 characters. It can have one of the following values:  - Just trying out DigitalOcean - Class project / Educational purposes - Website or blog - Web Application - Service or API - Mobile Application - Machine learning / AI / Data processing - IoT - Operational / Developer tooling  If another value for purpose is specified, for example, \\\"your custom purpose\\\", your purpose will be stored as `Other: your custom purpose`. 

##### environment: `str`<a id="environment-str"></a>

The environment of the project's resources.

##### created_at: `datetime`<a id="created_at-datetime"></a>

A time value given in ISO8601 combined date and time format that represents when the project was created.

##### updated_at: `datetime`<a id="updated_at-datetime"></a>

A time value given in ISO8601 combined date and time format that represents when the project was updated.

##### is_default: `bool`<a id="is_default-bool"></a>

If true, all resources will be added to this project if no project is specified.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`Project`](./digital_ocean_python_sdk/type/project.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/projects/{project_id}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.projects.update_default_project`<a id="digitaloceanprojectsupdate_default_project"></a>

To update you default project, send a PUT request to `/v2/projects/default`. All of the following attributes must be sent.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_default_project_response = digitalocean.projects.update_default_project(
    body=None,
    description="My website API",
    id="4e1bfbc3-dc3e-41f2-a18f-1b4d7ba71679",
    owner_uuid="99525febec065ca37b2ffe4f852fd2b2581895e7",
    owner_id=258992,
    name="my-web-api",
    purpose="Service or API",
    environment="Production",
    created_at="2018-09-27T20:10:35Z",
    updated_at="2018-09-27T20:10:35Z",
    is_default=False,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### description: `str`<a id="description-str"></a>

The description of the project. The maximum length is 255 characters.

##### id: `str`<a id="id-str"></a>

The unique universal identifier of this project.

##### owner_uuid: `str`<a id="owner_uuid-str"></a>

The unique universal identifier of the project owner.

##### owner_id: `int`<a id="owner_id-int"></a>

The integer id of the project owner.

##### name: `str`<a id="name-str"></a>

The human-readable name for the project. The maximum length is 175 characters and the name must be unique.

##### purpose: `str`<a id="purpose-str"></a>

The purpose of the project. The maximum length is 255 characters. It can have one of the following values:  - Just trying out DigitalOcean - Class project / Educational purposes - Website or blog - Web Application - Service or API - Mobile Application - Machine learning / AI / Data processing - IoT - Operational / Developer tooling  If another value for purpose is specified, for example, \\\"your custom purpose\\\", your purpose will be stored as `Other: your custom purpose`. 

##### environment: `str`<a id="environment-str"></a>

The environment of the project's resources.

##### created_at: `datetime`<a id="created_at-datetime"></a>

A time value given in ISO8601 combined date and time format that represents when the project was created.

##### updated_at: `datetime`<a id="updated_at-datetime"></a>

A time value given in ISO8601 combined date and time format that represents when the project was updated.

##### is_default: `bool`<a id="is_default-bool"></a>

If true, all resources will be added to this project if no project is specified.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`Project`](./digital_ocean_python_sdk/type/project.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/projects/default` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.projects.update_default_project_attributes`<a id="digitaloceanprojectsupdate_default_project_attributes"></a>

To update only specific attributes of your default project, send a PATCH request to `/v2/projects/default`. At least one of the following attributes needs to be sent.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_default_project_attributes_response = digitalocean.projects.update_default_project_attributes(
    body=None,
    description="My website API",
    id="4e1bfbc3-dc3e-41f2-a18f-1b4d7ba71679",
    owner_uuid="99525febec065ca37b2ffe4f852fd2b2581895e7",
    owner_id=258992,
    name="my-web-api",
    purpose="Service or API",
    environment="Production",
    created_at="2018-09-27T20:10:35Z",
    updated_at="2018-09-27T20:10:35Z",
    is_default=False,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### description: `str`<a id="description-str"></a>

The description of the project. The maximum length is 255 characters.

##### id: `str`<a id="id-str"></a>

The unique universal identifier of this project.

##### owner_uuid: `str`<a id="owner_uuid-str"></a>

The unique universal identifier of the project owner.

##### owner_id: `int`<a id="owner_id-int"></a>

The integer id of the project owner.

##### name: `str`<a id="name-str"></a>

The human-readable name for the project. The maximum length is 175 characters and the name must be unique.

##### purpose: `str`<a id="purpose-str"></a>

The purpose of the project. The maximum length is 255 characters. It can have one of the following values:  - Just trying out DigitalOcean - Class project / Educational purposes - Website or blog - Web Application - Service or API - Mobile Application - Machine learning / AI / Data processing - IoT - Operational / Developer tooling  If another value for purpose is specified, for example, \\\"your custom purpose\\\", your purpose will be stored as `Other: your custom purpose`. 

##### environment: `str`<a id="environment-str"></a>

The environment of the project's resources.

##### created_at: `datetime`<a id="created_at-datetime"></a>

A time value given in ISO8601 combined date and time format that represents when the project was created.

##### updated_at: `datetime`<a id="updated_at-datetime"></a>

A time value given in ISO8601 combined date and time format that represents when the project was updated.

##### is_default: `bool`<a id="is_default-bool"></a>

If true, all resources will be added to this project if no project is specified.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`Project`](./digital_ocean_python_sdk/type/project.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/projects/default` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.regions.list`<a id="digitaloceanregionslist"></a>

To list all of the regions that are available, send a GET request to `/v2/regions`.
The response will be a JSON object with a key called `regions`. The value of this will be an array of `region` objects, each of which will contain the standard region attributes.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = digitalocean.regions.list(
    per_page=2,
    page=1,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### per_page: `int`<a id="per_page-int"></a>

Number of items returned per page

##### page: `int`<a id="page-int"></a>

Which 'page' of paginated results to return.

#### 🔄 Return<a id="🔄-return"></a>

[`RegionsListResponse`](./digital_ocean_python_sdk/pydantic/regions_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/regions` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.reserved_ip_actions.get`<a id="digitaloceanreserved_ip_actionsget"></a>

To retrieve the status of a reserved IP action, send a GET request to `/v2/reserved_ips/$RESERVED_IP/actions/$ACTION_ID`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_response = digitalocean.reserved_ip_actions.get(
    reserved_ip="45.55.96.47",
    action_id=36804636,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### reserved_ip: `str`<a id="reserved_ip-str"></a>

A reserved IP address.

##### action_id: `int`<a id="action_id-int"></a>

A unique numeric ID that can be used to identify and reference an action.

#### 🔄 Return<a id="🔄-return"></a>

[`ReservedIPsActionsPostResponse`](./digital_ocean_python_sdk/pydantic/reserved_ips_actions_post_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/reserved_ips/{reserved_ip}/actions/{action_id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.reserved_ip_actions.list`<a id="digitaloceanreserved_ip_actionslist"></a>

To retrieve all actions that have been executed on a reserved IP, send a GET request to `/v2/reserved_ips/$RESERVED_IP/actions`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = digitalocean.reserved_ip_actions.list(
    reserved_ip="45.55.96.47",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### reserved_ip: `str`<a id="reserved_ip-str"></a>

A reserved IP address.

#### 🔄 Return<a id="🔄-return"></a>

[`ReservedIPsActionsListResponse`](./digital_ocean_python_sdk/pydantic/reserved_ips_actions_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/reserved_ips/{reserved_ip}/actions` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.reserved_ip_actions.post`<a id="digitaloceanreserved_ip_actionspost"></a>

To initiate an action on a reserved IP send a POST request to
`/v2/reserved_ips/$RESERVED_IP/actions`. In the JSON body to the request,
set the `type` attribute to on of the supported action types:

| Action     | Details
|------------|--------
| `assign`   | Assigns a reserved IP to a Droplet
| `unassign` | Unassign a reserved IP from a Droplet


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
post_response = digitalocean.reserved_ip_actions.post(
    body=None,
    reserved_ip="45.55.96.47",
    type="assign",
    droplet_id=758604968,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### reserved_ip: `str`<a id="reserved_ip-str"></a>

A reserved IP address.

##### type: `str`<a id="type-str"></a>

The type of action to initiate for the reserved IP.

##### droplet_id: `int`<a id="droplet_id-int"></a>

The ID of the Droplet that the reserved IP will be assigned to.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ReservedIPsActionsPostRequest`](./digital_ocean_python_sdk/type/reserved_ips_actions_post_request.py)
The `type` attribute set in the request body will specify the action that will be taken on the reserved IP. 

#### 🔄 Return<a id="🔄-return"></a>

[`ReservedIPsActionsPostResponse`](./digital_ocean_python_sdk/pydantic/reserved_ips_actions_post_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/reserved_ips/{reserved_ip}/actions` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.reserved_ips.create`<a id="digitaloceanreserved_ipscreate"></a>

On creation, a reserved IP must be either assigned to a Droplet or reserved to a region.
* To create a new reserved IP assigned to a Droplet, send a POST
  request to `/v2/reserved_ips` with the `droplet_id` attribute.

* To create a new reserved IP reserved to a region, send a POST request to
  `/v2/reserved_ips` with the `region` attribute.

**Note**:  In addition to the standard rate limiting, only 12 reserved IPs may be created per 60 seconds.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_response = digitalocean.reserved_ips.create(
    body=None,
    droplet_id=2457247,
    region="nyc3",
    project_id="746c6152-2fa2-11ed-92d3-27aaa54e4988",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### droplet_id: `int`<a id="droplet_id-int"></a>

The ID of the Droplet that the reserved IP will be assigned to.

##### region: `str`<a id="region-str"></a>

The slug identifier for the region the reserved IP will be reserved to.

##### project_id: `str`<a id="project_id-str"></a>

The UUID of the project to which the reserved IP will be assigned.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ReservedIpCreate`](./digital_ocean_python_sdk/type/reserved_ip_create.py)
#### 🔄 Return<a id="🔄-return"></a>

[`ReservedIPsCreateResponse`](./digital_ocean_python_sdk/pydantic/reserved_ips_create_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/reserved_ips` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.reserved_ips.delete`<a id="digitaloceanreserved_ipsdelete"></a>

To delete a reserved IP and remove it from your account, send a DELETE request
to `/v2/reserved_ips/$RESERVED_IP_ADDR`.

A successful request will receive a 204 status code with no body in response.
This indicates that the request was processed successfully.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.reserved_ips.delete(
    reserved_ip="45.55.96.47",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### reserved_ip: `str`<a id="reserved_ip-str"></a>

A reserved IP address.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/reserved_ips/{reserved_ip}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.reserved_ips.get`<a id="digitaloceanreserved_ipsget"></a>

To show information about a reserved IP, send a GET request to `/v2/reserved_ips/$RESERVED_IP_ADDR`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_response = digitalocean.reserved_ips.get(
    reserved_ip="45.55.96.47",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### reserved_ip: `str`<a id="reserved_ip-str"></a>

A reserved IP address.

#### 🔄 Return<a id="🔄-return"></a>

[`ReservedIPsGetResponse`](./digital_ocean_python_sdk/pydantic/reserved_ips_get_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/reserved_ips/{reserved_ip}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.reserved_ips.list`<a id="digitaloceanreserved_ipslist"></a>

To list all of the reserved IPs available on your account, send a GET request to `/v2/reserved_ips`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = digitalocean.reserved_ips.list(
    per_page=2,
    page=1,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### per_page: `int`<a id="per_page-int"></a>

Number of items returned per page

##### page: `int`<a id="page-int"></a>

Which 'page' of paginated results to return.

#### 🔄 Return<a id="🔄-return"></a>

[`ReservedIPsListResponse`](./digital_ocean_python_sdk/pydantic/reserved_ips_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/reserved_ips` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.ssh_keys.create`<a id="digitaloceanssh_keyscreate"></a>

To add a new SSH public key to your DigitalOcean account, send a POST request to `/v2/account/keys`. Set the `name` attribute to the name you wish to use and the `public_key` attribute to the full public key you are adding.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_response = digitalocean.ssh_keys.create(
    public_key="ssh-rsa AEXAMPLEaC1yc2EAAAADAQABAAAAQQDDHr/jh2Jy4yALcK4JyWbVkPRaWmhck3IgCoeOO3z1e2dBowLh64QAM+Qb72pxekALga2oi4GvT+TlWNhzPH4V example",
    name="My SSH Public Key",
    id=512189,
    fingerprint="3b:16:bf:e4:8b:00:8b:b8:59:8c:a9:d3:f0:19:45:fa",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### public_key: `str`<a id="public_key-str"></a>

The entire public key string that was uploaded. Embedded into the root user's `authorized_keys` file if you include this key during Droplet creation.

##### name: `str`<a id="name-str"></a>

A human-readable display name for this key, used to easily identify the SSH keys when they are displayed.

##### id: `int`<a id="id-int"></a>

A unique identification number for this key. Can be used to embed a  specific SSH key into a Droplet.

##### fingerprint: `str`<a id="fingerprint-str"></a>

A unique identifier that differentiates this key from other keys using  a format that SSH recognizes. The fingerprint is created when the key is added to your account.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`SshKeys`](./digital_ocean_python_sdk/type/ssh_keys.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/account/keys` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.ssh_keys.delete`<a id="digitaloceanssh_keysdelete"></a>

To destroy a public SSH key that you have in your account, send a DELETE request to `/v2/account/keys/$KEY_ID` or `/v2/account/keys/$KEY_FINGERPRINT`.
A 204 status will be returned, indicating that the action was successful and that the response body is empty.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.ssh_keys.delete(
    ssh_key_identifier=512189,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### ssh_key_identifier: Union[`int`, `str`]<a id="ssh_key_identifier-unionint-str"></a>


Either the ID or the fingerprint of an existing SSH key.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/account/keys/{ssh_key_identifier}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.ssh_keys.get`<a id="digitaloceanssh_keysget"></a>

To get information about a key, send a GET request to `/v2/account/keys/$KEY_ID` or `/v2/account/keys/$KEY_FINGERPRINT`.
The response will be a JSON object with the key `ssh_key` and value an ssh_key object which contains the standard ssh_key attributes.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_response = digitalocean.ssh_keys.get(
    ssh_key_identifier=512189,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### ssh_key_identifier: Union[`int`, `str`]<a id="ssh_key_identifier-unionint-str"></a>


Either the ID or the fingerprint of an existing SSH key.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/account/keys/{ssh_key_identifier}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.ssh_keys.list`<a id="digitaloceanssh_keyslist"></a>

To list all of the keys in your account, send a GET request to `/v2/account/keys`. The response will be a JSON object with a key set to `ssh_keys`. The value of this will be an array of ssh_key objects, each of which contains the standard ssh_key attributes.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = digitalocean.ssh_keys.list(
    per_page=2,
    page=1,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### per_page: `int`<a id="per_page-int"></a>

Number of items returned per page

##### page: `int`<a id="page-int"></a>

Which 'page' of paginated results to return.

#### 🔄 Return<a id="🔄-return"></a>

[`SshKeysListResponse`](./digital_ocean_python_sdk/pydantic/ssh_keys_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/account/keys` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.ssh_keys.update`<a id="digitaloceanssh_keysupdate"></a>

To update the name of an SSH key, send a PUT request to either `/v2/account/keys/$SSH_KEY_ID` or `/v2/account/keys/$SSH_KEY_FINGERPRINT`. Set the `name` attribute to the new name you want to use.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_response = digitalocean.ssh_keys.update(
    ssh_key_identifier=512189,
    name="My SSH Public Key",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### ssh_key_identifier: Union[`int`, `str`]<a id="ssh_key_identifier-unionint-str"></a>


Either the ID or the fingerprint of an existing SSH key.

##### name: `str`<a id="name-str"></a>

A human-readable display name for this key, used to easily identify the SSH keys when they are displayed.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`SshKeysUpdateRequest`](./digital_ocean_python_sdk/type/ssh_keys_update_request.py)
Set the `name` attribute to the new name you want to use.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/account/keys/{ssh_key_identifier}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.sizes.list`<a id="digitaloceansizeslist"></a>

To list all of available Droplet sizes, send a GET request to `/v2/sizes`.
The response will be a JSON object with a key called `sizes`. The value of this will be an array of `size` objects each of which contain the standard size attributes.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = digitalocean.sizes.list(
    per_page=2,
    page=1,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### per_page: `int`<a id="per_page-int"></a>

Number of items returned per page

##### page: `int`<a id="page-int"></a>

Which 'page' of paginated results to return.

#### 🔄 Return<a id="🔄-return"></a>

[`SizesListResponse`](./digital_ocean_python_sdk/pydantic/sizes_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/sizes` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.snapshots.delete`<a id="digitaloceansnapshotsdelete"></a>

Both Droplet and volume snapshots are managed through the `/v2/snapshots/`
endpoint. To delete a snapshot, send a DELETE request to
`/v2/snapshots/$SNAPSHOT_ID`.

A status of 204 will be given. This indicates that the request was processed
successfully, but that no response body is needed.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.snapshots.delete(
    snapshot_id=6372321,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### snapshot_id: Union[`int`, `str`]<a id="snapshot_id-unionint-str"></a>


Either the ID of an existing snapshot. This will be an integer for a Droplet snapshot or a string for a volume snapshot.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/snapshots/{snapshot_id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.snapshots.get`<a id="digitaloceansnapshotsget"></a>

To retrieve information about a snapshot, send a GET request to
`/v2/snapshots/$SNAPSHOT_ID`.

The response will be a JSON object with a key called `snapshot`. The value of
this will be an snapshot object containing the standard snapshot attributes.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_response = digitalocean.snapshots.get(
    snapshot_id=6372321,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### snapshot_id: Union[`int`, `str`]<a id="snapshot_id-unionint-str"></a>


Either the ID of an existing snapshot. This will be an integer for a Droplet snapshot or a string for a volume snapshot.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/snapshots/{snapshot_id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.snapshots.list`<a id="digitaloceansnapshotslist"></a>

To list all of the snapshots available on your account, send a GET request to
`/v2/snapshots`.

The response will be a JSON object with a key called `snapshots`. This will be
set to an array of `snapshot` objects, each of which will contain the standard
snapshot attributes.

### Filtering Results by Resource Type<a id="filtering-results-by-resource-type"></a>

It's possible to request filtered results by including certain query parameters.

#### List Droplet Snapshots<a id="list-droplet-snapshots"></a>

To retrieve only snapshots based on Droplets, include the `resource_type`
query parameter set to `droplet`. For example, `/v2/snapshots?resource_type=droplet`.

#### List Volume Snapshots<a id="list-volume-snapshots"></a>

To retrieve only snapshots based on volumes, include the `resource_type`
query parameter set to `volume`. For example, `/v2/snapshots?resource_type=volume`.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = digitalocean.snapshots.list(
    per_page=2,
    page=1,
    resource_type="droplet",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### per_page: `int`<a id="per_page-int"></a>

Number of items returned per page

##### page: `int`<a id="page-int"></a>

Which 'page' of paginated results to return.

##### resource_type: `str`<a id="resource_type-str"></a>

Used to filter snapshots by a resource type.

#### 🔄 Return<a id="🔄-return"></a>

[`SnapshotsListResponse`](./digital_ocean_python_sdk/pydantic/snapshots_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/snapshots` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.tags.create`<a id="digitaloceantagscreate"></a>

To create a tag you can send a POST request to `/v2/tags` with a `name` attribute.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_response = digitalocean.tags.create(
    name="extra-awesome",
    resources={},
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### name: `str`<a id="name-str"></a>

The name of the tag. Tags may contain letters, numbers, colons, dashes, and underscores. There is a limit of 255 characters per tag.  **Note:** Tag names are case stable, which means the capitalization you use when you first create a tag is canonical.  When working with tags in the API, you must use the tag's canonical capitalization. For example, if you create a tag named \\\"PROD\\\", the URL to add that tag to a resource would be `https://api.digitalocean.com/v2/tags/PROD/resources` (not `/v2/tags/prod/resources`).  Tagged resources in the control panel will always display the canonical capitalization. For example, if you create a tag named \\\"PROD\\\", you can tag resources in the control panel by entering \\\"prod\\\". The tag will still display with its canonical capitalization, \\\"PROD\\\". 

##### resources: [`TagsResources`](./digital_ocean_python_sdk/type/tags_resources.py)<a id="resources-tagsresourcesdigital_ocean_python_sdktypetags_resourcespy"></a>


#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`Tags`](./digital_ocean_python_sdk/type/tags.py)
#### 🔄 Return<a id="🔄-return"></a>

[`TagsCreateResponse`](./digital_ocean_python_sdk/pydantic/tags_create_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/tags` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.tags.delete`<a id="digitaloceantagsdelete"></a>

A tag can be deleted by sending a `DELETE` request to `/v2/tags/$TAG_NAME`. Deleting a tag also untags all the resources that have previously been tagged by the Tag

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.tags.delete(
    tag_id="awesome",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### tag_id: `str`<a id="tag_id-str"></a>

The name of the tag. Tags may contain letters, numbers, colons, dashes, and underscores. There is a limit of 255 characters per tag.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/tags/{tag_id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.tags.get`<a id="digitaloceantagsget"></a>

To retrieve an individual tag, you can send a `GET` request to `/v2/tags/$TAG_NAME`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_response = digitalocean.tags.get(
    tag_id="awesome",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### tag_id: `str`<a id="tag_id-str"></a>

The name of the tag. Tags may contain letters, numbers, colons, dashes, and underscores. There is a limit of 255 characters per tag.

#### 🔄 Return<a id="🔄-return"></a>

[`TagsGetResponse`](./digital_ocean_python_sdk/pydantic/tags_get_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/tags/{tag_id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.tags.list`<a id="digitaloceantagslist"></a>

To list all of your tags, you can send a GET request to `/v2/tags`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = digitalocean.tags.list(
    per_page=2,
    page=1,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### per_page: `int`<a id="per_page-int"></a>

Number of items returned per page

##### page: `int`<a id="page-int"></a>

Which 'page' of paginated results to return.

#### 🔄 Return<a id="🔄-return"></a>

[`TagsListResponse`](./digital_ocean_python_sdk/pydantic/tags_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/tags` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.tags.tag_resource`<a id="digitaloceantagstag_resource"></a>

Resources can be tagged by sending a POST request to `/v2/tags/$TAG_NAME/resources` with an array of json objects containing `resource_id` and `resource_type` attributes.
Currently only tagging of Droplets, Databases, Images, Volumes, and Volume Snapshots is supported. `resource_type` is expected to be the string `droplet`, `database`, `image`, `volume` or `volume_snapshot`. `resource_id` is expected to be the ID of the resource as a string.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.tags.tag_resource(
    resources=[None, None, None],
    tag_id="awesome",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### resources: [`TagsResourceResources`](./digital_ocean_python_sdk/type/tags_resource_resources.py)<a id="resources-tagsresourceresourcesdigital_ocean_python_sdktypetags_resource_resourcespy"></a>

##### tag_id: `str`<a id="tag_id-str"></a>

The name of the tag. Tags may contain letters, numbers, colons, dashes, and underscores. There is a limit of 255 characters per tag.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`TagsResource`](./digital_ocean_python_sdk/type/tags_resource.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/tags/{tag_id}/resources` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.tags.untag_resource`<a id="digitaloceantagsuntag_resource"></a>

Resources can be untagged by sending a DELETE request to `/v2/tags/$TAG_NAME/resources` with an array of json objects containing `resource_id` and `resource_type` attributes.
Currently only untagging of Droplets, Databases, Images, Volumes, and Volume Snapshots is supported. `resource_type` is expected to be the string `droplet`, `database`, `image`, `volume` or `volume_snapshot`. `resource_id` is expected to be the ID of the resource as a string.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.tags.untag_resource(
    resources=[None, None, None],
    tag_id="awesome",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### resources: [`TagsResourceResources`](./digital_ocean_python_sdk/type/tags_resource_resources.py)<a id="resources-tagsresourceresourcesdigital_ocean_python_sdktypetags_resource_resourcespy"></a>

##### tag_id: `str`<a id="tag_id-str"></a>

The name of the tag. Tags may contain letters, numbers, colons, dashes, and underscores. There is a limit of 255 characters per tag.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`TagsResource`](./digital_ocean_python_sdk/type/tags_resource.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/tags/{tag_id}/resources` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.uptime.create_check`<a id="digitaloceanuptimecreate_check"></a>

To create an Uptime check, send a POST request to `/v2/uptime/checks` specifying the attributes
in the table below in the JSON body.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_check_response = digitalocean.uptime.create_check(
    name="Landing page check",
    type="https",
    target="https://www.landingpage.com",
    regions=["us_east", "eu_west"],
    enabled=True,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### name: `str`<a id="name-str"></a>

A human-friendly display name.

##### type: `str`<a id="type-str"></a>

The type of health check to perform.

##### target: `str`<a id="target-str"></a>

The endpoint to perform healthchecks on.

##### regions: [`CheckUpdatableRegions`](./digital_ocean_python_sdk/type/check_updatable_regions.py)<a id="regions-checkupdatableregionsdigital_ocean_python_sdktypecheck_updatable_regionspy"></a>

##### enabled: `bool`<a id="enabled-bool"></a>

A boolean value indicating whether the check is enabled/disabled.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`CheckUpdatable`](./digital_ocean_python_sdk/type/check_updatable.py)
#### 🔄 Return<a id="🔄-return"></a>

[`UptimeCreateCheckResponse`](./digital_ocean_python_sdk/pydantic/uptime_create_check_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/uptime/checks` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.uptime.create_new_alert`<a id="digitaloceanuptimecreate_new_alert"></a>

To create an Uptime alert, send a POST request to `/v2/uptime/checks/$CHECK_ID/alerts` specifying the attributes
in the table below in the JSON body.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_new_alert_response = digitalocean.uptime.create_new_alert(
    check_id="4de7ac8b-495b-4884-9a69-1050c6793cd6",
    id="5a4981aa-9653-4bd1-bef5-d6bff52042e4",
    name="Landing page degraded performance",
    type="latency",
    threshold=300,
    comparison="greater_than",
    notifications={
        "email": ["bob@example.com"],
        "slack": [
            {
                "channel": "Production Alerts",
                "url": "https://hooks.slack.com/services/T1234567/AAAAAAAA/ZZZZZZ",
            }
        ],
    },
    period="2m",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### check_id: `str`<a id="check_id-str"></a>

A unique identifier for a check.

##### id: `str`<a id="id-str"></a>

A unique ID that can be used to identify and reference the alert.

##### name: `str`<a id="name-str"></a>

A human-friendly display name.

##### type: `str`<a id="type-str"></a>

The type of alert.

##### threshold: `int`<a id="threshold-int"></a>

The threshold at which the alert will enter a trigger state. The specific threshold is dependent on the alert type.

##### comparison: `str`<a id="comparison-str"></a>

The comparison operator used against the alert's threshold.

##### notifications: [`Notification`](./digital_ocean_python_sdk/type/notification.py)<a id="notifications-notificationdigital_ocean_python_sdktypenotificationpy"></a>


##### period: `str`<a id="period-str"></a>

Period of time the threshold must be exceeded to trigger the alert.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`Alert`](./digital_ocean_python_sdk/type/alert.py)
The ''type'' field dictates the type of alert, and hence what type of value to pass into the threshold property. Type | Description | Threshold Value -----|-------------|-------------------- `latency` | alerts on the response latency | milliseconds `down` | alerts on a target registering as down in any region | N/A (Not required) `down_global` | alerts on a target registering as down globally | N/A (Not required) `ssl_expiry` | alerts on a SSL certificate expiring within $threshold days | days 

#### 🔄 Return<a id="🔄-return"></a>

[`UptimeCreateNewAlertResponse`](./digital_ocean_python_sdk/pydantic/uptime_create_new_alert_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/uptime/checks/{check_id}/alerts` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.uptime.delete_alert`<a id="digitaloceanuptimedelete_alert"></a>

To delete an Uptime alert, send a DELETE request to `/v2/uptime/checks/$CHECK_ID/alerts/$ALERT_ID`. A 204 status
code with no body will be returned in response to a successful request.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.uptime.delete_alert(
    check_id="4de7ac8b-495b-4884-9a69-1050c6793cd6",
    alert_id="17f0f0ae-b7e5-4ef6-86e3-aa569db58284",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### check_id: `str`<a id="check_id-str"></a>

A unique identifier for a check.

##### alert_id: `str`<a id="alert_id-str"></a>

A unique identifier for an alert.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/uptime/checks/{check_id}/alerts/{alert_id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.uptime.delete_check`<a id="digitaloceanuptimedelete_check"></a>

To delete an Uptime check, send a DELETE request to `/v2/uptime/checks/$CHECK_ID`. A 204 status
code with no body will be returned in response to a successful request.


Deleting a check will also delete alerts associated with the check.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.uptime.delete_check(
    check_id="4de7ac8b-495b-4884-9a69-1050c6793cd6",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### check_id: `str`<a id="check_id-str"></a>

A unique identifier for a check.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/uptime/checks/{check_id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.uptime.get_check_by_id`<a id="digitaloceanuptimeget_check_by_id"></a>

To show information about an existing check, send a GET request to `/v2/uptime/checks/$CHECK_ID`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_check_by_id_response = digitalocean.uptime.get_check_by_id(
    check_id="4de7ac8b-495b-4884-9a69-1050c6793cd6",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### check_id: `str`<a id="check_id-str"></a>

A unique identifier for a check.

#### 🔄 Return<a id="🔄-return"></a>

[`UptimeCreateCheckResponse`](./digital_ocean_python_sdk/pydantic/uptime_create_check_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/uptime/checks/{check_id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.uptime.get_check_state`<a id="digitaloceanuptimeget_check_state"></a>

To show information about an existing check's state, send a GET request to `/v2/uptime/checks/$CHECK_ID/state`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_check_state_response = digitalocean.uptime.get_check_state(
    check_id="4de7ac8b-495b-4884-9a69-1050c6793cd6",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### check_id: `str`<a id="check_id-str"></a>

A unique identifier for a check.

#### 🔄 Return<a id="🔄-return"></a>

[`UptimeGetCheckStateResponse`](./digital_ocean_python_sdk/pydantic/uptime_get_check_state_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/uptime/checks/{check_id}/state` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.uptime.get_existing_alert`<a id="digitaloceanuptimeget_existing_alert"></a>

To show information about an existing alert, send a GET request to `/v2/uptime/checks/$CHECK_ID/alerts/$ALERT_ID`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_existing_alert_response = digitalocean.uptime.get_existing_alert(
    check_id="4de7ac8b-495b-4884-9a69-1050c6793cd6",
    alert_id="17f0f0ae-b7e5-4ef6-86e3-aa569db58284",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### check_id: `str`<a id="check_id-str"></a>

A unique identifier for a check.

##### alert_id: `str`<a id="alert_id-str"></a>

A unique identifier for an alert.

#### 🔄 Return<a id="🔄-return"></a>

[`UptimeCreateNewAlertResponse`](./digital_ocean_python_sdk/pydantic/uptime_create_new_alert_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/uptime/checks/{check_id}/alerts/{alert_id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.uptime.list_all_alerts`<a id="digitaloceanuptimelist_all_alerts"></a>

To list all of the alerts for an Uptime check, send a GET request to `/v2/uptime/checks/$CHECK_ID/alerts`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_all_alerts_response = digitalocean.uptime.list_all_alerts(
    check_id="4de7ac8b-495b-4884-9a69-1050c6793cd6",
    per_page=2,
    page=1,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### check_id: `str`<a id="check_id-str"></a>

A unique identifier for a check.

##### per_page: `int`<a id="per_page-int"></a>

Number of items returned per page

##### page: `int`<a id="page-int"></a>

Which 'page' of paginated results to return.

#### 🔄 Return<a id="🔄-return"></a>

[`UptimeListAllAlertsResponse`](./digital_ocean_python_sdk/pydantic/uptime_list_all_alerts_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/uptime/checks/{check_id}/alerts` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.uptime.list_checks`<a id="digitaloceanuptimelist_checks"></a>

To list all of the Uptime checks on your account, send a GET request to `/v2/uptime/checks`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_checks_response = digitalocean.uptime.list_checks(
    per_page=2,
    page=1,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### per_page: `int`<a id="per_page-int"></a>

Number of items returned per page

##### page: `int`<a id="page-int"></a>

Which 'page' of paginated results to return.

#### 🔄 Return<a id="🔄-return"></a>

[`UptimeListChecksResponse`](./digital_ocean_python_sdk/pydantic/uptime_list_checks_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/uptime/checks` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.uptime.update_alert_settings`<a id="digitaloceanuptimeupdate_alert_settings"></a>

To update the settings of an Uptime alert, send a PUT request to `/v2/uptime/checks/$CHECK_ID/alerts/$ALERT_ID`.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_alert_settings_response = digitalocean.uptime.update_alert_settings(
    check_id="4de7ac8b-495b-4884-9a69-1050c6793cd6",
    alert_id="17f0f0ae-b7e5-4ef6-86e3-aa569db58284",
    name="Landing page degraded performance",
    type="latency",
    threshold=300,
    comparison="greater_than",
    notifications={
        "email": ["bob@example.com"],
        "slack": [
            {
                "channel": "Production Alerts",
                "url": "https://hooks.slack.com/services/T1234567/AAAAAAAA/ZZZZZZ",
            }
        ],
    },
    period="2m",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### check_id: `str`<a id="check_id-str"></a>

A unique identifier for a check.

##### alert_id: `str`<a id="alert_id-str"></a>

A unique identifier for an alert.

##### name: `str`<a id="name-str"></a>

A human-friendly display name.

##### type: `str`<a id="type-str"></a>

The type of alert.

##### threshold: `int`<a id="threshold-int"></a>

The threshold at which the alert will enter a trigger state. The specific threshold is dependent on the alert type.

##### comparison: `str`<a id="comparison-str"></a>

The comparison operator used against the alert's threshold.

##### notifications: [`Notification`](./digital_ocean_python_sdk/type/notification.py)<a id="notifications-notificationdigital_ocean_python_sdktypenotificationpy"></a>


##### period: `str`<a id="period-str"></a>

Period of time the threshold must be exceeded to trigger the alert.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`AlertUpdatable`](./digital_ocean_python_sdk/type/alert_updatable.py)
#### 🔄 Return<a id="🔄-return"></a>

[`UptimeCreateNewAlertResponse`](./digital_ocean_python_sdk/pydantic/uptime_create_new_alert_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/uptime/checks/{check_id}/alerts/{alert_id}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.uptime.update_check_settings`<a id="digitaloceanuptimeupdate_check_settings"></a>

To update the settings of an Uptime check, send a PUT request to `/v2/uptime/checks/$CHECK_ID`.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_check_settings_response = digitalocean.uptime.update_check_settings(
    check_id="4de7ac8b-495b-4884-9a69-1050c6793cd6",
    name="Landing page check",
    type="https",
    target="https://www.landingpage.com",
    regions=["us_east", "eu_west"],
    enabled=True,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### check_id: `str`<a id="check_id-str"></a>

A unique identifier for a check.

##### name: `str`<a id="name-str"></a>

A human-friendly display name.

##### type: `str`<a id="type-str"></a>

The type of health check to perform.

##### target: `str`<a id="target-str"></a>

The endpoint to perform healthchecks on.

##### regions: [`CheckUpdatableRegions`](./digital_ocean_python_sdk/type/check_updatable_regions.py)<a id="regions-checkupdatableregionsdigital_ocean_python_sdktypecheck_updatable_regionspy"></a>

##### enabled: `bool`<a id="enabled-bool"></a>

A boolean value indicating whether the check is enabled/disabled.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`CheckUpdatable`](./digital_ocean_python_sdk/type/check_updatable.py)
#### 🔄 Return<a id="🔄-return"></a>

[`UptimeCreateCheckResponse`](./digital_ocean_python_sdk/pydantic/uptime_create_check_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/uptime/checks/{check_id}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.vpcs.create`<a id="digitaloceanvpcscreate"></a>

To create a VPC, send a POST request to `/v2/vpcs` specifying the attributes
in the table below in the JSON body.

**Note:** If you do not currently have a VPC network in a specific datacenter
region, the first one that you create will be set as the default for that
region. The default VPC for a region cannot be changed or deleted.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_response = digitalocean.vpcs.create(
    name="env.prod-vpc",
    region="nyc1",
    description="VPC for production environment",
    ip_range="10.10.10.0/24",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### name: `str`<a id="name-str"></a>

The name of the VPC. Must be unique and may only contain alphanumeric characters, dashes, and periods.

##### region: `str`<a id="region-str"></a>

The slug identifier for the region where the VPC will be created.

##### description: `str`<a id="description-str"></a>

A free-form text field for describing the VPC's purpose. It may be a maximum of 255 characters.

##### ip_range: `str`<a id="ip_range-str"></a>

The range of IP addresses in the VPC in CIDR notation. Network ranges cannot overlap with other networks in the same account and must be in range of private addresses as defined in RFC1918. It may not be smaller than `/28` nor larger than `/16`. If no IP range is specified, a `/20` network range is generated that won't conflict with other VPC networks in your account.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`VpcsCreateRequest`](./digital_ocean_python_sdk/type/vpcs_create_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`VpcsCreateResponse`](./digital_ocean_python_sdk/pydantic/vpcs_create_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/vpcs` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.vpcs.delete`<a id="digitaloceanvpcsdelete"></a>

To delete a VPC, send a DELETE request to `/v2/vpcs/$VPC_ID`. A 204 status
code with no body will be returned in response to a successful request.

The default VPC for a region can not be deleted. Additionally, a VPC can only
be deleted if it does not contain any member resources. Attempting to delete
a region's default VPC or a VPC that still has members will result in a
403 Forbidden error response.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
digitalocean.vpcs.delete(
    vpc_id="4de7ac8b-495b-4884-9a69-1050c6793cd6",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### vpc_id: `str`<a id="vpc_id-str"></a>

A unique identifier for a VPC.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/vpcs/{vpc_id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.vpcs.get`<a id="digitaloceanvpcsget"></a>

To show information about an existing VPC, send a GET request to `/v2/vpcs/$VPC_ID`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_response = digitalocean.vpcs.get(
    vpc_id="4de7ac8b-495b-4884-9a69-1050c6793cd6",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### vpc_id: `str`<a id="vpc_id-str"></a>

A unique identifier for a VPC.

#### 🔄 Return<a id="🔄-return"></a>

[`VpcsCreateResponse`](./digital_ocean_python_sdk/pydantic/vpcs_create_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/vpcs/{vpc_id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.vpcs.list`<a id="digitaloceanvpcslist"></a>

To list all of the VPCs on your account, send a GET request to `/v2/vpcs`.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = digitalocean.vpcs.list(
    per_page=2,
    page=1,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### per_page: `int`<a id="per_page-int"></a>

Number of items returned per page

##### page: `int`<a id="page-int"></a>

Which 'page' of paginated results to return.

#### 🔄 Return<a id="🔄-return"></a>

[`VpcsListResponse`](./digital_ocean_python_sdk/pydantic/vpcs_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/vpcs` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.vpcs.list_members`<a id="digitaloceanvpcslist_members"></a>

To list all of the resources that are members of a VPC, send a GET request to
`/v2/vpcs/$VPC_ID/members`.

To only list resources of a specific type that are members of the VPC,
included a `resource_type` query parameter. For example, to only list Droplets
in the VPC, send a GET request to `/v2/vpcs/$VPC_ID/members?resource_type=droplet`.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_members_response = digitalocean.vpcs.list_members(
    vpc_id="4de7ac8b-495b-4884-9a69-1050c6793cd6",
    resource_type="droplet",
    per_page=2,
    page=1,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### vpc_id: `str`<a id="vpc_id-str"></a>

A unique identifier for a VPC.

##### resource_type: `str`<a id="resource_type-str"></a>

Used to filter VPC members by a resource type.

##### per_page: `int`<a id="per_page-int"></a>

Number of items returned per page

##### page: `int`<a id="page-int"></a>

Which 'page' of paginated results to return.

#### 🔄 Return<a id="🔄-return"></a>

[`VpCsListMembersResponse`](./digital_ocean_python_sdk/pydantic/vp_cs_list_members_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/vpcs/{vpc_id}/members` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.vpcs.patch`<a id="digitaloceanvpcspatch"></a>

To update a subset of information about a VPC, send a PATCH request to
`/v2/vpcs/$VPC_ID`.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
patch_response = digitalocean.vpcs.patch(
    body=None,
    vpc_id="4de7ac8b-495b-4884-9a69-1050c6793cd6",
    description="VPC for production environment",
    name="env.prod-vpc",
    default=True,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### vpc_id: `str`<a id="vpc_id-str"></a>

A unique identifier for a VPC.

##### description: `str`<a id="description-str"></a>

A free-form text field for describing the VPC's purpose. It may be a maximum of 255 characters.

##### name: `str`<a id="name-str"></a>

The name of the VPC. Must be unique and may only contain alphanumeric characters, dashes, and periods.

##### default: `bool`<a id="default-bool"></a>

A boolean value indicating whether or not the VPC is the default network for the region. All applicable resources are placed into the default VPC network unless otherwise specified during their creation. The `default` field cannot be unset from `true`. If you want to set a new default VPC network, update the `default` field of another VPC network in the same region. The previous network's `default` field will be set to `false` when a new default VPC has been defined.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`VpcsPatchRequest`](./digital_ocean_python_sdk/type/vpcs_patch_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`VpcsCreateResponse`](./digital_ocean_python_sdk/pydantic/vpcs_create_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/vpcs/{vpc_id}` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `digitalocean.vpcs.update`<a id="digitaloceanvpcsupdate"></a>

To update information about a VPC, send a PUT request to `/v2/vpcs/$VPC_ID`.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_response = digitalocean.vpcs.update(
    name="env.prod-vpc",
    vpc_id="4de7ac8b-495b-4884-9a69-1050c6793cd6",
    description="VPC for production environment",
    default=True,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### name: `str`<a id="name-str"></a>

The name of the VPC. Must be unique and may only contain alphanumeric characters, dashes, and periods.

##### vpc_id: `str`<a id="vpc_id-str"></a>

A unique identifier for a VPC.

##### description: `str`<a id="description-str"></a>

A free-form text field for describing the VPC's purpose. It may be a maximum of 255 characters.

##### default: `bool`<a id="default-bool"></a>

A boolean value indicating whether or not the VPC is the default network for the region. All applicable resources are placed into the default VPC network unless otherwise specified during their creation. The `default` field cannot be unset from `true`. If you want to set a new default VPC network, update the `default` field of another VPC network in the same region. The previous network's `default` field will be set to `false` when a new default VPC has been defined.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`VpcsUpdateRequest`](./digital_ocean_python_sdk/type/vpcs_update_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`VpcsCreateResponse`](./digital_ocean_python_sdk/pydantic/vpcs_create_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/v2/vpcs/{vpc_id}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---


## Author<a id="author"></a>
This Python package is automatically generated by [Konfig](https://konfigthis.com)
