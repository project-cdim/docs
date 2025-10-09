# Changelog 0.1

## [0.1.1](https://github.com/project-cdim/docs/compare/v0.1.0...v0.1.1) - 2025-10-09

### Concepts

Changes to the Concepts since v0.1.0 are as follows:

#### Breaking changes

- The following services have been added:
  - Alert Management Services
    - Alert Manager
  - Job Management Services
    - Job Manager
- The following services have been removed:
  - Configuration Management Services
    - Configuration Collector

### Getting Started

Changes to the Getting Started since v0.1.0 are as follows:

#### Breaking changes

The procedure has been revised according to the following service configuration changes.

- The following services have been added:
  - Alert Management Services
    - Alert Manager
  - Job Management Services
    - Job Manager
- The following services have been unused:
  - Configuration Management Services
    - Configuration Collector

### Tutorial

Changes to the Tutorial since v0.1.0 are as follows:

#### Breaking changes

The procedure has been revised according to the following service configuration changes.

- The following services have been added:
  - Alert Management Services
    - Alert Manager
  - Job Management Services
    - Job Manager
- The following services have been unused:
  - Configuration Management Services
    - Configuration Collector

### Hardware Plugin Development Guide

Changes to the Hardware Plugin Development Guide since v0.1.0 are as follows:

#### Deprecations

- The following exception classes have been deprecated:
  - `HostCPUNotFoundHWControlError`
  - `HostCPUAndDeviceNotFoundHWControlError`

#### Breaking Changes

- Migrated class names to follow PEP8 CapitalizedWords (CamelCase) convention (e.g., `CpuResetFailureHwControlError` to `CPUResetFailureHWControlError`).

- Replaced the logger object provided by [`cdim-python-logger`](https://github.com/project-cdim/cdim-python-logger) with Python's standard Logger object.

- Updated the specification to raise an exception in the following cases:
  - When one or more `id`s fail to be retrieved in `get_port_info()`.
  - When one or more `switch_id`s fail to be retrieved in `get_switch_info()`.

#### Bug Fixes

- Fixed documentation to clarify that empty strings are not allowed in the fields returned by `get_device_info()`, `get_port_info()` and `get_switch_info()`.
