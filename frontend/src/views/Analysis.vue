<template>
  <div class="page-wrapper">
    <section class="welcome-section">
      <div class="welcome-content">
        <h1 class="welcome-title">题目分析</h1>
        <p class="welcome-subtitle">多维度数据分析，深入了解题库状况</p>
      </div>
    </section>

    <div class="analysis-content">
      <!-- 自定义标签页 -->
      <div class="tabs-new">
        <div
          v-for="tab in tabs"
          :key="tab.name"
          class="tab-item"
          :class="{ active: activeTab === tab.name }"
          @click="activeTab = tab.name"
        >
          {{ tab.label }}
        </div>
      </div>

      <!-- 知识点覆盖分析 -->
      <div v-if="activeTab === 'knowledge'" class="tab-panel">
        <div class="content-card">
          <h3 class="card-title">知识点覆盖情况</h3>
          <div class="knowledge-tree">
            <div
              v-for="node in knowledgeCoverageTree"
              :key="node.id"
              class="tree-node-new"
            >
              <div class="tree-node-header" @click="toggleNode(node)">
                <span class="tree-icon" :class="{ expanded: node.expanded }">
                  <i v-if="node.children && node.children.length" class="el-icon-arrow-right"></i>
                </span>
                <span class="tree-label">{{ node.name }}</span>
                <span class="question-count">({{ node.questionCount }}题)</span>
                <div class="progress-bar-mini">
                  <div
                    class="progress-fill"
                    :style="{ width: node.coverageRate + '%' }"
                  ></div>
                </div>
                <span class="progress-text">{{ node.coverageRate }}%</span>
              </div>
              <div v-if="node.expanded && node.children" class="tree-children">
                <div
                  v-for="child in node.children"
                  :key="child.id"
                  class="tree-node-child"
                >
                  <span class="tree-label">{{ child.name }}</span>
                  <span class="question-count">({{ child.questionCount }}题)</span>
                  <div class="progress-bar-mini">
                    <div
                      class="progress-fill"
                      :style="{ width: child.coverageRate + '%' }"
                    ></div>
                  </div>
                  <span class="progress-text">{{ child.coverageRate }}%</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 难度分布分析 -->
      <div v-if="activeTab === 'difficulty'" class="tab-panel">
        <div class="charts-grid">
          <div class="content-card chart-card">
            <h3 class="card-title">难度分布</h3>
            <div class="chart-container">
              <div class="pie-chart" ref="difficultyPieChart"></div>
            </div>
          </div>
          <div class="content-card chart-card">
            <h3 class="card-title">各难度题目数量</h3>
            <div class="chart-container">
              <div class="bar-chart" ref="difficultyBarChart"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- 题型分布分析 -->
      <div v-if="activeTab === 'type'" class="tab-panel">
        <div class="content-card">
          <h3 class="card-title">题型分布情况</h3>
          <div class="chart-container">
            <div class="pie-chart large" ref="typePieChart"></div>
          </div>
        </div>
      </div>

      <!-- 使用情况分析 -->
      <div v-if="activeTab === 'usage'" class="tab-panel">
        <div class="content-card">
          <h3 class="card-title">题目使用趋势</h3>
          <div class="chart-container">
            <div class="line-chart" ref="usageLineChart"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Analysis',
  data() {
    return {
      activeTab: 'knowledge',
      tabs: [
        { name: 'knowledge', label: '知识点覆盖分析' },
        { name: 'difficulty', label: '难度分布分析' },
        { name: 'type', label: '题型分布分析' },
        { name: 'usage', label: '使用情况分析' }
      ],
      knowledgeCoverageTree: [],
      difficultyData: {},
      typeData: {},
      usageData: { months: [], usage: [] }
    }
  },
  mounted() {
    this.loadKnowledgeCoverage()
    this.loadDifficultyDistribution()
    this.loadTypeDistribution()
    this.loadUsageTrend()
  },
  watch: {
    activeTab(newVal) {
      if (newVal === 'difficulty') {
        this.$nextTick(() => {
          this.renderDifficultyCharts()
        })
      } else if (newVal === 'type') {
        this.$nextTick(() => {
          this.renderTypeChart()
        })
      } else if (newVal === 'usage') {
        this.$nextTick(() => {
          this.renderUsageChart()
        })
      }
    }
  },
  methods: {
    toggleNode(node) {
      if (node.children && node.children.length) {
        this.$set(node, 'expanded', !node.expanded)
      }
    },
    loadKnowledgeCoverage() {
      this.$axios.get('/analysis/knowledge-coverage').then(response => {
        this.knowledgeCoverageTree = response.data.map(node => ({
          ...node,
          expanded: false
        }))
      }).catch(error => {
        console.error('加载知识点覆盖数据失败', error)
      })
    },
    loadDifficultyDistribution() {
      this.$axios.get('/analysis/difficulty-distribution').then(response => {
        this.difficultyData = response.data
      }).catch(error => {
        console.error('加载难度分布数据失败', error)
      })
    },
    loadTypeDistribution() {
      this.$axios.get('/analysis/type-distribution').then(response => {
        this.typeData = response.data
      }).catch(error => {
        console.error('加载题型分布数据失败', error)
      })
    },
    loadUsageTrend() {
      this.$axios.get('/analysis/usage-trend').then(response => {
        this.usageData = response.data
      }).catch(error => {
        console.error('加载使用趋势数据失败', error)
      })
    },
    renderDifficultyCharts() {
      // 简化的饼图渲染
      const pieContainer = this.$refs.difficultyPieChart
      if (pieContainer && Object.keys(this.difficultyData).length > 0) {
        this.renderSimplePieChart(pieContainer, this.difficultyData, {
          'L1': 'L1 记忆',
          'L2': 'L2 理解',
          'L3': 'L3 应用',
          'L4': 'L4 分析',
          'L5': 'L5 创造'
        })
      }

      // 简化的柱状图渲染
      const barContainer = this.$refs.difficultyBarChart
      if (barContainer && Object.keys(this.difficultyData).length > 0) {
        this.renderSimpleBarChart(barContainer, this.difficultyData, [
          'L1 记忆', 'L2 理解', 'L3 应用', 'L4 分析', 'L5 创造'
        ])
      }
    },
    renderTypeChart() {
      const container = this.$refs.typePieChart
      if (container && Object.keys(this.typeData).length > 0) {
        this.renderSimplePieChart(container, this.typeData)
      }
    },
    renderUsageChart() {
      const container = this.$refs.usageLineChart
      if (container && this.usageData.months && this.usageData.months.length > 0) {
        this.renderSimpleLineChart(container, this.usageData)
      }
    },
    renderSimplePieChart(container, data, labelMap = null) {
      const total = Object.values(data).reduce((sum, val) => sum + val, 0)
      const colors = ['#1a1a2e', '#16213e', '#0f3460', '#533483', '#e94560']

      let html = '<div class="simple-pie-chart">'
      let startAngle = 0

      Object.entries(data).forEach(([key, value], index) => {
        const percentage = (value / total) * 100
        const angle = (percentage / 100) * 360
        const color = colors[index % colors.length]
        const label = labelMap ? labelMap[key] : key

        html += `
          <div class="pie-segment" style="
            background: conic-gradient(${color} ${angle}deg, transparent ${angle}deg);
            transform: rotate(${startAngle}deg);
          "></div>
        `
        startAngle += angle
      })

      html += '<div class="pie-center"></div></div>'
      html += '<div class="pie-legend">'
      Object.entries(data).forEach(([key, value], index) => {
        const percentage = ((value / total) * 100).toFixed(1)
        const color = colors[index % colors.length]
        const label = labelMap ? labelMap[key] : key
        html += `
          <div class="legend-item">
            <span class="legend-color" style="background: ${color}"></span>
            <span class="legend-label">${label}</span>
            <span class="legend-value">${value} (${percentage}%)</span>
          </div>
        `
      })
      html += '</div>'

      container.innerHTML = html
    },
    renderSimpleBarChart(container, data, labels) {
      const maxValue = Math.max(...Object.values(data))
      const colors = ['#1a1a2e', '#16213e', '#0f3460', '#533483', '#e94560']

      let html = '<div class="simple-bar-chart">'
      labels.forEach((label, index) => {
        const key = Object.keys(data)[index] || label.split(' ')[0]
        const value = data[key] || 0
        const height = maxValue > 0 ? (value / maxValue) * 100 : 0
        const color = colors[index % colors.length]

        html += `
          <div class="bar-item">
            <div class="bar-wrapper">
              <div class="bar" style="height: ${height}%; background: ${color}">
                <span class="bar-value">${value}</span>
              </div>
            </div>
            <span class="bar-label">${label}</span>
          </div>
        `
      })
      html += '</div>'

      container.innerHTML = html
    },
    renderSimpleLineChart(container, data) {
      const maxValue = Math.max(...data.usage)
      const minValue = Math.min(...data.usage)
      const range = maxValue - minValue || 1

      let points = ''
      const stepX = 100 / (data.months.length - 1)

      data.usage.forEach((value, index) => {
        const x = index * stepX
        const y = 100 - ((value - minValue) / range) * 80 - 10
        points += `${x},${y} `
      })

      let html = `
        <div class="simple-line-chart">
          <svg viewBox="0 0 100 100" preserveAspectRatio="none">
            <polyline
              fill="none"
              stroke="#1a1a2e"
              stroke-width="0.5"
              points="${points}"
            />
            <polygon
              fill="rgba(26, 26, 46, 0.1)"
              stroke="none"
              points="0,100 ${points} 100,100"
            />
          </svg>
          <div class="line-labels">
      `

      data.months.forEach((month, index) => {
        const left = (index / (data.months.length - 1)) * 100
        html += `<span class="line-label" style="left: ${left}%">${month}</span>`
      })

      html += '</div></div>'
      container.innerHTML = html
    }
  }
}
</script>

<style lang="less" scoped>
.analysis-content {
  padding: 0 40px 40px;
}

// 标签页样式
.tabs-new {
  display: flex;
  gap: 8px;
  margin-bottom: 24px;
  padding: 6px;
  background: #f5f5f0;
  border-radius: 12px;
  width: fit-content;

  .tab-item {
    padding: 10px 20px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
    color: #666;
    cursor: pointer;
    transition: all 0.2s ease;

    &:hover {
      color: #1a1a2e;
    }

    &.active {
      background: #1a1a2e;
      color: #fff;
    }
  }
}

.tab-panel {
  animation: fadeIn 0.3s ease;
}

// 知识点树样式
.knowledge-tree {
  padding: 16px 0;
}

.tree-node-new {
  margin-bottom: 8px;
}

.tree-node-header {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  background: #f5f5f0;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover {
    background: #ebe8e0;
  }
}

.tree-icon {
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 8px;
  transition: transform 0.2s ease;

  &.expanded {
    transform: rotate(90deg);
  }

  i {
    font-size: 12px;
    color: #666;
  }
}

.tree-label {
  font-size: 14px;
  font-weight: 500;
  color: #1a1a2e;
}

.question-count {
  margin-left: 8px;
  font-size: 13px;
  color: #666;
}

.progress-bar-mini {
  width: 100px;
  height: 6px;
  background: #e0ddd5;
  border-radius: 3px;
  margin-left: 16px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #1a1a2e, #533483);
  border-radius: 3px;
  transition: width 0.3s ease;
}

.progress-text {
  margin-left: 8px;
  font-size: 12px;
  font-weight: 500;
  color: #1a1a2e;
  min-width: 36px;
  text-align: right;
}

.tree-children {
  margin-left: 32px;
  margin-top: 8px;
}

.tree-node-child {
  display: flex;
  align-items: center;
  padding: 10px 16px;
  background: #fafaf8;
  border-radius: 6px;
  margin-bottom: 6px;
}

// 图表网格
.charts-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;

  @media (max-width: 1024px) {
    grid-template-columns: 1fr;
  }
}

.chart-card {
  min-height: 400px;
}

.chart-container {
  margin-top: 20px;
  height: 320px;
  display: flex;
  align-items: center;
  justify-content: center;
}

// 简单饼图样式
.pie-chart {
  display: flex;
  align-items: center;
  gap: 40px;

  &.large {
    transform: scale(1.2);
  }
}

.simple-pie-chart {
  position: relative;
  width: 180px;
  height: 180px;
  border-radius: 50%;
}

.pie-segment {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
}

.pie-center {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100px;
  height: 100px;
  background: #fff;
  border-radius: 50%;
}

.pie-legend {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 2px;
}

.legend-label {
  font-size: 13px;
  color: #666;
  min-width: 80px;
}

.legend-value {
  font-size: 13px;
  font-weight: 500;
  color: #1a1a2e;
}

// 简单柱状图样式
.bar-chart {
  width: 100%;
  height: 100%;
}

.simple-bar-chart {
  display: flex;
  align-items: flex-end;
  justify-content: space-around;
  height: 100%;
  padding: 20px;
}

.bar-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
  max-width: 80px;
}

.bar-wrapper {
  width: 40px;
  height: 220px;
  display: flex;
  align-items: flex-end;
  background: #f5f5f0;
  border-radius: 4px 4px 0 0;
  overflow: hidden;
}

.bar {
  width: 100%;
  border-radius: 4px 4px 0 0;
  position: relative;
  transition: height 0.3s ease;
  min-height: 4px;
}

.bar-value {
  position: absolute;
  top: -20px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 12px;
  font-weight: 500;
  color: #1a1a2e;
}

.bar-label {
  margin-top: 12px;
  font-size: 12px;
  color: #666;
  text-align: center;
}

// 简单折线图样式
.line-chart {
  width: 100%;
  height: 100%;
}

.simple-line-chart {
  position: relative;
  width: 100%;
  height: 260px;

  svg {
    width: 100%;
    height: 100%;
  }
}

.line-labels {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-between;
  padding: 0 10px;
}

.line-label {
  font-size: 11px;
  color: #666;
  transform: translateX(-50%);
  white-space: nowrap;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
