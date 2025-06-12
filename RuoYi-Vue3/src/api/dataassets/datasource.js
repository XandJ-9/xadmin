import request from '@/utils/request'

// 获取数据源列表
export function getDataSourceList() {
  return request({
    url: '/api/datasources/',
    method: 'get'
  })
}

// 创建数据源
export function createDataSource(data) {
  return request({
    url: '/api/datasources/',
    method: 'post',
    data
  })
}

// 更新数据源
export function updateDataSource(id, data) {
  return request({
    url: `/api/datasources/${id}/`,
    method: 'put',
    data
  })
}

// 删除数据源
export function deleteDataSource(id) {
  return request({
    url: `/api/datasources/${id}/`,
    method: 'delete'
  })
}

// 测试数据源连接
export function testDataSourceConnection(id) {
  return request({
    url: `/api/datasources/${id}/test/`,
    method: 'post'
  })
}

// 执行SQL查询
export function executeQuery(dataSourceId, data) {
  const formData = new FormData()
  formData.append('sql', data)
  
  return request({
    url: `/api/datasources/${dataSourceId}/query/`,
    method: 'post',
    data: formData
  })
}

// 获取查询日志列表
export function getQueryLogs(params) {
  return request({
    url: '/api/querylogs/',
    method: 'get',
    params
  })
}

// 获取查询日志详情
export function getQueryLogDetail(id) {
  return request({
    url: `/api/querylogs/${id}/`,
    method: 'get'
  })
}