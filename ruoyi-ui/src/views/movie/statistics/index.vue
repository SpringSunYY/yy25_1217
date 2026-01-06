<template>
  <div class="dashboard-editor-container">

    <panel-group @handleSetLineChartData="handleSetLineChartData"/>

    <el-row class="chart-wrapper">
      <BarRankingCharts @item-click="handleChartClick"/>
    </el-row>
    <el-row class="chart-wrapper">
      <BarRankingCharts direction="left" :interval-time="0" @item-click="handleChartClick"/>
    </el-row>
  </div>
</template>

<script>
import PanelGroup from '../../dashboard/PanelGroup'
import LineChart from '../../dashboard/LineChart'
import RaddarChart from '../../dashboard/RaddarChart'
import PieChart from '../../dashboard/PieChart'
import BarChart from '../../dashboard/BarChart'
import BarRankingCharts from "@/components/echarts/BarRankingCharts.vue";

const lineChartData = {
  newVisitis: {
    expectedData: [100, 120, 161, 134, 105, 160, 165],
    actualData: [120, 82, 91, 154, 162, 140, 145]
  },
  messages: {
    expectedData: [200, 192, 120, 144, 160, 130, 140],
    actualData: [180, 160, 151, 106, 145, 150, 130]
  },
  purchases: {
    expectedData: [80, 100, 121, 104, 105, 90, 100],
    actualData: [120, 90, 100, 138, 142, 130, 130]
  },
  shoppings: {
    expectedData: [130, 140, 141, 142, 145, 150, 160],
    actualData: [120, 82, 91, 154, 162, 140, 130]
  }
}

export default {
  name: 'Index',
  components: {
    BarRankingCharts,
    PanelGroup,
    LineChart,
    RaddarChart,
    PieChart,
    BarChart
  },
  data() {
    return {
      lineChartData: lineChartData.newVisitis
    }
  },
  methods: {
    handleSetLineChartData(type) {
      this.lineChartData = lineChartData[type]
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
