var express = require("express");
var app = express();
const http = require('http');
var bodyParser = require('body-parser');
var fs = require("fs");


// support parsing of application/json type post data
app.use(bodyParser.json());
app.use(express.static('public'));

app.get("/", (req, res) => res.render("home.ejs"));


app.get("/search", function(localreq, localres) {
  console.log("Searching for results")
  console.log(localreq._parsedUrl.query);
  var customfilters = "/filters?";
  customfilters += localreq._parsedUrl.query;
  customfilters = customfilters.replace(/[+]/g, '%20');
  console.log("custom filter is:");
  console.log(customfilters);
  var options = {
    hostname: '35.190.152.161',
    // port: '80',
    path: customfilters,
    method: 'get',
    headers: {
      'content-type': 'application/json',
      'accept': 'application/json'
    },
    timeout: 600000000

  };

  var req = http.request(options, (res) => {
    var thereturn;
    res.setEncoding('utf8');
    res.on('data', (chunk) => {
      // console.log(`BODY: ${chunk}`);
      thereturn = chunk;

      // thereturn = JSON.parse(thereturn);
      console.log('thereturn inside', thereturn);

      fs.writeFile('./public/curgeo.json', thereturn, 'utf8', (err) => {
        console.log(err);
      });
      console.log("File has been created");

    });
    res.on('end', () => {
      console.log('No more data in response.');

      localres.render("result.ejs", {
        geojsonFeature: thereturn
      });
    });
  });

  req.on('error', (e) => {
    console.error(`problem with request: ${e.message}`);
  });
  req.end();

});



const server = app.listen(process.env.PORT,process.env.IP,function(){
    console.log("Server is listening!");
});

server.timeout = 600000000;  
