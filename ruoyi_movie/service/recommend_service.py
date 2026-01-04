# -*- coding: utf-8 -*-
# @Author  : YY
# @FileName: recommend_service.py
# @Time    : 2026-01-02 18:33:22

from typing import List, Optional, Dict, Tuple
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import math
import json

from ruoyi_common.exception import ServiceException
from ruoyi_common.utils.base import LogUtil
from ruoyi_movie.domain.entity import Recommend, View, Like, Movie
from ruoyi_movie.mapper.recommend_mapper import RecommendMapper
from ruoyi_movie.mapper.movie_mapper import MovieMapper

class RecommendService:
    """用户推荐服务类"""
    @classmethod
    def select_recommend_list(cls, recommend: Recommend) -> List[Recommend]:
        """
        查询用户推荐列表

        Args:
            recommend (recommend): 用户推荐对象

        Returns:
            List[recommend]: 用户推荐列表
        """
        return RecommendMapper.select_recommend_list(recommend)


    @classmethod
    def select_recommend_by_id(cls, id: int) -> Optional[Recommend]:
        """
        根据ID查询用户推荐

        Args:
            id (int): 推荐编号

        Returns:
            recommend: 用户推荐对象
        """
        return RecommendMapper.select_recommend_by_id(id)

    @classmethod
    def insert_recommend(cls, recommend: Recommend) -> int:
        """
        新增用户推荐

        Args:
            recommend (recommend): 用户推荐对象

        Returns:
            int: 插入的记录数
        """
        return RecommendMapper.insert_recommend(recommend)


    @classmethod
    def update_recommend(cls, recommend: Recommend) -> int:
        """
        修改用户推荐

        Args:
            recommend (recommend): 用户推荐对象

        Returns:
            int: 更新的记录数
        """
        return RecommendMapper.update_recommend(recommend)



    @classmethod
    def delete_recommend_by_ids(cls, ids: List[int]) -> int:
        """
        批量删除用户推荐

        Args:
            ids (List[int]): ID列表

        Returns:
            int: 删除的记录数
        """
        return RecommendMapper.delete_recommend_by_ids(ids)

    @classmethod
    def import_recommend(cls, recommend_list: List[Recommend], is_update: bool = False) -> str:
        """
        导入用户推荐数据

        Args:
            recommend_list (List[recommend]): 用户推荐列表
            is_update (bool): 是否更新已存在的数据

        Returns:
            str: 导入结果消息
        """
        if not recommend_list:
            raise ServiceException("导入用户推荐数据不能为空")

        success_count = 0
        fail_count = 0
        success_msg = ""
        fail_msg = ""

        for recommend in recommend_list:
            try:
                display_value = recommend

                display_value = getattr(recommend, "id", display_value)
                existing = None
                if recommend.id is not None:
                    existing = RecommendMapper.select_recommend_by_id(recommend.id)
                if existing:
                    if is_update:
                        result = RecommendMapper.update_recommend(recommend)
                    else:
                        fail_count += 1
                        fail_msg += f"<br/> 第{fail_count}条数据，已存在：{display_value}"
                        continue
                else:
                    result = RecommendMapper.insert_recommend(recommend)

                if result > 0:
                    success_count += 1
                    success_msg += f"<br/> 第{success_count}条数据，操作成功：{display_value}"
                else:
                    fail_count += 1
                    fail_msg += f"<br/> 第{fail_count}条数据，操作失败：{display_value}"
            except Exception as e:
                fail_count += 1
                fail_msg += f"<br/> 第{fail_count}条数据，导入失败，原因：{e.__class__.__name__}"
                LogUtil.logger.error(f"导入用户推荐失败，原因：{e}")

        if fail_count > 0:
            if success_msg:
                fail_msg = f"导入成功{success_count}条，失败{fail_count}条。{success_msg}<br/>" + fail_msg
            else:
                fail_msg = f"导入成功{success_count}条，失败{fail_count}条。{fail_msg}"
            raise ServiceException(fail_msg)
        success_msg = f"恭喜您，数据已全部导入成功！共 {success_count} 条，数据如下：" + success_msg
        return success_msg

    @classmethod
    def generate_recommendation_for_user(cls, user_id: int, user_name: str = None,
                                       genres_weight: float = 0.3,
                                       directors_weight: float = 0.25,
                                       country_weight: float = 0.2,
                                       actors_weight: float = 0.25,
                                       time_decay_factor: float = 0.9) -> Optional[Recommend]:
        """
        为用户生成个性化推荐（便捷方法）

        Args:
            user_id (int): 用户ID
            user_name (str): 用户名，用于保存推荐记录
            genres_weight (float): 类型权重，默认0.3
            directors_weight (float): 导演权重，默认0.25
            country_weight (float): 国家地区权重，默认0.2
            actors_weight (float): 主演权重，默认0.25
            time_decay_factor (float): 时间衰减因子，默认0.9

        Returns:
            Optional[Recommend]: 推荐结果
        """
        weights = {
            'genres': genres_weight,
            'directors': directors_weight,
            'country': country_weight,
            'actors': actors_weight
        }

        return cls.generate_user_recommendation(
            user_id=user_id,
            user_name=user_name,  # 传递用户名用于保存记录
            weights=weights,
            time_decay_factor=time_decay_factor
        )

    @classmethod
    def generate_user_recommendation(cls, user_id: int, user_name: str = None,
                                   weights: Dict[str, float] = None,
                                   time_decay_factor: float = 0.9) -> Optional[Recommend]:
        """
        生成用户个性化推荐

        Args:
            user_id (int): 用户ID
            user_name (str): 用户名
            weights (Dict[str, float]): 各维度权重，默认为 {'genres': 0.3, 'directors': 0.25, 'country': 0.2, 'actors': 0.25}
            time_decay_factor (float): 时间衰减因子，默认为0.9（每天衰减90%）

        Returns:
            Optional[Recommend]: 推荐结果对象
        """
        try:
            # 设置默认权重
            if weights is None:
                weights = {
                    'genres': 0.3,     # 类型权重
                    'directors': 0.25, # 导演权重
                    'country': 0.2,    # 国家地区权重
                    'actors': 0.25     # 主演权重
                }

            # 获取用户最近30天的浏览和点赞记录
            user_views = RecommendMapper.select_user_views_by_user_id(user_id, days=30)
            user_likes = RecommendMapper.select_user_likes_by_user_id(user_id, days=30)

            # 获取用户已浏览/点赞的电影ID，避免重复推荐
            exclude_movie_ids = set()
            for view in user_views:
                if view.movie_id:
                    exclude_movie_ids.add(view.movie_id)
            for like in user_likes:
                if like.movie_id:
                    exclude_movie_ids.add(like.movie_id)

            # 计算用户偏好向量（始终计算，即使没有浏览记录）
            user_preference = cls._calculate_user_preference(user_views, user_likes, time_decay_factor)

            # 获取候选电影（限制数量）
            all_candidate_movies = cls._get_all_candidate_movies(user_preference, exclude_movie_ids)

            # 计算候选电影的相似度分数
            movie_scores = []
            for movie_tuple in all_candidate_movies:
                movie, base_score = movie_tuple  # 解包元组
                score = cls._calculate_similarity_score(movie, user_preference, weights)
                movie_scores.append((movie, score))

            # 按相似度排序
            movie_scores.sort(key=lambda x: x[1], reverse=True)

            # 只保留相似度大于阈值的电影，最多3000条
            min_score_threshold = 0.1  # 相似度最低阈值
            filtered_movie_scores = [item for item in movie_scores if item[1] >= min_score_threshold][:3000]

            # 确保至少有一些电影
            if not filtered_movie_scores:
                LogUtil.logger.info(f"为用户 {user_id} 未找到任何符合条件的推荐电影")
                return None

            recommended_movies = filtered_movie_scores

            # 只保存电影ID和分数的列表，确保数据格式正确
            movie_scores_list = []
            for movie, score in recommended_movies:
                movie_id = movie.movie_id
                rounded_score = round(float(score), 6)
                if isinstance(movie_id, int) and isinstance(rounded_score, float):
                    movie_scores_list.append([movie_id, rounded_score])

            recommend_content = json.dumps({
                'movie_scores': movie_scores_list,
                'total_count': len(movie_scores_list),
                'create_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }, ensure_ascii=False, separators=(',', ':'))  # 紧凑格式，避免格式问题

            # 处理user_preference，将数值精确到两位小数
            processed_preference = {}
            for dimension, prefs in user_preference.items():
                processed_preference[dimension] = {
                    key: round(value, 2) for key, value in prefs.items()
                }

            # 保存推荐结果
            recommend = Recommend(
                user_id=user_id,
                user_name=user_name,
                model_info=json.dumps({
                    'weights': weights,
                    'time_decay_factor': time_decay_factor,
                    'total_views': len(user_views),
                    'total_likes': len(user_likes),
                    'user_preference': processed_preference,  # 处理后的偏好数据
                    'generated_at': datetime.now().isoformat()
                }, ensure_ascii=False),
                content=recommend_content,
                create_time=datetime.now()
            )

            # 保存到数据库
            result = RecommendMapper.insert_recommend(recommend)
            if result > 0:
                LogUtil.logger.info(f"成功为用户 {user_id} 生成推荐")
                return recommend
            else:
                LogUtil.logger.error(f"为用户 {user_id} 保存推荐失败")
                return None

        except Exception as e:
            LogUtil.logger.error(f"生成用户 {user_id} 推荐时出错: {e}")
            return None

    @classmethod
    def _calculate_user_preference(cls, user_views: List[View], user_likes: List[Like],
                                  time_decay_factor: float) -> Dict[str, Dict[str, float]]:
        """
        计算用户偏好向量

        Args:
            user_views (List[View]): 用户浏览记录
            user_likes (List[Like]): 用户点赞记录
            time_decay_factor (float): 时间衰减因子

        Returns:
            Dict[str, Dict[str, float]]: 用户偏好向量
        """
        preference = {
            'genres': defaultdict(float),
            'directors': defaultdict(float),
            'country': defaultdict(float),
            'actors': defaultdict(float)
        }

        now = datetime.now()

        # 处理浏览记录
        for view in user_views:
            # 计算时间衰减权重
            time_weight = cls._calculate_time_weight(view.create_time, now, time_decay_factor)
            # 浏览权重设为1.0，点赞权重设为2.0
            score_weight = 1.0

            total_weight = time_weight * score_weight

            # 累加各个维度的偏好
            cls._accumulate_preference(preference, view, total_weight)

        # 处理点赞记录
        for like in user_likes:
            # 计算时间衰减权重
            time_weight = cls._calculate_time_weight(like.create_time, now, time_decay_factor)
            # 点赞权重更高
            score_weight = 2.0

            total_weight = time_weight * score_weight

            # 累加各个维度的偏好
            cls._accumulate_preference(preference, like, total_weight)

        return dict(preference)

    @classmethod
    def _calculate_time_weight(cls, create_time: datetime, now: datetime,
                              decay_factor: float) -> float:
        """
        计算时间衰减权重

        Args:
            create_time (datetime): 创建时间
            now (datetime): 当前时间
            decay_factor (float): 衰减因子

        Returns:
            float: 时间权重
        """
        if not create_time:
            return 0.5  # 默认权重

        days_diff = (now - create_time).days
        if days_diff <= 0:
            return 1.0  # 当天权重为1

        # 每天衰减decay_factor
        return math.pow(decay_factor, days_diff)

    @classmethod
    def _accumulate_preference(cls, preference: Dict[str, Dict[str, float]],
                              record: View | Like, weight: float):
        """
        累加用户偏好

        Args:
            preference (Dict[str, Dict[str, float]]): 偏好向量
            record (View | Like): 浏览或点赞记录
            weight (float): 权重
        """
        # 处理类型
        if record.genres:
            genres_list = [g.strip() for g in record.genres.split('/') if g.strip()]
            for genre in genres_list:
                preference['genres'][genre] += weight

        # 处理导演
        if record.directors:
            directors_list = [d.strip() for d in record.directors.split('/') if d.strip()]
            for director in directors_list:
                preference['directors'][director] += weight

        # 处理国家地区
        if record.country:
            countries_list = [c.strip() for c in record.country.split('/') if c.strip()]
            for country in countries_list:
                preference['country'][country] += weight

        # 处理主演
        if record.actors:
            actors_list = [a.strip() for a in record.actors.split('/') if a.strip()]
            for actor in actors_list:
                preference['actors'][actor] += weight

    @classmethod
    def _generate_recommendations(cls, user_preference: Dict[str, Dict[str, float]],
                                weights: Dict[str, float], user_views: List[View],
                                user_likes: List[Like], top_n: int = 500) -> List[Tuple[Movie, float]]:
        """
        生成推荐电影列表

        Args:
            user_preference (Dict[str, Dict[str, float]]): 用户偏好向量
            weights (Dict[str, float]): 各维度权重
            user_views (List[View]): 用户浏览记录
            user_likes (List[Like]): 用户点赞记录
            top_n (int): 返回TOP N推荐

        Returns:
            List[Tuple[Movie, float]]: (电影, 相似度分数)元组列表
        """
        # 获取用户已浏览和点赞的电影ID，避免重复推荐
        exclude_movie_ids = set()
        for view in user_views:
            if view.movie_id:
                exclude_movie_ids.add(view.movie_id)
        for like in user_likes:
            if like.movie_id:
                exclude_movie_ids.add(like.movie_id)

        # 获取候选电影
        candidate_movies = cls._get_candidate_movies(user_preference, exclude_movie_ids, min(top_n * 3, 1000))  # 最多获取1000个候选

        # 计算相似度分数
        movie_scores = []
        for movie_tuple in candidate_movies:
            movie, base_score = movie_tuple  # 解包元组
            score = cls._calculate_similarity_score(movie, user_preference, weights)
            if score > 0:
                movie_scores.append((movie, score))

        # 按相似度排序，返回TOP N
        movie_scores.sort(key=lambda x: x[1], reverse=True)
        return movie_scores[:top_n]

    @classmethod
    def _get_candidate_movies(cls, user_preference: Dict[str, Dict[str, float]],
                            exclude_movie_ids: set, limit: int) -> List[Movie]:
        """
        获取候选电影

        Args:
            user_preference (Dict[str, Dict[str, float]]): 用户偏好向量
            exclude_movie_ids (set): 排除的电影ID
            limit (int): 候选电影数量限制

        Returns:
            List[Movie]: 候选电影列表
        """
        # 从用户最偏好的维度中选择关键词
        top_genres = sorted(user_preference['genres'].items(), key=lambda x: x[1], reverse=True)[:3]
        top_directors = sorted(user_preference['directors'].items(), key=lambda x: x[1], reverse=True)[:2]
        top_countries = sorted(user_preference['country'].items(), key=lambda x: x[1], reverse=True)[:2]
        top_actors = sorted(user_preference['actors'].items(), key=lambda x: x[1], reverse=True)[:3]

        # 构建搜索条件
        genres_str = '/'.join([genre for genre, _ in top_genres]) if top_genres else None
        directors_str = '/'.join([director for director, _ in top_directors]) if top_directors else None
        country_str = '/'.join([country for country, _ in top_countries]) if top_countries else None
        actors_str = '/'.join([actor for actor, _ in top_actors]) if top_actors else None

        # 智能候选电影获取策略
        candidates = []

        # 首先尝试精确匹配（用户最偏好的维度组合）
        if genres_str or directors_str or actors_str:
            matched_movies = RecommendMapper.select_similar_movies(
                genres=genres_str,
                directors=directors_str,
                country=None,  # 先不限制国家，扩大匹配范围
                actors=actors_str,
                exclude_movie_ids=list(exclude_movie_ids),
                limit=min(limit // 2, 500)  # 精确匹配占一半配额，增加到500
            )
            # 将Movie对象转换为(Movie, score)元组，默认给较高分数
            for movie in matched_movies:
                candidates.append((movie, 0.8))  # 精确匹配给0.8的基础分数

        # 然后补充热门电影，确保有足够的候选
        remaining_limit = limit - len(candidates)
        if remaining_limit > 0:
            popular_candidates = cls._get_popular_movies(
                exclude_movie_ids=list(exclude_movie_ids) + [movie.movie_id for movie, _ in candidates],
                limit=remaining_limit
            )
            candidates.extend(popular_candidates)

        return candidates[:limit]  # 确保不超过限制

    @classmethod
    def _get_all_candidate_movies(cls, user_preference: Dict[str, Dict[str, float]],
                                exclude_movie_ids: set) -> List[Tuple[Movie, float]]:
        """
        获取所有可能的候选电影（尽可能多）

        Args:
            user_preference (Dict[str, Dict[str, float]]): 用户偏好向量
            exclude_movie_ids (set): 排除的电影ID

        Returns:
            List[Tuple[Movie, float]]: 候选电影列表
        """
        candidates = []

        # 从用户最偏好的维度中选择关键词
        top_genres = sorted(user_preference['genres'].items(), key=lambda x: x[1], reverse=True)[:5]
        top_directors = sorted(user_preference['directors'].items(), key=lambda x: x[1], reverse=True)[:3]
        top_countries = sorted(user_preference['country'].items(), key=lambda x: x[1], reverse=True)[:3]
        top_actors = sorted(user_preference['actors'].items(), key=lambda x: x[1], reverse=True)[:5]

        # 构建搜索条件
        genres_str = '/'.join([genre for genre, _ in top_genres]) if top_genres else None
        directors_str = '/'.join([director for director, _ in top_directors]) if top_directors else None
        country_str = '/'.join([country for country, _ in top_countries]) if top_countries else None
        actors_str = '/'.join([actor for actor, _ in top_actors]) if top_actors else None

        # 获取匹配的电影（限制数量，避免过度推荐）
        try:
            matched_movies = MovieMapper.select_similar_movies_by_dimensions(
                genres=genres_str,
                directors=directors_str,
                country=country_str,
                actors=actors_str,
                exclude_movie_ids=list(exclude_movie_ids),
                limit=2000  # 限制候选电影数量
            )

            # 将Movie对象转换为(Movie, score)元组
            for movie in matched_movies:
                candidates.append((movie, 0.5))  # 基础分数0.5
        except Exception as e:
            LogUtil.logger.warning(f"获取匹配电影时出错: {e}")

        # 如果没有找到匹配的电影，或者匹配电影太少，补充热门电影
        if len(candidates) < 100:
            try:
                popular_movies = cls._get_all_popular_movies(exclude_movie_ids.union({movie.movie_id for movie, _ in candidates}))
                candidates.extend(popular_movies)
            except Exception as e:
                LogUtil.logger.warning(f"获取热门电影时出错: {e}")

        return candidates

    @classmethod
    def _get_all_popular_movies(cls, exclude_movie_ids: set = None) -> List[Tuple[Movie, float]]:
        """
        获取所有热门电影（按评分和观看人数排序）

        Args:
            exclude_movie_ids (set): 排除的电影ID

        Returns:
            List[Tuple[Movie, float]]: 热门电影列表
        """
        try:
            # 获取所有电影，按热门度排序
            popular_movies = MovieMapper.select_similar_movies_by_dimensions(
                genres=None,  # 不指定任何条件
                directors=None,
                country=None,
                actors=None,
                exclude_movie_ids=list(exclude_movie_ids) if exclude_movie_ids else None,
                limit=None  # 获取所有电影
            )

            # 为热门电影设置默认分数
            movie_scores = []
            for movie in popular_movies:
                # 计算基于评分和观看人数的默认分数
                rating_score = (movie.rating or 0) / 10.0  # 评分归一化
                view_score = min((movie.view_count or 0) / 10000.0, 1.0)  # 观看人数归一化
                default_score = (rating_score * 0.7 + view_score * 0.3)  # 加权平均

                movie_scores.append((movie, default_score))

            # 按分数排序
            movie_scores.sort(key=lambda x: x[1], reverse=True)

            return movie_scores

        except Exception as e:
            LogUtil.logger.error(f"获取所有热门电影失败: {e}")
            return []

    @classmethod
    def _get_popular_movies(cls, exclude_movie_ids: List[int] = None, limit: int = 500) -> List[Tuple[Movie, float]]:
        """
        获取热门电影（当用户没有偏好数据时使用）

        Args:
            exclude_movie_ids (List[int]): 排除的电影ID
            limit (int): 返回数量限制

        Returns:
            List[Tuple[Movie, float]]: (电影, 默认分数)元组列表
        """
        try:
            # 获取热门电影（评分高、观看人数多的电影）
            from ruoyi_movie.mapper.movie_mapper import MovieMapper
            popular_movies = MovieMapper.select_similar_movies_by_dimensions(
                genres=None,  # 不指定任何条件，返回所有电影按热门度排序
                directors=None,
                country=None,
                actors=None,
                exclude_movie_ids=exclude_movie_ids,
                limit=limit
            )

            # 为热门电影设置默认相似度分数（基于评分和观看人数）
            movie_scores = []
            for movie in popular_movies:
                # 计算一个基于评分和观看人数的默认分数
                rating_score = (movie.rating or 0) / 10.0  # 评分归一化到0-1
                view_score = min((movie.view_count or 0) / 10000.0, 1.0)  # 观看人数归一化，最高1分
                default_score = (rating_score * 0.7 + view_score * 0.3)  # 加权平均

                movie_scores.append((movie, default_score))

            return movie_scores

        except Exception as e:
            LogUtil.logger.error(f"获取热门电影失败: {e}")
            return []

    @classmethod
    def _calculate_similarity_score(cls, movie: Movie,
                                  user_preference: Dict[str, Dict[str, float]],
                                  weights: Dict[str, float]) -> float:
        """
        计算电影与用户偏好的相似度分数（优化版）

        Args:
            movie (Movie): 电影对象
            user_preference (Dict[str, Dict[str, float]]): 用户偏好向量
            weights (Dict[str, float]): 各维度权重

        Returns:
            float: 相似度分数
        """
        total_score = 0.0
        dimension_scores = {}

        # 类型相似度 - 最重要的维度
        if movie.genres and 'genres' in user_preference:
            genre_score = cls._calculate_dimension_similarity(
                movie.genres, user_preference['genres']
            )
            dimension_scores['genres'] = genre_score
            total_score += genre_score * weights['genres']

        # 导演相似度
        if movie.directors and 'directors' in user_preference:
            director_score = cls._calculate_dimension_similarity(
                movie.directors, user_preference['directors']
            )
            dimension_scores['directors'] = director_score
            total_score += director_score * weights['directors']

        # 国家地区相似度
        if movie.country and 'country' in user_preference:
            country_score = cls._calculate_dimension_similarity(
                movie.country, user_preference['country']
            )
            dimension_scores['country'] = country_score
            total_score += country_score * weights['country']

        # 主演相似度
        if movie.actors and 'actors' in user_preference:
            actor_score = cls._calculate_dimension_similarity(
                movie.actors, user_preference['actors']
            )
            dimension_scores['actors'] = actor_score
            total_score += actor_score * weights['actors']

        # 增加电影质量因子（评分和观看人数）
        quality_score = cls._calculate_movie_quality_score(movie)
        total_score += quality_score * 0.1  # 质量因子权重10%

        # 增加多样性奖励
        diversity_bonus = cls._calculate_diversity_bonus(movie, dimension_scores)
        total_score += diversity_bonus

        return max(total_score, 0.0)  # 确保分数不为负数

    @classmethod
    def _calculate_movie_quality_score(cls, movie: Movie) -> float:
        """
        计算电影质量分数

        Args:
            movie (Movie): 电影对象

        Returns:
            float: 质量分数 (0-1)
        """
        quality_score = 0.0

        # 评分因子 (0-10分转换为0-1分)
        if movie.rating:
            rating_score = min(movie.rating / 10.0, 1.0)
            quality_score += rating_score * 0.6  # 60%权重

        # 观看人数因子 (归一化)
        if movie.view_count:
            # 使用对数变换，避免大数字主导评分
            view_score = min(math.log10(movie.view_count + 1) / 6.0, 1.0)  # log10(1000000)=6
            quality_score += view_score * 0.4  # 40%权重

        return quality_score

    @classmethod
    def _calculate_diversity_bonus(cls, movie: Movie, dimension_scores: Dict[str, float]) -> float:
        """
        计算多样性奖励分数

        Args:
            movie (Movie): 电影对象
            dimension_scores (Dict[str, float]): 各维度相似度分数

        Returns:
            float: 多样性奖励分数
        """
        # 如果电影在多个维度都有较高相似度，给与奖励
        high_similarity_count = sum(1 for score in dimension_scores.values() if score > 0.5)
        if high_similarity_count >= 2:
            return 0.1 * high_similarity_count  # 每多一个高相似度维度奖励0.1分

        # 如果电影包含多个类型，给与奖励
        if movie.genres and len(movie.genres.split('/')) > 2:
            return 0.05  # 类型多样性奖励

        return 0.0

    @classmethod
    def _calculate_dimension_similarity(cls, movie_values: str,
                                     user_preference: Dict[str, float]) -> float:
        """
        计算单个维度的相似度分数（优化版）

        Args:
            movie_values (str): 电影的维度值（可能包含多个值，用/分隔）
            user_preference (Dict[str, float]): 用户对该维度的偏好

        Returns:
            float: 相似度分数
        """
        if not movie_values or not user_preference:
            return 0.0

        # 解析电影的维度值
        movie_items = set(item.strip() for item in movie_values.split('/') if item.strip())

        # 计算加权匹配分数
        total_preference_weight = sum(user_preference.values())
        if total_preference_weight == 0:
            return 0.0

        matched_score = 0.0
        match_count = 0

        for item in movie_items:
            if item in user_preference:
                # 使用用户偏好权重，而不是简单匹配
                item_weight = user_preference[item]
                matched_score += item_weight
                match_count += 1

        # 归一化相似度
        if match_count == 0:
            return 0.0

        similarity = matched_score / total_preference_weight

        # 多个匹配项奖励（鼓励多样性）
        if match_count > 1:
            diversity_bonus = 0.1 * (match_count - 1)  # 每多匹配一个加10%奖励
            similarity = min(similarity * (1 + diversity_bonus), 1.0)

        # 完全匹配奖励
        if match_count == len(movie_items) and len(movie_items) > 1:
            similarity = min(similarity * 1.2, 1.0)  # 完全匹配加20%奖励

        return min(similarity, 1.0)

    @classmethod
    def _build_recommend_content(cls, recommended_movies: List[Tuple[Movie, float]],
                               user_preference: Dict[str, Dict[str, float]] = None,
                               total_count: int = 0) -> str:
        """
        构建推荐内容

        Args:
            recommended_movies (List[Tuple[Movie, float]]): 推荐电影和分数（可以是所有电影）
            user_preference (Dict[str, Dict[str, float]]): 用户偏好向量
            total_count (int): 总推荐数量

        Returns:
            str: 推荐内容JSON字符串
        """
        # 构建推荐电影列表
        movies_list = []
        for movie, score in recommended_movies:
            # 计算各维度的评分详情
            dimension_scores = {}

            # 类型维度评分
            if movie.genres and 'genres' in user_preference:
                genre_score = cls._calculate_dimension_similarity(
                    movie.genres, user_preference['genres']
                )
                dimension_scores['genres'] = round(genre_score, 4)

            # 导演维度评分
            if movie.directors and 'directors' in user_preference:
                director_score = cls._calculate_dimension_similarity(
                    movie.directors, user_preference['directors']
                )
                dimension_scores['directors'] = round(director_score, 4)

            # 国家地区维度评分
            if movie.country and 'country' in user_preference:
                country_score = cls._calculate_dimension_similarity(
                    movie.country, user_preference['country']
                )
                dimension_scores['country'] = round(country_score, 4)

            # 主演维度评分
            if movie.actors and 'actors' in user_preference:
                actor_score = cls._calculate_dimension_similarity(
                    movie.actors, user_preference['actors']
                )
                dimension_scores['actors'] = round(actor_score, 4)

            movie_data = {
                'movieId': movie.movie_id or 0,  # 驼峰命名
                'title': movie.title or '',
                'rating': movie.rating or 0.0,
                'genres': movie.genres or '',
                'directors': movie.directors or '',
                'country': movie.country or '',
                'actors': movie.actors or '',
                'coverUrl': movie.cover_url or '',  # 驼峰命名
                'similarityScore': round(score, 4),  # 驼峰命名
                'dimensionScores': dimension_scores  # 驼峰命名
            }
            movies_list.append(movie_data)

        # 返回包含total的完整数据结构
        result = {
            'movies': movies_list,
            'total': total_count,
            'saved_count': len(movies_list)
        }
        return json.dumps(result, ensure_ascii=False)

    @classmethod
    def get_recommend_movies_for_user(cls, user_id: int) -> Tuple[List[Tuple[int, float]], int]:
        """
        从数据库获取用户的推荐电影列表（电影ID和相似度分数）

        Args:
            user_id (int): 用户ID

        Returns:
            List[Tuple[int, float]]: [(movie_id, similarity_score), ...] 按相似度降序排序
        """
        try:
            # 获取用户最新的推荐记录
            recommend = RecommendMapper.select_user_recommend_history(user_id)
            if not recommend or not recommend.content:
                LogUtil.logger.info(f"用户 {user_id} 没有推荐记录")
                return [], 0

            # 解析存储的电影ID和分数列表
            try:
                content_data = json.loads(recommend.content)
            except json.JSONDecodeError as json_error:
                LogUtil.logger.error(f"用户 {user_id} 的推荐内容JSON解析失败: {json_error}, content长度: {len(recommend.content)}")
                # 尝试清理可能的特殊字符
                try:
                    cleaned_content = recommend.content.replace('\x00', '').replace('\ufeff', '')
                    content_data = json.loads(cleaned_content)
                except:
                    LogUtil.logger.error(f"用户 {user_id} 的推荐内容JSON解析失败，即使清理后也失败")
                    return []

            movie_scores = content_data.get('movie_scores', [])
            total_count = content_data.get('total_count', len(movie_scores))

            # 确保数据格式正确
            if not isinstance(movie_scores, list):
                LogUtil.logger.error(f"用户 {user_id} 的推荐内容格式错误: {type(movie_scores)}")
                return [], 0

            # 验证数据格式
            valid_scores = []
            for item in movie_scores:
                if isinstance(item, list) and len(item) == 2 and isinstance(item[0], int) and isinstance(item[1], (int, float)):
                    valid_scores.append((item[0], float(item[1])))
                else:
                    LogUtil.logger.warning(f"用户 {user_id} 的推荐数据格式无效: {item}")

            # 按相似度降序排序
            valid_scores.sort(key=lambda x: x[1], reverse=True)

            # 返回包含总数的元组
            return valid_scores, total_count

        except Exception as e:
            LogUtil.logger.error(f"获取用户 {user_id} 推荐电影列表时出错: {e}")
            import traceback
            LogUtil.logger.error(f"详细错误信息: {traceback.format_exc()}")
            return [], 0
