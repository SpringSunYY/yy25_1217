<template>
  <div class="movie-list-container">
    <!-- 电影列表 -->
    <el-card class="movie-list-card" shadow="never">
      <div slot="header" class="clearfix">
        <span><i class="el-icon-film"></i> {{ title || '电影列表' }}</span>
        <span v-if="total > 0" class="result-count">共 {{ total }} 部电影</span>
      </div>

      <!-- 加载状态 -->
      <div v-if="loading && movieList.length === 0" class="loading-section">
        <el-skeleton
          :loading="loading"
          animated
          :count="6"
          :rows="4"
          :throttle="500"
        />
      </div>

      <!-- 无数据 -->
      <div v-else-if="movieList.length === 0" class="empty-section">
        <el-empty description="没有找到相关电影">
          <el-button v-if="showRefresh" type="primary" @click="handleRefresh">刷新</el-button>
        </el-empty>
      </div>

      <!-- 电影列表 -->
      <div v-else class="movie-grid">
        <div
          v-for="movie in movieList"
          :key="movie.id"
          class="movie-card"
          @click="handleMovieClick(movie)"
        >
          <div class="movie-cover">
            <image-preview :height="400" :src="movie.coverUrl" :alt="movie.title"/>
            <div class="movie-rating" v-if="movie.rating">
              <i class="el-icon-star-on"></i>
              {{ movie.rating }}
            </div>
          </div>

          <div class="movie-info">
            <h4 class="movie-title">{{ movie.title }}</h4>

            <div class="movie-meta">
              <span class="meta-year">{{ movie.publishYear }}年</span>
              <span class="meta-country" v-if="movie.country">{{ movie.country }}</span>
            </div>

            <div class="movie-genres" v-if="movie.genres">
              <span
                v-for="genre in movie.genres.split('/').slice(0, 2)"
                :key="genre"
                class="genre-tag"
              >
                {{ genre }}
              </span>
            </div>

            <div class="movie-crew">
              <div class="crew-item" v-if="movie.directors">
                <span class="crew-label">导演：</span>{{ movie.directors.split('/')[0] }}
              </div>
              <div class="crew-item" v-if="movie.writers">
                <span class="crew-label">编剧：</span>{{ movie.writers.split('/')[0] }}
              </div>
              <div class="crew-item" v-if="movie.actors">
                <span class="crew-label">主演：</span>{{ movie.actors.split('/').slice(0, 2).join('、') }}
              </div>
            </div>

            <div class="movie-details">
              <div class="detail-row" v-if="movie.pubDate">
                <span class="detail-label">上映：</span>
                <span class="detail-value">{{ movie.pubDate }}</span>
              </div>
              <div class="detail-row" v-if="movie.language">
                <span class="detail-label">语言：</span>
                <span class="detail-value">{{ movie.language.split('/').join('、') }}</span>
              </div>
            </div>

            <div class="movie-stats">
              <div class="stat-item" v-if="movie.wishCount">
                <i class="el-icon-star-off"></i>
                <span>{{ formatNumber(movie.wishCount) }}</span>
              </div>
              <div class="stat-item" v-if="movie.viewCount">
                <i class="el-icon-view"></i>
                <span>{{ formatNumber(movie.viewCount) }}</span>
              </div>
              <div class="stat-item" v-if="movie.reviewsCount">
                <i class="el-icon-chat-line-round"></i>
                <span>{{ formatNumber(movie.reviewsCount) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 加载完毕 -->
      <div v-else-if="movieList.length > 0" class="load-finished">
        <span class="finished-text">没有更多电影了</span>
      </div>
    </el-card>
  </div>
</template>

<script>
import ImagePreview from "@/components/ImagePreview/index.vue";

export default {
  name: 'MovieList',
  components: {ImagePreview},
  props: {
    // 标题
    title: {
      type: String,
      default: '电影列表'
    },
    // 电影列表数据
    movieList: {
      type: Array,
      default: () => []
    },
    // 总数量
    total: {
      type: Number,
      default: 0
    },
    // 加载状态
    loading: {
      type: Boolean,
      default: false
    },
    // 是否还有更多数据
    hasMore: {
      type: Boolean,
      default: false
    },
    // 是否显示刷新按钮
    showRefresh: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      // 无限滚动观察器由父组件管理
    }
  },
  mounted() {
    // IntersectionObserver现在由父组件处理
  },
  methods: {

    // 处理电影点击
    handleMovieClick(movie) {
      this.$emit('movie-click', movie)
    },

    // 处理刷新
    handleRefresh() {
      this.$emit('refresh')
    },

    // 格式化数字
    formatNumber(num) {
      if (num >= 10000) {
        return (num / 10000).toFixed(1) + '万'
      }
      return num.toString()
    }
  }
}
</script>

<style lang="scss" scoped>
.movie-list-container {
  width: 100%;
}

.movie-list-card {
  ::v-deep .el-card__header {
    background-color: #fafafa;
    border-bottom: 1px solid #ebeef5;
    padding: 15px 20px;

    .result-count {
      float: right;
      color: #666;
      font-size: 14px;
    }
  }

  ::v-deep .el-card__body {
    padding: 20px;
  }
}

.loading-section,
.empty-section {
  text-align: center;
  padding: 40px 0;
}

.movie-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
}

.load-finished {
  text-align: center;
  color: #999;
  font-size: 14px;
  margin: 20px 0;
}

/* 电影卡片 */
.movie-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  transition: all 0.25s ease;
  cursor: pointer;

  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
  }

  .movie-cover {
    position: relative;
    height: 260px;
    overflow: hidden;

    img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.25s ease;
    }

    .movie-rating {
      position: absolute;
      top: 8px;
      right: 8px;
      background: linear-gradient(135deg, #ffd700, #ffb347);
      color: #333;
      padding: 4px 8px;
      border-radius: 16px;
      font-size: 12px;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 3px;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);

      i {
        color: #ff6b35;
        font-size: 11px;
      }
    }
  }

  &:hover .movie-cover img {
    transform: scale(1.03);
  }

  .movie-info {
    padding: 16px;

    .movie-title {
      font-size: 16px;
      font-weight: 600;
      color: #1f2937;
      margin: 0 0 10px 0;
      line-height: 1.4;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }

    .movie-meta {
      display: flex;
      gap: 6px;
      margin-bottom: 10px;

      .meta-year,
      .meta-country {
        background: #f3f4f6;
        color: #6b7280;
        padding: 3px 6px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: 500;
      }
    }

    .movie-genres {
      margin-bottom: 8px;

      .genre-tag {
        display: inline-block;
        background: #eff6ff;
        color: #3b82f6;
        padding: 2px 6px;
        border-radius: 8px;
        font-size: 11px;
        font-weight: 500;
        margin-right: 4px;
        margin-bottom: 4px;
      }
    }

    .movie-crew {
      .crew-item {
        font-size: 12px;
        color: #6b7280;
        margin-bottom: 4px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;

        .crew-label {
          color: #9ca3af;
          font-weight: 500;
        }
      }
    }

    .movie-details {
      margin-bottom: 10px;

      .detail-row {
        display: flex;
        align-items: center;
        font-size: 12px;
        margin-bottom: 4px;

        .detail-label {
          color: #9ca3af;
          font-weight: 500;
          min-width: 35px;
          flex-shrink: 0;
        }

        .detail-value {
          color: #4b5563;
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
        }
      }
    }

    .movie-stats {
      display: flex;
      gap: 12px;

      .stat-item {
        display: flex;
        align-items: center;
        gap: 4px;
        font-size: 12px;
        color: #6b7280;
        font-weight: 500;

        i {
          color: #9ca3af;
          font-size: 13px;
        }
      }
    }
  }
}

/* 加载触发器 */
.load-trigger {
  height: 20px;
  margin: 20px 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .movie-grid {
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 16px;
  }
}

@media (max-width: 480px) {
  .movie-grid {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 12px;
  }

  .movie-card {
    .movie-cover {
      height: 220px;
    }

    .movie-info {
      padding: 12px;

      .movie-title {
        font-size: 14px;
        margin-bottom: 6px;
      }

      .movie-genres .genre-tag {
        font-size: 10px;
        padding: 2px 4px;
        margin-right: 3px;
        margin-bottom: 3px;
      }

      .movie-crew .crew-item {
        font-size: 11px;
        margin-bottom: 3px;
      }

      .movie-details .detail-row {
        font-size: 11px;
        margin-bottom: 3px;

        .detail-label {
          min-width: 30px;
        }
      }

      .movie-stats {
        gap: 8px;

        .stat-item {
          font-size: 11px;

          i {
            font-size: 12px;
          }
        }
      }
    }
  }
}
</style>
