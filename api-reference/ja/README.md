# APIリファレンス

Composable Disaggregated Infrastructure Manager (CDIM) が提供する外部APIのリファレンスです。

> [!NOTE]
> CDIMは現在開発途上であり、今後予告なく機能の変更、削除、または非互換のある変更が行われる可能性があります。最新の情報を得るために、定期的にリファレンスを確認し、アップデートにご注意いただくようお願いいたします。

## API一覧

* [構成案反映API][]
* [構成情報管理API][]
* 性能情報管理API
  * 性能情報管理はVictoriaMetricsを使用しており、蓄積されている性能情報はVictriaMetricsのQueryを使用して取得します。詳細については[VictriaMetricsのAPI example][]を参照してください。

[構成案反映API]: https://project-cdim.github.io/docs/api-reference/ja/layout-apply-api/index.html
[構成情報管理API]: https://project-cdim.github.io/docs/api-reference/ja/configuration-management-api/index.html
[VictriaMetricsのAPI example]: https://docs.victoriametrics.com/url-examples/#apiv1query_range