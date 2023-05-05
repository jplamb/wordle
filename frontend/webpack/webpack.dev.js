const { merge } = require('webpack-merge');
const common = require('./webpack.common.js');
const path = require('path');
const DotenvWebpack = require('dotenv-webpack');

module.exports = merge(common, {
  mode: 'development',
  devtool: 'inline-source-map',
  entry: './src/index.tsx',
  output: {
    path: path.resolve(__dirname, 'public', 'frontend'),
    filename: 'bundle.js',
    publicPath: 'http://localhost:8080/static/frontend/', // Add this line
  },
  plugins: [new DotenvWebpack()]
});
