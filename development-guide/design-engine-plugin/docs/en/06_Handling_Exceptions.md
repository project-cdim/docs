# 6. Handling Exceptions

This chapter explains how to implement exception handling in plugins.  
Errors that occur during plugin execution must be returned by setting error information in `PluginProcessException`, or in a class that inherits from this exception.  
The error information is used as the error payload returned to the upper module that invoked the Layout Design function.  
The only exception class provided by the Layout Design function is `PluginProcessException`.

## 6.1. Exception Class Structure

The exception class `PluginProcessException` used by the Layout Design function is defined in the package `src.common.exceptions` of the Layout Design.

```python
class PluginProcessException(Exception):
```

This exception class inherits from Python’s built‑in `Exception`.  
You can use this exception class with the following import statement.

```python
from common.exceptions import PluginProcessException
```

### Attributes

- `message: str`  
    - Error message used in the HTTP response body returned by the Layout Design function.
    - There is no particular formatting requirement for the error message.

- `status_code: int`  
    - HTTP status code used in the HTTP response from the Layout Design function when an error occurs.
    - The default value is `500` (Internal Server Error).

### Methods

- `__init__(self, message, status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value)`  
    - Constructor for this exception class.
    - `HTTPStatus`, used for the default of `status_code`, is a class defined in Python’s built‑in `http` module.

### HTTP Status Codes

The HTTP status code returned to the Layout Design function should be set to 4XX or 5XX according to the plugin’s requirements.
Below are example HTTP statuses and their guidelines. These are reference examples; feel free to choose or extend them as needed.

| HTTP Status Code | Summary | Guideline |
| --- | --- | --- |
| 400 | Bad Request | When the input information is invalid |
| 404 | Not Found | When the specified design ID does not exist |
| 409 | Conflict | When the design state cannot transition in response to a layout design cancel request |
| 500 | Internal Server Error | When an error occurs in plugin or design engine processing, or when another component encounters an error |

## 6.2. Adding Exceptions

If you need exception classes other than `PluginProcessException` when implementing the plugin, add new exception classes within your plugin module.  
When adding exception classes, make them inherit from `PluginProcessException`.
