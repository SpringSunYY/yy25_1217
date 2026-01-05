<template>
  <div class="app-container">
    <div class="chart-warper">
      <PieGradientTooltipCharts
        :chart-data="genresStatisticsData"
        :chart-title="genresStatisticsName"/>
    </div>
    <div class="chart-warper" style="width: 40%">
      <PeopleWordCharts
        :chart-data="actorsStatisticsData"
        :chart-title="actorsStatisticsName"
      />
    </div>
  </div>
</template>

<script>

import {getRecommend} from "@/api/movie/recommend";
import PieGradientTooltipCharts from "@/components/echarts/PieGradientTooltipCharts.vue";
import PeopleWordCharts from "@/components/echarts/PeopleWordCharts.vue";

export default {
  name: "RecommendModel",
  components: {PeopleWordCharts, PieGradientTooltipCharts},
  data() {
    return {
      recommend: {},
      recommendId: null,
      genresStatisticsData: [],
      genresStatisticsName: '剧情模型',

      actorsStatisticsData: [],
      actorsStatisticsName: '演员模型'
    };
  },
  created() {
    this.recommendId = this.$route.query && this.$route.query.recommendId;
    this.getRecommend();
  },
  watch: {
    // 监听路由
    $route(to, from) {
      this.recommendId = to.query.recommendId;
      if (this.recommendId) {
        this.getRecommend();
      }
    }
  },
  methods: {
    getRecommend() {
      getRecommend(this.recommendId).then((response) => {
        this.recommend = response.data;
        let modelInfo = {}
        if (this.recommend.modelInfo) {
          modelInfo = JSON.parse(this.recommend.modelInfo)
        } else {
          return
        }
        let userPreference = modelInfo.userPreference
        // console.log(userPreference)
        if (userPreference.genres) {
          this.genresStatisticsData = userPreference.genres.map(item => {
            return {
              name: item.name,
              value: item.value
            }
          });
        }
        if (userPreference.actors) {
          this.actorsStatisticsData = userPreference.actors.map(item => {
            return {
              name: item.name,
              value: item.value
            }
          });
        }
      });
    },
  }
};
</script>
<style scoped>
.chart-warper {
  height: 500px;
}
</style>
