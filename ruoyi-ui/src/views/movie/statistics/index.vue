<template>
  <div class="dashboard-editor-container">
    <el-row class="chart-wrapper">
      <BarRankingCharts @item-click="handleChartClick"/>
    </el-row>
    <el-row class="chart-wrapper">
      <BarRankingCharts direction="left" :interval-time="0" @item-click="handleChartClick"/>
    </el-row>
    <el-row class="chart-wrapper">
      <TableRanking  @rowClicked="handleChartClick"/>
    </el-row>
  </div>
</template>

<script>


import BarRankingCharts from "@/components/echarts/BarRankingCharts.vue";
import TableRanking from "@/components/echarts/TableRanking.vue";

export default {
  name: 'Index',
  components: {
    TableRanking,
    BarRankingCharts
  },
  data() {
    return {
    }
  },
  methods: {
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
