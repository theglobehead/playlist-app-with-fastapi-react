module.exports = {
  entry: ['./views/index.js'],
  mode: 'development',
  watch: true,  // Enable for easier frontend development
  output: {
    path: __dirname,
    filename: './views/dist/index.js',
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: [
            /node_modules/,
            /dist/
        ],
        use: {
          loader: "babel-loader",
          options: {
            presets: ['@babel/preset-env', '@babel/preset-react']
          }
        }
      },
    ]
  },
};