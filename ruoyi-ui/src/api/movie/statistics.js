import request from '@/utils/request'

//演员票房排行
export function getActorRankStatistics(query) {
  return request({
    url: '/movie/statistics/actor/rank',
    method: 'get',
    params: query
  })
}
