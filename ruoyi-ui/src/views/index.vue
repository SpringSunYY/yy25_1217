<template>
  <div class="home-container">
    <!-- 欢迎区域 -->
    <div class="welcome-section">
      <div class="welcome-content">
        <h1 class="welcome-title">
          <i class="el-icon-s-home"></i>
          欢迎来到电影推荐系统
        </h1>
        <p class="welcome-subtitle">发现您喜欢的电影，发现更多精彩</p>
      </div>
    </div>

    <!-- 推荐电影区域 -->
    <div class="recommendation-section">
      <MovieList
        ref="movieList"
        title="为您推荐"
        :movie-list="recommendations"
        :total="total"
        :loading="loading"
        :has-more="hasMore"
        :show-refresh="true"
        @movie-click="handleMovieClick"
        @refresh="handleRefresh"
      />

      <!-- 无限滚动加载触发器 -->
      <div v-if="hasMore" ref="loadTrigger" class="load-trigger"></div>
    </div>

  </div>
</template>

<script>
import MovieList from '@/components/MovieList.vue'
import {getUserRecommendation} from '@/api/movie/recommend'

export default {
  name: 'Index',
  components: {
    MovieList
  },
  data() {
    return {
      // 推荐电影列表
      recommendations: [],
      // 总数量
      total: 0,
      // 加载状态
      loading: false,
      loadingMore: false, // 新增：加载更多状态
      // 是否还有更多数据
      hasMore: false,
      // 分页参数
      pageParams: {
        pageNum: 1,
        pageSize: 50
      },
      // 滚动位置保存
      savedScrollTop: 0,
      // 无限滚动观察器
      observer: null
    }
  },
  computed: {},
  created() {
    this.loadRecommendations()
  },

  activated() {
    // keep-alive激活时恢复滚动位置并重新连接观察器
    this.$nextTick(() => {
      if (this.savedScrollTop > 0) {
        window.scrollTo(0, this.savedScrollTop)
      }
      // 重新连接观察器
      if (this.observer && this.$refs.loadTrigger && this.hasMore) {
        this.observer.observe(this.$refs.loadTrigger)
      }
    })
  },

  deactivated() {
    // keep-alive失活时保存滚动位置并断开观察器
    this.savedScrollTop = window.pageYOffset || document.documentElement.scrollTop
    // 断开观察器
    if (this.observer) {
      this.observer.disconnect()
    }
  },

  beforeDestroy() {
    if (this.observer) {
      this.observer.disconnect()
      this.observer = null
    }
  },
  mounted() {
    this.setupIntersectionObserver()
  },

  methods: {
    // 设置无限滚动观察器
    setupIntersectionObserver() {
      if (!window.IntersectionObserver) {
        console.warn('IntersectionObserver not supported')
        return
      }

      // 如果已存在观察器，先断开
      if (this.observer) {
        this.observer.disconnect()
      }

      this.observer = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting && this.hasMore && !this.loading && !this.loadingMore) {
              this.loadMore()
            }
          })
        },
        {
          root: null,
          rootMargin: '100px',
          threshold: 0.1
        }
      )

      // 延迟开始观察，确保DOM已渲染
      this.$nextTick(() => {
        if (this.$refs.loadTrigger) {
          this.observer.observe(this.$refs.loadTrigger)
        }
      })
    },

    // 加载推荐电影
    loadRecommendations() {
      if (this.loading && !this.loadingMore) return

      const params = {
        pageNum: this.pageParams.pageNum,
        pageSize: this.pageParams.pageSize
      }

      this.loading = !this.loadingMore
      this.loadingMore = this.loadingMore && true

      getUserRecommendation(
        this.pageParams.pageNum,
        this.pageParams.pageSize
      ).then(response => {
        if (response.code === 200) {
          // 后端返回格式：{code, msg, rows, total}
          const currentPageData = response.rows || []

          if (this.loadingMore) {
            this.recommendations = [...this.recommendations, ...currentPageData]
          } else {
            this.recommendations = currentPageData
          }

          this.total = response.total || 0

          // 检查当前页是否返回了完整的数据量
          // 如果返回的数据少于请求的数量，说明没有更多数据了
          this.hasMore = currentPageData.length === this.pageParams.pageSize &&
                        this.recommendations.length < this.total
        } else {
          this.$message.error(response.msg || '获取推荐失败')
        }
      }).catch(error => {
        this.$message.error('获取推荐失败，请稍后重试')
      }).finally(() => {
        this.loading = false
        this.loadingMore = false

        // 重新观察加载触发器
        this.$nextTick(() => {
          if (this.observer && this.$refs.loadTrigger && this.hasMore) {
            this.observer.observe(this.$refs.loadTrigger)
          }
        })
      })
    },

    // 加载更多
    loadMore() {
      if (!this.hasMore || this.loadingMore) return

      this.pageParams.pageNum++
      this.loadingMore = true
      this.loadRecommendations()
    },

    // 刷新推荐
    handleRefresh() {
      this.pageParams.pageNum = 1
      this.recommendations = []
      this.loadRecommendations()
    },

    // 处理电影点击
    handleMovieClick(movie) {
      // 跳转到电影详情页
      const routeData = this.$router.resolve({
        name: 'MovieDetail',
        params: {movieId: movie.movieId}
      });
      window.open(routeData.href, '_blank');
    }
  }
}
</script>

<style lang="scss" scoped>
.home-container {
  min-height: 100vh;
  background: #f5f5f5;
  padding: 20px;
}

/* 欢迎区域 */
.welcome-section {
  margin-bottom: 30px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  padding: 40px 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);

  .welcome-content {
    text-align: center;
    color: white;

    .welcome-title {
      font-size: 2.5rem;
      font-weight: 700;
      margin-bottom: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 15px;
      text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);

      i {
        font-size: 2.8rem;
        color: #ffd700;
        filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
      }
    }

    .welcome-subtitle {
      font-size: 1.2rem;
      opacity: 0.9;
      margin: 0;
      text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
    }
  }
}

/* 推荐区域 */
.recommendation-section {
  max-width: 1400px;
  margin: 0 auto;
}


/* 响应式设计 */
@media (max-width: 768px) {
  .home-container {
    padding: 15px;
  }

  .welcome-section .welcome-content .welcome-title {
    font-size: 2rem;

    i {
      font-size: 2.4rem;
    }
  }

  .welcome-section .welcome-content .welcome-subtitle {
    font-size: 1rem;
  }
}

@media (max-width: 480px) {
  .home-container {
    padding: 10px;
  }

  .welcome-section .welcome-content .welcome-title {
    font-size: 1.8rem;
    flex-direction: column;
    gap: 10px;

    i {
      font-size: 2rem;
    }
  }

  .welcome-section .welcome-content .welcome-subtitle {
    font-size: 0.9rem;
  }
}
</style>
