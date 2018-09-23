"use strict";
const path = require("path");
const utils = require("./utils");
const webpack = require("webpack");
const config = require("../config");
const merge = require("webpack-merge");
const baseWebpackConfig = require("./webpack.base.conf");
const UglifyJsPlugin = require("uglifyjs-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const CopyWebpackPlugin = require("copy-webpack-plugin");

const env = require("../config/prod.env");

module.exports = merge(baseWebpackConfig, {
  mode: "production",

  output: {
    path: config.build.distPath,
    filename: "js/[name].[chunkhash].js",
    chunkFilename: "js/[id].[chunkhash].js"
  },
  devtool: config.build.productionSourceMap ? config.build.devtool : false,
  optimization: {
    concatenateModules: true,
    splitChunks: {
      chunks: "all",
      name: true
    }
  },
  module: {
    rules: utils.styleLoaders({
      sourceMap: config.build.productionSourceMap,
      extract: true
    })
  },
  plugins: [
    // http://vuejs.github.io/vue-loader/en/workflow/production.html
    new webpack.DefinePlugin({
      "process.env": env
    }),
    new UglifyJsPlugin({
      uglifyOptions: {
        compress: {
          warnings: false
        }
      },
      sourceMap: config.build.productionSourceMap,
      parallel: true
    }),
    // extract css into its own file
    new MiniCssExtractPlugin({
      filename: "css/[name].[contenthash].css",
      allChunks: true
    }),
    // generate dist index.html with correct asset hash for caching.
    // you can customize output by editing /index.html
    // see https://github.com/ampedandwired/html-webpack-plugin
    new HtmlWebpackPlugin({
      template: config.build.indexTemplate,
      filename: config.build.indexTarget,
      inject: true,
      minify: {
        removeComments: true,
        collapseWhitespace: true,
        removeAttributeQuotes: true
        // more options:
        // https://github.com/kangax/html-minifier#options-quick-reference
      },
      // necessary to consistently work with multiple chunks via CommonsChunkPlugin
      chunksSortMode: "dependency"
    }),
    // keep module.id stable when vendor modules does not change
    new webpack.HashedModuleIdsPlugin(),
    // copy custom static assets
    new CopyWebpackPlugin([
      {
        from: path.resolve(__dirname, "../static"),
        to: config.build.distAssetsPath,
        ignore: [".*"]
      }
    ])
  ]
});
