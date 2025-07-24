from datasource.models import DataSource
from datasource.executors.factory import QueryExecutorFactory
from ..models  import InterfaceInfo,InterfaceField


# class InterfaceQueryException(Exception):
#     pass


PROPERTIES = {
        "paraCode": "interface_para_code",
        "paraDesc": "interface_para_desc",
        "dataType": "interface_data_type",
        "showFlag": "interface_show_flag",
        "parentName": "interface_parent_name",
        "paraInterface": "interface_para_interface_code",
        "exportFlag": "interface_export_flag",
        "showDesc": "interface_show_desc",
        "position": "interface_para_position",
        "parentPosition": "interface_parent_position",
        "paraName": "interface_para_name"
}

DATA_PAGE = {

}

def make_field_properties(interface_field: InterfaceField):
    result = {}
    for  key, value in PROPERTIES.items():
        if hasattr(interface_field, value):
            value = getattr(interface_field, value)
        else:
            value = ''
        result[key] = value
    return result


class InterfaceQueryResult:
    """
    Represents the result of an interface query.
    """

    def __init__(self, interface: InterfaceInfo, page_no: int = 1, page_size: int = 20):
        """
        Initializes the InterfaceQueryResult with the provided data.

        :param data: A dictionary containing the query result data.
        """
        self.interface = interface
        self.page_no = page_no
        self.page_size = page_size
        self.data_result = None
        self.property_result = None
        self.query_success = False
        self.query_error = None

    def get_executor(self, interface_db_type, interface_db_name):
        datasource = DataSource.objects.filter(type=interface_db_type,database=interface_db_name).first()
        if datasource is None:
            raise Exception("数据源类型%s或者数据库%s不存在"%(interface_db_type, interface_db_name))
        executor =QueryExecutorFactory.get_executor(datasource_type=datasource.type,
                                            host=datasource.host, 
                                            port=datasource.port,
                                            database= datasource.database, 
                                            username =datasource.username, 
                                            password=datasource.password)
        return executor
    def get_result(self) -> dict:
        """
        Returns the query result data.

        :return: The data as a dictionary.
        """
        if not self.query_success:
            return {
                "code": "-1",
                "message": self.query_error if self.query_error else "Query failed"
            }
        interface_fields = InterfaceField.objects.filter(interface=self.interface)
        self.property_result = {}
        for field in interface_fields:
            self.property_result[field.interface_para_code] = make_field_properties(field)
        result = {
            "reportName": self.interface.report.name,
            "interfaceName": self.interface.interface_name,
            "isPaging": self.interface.is_paging,
            "isTotal": self.interface.is_total,
            "property": self.property_result,
            "code": "0",
            "message": "success"
        }
        if self.interface.is_paging == "1":
            result['data'] = self.data_result
        else:
            result['data'] = self.data_result.get('data',[])
            result['totaldata'] = self.data_result.get('totaldata', [])
        return result

    def execute_query(self, interface_sql: str, total_sql: str = None, offset: int = 1, limit: int = 10000) -> dict:
        """
        Executes the query and returns the result.

        :param interface_sql: The SQL query to execute.
        :param limit: The maximum number of results to return.
        :return: The query result as a dictionary.
        :raises InterfaceQueryException: If there is an error during query execution.

        """
        try:
            self.data_result = {}
            executor = self.get_executor(self.interface.interface_db_type, self.interface.interface_db_name)
            if self.interface.is_paging == "1":
                query_result = executor.execute_query_page(sql=interface_sql, page_num= offset, page_size= limit)
                self.data_result["list"]= query_result.get('data', [])
                self.data_result["total"] = query_result.get('total', 0)
                if self.interface.is_total == "1":
                    query_result = executor.execute_query_page(sql=total_sql)
                    self.data_result["totalList"] = query_result.get('data', [])
            else:
                query_result = executor.execute_query(sql=interface_sql)
                self.data_result["data"] = query_result.get('data', [])
                if self.interface.is_total == "1":
                    query_result = executor.execute_query(sql=total_sql)
                    self.data_result["totaldata"] = query_result.get('data', [])
            self.query_success = True
        except Exception as e:
            self.query_success = False
            self.query_error = str(e)
            raise e
        
        @property
        def success(self):
            return self.query_success