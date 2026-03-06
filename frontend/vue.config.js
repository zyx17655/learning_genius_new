module.exports = {
  devServer: {
    port: 8081,
    open: true
  },
  css: {
    loaderOptions: {
      less: {
        lessOptions: {
          javascriptEnabled: true
        }
      }
    }
  },
  lintOnSave: false
}
