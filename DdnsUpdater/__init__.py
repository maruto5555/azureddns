import logging
import requests
import azure.functions as func
from azure.identity import DefaultAzureCredential
from azure.mgmt.dns import DnsManagementClient

SUBSCRIPTION_ID = "223e7a56-d45a-4583-881d-b4b25b8f5c9c"
RESOURCE_GROUP = "wwy"
ZONE_NAME = "wongwingyin.top"
RECORD_SET_NAME = "home"
RECORD_TYPE = "A"

def main(mytimer: func.TimerRequest) -> None:
    logging.info("🚀 DDNS 更新啟動")

    try:
        current_ip = requests.get("https://api.ipify.org").text.strip()
        logging.info(f"🌐 外部 IP：{current_ip}")

        credentials = DefaultAzureCredential()
        dns_client = DnsManagementClient(credentials, SUBSCRIPTION_ID)
        record_set = dns_client.record_sets.get(RESOURCE_GROUP, ZONE_NAME, RECORD_SET_NAME, RECORD_TYPE)

        existing_ip = record_set.a_records[0].ipv4_address if record_set.a_records else None

        if existing_ip != current_ip:
            logging.info(f"📌 IP 變更：{existing_ip} ➜ {current_ip}")
            record_set.a_records = [{ "ipv4_address": current_ip }]
            dns_client.record_sets.create_or_update(
                RESOURCE_GROUP,
                ZONE_NAME,
                RECORD_SET_NAME,
                RECORD_TYPE,
                record_set,
                if_match=record_set.etag
            )
            logging.info("✅ DNS A 記錄已更新成功")
        else:
            logging.info("🔄 IP 無變更，略過更新")
    except Exception as e:
        logging.error(f"❌ 更新失敗：{str(e)}")
