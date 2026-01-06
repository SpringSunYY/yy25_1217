<template>
  <div :class="className" :style="{ height, width }" ref="chartRef"></div>
</template>

<script>
import * as echarts from 'echarts';

export default {
  name: 'PieBarRankingCharts',
  props: {
    className: {type: String, default: 'chart'},
    width: {type: String, default: '100%'},
    height: {type: String, default: '100%'},
    chartData: {
      type: Array,
      default: () => [
        {
          name: "医养健康",
          value: 12,
          tooltipText: "关注老年人医疗与康复服务",
          values: [
            {"name": "沈河区", "value": 3143, "tooltipText": "沈阳市的政治中心"},
            {"name": "皇姑区", "value": 2889, "tooltipText": "教育资源丰富"},
            {"name": "新民市", "value": 2844, "tooltipText": "农产品基地"},
            {"name": "于洪区", "value": 2736, "tooltipText": "物流集散地"},
            {"name": "铁西区", "value": 4000, "tooltipText": "测试排序：原本在后现在应排第一"},
            {"name": "大东区", "value": 2229, "tooltipText": "汽车产业"},
            {"name": "沈北新区", "value": 2168, "tooltipText": "大学城"},
            {"name": "沈河区", "value": 3143, "tooltipText": "沈阳市的政治中心"},
            {"name": "皇姑区", "value": 2889, "tooltipText": "教育资源丰富"},
            {"name": "新民市", "value": 2844, "tooltipText": "农产品基地"},
            {"name": "于洪区", "value": 2736, "tooltipText": "物流集散地"},
            {"name": "铁西区", "value": 4000, "tooltipText": "测试排序：原本在后现在应排第一"},
            {"name": "大东区", "value": 2229, "tooltipText": "汽车产业"},
            {"name": "沈北新区", "value": 2168, "tooltipText": "大学城"}
          ]
        },
        {
          name: "文化创意",
          value: 8,
          tooltipText: "涵盖动漫、游戏、设计等领域",
          values: [
            {"name": "和平区", "value": 1500, "tooltipText": "文创园区集中"},
            {"name": "沈河区", "value": 1200, "tooltipText": "文化底蕴深厚"},
            {"name": "大东区", "value": 1900, "tooltipText": "排序测试：应排第一"}
          ]
        },
        {
          name: "新一代信息技术",
          value: 15,
          tooltipText: "包含 5G、人工智能、大数据",
          values: [
            {"name": "浑南区", "value": 4500, "tooltipText": "高新企业聚集"},
            {"name": "沈北新区", "value": 3200, "tooltipText": "数字产业园"}
          ]
        }
      ]
    },
    showCount: {type: Number, default: 8},
    intervalTime: {type: Number, default: 2500},
    backgroundColor: {type: String, default: '#041139'}
  },

  data() {
    return {
      chart: null,
      timer: null,
      startIndex: 0, // 柱状图轮播起始索引
      isInteracting: false,
      activeIndustry: '', // 当前选中的饼图分类名
      currentBarData: [], // 当前显示的已排序柱状图数据
      colors: ['#2ca1ff', '#0adbfa', '#febe13', '#65e5dd', '#7b2cff', '#fd5151', '#f071ff', '#85f67a']
    };
  },

  watch: {
    chartData: {
      deep: true,
      handler(newVal) {
        if (newVal && newVal.length > 0) {
          this.initActiveData();
          this.renderChart();
          this.resetRotation();
        }
      }
    }
  },

  mounted() {
    if (this.chartData && this.chartData.length > 0) {
      this.initActiveData();
    }
    this.initChart();
    window.addEventListener('resize', this.handleResize);
  },

  beforeDestroy() {
    this.stopRotation();
    if (this.chart) {
      this.chart.dispose();
      this.chart = null;
    }
    window.removeEventListener('resize', this.handleResize);
  },

  methods: {
    // 初始化选中的数据（默认第一条）
    initActiveData() {
      if (!this.activeIndustry && this.chartData.length > 0) {
        const first = this.chartData[0];
        this.activeIndustry = first.name;
        this.currentBarData = [...first.values].sort((a, b) => b.value - a.value);
      }
    },

    initChart() {
      if (!this.$refs.chartRef) return;
      this.chart = echarts.init(this.$refs.chartRef);
      this.renderChart();
      this.resetRotation();
      this.initChartEvents();
    },

    // 处理饼图数据（增加透明间隙）
    getPieSeriesData() {
      const pieData = [];
      let total = 0;
      this.chartData.forEach(item => {
        //如果没有value
        if (!item.value) {
          // 如果没有value，则将value设置为values的和
          item.value = item.values.reduce((sum, bar) => sum + bar.value, 0);
        }
        total += item.value;
      });

      this.chartData.forEach((item, i) => {
        pieData.push({
          value: item.value,
          name: item.name,
          originData: item,
          itemStyle: {
            borderWidth: 2,
            borderRadius: 5,
            borderColor: this.colors[i % this.colors.length],
            shadowBlur: 5,
            shadowColor: this.colors[i % this.colors.length]
          },
          // 选中后的高亮边框样式
          select: {
            itemStyle: {borderWidth: 4, borderColor: '#fff', shadowBlur: 10}
          }
        }, {
          // 间隙块
          value: total * 0.02,
          name: '',
          itemStyle: {color: 'transparent'},
          tooltip: {show: false}
        });
      });
      return pieData;
    },

    renderChart() {
      if (!this.chart) return;
      const totalValue = this.chartData.reduce((sum, item) => sum + item.value, 0).toFixed(2)

      const option = {
        backgroundColor: this.backgroundColor,
        title: [
          {
            text: '签约项目分类',
            left: '21%',
            top: '40%',
            textStyle: {color: '#fff', fontSize: 18, fontWeight: 'bold'}
          },
          {
            text: `【${this.activeIndustry}】排行`,
            left: '65%',
            top: 20,
            textStyle: {color: '#fff', fontSize: 20, fontWeight: 'bold'}
          }
        ],
        tooltip: {
          trigger: 'item',
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          formatter: (params) => {
            if (params.seriesName === '行业分布') {
              if (!params.name) return '';
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
            } else {
              const item = this.currentBarData[params.dataIndex];
              let html = `<div style="padding:10px; color:#fff;">
                          <b style="font-size:16px; color:#56fb93">NO.${params.dataIndex + 1} - ${item.name}</b><br/>
                          <span style="opacity:0.8">数值：</span>${item.value}<br/>`;
              if (item.tooltipText) {
                html += `<span style="opacity:0.8">描述：</span><span style="color:#347CDD">${item.tooltipText}</span>`;
              }
              html += `</div>`;
              return html;
            }
          }
        },
        legend: {
          type: 'scroll',
          orient: 'horizontal',
          bottom: '5%',
          left: '5%',
          width: '40%',
          data: this.chartData.map(i => i.name),
          textStyle: {color: '#24adfe'},
          pageTextStyle: {color: '#fff'}
        },
        grid: {left: '50%', right: '5%', top: '15%', bottom: '10%', containLabel: true},
        xAxis: {type: 'value', show: false},
        yAxis: {
          type: 'category',
          data: this.currentBarData.map(i => i.name),
          inverse: true,
          axisLine: {show: false},
          axisTick: {show: false},
          axisLabel: {
            color: "#fff",
            fontSize: 14,
            formatter: (value, index) => {
              if (index === 0) return '{a|' + value + '}';
              if (index === 1) return '{b|' + value + '}';
              if (index === 2) return '{c|' + value + '}';
              return value;
            },
            rich: {
              a: {color: '#ffde00', fontSize: 16, fontWeight: 'bold'},
              b: {color: '#cfcfcf', fontSize: 15},
              c: {color: '#d39050', fontSize: 14}
            }
          }
        },
        dataZoom: [{
          type: 'inside',
          yAxisIndex: 0,
          startValue: this.startIndex,
          endValue: this.startIndex + this.showCount,
          zoomLock: false,
          zoomOnMouseWheel: false,
          moveOnMouseWheel: true
        }],
        series: [
          {
            name: '行业分布',
            type: 'pie',
            radius: ['65%', '80%'],
            center: ['25%', '45%'],
            selectedMode: 'single',
            data: this.getPieSeriesData(),
            label: {show: false},
            emphasis: {scale: true}
          },
          {
            name: '排行',
            type: 'bar',
            barWidth: 18,
            showBackground: true,
            backgroundStyle: {color: 'rgba(255, 255, 255, 0.05)', borderRadius: 10},
            itemStyle: {
              borderRadius: 10,
              color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                {offset: 0, color: '#347CDD'},
                {offset: 1, color: '#56fb93'}
              ])
            },
            label: {show: true, position: 'right', color: '#fff'},
            data: this.currentBarData.map(i => i.value)
          }
        ]
      };

      this.chart.setOption(option, true);

      // 默认高亮当前选中的饼图块
      const activeIdx = this.chartData.findIndex(i => i.name === this.activeIndustry);
      if (activeIdx !== -1) {
        this.chart.dispatchAction({
          type: 'pieSelect',
          dataIndex: activeIdx * 2 // 因为有间隙块，索引需要 * 2
        });
      }
    },

    initChartEvents() {
      // 1. 鼠标交互暂停轮播
      this.chart.on('mousemove', () => {
        this.isInteracting = true;
      });
      this.chart.on('globalout', () => {
        this.isInteracting = false;
      });

      // 2. 滚动同步逻辑
      this.chart.on('dataZoom', (params) => {
        let start = params.batch ? params.batch[0].startValue : params.startValue;
        if (start !== undefined) this.startIndex = Math.ceil(start);
      });

      // 3. 点击事件联动
      this.chart.on('click', (params) => {
        if (params.seriesName === '行业分布' && params.name !== '') {
          // --- 饼图点击逻辑 ---
          const selected = this.chartData.find(item => item.name === params.name);
          if (selected) {
            this.activeIndustry = selected.name;
            this.currentBarData = [...selected.values].sort((a, b) => b.value - a.value);
            this.startIndex = 0;
            this.renderChart(); // 重新渲染以更新标题、轴和排序
            this.$emit('pie-click', selected);
          }
        } else if (params.seriesName === '区县排行') {
          // --- 柱状图点击逻辑 ---
          const itemData = this.currentBarData[params.dataIndex];
          this.$emit('bar-click', itemData); // 向父组件回传该区县的原始数据对象
        }
      });
    },

    resetRotation() {
      this.stopRotation();
      if (this.intervalTime > 0) this.startRotation();
    },

    startRotation() {
      this.timer = setInterval(() => {
        if (!this.isInteracting && this.currentBarData.length > this.showCount) {
          const totalLength = this.currentBarData.length;
          if (this.startIndex >= totalLength - this.showCount - 1) {
            this.startIndex = 0;
          } else {
            this.startIndex++;
          }
          this.chart.dispatchAction({
            type: 'dataZoom',
            startValue: this.startIndex,
            endValue: this.startIndex + this.showCount
          });
        }
      }, this.intervalTime);
    },

    stopRotation() {
      if (this.timer) {
        clearInterval(this.timer);
        this.timer = null;
      }
    },

    handleResize() {
      this.chart?.resize();
    }
  }
};
</script>
