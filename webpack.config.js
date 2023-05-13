var path = require('path');

const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = {
    context: __dirname,
    entry: {
        style: "./expense_fe/js/style.js",
    },
    output: {
        path: path.resolve('./static/'),
        filename: '[name].js',
    },
    plugins: [new MiniCssExtractPlugin()],
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
        ]
    }
}