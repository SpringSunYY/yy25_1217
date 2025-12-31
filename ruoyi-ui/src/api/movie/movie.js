import request from '@/utils/request'





// 查询电影信息表列表
export function listMovie(query) {
  return request({
    url: '/movie/movie/list',
    method: 'get',
    params: query
  })
}

// 查询电影信息表详细
export function getMovie(id) {
  return request({
    url: '/movie/movie/' +id,
    method: 'get'
  })
}

// 新增电影信息表
export function addMovie(data) {
  return request({
    url: '/movie/movie',
    method: 'post',
    data: data
  })
}

// 修改电影信息表
export function updateMovie(data) {
  return request({
    // 后端 Flask 控制器使用的是不带主键的 PUT '' 路径，这里保持一致
    url: '/movie/movie',
    method: 'put',
    data: data
  })
}

// 删除电影信息表
export function delMovie(id) {
  return request({
    url: '/movie/movie/' +id,
    method: 'delete'
  })
}

// 电影搜索
export function searchMovie(query) {
  return request({
    url: '/movie/movie/search',
    method: 'get',
    params: query
  })
}

// 获取电影搜索选项
export function getMovieSearchOptions() {
  return request({
    url: '/movie/movie/search/options',
    method: 'get'
  })
}