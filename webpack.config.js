const path = require('path');

module.exports = {
  mode: 'production',
  entry: {
    chat: './frontend_chat/src/index.tsx',
    main: './static/assets/js/main.js',
  },
  output: {
    filename: '[name].js-bundle.js',
    path: path.resolve(__dirname, './static'),
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx|ts|tsx)$/,
        exclude: /node_modules/,
        loader: 'babel-loader',
        options: {
          presets: [
            '@babel/preset-env',
            '@babel/preset-react',
            '@babel/preset-typescript',
          ],
        },
      },
      {
        test: /\.css$/i,
        use: ['style-loader', 'css-loader', 'sass-loader'],
      },
    ],
  },
};


