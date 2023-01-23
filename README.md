# Dynatrace Hashicorp Vault V1 Extension
This repo is created and maintained by Aaron Philipose for the purpose of open-source ado

This extension is designed to be used on a Dynatrace ActiveGate for Collecting Metrics for a Hashicorp Vault Process Group.
This extension does not use the traditional method of ingesting metrics through the v1 extension as it is easier to maintain flexibility and maintain the reporting style of the vault using Dynatrace Metrics API ingest format.
Because of this method we are able to dynamically ingest metrics for different vault items that Hashicorp vault is using.

Currently this extension does not support authentication to access the Hashicorp Vault thought this can be incorporated if requested.

This Extension requires 4 variables:

1. Hashicorp Vault Metrics URL
2. Dynatrace Tenant URL
3. Dynatrace API Token (requires metrics.ingest)
4. Process Group ID to attach to.
