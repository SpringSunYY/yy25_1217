<template>
  <div :class="className" :style="{ height, width }" ref="chartRef"></div>
</template>

<script>
import * as echarts from 'echarts'

export default {
  name: 'PieGradientTooltipCharts',

  props: {
    className: {
      type: String,
      default: 'chart'
    },
    width: {
      type: String,
      default: '100%'
    },
    height: {
      type: String,
      default: '100%'
    },
    chartData: {
      type: Array,
      default: () => [
        {tooltipText: "关注老年人医疗与康复服务", name: "医养健康", value: 1},
        {tooltipText: "涵盖动漫、游戏、设计等领域", name: "文化创意", value: 2},
        {tooltipText: "包含 5G、人工智能、大数据", name: "新一代信息技术产业", value: 3},
        {tooltipText: "重点关注光伏与石墨烯材料", name: "新能源新材料", value: 12},
        {tooltipText: "", name: "现代海洋", value: 1},
        {tooltipText: "金融科技与普惠金融", name: "现代金融服务", value: 0},
        {tooltipText: "智慧农业与现代种业", name: "现代高效农业", value: 1},
        {tooltipText: "文旅融合精品项目", name: "精品旅游", value: 5},
        {tooltipText: "精细化工与绿色化工", name: "高端化工", value: 3},
        {tooltipText: "智能制造与数控机床", name: "高端装备产业", value: 10}
      ]
    },
    // 中心显示的标题文字
    chartTitle: {
      type: String,
      default: '签约项目分类'
    },
    backgroundColor: {
      type: String,
      default: 'transparent'
    },
    defaultColor: {
      type: Array,
      default: () => [
        '#2ca1ff', '#0adbfa', '#febe13', '#65e5dd',
        '#7b2cff', '#fd5151', '#f071ff', '#85f67a',
        '#0baefd', '#fdcd0b', '#0bfdab', '#ff5353',
        '#ff72cb', '#8488ff', '#A5DEE4', '#81C7D4', '#24936E',
        '#5B8FF9', '#5AD8A6', '#5D7092', '#F6BD16', '#E86A92',
        '#7262FD', '#269A29', '#8E36BE', '#41A7E2', '#7747A3',
        '#FF7F50', '#FFDAB9', '#ADFF2F', '#00CED1', '#9370DB',
        '#3CB371', '#FF69B4', '#FFB6C1', '#DA70D6', '#98FB98',
        '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7',
        '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9'
      ]
    }
  },

  data() {
    return {
      chart: null,
    }
  },

  watch: {
    chartData: {
      deep: true,
      handler(val) {
        this.setOptions(val)
      }
    }
  },

  mounted() {
    this.$nextTick(() => {
      this.initChart()
      window.addEventListener('resize', this.handleResize)
    })
  },

  beforeDestroy() {
    window.removeEventListener('resize', this.handleResize)
    if (this.chart) {
      this.chart.dispose()
      this.chart = null
    }
  },

  methods: {
    initChart() {
      if (!this.$refs.chartRef) return
      this.chart = echarts.init(this.$refs.chartRef)
      this.setOptions(this.chartData)
    },

    setOptions(list) {
      if (!this.chart || !list || list.length === 0) return

      // 1. 计算总数
      const totalValue = list.reduce((sum, item) => sum + item.value, 0).toFixed(2)

      // 2. 构建带间隙的 ECharts data 数组
      const formattedData = []
      for (let i = 0; i < list.length; i++) {
        const itemColor = this.defaultColor[i % this.defaultColor.length]

        // 注入原始数据项
        formattedData.push({
          value: list[i].value,
          name: list[i].name,
          originData: list[i], // 挂载原始数据供 tooltip 调用
          itemStyle: {
            normal: {
              borderWidth: 2,
              shadowBlur: 5,
              borderRadius: 5,
              borderColor: itemColor,
              shadowColor: itemColor
            }
          }
        }, {
          // 注入间隙
          value: totalValue * 0.01,
          name: '',
          itemStyle: {
            normal: {
              color: 'rgba(0, 0, 0, 0)',
              borderColor: 'rgba(0, 0, 0, 0)',
              borderWidth: 0
            }
          },
          tooltip: {show: false}
        })
      }

      const option = {
        backgroundColor: this.backgroundColor,
        color: this.defaultColor,
        title: {
          text: this.chartTitle,
          left: '35%', // 居中于饼图圆心
          top: 'center',
          textAlign: 'center',
          textStyle: {
            color: '#ffffff',
            fontWeight: 'bold',
            fontSize: 20, // 对应原 1.5rem
          }
        },
        tooltip: {
          show: true,
          trigger: 'item',
          backgroundColor: 'rgba(0, 0, 0, 0.7)',
          borderColor: '#00ccff',
          borderWidth: 1,
          textStyle: {color: '#fff'},
          formatter: (params) => {
            if (params.name === '') return ''

            const item = params.data.originData
            const percent = totalValue > 0 ? ((item.value / totalValue) * 100).toFixed(2) : 0

            let res = `<div style="font-weight:bold; border-bottom:1px solid #666; margin-bottom:5px; padding-bottom:5px;">
                        总计:${totalValue}
                       </div>`
            res += `${item.name}: ${item.value} (${percent}%)`

            if (item.tooltipText) {
              res += `<br/><span style="color:#aaa; font-size:12px;">${item.tooltipText}</span>`
            }
            return res
          }
        },
        legend: {
          orient: 'vertical',
          data: list.map(i => i.name),
          left: 'right',
          top: 'center',
          align: 'left',
          itemGap: 10,
          textStyle: {
            color: 'rgba(36, 173, 254, 1)',
            fontSize: 14,
          },
          itemHeight: 10,
          itemWidth: 10,
          icon: 'circle'
        },
        series: [{
          name: '项目分布',
          type: 'pie',
          clockWise: false,
          radius: ['50%', '65%'],
          center: ['35%', '50%'],
          emphasis: {
            scale: true
          },
          label: {show: false},
          labelLine: {show: false},
          data: formattedData
        }]
      }

      this.chart.setOption(option, true)
    },

    handleResize() {
      if (this.chart) {
        this.chart.resize()
      }
    }
  }
}
</script>

<style scoped>
.chart {
  width: 100%;
  height: 100%;
  overflow: hidden;
}
</style>
