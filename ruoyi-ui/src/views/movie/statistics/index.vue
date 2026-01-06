<template>
  <div class="dashboard-editor-container">
    <el-row class="chart-wrapper">
      <BarRankingCharts
        :chart-data="actorRankStatisticsData"
        :chart-title="actorRankStatisticsName"
        @item-click="handleChartClick"/>
    </el-row>
    <el-row class="chart-wrapper">
      <BarRankingCharts direction="left"
                        :chart-data="directorRankStatisticsData"
                        :chart-title="directorRankStatisticsName"
                        @item-click="handleChartClick"/>
    </el-row>
    <el-row class="chart-wrapper">
      <TableRanking @rowClicked="handleChartClick"/>
    </el-row>
    <el-row class="chart-wrapper">
      <PieBarRankingCharts @bar-click="handleChartClick"
                           @pie-click="handleChartClick"/>
    </el-row>
  </div>
</template>

<script>


import BarRankingCharts from "@/components/echarts/BarRankingCharts.vue";
import TableRanking from "@/components/echarts/TableRanking.vue";
import PieBarRankingCharts from "@/components/echarts/PieBarRankingCharts.vue";
import {getActorRankStatistics, getDirectorRankStatistics} from "@/api/movie/statistics";

export default {
  name: 'Index',
  components: {
    PieBarRankingCharts,
    TableRanking,
    BarRankingCharts
  },
  data() {
    return {
      queryParams: {},
      dataRange: [],

      actorRankStatisticsData: [],
      actorRankStatisticsName: "演员播放排行",

      //导演排行
      directorRankStatisticsData: [],
      directorRankStatisticsName: "导演评分排行",

    }
  },
  created() {
    this.getStatisticsData();
  },
  methods: {
    getStatisticsData() {
      if (this.dataRange.length && this.dataRange.length >= 1) {
        this.queryParams = {
          startTime: this.dataRange[0],
          endTime: this.dataRange[1]
        }
      }
      this.getActorRankStatistics();
      this.getDirectorRankStatistics();
    },
    getActorRankStatistics() {
      getActorRankStatistics(this.queryParams).then(res => {
          this.actorRankStatisticsData = res.data;
        }
      )
    },
    getDirectorRankStatistics() {
      getDirectorRankStatistics(this.queryParams).then(res => {
          this.directorRankStatisticsData = res.data;
        }
      )
    },
    handleChartClick(item) {
      console.log(item)
    }
  }
}
</script>

<style lang="scss" scoped>
.dashboard-editor-container {
  padding: 32px;
  background-color: rgb(240, 242, 245);
  position: relative;

  .chart-wrapper {
    height: 35vh;
    background: rgba(0, 0, 0, 0.13);
    padding: 16px 16px 0;
    margin-bottom: 32px;
  }
}

@media (max-width: 1024px) {
  .chart-wrapper {
    padding: 8px;
  }
}
</style>
