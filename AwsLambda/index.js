const Influx = require('influx');
const Line = require('./line');
const myLine = new Line();
var text = null;
exports.handler = async (event,context,callback) => {
    var moistureValue = JSON.parse(event.moistureValue);
    text = "土壌水分量を測定しました。\n土壌水分量：" + moistureValue + "\n過去のデータは下記リンクを参照してください。\n" +"http://18.237.225.63:3000/d/wfwyOrR4k/moisture?orgId=1"

    var result = writeToInfluxDB (moistureValue);
    callback(null, result);
  };

function writeToInfluxDB(moistureValue)
{
    console.log("Executing Iflux insert");

    const client = new Influx.InfluxDB({
        database: process.env.INFLUXDB,
        username: process.env.INFLUXDBUSRNAME,
        password: process.env.INFLUXDBPWD,
        port: process.env.INFLUXDBPORT,
        hosts: [{ host: process.env.INFLUXDBHOST }],
        schema: [{
            measurement: 'moisture',
            fields: {
                moistureValue: Influx.FieldType.FLOAT, 
            }
            ,
            tags: []
        }]
    });

    client.writePoints([{
        measurement: 'moisture', fields: { moistureValue: moistureValue}

    }])
    // LINE Notify トークンセット
    myLine.setToken(process.env.LINE_TOKEN);
    // LINE Notify 実行（「こんにちは！」とメッセージを送る）
    myLine.notify(text);
    console.log("Finished executing");
}