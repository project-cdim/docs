# 7. Logging

As a general policy, the Layout Design and each plugin should use separate logger objects and write to separate log files.
With this policy, there are no constraints on which logger you use in a plugin or the exact log record format.  
Below are notes regarding plugin log output.
- If using Python's standard [logger objects](https://docs.python.org/3.14/library/logging.html#logger-objects), do not use the root logger in plugins.
- Although there are no restrictions on the destination directory for plugin log files, we recommend specifying the same directory as the Layout Design log output destination (default: `/var/log/cdim/`).

The table below follows Python's standard logger levels and summarizes the policy for each level.

| Level | Policy |
| --- | --- |
| DEBUG | Information about system behavior |
| INFO | Noteworthy events such as start/finish of processing |
| WARNING | Abnormal but non-error conditions |
| ERROR | Failures that prevent parts of the system from functioning (e.g., DB connection failure) |
| CRITICAL | Fatal problems that prevent program continuation |
