# ADLSG2-with-Private-Link-Databricks-Power-BI
This post is to summarize what we did to install ADLSG2 with private endpoint and Databricks in a VNET and consume the Databricks table from Power BI desktop and web.

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
IN the VNET, we create this ADLSG2 with private endpoints. Pay attention here: at the time you create private endpoint, if you select Target subresource with value of blob, your private endpoint's FQDN will be *.blob.core.windows.net and late on you have to connect to the ADLSG2 as BLOB.

If you select Target subresource with value of dfs, your private endpoint's FQDN will be *.dsf.core.windows.net and late on you have to connect to the ADLSG2 as DFS.

| FQDN                             | Private IP |
| ---------------------------------|:-----------|
| onbpoclake.blob.core.windows.net | 172.17.0.5 |
| onbpoclake.dfs.core.windows.net  | 172.17.0.6 |

## Databricks
In the VNET, we create the Azure Datarbicks Workspace with two subnet 172.17.2.0/24 for public subnet and 172.17.3.0/24 for private one. These subnets will be sufficient for us to create multiple clsuters late on. As per Databricsk (https://docs.azuredatabricks.net/administration-guide/cloud-configurations/azure/vnet-inject.html): 
A workspace with a smaller virtual network can run out of IP addresses (network space) more quickly than a workspace with a larger virtual network. For example, a workspace with a /24 virtual network and /26 subnets can have a maximum of 64 nodes active at a time, whereas a workspace with a /20 virtual network and /22 subnets can house a maximum of 1024 nodes.

For different private endpoints, the way to mount the ADLSG2 fiel system to the databricks are different and the source code is included here.

## Power BI
Once the raw data has been proceesed by notebooks and presented as a permanent table in the Databricks workspace, we can use Power BI to visualize it with a Personal access token. To avoid exposing the access information, in Power BI Desktop at the time fo Get Data, you may select to Other/Spark and IMPORT tables (https://docs.azuredatabricks.net/bi/power-bi.html). Once the report is ready you can PUBLISH it to PowerBI.com.  
