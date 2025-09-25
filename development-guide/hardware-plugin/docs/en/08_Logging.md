# 8. Logging

Plugins can output application logs using Python's standard [Logger object](https://docs.python.org/3.12/library/logging.html#logger-objects). In each module, obtain the logger object by specifying `__name__` as an argument to [`logging.getLogger`](https://docs.python.org/3.12/library/logging.html#logging.getLogger) as shown below:

```python
import logging
logger = logging.getLogger(__name__)
```

For application logs, use the following log levels and policies as shown in the table below.

|Level|Policy|
|--|--|
|DEBUG|Information for development and debugging|
|INFO|Information to understand the operation|
|WARNING|Information that requires attention but can continue processing the request|
|ERROR|Cases where it is not possible to process the request|
|CRITICAL|Cases where a very serious error occurs that prevents the service from continuing|

Several log messages in the HW control function are defined in the `app.common.messages.message` module.
If the message you want to output exists in the predefined log messages, a message code can be used.  
For more details, see [8.1. Default Log Messages](#81-default-log-messages).

## 8.1. Default Log Messages

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

- InvalidLogMessageParameterHWControlError

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
