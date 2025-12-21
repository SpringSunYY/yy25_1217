# -*- coding: utf-8 -*-
# @Module: movie
# @Author: YY

def init_app(app):
    """
    初始化模块，注册蓝图
    
    Args:
        app: Flask应用实例
    """
    # 导入 controller 模块，自动注册所有蓝图
    # 使用 pythonModelName 生成 Python 导入路径
    from ruoyi_movie.controller import view
    app.register_blueprint(view)
    # 使用 pythonModelName 生成 Python 导入路径
    from ruoyi_movie.controller import recommend
    app.register_blueprint(recommend)
    # 使用 pythonModelName 生成 Python 导入路径
    from ruoyi_movie.controller import movie_review
    app.register_blueprint(movie_review)
    # 使用 pythonModelName 生成 Python 导入路径
    from ruoyi_movie.controller import movie
    app.register_blueprint(movie)
    # 使用 pythonModelName 生成 Python 导入路径
    from ruoyi_movie.controller import like
    app.register_blueprint(like)