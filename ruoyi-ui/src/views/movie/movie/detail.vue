<template>
  <div class="movie-detail">
    <!-- 电影信息 -->
    <div class="movie-info" v-if="movie.movieId">
      <!-- 电影封面 -->
      <div class="movie-cover-section" v-if="movie.coverUrl">
        <div class="movie-cover-wrapper" @click="openDetailUrl">
          <img :src="getProxyImageUrl(movie.coverUrl)" :alt="movie.title" class="movie-cover-img"/>
          <div class="cover-overlay">
            <i class="el-icon-link"></i>
            <span>查看详情</span>
          </div>
        </div>
      </div>

      <div class="movie-header">
        <h1 class="movie-title">{{ movie.title }}</h1>
        <div class="movie-actions">
          <button class="like-btn" :class="{ 'liked': isLiked }" @click="handleLike">
            <i :class="isLiked ? 'el-icon-star-on' : 'el-icon-star-off'"></i>
            <span>{{ isLiked ? '已点赞' : '点赞' }}</span>
          </button>
        </div>
      </div>

      <div class="movie-stats">
        <span class="rating">评分：{{ movie.rating }}/10</span>
        <span class="view-count">看过：{{ movie.viewCount }}人</span>
        <span class="wish-count">想看：{{ movie.wishCount }}人</span>
        <span class="reviews-count">影评：{{ movie.reviewsCount }}条</span>
      </div>

      <div class="movie-meta">
        <div class="meta-row">
          <div class="meta-item">
            <label>导演：</label>
            <span>{{ movie.directors }}</span>
          </div>
          <div class="meta-item">
            <label>编剧：</label>
            <span>{{ movie.writers }}</span>
          </div>
        </div>
        <div class="meta-row">
          <div class="meta-item">
            <label>主演：</label>
            <span>{{ movie.actors }}</span>
          </div>
          <div class="meta-item">
            <label>类型：</label>
            <span>{{ movie.genres }}</span>
          </div>
        </div>
        <div class="meta-row">
          <div class="meta-item">
            <label>国家地区：</label>
            <span>{{ movie.country }}</span>
          </div>
          <div class="meta-item">
            <label>语言：</label>
            <span>{{ movie.language }}</span>
          </div>
        </div>
        <div class="meta-row">
          <div class="meta-item">
            <label>上映时间：</label>
            <span>{{ movie.pubDate }}</span>
          </div>
          <div class="meta-item">
            <label>片长：</label>
            <span>{{ movie.duration }}</span>
          </div>
        </div>
      </div>

      <div class="movie-description">
        <h3>剧情简介</h3>
        <p>{{ movie.summary }}</p>
      </div>
    </div>

    <!-- 电影评论 -->
    <div class="movie-reviews" v-if="movieReview.length > 0">
      <h2 class="reviews-title">影评 ({{ movieReview.length }})</h2>

      <!-- 长评 -->
      <div class="reviews-section" v-if="longReviews.length > 0">
        <h3 class="section-title">长评 ({{ longReviews.length }})</h3>
        <div class="review-item long-review" v-for="review in longReviews" :key="review.id">
          <div class="review-header">
            <div class="user-info">
              <img v-if="review.userAvatar" :src="review.userAvatar" class="user-avatar" :alt="review.userName"/>
              <div v-else class="user-avatar-placeholder">
                <i class="el-icon-user"></i>
              </div>
              <div class="user-details">
                <span class="review-user">{{ review.userName }}</span>
                <div class="review-meta">
                  <span class="review-rating">
                    <i v-for="n in review.ratingStar" :key="n" class="el-icon-star-on star-filled"></i>
                    <i v-for="n in (5 - review.ratingStar)" :key="'empty-' + n" class="el-icon-star-off star-empty"></i>
                  </span>
                  <span class="review-date">{{ formatDate(review.commentTime) }}</span>
                </div>
              </div>
            </div>
            <div class="review-stats">
              <span class="stat-item useful">
                <i class="el-icon-thumb-up"></i>
                {{ review.votesUp || 0 }}
              </span>
              <span class="stat-item useless">
                <i class="el-icon-thumb-down"></i>
                {{ review.votesDown || 0 }}
              </span>
              <span class="stat-item replies">
                <i class="el-icon-chat-line-round"></i>
                {{ review.repliesCount || 0 }}
              </span>
            </div>
          </div>
          <div class="review-title" v-if="review.reviewTitle">{{ review.reviewTitle }}</div>
          <div class="review-content">{{ review.content }}</div>
        </div>
      </div>

      <!-- 短评 -->
      <div class="reviews-section" v-if="shortReviews.length > 0">
        <h3 class="section-title">短评 ({{ shortReviews.length }})</h3>
        <div class="review-item short-review" v-for="review in shortReviews" :key="review.id">
          <div class="review-header">
            <span class="review-user">{{ review.userName }}</span>
            <div class="review-meta">
              <span class="review-rating">
                <i v-for="n in review.ratingStar" :key="n" class="el-icon-star-on star-filled"></i>
                <i v-for="n in (5 - review.ratingStar)" :key="'empty-' + n" class="el-icon-star-off star-empty"></i>
              </span>
              <span class="review-date">{{ formatDate(review.commentTime) }}</span>
            </div>
          </div>
          <div class="review-content">{{ review.content }}</div>
          <div class="review-footer">
            <span class="stat-item useful">
              <i class="el-icon-thumb-up"></i>
              {{ review.votesUp || 0 }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-else-if="!movie.movieId" class="loading">加载中...</div>
    <div v-else class="no-reviews">暂无影评</div>
  </div>
</template>
<script>
import {getMovieDetail} from "@/api/movie/movie";
import {addLike, cancelLike} from "@/api/movie/like";

export default {
  name: "MovieDetail",
  data() {
    return {
      movie: {},
      movieReview: [],
      isLiked: false
    }
  },
  computed: {
    // 长评
    longReviews() {
      return this.movieReview.filter(review => review.type?.includes('长评'));
    },
    // 短评
    shortReviews() {
      return this.movieReview.filter(review => review.type?.includes('长评'));
    }
  },
  created() {
    this.getMovieDetail(this.$route.params.movieId);
  },
  methods: {
    getMovieDetail(movieId) {
      console.log('开始获取电影详情，movieId:', movieId)
      getMovieDetail(movieId).then(response => {

        const detailData = response.data;
        if (detailData) {
          this.movie = detailData.movie || {};
          this.movieReview = detailData.movieReview || [];
          this.isLiked = detailData.isLiked || false;
        } else {
          console.error('API返回数据格式错误，没有data字段')
          this.$message.error('数据格式错误')
        }
      }).catch(error => {
        console.error('获取电影详情失败:', error)
        if (error.response) {
          console.error('响应状态:', error.response.status)
          console.error('响应数据:', error.response.data)
        }
        this.$message.error('获取电影详情失败：' + (error.response?.data?.msg || error.message))
      })
    },

    // 点赞功能
    handleLike() {
      this.isLiked = !this.isLiked;
      this.$message.success(this.isLiked ? '已点赞' : '已取消点赞');
      if (this.isLiked) {
        addLike({movieId: this.movie.movieId})
      } else {
        cancelLike({movieId: this.movie.movieId})
      }
    },

    // 格式化日期
    formatDate(dateStr) {
      if (!dateStr) return '';
      const date = new Date(dateStr);
      return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      });
    },

    // 获取代理图片URL
    getProxyImageUrl(url) {
      if (!url) return '';
      return process.env.VUE_APP_BASE_API + "/common/proxy-image?url=" + encodeURIComponent(url);
    },

    // 打开详情页
    openDetailUrl() {
      if (this.movie.detailUrl) {
        window.open('https://movie.douban.com/subject/' + this.movie.movieId, '_blank');
      } else {
        this.$message.warning('暂无详情页链接');
      }
    },
  }
}
</script>
<style scoped lang="scss">
.movie-detail {
  padding: 20px;
  max-width: 1000px;
  margin: 0 auto;
  background: #fff;
  min-height: 100vh;
}

// 电影信息样式
.movie-info {
  margin-bottom: 40px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);

  // 电影封面区域
  .movie-cover-section {
    position: relative;
    width: 100%;
    height: 280px;
    overflow: hidden;

    .movie-cover-wrapper {
      position: relative;
      width: 100%;
      height: 100%;
      cursor: pointer;
      transition: transform 0.3s ease;

      &:hover {
        transform: scale(1.02);

        .cover-overlay {
          opacity: 1;
        }
      }

      .movie-cover-img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        display: block;
      }

      .cover-overlay {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.6);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        opacity: 0;
        transition: opacity 0.3s ease;
        color: #fff;

        i {
          font-size: 32px;
          margin-bottom: 8px;
        }

        span {
          font-size: 16px;
          font-weight: bold;
        }
      }
    }
  }

  .movie-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    padding: 30px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

    .movie-title {
      color: #fff;
      font-size: 28px;
      font-weight: bold;
      margin: 0;
      flex: 1;
    }

    .movie-actions {
      .like-btn {
        background: rgba(255, 255, 255, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.3);
        color: #fff;
        padding: 8px 16px;
        border-radius: 20px;
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: 6px;

        &:hover {
          background: rgba(255, 255, 255, 0.3);
          transform: translateY(-2px);
        }

        &.liked {
          background: #ff6b35;
          border-color: #ff6b35;
          color: #fff;

          &:hover {
            background: #e55a2b;
            border-color: #e55a2b;
            transform: translateY(-2px);
          }

          i {
            color: #fff;
          }
        }

        i {
          font-size: 16px;
          transition: all 0.3s ease;
        }
      }
    }
  }

  .movie-stats {
    padding: 20px 30px;
    background: #f8f9fa;
    display: flex;
    gap: 20px;
    flex-wrap: wrap;
    align-items: center;

    .rating {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 14px;
      color: #666;
      padding: 8px 12px;
      background: #fff;
      border-radius: 6px;
      border: 1px solid #e9ecef;

      .rating-stars {
        display: flex;
        gap: 2px;

        .star-filled {
          color: #ff6b35;
          font-size: 16px;
        }

        .star-empty {
          color: #ddd;
          font-size: 16px;
        }
      }

      .rating-score {
        color: #ff6b35;
        font-weight: bold;
        margin-left: 4px;
      }
    }

    span:not(.rating) {
      font-size: 14px;
      color: #666;
      padding: 4px 8px;
      background: #fff;
      border-radius: 4px;
      border: 1px solid #e9ecef;
    }
  }

  .movie-meta {
    padding: 20px 30px;

    .meta-row {
      display: flex;
      gap: 40px;
      margin-bottom: 12px;

      &:last-child {
        margin-bottom: 0;
      }

      .meta-item {
        flex: 1;
        display: flex;
        align-items: flex-start;

        label {
          font-weight: bold;
          color: #333;
          min-width: 80px;
          margin-right: 12px;
          flex-shrink: 0;
        }

        span {
          color: #666;
          line-height: 1.4;
          word-break: break-word;
        }
      }
    }
  }

  .movie-description {
    padding: 20px 30px;
    border-top: 1px solid #e9ecef;

    h3 {
      color: #333;
      margin-bottom: 15px;
      font-size: 18px;
      font-weight: bold;
    }

    p {
      line-height: 1.8;
      color: #555;
      text-align: justify;
      margin: 0;
    }
  }

}

// 评论样式
.movie-reviews {
  .reviews-title {
    color: #333;
    font-size: 24px;
    margin-bottom: 30px;
    padding-bottom: 10px;
    border-bottom: 2px solid #e9ecef;
  }

  .reviews-section {
    margin-bottom: 40px;

    .section-title {
      color: #666;
      font-size: 18px;
      margin-bottom: 20px;
      padding: 10px 0;
      border-bottom: 1px solid #e9ecef;
    }
  }

  .review-item {
    border: 1px solid #e9ecef;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 20px;
    background: #fff;
    transition: box-shadow 0.3s ease;

    &:hover {
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    }
  }

  // 长评样式
  .long-review {
    .review-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 15px;

      .user-info {
        display: flex;
        align-items: center;
        gap: 12px;

        .user-avatar {
          width: 50px;
          height: 50px;
          border-radius: 50%;
          object-fit: cover;
          border: 2px solid #e9ecef;
        }

        .user-avatar-placeholder {
          width: 50px;
          height: 50px;
          border-radius: 50%;
          background: #f8f9fa;
          display: flex;
          align-items: center;
          justify-content: center;
          border: 2px solid #e9ecef;

          i {
            font-size: 20px;
            color: #adb5bd;
          }
        }

        .user-details {
          .review-user {
            font-weight: bold;
            color: #333;
            font-size: 16px;
            display: block;
            margin-bottom: 4px;
          }

          .review-meta {
            display: flex;
            align-items: center;
            gap: 12px;

            .review-rating {
              display: flex;
              align-items: center;
              gap: 2px;

              .star-filled {
                color: #ff6b35;
                font-size: 14px;
              }

              .star-empty {
                color: #ddd;
                font-size: 14px;
              }
            }

            .review-date {
              color: #999;
              font-size: 12px;
            }
          }
        }
      }

      .review-stats {
        display: flex;
        gap: 16px;

        .stat-item {
          display: flex;
          align-items: center;
          gap: 4px;
          color: #666;
          font-size: 14px;

          i {
            font-size: 16px;
          }

          &.useful::before {
            content: "有用";
            margin-right: 4px;
            font-size: 12px;
            color: #52c41a;
          }

          &.useless::before {
            content: "没用";
            margin-right: 4px;
            font-size: 12px;
            color: #ff4d4f;
          }

          &.replies::before {
            content: "回应";
            margin-right: 4px;
            font-size: 12px;
            color: #1890ff;
          }
        }
      }
    }

    .review-title {
      font-size: 16px;
      font-weight: bold;
      color: #333;
      margin-bottom: 10px;
      padding: 8px 0;
      border-bottom: 1px solid #f8f9fa;
    }

    .review-content {
      color: #555;
      line-height: 1.7;
      font-size: 15px;
    }
  }

  // 短评样式
  .short-review {
    .review-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;

      .review-user {
        font-weight: bold;
        color: #333;
      }

      .review-meta {
        display: flex;
        align-items: center;
        gap: 12px;

        .review-rating {
          display: flex;
          align-items: center;
          gap: 2px;

          .star-filled {
            color: #ff6b35;
            font-size: 14px;
          }

          .star-empty {
            color: #ddd;
            font-size: 14px;
          }
        }

        .review-date {
          color: #999;
          font-size: 12px;
        }
      }
    }

    .review-content {
      color: #555;
      line-height: 1.5;
      font-size: 14px;
      margin-bottom: 12px;
    }

    .review-footer {
      display: flex;
      justify-content: flex-end;

      .stat-item {
        display: flex;
        align-items: center;
        gap: 4px;
        color: #666;
        font-size: 12px;

        i {
          font-size: 14px;
        }

        &.useful::before {
          content: "有用";
          margin-right: 4px;
          font-size: 12px;
          color: #52c41a;
        }
      }
    }
  }
}

// 加载和空状态
.loading, .no-reviews {
  text-align: center;
  padding: 60px 20px;
  color: #666;
  font-size: 16px;
}

.no-reviews {
  color: #999;
}

// 响应式设计
@media (max-width: 768px) {
  .movie-detail {
    padding: 10px;
  }

  .movie-info {
    .movie-cover-section {
      height: 200px;
    }

    .movie-header {
      padding: 20px;
      flex-direction: column;
      gap: 15px;

      .movie-title {
        font-size: 24px;
      }
    }

    .movie-stats {
      padding: 15px 20px;
      flex-direction: column;
      gap: 10px;

      span {
        text-align: center;
      }
    }

    .movie-meta {
      padding: 15px 20px;

      .meta-row {
        flex-direction: column;
        gap: 8px;

        .meta-item {
          label {
            min-width: 70px;
          }
        }
      }
    }
  }

  .review-item {
    padding: 15px;
  }

  .long-review .review-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;

    .review-stats {
      align-self: flex-end;
    }
  }
}
</style>
