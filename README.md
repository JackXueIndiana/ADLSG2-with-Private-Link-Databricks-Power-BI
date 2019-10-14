# ADLSG2-with-Private-Link-Databricks-Power-BI
This post is to summarize what we did to install ADLSG2 with private link and Databricks in a VNET and consume the Databricks table from Power BI desktop and web.

## VNET
To create a VNET is the first thing we need to do. We create a 172.17.0.0/16 which contains 65,536 IP addresses. In it, there are a number of subnets:


## VM
To enable users to runing different applications from a VM with the Azure Data Lake Storage Gen 2 (ADLSG2) as the data repository, a VM is created in the VNET. Its private IP address is 172.17.0.4 and in the default subnet.


| Name               | Address range | IPv4 available addresses | Delegated to                    | Security group              |
| -------------------|:--------------|:-------------------------|:--------------------------------|:----------------------------|
| default            | 172.17.0.0/24 | 249                      | -                               | -                           |
| AzureBastionSubnet | 172.17.1.0/24 | 250                      | -                               | -                           |
| onbpocdbspri       | 172.17.3.0/24 | 249                      | Microsoft.Databricks/workspaces | databricksnsg74bdgxsqpvvlo  |
| onbpocdbspub       | 172.17.2.0/24 | 249                      | Microsoft.Databricks/workspaces | databricksnsg74bdgxsqpvvlo  |
