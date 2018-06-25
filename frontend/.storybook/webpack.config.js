const path = require("path");

const vueLoaderConfig = require('../build/vue-loader.conf');

module.exports = {
    resolve: {
        extensions: ['.js', '.vue', '.json'],
        alias: {
            'vue$': 'vue/dist/vue.esm.js'
        }
    },
    module: {
        rules: [
            {
                test: /\.svg$/,
                loader: 'vue-svg-loader', // `vue-svg` for webpack 1.x
                options: {
                    // optional [svgo](https://github.com/svg/svgo) options
                    svgo: {
                        plugins: [
                            {removeDoctype: true},
                            {removeComments: true}
                        ]
                    }
                },
                include: path.resolve(__dirname, "..")
            }
        ]
    }
};
