# Azure DDNS Python Function

這是一個使用 Azure Functions 的 DDNS 自動更新工具，透過 Python 語言實作，每 10 分鐘檢查外部 IP 是否變更，若有變動則自動更新 Azure DNS A 記錄。

## 部署步驟
1. 建立 Azure Function App 並啟用 Managed Identity
2. 將身份賦予 DNS Zone 的 Contributor 權限
3. 設定 `SUBSCRIPTION_ID`, `RESOURCE_GROUP`, `ZONE_NAME`, `RECORD_SET_NAME`
4. 部署程式並監控 Log

## 授權
MIT
