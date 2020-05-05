"use strict";

const path = require('path');
const WebpackManifestPlugin = require('webpack-yam-plugin');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');

const PRODUCTION = process.env.PRODUCTION === '1';
const MANIFEST_PATH = path.join(__dirname, 'admin_list_controls/webpack_manifest.json');
const STATIC_ROOT = path.join(__dirname, 'admin_list_controls/static');
const OUTPUT_DIR = path.join(STATIC_ROOT, 'admin_list_controls/dist');

module.exports = function() {
	if (PRODUCTION) {
		console.log('Building for production...');
	} else {
	    console.log('Building for development...');
	}

	const config = {
		context: __dirname,
		entry: {
			admin_list_controls: './admin_list_controls/src/admin_list_controls',
		},
		output: {
			path: OUTPUT_DIR,
			filename: '[name]-[hash].js'
		},
		module: {
			rules: [
				{
					test: /\.jsx?$/,
					exclude: /node_modules|bower_components/,
					loader: 'babel-loader'
				},
				{
					test: /\.s[ac]ss$/i,
					use: [
						'style-loader',
						'css-loader',
						'sass-loader',
					],
				},
			]
		},
		plugins: [
			new WebpackManifestPlugin({
				manifestPath: MANIFEST_PATH,
				outputRoot: STATIC_ROOT
			}),
			// All files inside webpack's output.path directory will be removed once, but the
         	// directory itself will not be. If using webpack 4+'s default configuration,
         	// everything under <PROJECT_DIR>/dist/ will be removed.
			// During rebuilds, all webpack assets that are not used anymore
			// will be removed automatically.
			new CleanWebpackPlugin(),
		]
	};

	if (PRODUCTION) {
		config.optimization = {
			minimize: true
        };
		config.mode = 'production';
		config.devtool = 'source-map';
	} else {
		config.mode = 'development';
		config.devtool = 'eval-source-map';
	}

	return config;
};
