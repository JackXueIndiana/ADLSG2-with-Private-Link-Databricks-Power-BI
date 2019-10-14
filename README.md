# ADLSG2-with-Private-Link-Databricks-Power-BI
This post is to summarize what we did to install ADLSG2 with private link and Databricks in a VNET and consume the Databricks table from Power BI desktop and web.

## VNET
To create a VNET is the first thing we need to do. We create a 172.17.0.0/16 which contains 65,536 IP addresses. In it, there are a number of subnets:

| Name               | Address range | IPv4 available addresses | Delegated to                    | Security group              |
| -------------------|:--------------|:-------------------------|:--------------------------------|:----------------------------|
| default            | 172.17.0.0/24 | 249                      | -                               | -                           |
| AzureBastionSubnet | 172.17.1.0/24 | 250                      | -                               | -                           |
| onbpocdbspri       | 172.17.3.0/24 | 249                      | Microsoft.Databricks/workspaces | databricksnsg74bdgxsqpvvlo  |
| onbpocdbspub       | 172.17.2.0/24 | 249                      | Microsoft.Databricks/workspaces | databricksnsg74bdgxsqpvvlo  |

## VM
To enable users to runing different applications, such as Azure Storage Explorer, from a VM (Win 10 Pro, Standard D2 (2 vcpus, 7 GiB memory)) with the Azure Data Lake Storage Gen 2 (ADLSG2) as the data repository, a VM is created in the VNET. Its private IP address is 172.17.0.4 and in the default subnet. This VM is created without public IP address.

## Bastion
To convience to the addmin, we use Azure Bastion (preview), which created a public IP address, named onbpocvnet-ip and a subnet 172.17.1.0/24. When the Bastion host is installed, you can access this VM from VM's Operation in Azure Portal.

## Azure Data Lake Storage Gen 2
We create this ADLSG2 with private link. Pay attention here.

| FQDN                             | Private IP |
| ---------------------------------|:-----------|
| onbpoclake.blob.core.windows.net | 172.17.0.5 |


