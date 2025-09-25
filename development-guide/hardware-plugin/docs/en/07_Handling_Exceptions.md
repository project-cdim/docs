# 7. Handling Exceptions

Errors that occur while running the plugin need to be set in a class that inherits from `BaseHWControlError` and returned with error information.  
This error information is often used as the error information returned to the upper module that calls the HW control functions.  
Check the various HW Control Errors and use the one that is most suitable for the error situation.  

This chapter will cover the following topics.

* [7.1. Structure of Exception Classes](#71-structure-of-exception-classes): The structure of exception classes raised by the HW control functions during abnormalities.
* [7.2. Defined Exceptions](#72-defined-exceptions): A list of exception classes defined for abnormalities occurring in plugins.
* [7.3. Adding Exceptions](#73-adding-exceptions): How to create new exception classes in plugins.

Currently, there are parts for which the specifications are being formulated regarding exception handling, and there may be incompatible updates in future releases.

## 7.1. Structure of Exception Classes

Exceptions used in HW control functions are defined in the `app.common.basic_exceptions` package of the HW control function.  
Exceptions used in HW control functions are derived from the classes defined below.  

### Base Exception Class

```python
class BaseHWControlError(Exception):
```

This exception class inherits from the built-in `Exception` class in Python.  
This exception class has the following attributes:  

* `http_code(int)`
  * The HTTP status code used in the HTTP response during an error.
* `error_code(str)`
  * The error code used in the body of the HTTP response during an error.
  * For more details, please refer to [Error Codes](#error-codes).
* `default_error_message(str)`
  * Default error message set for the exception class.
* `message(str)`
  * The error message used in the body of the HTTP response during an error.

This exception class has the following method:

* `__init__(*args: object, additional_message: str = "")`
  * Constructor for this exception class.
  * Arguments:
    * `args(object)`: Passed to the base class constructor as error information output in the traceback.
    * `additional_message(str)`: Combined with `default_error_message` as an additional error message. The concatenated message can be referenced via `message`.

### Error Codes

The error code is a string consisting of information that identifies an error, composed of a total of 11 characters from the following elements:

| Setting Item | Position | Description |
|--------------|----------|-------------|
| Error Level | 1 | 'C': A critical fault has occurred, making it difficult to continue the service of the HW control function.<br>'E': A fault has occurred, but the HW control function service can continue. |
| Retry Possibility | 2 | 'F': The same request will not succeed again.<br>'R': There is a possibility that the same request will succeed again (due to resource shortages or conflicts, etc.). |
| Base Exception Class Code | 3-5 | A string representing a 3-digit decimal notation, largely classifying the content of the error. For specific types, please refer to [Base Exception Classes](#base-exception-classes). |
| Vendor-dependent Extended Exception Class Code | 6-8 | A 3-letter uppercase alphabet used to identify error codes added in plugins. Exceptions defined in HW control functions are "BAS". Ensure that each plugin uses a string that does not overlap with other plugins.<br>For adding exceptions in plugins, please refer to [7.3 Adding Exceptions](#73-adding-exceptions). |
| Detailed Exception Class Code | 9-11 | A 3-digit decimal notation string used to identify exceptions within the same base exception class/vendor-dependent extended exception class. |

### Base Exception Classes

The base exception class is a basic exception categorized by error codes, inheriting from the fundamental exception class.  
The following are defined.

* `UnknownHWControlError`
  * Please raise this exception when an unknown critical error occurs. For example, cases where continuing the process could lead to hardware destruction are assumed.
  * Base Exception Class Code:`"001"`
  * Error Code: `"CF001BAS000"`
  * HTTP Status Code: `500`
  * Default Error Message: `"The server encountered an internal error and was unable to complete your request."`

* `AuthenticationHWControlError`
  * Please raise this exception when an authentication-related error occurs.
  * Base Exception Class Code: `"002"`
  * Error Code: `"EF002BAS000"`
  * HTTP Status Code: `401`
  * Default Error Message: `"Authentication failed."`

* `BadRequestHWControlError`
  * Please raise this exception when an error occurs due to an invalid request. For example, requesting power control for a device that does not support power control.
  * Base Exception Class Code: `"003"`
  * Error Code: `"EF003BAS000"`
  * HTTP Status Code: `400`
  * Default Error Message: `"Your request is invalid."`

* `ControlObjectHWControlError`
  * Please raise this exception when an error occurs in the OOB Controller or Fabric Manager.
  * Base Exception Class Code: `"004"`
  * Error Code: `"EF004BAS000"`
  * HTTP Status Code: `500`
  * Default Error Message: `"Failed to operate the specified device."`

* `ResourceBusyHWControlError`
  * Please raise this exception when the specified resource is busy and the requested operation cannot be performed.
  * Base Exception Class Code: `"005"`
  * Error Code: `"ER005BAS000"`
  * HTTP Status Code: `503`
  * Default Error Message:  `"The specified resource is not found."`

* `ConfigurationHWControlError`
  * Please raise this exception when an error occurs due to a configuration or setup issue in hw-control. For example, when processing cannot be executed due to a plugin configuration file problem.
  * Base Exception Class Code: `"007"`
  * Error Code: `"EF007BAS000"`
  * HTTP Status Code: `500`
  * Default Error Message: `"Your request failed due to the missing required system configuration."`

* `InternalHWControlError`
  * Please raise this exception when an internal error occurs in the hw-control application, including plugins.
  * Base Exception Class Code: `"010"`
  * Error Code: `"EF010BAS000"`
  * HTTP Status Code: `500`
  * Default Error Message: `"The server encountered an internal error."`

* `RequestConflictHWControlError`
  * Please raise this exception when the state of the specified resource conflicts with the request. For example, requesting a connection to a device that is already connected to another device.
  * Base Exception Class Code: `"011"`
  * Error Code: `"EF011BAS000"`
  * HTTP Status Code: `409`
  * Default Error Message: `"The request conflicts with the current resource state."`

* `DependencyServiceHWControlError`
  * Please raise this exception when processing fails due to an error in an external CDIM component outside of hw-control.
  * Base Exception Class Code: `"012"`
  * Error Code: `"EF012BAS000"`
  * HTTP Status Code: `500`
  * Default Error Message: `"Operation could not be completed due to a failure in external dependencies."`

* `DeviceNotFoundHWControlError`
  * Please raise this exception when the target device for control or information retrieval does not exist.
  * Base Exception Class Code: `"013"`
  * Error Code: `"EF013BAS000"`
  * HTTP Status Code: `404`
  * Default Error Message: `"The specified target device is not found."`

## 7.2. Defined Exceptions

These exception classes are intended for use when a plugin detects an anomaly, and they inherit from the same base exception class as the base exception class code.  
These classes, which inherit from the base exception class, are called detailed exception classes.  

The following exception classes are defined:

* `OOBAuthenticationHWControlError`
  * Raise this exception when authentication to the OOB Controller fails.
  * Base class：`AuthenticationHWControlError`
  * Target Plugin: OOB
  * Error Code: `"EF002BAS002"`
  * HTTP Status Code: `401`
  * Default Error Message: `"Authentication to the Out-of-Band Controller failed."`

* `HostCPUNotFoundHWControlError`
  * **Deprecated**
  * This class is retained for compatibility with legacy plugins, but is scheduled for removal in the next release. Please use `UpstreamDeviceNotFoundHWControlError` instead.
  * Base class：`DeviceNotFoundHWControlError`
  * Target Plugin: FM
  * Error Code: `"EF013BAS001"`
  * HTTP Status Code: `404`
  * Default Error Message: `"The specified Host CPU is not found."`

* `HostCPUAndDeviceNotFoundHWControlError`
  * **Deprecated**
  * This class is retained for compatibility with legacy plugins, but is scheduled for removal in the next release. In the FM plugin's `connect` or `disconnect` method, if it is determined that the target device does not exist, please raise `UpstreamDeviceNotFoundHWControlError` or `DownstreamDeviceNotFoundHWControlError`.
  * Base class：`DeviceNotFoundHWControlError`
  * Target Plugin: FM
  * Error Code: `"EF013BAS002"`
  * HTTP Status Code: `404`
  * Default Error Message: `"The specified Host CPU and target device are not found."`

* `UpstreamDeviceNotFoundHWControlError`
  * Raise this exception in the FM plugin's `connect` or `disconnect` method when the specified USP does not contain a device.
  * Base class: `DeviceNotFoundHWControlError`
  * Target Plugin: FM
  * Error Code: `"EF013BAS000"` (inherits the value from the base class)
  * HTTP Status Code: `404`
  * Default Error Message: `"The specified target device is not found."` (inherits the value from the base class)

* `DownstreamDeviceNotFoundHWControlError`
  * Raise this exception in the FM plugin's `connect` or `disconnect` method when the specified DSP does not contain a device.
  * Base class: `DeviceNotFoundHWControlError`
  * Target Plugin: FM
  * Error Code: `"EF013BAS000"` (inherits the value from the base class)
  * HTTP Status Code: `404`
  * Default Error Message: `"The specified target device is not found."` (inherits the value from the base class)

* `ResourceNotFoundHWControlError`
  * Raise this exception in the FM plugin when the specified resource does not exist.
  * Base class：`DeviceNotFoundHWControlError`
  * Target Plugin: FM
  * Error Code: `"EF013BAS003"`
  * HTTP Status Code: `404`
  * Default Error Message: `"The specified resource is not found."`

* `SwitchNotFoundHWControlError`
  * Raise this exception in the FM plugin when the specified switch does not exist.
  * Base class：`DeviceNotFoundHWControlError`
  * Target Plugin: FM
  * Error Code: `"EF013BAS004"`
  * HTTP Status Code: `404`
  * Default Error Message: `"The specified switch is not found."`

* `RequestNotSupportedHWControlError`
  * Raise this exception when a request is made for an operation that is not supported for the specified device.
  * Base class：`DeviceNotFoundHWControlError`
  * Target Plugin: OOB
  * Error Code: `"EF003BAS010"`
  * HTTP Status Code: `400`
  * Default Error Message: `"Your request is not supported for the specified target device."`

* `FMConnectFailureHWControlError`
  * Raise this exception in the Fabric Manager when a connection between the specified Host CPU and device fails.
  * Base class：`ControlObjectHWControlError`
  * Target Plugin: FM
  * Error Code: `"EF004BAS001"`
  * HTTP Status Code: `500`
  * Default Error Message: `"The Fabric Manager failed to establish a connection between the specified Host CPU and target device."`

* `FMDisconnectFailureHWControlError`
  * Raise this exception in the Fabric Manager when disconnection between the specified Host CPU and device fails.
  * Base class：`ControlObjectHWControlError`
  * Target Plugin: FM
  * Error Code: `"EF004BAS002"`
  * HTTP Status Code: `500`
  * Default Error Message: `"The Fabric Manager failed to disconnect a connection between the specified Host CPU and the target device."`

* `PowerOnFailureHWControlError`
  * Raise this exception when the OOB Controller fails to power on the specified device.
  * Base class：`ControlObjectHWControlError`
  * Target Plugin: OOB
  * Error Code: `"EF004BAS003"`
  * HTTP Status Code: `500`
  * Default Error Message: `"The Out-of-Band Controller failed to power on the specified device."`

* `PowerOffFailureHWControlError`
  * Raise this exception when the OOB Controller fails to power off the specified device.
  * Base class：`ControlObjectHWControlError`
  * Target Plugin: OOB
  * Error Code: `"EF004BAS004"`
  * HTTP Status Code: `500`
  * Default Error Message: `"The Out-of-Band Controller failed to power off the specified device."`

* `CPUResetFailureHWControlError`
  * Raise this exception when the OOB Controller fails to reset the specified Host CPU.
  * Base class：`ControlObjectHWControlError`
  * Target Plugin: OOB
  * Error Code: `"EF004BAS005"`
  * HTTP Status Code: `500`
  * Default Error Message: `"The Out-of-Band Controller failed to reset the specified Host CPU."`

* `InvalidDeviceTypeParameterHWControlError`
  * Raise this exception in the OOB plugin when the specified device type is invalid.
  * Base class：`ConfigurationHWControlError`
  * Target Plugin: OOB
  * Error Code: `"EF007BAS016"`
  * HTTP Status Code: `500`
  * Default Error Message: `"The specified Device Type is invalid."`

## 7.3. Adding Exceptions

If the defined error situation does not apply or if you want to change the information returned to the upper levels, please add a new exception within the plugin module.  
The exception class defined by a plugin is called an extended exception class.

To add an exception, determine the following information:

* Vendor-dependent extended exception code  
It consists of three uppercase letters of the alphabet.  
The vendor-dependent extended exception class code is assumed to be a string that does not overlap with other plugins for each plugin. Since no plugins are currently available, please decide on any three uppercase letters other than "BAS".  
For details, refer to [9.2. Limitations Vendor-dependent extended exception class code](09_Special_Notes.md#vendor-dependent-extended-exception-class-code).

* Base Class for Exceptions  
Select one exception that is close from the [Base Exception Classes](#base-exception-classes) or [Defined Exceptions](#72-defined-exceptions).  

* Error Level  
Verify whether the error is fatal or not.  

* Retry Possibility  
Check if processing the same request after some time might succeed.  

* HTTP Status Code  
Determine the HTTP status code to return to the upper level, following the Status Code of RFC9110.  

* Default Error Message  
Determine the default error message in English to be returned to the higher level.  

* Exception Class Name  
The class name is arbitrary but should end with `HWControlError`.  

* Detailed Exception Class Code  
Choose a unique three-digit number that can be identified within the inherited base exception class.  

An example of adding such an exception to a class is shown below.

|Item Name|Example|
|--|--|
|Vendor-Specific Extension Exception Code|"SPL"|
|Base Class for Exception|`BadRequestHWControlError`|
|Error Level|Non-fatal|
|Retry Possibility|No point in retrying for a continuing error|
|HTTP Status Code|400|
|Default Error Message|"Sample exception message."|
|Exception Class Name|`SampleHWControlError`|
|Detailed Exception Class Code|"001"|

```python
import app.common.basic_exceptions as exc


class SampleHWControlError(exc.BadRequestHWControlError):
    """Sample extended exception class

    sample docstring
    """
    # To change the HTTP status code from an inherited class, set the class variable http_code.
    # In this example, the same value as the parent is used, so no setting is necessary.
    # http_code: int = http.HTTPStatus.BAD_REQUEST.value

    # Set the error code in the class variable error_code.
    # In this example, the error code is "EF003SPL001".
    # - Error Level: Non-critical "E"  
    # - Retry Possibility: No possibility of success with retry "F"
    # - Base Exception Class Code: BadRequestHWControlError "003"
    # - Vendor-Specific Extension Exception Code: "SPL"
    # - Detailed Exception Class Code: "001"
    error_code: str = "EF003SPL001"

    # Set the default error message in the class variable default_error_message.
    # If using the same value as the parent, no setting is necessary.
    default_error_message: str = "Sample exception message."
```
