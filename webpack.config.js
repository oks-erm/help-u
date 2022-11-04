const path = require('path');

module.exports = {
  entry: './frontend_chat/src/index.tsx', 
  output: {
    filename: 'js-bundle.js',
    path: path.resolve(__dirname, './static'),  
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx|ts|tsx)$/,
        exclude: /node_modules/,
        loader: "babel-loader",
        options: { presets: ["@babel/preset-env", "@babel/preset-react", "@babel/preset-typescript"] }
      }
    ]
  }
};

