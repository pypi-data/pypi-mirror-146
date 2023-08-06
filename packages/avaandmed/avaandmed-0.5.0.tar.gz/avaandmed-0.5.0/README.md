# avaandmed-py
[![build](https://github.com/Michanix/avaandmed-py/actions/workflows/avaandmed.yml/badge.svg?branch=main)](https://github.com/Michanix/avaandmed-py/actions/workflows/avaandmed.yml)
[![codecov](https://codecov.io/gh/Michanix/avaandmed-py/branch/main/graph/badge.svg?token=DS5MNSZOII)](https://codecov.io/gh/Michanix/avaandmed-py)

## Documentation
- Official [Avaandmed API Swagger](https://avaandmed.eesti.ee/api/dataset-docs/#/)
- Official general [documentation](https://avaandmed.eesti.ee/instructions/api-uldjuhend) about API. Available only in Estonian.

## Requirements
- Python 3.6+

## Installation
## TODO

## Usage
Firstly you going to need to import `avaandmed` package and create client instance. 
Through that you can access necessary information for you Avaandmed account. You can create multiple instances for different accounts as well.

Library trying to copy workflow of API as much as possible.

```python
key_id = 'key_id_value'
token = 'token_value'
client = Avaandmed(api_token=token, key_id=key_id)
```

### Generic datasets
Getting some [Generic datasets](https://avaandmed.eesti.ee/api/dataset-docs/#/Generic%20dataset) is quite straightforward. Just use `datasets` property provided by `client` instance.

```python
datasets: Datasets = client.datasets
specific_ds: Dataset = datasets.get_by_id(some_ds_id)
```

Getting list of publicly available datasets. By default it will return first 20 datasets, but this can be adjusted by providing `limit` value.

```python
all_datasets: List[Dataset] = client.datasets.get_dataset_list() # retrieve first 20 datasets in the list
get_5_datasets: List[Dataset] = client.datasets.get_dataset_list(limit=5) # retrieves 5 datasets in the list
```

You can apply for access permissions for specific dataset as well. Or submit privacy violations for specific dataset.

```python
client.datasets.apply_for_access('dataset_id', 'description')
client.dataset.file_privacy_violations('dataset_id', 'description')
```


### User's datasets
[User](https://avaandmed.eesti.ee/api/dataset-docs/#/User's%20datasets)'s own datasets can be accessed and interacted in the following way.

```python
me: Me = client.users.me
# List all user's dataset
my_dataset: UserDataset = me.dataset

# Retrieves specific dataset
specific_ds: Dataset = me.get_by_id('dataset_id') 
# Delete specific dataset
my_dataset.delete('dataset_id')
# Update dataset
# To update dataset you need to provide a dictionary with fields you wish to update.
# Fields should be camelCased as per official Swagger document.
updateParams = {
    "maintainerPhone": "37255511122",
    "maintenerEmail": "maintainer@mail.com"
}
my_dataset.update(updateParams)

# Create dataset metadata
# To create dataset's metadata you can use DatasetMetadata model.
# For user's convinience parameters can be provided in camelCase manner to match 
# naming convention of the JSON that is used by Open Data.
# There are fields that are required to be filled and some don't. Optional fields can be left 
# out.
metadata: DatasetMetadata = DatasetMetadata(nameEn="new dataset", nameEt="new dataset"...)
my_dataset.create_dataset_metadata(metadata)
# You can consider specific privacy violations for your dataset
my_dataset.consider_privacy_violation('id')

# Or you can discard it
my_dataset.discard_privacy_violation('id')

# Approve access permission by its ID
my_dataset.approve_access_permission('permission_id')

# Decline access permission by its ID
my_dataset.decline_access_permission('permission_id')
```

### Organization's API
[Organization](https://avaandmed.eesti.ee/api/dataset-docs/#/Organization's%20datasets)'s datasets can be accessed and interacted in the similar way as User's.

```python
my_org = client.organization('org_id').my_organization
my_org_ds = my_org.dataset

# List all organizations 
all_orgs = my_org.get_list_my_orgs()

# Retrieve specifc organization
specifc_org = my_org.get_my_org_by_id('org_id')

# Retrieves specific dataset
specific_ds: Dataset = my_org_ds.get_by_id('dataset_id') 
# Delete specific dataset
my_org_ds.delete('dataset_id')
# Update dataset
# To update dataset you need to provide a dictionary with fields you wish to update.
# Fields should be camelCased as per official Swagger document.
updateParams = {
    "maintainerPhone": "37255511122",
    "maintenerEmail": "maintainer@mail.com"
}
my_org_ds.update(updateParams)

# Create dataset metadata
# To create dataset's metadata you can use DatasetMetadata model.
# For user's convinience parameters can be provided in camelCase manner to match 
# naming convention of the JSON that is used by Open Data.
# There are fields that are required to be filled and some don't. Optional fields can be left 
# out.
metadata: DatasetMetadata = DatasetMetadata(nameEn="new dataset", nameEt="new dataset"...)
my_org_ds.create_dataset_metadata(metadata)
# You can consider specific privacy violations for your dataset
my_org_ds.consider_privacy_violation('id')

# Or you can discard it
my_org_ds.discard_privacy_violation('id')

# Approve access permission by its ID
my_org_ds.approve_access_permission('permission_id')

# Decline access permission by its ID
my_org_ds.decline_access_permission('permission_id')
```

### Core's API
Information from [Core](https://avaandmed.eesti.ee/api/dataset-docs/#/Core) endpoints also can be retrieved.

```python
key_id = 'key_id_value'
token = 'token_value'
client = Avaandmed(api_token=token, key_id=key_id)

regions: List[Region] = client.get_regions() # return list of available regions
categories: List[Category] = client.get_categories() # returns list of available categories

# Since there are a lot of available keywords you can query keywords by providing
# some specific word and also extend/limit returned list of keywords.
# By default this methods returns just first 20 keywords.
keywords: List[KeywordInfo] = client.get_keywords(search_word='some_word', limit=5)
```

### Note on DatasetMetadata class
This class has required and optional fields. Due to amount of fields that this class contains it is easier to put documentation of that class in here rather that trying to compress it into docstring. Hence this section.

```python
class DatasetMetadata(ApiResource):
    name_et: str = Field(...)
    name_en: str = Field(...)
    description_et: str = Field(...)
    description_en: str = Field(...)
    maintainer: str = Field(...)
    maintainer_email: str = Field(...)
    maintainer_phone: str = Field(...)
    keyword_ids: List[int] = Field(...)
    category_ids: List[int] = Field(...)
    region_ids: List[int] = Field(...)
    data_from: datetime = Field(...)
    available_to: datetime = Field(...)
    update_interval_unit: UpdateIntervalUnit = Field(...)
    update_interval_frequency: int = Field(...)
    # optional fields
    conformities: Optional[List[Conformity]] = []
    lineage: Optional[str]
    spatial_representation_type: Optional[str]
    spatial_data_service_type: Optional[str]
    topic_categories: Optional[List[TopicCategory]] = []
    pixel_size: Optional[int]
    coordinate_reference_system_ids: Optional[List[int]] = []
    south_latitude: Optional[str]
    north_latitude: Optional[str]
    west_longitude: Optional[str]
    east_longitude: Optional[str]
    language: Optional[str]
    qualified_attribution: Optional[str]
    was_generated_by: Optional[str]
    spatial_resolution: Optional[str]
    temporal_resolution: Optional[str]
    maturity: Optional[str]
    parent_dataset_ids: Optional[List[str]]
    child_dataset_ids: Optional[List[str]]
    version_notes: Optional[str]
    data_to: Optional[datetime]
    landing_page: Optional[str]
    resource_type: Optional[ResourceType]
```

### File uploading
Users and Organizations can upload files for specific datasets.

However there is something that needs to kept in mind before uploading files for freshly created datasets. 

When uploading files for new datasets, make sure that dataset already has been *granted access* and *license*. Otherwise, unexpected my occur when trying to access dataset if file was uploaded beforehand.

File uploading process is same for both User's and Organization's datasets.

```python
file_name: str = 'file.csv' # This is how your file will be called in Open Data.
file_type: str = 'text/csv'
file_path: str = 'path_to_file'
dataset_id: str = 'dataset_id'

# This will return object of type File
file: File = my_datasets.upload_file(dataset_id, file_name, file_type, file_path)

# And you can obviously access different attributes of the file provided by Open Data
print(file.id)
print(file.name)
print(file.size)
```

## Development
It's recommend to use virtual enviroment during the development.

More information on virtual enviroments can be found [here](https://docs.python.org/3/library/venv.html).

```
git clone https://github.com/Michanix/avaandmed-py.git
cd avaandmed-py
pip install -r requirements.txt
```

### Run tests
[Pytest](https://docs.pytest.org/en/6.2.x/) is used for testing.

[Reponses](https://github.com/getsentry/responses) library is used for mocking responses from Avaadmed API. 

[tox](https://tox.wiki/en/latest/index.html) is used to run tests with different Python versions.

All data for testing is available in **tests/data** folder.

```
cd tests
pytest # to run all tests
pytest path/to/test_file.py # to run specific set of tests
```

Or if you want to use `tox` just run in the root of the folder and it should run tests for all Python versions specified in `tox.ini` file.
However, you probably gonna need to have multiple Python versions on your machine to test with each version. 
Otherwise it will only for tests for version that is currently installed.