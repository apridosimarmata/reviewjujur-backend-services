var express = require('express');
var morgan = require('morgan');
var bodyParser = require('body-parser');

var app = express();

app.use(bodyParser.urlencoded({
  limit: '50mb',
  extended: true
}));

app.use(bodyParser.json({limit: '50mb'}));

app.use(morgan('combined'))

app.post("/", (req, res) => {
    
});

app.listen(5004, () => {
 console.log("Server running on port 5004");
});