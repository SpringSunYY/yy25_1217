<template>
  <div :class="className" :style="{ height, width }" ref="chartRef"/>
</template>

<script>
// 引入 ECharts 核心库
import * as echarts from 'echarts';
// 必须引入词云扩展插件
import 'echarts-wordcloud';
import {generateRandomColor} from "@/utils/ruoyi";

export default {
  name: 'PeopleWordCharts',
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
        {name: '花鸟市场', value: 1446, tooltipText: '这里是关于花鸟市场的详细描述文字'},
        {name: '汽车', value: 928, tooltipText: '汽车行业趋势分析'},
        {name: '视频', value: 906},
        {name: '电视', value: 825},
        {name: 'Lover Boy 88', value: 514},
        {name: '动漫', value: 486},
        {name: '音乐', value: 53},
        {name: '直播', value: 163},
        {name: '广播电台', value: 86},
        {name: '戏曲曲艺', value: 17},
        {name: '演出票务', value: 6},
        {name: '给陌生的你听', value: 1},
        {name: '资讯', value: 1437},
        {name: '商业财经', value: 422},
        {name: '娱乐八卦', value: 353},
        {name: '军事', value: 331},
        {name: '科技资讯', value: 313},
        {name: '社会时政', value: 307},
        {name: '时尚', value: 43},
        {name: '网络奇闻', value: 15},
        {name: '旅游出行', value: 438},
        {name: '景点类型', value: 957},
        {name: '国内游', value: 927},
        {name: '远途出行方式', value: 908},
        {name: '酒店', value: 693},
        {name: '关注景点', value: 611},
        {name: '旅游网站偏好', value: 512},
        {name: '出国游', value: 382},
        {name: '交通票务', value: 312},
        {name: '旅游方式', value: 187},
        {name: '旅游主题', value: 163},
        {name: '港澳台', value: 104},
        {name: '本地周边游', value: 3},
        {name: '小卖家', value: 1331},
        {name: '全日制学校', value: 941},
        {name: '基础教育科目', value: 585},
        {name: '考试培训', value: 473},
        {name: '语言学习', value: 358},
        {name: '留学', value: 246},
        {name: 'K12课程培训', value: 207},
        {name: '艺术培训', value: 194},
        {name: '技能培训', value: 104},
        {name: 'IT培训', value: 87},
        {name: '高等教育专业', value: 63},
        {name: '家教', value: 48},
        {name: '体育培训', value: 23},
        {name: '职场培训', value: 5},
        {name: '金融财经', value: 1328},
        {name: '银行', value: 765},
        {name: '股票', value: 452},
        {name: '保险', value: 415},
        {name: '贷款', value: 253},
        {name: '基金', value: 211},
        {name: '信用卡', value: 180},
        {name: '外汇', value: 138},
        {name: 'P2P', value: 116},
        {name: '贵金属', value: 98},
        {name: '债券', value: 93},
        {name: '网络理财', value: 92},
        {name: '信托', value: 90},
        {name: '征信', value: 76},
        {name: '期货', value: 76},
        {name: '公积金', value: 40},
        {name: '银行理财', value: 36},
        {name: '银行业务', value: 30},
        {name: '典当', value: 7},
        {name: '海外置业', value: 1},
        {name: '汽车', value: 1309},
        {name: '汽车档次', value: 965},
        {name: '汽车品牌', value: 900},
        {name: '汽车车型', value: 727},
        {name: '购车阶段', value: 461},
        {name: '二手车', value: 309},
        {name: '汽车美容', value: 260},
        {name: '新能源汽车', value: 173},
        {name: '汽车维修', value: 155},
        {name: '租车服务', value: 136},
        {name: '车展', value: 121},
        {name: '违章查询', value: 76},
        {name: '汽车改装', value: 62},
        {name: '汽车用品', value: 37},
        {name: '路况查询', value: 32},
        {name: '汽车保险', value: 28},
        {name: '陪驾代驾', value: 4},
        {name: '网络购物', value: 1275},
        {name: '做我的猫', value: 1088},
        {name: '只想要你知道', value: 907},
        {name: '团购', value: 837},
        {name: '比价', value: 201},
        {name: '海淘', value: 195},
        {name: '移动APP购物', value: 179},
        {name: '支付方式', value: 119},
        {name: '代购', value: 43},
        {name: '体育健身', value: 1234},
        {name: '体育赛事项目', value: 802},
        {name: '运动项目', value: 405},
        {name: '体育类赛事', value: 337},
        {name: '健身项目', value: 199},
        {name: '健身房健身', value: 78},
        {name: '运动健身', value: 77},
        {name: '家庭健身', value: 36},
        {name: '健身器械', value: 29},
        {name: '办公室健身', value: 3},
        {name: '商务服务', value: 1201},
        {name: '法律咨询', value: 508},
        {name: '化工材料', value: 147},
        {name: '广告服务', value: 125},
        {name: '会计审计', value: 115},
        {name: '人员招聘', value: 101},
        {name: '印刷打印', value: 66},
        {name: '知识产权', value: 32},
        {name: '翻译', value: 22},
        {name: '安全安保', value: 9},
        {name: '公关服务', value: 8},
        {name: '商旅服务', value: 2},
        {name: '展会服务', value: 2},
        {name: '特许经营', value: 1},
        {name: '休闲爱好', value: 1169},
        {name: '收藏', value: 412},
        {name: '摄影', value: 393},
        {name: '温泉', value: 230},
        {name: '博彩彩票', value: 211},
        {name: '美术', value: 207},
        {name: '书法', value: 139},
        {name: 'DIY手工', value: 75},
        {name: '舞蹈', value: 23},
        {name: '钓鱼', value: 21},
        {name: '棋牌桌游', value: 17},
        {name: 'KTV', value: 6},
        {name: '密室', value: 5},
        {name: '采摘', value: 4},
        {name: '电玩', value: 1},
        {name: '真人CS', value: 1},
        {name: '轰趴', value: 1},
        {name: '电玩', value: 1},
        {name: '真人CS', value: 1},
        {name: '轰趴', value: 1},
        {name: '家电数码', value: 1111},
        {name: '手机', value: 885},
        {name: '电脑', value: 543},
        {name: '大家电', value: 321},
        {name: '家电关注品牌', value: 253},
        {name: '网络设备', value: 162},
        {name: '摄影器材', value: 149},
        {name: '影音设备', value: 133},
        {name: '办公数码设备', value: 113},
        {name: '生活电器', value: 67},
        {name: '厨房电器', value: 54},
        {name: '智能设备', value: 45},
        {name: '个人护理电器', value: 22},
        {name: '服饰鞋包', value: 1047},
        {name: '服装', value: 566},
        {name: '饰品', value: 289},
        {name: '鞋', value: 184},
        {name: '箱包', value: 168},
        {name: '奢侈品', value: 137},
        {name: '母婴亲子', value: 1041},
        {name: '孕婴保健', value: 505},
        {name: '母婴社区', value: 299},
        {name: '早教', value: 103},
        {name: '奶粉辅食', value: 66},
        {name: '童车童床', value: 41},
        {name: '关注品牌', value: 271},
        {name: '宝宝玩乐', value: 30},
        {name: '母婴护理服务', value: 25},
        {name: '纸尿裤湿巾', value: 16},
        {name: '妈妈用品', value: 15},
        {name: '宝宝起名', value: 12},
        {name: '童装童鞋', value: 9},
        {name: '胎教', value: 8},
        {name: '宝宝安全', value: 1},
        {name: '宝宝洗护用品', value: 1},
        {name: '软件应用', value: 1018},
        {name: '系统工具', value: 896},
        {name: '理财购物', value: 440},
        {name: '生活实用', value: 365},
        {name: '影音图像', value: 256},
        {name: '社交通讯', value: 214},
        {name: '手机美化', value: 39},
        {name: '办公学习', value: 28},
        {name: '应用市场', value: 23},
        {name: '母婴育儿', value: 14},
        {name: '游戏', value: 946},
        {name: '手机游戏', value: 565},
        {name: 'PC游戏', value: 353},
        {name: '网页游戏', value: 254},
        {name: '游戏机', value: 188},
        {name: '模拟辅助', value: 166},
        {name: '个护美容', value: 942},
        {name: '护肤品', value: 177},
        {name: '彩妆', value: 133},
        {name: '美发', value: 80},
        {name: '香水', value: 50},
        {name: '个人护理', value: 46},
        {name: '美甲', value: 26},
        {name: 'SPA美体', value: 21},
        {name: '花鸟萌宠', value: 914},
        {name: '绿植花卉', value: 311},
        {name: '狗', value: 257},
        {name: '其他宠物', value: 131},
        {name: '水族', value: 125},
        {name: '猫', value: 122},
        {name: '动物', value: 81},
        {name: '鸟', value: 67},
        {name: '宠物用品', value: 41},
        {name: '宠物服务', value: 26},
        {name: '书籍阅读', value: 913},
        {name: '网络小说', value: 483},
        {name: '关注书籍', value: 128},
        {name: '文学', value: 105},
        {name: '报刊杂志', value: 77},
        {name: '人文社科', value: 22},
        {name: '建材家居', value: 907},
        {name: '装修建材', value: 644},
        {name: '家具', value: 273},
        {name: '家居风格', value: 187},
        {name: '家居家装关注品牌', value: 140},
        {name: '家纺', value: 107},
        {name: '厨具', value: 47},
        {name: '灯具', value: 43},
        {name: '家居饰品', value: 29},
        {name: '家居日常用品', value: 10},
        {name: '生活服务', value: 883},
        {name: '物流配送', value: 536},
        {name: '家政服务', value: 108},
        {name: '摄影服务', value: 49},
        {name: '搬家服务', value: 38},
        {name: '物业维修', value: 37},
        {name: '婚庆服务', value: 24},
        {name: '二手回收', value: 24},
        {name: '鲜花配送', value: 3},
        {name: '维修服务', value: 3},
        {name: '殡葬服务', value: 1},
        {name: '求职创业', value: 874},
        {name: '创业', value: 363},
        {name: '目标职位', value: 162},
        {name: '目标行业', value: 50},
        {name: '兼职', value: 21},
        {name: '期望年薪', value: 20},
        {name: '实习', value: 16},
        {name: '雇主类型', value: 10},
        {name: '星座运势', value: 789},
        {name: '星座', value: 316},
        {name: '算命', value: 303},
        {name: '解梦', value: 196},
        {name: '风水', value: 93},
        {name: '面相分析', value: 47},
        {name: '手相', value: 32},
        {name: '公益', value: 90}
      ]
    },
    // 遮罩图片：base64 或 图片路径
    maskImage: {
      type: String,
      default: 'data:image/png;base64,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',
    },
    // 字体大小范围
    sizeRange: {
      type: Array,
      default: () => [12, 32]
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
      imageObj: null
    };
  },
  computed: {
    // 计算总分母，用于计算百分比
    totalValue() {
      return this.chartData.reduce((prev, curr) => prev + (Number(curr.value) || 0), 0).toFixed(2);
    }
  },
  watch: {
    chartData: {
      handler() {
        this.initChart();
      },
      deep: true
    },
    maskImage: {
      handler() {
        this.prepareMaskAndInit();
      }
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.prepareMaskAndInit();
      window.addEventListener('resize', this.handleResize);
    });
  },
  beforeDestroy() {
    if (this.chart) {
      this.chart.dispose();
      this.chart = null;
    }
    window.removeEventListener('resize', this.handleResize);
  },
  methods: {
    /**
     * @description 处理遮罩图加载并初始化
     */
    prepareMaskAndInit() {
      if (this.maskImage) {
        this.imageObj = new Image();
        this.imageObj.src = this.maskImage;
        this.imageObj.onload = () => {
          this.initChart();
        };
      } else {
        this.initChart();
      }
    },

    /**
     * @description 初始化词云
     */
    initChart() {
      if (!this.$refs.chartRef) return;

      if (this.chart) {
        this.chart.dispose();
      }

      this.chart = echarts.init(this.$refs.chartRef);
      const total = this.totalValue;

      const option = {
        backgroundColor: 'transparent',
        tooltip: {
          show: true,
          confine: true, // 限制在图表范围内
          backgroundColor: 'rgba(0,0,0,0.7)',
          textStyle: {color: '#fff'},
          formatter: (params) => {
            const percent = total > 0 ? ((params.value / total) * 100).toFixed(2) + '%' : '0%';
            const extraText = params.data.tooltipText
              ? `<br/>${params.data.tooltipText}`
              : '';

            return `
              总计：${total}<br/>
              ${params.name}：${params.value} (${percent})
              ${extraText}
            `;
          }
        },
        series: [
          {
            type: 'wordCloud',
            // 词云形状：'circle', 'cardioid', 'diamond', 'triangle-forward', 'triangle', 'pentagon', 'star'
            // 如果设置了 maskImage，则此 shape 会被忽略
            shape: 'circle',
            maskImage: this.imageObj,
            left: 'center',
            top: 'center',
            width: '90%',
            height: '90%',
            right: null,
            bottom: null,
            sizeRange: this.sizeRange,
            rotationRange: [-45, 0, 45, 90],
            rotationStep: 45,
            gridSize: 8,
            drawOutOfBound: false, // 允许词云超出画布边缘
            layoutAnimation: true,
            textStyle: {
              fontFamily: 'sans-serif',
              fontWeight: 'bold',
              // 颜色随机生成
              // color: generateRandomColor(this.defaultColor)
              color: () => {
                return generateRandomColor(this.defaultColor);
              }
            },
            emphasis: {
              textStyle: {
                shadowBlur: 10,
                shadowColor: '#333'
              }
            },
            data: this.chartData
          }
        ]
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
  width: 100%;
  margin: 0 auto;
}
</style>
