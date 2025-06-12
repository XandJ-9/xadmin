import request from '@/utils/request'

// 平台相关API
// 获取平台列表
export function getPlatformList(params) {
  return request({
    url: '/api/report/platforms/',
    method: 'get',
    params
  })
}

// 创建平台
export function createPlatform(data) {
  return request({
    url: '/api/report/platforms/',
    method: 'post',
    data
  })
}

// 更新平台
export function updatePlatform(id, data) {
  return request({
    url: `/api/report/platforms/${id}/`,
    method: 'put',
    data
  })
}

// 删除平台
export function deletePlatform(id) {
  return request({
    url: `/api/report/platforms/${id}/`,
    method: 'delete'
  })
}

// 模块相关API
// 获取模块列表
export function getModuleList(params) {
  return request({
    url: '/api/report/modules/',
    method: 'get',
    params
  })
}

// 根据平台ID获取模块列表
export function getModulesByPlatform(platformId) {
  return request({
    url: '/api/report/modules/',
    method: 'get',
    params: { platform: platformId }
  })
}

// 创建模块
export function createModule(data) {
  return request({
    url: '/api/report/modules/',
    method: 'post',
    data
  })
}

// 更新模块
export function updateModule(id, data) {
  return request({
    url: `/api/report/modules/${id}/`,
    method: 'put',
    data
  })
}

// 删除模块
export function deleteModule(id) {
  return request({
    url: `/api/report/modules/${id}/`,
    method: 'delete'
  })
}

// 报表相关API
// 获取报表列表
export function getReportList(params) {
  return request({
    url: '/api/report/reports/',
    method: 'get',
    params
  })
}

// 创建报表
export function createReport(data) {
  return request({
    url: '/api/report/reports/',
    method: 'post',
    data
  })
}

// 更新报表
export function updateReport(id, data) {
  return request({
    url: `/api/report/reports/${id}/`,
    method: 'put',
    data
  })
}

// 删除报表
export function deleteReport(id) {
  return request({
    url: `/api/report/reports/${id}/`,
    method: 'delete'
  })
}

// 接口相关API
// 获取接口列表
export function getInterfaceList(params) {
  return request({
    url: '/api/report/interfaces/',
    method: 'get',
    params
  })
}

// 获取接口详情
export function getInterfaceDetail(id) {
  return request({
    url: `/api/report/interfaces/${id}/`,
    method: 'get'
  })
}

// 创建接口
export function createInterface(data) {
  return request({
    url: '/api/report/interfaces/',
    method: 'post',
    data
  })
}

// 更新接口
export function updateInterface(id, data) {
  return request({
    url: `/api/report/interfaces/${id}/`,
    method: 'put',
    data
  })
}

// 删除接口
export function deleteInterface(id) {
  return request({
    url: `/api/report/interfaces/${id}/`,
    method: 'delete'
  })
}

// 导出接口
export function exportInterface(id) {
  return request({
    url: `/api/report/interfaces/${id}/export/`,
    method: 'get',
    responseType: 'blob'
  })
}

// 导入接口
export function importInterface(file) {
  const formData = new FormData()
  formData.append('file', file)
  
  return request({
    url: '/api/report/import-interface/',
    method: 'post',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// 接口字段相关API
// 获取接口字段列表
export function getInterfaceFields(params) {
  return request({
    url: '/api/report/interface-fields/',
    method: 'get',
    params
  })
}

// 创建接口字段
export function createInterfaceField(data) {
  return request({
    url: '/api/report/interface-fields/',
    method: 'post',
    data
  })
}

// 更新接口字段
export function updateInterfaceField(id, data) {
  return request({
    url: `/api/report/interface-fields/${id}/`,
    method: 'put',
    data
  })
}

// 删除接口字段
export function deleteInterfaceField(id) {
  return request({
    url: `/api/report/interface-fields/${id}/`,
    method: 'delete'
  })
}

// 接口查询相关API
// 执行接口查询
export function executeInterfaceQuery(interfaceCode, data) {
  return request({
    url: `/api/report/execute-query/?interface_code=${interfaceCode}`,
    method: 'post',
    data
  })
}

// 获取接口查询日志
export function getInterfaceQueryLogs(params) {
  return request({
    url: '/api/report/interface-logs/',
    method: 'get',
    params
  })
}

// 获取接口查询日志详情
export function getInterfaceQueryLogDetail(id) {
  return request({
    url: `/api/report/interface-logs/${id}/`,
    method: 'get'
  })
}