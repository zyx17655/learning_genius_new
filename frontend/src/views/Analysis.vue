<template>
  <div class="analysis">
    <el-card>
      <h2>题目分析</h2>
      
      <el-tabs v-model="activeTab">
        <el-tab-pane label="知识点覆盖分析" name="knowledge">
          <el-card>
            <h3>知识点覆盖情况</h3>
            <div class="chart-container">
              <el-tree
                :data="knowledgeCoverageTree"
                node-key="id"
                :props="treeProps"
                default-expand-all
              >
                <template slot-scope="{ node, data }">
                  <span class="tree-node">
                    <span>{{ node.label }}</span>
                    <span class="question-count">({{ data.questionCount }}题)</span>
                    <el-progress :percentage="data.coverageRate" :stroke-width="8" :show-text="false" style="width: 100px; margin-left: 10px;"></el-progress>
                  </span>
                </template>
              </el-tree>
            </div>
          </el-card>
        </el-tab-pane>
        
        <el-tab-pane label="难度分布分析" name="difficulty">
          <el-card>
            <h3>题目难度分布</h3>
            <div class="chart-container">
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-chart :options="difficultyPieOptions"></el-chart>
                </el-col>
                <el-col :span="12">
                  <el-chart :options="difficultyBarOptions"></el-chart>
                </el-col>
              </el-row>
            </div>
          </el-card>
        </el-tab-pane>
        
        <el-tab-pane label="题型分布分析" name="type">
          <el-card>
            <h3>题型分布情况</h3>
            <div class="chart-container">
              <el-chart :options="typePieOptions"></el-chart>
            </div>
          </el-card>
        </el-tab-pane>
        
        <el-tab-pane label="使用情况分析" name="usage">
          <el-card>
            <h3>题目使用情况</h3>
            <div class="chart-container">
              <el-chart :options="usageLineOptions"></el-chart>
            </div>
          </el-card>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'Analysis',
  data() {
    return {
      activeTab: 'knowledge',
      treeProps: {
        children: 'children',
        label: 'name'
      },
      knowledgeCoverageTree: [],
      difficultyPieOptions: {
        title: {
          text: '难度分布',
          left: 'center'
        },
        tooltip: {
          trigger: 'item'
        },
        legend: {
          orient: 'vertical',
          left: 'left'
        },
        series: [
          {
            name: '难度',
            type: 'pie',
            radius: '50%',
            data: [],
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      },
      difficultyBarOptions: {
        title: {
          text: '各难度题目数量',
          left: 'center'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        xAxis: {
          type: 'category',
          data: ['L1 记忆', 'L2 理解', 'L3 应用', 'L4 分析', 'L5 创造']
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            data: [],
            type: 'bar'
          }
        ]
      },
      typePieOptions: {
        title: {
          text: '题型分布',
          left: 'center'
        },
        tooltip: {
          trigger: 'item'
        },
        legend: {
          orient: 'vertical',
          left: 'left'
        },
        series: [
          {
            name: '题型',
            type: 'pie',
            radius: '50%',
            data: [],
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      },
      usageLineOptions: {
        title: {
          text: '题目使用趋势',
          left: 'center'
        },
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: []
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            name: '使用次数',
            type: 'line',
            stack: 'Total',
            data: []
          }
        ]
      }
    }
  },
  mounted() {
    this.loadKnowledgeCoverage()
    this.loadDifficultyDistribution()
    this.loadTypeDistribution()
    this.loadUsageTrend()
  },
  methods: {
    loadKnowledgeCoverage() {
      this.$axios.get('/analysis/knowledge-coverage').then(response => {
        this.knowledgeCoverageTree = response.data
      }).catch(error => {
        console.error('加载知识点覆盖数据失败', error)
      })
    },
    loadDifficultyDistribution() {
      this.$axios.get('/analysis/difficulty-distribution').then(response => {
        const data = response.data
        const difficultyLabels = {
          'L1': 'L1 记忆',
          'L2': 'L2 理解',
          'L3': 'L3 应用',
          'L4': 'L4 分析',
          'L5': 'L5 创造'
        }
        
        const pieData = []
        const barData = []
        
        for (const [key, value] of Object.entries(data)) {
          pieData.push({ value: value, name: difficultyLabels[key] })
          barData.push(value)
        }
        
        this.difficultyPieOptions.series[0].data = pieData
        this.difficultyBarOptions.series[0].data = barData
      }).catch(error => {
        console.error('加载难度分布数据失败', error)
      })
    },
    loadTypeDistribution() {
      this.$axios.get('/analysis/type-distribution').then(response => {
        const data = response.data
        const pieData = []
        
        for (const [key, value] of Object.entries(data)) {
          pieData.push({ value: value, name: key })
        }
        
        this.typePieOptions.series[0].data = pieData
      }).catch(error => {
        console.error('加载题型分布数据失败', error)
      })
    },
    loadUsageTrend() {
      this.$axios.get('/analysis/usage-trend').then(response => {
        const data = response.data
        this.usageLineOptions.xAxis.data = data.months
        this.usageLineOptions.series[0].data = data.usage
      }).catch(error => {
        console.error('加载使用趋势数据失败', error)
      })
    }
  }
}
</script>

<style scoped>
.analysis {
  padding: 20px;
}

.chart-container {
  margin-top: 20px;
  height: 400px;
}

.tree-node {
  display: flex;
  align-items: center;
  width: 100%;
}

.question-count {
  margin-left: 10px;
  color: #606266;
}
</style>