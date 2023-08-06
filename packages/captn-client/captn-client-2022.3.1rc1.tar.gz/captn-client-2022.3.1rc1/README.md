# Capt’n python client 2022.3.1rc1

## Docs

Full documentation can be found at the following link:

- <a href="https://docs.captn.ai" target="_blank">https://docs.captn.ai/</a>


## How to install

If you don't have the captn library already installed, please install it using pip.


```console
pip install captn-client
```

## How to use

To access the captn service, you must create a developer account. Please fill out the signup form below to get one:

- [https://bit.ly/3I4cNuv](https://bit.ly/3I4cNuv)

Upon successful verification, you will receive the username/password for the developer account in an email. 

Finally, you need an application token to access all the APIs in captn service. Please call the `Client.get_token` method with the username/password to get one. 

You can either pass the username, password, and server address as parameters to the `Client.get_token` method or store the same in the **CAPTN_SERVICE_USERNAME**, **CAPTN_SERVICE_PASSWORD**, and **CAPTN_SERVER_URL** environment variables.

After successful authentication, the captn services will be available to access.

For more information, please check:

- [Tutorial](https://docs.captn.ai/Tutorial/) with more elaborate example, and

- [API](https://docs.captn.ai/API/client/Client/) with reference documentation.


Below is a minimal example explaining how to load the data, train a model and make predictions using captn services. 

!!! info

	In the below example, the username, password, and server address are stored in **CAPTN_SERVICE_USERNAME**, **CAPTN_SERVICE_PASSWORD**, and **CAPTN_SERVER_URL** environment variables.


### 0. Get token


```python
from captn.client import Client, DataBlob, DataSource

Client.get_token()
```

### 1. Connect and preprocess data

In our example, we will be using the captn APIs to load and preprocess a sample CSV file stored in an AWS S3 bucket. 


```python
data_blob = DataBlob.from_s3(
    uri="s3://test-airt-service/sample_gaming_130k/"
)
data_blob.progress_bar()

```

    100%|██████████| 1/1 [01:35<00:00, 95.95s/it]


The sample data we used in this example doesn't have the header rows and their data types defined. 

The following code creates the necessary headers along with their data types and reads only a subset of columns that are required for modeling:



```python
prefix = ["revenue", "ad_revenue", "conversion", "retention"]
days = list(range(30)) + list(range(30, 361, 30))
dtype = {
    "date": "str",
    "game_name": "str",
    "platform": "str",
    "user_type": "str",
    "network": "str",
    "campaign": "str",
    "adgroup": "str",
    "installs": "int32",
    "spend": "float32",
}
dtype.update({f"{p}_{d}": "float32" for p in prefix for d in days})
names = list(dtype.keys())

kwargs = {"delimiter": "|", "names": names, "parse_dates": ["date"], "usecols": names[:42], "dtype": dtype}
```

Finally, the above variables are passed to the `DataBlob.from_csv` method which preprocesses the data and stores it in captn server.


```python
data_source = data_blob.from_csv(
    index_column="game_name",
    sort_by="date",
    **kwargs
)

data_source.progress_bar()
```

    100%|██████████| 1/1 [00:40<00:00, 40.53s/it]



```python
print(data_source.head())
```

             date platform          user_type            network      campaign  \
    0  2021-03-15      ios      jetfuelit_int      jetfuelit_int    campaign_0   
    1  2021-03-15      ios      jetfuelit_int      jetfuelit_int    campaign_0   
    2  2021-03-15      ios      jetfuelit_int      jetfuelit_int    campaign_0   
    3  2021-03-15      ios      jetfuelit_int      jetfuelit_int    campaign_0   
    4  2021-03-15      ios      jetfuelit_int      jetfuelit_int    campaign_0   
    5  2021-03-15  android  googleadwords_int  googleadwords_int  campaign_283   
    6  2021-03-15  android  googleadwords_int  googleadwords_int    campaign_2   
    7  2021-03-15  android         moloco_int         moloco_int  campaign_191   
    8  2021-03-15  android      jetfuelit_int      jetfuelit_int    campaign_0   
    9  2021-03-15  android      jetfuelit_int      jetfuelit_int    campaign_0   
    
            adgroup  installs       spend  revenue_0  revenue_1  ...  revenue_23  \
    0   adgroup_541         1    0.600000   0.000000   0.018173  ...    0.018173   
    1  adgroup_2351         2    4.900000   0.000000   0.034000  ...    0.034000   
    2   adgroup_636         3    7.350000   0.000000   0.000000  ...   12.112897   
    3   adgroup_569         1    0.750000   0.000000   0.029673  ...    0.029673   
    4   adgroup_243         2    3.440000   0.000000   0.027981  ...    0.042155   
    5  adgroup_1685        11    0.000000   0.000000   0.097342  ...    0.139581   
    6    adgroup_56        32   30.090000   0.000000   0.802349  ...    2.548253   
    7          None       291  503.480011  34.701553  63.618111  ...  116.508331   
    8   adgroup_190         4    2.740000   0.000000   0.000000  ...    0.000000   
    9   adgroup_755         8   11.300000  13.976003  14.358793  ...   14.338905   
    
       revenue_24  revenue_25  revenue_26  revenue_27  revenue_28  revenue_29  \
    0    0.018173    0.018173    0.018173    0.018173    0.018173    0.018173   
    1    6.034000    6.034000    6.034000    6.034000    6.034000    6.034000   
    2   12.112897   12.112897   12.112897   12.112897   12.112897   12.112897   
    3    0.029673    0.029673    0.029673    0.029673    0.029673    0.029673   
    4    0.042155    0.042155    0.042155    0.042155    0.042155    0.042155   
    5    0.139581    0.139581    0.139581    0.139581    0.139581    0.139581   
    6    2.548253    2.771138    2.805776    2.805776    2.805776    2.805776   
    7  117.334709  117.387489  117.509506  118.811417  118.760765  119.151291   
    8    0.000000    0.000000    0.000000    0.000000    0.000000    0.000000   
    9   14.338905   14.338905   14.338905   14.338905   14.338905   14.338905   
    
       revenue_30  revenue_60  revenue_90  
    0    0.018173    0.018173    0.018173  
    1    6.034000    6.034000   13.030497  
    2   12.112897   12.112897   12.112897  
    3    0.029673    0.029673    0.029673  
    4    0.042155    0.042155    0.042155  
    5    0.139581    0.139581    0.139581  
    6    2.805776    2.805776    2.805776  
    7  119.350220  139.069443  147.528793  
    8    0.000000    0.000000    0.000000  
    9   14.338905   14.338905   14.338905  
    
    [10 rows x 41 columns]


### 2. Training


```python
# Todo
```
