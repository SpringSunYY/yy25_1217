import request from '@/utils/request'

//演员票房排行
export function getActorRankStatistics(query) {
  return request({
    url: '/movie/statistics/actor/rank',
    method: 'get',
    params: query
  })
}

//导演排行
export function getDirectorRankStatistics(query) {
  return request({
    url: '/movie/statistics/director/rank',
    method: 'get',
    params: query
  })
}

//电影排行
export function getMovieRankStatistics(query) {
  return request({
    url: '/movie/statistics/movie/rank',
    method: 'get',
    params: query
  })
}


//分类排行
export function getGenresRankStatistics(query) {
  return request({
    url: '/movie/statistics/genres/rank',
    method: 'get',
    params: query
  })
}
