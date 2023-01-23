"""_summary_: Get metrics from Hashicorp Vault API"""
import logging
import requests
from ruxit.api.base_plugin import RemoteBasePlugin

logger = logging.getLogger(__name__)

vault_samples = {
    "vault.barrier.get": None,
}

class HashicorpVaultPlugin(RemoteBasePlugin):
    """_summary_: Core Plugin Structure"""
    def initialize(self, **kwargs):
        config = kwargs['config']
        self.vault_url = config['vault_url']

    def query(self, **kwargs):
        """_summary_: Query Vault API"""
        vault_response = requests.get(url=self.vault_url, timeout=10)
        vault_response_json = vault_response.json()

        group = self.topology_builder.create_group(12668946693571282165, "Hashicorp Vault")
        device = group.create_device("vault1", "Vault 1")

        for sample in vault_response_json['Samples']:
            # self.results_builder.add_sample(sample)
            logger.info("Sample: %s", sample)
            device.absolute(key="vault.barrier.get.count", value=sample['count'])
        # logger.info("Vault Response: %s", vault_response.text)
