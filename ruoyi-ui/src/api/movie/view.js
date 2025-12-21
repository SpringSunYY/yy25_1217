import request from '@/utils/request'





// 查询用户浏览列表
export function listView(query) {
  return request({
    url: '/movie/view/list',
    method: 'get',
    params: query
  })
}

// 查询用户浏览详细
export function getView(id) {
  return request({
    url: '/movie/view/' +id,
    method: 'get'
  })
}

// 新增用户浏览
export function addView(data) {
  return request({
    url: '/movie/view',
    method: 'post',
    data: data
  })
}

// 修改用户浏览
export function updateView(data) {
  return request({
    // 后端 Flask 控制器使用的是不带主键的 PUT '' 路径，这里保持一致
    url: '/movie/view',
    method: 'put',
    data: data
  })
}

// 删除用户浏览
export function delView(id) {
  return request({
    url: '/movie/view/' +id,
    method: 'delete'
  })
}