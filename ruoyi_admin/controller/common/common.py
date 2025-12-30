# -*- coding: utf-8 -*-
# @Author  : shaw-lee

import os
import time
import requests
from flask import request, send_from_directory, Response
from pydantic import Field
from typing_extensions import Annotated
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import NotFound

from ruoyi_common.config import RuoYiConfig
from ruoyi_common.constant import Constants
from ruoyi_common.descriptor.serializer import JsonSerializer
from ruoyi_common.descriptor.validator import FileValidator, QueryValidator
from ruoyi_common.base.model import AjaxResponse, MultiFile
from ruoyi_common.utils import FileUploadUtil, FileUtil, StringUtil
from ... import reg


@reg.api.route('/common/download')
@QueryValidator()
@JsonSerializer()
def common_download(
        file_name: Annotated[str, Field(min_length=1, max_length=100)],
        delete: Annotated[bool, Field(annotations=bool, default=False)],
):
    file_path = RuoYiConfig.download_path + file_name
    download_name = time.time() * 1000 + file_name[file_name.index("_") + 1:]
    try:
        response = send_from_directory(
            directory=RuoYiConfig.download_path,
            path=file_name,
            as_attachment=True,
            download_name=download_name,
        )
        if delete:
            FileUtil.delete_file(file_path)
    except NotFound as e:
        return AjaxResponse.from_error("文件不存在")
    except Exception as e:
        return AjaxResponse.from_error("下载失败")
    return response


@reg.api.route('/common/upload', methods=['POST'])
@FileValidator()
@JsonSerializer()
def common_upload(file: MultiFile):
    file: FileStorage = file.one()
    file_name = FileUploadUtil.upload(file, RuoYiConfig.upload_path)
    url = request.host_url[:-1] + file_name
    new_file_name = FileUploadUtil.get_filename(file_name)
    original_filename = file.filename
    ajax_response = AjaxResponse.from_success()
    # 为了兼容若依 Vue 前端，这里的字段名与 Java 版保持一致（驼峰命名）
    setattr(ajax_response, "url", url)
    setattr(ajax_response, "fileName", file_name)
    setattr(ajax_response, "newFileName", new_file_name)
    setattr(ajax_response, "originalFilename", original_filename)
    return ajax_response


@reg.api.route('/common/uploads', methods=['POST'])
@FileValidator()
@JsonSerializer()
def common_uploads(files: MultiFile):
    file_names = []
    urls = []
    new_file_names = []
    original_filenames = []
    for _, file in files.items():
        file_name = FileUploadUtil.upload(file, RuoYiConfig.upload_path)
        file_names.append(file_name)
        url = request.host_url[:-1] + file_name
        urls.append(url)
        new_file_name = FileUploadUtil.get_filename(file_name)
        new_file_names.append(new_file_name)
        original_filename = file.filename
        original_filenames.append(original_filename)
    ajax_response = AjaxResponse.from_success()
    # 多文件上传字段命名也与若依保持一致
    setattr(ajax_response, "urls", ",".join(urls))
    setattr(ajax_response, "fileNames", ",".join(file_names))
    setattr(ajax_response, "newFileNames", ",".join(new_file_names))
    setattr(ajax_response, "originalFilenames", ",".join(original_filenames))
    return ajax_response


@reg.api.route('/common/download/resource')
@QueryValidator()
@JsonSerializer()
def common_download_resource(
        resource: Annotated[str, Field(annotation=str, min_length=1, max_length=100)]
):
    download_path = RuoYiConfig.download_path + StringUtil.substring_after(resource, Constants.RESOURCE_PREFIX)
    download_name = os.path.basename(download_path)
    try:
        response = send_from_directory(
            directory=RuoYiConfig.download_path,
            path=download_path,
            as_attachment=True,
            download_name=download_name,
        )
    except NotFound as e:
        return AjaxResponse.from_error("文件不存在")
    except Exception as e:
        return AjaxResponse.from_error("下载失败")
    return response


@reg.api.route('/common/proxy-image')
@QueryValidator()
def common_proxy_image(
        url: Annotated[str, Field(min_length=1, max_length=1000)]
):
    """
    代理外部图片请求，解决前端直接访问外部图片时可能出现的403错误。

    例如：
    URL: /common/proxy-image?url=https://img9.doubanio.com/...
    """
    try:
        # 设置请求头，模拟浏览器访问
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://www.douban.com/'
        }

        # 发送请求获取图片
        response = requests.get(url, headers=headers, timeout=10, stream=True)

        if response.status_code == 200:
            # 返回图片内容，保持原始内容类型
            return Response(
                response.content,
                mimetype=response.headers.get('content-type', 'image/jpeg'),
                headers={
                    'Cache-Control': 'public, max-age=3600',  # 缓存1小时
                    'Access-Control-Allow-Origin': '*'
                }
            )
        else:
            return AjaxResponse.from_error(f"获取图片失败: {response.status_code}")

    except requests.exceptions.Timeout:
        return AjaxResponse.from_error("图片加载超时")
    except requests.exceptions.RequestException as e:
        return AjaxResponse.from_error(f"图片加载失败: {str(e)}")
    except Exception as e:
        return AjaxResponse.from_error(f"服务器错误: {str(e)}")


@reg.api.route(f"{Constants.RESOURCE_PREFIX}/<path:resource>")
def common_profile_resource(resource: str):
    """
    静态资源访问：
    将 /profile/** 映射到配置的 profile 物理目录下，与 Java 版若依保持一致。

    例如：
    ruoyi.profile = G:/ruoyi/uploadPath
    URL:  /profile/upload/2025/11/18/xxx.jpg
    实际: G:/ruoyi/uploadPath/upload/2025/11/18/xxx.jpg
    """
    try:
        return send_from_directory(
            directory=RuoYiConfig.profile,
            path=resource,
        )
    except NotFound:
        return AjaxResponse.from_error("文件不存在")
