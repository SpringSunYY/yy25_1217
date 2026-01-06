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
      <TableRanking
        :data="movieTableData"
        :columns="movieTableColumns"
        @rowClicked="handleChartClick"/>
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
import {getActorRankStatistics, getDirectorRankStatistics, getMovieRankStatistics} from "@/api/movie/statistics";

export default {
  name: 'Index',
  components: {
    PieBarRankingCharts,
    TableRanking,
    BarRankingCharts
  },
  data() {
    return {
      queryParams: {
        count_number: 300
      },
      dataRange: [],

      actorRankStatisticsData: [],
      actorRankStatisticsName: "演员播放排行",

      //导演排行
      directorRankStatisticsData: [],
      directorRankStatisticsName: "导演评分排行",

      movieTableData: [],
      movieTableColumns: [
        {
          label: '电影名称',
          prop: 'title'
        },
        {
          label: '导演',
          prop: 'directors'
        },
        {
          label: '播放量',
          prop: 'viewCount'
        },
        {
          label: '上映时间',
          prop: 'publishDate'
        },
        {
          label: '上映年份',
          prop: 'publishYear'
        }
      ],
    }
  },
  created() {
    this.getStatisticsData();
  },
  methods: {
    getStatisticsData() {
      if (this.dataRange.length && this.dataRange.length >= 1) {
        this.queryParams = {
          start_time: this.dataRange[0],
          end_time: this.dataRange[1]
        }
      }
      this.getActorRankStatistics();
      this.getDirectorRankStatistics();
      this.getMovieTableData();
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
    getMovieTableData() {
      getMovieRankStatistics(this.queryParams).then(res => {
        this.movieTableData = res.data;
      })
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
