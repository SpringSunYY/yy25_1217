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
from ruoyi_framework.descriptor.log import Log
from ruoyi_framework.descriptor.permission import HasPerm, PreAuthorize
from ruoyi_movie.controller import movie_review as movie_review_bp
from ruoyi_movie.domain.entity import MovieReview
from ruoyi_movie.service.movie_review_service import MovieReviewService

# 使用 controller/__init__.py 中定义的蓝图
gen = movie_review_bp

movie_review_service = MovieReviewService()


def _clear_page_context():
    if hasattr(g, "criterian_meta"):
        g.criterian_meta.page = None


@gen.route('/list', methods=["GET"])
@QueryValidator(is_page=True)
@PreAuthorize(HasPerm('movie:movieReview:list'))
@JsonSerializer()
def movie_review_list(dto: MovieReview):
    """查询影评信息表列表"""
    movie_review_entity = MovieReview()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(movie_review_entity, attr):
            setattr(movie_review_entity, attr, getattr(dto, attr))
    movie_reviews = movie_review_service.select_movie_review_list(movie_review_entity)
    return TableResponse(code=HttpStatus.SUCCESS, msg='查询成功', rows=movie_reviews)


@gen.route('/<int:id>', methods=['GET'])
@PathValidator()
@PreAuthorize(HasPerm('movie:movieReview:query'))
@JsonSerializer()
def get_movie_review(id: int):
    """获取影评信息表详细信息"""
    movie_review_entity = movie_review_service.select_movie_review_by_id(id)
    return AjaxResponse.from_success(data=movie_review_entity)


@gen.route('', methods=['POST'])
@BodyValidator()
@PreAuthorize(HasPerm('movie:movieReview:add'))
@Log(title='影评信息表管理', business_type=BusinessType.INSERT)
@JsonSerializer()
def add_movie_review(dto: MovieReview):
    """新增影评信息表"""
    movie_review_entity = MovieReview()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(movie_review_entity, attr):
            setattr(movie_review_entity, attr, getattr(dto, attr))
    result = movie_review_service.insert_movie_review(movie_review_entity)
    if result > 0:
        return AjaxResponse.from_success(msg='新增成功')
    return AjaxResponse.from_success( msg='新增失败')


@gen.route('', methods=['PUT'])
@BodyValidator()
@PreAuthorize(HasPerm('movie:movieReview:edit'))
@Log(title='影评信息表管理', business_type=BusinessType.UPDATE)
@JsonSerializer()
def update_movie_review(dto: MovieReview):
    """修改影评信息表"""
    movie_review_entity = MovieReview()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(movie_review_entity, attr):
            setattr(movie_review_entity, attr, getattr(dto, attr))
    result = movie_review_service.update_movie_review(movie_review_entity)
    if result > 0:
        return AjaxResponse.from_success(msg='修改成功')
    return AjaxResponse.from_error( msg='修改失败')


@gen.route('/<ids>', methods=['DELETE'])
@PathValidator()
@PreAuthorize(HasPerm('movie:movieReview:remove'))
@Log(title='影评信息表管理', business_type=BusinessType.DELETE)
@JsonSerializer()
def delete_movie_review(ids: str):
    """删除影评信息表"""
    try:
        id_list = [int(id) for id in ids.split(',')]
        result = movie_review_service.delete_movie_review_by_ids(id_list)
        if result > 0:
            return AjaxResponse.from_success(msg='删除成功')
        return AjaxResponse.from_error(code=HttpStatus.ERROR, msg='删除失败')
    except Exception as e:
        return AjaxResponse.from_error(msg=f'删除失败: {str(e)}')


@gen.route('/export', methods=['POST'])
@FileDownloadValidator()
@PreAuthorize(HasPerm('movie:movieReview:export'))
@Log(title='影评信息表管理', business_type=BusinessType.EXPORT)
@BaseSerializer()
def export_movie_review(dto: MovieReview):
    """导出影评信息表列表"""
    movie_review_entity = MovieReview()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(movie_review_entity, attr):
            setattr(movie_review_entity, attr, getattr(dto, attr))
    _clear_page_context()
    movie_review_entity.page_num = None
    movie_review_entity.page_size = None
    movie_reviews = movie_review_service.select_movie_review_list(movie_review_entity)
    # 使用ExcelUtil导出Excel文件
    excel_util = ExcelUtil(MovieReview)
    return excel_util.export_response(movie_reviews, "影评信息表数据")


@gen.route('/importTemplate', methods=['POST'])
@login_required
@BaseSerializer()
def import_template():
    """下载影评信息表导入模板"""
    excel_util = ExcelUtil(MovieReview)
    return excel_util.import_template_response(sheetname="影评信息表数据")


@gen.route('/importData', methods=['POST'])
@FileUploadValidator()
@PreAuthorize(HasPerm('movie:movieReview:import'))
@Log(title='影评信息表管理', business_type=BusinessType.IMPORT)
@JsonSerializer()
def import_data(
        file: List[FileStorage],
        update_support: Annotated[bool, BeforeValidator(lambda x: x != "0")]
):
    """导入影评信息表数据"""
    file = file[0]
    excel_util = ExcelUtil(MovieReview)
    movie_review_list = excel_util.import_file(file, sheetname="影评信息表数据")
    msg = movie_review_service.import_movie_review(movie_review_list, update_support)
    return AjaxResponse.from_success(msg=msg)
