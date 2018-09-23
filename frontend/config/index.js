"use strict";
// Template version: 1.3.1
// see http://vuejs-templates.github.io/webpack for documentation.

const path = require("path");

module.exports = {
  dev: {
    // Source maps.
    // https://webpack.js.org/configuration/devtool/#development
    devtool: "cheap-module-eval-source-map",

    // If you have problems debugging vue-files in devtools,
    // set this to false - it *may* help
    // https://vue-loader.vuejs.org/en/options.html#cachebusting
    cacheBusting: true,

    cssSourceMap: true
  },

  build: {
    indexTemplate: path.resolve(__dirname, "../src/index.html"),
    indexTarget: path.resolve(__dirname, "../dist/index.html"),

    // Paths
    distPath: path.resolve(__dirname, "../dist"),
    distPublicPath: "/",

    // Source maps.
    productionSourceMap: true,
    // https://webpack.js.org/configuration/devtool/#production
    devtool: "#source-map"
  }
};
