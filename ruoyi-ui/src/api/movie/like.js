import request from '@/utils/request'





// 查询用户点赞表列表
export function listLike(query) {
  return request({
    url: '/movie/like/list',
    method: 'get',
    params: query
  })
}

// 查询用户点赞表详细
export function getLike(id) {
  return request({
    url: '/movie/like/' +id,
    method: 'get'
  })
}

// 新增用户点赞表
export function addLike(data) {
  return request({
    url: '/movie/like',
    method: 'post',
    data: data
  })
}

//取消点赞
export function cancelLike(data){
  return request({
    url: '/movie/like/cancel',
    method: 'post',
    data: data
  })
}

// 修改用户点赞表
export function updateLike(data) {
  return request({
    // 后端 Flask 控制器使用的是不带主键的 PUT '' 路径，这里保持一致
    url: '/movie/like',
    method: 'put',
    data: data
  })
}

// 删除用户点赞表
export function delLike(id) {
  return request({
    url: '/movie/like/' +id,
    method: 'delete'
  })
}
