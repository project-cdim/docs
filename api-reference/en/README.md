# API Reference

This is the external API reference provided by the Composable Disaggregated Infrastructure Manager (CDIM).

> [!NOTE] CDIM is currently under development and functionality may change, be deleted, or become incompatible without notice. Please check the reference regularly and stay updated for the latest information.

## API List

* [Layout Apply API][]
* [Configuration Management API][]
* Performance Management API
  * Performance manager uses VictoriaMetrics, and the accumulated performance information is retrieved using VictoriaMetrics's Query. For details, please refer to [VictoriaMetrics API example][].

[Layout Apply API]: https://project-cdim.github.io/docs/api-reference/en/layout-apply-api/index.html
[Configuration Management API]: https://project-cdim.github.io/docs/api-reference/en/configuration-management-api/index.html
[VictoriaMetrics API example]: https://docs.victoriametrics.com/url-examples/#apiv1query_range