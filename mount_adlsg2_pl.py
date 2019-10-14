# Databricks notebook source
# MAGIC %md #Something Special for Mounting ADLSG2 with Private LInk to Databricks
# MAGIC This will fail. After a ADLG2 having a private link, it only expose this endpoint the VNET with a FQDN of onbpoclake.blob.core.windows.net
# MAGIC Pay attention: **blob** whitch means we have to use the way to mount a Blob to mount this ADLSG2 through private link.

# COMMAND ----------

# THIS WILL FAIL.
configs = {"fs.azure.account.auth.type": "OAuth",
       "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
       "fs.azure.account.oauth2.client.id": "9ca9368b-050c-4ba7-967a-73f",
       "fs.azure.account.oauth2.client.secret": "/R4@@Ey/gtFNjBVfS0ocL",
       "fs.azure.account.oauth2.client.endpoint": "https://login.microsoftonline.com/72f988bf-86f1-41af-91/oauth2/token",
       "fs.azure.createRemoteFileSystemDuringInitialization": "true"}

dbutils.fs.mount(
source = "abfss://onbpoc@onbpoclake.dfs.core.windows.net",
#source = "abfss://onbpoc@onbpoclake.blob.core.windows.net/",
mount_point = "/mnt/onbpoc",
extra_configs = configs)

# COMMAND ----------

# MAGIC %fs
# MAGIC ls "dbfs:/mnt"

# COMMAND ----------

# Drop mounts
dbutils.fs.unmount("/mnt/onbpoc/")

# COMMAND ----------

# MAGIC %md # Mount this ADLSG2 as BLOB
# MAGIC More specifically we use a SAS key to do so.

# COMMAND ----------

container_name = 'onbpoc'
storage_name = 'onbpoclake'
mount_name = '/mnt/onbpoc' # This path can be used to access the contents of the blob container 
sas_key = '?sv=2018-03-28&ss=bfqt&srt=sco&sp=rwdlacup&se=2020-10-13T11:20:47sLMfBFD42fdp7GYNRRIc%3D'

dbutils.fs.mount(
  source = "wasbs://%s@%s.blob.core.windows.net" % (container_name, storage_name),
  mount_point = mount_name,
  extra_configs = {"fs.azure.sas.%s.%s.blob.core.windows.net" % (container_name, storage_name) : sas_key })

# COMMAND ----------

# MAGIC %fs
# MAGIC ls "dbfs:/mnt/onbpoc/input"

# COMMAND ----------

import os.path
import IPython
from pyspark.sql import SQLContext
display(dbutils.fs.ls("/mnt/onbpoc/input"))

# COMMAND ----------

# MAGIC %md # Create a table in the workspace so Power BI can use it
# MAGIC We apply the schema to the dataset with fully defined datatypes.

# COMMAND ----------

from pyspark.sql.types import *
from pyspark.sql.functions import *

loanSchema = StructType([
  StructField("Loan_ID", StringType(), False),
  StructField("Gender", StringType(), False),
  StructField("Married", StringType(), False),
  StructField("Dependents", StringType(), False),
  StructField("Education", StringType(), False),
  StructField("Self_Employed", StringType(), False),
  StructField("ApplicantIncome", IntegerType(), False),
  StructField("CoapplicantIncome", IntegerType(), False),
  StructField("LoanAmount", IntegerType(), False),
  StructField("Loan_Amount_Term", IntegerType(), False),
  StructField("Credit_History", IntegerType(), False),
  StructField("Property_Area", StringType(), False),
  StructField("Loan_Status", StringType(), False),
])

data = spark.read.csv('/mnt/onbpoc/input/Loan-applicant-details.csv.txt', schema=loanSchema, header=False)
data.show()

# COMMAND ----------

# MAGIC %md #Create a workspace table
# MAGIC We first create the table and them print a count.

# COMMAND ----------

sqlContext.sql("DROP TABLE IF EXISTS loanAppTable")
sqlContext.sql("DROP TABLE IF EXISTS temptable")

# COMMAND ----------

data.show()

# COMMAND ----------

data.registerTempTable("temptable")

# COMMAND ----------

out1 = spark.sql("SELECT * FROM temptable")
print(out1.count())

# COMMAND ----------

dbutils.fs.rm("dbfs:/user/hive/warehouse/loanapptable/", recurse=True)

# COMMAND ----------

sqlContext.sql("CREATE TABLE IF NOT EXISTS loanAppTable as select * from temptable")

# COMMAND ----------

out1 = spark.sql("SELECT * FROM loanAppTable")
print(out1.count())

# COMMAND ----------


