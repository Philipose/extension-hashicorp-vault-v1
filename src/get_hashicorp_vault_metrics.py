"""_summary_: Get metrics from Hashicorp Vault API"""
import logging
import requests
from ruxit.api.base_plugin import RemoteBasePlugin

logger = logging.getLogger(__name__)

vault_samples = {
    "vault.barrier.get": None,
}

METRIC_INGEST_ENDPOINT = "/api/v2/metrics/ingest"

class HashicorpVaultPlugin(RemoteBasePlugin):
    """_summary_: Core Plugin Structure"""
    def initialize(self, **kwargs):
        config = kwargs['config']
        self.vault_url = config['vault_url']
        self.dt_tenant_url= config['dt_tenant_url']
        if self.dt_tenant_url.endswith("/"):
            self.dt_tenant_url = self.dt_tenant_url[:-1]
        self.dt_tenant_token = config['dt_tenant_token']
        self.process_group_id = config['process_group_id']

    def query(self, **kwargs):
        """_summary_: Query Vault API"""
        vault_response = requests.get(url=self.vault_url, timeout=10)
        vault_response_json = vault_response.json()

        metrics = ""
        for gauge in vault_response_json['Gauges']:
            if 'Value' in gauge:
                metric_line = f"{gauge['Name']},dt.entity.process_group={self.process_group_id} gauge,{gauge['Value']}"
                metrics= f"{metrics}{metric_line}\n"

        for counter in vault_response_json['Counters']:
            if 'Count' in counter:
                metric_line = f"{counter['Name']},dt.entity.process_group={self.process_group_id} count,{counter['Count']}"
                metrics= f"{metrics}{metric_line}\n"

        for sample in vault_response_json['Samples']:
            if (
                    'Name' in sample and \
                    'Sum' in sample and \
                    'Min' in sample and \
                    'Max' in sample and \
                    'Count' in sample
                ):
                metric_line = f"{sample['Name']},dt.entity.process_group={self.process_group_id} gauge,min={sample['Min']},max={sample['Max']},sum={sample['Sum']},count={sample['Count']}"
                metrics= f"{metrics}{metric_line}\n"

        push_metrics_response = requests.post(
                url=f"{self.dt_tenant_url}{METRIC_INGEST_ENDPOINT}",
                headers={'Authorization': f'Api-Token {self.dt_tenant_token}',
                'Content-Type': 'text/plain'},
                data=metrics,
                timeout=10,
        )
        logger.info("DT_API_RESPONSE: %s", push_metrics_response.status_code)
        if 400 <= push_metrics_response.status_code < 600:
            logger.info("DT_API_RESPONSE TEXT: %s", push_metrics_response.text)
