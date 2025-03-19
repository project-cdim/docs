# 8. Logging

When outputting application logs from the plugin, please use the logger object of the HW control function.
This will enable log collection during failures in the operational environment.  
The logger object used in the HW control function is defined under the object name `LOGGER` in the `app.common.utils.log` module of the HW control function.  
For details, please refer to [8.1. Logger Object for HW Control Function](#81-logger-object-for-hw-control-function).  

Several log messages in the HW control function are defined in the `app.common.messages.message` module.  
For more details, see [8.2. Default Log Messages](#82-default-log-messages).

The log message model class that can be used as an aid for log output in HW control functions is defined in the `app.common.messages.message` module.  
For details, please refer to [8.3. Log Message Model Classes](#83-log-message-model-classes).  

## 8.1. Logger Object for HW Control Function

The logger object used in the HW control function inherits features from Python's built-in `logging` module.  
The following logging levels exist, and the corresponding functions are used to output application logs.  

|Level|Function Name|Policy|
|--|--|--|
|DEBUG|`debug(message: str, stack_info: bool = False)`|Information for development and debugging|
|INFO|`info(message: str, stack_info: bool = False)`|Information to understand the operation|
|WARNING|`warning(message: str, stack_info: bool = False)`|Information that requires attention but can continue processing the request|
|ERROR|`error(message: str, stack_info: bool = True)`|Cases where it is not possible to process the request|
|CRITICAL|`critical(message: str, stack_info: bool = True)`|Cases where a very serious error occurs that prevents the service from continuing|

The arguments for the function are as follows:

- `message`
  - A string message to be output to the log.
- `stack_info`
  - Outputs the stack trace if True.

If the message you want to output exists in the predefined log messages, a message code can be used.  
For predefined log messages, please refer to [8.2. Default Log Messages](#82-default-log-messages).  
If you want to output a message that is not in the predefined log messages, you can use the log message model class.  
For instructions on how to use the log message model class, please refer to [8.3. Log Message Model Classes](#83-log-message-model-classes).  
If you do not use message codes or the log message model class, please describe it as follows.  

```python
from app.common.utils.log import LOGGER

LOGGER.info("Any message.", False)
```

## 8.2. Default Log Messages

Messages that can be used for log output from plugins are defined.  

|Message Code|Log Message|Remarks|
|------|----------|----|
|"W00001"|W00001: Unexpected Exception: [(0)exception information]*1|Handling unexpected exceptions|
|"W00002"|W00002: Unexpected DeviceType: [(0)device type]|Unexpected device type specified|
|"W00006"|W00006: Device information not found: [(0)device ID, OOB device ID, device type, etc.]|Target device information not found|
|"W00007"|W00007: File does not exist: [(0)file path]| File does not exist|
|"W00008"|W00008: Required item does not exist: [(0)item name, etc.]| Required item does not exist|
|"W00009"|W00009: Invalid type value: [(0)item name, value, expected data type, etc.] | Data type error|
|"W00010"|W00010: Power Operation Error: [(0)ResetType, ur]|Power operation error on target device|
|"W00011"|W00011: Not Power Operation Device: [(0)ResetType, ur]|Device specified that cannot perform power operation|
|"W00012"|W00012: Failed to get OOB Response: [(0)url]|OOB response error|
|"E00001"|E00001: Unexpected Exception: [(0)exception information]*1|Handling unexpected exceptions when information retrieval fails|
|"E00002"|E00002: Unexpected DeviceType: [(0) Device Type]|Unexpected device type specified|
|"E00003"|E00003: Device information not found: [(0) Device ID, OOB Device ID, Device Type, etc.]| Target device information not found|
|"E00004"|E00004: Power Operation Error: [(0) Reset Type, URL]|Target device power operation error|
|"E00005"|E00005: Not Power Operation Device: [(0) Reset Type, URL]|Designation of a device that cannot perform power operations|
|"E00006"|E00006: Failed to get OOB Response: [(0) URL]|Response error from OOB|

*1 `traceback.format_exc()` etc.

Additionally, the following function is defined for formatting log output.

```python
get_log_message(message_code: str, param_list: list) -> str:
```

This function takes the following arguments:

- `message_code`
  - Specifies the message code as a string.
- `param_list`
  - Specifies the string to output in the [(0)] part of the message code in list format.

This function returns a string for log output.  
If there are any deficiencies in the arguments, the following exceptions are thrown.  

- InvalidLogMessageParameterHwControlError

These messages can be invoked and logged as follows.  

```python
from app.common.messages import message
from app.common.utils.log import LOGGER

LOGGER.warning(message.get_log_message(message.W00006, ["device_id: xxx, device_type: xxx"]))
```

It will be output as follows.

```text
yyyy/mm/dd HH:MM:SS.uuuuuu WARNING {"file":"---/plugins/xx/xxxx/xxxx_plugin.py","line":4,"message":"W00006: Device information not found: device_id: xxx, device_type: xxx"}
```

## 8.3. Log Message Model Classes

A class intended for use when outputting variable information to logs is defined.  

|Log Message Model Classes|Description|
|-------------------------|-----------|
|[`BaseLogMessage`](#baselogmessage)|Base message model class for recording the identifier of the REST API that called the HW control function in the log|
|[`ExceptionLog`](#exceptionlog)|Message model class for logging instances of exception classes|

### BaseLogMessage

```python
class BaseLogMessage(BaseModel):
```

This model class inherits from the `BaseModel` class of the Pydantic Python OSS library.  
The behavior of the constructor of this model class follows the specifications of Pydantic's `BaseModel` class.  
This model class has the following attributes:  

- `request_id(str | None)`
  - An identifier assigned to the REST API that called the HW control.
  - It is automatically set when called as an extension of the HW control function's REST API.
- `detail(str | None)`
  - Any additional information. None if unspecified.

This model class has the following method:

- `to_json_encodable()`
  - A method that converts the instance's information into a serialized dictionary format.

### ExceptionLog

```python
class ExceptionLog(BaseLogMessage):
```

This model class inherits the `BaseLogMessage` class to log instances of exception classes.  
The model class has the following attributes:

- `action(str)`
  - The operation that triggered the log output. Defaults to "exception raised" if unspecified.
- `trace_back(str | None)`
  - The traceback. Defaults to None if unspecified.

These classes can be called as follows to output logs.

```python
import traceback
from app.common.messages import message
from app.common.utils.log import LOGGER

LOGGER.info(str(message.BaseLogMessage(detail="Add sample message.").to_json_encodable()), False)
LOGGER.error(str(message.ExceptionLog(trace_back=traceback.format_exc()).to_json_encodable()))
```

The output will be as follows.

```text
yyyy/mm/dd HH:MM:SS.uuuuuu INFO {"file":"---/plugins/xx/xxxx/xxxx_plugin.py","line":6,"message":"{'request_id': 'rrrrrrrr', 'detail': 'Add sample message.'}"}
yyyy/mm/dd HH:MM:SS.uuuuuu ERROR {"file":"---/plugins/xx/xxxx/xxxx_plugin.py","line":10,"message":"{'request_id': 'rrrrrrrr', 'detail': None, 'action': 'exception raised', 'trace_back': 'NoneType: None\\n'}","stacktrace":["  File \".../plugins/xx/xxxx/xxxx_plugin.py\", line 10, in <module>\n    LOGGER.error(str(message.ExceptionLog(trace_back=traceback.format_exc()).to_json_encodable()), True)\n","  File \"/usr/local/lib/python3.12/dist-packages/gilogger/impl/standard/standard.py\", line 116, in error\n    self.logger.error(self._appLogToJson(message, self._getStacktrace(stack_info)))\n","  File \"/usr/local/lib/python3.12/dist-packages/gilogger/impl/igilogger.py\", line 64, in _getStacktrace\n    stacktrace = traceback.extract_stack().format()\n"]}
```

### Adding a Class

When you want to output specific information to the log, you can create a new class that inherits from the `BaseLogMessage` class.  
Below is an example of creating a class that adds the output of information containing a string `data1` and a number `data2`.

```python
from app.common.messages import message
from app.common.utils.log import LOGGER

class SampleLogMessage(message.BaseLogMessage):
    """A 'log message model' class for logging the sample class instance.

    sample docstrings
    """
    data1: str
    data2: int

...
mydata = {"data1": "string", "data2": 0}
LOGGER.info(str(SampleLogMessage(**mydata, detail="add my data").to_json_encodable()), False)
...
```

The output will be as follows.

```text
yyyy/mm/dd HH:MM:SS.uuuuuu INFO {"file":"---/plugins/xx/xxxx/xxxx_plugin.py","line":9,"message":"{'request_id': 'rrrrrrrr', 'detail': 'add my data', 'data1': 'string', 'data2': 0}"}
```
