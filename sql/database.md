# 数据库设计文档

### 电影信息表：`tb_movie`

| 字段名          | 数据类型 | 长度 | 键类型 | 允许为空 | 默认值 | 描述         |
| --------------- | -------- | ---- | ------ | -------- | ------ | ------------ |
| id              | bigint   |      | 主键   | 否       |        | 编号         |
| movie_id        | bigint   |      |        | 否       |        | 电影ID       |
| title           | varchar  | 255  |        | 否       |        | 名称         |
| rating          | decimal  | 3,1  |        | 是       | NULL   | 评分         |
| view_count      | int      |      |        | 是       | 0      | 看过人数     |
| wish_count      | int      |      |        | 是       | 0      | 想看人数     |
| reviews_count   | int      |      |        | 是       | 0      | 总影评数     |
| language        | varchar  | 64   |        | 是       | NULL   | 语言         |
| country         | varchar  | 64   |        | 是       | NULL   | 国家地区     |
| directors       | varchar  | 255  |        | 是       | NULL   | 导演         |
| writers         | varchar  | 255  |        | 是       | NULL   | 编剧         |
| actors          | varchar  | 512  |        | 是       | NULL   | 主演         |
| duration        | varchar  | 64   |        | 是       | NULL   | 片长         |
| duration_minute | int      |      |        | 是       | NULL   | 片长（分钟） |
| pub_date        | varchar  | 64   |        | 是       | NULL   | 上映日期     |
| publish_date    | datetime |      |        | 是       | NULL   | 上映时间     |
| publish_year    | int      |      |        | 是       | NULL   | 上映年份     |
| genres          | varchar  | 128  |        | 是       | NULL   | 类型         |
| summary         | text     |      |        | 是       | NULL   | 剧情简介     |
| cover_url       | varchar  | 512  |        | 是       | NULL   | 封面         |
| detail_url      | varchar  | 512  |        | 是       | NULL   | 详情页       |

#### SQL
```sql
DROP TABLE IF EXISTS `tb_movie`;
CREATE TABLE `tb_movie` (
  `id` bigint NOT NULL COMMENT '编号',
  `movie_id` bigint NOT NULL COMMENT '电影ID',
  `title` varchar(255) NOT NULL COMMENT '名称',
  `rating` decimal NULL COMMENT '评分',
  `view_count` int NULL DEFAULT 0 COMMENT '看过人数',
  `wish_count` int NULL DEFAULT 0 COMMENT '想看人数',
  `reviews_count` int NULL DEFAULT 0 COMMENT '总影评数',
  `language` varchar(64) NULL COMMENT '语言',
  `country` varchar(64) NULL COMMENT '国家地区',
  `directors` varchar(255) NULL COMMENT '导演',
  `writers` varchar(255) NULL COMMENT '编剧',
  `actors` varchar(512) NULL COMMENT '主演',
  `duration` varchar(64) NULL COMMENT '片长',
  `duration_minute` int NULL COMMENT '片长（分钟）',
  `pub_date` varchar(64) NULL COMMENT '上映日期',
  `publish_date` datetime NULL COMMENT '上映时间',
  `publish_year` int NULL COMMENT '上映年份',
  `genres` varchar(128) NULL COMMENT '类型',
  `summary` text NULL COMMENT '剧情简介',
  `cover_url` varchar(512) NULL COMMENT '封面',
  `detail_url` varchar(512) NULL COMMENT '详情页',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='电影信息';
```

### 影评信息表：`tb_movie_review`

| 字段名        | 数据类型 | 长度 | 键类型 | 允许为空 | 默认值 | 描述        |
| ------------- | -------- | ---- | ------ | -------- | ------ | ----------- |
| id            | bigint   |      | 主键   | 否       |        | 编号        |
| review_id     | bigint   |      | 主键   | 否       |        | 评论ID      |
| movie_id      | bigint   |      |        | 否       |        | 电影ID      |
| type          | varchar  | 16   |        | 是       |        | 评论类型    |
| user_name     | varchar  | 64   |        | 是       | NULL   | 用户名      |
| rating_star   | int      |      |        | 是       | NULL   | 星级（1–5） |
| votes_up      | int      |      |        | 是       | 0      | 有用数      |
| votes_down    | int      |      |        | 是       | 0      | 没用数      |
| replies_count | int      |      |        | 是       | 0      | 回应数      |
| comment_time  | datetime |      |        | 是       | NULL   | 时间        |
| review_title  | varchar  | 255  |        | 是       | NULL   | 影评标题    |
| user_avatar   | varchar  | 512  |        | 是       | NULL   | 用户头像    |
| content       | text     |      |        | 是       | NULL   | 内容        |

#### SQL
```sql
DROP TABLE IF EXISTS `tb_movie_review`;
CREATE TABLE `tb_movie_review` (
  `id` bigint NOT NULL COMMENT '编号',
  `review_id` bigint NOT NULL COMMENT '评论ID',
  `movie_id` bigint NOT NULL COMMENT '电影ID',
  `type` varchar(16) NULL COMMENT '评论类型',
  `user_name` varchar(64) NULL COMMENT '用户名',
  `rating_star` int NULL COMMENT '星级（1–5）',
  `votes_up` int NULL DEFAULT 0 COMMENT '有用数',
  `votes_down` int NULL DEFAULT 0 COMMENT '没用数',
  `replies_count` int NULL DEFAULT 0 COMMENT '回应数',
  `comment_time` datetime NULL COMMENT '时间',
  `review_title` varchar(255) NULL COMMENT '影评标题',
  `user_avatar` varchar(512) NULL COMMENT '用户头像',
  `content` text NULL COMMENT '内容',
  PRIMARY KEY (`review_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='影评信息';
```

### 用户浏览表：`tb_view`

| 字段名      | 数据类型 | 长度 | 键类型 | 允许为空 | 默认值 | 描述     |
| ----------- | -------- | ---- | ------ | -------- | ------ | -------- |
| id          | bigint   |      | 主键   | 否       |        | 浏览编号 |
| user_id     | bigint   |      |        | 否       |        | 用户     |
| user_name   | varchar  | 32   |        | 否       |        | 用户名   |
| movie_id    | bigint   |      |        | 否       |        | 电影ID   |
| movie_title | varchar  | 255  |        | 是       |        | 名称     |
| cover_url   | varchar  | 512  |        | 是       | NULL   | 封面     |
| genres      | varchar  | 128  |        | 是       | NULL   | 类型     |
| directors   | varchar  | 255  |        | 是       | NULL   | 导演     |
| country     | varchar  | 64   |        | 是       | NULL   | 国家地区 |
| actors      | varchar  | 512  |        | 是       | NULL   | 主演     |
| score       | decimal  | 5,2  |        | 否       | 0      | 分数     |
| create_time | datetime |      |        | 否       |        | 创建时间 |

#### SQL
```sql
DROP TABLE IF EXISTS `tb_view`;
CREATE TABLE `tb_view` (
  `id` bigint NOT NULL COMMENT '浏览编号',
  `user_id` bigint NOT NULL COMMENT '用户',
  `user_name` varchar(32) NOT NULL COMMENT '用户名',
  `movie_id` bigint NOT NULL COMMENT '电影ID',
  `movie_title` varchar(255) NULL COMMENT '名称',
  `cover_url` varchar(512) NULL COMMENT '封面',
  `genres` varchar(128) NULL COMMENT '类型',
  `directors` varchar(255) NULL COMMENT '导演',
  `country` varchar(64) NULL COMMENT '国家地区',
  `actors` varchar(512) NULL COMMENT '主演',
  `score` decimal NOT NULL DEFAULT 0 COMMENT '分数',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户浏览';
```

### 用户点赞表：`tb_like`

| 字段名      | 数据类型 | 长度 | 键类型 | 允许为空 | 默认值 | 描述     |
| ----------- | -------- | ---- | ------ | -------- | ------ | -------- |
| id          | bigint   |      | 主键   | 否       |        | 点赞编号 |
| user_id     | bigint   |      |        | 否       |        | 用户     |
| user_name   | varchar  | 32   |        | 否       |        | 用户名   |
| movie_id    | bigint   |      |        | 否       |        | 电影ID   |
| movie_title | varchar  | 255  |        | 是       |        | 名称     |
| cover_url   | varchar  | 512  |        | 是       | NULL   | 封面     |
| genres      | varchar  | 128  |        | 是       | NULL   | 类型     |
| directors   | varchar  | 255  |        | 是       | NULL   | 导演     |
| country     | varchar  | 64   |        | 是       | NULL   | 国家地区 |
| actors      | varchar  | 512  |        | 是       | NULL   | 主演     |
| score       | decimal  | 5,2  |        | 否       | 0      | 分数     |
| create_time | datetime |      |        | 否       |        | 创建时间 |

#### SQL
```sql
DROP TABLE IF EXISTS `tb_like`;
CREATE TABLE `tb_like` (
  `id` bigint NOT NULL COMMENT '点赞编号',
  `user_id` bigint NOT NULL COMMENT '用户',
  `user_name` varchar(32) NOT NULL COMMENT '用户名',
  `movie_id` bigint NOT NULL COMMENT '电影ID',
  `movie_title` varchar(255) NULL COMMENT '名称',
  `cover_url` varchar(512) NULL COMMENT '封面',
  `genres` varchar(128) NULL COMMENT '类型',
  `directors` varchar(255) NULL COMMENT '导演',
  `country` varchar(64) NULL COMMENT '国家地区',
  `actors` varchar(512) NULL COMMENT '主演',
  `score` decimal NOT NULL DEFAULT 0 COMMENT '分数',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户点赞';
```

### 用户推荐：`tb_recommend`

| 字段名      | 数据类型 | 长度 | 键类型 | 允许为空 | 默认值 | 描述     |
| ----------- | -------- | ---- | ------ | -------- | ------ | -------- |
| id          | bigint   |      | 主键   | 否       | 自增   | 推荐编号 |
| user_id     | bigint   |      |        | 否       |        | 用户     |
| user_name   | varchar  | 32   |        | 否       |        | 用户名   |
| model_info  | text     |      |        | 否       |        | 推荐模型 |
| content     | text     |      |        | 否       |        | 推荐内容 |
| create_time | datetime |      |        | 否       |        | 创建时间 |

#### SQL
```sql
DROP TABLE IF EXISTS `tb_recommend`;
CREATE TABLE `tb_recommend` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '推荐编号',
  `user_id` bigint NOT NULL COMMENT '用户',
  `user_name` varchar(32) NOT NULL COMMENT '用户名',
  `model_info` text NOT NULL COMMENT '推荐模型',
  `content` text NOT NULL COMMENT '推荐内容',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户推荐';
```

---
## 📋 完整 SQL 汇总脚本

```sql
DROP TABLE IF EXISTS `tb_movie`;
CREATE TABLE `tb_movie` (
  `id` bigint NOT NULL COMMENT '编号',
  `movie_id` bigint NOT NULL COMMENT '电影ID',
  `title` varchar(255) NOT NULL COMMENT '名称',
  `rating` decimal NULL COMMENT '评分',
  `view_count` int NULL DEFAULT 0 COMMENT '看过人数',
  `wish_count` int NULL DEFAULT 0 COMMENT '想看人数',
  `reviews_count` int NULL DEFAULT 0 COMMENT '总影评数',
  `language` varchar(64) NULL COMMENT '语言',
  `country` varchar(64) NULL COMMENT '国家地区',
  `directors` varchar(255) NULL COMMENT '导演',
  `writers` varchar(255) NULL COMMENT '编剧',
  `actors` varchar(512) NULL COMMENT '主演',
  `duration` varchar(64) NULL COMMENT '片长',
  `duration_minute` int NULL COMMENT '片长（分钟）',
  `pub_date` varchar(64) NULL COMMENT '上映日期',
  `publish_date` datetime NULL COMMENT '上映时间',
  `publish_year` int NULL COMMENT '上映年份',
  `genres` varchar(128) NULL COMMENT '类型',
  `summary` text NULL COMMENT '剧情简介',
  `cover_url` varchar(512) NULL COMMENT '封面',
  `detail_url` varchar(512) NULL COMMENT '详情页',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='电影信息';

DROP TABLE IF EXISTS `tb_movie_review`;
CREATE TABLE `tb_movie_review` (
  `id` bigint NOT NULL COMMENT '编号',
  `review_id` bigint NOT NULL COMMENT '评论ID',
  `movie_id` bigint NOT NULL COMMENT '电影ID',
  `type` varchar(16) NULL COMMENT '评论类型',
  `user_name` varchar(64) NULL COMMENT '用户名',
  `rating_star` int NULL COMMENT '星级（1–5）',
  `votes_up` int NULL DEFAULT 0 COMMENT '有用数',
  `votes_down` int NULL DEFAULT 0 COMMENT '没用数',
  `replies_count` int NULL DEFAULT 0 COMMENT '回应数',
  `comment_time` datetime NULL COMMENT '时间',
  `review_title` varchar(255) NULL COMMENT '影评标题',
  `user_avatar` varchar(512) NULL COMMENT '用户头像',
  `content` text NULL COMMENT '内容',
  PRIMARY KEY (`review_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='影评信息';

DROP TABLE IF EXISTS `tb_view`;
CREATE TABLE `tb_view` (
  `id` bigint NOT NULL COMMENT '浏览编号',
  `user_id` bigint NOT NULL COMMENT '用户',
  `user_name` varchar(32) NOT NULL COMMENT '用户名',
  `movie_id` bigint NOT NULL COMMENT '电影ID',
  `movie_title` varchar(255) NULL COMMENT '名称',
  `cover_url` varchar(512) NULL COMMENT '封面',
  `genres` varchar(128) NULL COMMENT '类型',
  `directors` varchar(255) NULL COMMENT '导演',
  `country` varchar(64) NULL COMMENT '国家地区',
  `actors` varchar(512) NULL COMMENT '主演',
  `score` decimal NOT NULL DEFAULT 0 COMMENT '分数',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户浏览';

DROP TABLE IF EXISTS `tb_like`;
CREATE TABLE `tb_like` (
  `id` bigint NOT NULL COMMENT '点赞编号',
  `user_id` bigint NOT NULL COMMENT '用户',
  `user_name` varchar(32) NOT NULL COMMENT '用户名',
  `movie_id` bigint NOT NULL COMMENT '电影ID',
  `movie_title` varchar(255) NULL COMMENT '名称',
  `cover_url` varchar(512) NULL COMMENT '封面',
  `genres` varchar(128) NULL COMMENT '类型',
  `directors` varchar(255) NULL COMMENT '导演',
  `country` varchar(64) NULL COMMENT '国家地区',
  `actors` varchar(512) NULL COMMENT '主演',
  `score` decimal NOT NULL DEFAULT 0 COMMENT '分数',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户点赞';

DROP TABLE IF EXISTS `tb_recommend`;
CREATE TABLE `tb_recommend` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '推荐编号',
  `user_id` bigint NOT NULL COMMENT '用户',
  `user_name` varchar(32) NOT NULL COMMENT '用户名',
  `model_info` text NOT NULL COMMENT '推荐模型',
  `content` text NOT NULL COMMENT '推荐内容',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户推荐';
```

