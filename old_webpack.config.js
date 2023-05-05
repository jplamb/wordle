const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
  entry: './frontend/src/index.tsx',
  output: {
    path: path.resolve(__dirname, 'frontend', 'dist'),
    filename: 'main.[contenthash].js',
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: 'frontend/build/static/template.html',
      filename: 'index.html',
    }),
  ],
  module: {
    rules: [
      {
        test: /\.(ts|tsx)$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: [
              '@babel/preset-env',
              '@babel/preset-react',
              '@babel/preset-typescript',
            ],
          },
        },
      },
    ],
  },
  resolve: {
    extensions: ['.ts', '.tsx', '.js']
  },
};
