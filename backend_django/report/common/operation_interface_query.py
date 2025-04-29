from ..models  import InterfaceInfo,InterfaceField,InterfaceQueryLog

def wrap_query_result(query_result, interface_fields:list[InterfaceField], interface_info: InterfaceInfo):
    '''
        "reportName": "数据驾驶舱",
        "interfaceName": "数据大盘基础数据"
        "code": "0",
        "isSecondTable": "0",
        "totaldata": [],
        "isTotal": "0",
        "isPaging": "0",
        "message": "success",
        "property":{},
        "data": []
    '''
    props = {}
    for field in interface_fields:
        field_info = {
                        "paraCode": field.interface_para_code,
                        "paraDesc": field.interface_para_desc,
                        "dataType": field.interface_data_type,
                        "showFlag": field.interface_show_flag,
                        "parentName": field.interface_parent_name,
                        "paraInterface": field.interface_para_interface_code,
                        "exportFlag": field.interface_export_flag,
                        "showDesc": field.interface_show_desc,
                        "position": field.interface_para_position,
                        "parentPosition": field.interface_parent_position,
                        "paraName": field.interface_para_name
        }
        props[field.interface_para_code] = field_info
    return {
        "reportName": interface_info.report.name,
        "interfaceName": interface_info.interface_name,
        "code":"0",
        "isSecondTable": interface_info.is_second_table,
        "totaldata": [],
        "isTotal": interface_info.is_total,
        "isPaging": interface_info.is_paging,
        "message": "success",
        "property": props,
        "data": query_result['data']
    }
