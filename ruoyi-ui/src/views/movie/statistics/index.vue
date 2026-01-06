<template>
  <div class="app-container">
    <el-row>
      <el-col :span="24">
        <div class="chart-wrapper">
          <PieBarRankingCharts
            :chart-data="genresRankStatisticsData"
            :chart-title="genresRankStatisticsName"
            @bar-click="handleChartClick"
            @pie-click="handleChartClick"/>
        </div>
      </el-col>
      <el-col :span="8">
        <div class="chart-wrapper"></div>
      </el-col>
      <el-col :span="16">
        <div class="chart-wrapper">
          <BarRankingCharts direction="left"
                            :chart-data="directorRankStatisticsData"
                            :chart-title="directorRankStatisticsName"
                            @item-click="handleChartClick"/>
        </div>
      </el-col>
      <el-col :span="16">
        <div class="chart-wrapper">
          <BarRankingCharts
            :chart-data="actorRankStatisticsData"
            :chart-title="actorRankStatisticsName"
            @item-click="handleChartClick"/>
        </div>
      </el-col>
      <el-col :span="8">
        <div class="chart-wrapper"></div>
      </el-col>
      <el-col :span="8">
        <div class="chart-wrapper"></div>
      </el-col>
      <el-col :span="16">
        <div class="chart-wrapper">
          <TableRanking
            :data="movieTableData"
            :columns="movieTableColumns"
            @rowClicked="handleChartClick"/>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>


import BarRankingCharts from "@/components/echarts/BarRankingCharts.vue";
import TableRanking from "@/components/echarts/TableRanking.vue";
import PieBarRankingCharts from "@/components/echarts/PieBarRankingCharts.vue";
import {
  getActorRankStatistics,
  getDirectorRankStatistics,
  getGenresRankStatistics,
  getMovieRankStatistics
} from "@/api/movie/statistics";

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
        countNumber: 300
      },
      dataRange: [],

      actorRankStatisticsData: [],
      actorRankStatisticsName: "演员播放排行",

      //导演排行
      directorRankStatisticsData: [],
      directorRankStatisticsName: "导演评分排行",

      //分类
      genresRankStatisticsData: [],
      genresRankStatisticsName: "电影分类排行",

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
      this.getGenresRankStatistics();
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
    getGenresRankStatistics() {
      getGenresRankStatistics(this.queryParams).then(res => {
        this.genresRankStatisticsData = res.data;
      })
    },
    handleChartClick(item) {
      console.log(item)
    }
  }
}
</script>

<style lang="scss" scoped>
.app-container {
  background-image: url("../../../assets/images/map.png");
  background-repeat: no-repeat;
  background-size: cover;
  background-attachment: fixed;
  background-position: center;
  min-height: 92vh;
  margin-top: -10px;
  padding: 32px;
}

.chart-wrapper {
  height: 40vh;
  padding: 16px 16px 0;
  margin-bottom: 32px;
}

@media (max-width: 1024px) {
  .chart-wrapper {
    padding: 8px;
  }
}
</style>
