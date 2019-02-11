const webpack = require('webpack');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const CSSExtract = new ExtractTextPlugin('styles.css');
const CopyWebpackPlugin = require('copy-webpack-plugin');

module.exports = {
    entry: ['babel-polyfill', './src/app.js'],

    module: {
        rules: [
            {
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                use: ['babel-loader']
            },
            {
                test: /\.s?css$/,
                use: CSSExtract.extract({
                    use: [
                        {
                            loader: 'css-loader'

                        },
                        {
                            loader: 'sass-loader'

                        }
                    ]
                })
            },
            {
                test: /\.html$/,
                loader: "file-loader?name=[name].[ext]",
            },
        ]
    },
    resolve: {
        extensions: ['*', '.js', '.jsx']
    },
    output: {
        path: __dirname + '/dist',
        publicPath: '/',
        filename: 'bundle.js',
    },
    plugins: [
        CSSExtract,
        new webpack.HotModuleReplacementPlugin(),
        new CopyWebpackPlugin([
            {from: './public/index.html', to: 'index.html'},
            {from: './public/images', to: 'images'},
        ])
    ],
    devServer: {
        inline: true,
        contentBase: './dist',
        port: 4000,
        // contentBase: [path.join(process.cwd(), 'public'), path.join(process.cwd(), 'src')],
        hot: true,
        // port: 4000,
        // publicPath: path.join(process.cwd(), '/dist'),
        historyApiFallback: true,
        // inline: true,
    }
};

