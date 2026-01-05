<template>
  <div :class="className" :style="{ height, width }" ref="chartRef"/>
</template>

<script>
import * as echarts from 'echarts';
import {generateRandomColor} from "@/utils/ruoyi";

export default {
  name: 'ScatterRippleCharts',
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
    chartTitle: {
      type: String,
      default: '人员构成分布'
    },
    chartData: {
      type: Array,
      default: () => [
        {name: "电力热力", value: 130, tooltipText: "电力供应与热力生产"},
        {name: "管理员", value: 80, tooltipText: "系统后台管理"},
        {name: "医生", value: 110, tooltipText: "医疗诊断专家"},
        {name: "护工", value: 600, tooltipText: "专业生活护理"},
        {name: "护士", value: 95, tooltipText: "医疗护理服务"},
        {name: "技师", value: 70, tooltipText: "技术支持"},
        {name: "志愿者", value: 50, tooltipText: "社区服务"}
      ]
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
    },
    minBubbleSize: {
      type: Number,
      default: 70
    },
    maxBubbleSize: {
      type: Number,
      default: 130
    }
  }
  ,
  data() {
    return {
      chart: null,
      totalSum: 0
    };
  }
  ,
  watch: {
    chartData: {
      handler() {
        this.setOptions();
      },
      deep: true
    }
  }
  ,
  mounted() {
    this.$nextTick(() => {
      this.initChart();
      window.addEventListener('resize', this.handleResize);
    });
  }
  ,
  beforeDestroy() {
    if (this.chart) {
      this.chart.dispose();
      this.chart = null;
    }
    window.removeEventListener('resize', this.handleResize);
  }
  ,
  methods: {
    /**
     * 带碰撞检测的随机位置生成
     */
    generateBubbleData() {
      const datas = [];
      const maxVal = Math.max(...this.chartData.map(d => d.value));

      this.chartData.forEach((item, index) => {
        const currentSize = this.minBubbleSize + (item.value / maxVal) * (this.maxBubbleSize - this.minBubbleSize);

        let x, y, isOverlap;
        let attempts = 0;

        // 为每个气泡寻找一个不重叠的随机位置
        do {
          isOverlap = false;
          // 随机坐标 (20% - 80% 之间，留出边缘避免切边)
          x = Math.floor(Math.random() * 60) + 20;
          y = Math.floor(Math.random() * 60) + 20;
          attempts++;

          // 碰撞检测：遍历已生成的点，确保圆心距离 > 两圆半径之和
          for (let i = 0; i < datas.length; i++) {
            const prev = datas[i];
            const dx = x - prev.value[0];
            const dy = y - prev.value[1];
            const distance = Math.sqrt(dx * dx + dy * dy);

            // 映射到坐标系，给一个安全间距系数
            const minDistance = (currentSize + prev.symbolSize) / 10;
            if (distance < minDistance) {
              isOverlap = true;
              break;
            }
          }
        } while (isOverlap && attempts < 100);

        datas.push({
          name: item.name,
          value: [x, y],
          symbolSize: currentSize,
          tooltipText: item.tooltipText || item.name,
          rawValue: item.value,
          itemStyle: {
            normal: {
              color: generateRandomColor(this.defaultColor),
              opacity: 0.9,
              shadowBlur: 15,
              shadowColor: 'rgba(0,0,0,0.2)'
            }
          }
        });
      });

      return datas;
    }
    ,

    /**
     * 初始化图表
     */
    initChart() {
      if (!this.$refs.chartRef) return;

      if (this.chart) {
        this.chart.dispose();
      }
      this.chart = echarts.init(this.$refs.chartRef);
      this.setOptions();
    },
    setOptions() {
      // 计算总计
      this.totalSum = this.chartData.reduce((sum, item) => sum + (item.value || 0), 0);

      const processedData = this.generateBubbleData();

      const option = {
        backgroundColor: this.backgroundColor,
        title: {
          text: this.chartTitle,
          left: 'center',
          top: 20,
          textStyle: {color: '#fff', fontSize: 20}
        },
        dataZoom: [
          {
            type: 'inside',
            xAxisIndex: [0],
            yAxisIndex: [0],
            filterMode: 'none',
            zoomOnMouseWheel: true,
            moveOnMouseMove: true
          }
        ],
        tooltip: {
          show: true,
          backgroundColor: 'rgba(0,0,0,0.8)',
          borderColor: '#555',
          textStyle: {color: '#fff'},
          formatter: (params) => {
            const d = params.data;
            console.log(d)
            const percentage = ((d.rawValue / this.totalSum) * 100).toFixed(2);
            console.log(percentage)
            let res = `<div style="line-height:22px;">
                        <b style="color:#FFD700">总计: ${this.totalSum}</b><br/>
                        ${d.name}: ${d.rawValue} (${percentage}%)`;
            if (d.tooltipText) {
              res += `<br/><span style="color:#00FFFF">${d.tooltipText}</span>`;
            }
            res += `</div>`;
            return res;
          }
        },
        grid: {
          left: 0,
          right: 0,
          top: 0,
          bottom: 0
        },
        xAxis: {
          type: 'value',
          show: false,
          min: 0,
          max: 100
        },
        yAxis: {
          type: 'value',
          show: false,
          min: 0,
          max: 100
        },
        series: [{
          type: 'effectScatter',
          symbol: 'circle',
          symbolSize: 120,
          label: {
            normal: {
              show: true,
              formatter: '{b}',
              color: '#fff',
              textStyle: {
                fontSize: '20'
              }
            }
          },
          data: processedData
        }]
      };

      this.chart.setOption(option);
    },

    handleResize() {
      if (this.chart) {
        this.chart.resize();
      }
    }
  }
};
</script>

<style scoped>
.chart {
  min-height: 400px;
}
</style>
