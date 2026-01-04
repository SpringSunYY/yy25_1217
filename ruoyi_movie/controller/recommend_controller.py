from typing import List

from flask import g
from flask_login import login_required
from pydantic import BeforeValidator
from typing_extensions import Annotated
from werkzeug.datastructures import FileStorage

from ruoyi_common.base.model import AjaxResponse, TableResponse
from ruoyi_common.constant import HttpStatus
from ruoyi_common.descriptor.serializer import BaseSerializer, JsonSerializer
from ruoyi_common.descriptor.validator import QueryValidator, BodyValidator, PathValidator, FileDownloadValidator, \
    FileUploadValidator
from ruoyi_common.domain.enum import BusinessType
from ruoyi_common.utils.base import ExcelUtil
from ruoyi_common.utils.security_util import get_user_id, get_username
from ruoyi_framework.descriptor.log import Log
from ruoyi_framework.descriptor.permission import HasPerm, PreAuthorize
from ruoyi_movie.controller import recommend as recommend_bp
from ruoyi_movie.domain.entity import Recommend
from ruoyi_movie.service.recommend_service import RecommendService
from flask import request, g

# 使用 controller/__init__.py 中定义的蓝图
gen = recommend_bp

recommend_service = RecommendService()


def _clear_page_context():
    if hasattr(g, "criterian_meta"):
        g.criterian_meta.page = None


@gen.route('/list', methods=["GET"])
@QueryValidator(is_page=True)
@PreAuthorize(HasPerm('movie:recommend:list'))
@JsonSerializer()
def recommend_list(dto: Recommend):
    """查询用户推荐列表"""
    recommend_entity = Recommend()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(recommend_entity, attr):
            setattr(recommend_entity, attr, getattr(dto, attr))
    recommends = recommend_service.select_recommend_list(recommend_entity)
    return TableResponse(code=HttpStatus.SUCCESS, msg='查询成功', rows=recommends)


@gen.route('/<int:id>', methods=['GET'])
@PathValidator()
@PreAuthorize(HasPerm('movie:recommend:query'))
@JsonSerializer()
def get_recommend(id: int):
    """获取用户推荐详细信息"""
    recommend_entity = recommend_service.select_recommend_by_id(id)
    return AjaxResponse.from_success(data=recommend_entity)


@gen.route('', methods=['POST'])
@BodyValidator()
@PreAuthorize(HasPerm('movie:recommend:add'))
@Log(title='用户推荐管理', business_type=BusinessType.INSERT)
@JsonSerializer()
def add_recommend(dto: Recommend):
    """新增用户推荐"""
    recommend_entity = Recommend()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(recommend_entity, attr):
            setattr(recommend_entity, attr, getattr(dto, attr))
    result = recommend_service.insert_recommend(recommend_entity)
    if result > 0:
        return AjaxResponse.from_success(msg='新增成功')
    return AjaxResponse.from_error(msg='新增失败')


@gen.route('', methods=['PUT'])
@BodyValidator()
@PreAuthorize(HasPerm('movie:recommend:edit'))
@Log(title='用户推荐管理', business_type=BusinessType.UPDATE)
@JsonSerializer()
def update_recommend(dto: Recommend):
    """修改用户推荐"""
    recommend_entity = Recommend()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(recommend_entity, attr):
            setattr(recommend_entity, attr, getattr(dto, attr))
    result = recommend_service.update_recommend(recommend_entity)
    if result > 0:
        return AjaxResponse.from_success(msg='修改成功')
    return AjaxResponse.from_error(msg='修改失败')


@gen.route('/<ids>', methods=['DELETE'])
@PathValidator()
@PreAuthorize(HasPerm('movie:recommend:remove'))
@Log(title='用户推荐管理', business_type=BusinessType.DELETE)
@JsonSerializer()
def delete_recommend(ids: str):
    """删除用户推荐"""
    try:
        id_list = [int(id) for id in ids.split(',')]
        result = recommend_service.delete_recommend_by_ids(id_list)
        if result > 0:
            return AjaxResponse.from_success(msg='删除成功')
        return AjaxResponse.from_error(code=HttpStatus.ERROR, msg='删除失败')
    except Exception as e:
        return AjaxResponse.from_error(msg=f'删除失败: {str(e)}')


@gen.route('/export', methods=['POST'])
@FileDownloadValidator()
@PreAuthorize(HasPerm('movie:recommend:export'))
@Log(title='用户推荐管理', business_type=BusinessType.EXPORT)
@BaseSerializer()
def export_recommend(dto: Recommend):
    """导出用户推荐列表"""
    recommend_entity = Recommend()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(recommend_entity, attr):
            setattr(recommend_entity, attr, getattr(dto, attr))
    _clear_page_context()
    recommend_entity.page_num = None
    recommend_entity.page_size = None
    recommends = recommend_service.select_recommend_list(recommend_entity)
    # 使用ExcelUtil导出Excel文件
    excel_util = ExcelUtil(Recommend)
    return excel_util.export_response(recommends, "用户推荐数据")


@gen.route('/importTemplate', methods=['POST'])
@login_required
@BaseSerializer()
def import_template():
    """下载用户推荐导入模板"""
    excel_util = ExcelUtil(Recommend)
    return excel_util.import_template_response(sheetname="用户推荐数据")


@gen.route('/importData', methods=['POST'])
@FileUploadValidator()
@PreAuthorize(HasPerm('movie:recommend:import'))
@Log(title='用户推荐管理', business_type=BusinessType.IMPORT)
@JsonSerializer()
def import_data(
        file: List[FileStorage],
        update_support: Annotated[bool, BeforeValidator(lambda x: x != "0")]
):
    """导入用户推荐数据"""
    file = file[0]
    excel_util = ExcelUtil(Recommend)
    recommend_list = excel_util.import_file(file, sheetname="用户推荐数据")
    msg = recommend_service.import_recommend(recommend_list, update_support)
    return AjaxResponse.from_success(msg=msg)


@gen.route('/content', methods=['GET'])
@QueryValidator()
@PreAuthorize(HasPerm('movie:recommend:query'))
@JsonSerializer()
def get_recommend_content():
    """获取用户推荐内容"""
    try:
        user_id = get_user_id()
        page_num = request.args.get('pageNum', 1, type=int)
        page_size = request.args.get('pageSize', 10, type=int)

        # 获取所有推荐电影ID和分数，以及总数量
        all_movie_scores, total_count = recommend_service.get_recommend_movies_for_user(user_id)

        # 如果没有推荐数据，自动生成新的推荐
        if not all_movie_scores:
            try:
                from ruoyi_common.utils.security_util import get_username
                user_name = get_username()
                recommend_service.generate_recommendation_for_user(
                    user_id=user_id,
                    user_name=user_name,
                    genres_weight=0.3,
                    directors_weight=0.25,
                    country_weight=0.2,
                    actors_weight=0.25,
                    time_decay_factor=0.9
                )
                # 重新获取
                all_movie_scores, total_count = recommend_service.get_recommend_movies_for_user(user_id)
            except Exception as gen_error:
                print(f"自动生成推荐失败: {gen_error}")
                all_movie_scores, total_count = [], 0

        # 分页处理（使用数据库中存储的总数量）
        start_idx = (page_num - 1) * page_size
        end_idx = start_idx + page_size
        page_movie_scores = all_movie_scores[start_idx:end_idx]

        # 获取当前页面的电影ID
        page_movie_ids = [movie_id for movie_id, score in page_movie_scores]

        # 批量查询电影详细信息
        recommendations = []
        if page_movie_ids:
            from ruoyi_movie.mapper.movie_mapper import MovieMapper
            movies = MovieMapper.select_movies_by_ids(page_movie_ids)

            # 创建电影ID到电影对象的映射
            movie_dict = {movie.movie_id: movie for movie in movies}

            # 如果查询到的电影数量不匹配，跳过缺失的电影
            if len(movies) != len(page_movie_ids):
                missing_ids = set(page_movie_ids) - set(movie.movie_id for movie in movies)
                if missing_ids:
                    print(f"警告：{len(missing_ids)}部电影不存在，已跳过")

            # 计算用户偏好向量（用于维度评分计算）
            from ruoyi_movie.mapper.view_mapper import ViewMapper
            from ruoyi_movie.mapper.like_mapper import LikeMapper
            user_views = ViewMapper.select_user_views_by_user_id(user_id, days=30)
            user_likes = LikeMapper.select_user_likes_by_user_id(user_id, days=30)
            user_preference = recommend_service._calculate_user_preference(user_views, user_likes, 0.9)

            # 构建推荐结果
            for movie_id, score in page_movie_scores:
                movie_detail = movie_dict.get(movie_id)
                if not movie_detail:
                    continue

                # 计算各维度的评分详情
                dimension_scores = {}

                # 类型维度评分
                if movie_detail.genres and 'genres' in user_preference:
                    genre_score = recommend_service._calculate_dimension_similarity(
                        movie_detail.genres, user_preference['genres']
                    )
                    dimension_scores['genres'] = round(genre_score, 4)

                # 导演维度评分
                if movie_detail.directors and 'directors' in user_preference:
                    director_score = recommend_service._calculate_dimension_similarity(
                        movie_detail.directors, user_preference['directors']
                    )
                    dimension_scores['directors'] = round(director_score, 4)

                # 国家地区维度评分
                if movie_detail.country and 'country' in user_preference:
                    country_score = recommend_service._calculate_dimension_similarity(
                        movie_detail.country, user_preference['country']
                    )
                    dimension_scores['country'] = round(country_score, 4)

                # 主演维度评分
                if movie_detail.actors and 'actors' in user_preference:
                    actor_score = recommend_service._calculate_dimension_similarity(
                        movie_detail.actors, user_preference['actors']
                    )
                    dimension_scores['actors'] = round(actor_score, 4)

                movie_data = {
                    'movieId': movie_detail.movie_id or 0,
                    'title': movie_detail.title or '',
                    'rating': movie_detail.rating or 0.0,
                    'genres': movie_detail.genres or '',
                    'directors': movie_detail.directors or '',
                    'country': movie_detail.country or '',
                    'actors': movie_detail.actors or '',
                    'coverUrl': movie_detail.cover_url or '',
                    'similarityScore': round(score, 4),
                    'dimensionScores': dimension_scores
                }
                recommendations.append(movie_data)

        # 异步保存推荐记录（不阻塞响应）
        try:
            from ruoyi_common.utils.security_util import get_username
            user_name = get_username()
            recommend_service.generate_recommendation_for_user(
                user_id=user_id,
                user_name=user_name,
                genres_weight=0.3,
                directors_weight=0.25,
                country_weight=0.2,
                actors_weight=0.25,
                time_decay_factor=0.9
            )
        except Exception as save_error:
            print(f"异步保存推荐记录失败: {save_error}")

        # 返回统一格式，符合项目规范：code, msg, rows, total
        return {
            'code': HttpStatus.SUCCESS,
            'msg': '获取成功',
            'rows': recommendations,
            'total': total_count
        }

    except Exception as e:
        print(f"获取推荐内容失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return AjaxResponse.from_error(msg=f'获取推荐内容失败: {str(e)}')


