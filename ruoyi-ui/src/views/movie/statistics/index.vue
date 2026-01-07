<template>
  <div class="app-container">
    <el-row>
      <el-col :span="24">
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <div style="flex: 1; display: flex; justify-content: center;">
            <p style="font-size: 48px;color: white;font-weight: bold;margin: 0;">电影数据排行分析</p>
          </div>
          <div style="display: flex; align-items: center; gap: 16px;">
            <el-date-picker
              v-model="dataRange"
              value-format="yyyy-MM-dd"
              type="daterange"
              range-separator="-"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
            ></el-date-picker>
            <el-button type="primary" icon="el-icon-search" size="mini" @click="handleQuery">搜索</el-button>
            <el-button icon="el-icon-refresh" size="mini" @click="resetQuery">重置</el-button>
          </div>
        </div>
      </el-col>
      <el-col :span="24">
        <div class="chart-wrapper">
          <PieBarRankingCharts
            :chart-data="genresRankStatisticsData"
            :chart-title="genresRankStatisticsName"
            @bar-click="handleChartClick"
            @pie-click="handlePieChartClick"/>
        </div>
      </el-col>
      <el-col :span="8">
        <div class="chart-wrapper">
          <p class="chart-title">导演评分排行</p>
          <p class="chart-content">导演评分排行是根据导演执导的电影评分的平均分进行排行的，点击相关的导演可以搜索导演相关电影</p>
        </div>
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
        <div class="chart-wrapper">
          <p class="chart-title">演员播放排行</p>
          <p class="chart-content">演员播放排行是根据演员参演的电影播放总次数进行排行的，点击相关的演员可以搜索演员相关电影</p>
        </div>
      </el-col>
      <el-col :span="8">
        <div class="chart-wrapper">
          <p class="chart-title">电影播放排行</p>
          <p class="chart-content">电影播放排行是根据电影的播放次数进行排行的，点击相关的电影可以查看电影详情</p>
        </div>
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
          startTime: this.dataRange[0],
          endTime: this.dataRange[1]
        }
      }
      this.getActorRankStatistics();
      this.getDirectorRankStatistics();
      this.getMovieTableData();
      this.getGenresRankStatistics();
    },
    //搜索电影
    handleQuery(){
      this.getStatisticsData();
    },
    resetQuery() {
      this.dataRange = [];
      this.queryParams = {
        countNumber: 300,
        genres: ""
      };
      this.getStatisticsData();
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
    },
    //点击分类
    handlePieChartClick(item) {
      this.queryParams.genres = item.name;
      this.getActorRankStatistics();
      this.getDirectorRankStatistics();
      this.getMovieTableData();
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
  padding: 16px;
  margin-bottom: 32px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.chart-title {
  color: white;
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 16px;
}

.chart-content {
  color: white;
  font-size: 24px;
  text-indent: 2em;
}

@media (max-width: 1024px) {
  .chart-wrapper {
    padding: 8px;
  }
}
</style>
