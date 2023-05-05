const { merge } = require('webpack-merge');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const common = require('./webpack.common.js');
const DotenvWebpack = require('dotenv-webpack');

module.exports = merge(common, {
  mode: 'production',
  plugins: [new CleanWebpackPlugin(), new DotenvWebpack()],
});
