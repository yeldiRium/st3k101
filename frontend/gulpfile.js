const gulp = require("gulp");
const path = require("path");
const rm = require('rimraf');
const webpack = require("webpack");
const config = require('./config');

gulp.task("cleanDist", done => {
    rm(config.build.distPath, done);
});

gulp.task("build", ["cleanDist"], done => {
    const webpackConfig = require('./webpack/webpack.prod.conf');
    webpack(webpackConfig, (err, stats) => {
        if (err) throw err;
        process.stdout.write(stats.toString({
            colors: true,
            modules: false,
            children: false, // If you are using ts-loader, setting this to true will make TypeScript errors show up during build.
            chunks: false,
            chunkModules: false
        }) + '\n\n');

        if (stats.hasErrors()) {
            console.log('  Build failed with errors.\n');
            process.exit(1);
        }

        console.log('  Build complete.\n');
        console.log(
            '  Tip: built files are meant to be served over an HTTP server.\n' +
            '  Opening index.html over file:// won\'t work.\n'
        );

        done();
    });
});

gulp.task("dev", ["cleanDist"], done => {
    const webpackConfig = require('./webpack/webpack.dev.conf');
    console.log(
        "Webpack will run in watch mode now.\n" +
        "To exit, interrupt the process (e.g. ctrl+c)."
    );
    webpack(webpackConfig, (err, stats) => {
        if (err) throw err;
        process.stdout.write(stats.toString({
            colors: true,
            modules: false,
            children: false,
            chunks: false,
            chunkModules: false
        }) + '\n\n');

        if (stats.hasErrors()) {
            console.log('  Build failed with errors.\n');
            process.exit(1);
        }

        console.log('  Build complete.\n');
    });
});