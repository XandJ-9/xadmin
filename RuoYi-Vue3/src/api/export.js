import { download } from '@/utils/request'

export function userImportTemplate() {
    download(
        '/system/user/importTemplate',
        `user_${new Date().getTime()}.xlsx`
    )
}

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