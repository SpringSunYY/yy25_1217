import request from '@/utils/request'





// 查询影评信息表列表
export function listMovieReview(query) {
  return request({
    url: '/movie/movieReview/list',
    method: 'get',
    params: query
  })
}

// 查询影评信息表详细
export function getMovieReview(reviewId) {
  return request({
    url: '/movie/movieReview/' +reviewId,
    method: 'get'
  })
}

// 新增影评信息表
export function addMovieReview(data) {
  return request({
    url: '/movie/movieReview',
    method: 'post',
    data: data
  })
}

// 修改影评信息表
export function updateMovieReview(data) {
  return request({
    // 后端 Flask 控制器使用的是不带主键的 PUT '' 路径，这里保持一致
    url: '/movie/movieReview',
    method: 'put',
    data: data
  })
}

// 删除影评信息表
export function delMovieReview(reviewId) {
  return request({
    url: '/movie/movieReview/' +reviewId,
    method: 'delete'
  })
}