import request from '@/utils/request'

// 获取数据源列表
export function getDataSourceList(params) {
  return request({
    url: '/datasources/',
    method: 'get',
    params
  })
}

// 创建数据源
export function createDataSource(data) {
  return request({
    url: '/datasources/',
    method: 'post',
    data
  })
}

// 更新数据源
export function updateDataSource(id, data) {
  return request({
    url: `/datasources/${id}/`,
    method: 'put',
    data
  })
}

// 删除数据源
export function deleteDataSource(id) {
  return request({
    url: `/datasources/${id}/`,
    method: 'delete'
  })
}

export function getDataSourceTypeList() {
    return request({
        url: '/datasources/types/',
        method: 'get'
    })
}

// 测试数据源连接
export function testDataSourceConnection(id) {
  return request({
    url: `/datasources/${id}/test/`,
    method: 'get'
  })
}

// 执行SQL查询
export function executeQuery(dataSourceId, data) {
  const formData = new FormData()
  formData.append('sql', data)
  
  return request({
    url: `/datasources/${dataSourceId}/query/`,
    headers: {
        'Content-Type': 'multipart/form-data'
    },
    method: 'post',
    data: formData
  })
}

// 保存SQL查询
export function saveSqlQuery(dataSourceId, name, sql) {
  return request({
    url: `/datasources/${dataSourceId}/save-query/`,
    method: 'post',
    data: {
      name,
      sql
    }
  })
}

// 获取查询日志列表
export function getQueryLogs(params) {
  return request({
    url: '/querylogs/',
    method: 'get',
    params
  })
}

// 获取查询日志详情
export function getQueryLogDetail(id) {
  return request({
    url: `/querylogs/${id}/`,
    method: 'get'
  })
}