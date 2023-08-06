import pandas as pd
from typing import List, Optional

from pyrasgo.utils.versioning import deprecated_without_replacement

from .error import APIError
from pyrasgo import schemas
from pyrasgo import primitives


class Get():

    def __init__(self):
        from .connection import Connection
        from pyrasgo.config import get_session_api_key
        from pyrasgo.storage import DataWarehouse, SnowflakeDataWarehouse

        api_key = get_session_api_key()
        self.api = Connection(api_key=api_key)
        self.data_warehouse: SnowflakeDataWarehouse = DataWarehouse.connect()

    @deprecated_without_replacement('v1.0')
    def collection(self, id: int) -> primitives.Collection:
        """
        Returns a Rasgo Collection (set of joined Features) matching the specified id
        """
        try:
            return primitives.Collection(api_object=self.api._get(f"/models/{id}", api_version=1).json())
        except:
            raise APIError(f"Collection {id} does not exist or this API key does not have access.")

    @deprecated_without_replacement('v1.0')
    def collection_attributes(self, id: int) -> schemas.CollectionAttributes:
        """
        Returns a dict of attributes for a collection
        """
        try:
            response = self.api._get(f"/models/{id}/attributes", api_version=1).json()
            dict_out = {}
            for kv in response:
                dict_out[kv['key']] = kv['value']
            return schemas.CollectionAttributes(collectionId=id, attributes=dict_out)
        except:
            raise APIError(f"Collection {id} does not exist or this API key does not have access.")

    @deprecated_without_replacement('v1.0')
    def collections(self, include_shared: bool=False) -> List[primitives.Collection]:
        """
        Returns all Rasgo Collections (set of joined Features) that I have author access to. Add an include_shared
        parameter to return all Rasgo Collections that I have any access to (author or shared access)
        :param include_shared: Boolean value indicating if the return should include all accessible collections
        """
        try:
            return [primitives.Collection(api_object=entry) for entry in self.api._get(f"/models", {"include_shared": include_shared}, api_version=1).json()]
        except:
            raise APIError("Collections do not exist or this API key does not have access.")

    @deprecated_without_replacement('v1.0')
    def collections_by_attribute(self, key: str, value: str = None) -> List[primitives.Collection]:
        """
        Returns a list of Rasgo Collections that match an attribute
        """
        try:
            params = {"key": key}
            if value:
                params.update({"value": value})
            response = self.api._get(f"/models/attributes/models", params=params, api_version=1).json()
            return [primitives.Collection(api_object=r) for r in response]
        except:
            raise APIError(f"Key {key}: {value or 'Any'} does not exist or this API key does not have access.")

    @deprecated_without_replacement('v1.0')
    def data_sources(self, with_features_only: bool = False) -> List[primitives.DataSource]:
        """
        Returns all DataSources available in your organization or Rasgo Community
        """
        try:
            response = self.api._get("/data-source", {"with_features_only": with_features_only}, api_version=1).json()
            return [primitives.DataSource(api_object=entry) for entry in response]
        except:
            raise APIError("Data Sources do not exist or this API key does not have access.")

    @deprecated_without_replacement('v1.0')
    def data_source(self, id: int) -> primitives.DataSource:
        """
        Returns the DataSource with the specified id
        """
        try:
            response = self.api._get(f"/data-source/{id}", api_version=1).json()
            return primitives.DataSource(api_object=response)
        except:
            raise APIError(f"Data Source {id} does not exist or this API key does not have access.")

    @deprecated_without_replacement('v1.0')
    def data_source_stats(self, id: int):
        """
        Returns the stats profile of the specificed data source
        """
        try:
            return self.api._get(f"/data-source/profile/{id}", api_version=1).json()
        except:
            raise APIError(f"Stats do not exist for DataSource {id}")

    @deprecated_without_replacement('v1.0')
    def dataframes(self) -> List[schemas.Dataframe]:
        """
        Returns all Dataframes available in your organization or Rasgo Community
        """
        try:
            response = self.api._get("/dataframes", api_version=1).json()
            return [schemas.Dataframe(**entry) for entry in response]
        except:
            raise APIError("Dataframes do not exist or this API key does not have access.")

    @deprecated_without_replacement('v1.0')
    def dataframe(self, unique_id: str) -> schemas.Dataframe:
        """
        Returns the Dataframe with the specified id
        """
        try:
            response = self.api._get(f"/dataframes/{unique_id}", api_version=1).json()
            return schemas.Dataframe(**response)
        except:
            raise APIError(f"Dataframe {unique_id} does not exist or this API key does not have access.")

    @deprecated_without_replacement('v1.0')
    def feature(self, id: int) -> primitives.Feature:
        """
        Returns the Feature with the specified id
        """
        try:
            return primitives.Feature(api_object=self.api._get(f"/features/{id}", api_version=1).json())
        except:
            raise APIError(f"Feature {id} does not exist or this API key does not have access.")

    @deprecated_without_replacement('v1.0')
    def feature_attributes(self, id: int) -> schemas.FeatureAttributes:
        """
        Returns a dict of attributes for a feature
        """
        try:
            response = self.api._get(f"/features/{id}/attributes", api_version=1).json()
            dict_out = {}
            for kv in response:
                dict_out[kv['key']] = kv['value']
            return schemas.FeatureAttributes(featureId=id, attributes=dict_out)
        except:
            raise APIError(f"Feature {id} does not exist or this API key does not have access.")

    @deprecated_without_replacement('v1.0')
    def feature_attributes_log(self, id: int) -> tuple:
        """
        Returns a list of all attributes values logged to a feature over time
        """
        try:
            response = self.api._get(f"/features/{id}/attributes/log", api_version=1).json()
            lst_out = []
            for kv in response:
                dict_item={}
                dict_item[kv['key']] = kv.get('value', None)
                dict_item['updatedBy'] = kv.get('recordAuthorId', None)
                dict_item['updated'] = kv.get('recordTimestamp', None)
                lst_out.append(dict_item)
            return schemas.FeatureAttributesLog(featureId=id, attributes=lst_out)
        except:
            raise APIError(f"Feature {id} does not exist or this API key does not have access.")


    @deprecated_without_replacement('v1.0')
    def features_yml(self, data_source_id: int) -> schemas.FeaturesYML:
        """
        Returns the Features with the specified id
        """
        try:
            response = self.data_source(data_source_id)
            return schemas.FeaturesYML(
                name = response.name,
                sourceTable = response.dataTable.fqtn,
                dimensions = [{"columnName": d.columnName, "dataType": d.dataType, "granularity": d.granularity.name} for d in response.dimensions],
                features = response.features,
                sourceCode = response.sourceCode,
                sourceType = response.sourceType
            )
        except:
            raise APIError(f"Feature {id} does not exist or this API key does not have access.")

    @deprecated_without_replacement('v1.0')
    def feature_stats(self, id: int) -> Optional[schemas.FeatureStats]:
        """
        Returns the stats profile for the specified Feature
        """
        try:
            stats_json = self.api._get(f"/features/{id}/stats", api_version=1).json()
            return schemas.FeatureStats(**stats_json["featureStats"])
        except:
            raise APIError(f"Stats do not exist yet for feature {id}.")

    @deprecated_without_replacement('v1.0')
    def features(self) -> primitives.FeatureList:
        """
        Returns a list of Features available in your organization or Rasgo Community
        """
        try:
            return primitives.FeatureList(api_object=self.api._get("/features", api_version=1).json())
        except:
            raise APIError("Features do not exist or this API key does not have access.")

    @deprecated_without_replacement('v1.0')
    def features_by_attribute(self, key: str, value: str = None) -> primitives.FeatureList:
        """
        Returns a list of features that match an attribute
        """
        try:
            params = {"key": key}
            if value:
                params.update({"value": value})
            return primitives.FeatureList(api_object=self.api._get(f"/features/attributes/features", params=params, api_version=1).json())
        except:
            raise APIError(f"Key {key}: {value or 'Any'} does not exist or this API key does not have access.")

    @deprecated_without_replacement('v1.0')
    def shared_collections(self) -> List[primitives.Collection]:
        """
        Returns all Rasgo Collections (set of joined Features) shared in my organization or in Rasgo community
        """
        try:
            return [primitives.Collection(api_object=entry) for entry in self.api._get(f"/models/shared", api_version=1).json()]
        except:
            raise APIError("Shared Collections do not exist or this API key does not have access.")

    @deprecated_without_replacement('v1.0')
    def source_columns(self, table: Optional[str] = None, database: Optional[str] = None, schema: Optional[str] = None, data_type: Optional[str] = None) -> pd.DataFrame:
        """
        Returns a DataFrame of columns in Snowflake tables and views that are queryable as feature sources
        """
        return self.data_warehouse.get_source_columns(table=table, database=database, schema=schema, data_type=data_type)

    @deprecated_without_replacement('v1.0')
    def source_tables(self, database: Optional[str] = None, schema: Optional[str] = None) -> pd.DataFrame:
        """
        Return a DataFrame of Snowflake tables and views that are queryable as feature sources
        """
        return self.data_warehouse.get_source_tables(database=database, schema=schema)

    def transform(self, transform_id: int) -> schemas.Transform:
        """Returns an individual transform"""
        try:
            response = self.api._get(f"/transform/{transform_id}", api_version=1).json()
            return schemas.Transform(**response)
        except:
            raise APIError(f"Transform with id '{transform_id}' does not exist "
                           f"or this API key does not have access.")

    def transforms(self) -> List[schemas.Transform]:
        """Returns a list of available transforms
        """
        response = self.api._get(f"/transform", api_version=1).json()
        return [schemas.Transform(**r) for r in response]

    def user(self):
        response = self.api._get("/users/me", api_version=1).json()
        return schemas.User(**response)

    def dataset(
            self,
            dataset_id: Optional[int] = None,
            fqtn: Optional[str] = None,
            resource_key: Optional[str] = None,
            version: Optional[int] = None
    ) -> primitives.Dataset:
        """
        Return a Rasgo dataset primitive by Id or FQTN
        """
        no_input_supplied = dataset_id is None and not fqtn and not resource_key
        too_many_inputs_supplied = (bool(dataset_id) + bool(fqtn) + bool(resource_key or version)) > 1
        if no_input_supplied or too_many_inputs_supplied:
            raise ValueError("Valid Dataset retrieval options are:\n"
                             "1. id\n2. fqtn\n3. resource_key\n4. resource_key and version")

        try:
            if dataset_id:
                response = self.api._get(f"/datasets/{dataset_id}", api_version=2).json()
            elif fqtn:
                response = self.api._get(f"/datasets/match/{fqtn}", api_version=2).json()
            elif resource_key:
                response = self.api._get(
                    f"/datasets/rk/{resource_key}{f'/{version}' if version else ''}",
                    api_version=2
                ).json()
            dataset_schema = schemas.Dataset(**response)

            operation_set_schema = None
            if dataset_schema.dw_operation_set_id:
                response = self.api._get(
                    f"/operation-sets/{dataset_schema.dw_operation_set_id}",
                    api_version=2
                ).json()
                operation_set_schema = schemas.OperationSet(**response)
            return primitives.Dataset(
                api_dataset=dataset_schema,
                api_operation_set=operation_set_schema
            )
        except:
            if dataset_id:
                raise APIError(f"Dataset with id '{dataset_id!r}' does not exist "
                               f"or this API key does not have access.")
            elif fqtn:
                raise APIError(f"Dataset with fqtn '{fqtn}' does not exist "
                               f"or this API key does not have access.")

    def dataset_yaml(
            self,
            dataset_id: Optional[int] = None,
    ) -> str:
        try:
            return self.api._get(f"/datasets/{dataset_id}/yaml", api_version=2).text
        except:
            raise APIError(f"Dataset with id '{dataset_id!r}' does not exist or this API key does not have access.")

    def datasets(self) -> List[primitives.Dataset]:
        """
        Return all datasets in Rasgo attached to your organization
        """
        # Get transforms  so we can cache them for use in transforming datasets
        transforms = self.transforms()
        PAGE_SIZE = 100
        offset = 0

        datasets = []
        while True:
            response = self.api._get(f"/datasets?page_size={PAGE_SIZE}&page_start={offset}", api_version=2).json()
            for r in response:
                dataset_schema = schemas.Dataset(**r)
                dataset = primitives.Dataset(
                    api_dataset=dataset_schema,
                    transforms=transforms
                )
                datasets.append(dataset)
            if len(response) < PAGE_SIZE:
                break
            offset+=PAGE_SIZE
        return datasets

    def dataset_py(self, dataset_id: int) -> str:
        """
        Return the pyrasgo code which will create an offline copy
        of a dataset (by ds id)  whether DS is in draft or
        unpublished status
        """
        resp = self.api._get(
            f"/datasets/{dataset_id}/export/python",
            api_version=2
        ).json()
        return resp

    def accelerator(self, accelerator_id: int) -> schemas.Accelerator:
        """
        Return an Accelerator with specified id
        """
        response = self.api._get(
            f"/accelerators/{accelerator_id}", api_version=2
        ).json()
        return primitives.Accelerator(
            api_accelerator=schemas.Accelerator(**response)
        )

    def accelerators(self) -> List[primitives.Accelerator]:
        """
        Return a list of all Accelerator's available to user
        """
        # Make API call get get bulk Accelerator Json objs
        response = self.api._get("/accelerators", api_version=2).json()

        # Convert response to Accelerator Primitives
        accelerators = []
        for accelerator_json in response:
            api_accelerator = schemas.AcceleratorBulk(**accelerator_json)
            accelerator = primitives.Accelerator(api_accelerator=api_accelerator)
            accelerators.append(accelerator)
        return accelerators


    # ----------------------------------
    #  Internal/Private Get Calls
    # ----------------------------------

    def _dataset_columns(self, dataset_id: int) -> List[schemas.DatasetColumn]:
        """
        Return the dataset columns for a specific dataset

        Args:
            dataset_id: Id of dataset to retrieve columns for
        """
        response = self.api._get(
            f"/dataset-columns/ds/{dataset_id}",
            api_version=2
        ).json()
        return [schemas.DatasetColumn(**x) for x in response]


    def _operation_set(self, operation_set_id: int) -> schemas.OperationSet:
        """
        Return a Rasgo operation set by id
        """
        response = self.api._get(
            f"/operation-sets/{operation_set_id}",
            api_version=2
        ).json()
        return schemas.OperationSet(**response)

    def _operation_set_async_status(self, task_id: int) -> schemas.OperationSetAsyncTask:
        """
        Returns the status of an Operation Set creation task by id
        """
        response = self.api._get(
            f"/operation-sets/async/{task_id}",
            api_version=2
        ).json()
        return schemas.OperationSetAsyncTask(**response)

    def _operation_set_offline_async_status(self, task_id: int) -> schemas.OperationSetOfflineAsyncTask:
        """
        Returns the status of an Operation Set creation task by id
        """
        response = self.api._get(
            f"/operation-sets/offline/async/{task_id}",
            api_version=2
        ).json()
        return schemas.OperationSetOfflineAsyncTask(**response)
