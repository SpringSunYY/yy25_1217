
from typing import List

from flask import g
from flask_login import login_required
from pydantic import BeforeValidator
from typing_extensions import Annotated
from werkzeug.datastructures import FileStorage

from ruoyi_common.base.model import AjaxResponse, TableResponse
from ruoyi_common.constant import HttpStatus
from ruoyi_common.descriptor.serializer import BaseSerializer, JsonSerializer
from ruoyi_common.descriptor.validator import QueryValidator, BodyValidator, PathValidator, FileDownloadValidator, FileUploadValidator
from ruoyi_common.domain.enum import BusinessType
from ruoyi_common.utils.base import ExcelUtil
from ruoyi_framework.descriptor.log import Log
from ruoyi_framework.descriptor.permission import HasPerm, PreAuthorize
from ruoyi_movie.controller import movie as movie_bp
from ruoyi_movie.domain.entity import Movie
from ruoyi_movie.service.movie_service import MovieService

# 使用 controller/__init__.py 中定义的蓝图
gen = movie_bp

movie_service = MovieService()


def _clear_page_context():
    if hasattr(g, "criterian_meta"):
        g.criterian_meta.page = None

@gen.route('/list', methods=["GET"])
@QueryValidator(is_page=True)
@PreAuthorize(HasPerm('movie:movie:list'))
@JsonSerializer()
def movie_list(dto: Movie):
    """查询电影信息表列表"""
    movie_entity = Movie()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(movie_entity, attr):
            setattr(movie_entity, attr, getattr(dto, attr))
    movies = movie_service.select_movie_list(movie_entity)
    return TableResponse(code=HttpStatus.SUCCESS, msg='查询成功', rows=movies)


@gen.route('/<int:id>', methods=['GET'])
@PathValidator()
@PreAuthorize(HasPerm('movie:movie:query'))
@JsonSerializer()
def get_movie(id: int):
    """获取电影信息表详细信息"""
    movie_entity = movie_service.select_movie_by_id(id)
    return AjaxResponse.from_success(data=movie_entity)


@gen.route('', methods=['POST'])
@BodyValidator()
@PreAuthorize(HasPerm('movie:movie:add'))
@Log(title='电影信息表管理', business_type=BusinessType.INSERT)
@JsonSerializer()
def add_movie(dto: Movie):
    """新增电影信息表"""
    movie_entity = Movie()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(movie_entity, attr):
            setattr(movie_entity, attr, getattr(dto, attr))
    result = movie_service.insert_movie(movie_entity)
    if result > 0:
        return AjaxResponse.from_success(msg='新增成功')
    return AjaxResponse.from_error(code=HttpStatus.ERROR, msg='新增失败')


@gen.route('', methods=['PUT'])
@BodyValidator()
@PreAuthorize(HasPerm('movie:movie:edit'))
@Log(title='电影信息表管理', business_type=BusinessType.UPDATE)
@JsonSerializer()
def update_movie(dto: Movie):
    """修改电影信息表"""
    movie_entity = Movie()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(movie_entity, attr):
            setattr(movie_entity, attr, getattr(dto, attr))
    result = movie_service.update_movie(movie_entity)
    if result > 0:
        return AjaxResponse.from_success(msg='修改成功')
    return AjaxResponse.from_error(code=HttpStatus.ERROR, msg='修改失败')



@gen.route('/<ids>', methods=['DELETE'])
@PathValidator()
@PreAuthorize(HasPerm('movie:movie:remove'))
@Log(title='电影信息表管理', business_type=BusinessType.DELETE)
@JsonSerializer()
def delete_movie(ids: str):
    """删除电影信息表"""
    try:
        id_list = [int(id) for id in ids.split(',')]
        result = movie_service.delete_movie_by_ids(id_list)
        if result > 0:
            return AjaxResponse.from_success(msg='删除成功')
        return AjaxResponse.from_error(code=HttpStatus.ERROR, msg='删除失败')
    except Exception as e:
        return AjaxResponse.from_error(msg=f'删除失败: {str(e)}')


@gen.route('/export', methods=['POST'])
@FileDownloadValidator()
@PreAuthorize(HasPerm('movie:movie:export'))
@Log(title='电影信息表管理', business_type=BusinessType.EXPORT)
@BaseSerializer()
def export_movie(dto: Movie):
    """导出电影信息表列表"""
    movie_entity = Movie()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(movie_entity, attr):
            setattr(movie_entity, attr, getattr(dto, attr))
    _clear_page_context()
    movie_entity.page_num = None
    movie_entity.page_size = None
    movies = movie_service.select_movie_list(movie_entity)
    # 使用ExcelUtil导出Excel文件
    excel_util = ExcelUtil(Movie)
    return excel_util.export_response(movies, "电影信息表数据")

@gen.route('/importTemplate', methods=['POST'])
@login_required
@BaseSerializer()
def import_template():
    """下载电影信息表导入模板"""
    excel_util = ExcelUtil(Movie)
    return excel_util.import_template_response(sheetname="电影信息表数据")

@gen.route('/importData', methods=['POST'])
@FileUploadValidator()
@PreAuthorize(HasPerm('movie:movie:import'))
@Log(title='电影信息表管理', business_type=BusinessType.IMPORT)
@JsonSerializer()
def import_data(
    file: List[FileStorage],
    update_support: Annotated[bool, BeforeValidator(lambda x: x != "0")]
):
    """导入电影信息表数据"""
    file = file[0]
    excel_util = ExcelUtil(Movie)
    movie_list = excel_util.import_file(file, sheetname="电影信息表数据")
    msg = movie_service.import_movie(movie_list, update_support)
    return AjaxResponse.from_success(msg=msg)