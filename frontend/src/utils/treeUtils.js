/**
 * 工具方法：将扁平的菜单数据转换为树形结构
 * @param {Array} data 扁平的菜单数据数组
 * @param {Object} options 配置选项
 * @param {String} options.idKey 唯一标识字段名，默认为'id'
 * @param {String} options.parentKey 父节点标识字段名，默认为'parent'
 * @param {String} options.childrenKey 子节点数组字段名，默认为'children'
 * @returns {Array} 转换后的树形结构数据
 */
export const listToTree = (data, options = {}) => {
  // 默认配置
  const {
    idKey = 'id',
    parentKey = 'parent',
    childrenKey = 'children'
  } = options

  // 如果数据为空，直接返回空数组
  if (!data || !Array.isArray(data) || data.length === 0) {
    return []
  }

  // 创建一个映射表，用于快速查找节点
  const map = {}
  data.forEach(item => {
    map[item[idKey]] = { ...item }
  })

  // 存储结果的数组
  const result = []

  // 遍历数据，构建树形结构
  data.forEach(item => {
    const id = item[idKey]
    const parentId = item[parentKey]
    const node = map[id]

    // 初始化子节点数组
    if (!node[childrenKey]) {
      node[childrenKey] = []
    }

    // 如果是根节点（没有父节点或父节点不存在），则直接添加到结果数组
    if (parentId === null || parentId === undefined || !map[parentId]) {
      result.push(node)
    } else {
      // 如果有父节点，则添加到父节点的children数组中
      if (!map[parentId][childrenKey]) {
        map[parentId][childrenKey] = []
      }
      map[parentId][childrenKey].push(node)
    }
  })

  return result
}

/**
 * 工具方法：将树形结构数据转换为扁平数组
 * @param {Array} treeData 树形结构数据
 * @param {Object} options 配置选项
 * @param {String} options.childrenKey 子节点数组字段名，默认为'children'
 * @returns {Array} 转换后的扁平数组
 */
export const treeToList = (treeData, options = {}) => {
  const { childrenKey = 'children' } = options
  const result = []

  // 如果数据为空，直接返回空数组
  if (!treeData || !Array.isArray(treeData) || treeData.length === 0) {
    return result
  }

  // 递归函数，用于遍历树形结构
  const flatten = (items) => {
    items.forEach(item => {
      // 创建一个不包含children的新对象
      const { [childrenKey]: children, ...rest } = item
      result.push(rest)

      // 如果有子节点，则递归处理
      if (children && Array.isArray(children) && children.length > 0) {
        flatten(children)
      }
    })
  }

  flatten(treeData)
  return result
}

/**
 * 工具方法：根据指定条件查找树形结构中的节点
 * @param {Array} treeData 树形结构数据
 * @param {Function} predicate 判断函数，返回true表示找到目标节点
 * @param {Object} options 配置选项
 * @param {String} options.childrenKey 子节点数组字段名，默认为'children'
 * @returns {Object|null} 找到的节点或null
 */
export const findNodeInTree = (treeData, predicate, options = {}) => {
  const { childrenKey = 'children' } = options

  // 如果数据为空，直接返回null
  if (!treeData || !Array.isArray(treeData) || treeData.length === 0) {
    return null
  }

  // 递归函数，用于遍历树形结构
  const find = (items) => {
    for (const item of items) {
      // 如果当前节点满足条件，则返回
      if (predicate(item)) {
        return item
      }

      // 如果有子节点，则递归查找
      if (item[childrenKey] && Array.isArray(item[childrenKey]) && item[childrenKey].length > 0) {
        const found = find(item[childrenKey])
        if (found) {
          return found
        }
      }
    }
    return null
  }

  return find(treeData)
}