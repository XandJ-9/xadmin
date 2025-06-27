import { download } from '@/utils/request'

// 导出文件
export function exportUser(params, data) {
    download(
        '/system/user/export',
        `user_${new Date().getTime()}.xlsx`,
        params,
        data
    )
}


export function exportRole(params, data) {
    download(
        '/system/role/export',
        `role_${new Date().getTime()}.xlsx`,
        params,
        data
    )
}