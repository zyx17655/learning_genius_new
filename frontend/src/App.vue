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
            </nav>
          </div>
          
          <div class="header-right">
            <div class="user-info">
              <div class="user-name">李老师</div>
              <div class="user-dept">Python课程组</div>
            </div>
            <div class="user-avatar">
              李
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
  background: @bg-card;
  border-bottom: 1px solid @border-color;
  box-shadow: @shadow-sm;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  max-width: @max-width;
  margin: 0 auto;
  padding: 0 @spacing-xl;
  height: @header-height;
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
  width: 36px;
  height: 36px;
  background: @primary-color;
  border-radius: @radius-md;
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-svg {
  width: 20px;
  height: 20px;
  color: @text-white;
}

.logo-text {
  font-size: @font-size-lg;
  font-weight: 600;
  color: @text-primary;
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
  color: @text-secondary;
  border-radius: @radius-md;
  text-decoration: none;
  transition: all @transition-fast;

  &:hover {
    color: @text-primary;
    background: @bg-hover;
  }

  &.nav-link-active {
    color: @primary-color;
    background: fade(@primary-color, 8%);
  }
}

.nav-icon {
  width: 16px;
  height: 16px;
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
  color: @text-primary;
}

.user-dept {
  font-size: @font-size-xs;
  color: @text-muted;
}

.user-avatar {
  width: 36px;
  height: 36px;
  background: @primary-color;
  color: @text-white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: @font-size-md;
  font-weight: 500;
}

.app-main {
  max-width: @max-width;
  margin: 0 auto;
  padding: @spacing-xl;
  min-height: calc(100vh - @header-height);
}
</style>
