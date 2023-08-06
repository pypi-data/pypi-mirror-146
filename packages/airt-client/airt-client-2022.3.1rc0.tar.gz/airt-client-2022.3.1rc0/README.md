# Python client for airt service 2022.3.1rc0

A python library encapsulating airt service REST API available at:

- <a href="https://api.airt.ai/docs" target="_blank">https://api.airt.ai/</a>

## Docs

For full documentation, Please follow the below link:

- <a href="https://docs.airt.ai" target="_blank">https://docs.airt.ai/</a>


## How to install

If you don't have the airt library already installed, please install it using pip.


```console
pip install airt-client
```

## How to use

To access the airt service, you must create a developer account. Please fill out the signup form below to get one:

- [https://bit.ly/3hbXQLY](https://bit.ly/3hbXQLY)

Upon successful verification, you will receive the username/password for the developer account in an email. 

Finally, you need an application token to access all the APIs in airt service. Please call the `Client.get_token` method with the username/password to get one. You 
can either pass the username, password, and server address as parameters to the `Client.get_token` method or store the same in the **AIRT_SERVICE_USERNAME**, 
**AIRT_SERVICE_PASSWORD**, and **AIRT_SERVER_URL** environment variables.

Upon successful authentication, the airt services will be available to access.
    
For more information, please check:

- [Tutorial](https://docs.airt.ai/Tutorial/) with more elaborate example, and

- [API](https://docs.airt.ai/API/client/Client/) with reference documentation.

Below is a minimal example explaining how to train a model and make predictions using airt services. 

!!! info

	In the below example, the username, password, and server address are stored in **AIRT_SERVICE_USERNAME**, **AIRT_SERVICE_PASSWORD**, and **AIRT_SERVER_URL** environment variables.


### 0. Get token


```
from airt.client import Client, DataSource, DataBlob

Client.get_token()
```

### 1. Connect data


```
# In this case, the input data is a CSV file strored in an AWS S3 bucket.

# Pulling the data into airt server
data_blob = DataBlob.from_s3(
    uri="s3://test-airt-service/ecommerce_behavior_csv"
)
data_blob.progress_bar()

# Preprocessing the data
data_source = data_blob.from_csv(
    index_column="user_id",
    sort_by="event_time"
)
data_source.progress_bar()

print(data_source.head())
```

    100%|██████████| 1/1 [00:35<00:00, 35.35s/it]
    100%|██████████| 1/1 [00:30<00:00, 30.32s/it]

                      event_time event_type  product_id          category_id  \
    0  2019-11-06 06:51:52+00:00       view    26300219  2053013563424899933   
    1  2019-11-05 21:25:44+00:00       view     2400724  2053013563743667055   
    2  2019-11-05 21:27:43+00:00       view     2400724  2053013563743667055   
    3  2019-11-05 19:38:48+00:00       view     3601406  2053013563810775923   
    4  2019-11-05 19:40:21+00:00       view     3601406  2053013563810775923   
    5  2019-11-06 05:39:21+00:00       view    15200134  2053013553484398879   
    6  2019-11-06 05:39:34+00:00       view    15200134  2053013553484398879   
    7  2019-11-05 20:25:52+00:00       view     1005106  2053013555631882655   
    8  2019-11-05 23:13:43+00:00       view    31501222  2053013558031024687   
    9  2019-11-06 07:00:32+00:00       view     1005115  2053013555631882655   
    
                   category_code                      brand    price  \
    0                       None                    sokolov    40.54   
    1    appliances.kitchen.hood                      bosch   246.85   
    2    appliances.kitchen.hood                      bosch   246.85   
    3  appliances.kitchen.washer                       beko   195.60   
    4  appliances.kitchen.washer                       beko   195.60   
    5                       None                      racer    55.86   
    6                       None                      racer    55.86   
    7     electronics.smartphone                      apple  1422.31   
    8                       None  dobrusskijfarforovyjzavod   115.18   
    9     electronics.smartphone                      apple   915.69   
    
                               user_session  
    0  d1fdcbf1-bb1f-434b-8f1a-4b77f29a84a0  
    1  b097b84d-cfb8-432c-9ab0-a841bb4d727f  
    2  b097b84d-cfb8-432c-9ab0-a841bb4d727f  
    3  d18427ab-8f2b-44f7-860d-a26b9510a70b  
    4  d18427ab-8f2b-44f7-860d-a26b9510a70b  
    5  fc582087-72f8-428a-b65a-c2f45d74dc27  
    6  fc582087-72f8-428a-b65a-c2f45d74dc27  
    7  79d8406f-4aa3-412c-8605-8be1031e63d6  
    8  e3d5a1a4-f8fd-4ac3-acb7-af6ccd1e3fa9  
    9  15197c7e-aba0-43b4-9f3a-a815e31ade40  


    


### 2. Train


```
from datetime import timedelta

model = data_source.train(
    client_column="user_id",
    target_column="event_type",
    target="*purchase",
    predict_after=timedelta(hours=3),
)
model.progress_bar()
print(model.evaluate())
```

    100%|██████████| 5/5 [00:00<00:00, 147.61it/s]

                eval
    accuracy   0.985
    recall     0.962
    precision  0.934


    


### 3. Predict


```
predictions = model.predict()
predictions.progress_bar()
print(predictions.to_pandas().head())
```

    100%|██████████| 3/3 [00:10<00:00,  3.38s/it]

                  Score
    user_id            
    520088904  0.979853
    530496790  0.979157
    561587266  0.979055
    518085591  0.978915
    558856683  0.977960


    

