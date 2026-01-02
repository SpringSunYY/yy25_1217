<template>
  <div class="movie-search-container">
    <!-- 搜索区域 -->
    <div class="search-section">
      <div class="search-wrapper">
        <!-- 主搜索框 -->
        <div class="main-search">
          <div class="search-input-container">
            <div class="search-input-wrapper">
              <el-input
                v-model="searchParams.title"
                placeholder="搜索电影名称..."
                size="large"
                clearable
                @input="debouncedSearch"
                @keyup.enter.native="handleSearch"
                :loading="searching"
                class="main-search-input"
              >
              </el-input>

              <!-- 搜索状态指示器 -->
              <div v-if="searching" class="search-loading">
                <i class="el-icon-loading"></i>
              </div>
            </div>

            <!-- 排序控制 -->
            <div class="sort-selector">
              <el-dropdown @command="handleSortChange" trigger="click">
                <el-button type="text" class="sort-button">
                  <i class="el-icon-sort"></i>
                  {{ getSortText() }}
                  <i class="el-icon-arrow-down el-icon--right"></i>
                </el-button>
                <el-dropdown-menu slot="dropdown">
                  <el-dropdown-item command="view_count_desc">
                    <i class="el-icon-view"></i> 热度↓
                  </el-dropdown-item>
                  <el-dropdown-item command="view_count_asc">
                    <i class="el-icon-view"></i> 热度↑
                  </el-dropdown-item>
                  <el-dropdown-item command="rating_desc">
                    <i class="el-icon-star-off"></i> 评分↓
                  </el-dropdown-item>
                  <el-dropdown-item command="rating_asc">
                    <i class="el-icon-star-off"></i> 评分↑
                  </el-dropdown-item>
                  <el-dropdown-item command="publish_year_desc">
                    <i class="el-icon-date"></i> 年份↓
                  </el-dropdown-item>
                  <el-dropdown-item command="publish_year_asc">
                    <i class="el-icon-date"></i> 年份↑
                  </el-dropdown-item>
                </el-dropdown-menu>
              </el-dropdown>
            </div>
          </div>
        </div>

        <!-- 高级筛选 -->
        <div class="advanced-filters">
          <div class="filter-row">
            <!-- 导演编剧主演搜索 -->
            <div class="people-search">
              <el-input
                v-model="searchParams.directors"
                placeholder="导演"
                size="small"
                clearable
                @input="handleSearch"
                class="people-input"
              />
              <el-input
                v-model="searchParams.writers"
                placeholder="编剧"
                size="small"
                clearable
                @input="handleSearch"
                class="people-input"
              />
              <el-input
                v-model="searchParams.actors"
                placeholder="主演"
                size="small"
                clearable
                @input="handleSearch"
                class="people-input"
              />
            </div>

            <!-- 年份筛选 -->
            <div class="year-filter">
              <span class="filter-label">年份：</span>
              <div class="year-tags">
                <el-tag
                  v-for="yearRange in searchOptions.yearRanges"
                  :key="'year-' + yearRange.value"
                  :type="searchParams.yearRange === yearRange.value ? 'primary' : ''"
                  @click="searchParams.yearRange = searchParams.yearRange === yearRange.value ? '' : yearRange.value; handleSearch()"
                  class="year-tag"
                  size="small"
                >
                  {{ yearRange.label }}
                </el-tag>
              </div>
            </div>
          </div>
        </div>

        <!-- 筛选标签 -->
        <div class="filter-section">
          <!-- 类型筛选 -->
          <div class="filter-category">
            <div class="category-header">
              <span class="category-title">
                <i class="el-icon-price-tag"></i>
                电影类型
              </span>
            </div>
            <div class="category-content">
              <div class="tag-cloud">
                <el-tag
                  v-for="genre in visibleGenres"
                  :key="'genre-' + genre"
                  :type="searchParams.genres.includes(genre) ? 'primary' : ''"
                  @click="toggleGenre(genre)"
                  class="genre-tag"
                  size="small"
                >
                  {{ genre }}
                </el-tag>
              </div>
              <div class="category-footer" v-if="searchOptions.genres.length > 20">
                <el-button
                  v-if="!showAllGenres"
                  type="text"
                  size="mini"
                  @click="showAllGenres = true"
                  class="expand-btn"
                >
                  <i class="el-icon-plus"></i>
                  显示更多 ({{ searchOptions.genres.length - 20 }})
                </el-button>
                <el-button
                  v-if="showAllGenres"
                  type="text"
                  size="mini"
                  @click="showAllGenres = false"
                  class="collapse-btn"
                >
                  <i class="el-icon-minus"></i>
                  收起
                </el-button>
              </div>
            </div>
          </div>

          <!-- 地区筛选 -->
          <div class="filter-category">
            <div class="category-header">
              <span class="category-title">
                <i class="el-icon-location-outline"></i>
                国家地区
              </span>
            </div>
            <div class="category-content">
              <div class="tag-cloud">
                <el-tag
                  v-for="country in visibleCountries"
                  :key="'country-' + country"
                  :type="searchParams.countries.includes(country) ? 'primary' : ''"
                  @click="toggleCountry(country)"
                  class="country-tag"
                  size="small"
                >
                  {{ country }}
                </el-tag>
              </div>
              <div class="category-footer" v-if="searchOptions.countries.length > 24">
                <el-button
                  v-if="!showAllCountries"
                  type="text"
                  size="mini"
                  @click="showAllCountries = true"
                  class="expand-btn"
                >
                  <i class="el-icon-plus"></i>
                  显示更多 ({{ searchOptions.countries.length - 24 }})
                </el-button>
                <el-button
                  v-if="showAllCountries"
                  type="text"
                  size="mini"
                  @click="showAllCountries = false"
                  class="collapse-btn"
                >
                  <i class="el-icon-minus"></i>
                  收起
                </el-button>
              </div>
            </div>
          </div>
        </div>

        <!-- 已选条件展示 -->
        <div class="active-filters-bar" v-if="hasActiveFilters">
          <div class="active-filters-content">
            <span class="active-label">
              <i class="el-icon-check"></i>
              已选条件:
            </span>
            <div class="active-tags-wrapper">
              <el-tag
                v-for="genre in searchParams.genres"
                :key="'active-genre-' + genre"
                type="primary"
                size="mini"
                closable
                @close="toggleGenre(genre)"
                class="active-tag"
              >
                类型: {{ genre }}
              </el-tag>
              <el-tag
                v-for="country in searchParams.countries"
                :key="'active-country-' + country"
                type="success"
                size="mini"
                closable
                @close="toggleCountry(country)"
                class="active-tag"
              >
                地区: {{ country }}
              </el-tag>
              <el-tag
                v-if="searchParams.yearRange"
                type="warning"
                size="mini"
                closable
                @close="searchParams.yearRange = ''; handleSearch()"
                class="active-tag"
              >
                年份: {{ getYearRangeLabel(searchParams.yearRange) }}
              </el-tag>
            </div>
            <el-button
              type="text"
              size="mini"
              @click="resetSearch"
              class="clear-all-btn"
            >
              <i class="el-icon-delete"></i>
              清空全部
            </el-button>
          </div>
        </div>
      </div>
    </div>

    <!-- 电影列表 -->
    <el-card class="movie-list-card" shadow="never">
      <div slot="header" class="clearfix">
        <span><i class="el-icon-film"></i> 搜索结果</span>
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
          <el-button type="primary" @click="resetSearch">清空条件</el-button>
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

      <!-- 无限滚动加载触发器 -->
      <div v-if="hasMore" ref="loadTrigger" class="load-trigger"></div>

      <!-- 加载完毕 -->
      <div v-else-if="movieList.length > 0" class="load-finished">
        <span class="finished-text">没有更多电影了</span>
      </div>
    </el-card>
  </div>
</template>

<script>

import {getMovieDetail, getMovieSearchOptions, searchMovie} from '@/api/movie/movie'
import ImagePreview from "@/components/ImagePreview/index.vue";

export default {
  name: 'Index',
  components: {ImagePreview},
  data() {
    return {
      // 搜索参数
      searchParams: {
        title: '',
        genres: [],
        countries: [],
        yearRange: '',
        directors: '',
        writers: '',
        actors: '',
        sortField: 'view_count',
        sortOrder: 'desc',
        pageNum: 1,
        pageSize: 20
      },
      // 搜索选项
      searchOptions: {
        genres: [],
        countries: [],
        yearRanges: [],
        sortOptions: []
      },
      // 电影列表
      movieList: [],
      // 总数量
      total: 0,
      // 加载状态
      loading: false,
      loadingMore: false,
      // 是否还有更多数据
      hasMore: true,
      // 防抖定时器
      searchTimer: null,
      // 国家搜索相关
      showCountryInput: false,
      countrySearchText: '',
      filteredCountries: [],
      // 排序状态
      sortField: 'view_count',
      sortOrder: 'desc',
      // 展开状态
      showAllGenres: false,
      showAllCountries: false,
      // 搜索状态
      searching: false,
      // 无限滚动观察器
      observer: null
    }
  },
  computed: {
    hasActiveFilters() {
      return this.searchParams.genres.length > 0 ||
        this.searchParams.countries.length > 0 ||
        this.searchParams.yearRange ||
        this.searchParams.directors ||
        this.searchParams.actors
    },

    visibleGenres() {
      return this.showAllGenres ? this.searchOptions.genres : this.searchOptions.genres.slice(0, 20)
    },

    visibleCountries() {
      return this.showAllCountries ? this.searchOptions.countries : this.searchOptions.countries.slice(0, 24)
    }
  },
  mounted() {
    this.setupIntersectionObserver()
  },

  activated() {
    // keep-alive激活时重新连接观察器
    this.$nextTick(() => {
      if (this.observer && this.$refs.loadTrigger) {
        this.observer.observe(this.$refs.loadTrigger)
      }
    })
  },

  deactivated() {
    // keep-alive失活时断开观察器
    if (this.observer) {
      this.observer.disconnect()
    }
  },

  beforeDestroy() {
    if (this.observer) {
      this.observer.disconnect()
    }
  },

  created() {
    this.getSearchOptions()
    this.handleSearch()
  },
  methods: {
    // 获取搜索选项
    getSearchOptions() {
      getMovieSearchOptions().then(response => {
        if (response.code === 200) {
          this.searchOptions = response.data
        }
      }).catch(() => {
        this.$message.error('获取搜索选项失败')
      })
    },

    // 处理搜索
    handleSearch() {
      // 防抖处理
      if (this.searchTimer) {
        clearTimeout(this.searchTimer)
      }
      this.searchTimer = setTimeout(() => {
        this.searchParams.pageNum = 1
        this.movieList = []
        this.hasMore = true

        this.searchMovies()
      }, 500)
    },

    // 处理排序变化
    handleSortChange(command) {
      const sortMapping = {
        'view_count_desc': {field: 'view_count', order: 'desc'},
        'view_count_asc': {field: 'view_count', order: 'asc'},
        'rating_desc': {field: 'rating', order: 'desc'},
        'rating_asc': {field: 'rating', order: 'asc'},
        'publish_year_desc': {field: 'publish_year', order: 'desc'},
        'publish_year_asc': {field: 'publish_year', order: 'asc'}
      }

      if (sortMapping[command]) {
        this.searchParams.sortField = sortMapping[command].field
        this.searchParams.sortOrder = sortMapping[command].order
        this.handleSearch()
      }
    },

    // 获取排序显示文本
    getSortText() {
      const fieldMap = {
        'view_count': '热度',
        'rating': '评分',
        'publish_year': '年份'
      }
      const orderMap = {
        'desc': '↓',
        'asc': '↑'
      }
      const fieldText = fieldMap[this.searchParams.sortField] || '热度'
      const orderText = orderMap[this.searchParams.sortOrder] || '↓'
      return `${fieldText}${orderText}`
    },

    // 获取年份区间标签
    getYearRangeLabel(value) {
      const yearRange = this.searchOptions.yearRanges.find(yr => yr.value === value)
      return yearRange ? yearRange.label : value
    },

    // 搜索电影
    searchMovies() {
      if (this.loading && !this.loadingMore) return

      const params = {
        ...this.searchParams,
        genres: this.searchParams.genres.join(','),
        country: this.searchParams.countries.join('/'),
        year_range: this.searchParams.yearRange,
        sort_field: this.searchParams.sortField,
        sort_order: this.searchParams.sortOrder
      }

      this.loading = !this.loadingMore
      this.loadingMore = this.loadingMore && true
      this.searching = !this.loadingMore

      searchMovie(params).then(response => {
        if (response.code === 200) {
          const newMovies = response.rows || []
          if (this.loadingMore) {
            this.movieList = [...this.movieList, ...newMovies]
          } else {
            this.movieList = newMovies
            this.total = response.total || 0
          }

          // 判断是否还有更多数据
          this.hasMore = newMovies.length === this.searchParams.pageSize
        }
      }).catch(() => {
        this.$message.error('搜索失败')
      }).finally(() => {
        this.loading = false
        this.loadingMore = false
        this.searching = false

        // 重新观察加载触发器
        this.$nextTick(() => {
          if (this.observer && this.$refs.loadTrigger) {
            this.observer.observe(this.$refs.loadTrigger)
          }
        })
      })
    },

    // 加载更多
    loadMore() {
      if (!this.hasMore || this.loadingMore) return

      this.searchParams.pageNum++
      this.loadingMore = true
      this.searchMovies()
    },

    // 处理电影点击
    handleMovieClick(movie) {
      // 跳转到电影详情页，打开一下个新页面
      const routeData = this.$router.resolve({
        name: 'MovieDetail',
        params: {movieId: movie.movieId}
      });
      window.open(routeData.href, '_blank');
    },


    // 格式化数字
    formatNumber(num) {
      if (num >= 10000) {
        return (num / 10000).toFixed(1) + '万'
      }
      return num.toString()
    },

    // 切换类型选择
    toggleGenre(genre) {
      const index = this.searchParams.genres.indexOf(genre)
      if (index > -1) {
        this.searchParams.genres.splice(index, 1)
      } else {
        this.searchParams.genres.push(genre)
      }
      this.handleSearch()
    },

    // 切换国家选择
    toggleCountry(country) {
      const index = this.searchParams.countries.indexOf(country)
      if (index > -1) {
        this.searchParams.countries.splice(index, 1)
      } else {
        this.searchParams.countries.push(country)
      }
      this.handleSearch()
    },

    // 过滤国家
    filterCountries() {
      if (!this.countrySearchText) {
        this.filteredCountries = []
        return
      }
      this.filteredCountries = this.searchOptions.countries.filter(country =>
        country.toLowerCase().includes(this.countrySearchText.toLowerCase())
      )
    },

    // 防抖搜索
    debouncedSearch() {
      if (this.searchTimer) {
        clearTimeout(this.searchTimer)
      }
      this.searchTimer = setTimeout(() => {
        this.handleSearch()
      }, 500)
    },

    // 设置无限滚动观察器
    setupIntersectionObserver() {
      if (!window.IntersectionObserver) {
        console.warn('IntersectionObserver not supported')
        return
      }

      this.observer = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting && this.hasMore && !this.loadingMore) {
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
    },

    // 确保页面可以滚动
    ensurePageScrollable() {
      // 确保body和html可以滚动
      const body = document.body
      const html = document.documentElement

      // 移除可能导致无法滚动的样式
      body.style.overflow = ''
      body.style.height = ''
      html.style.overflow = ''
      html.style.height = ''

      // 确保容器可以滚动
      const container = this.$el
      if (container) {
        container.style.overflow = ''
        container.style.height = ''
      }

      // 强制重新计算布局
      this.$nextTick(() => {
        window.scrollTo(0, 0)
      })
    },

    // 重置搜索条件
    resetSearch() {
      this.searchParams = {
        title: '',
        genres: [],
        countries: [],
        yearRange: '',
        directors: '',
        writers: '',
        actors: '',
        sortField: 'view_count',
        sortOrder: 'desc',
        pageNum: 1,
        pageSize: 20
      }
      this.showAllGenres = false
      this.showAllCountries = false
      this.handleSearch()
    }
  }
}
</script>

<style lang="scss" scoped>
.movie-search-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 20px;
  /* 确保容器可以滚动 */
  overflow-y: auto;
  overflow-x: hidden;
}

/* 确保页面滚动正常 */
:global(body) {
  overflow-y: auto !important;
  overflow-x: hidden !important;
  height: auto !important;
}

:global(html) {
  overflow-y: auto !important;
  overflow-x: hidden !important;
  height: auto !important;
}

/* 搜索区域 */
.search-section {
  max-width: 100%;
  margin: 0 auto;

  .search-wrapper {
    background: white;
    border-radius: 16px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    margin-bottom: 24px;

    .main-search {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      padding: 40px 30px;
      position: relative;

      &::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="search-bg" width="20" height="20" patternUnits="userSpaceOnUse"><circle cx="10" cy="10" r="1" fill="rgba(255,255,255,0.1)"/></pattern></defs><rect width="100" height="100" fill="url(%23search-bg)"/></svg>');
        opacity: 0.5;
      }

      .search-input-container {
        position: relative;
        z-index: 2;
        display: flex;
        align-items: center;
        gap: 20px;

        .search-input-wrapper {
          flex: 1;
          position: relative;

          .main-search-input {
            width: 100%;

            ::v-deep .el-input__inner {
              height: 60px;
              border-radius: 30px;
              border: 3px solid rgba(255, 255, 255, 0.3);
              background: rgba(255, 255, 255, 0.95);
              font-size: 18px;
              font-weight: 500;
              color: #333;
              backdrop-filter: blur(10px);
              transition: all 0.3s ease;
              position: relative;

              &:focus {
                border-color: #fff;
                box-shadow: 0 0 0 4px rgba(255, 255, 255, 0.3);
                background: white;
                transform: scale(1.02);
              }

              &::placeholder {
                color: #64748b;
                font-weight: 400;
              }

              &:hover {
                border-color: rgba(255, 255, 255, 0.5);
              }
            }

            ::v-deep .el-input__prefix {
              color: #667eea;
              font-size: 20px;
            }
          }

          .search-loading {
            position: absolute;
            right: 20px;
            top: 50%;
            transform: translateY(-50%);
            color: #667eea;

            i {
              font-size: 20px;
              animation: rotating 2s linear infinite;
            }
          }

          @keyframes rotating {
            0% {
              transform: rotate(0deg);
            }
            100% {
              transform: rotate(360deg);
            }
          }
        }

        .sort-selector {
          .sort-button {
            background: rgba(255, 255, 255, 0.2);
            border: 2px solid rgba(255, 255, 255, 0.3);
            color: white;
            padding: 12px 20px;
            border-radius: 25px;
            font-weight: 500;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
            white-space: nowrap;

            &:hover {
              background: rgba(255, 255, 255, 0.3);
              border-color: rgba(255, 255, 255, 0.5);
            }

            i {
              margin-right: 6px;
            }
          }
        }
      }
    }

    .advanced-filters {
      background: #f8fafc;
      border-top: 1px solid #e2e8f0;

      .filter-row {
        padding: 20px 30px;
        display: flex;
        align-items: center;
        gap: 30px;

        .people-search {
          display: flex;
          gap: 12px;
          flex: 1;

          .people-input {
            flex: 1;

            ::v-deep .el-input__inner {
              border-radius: 8px;
              border: 1px solid #d1d5db;
              transition: all 0.2s ease;

              &:focus {
                border-color: #667eea;
                box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.1);
              }
            }
          }
        }

        .year-filter {
          display: flex;
          align-items: center;
          gap: 12px;

          .filter-label {
            font-size: 14px;
            font-weight: 600;
            color: #374151;
            white-space: nowrap;
          }

          .year-tags {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;

            .year-tag {
              cursor: pointer;
              transition: all 0.2s ease;

              &:hover {
                transform: translateY(-1px);
              }

              &.el-tag--primary {
                background-color: #667eea;
                border-color: #667eea;
              }
            }
          }
        }
      }
    }
  }

  .filter-section {
    display: grid;
    padding: 10px 20px;
    grid-template-columns: 1fr 1fr;
    gap: 24px;

    .filter-category {
      background: white;
      border-radius: 12px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
      overflow: hidden;

      .category-header {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 16px 20px;
        color: white;

        .category-title {
          font-size: 16px;
          font-weight: 600;
          display: flex;
          align-items: center;
          gap: 8px;

          i {
            font-size: 18px;
          }
        }
      }

      .category-content {
        padding: 20px;

        .tag-cloud {
          display: flex;
          flex-wrap: wrap;
          gap: 8px;

          .genre-tag,
          .country-tag {
            cursor: pointer;
            transition: all 0.3s ease;
            border: 1px solid #e2e8f0;

            &:hover {
              transform: translateY(-2px);
              box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            }

            &.el-tag--primary {
              background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
              border-color: #667eea;
              color: white;
              font-weight: 500;
            }
          }

          .more-button {
            color: #667eea;
            font-size: 12px;
            padding: 4px 8px;
            border-radius: 4px;
            transition: all 0.2s ease;
            align-self: center;
            margin-top: 8px;

            &:hover {
              background-color: rgba(102, 126, 234, 0.1);
              color: #4f46e5;
            }

            i {
              font-size: 11px;
              margin-left: 4px;
            }
          }
        }
      }
    }
  }
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

.load-more-section {
  text-align: center;
  margin: 20px 0;
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
      //margin-bottom: 10px;

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

/* 国家标签样式 */
.country-tags {
  max-height: 200px;
  overflow-y: auto;

  .country-tag {
    cursor: pointer;
    margin: 4px 4px 0 0;
    transition: all 0.2s ease;

    &:hover {
      transform: scale(1.05);
    }
  }

  .selected-countries {
    margin-top: 12px;
    padding: 8px;
    background: #f8f9fa;
    border-radius: 4px;

    .selected-label {
      font-size: 12px;
      color: #666;
      margin-right: 8px;
    }

    .selected-tag {
      margin: 2px 2px 0 0;
    }
  }
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .movie-search-container {
    padding: 15px;
  }

  .filter-row {
    flex-direction: column;
    align-items: stretch;
    gap: 20px;

    .people-search {
      order: 2;
    }

    .year-filter {
      order: 1;
      justify-content: flex-start;
    }
  }

  .filter-section {
    grid-template-columns: 1fr;
    gap: 20px;
  }
}

@media (max-width: 768px) {
  .movie-search-container {
    padding: 10px;
  }

  .search-wrapper .main-search {
    padding: 30px 20px;
  }

  .search-input-container {
    flex-direction: column;
    gap: 16px;

    .sort-selector {
      align-self: stretch;
      display: flex;
      justify-content: center;
    }
  }

  .main-search-input {
    ::v-deep .el-input__inner {
      height: 50px;
      font-size: 16px;
    }
  }

  .filter-row {
    padding: 16px 20px;
    gap: 16px;
  }

  .people-search {
    flex-direction: column;
    gap: 8px;

    .people-input {
      width: 100%;
    }
  }

  .filter-section .filter-category .category-content {
    padding: 16px;
  }

  .movie-grid {
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 16px;
  }
}

@media (max-width: 480px) {
  .search-wrapper .main-search {
    padding: 24px 16px;
  }

  .main-search-input {
    ::v-deep .el-input__inner {
      height: 46px;
      font-size: 15px;
    }
  }

  .sort-button {
    padding: 10px 16px;
    font-size: 14px;
  }

  .filter-row {
    padding: 12px 16px;
  }

  .movie-grid {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 12px;
  }

  .tag-cloud {
    gap: 6px;

    .genre-tag,
    .country-tag {
      font-size: 12px;
      padding: 4px 8px;
    }
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

/* 已选条件条样式 */
.active-filters-bar {
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  border: 1px solid #0ea5e9;
  border-radius: 8px;
  padding: 12px 16px;
  margin: 20px;
  position: relative;

  &::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 4px;
    background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
    border-radius: 4px 0 0 4px;
  }

  .active-filters-content {
    display: flex;
    align-items: center;
    gap: 12px;

    .active-label {
      font-size: 14px;
      font-weight: 600;
      color: #0c4a6e;
      white-space: nowrap;
      display: flex;
      align-items: center;
      gap: 6px;

      i {
        color: #0ea5e9;
        font-size: 16px;
      }
    }

    .active-tags-wrapper {
      flex: 1;
      display: flex;
      flex-wrap: wrap;
      gap: 6px;

      .active-tag {
        font-size: 12px;
        border-radius: 4px;
      }
    }

    .clear-all-btn {
      font-size: 12px;
      color: #dc2626;
      padding: 4px 8px;
      border-radius: 4px;
      transition: all 0.2s ease;
      white-space: nowrap;

      &:hover {
        background-color: #fef2f2;
        color: #b91c1c;
      }

      i {
        font-size: 11px;
      }
    }
  }
}

/* 分类内容底部样式 */
.category-footer {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #f3f4f6;

  .expand-btn,
  .collapse-btn {
    color: #667eea;
    font-size: 12px;
    transition: all 0.2s ease;

    &:hover {
      color: #4f46e5;
      background-color: rgba(102, 126, 234, 0.05);
    }

    i {
      font-size: 11px;
      margin-right: 4px;
    }
  }
}
</style>
