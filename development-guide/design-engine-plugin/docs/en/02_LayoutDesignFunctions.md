# 2. Layout Design Overview

This chapter outlines the REST APIs of the Layout Design and then lists the functions that a plugin implements.

## 2.1. REST APIs of Layout Design Functions

The following REST APIs of the Layout Design are relevant to plugins.

| No. | Name | URI | HTTP Method | Overview |
| --- | --- | --- | --- | --- |
| 1 | Layout Design Request | /cdim/api/v1/layout-designs | POST | Accepts service definitions and resource requirements, starts the layout design process, and returns a design ID. |
| 2 | Get Layout Design Result | /cdim/api/v1/layout-designs/{designID} | GET | Returns the layout design result for the specified design ID. |
| 3 | List Layout Design Results | /cdim/api/v1/layout-designs | GET | Returns a list of layout design results. |
| 4 | Cancel Layout Design | /cdim/api/v1/layout-designs/{designID}?action=cancel | PUT | Cancels the layout design process for the specified design ID. |
| 5 | Delete Layout Design Result | /cdim/api/v1/layout-designs/{designID} | DELETE | Deletes the layout design result for the specified design ID. |

## 2.2. Plugin Overview

A plugin is implemented as a class (see [4.2. Class Structure](04_Configuration.md#42-class-structure)).
The REST APIs of the Layout Design delegate engine-specific processing to the plugin, and the plugin calls the underlying Design Engine.

The methods implemented by a plugin are listed below.

### Plugin Methods

| No. | Name | Method | Overview |
| --- | --- | --- | --- |
| 1 | Layout Design Request | request_design | Accepts service definitions, resource requirements, resource performance data, and node configuration data, starts the layout design process, and returns a design ID. |
| 2 | Get Layout Design Result | get_design | Returns the layout design result for the specified design ID. |
| 3 | List Layout Design Results | get_all_design | Returns a list of layout design results. |
| 4 | Cancel Layout Design | cancel_design | Cancels the layout design process for the specified design ID. |
| 5 | Delete Layout Design Result | delete_design | Deletes the layout design result for the specified design ID. |

### Inputs for Layout Design Request

The inputs provided to the plugin in a layout design request are summarized below.
See [Appendix 1. Arguments to request_design](a01_Args_to_request_design_Function.md) for details.

| No. | Data | Parameter | Type | Overview |
| --- | --- | --- | --- | --- |
| 1 | [Request ID](a01_Args_to_request_design_Function.md#request-id-requestid) | requestID | str | ID used by the caller of the Layout Design to identify the layout design request. |
| 2 | [Target Node IDs](a01_Args_to_request_design_Function.md#target-node-ids-targetnodeids) | targetNodeIDs | list[str] | IDs of nodes to be designed among all nodes. |
| 3 | [Service Set Request Resources](a01_Args_to_request_design_Function.md#service-set-request-resources-servicesetrequestresources) | serviceSetRequestResources | dict | Resource types and performance required by services. |
| 4 | [Services](a01_Args_to_request_design_Function.md#services-services) | services | dict | Service definitions. |
| 5 | [All Resources](a01_Args_to_request_design_Function.md#all-resources-resources) | resources | list[dict] | Performance information of all resources retrieved from the Configuration Manager. |
| 6 | [All Nodes](a01_Args_to_request_design_Function.md#all-nodes-nodes) | nodes | list[dict] | Configuration information of all nodes at execution time retrieved from the Configuration Manager. |
| 7 | [Design All Nodes Flag](a01_Args_to_request_design_Function.md#design-all-nodes-flag-designallnodes) | designAllNodes | bool | Whether all nodes are in scope. |
| 8 | [Partial Design Flag](a01_Args_to_request_design_Function.md#partial-design-flag-partialdesign) | partialDesign | bool | Whether only specified services/nodes (partial design) or all (entire design) are in scope. |
| 9 | [Skip Migration Condition Flag](a01_Args_to_request_design_Function.md#skip-migration-condition-flag-nocondition) | noCondition | bool | Whether migration conditions are unnecessary as part of the design result. |
| 10 | [Policies](a01_Args_to_request_design_Function.md#policies-policies) | policies | dict | Policies for resource selection retrieved from the Policy Manager. |

### Overview of Layout Design Result

The information returned as the layout design result is summarized below.
See [Appendix 2. Return Value of get_design](a02_Return_Value_from_get_design.md) for details about design, tolerance conditions, and migration procedures.

| No. | Data | Parameter | Type | Overview |
| --- | --- | --- | --- | --- |
| 1 | [Design Status](a02_Return_Value_from_get_design.md#design-status-status) | status | str | Status string of the layout plan (IN_PROGRESS, COMPLETED, FAILED, CANCELING, CANCELED). |
| 2 | [Request ID](a02_Return_Value_from_get_design.md#request-id-requestid) | requestID | str | The request ID managed by the caller, returned as provided in the input. |
| 3 | [Started At](a02_Return_Value_from_get_design.md#started-at-startedat) | startedAt | str | Time when the plugin/engine started the design process. |
| 4 | [Ended At](a02_Return_Value_from_get_design.md#ended-at-endedat) | endedAt | str | Time when the plugin/engine finished the design process. |
| 5 | [Design](a02_Return_Value_from_get_design.md#design-design) | design | dict | Node layout plan created from the input. |
| 6 | [Conditions](a02_Return_Value_from_get_design.md#conditions-conditions) | conditions | dict | Tolerance conditions for migrating from the current node configuration to the designed layout plan. |
| 7 | [Procedures](a02_Return_Value_from_get_design.md#procedures-procedures) | procedures | list[dict] | Migration procedures to move from the current node configuration to the designed layout plan. |
| 8 | [Failure Cause](a02_Return_Value_from_get_design.md#failure-cause-cause) | cause | str | Failure reason when the design status is FAILED. |
