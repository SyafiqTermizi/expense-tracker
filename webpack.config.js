// https://github.com/baileyherbert/svelte-webpack-starter

const path = require('path');
const SveltePreprocess = require('svelte-preprocess');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = {
    context: __dirname,
    entry: {
        style: "./expense_fe/js/style.js"
    },
    resolve: {
        alias: {
            // Note: Later in this config file, we'll automatically add paths from `tsconfig.compilerOptions.paths`
            svelte: path.resolve('node_modules', 'svelte')
        },
        extensions: ['.mjs', '.js', '.ts', '.svelte'],
        mainFields: ['svelte', 'browser', 'module', 'main'],
        conditionNames: ['svelte', 'browser']
    },
    output: {
        path: path.resolve('./static/'),
        filename: '[name].js',
    },
    plugins: [
        new MiniCssExtractPlugin(),
    ],
    module: {
        rules: [
            {
                test: /\.(sa|sc|c)ss$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    "css-loader",
                    "postcss-loader",
                    "sass-loader",
                ],
                exclude: /node_modules/,
            },
            {
                test: /\.svelte$/,
                use: {
                    loader: 'svelte-loader',
                    options: {
                        compilerOptions: {
                            // Dev mode must be enabled for HMR to work!
                            dev: true
                        },
                        emitCss: false,
                        hotReload: true,
                        hotOptions: {
                            // List of options and defaults: https://www.npmjs.com/package/svelte-loader-hot#usage
                            noPreserveState: false,
                            optimistic: true,
                        },
                        preprocess: SveltePreprocess({
                            scss: false,
                            sass: false,
                        })
                    }
                }
            },
            {
                test: /\.tsx?$/,
                use: 'ts-loader',
                exclude: /node_modules/,
            },
            {
                test: /node_modules\/svelte\/.*\.mjs$/,
                resolve: {
                    fullySpecified: false
                }
            },
        ]
    }
}