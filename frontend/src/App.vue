<template>
  <div id="app">
    <div class="app-wrapper">
      <header class="app-header">
        <div class="header-content">
          <div class="header-left">
            <div class="logo">
              <div class="logo-icon">
                <svg class="logo-svg" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
                </svg>
              </div>
              <span class="logo-text">智能题库</span>
            </div>
            
            <nav class="main-nav">
              <router-link
                to="/"
                :class="['nav-link', $route.path === '/' ? 'nav-link-active' : '']"
              >
                <svg class="nav-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                </svg>
                题库管理
              </router-link>
              <router-link
                to="/rules"
                :class="['nav-link', $route.path === '/rules' ? 'nav-link-active' : '']"
              >
                <svg class="nav-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"/>
                </svg>
                规则管理
              </router-link>
              <router-link
                to="/question-compare"
                :class="['nav-link', $route.path === '/question-compare' ? 'nav-link-active' : '']"
              >
                <svg class="nav-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
                </svg>
                题目对比
              </router-link>
              <router-link
                to="/mcp-logs"
                :class="['nav-link', $route.path === '/mcp-logs' ? 'nav-link-active' : '']"
              >
                <svg class="nav-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                </svg>
                MCP服务
              </router-link>
            </nav>
          </div>
          
          <div class="header-right">
            <div class="user-info">
              <div class="user-name">李老师</div>
              <div class="user-dept">Python课程组</div>
            </div>
            <div class="user-avatar">
              <svg class="avatar-svg" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
              </svg>
            </div>
          </div>
        </div>
      </header>
      
      <main class="app-main">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style lang="less" scoped>
@import './assets/styles/variables.less';

.app-wrapper {
  min-height: 100vh;
  background-color: @bg-page !important;
}

#app {
  background-color: @bg-page !important;
  min-height: 100vh;
}

.app-header {
  background: @primary-color;
  border-bottom: none;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  max-width: @max-width;
  margin: 0 auto;
  padding: 0 @spacing-xl;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-left {
  display: flex;
  align-items: center;
  gap: @spacing-2xl;
}

.logo {
  display: flex;
  align-items: center;
  gap: @spacing-sm;
}

.logo-icon {
  width: 40px;
  height: 40px;
  background: @text-white;
  border-radius: @radius-md;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.logo-svg {
  width: 22px;
  height: 22px;
  color: @primary-color;
}

.logo-text {
  font-size: @font-size-lg;
  font-weight: 600;
  color: @text-white;
  letter-spacing: 0.5px;
}

.main-nav {
  display: flex;
  align-items: center;
  gap: @spacing-xs;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: @spacing-xs;
  padding: @spacing-sm @spacing-md;
  font-size: @font-size-md;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.75);
  border-radius: @radius-md;
  text-decoration: none;
  transition: all @transition-fast;

  &:hover {
    color: @text-white;
    background: rgba(255, 255, 255, 0.1);
  }

  &.nav-link-active {
    color: @text-white;
    background: rgba(255, 255, 255, 0.15);
    font-weight: 600;
  }
}

.nav-icon {
  width: 18px;
  height: 18px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: @spacing-md;
}

.user-info {
  text-align: right;
}

.user-name {
  font-size: @font-size-md;
  font-weight: 500;
  color: @text-white;
}

.user-dept {
  font-size: @font-size-xs;
  color: rgba(255, 255, 255, 0.65);
}

.user-avatar {
  width: 40px;
  height: 40px;
  background: @text-white;
  color: @primary-color;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: @font-size-md;
  font-weight: 600;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.avatar-svg {
  width: 22px;
  height: 22px;
}

.app-main {
  max-width: @max-width;
  margin: 0 auto;
  padding: @spacing-lg @spacing-lg;
  min-height: calc(100vh - 64px);
}
</style>
