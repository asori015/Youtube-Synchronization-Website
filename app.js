const NodeMediaServer = require('node-media-server');

const config = {
  rtmp: {
    port: process.env.PORT,
    chunk_size: 60000,
    gop_cache: true,
    ping: 30,
    ping_timeout: 60
  },
  http: {
    port: 1935,
    allow_origin: '*'
  }
};

var nms = new NodeMediaServer(config)
nms.run();
