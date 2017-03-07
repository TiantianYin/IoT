'use strict';

console.log('Loading function');
exports.handler = (event, context, callback) => {
    //console.log('Received event:', JSON.stringify(event, null, 2));
    event.Records.forEach((record) => {
        // Kinesis data is base64 encoded so decode here
        const payload = new Buffer(record.kinesis.data, 'base64').toString('ascii');
        console.log('Decoded payload:', payload);
    });
    callback(null, `Successfully processed ${event.Records.length} records.`);
};

// If this file contains double-curly-braces, that's because
// it is a template that has not been processed into JavaScript yet.
console.log('Loading event');
exports.handler = function(event, context) {
  var AWS = require('aws-sdk');
  var sns = new AWS.SNS();
  var ml = new AWS.MachineLearning();
  var endpointUrl = 'https://realtime.machinelearning.us-east-1.amazonaws.com';
  var mlModelId = 'ml-MUUGZTVL2DWDPAPK';
  var snsTopicArn = 'arn:aws:sns:us-east-1:768104751743:Lab5';
  var snsMessageSubject = 'Switch or not: s';
  var snsMessagePrefix = 'ML model '+mlModelId;
  var numMessagesProcessed = 0;
  var numMessagesToBeProcessed = event.Records.length;
  console.log("numMessagesToBeProcessed:"+numMessagesToBeProcessed);

  var sendSns = function(tweetData) {
    var params = {};
    params['TopicArn'] = snsTopicArn;
    params['Subject']  = snsMessageSubject;
    params['Message']  = snsMessagePrefix+tweetData
    console.log('Calling Amazon SNS to publish.');
    sns.publish(
      params,
      function(err, data) {
        if (err) {
          console.log('1')
          console.log(err, err.stack); // an error occurred
          context.done(null, 'Failed when publishing to SNS');
        }
        else {
          console.log('2')
          context.done(null, 'Published to SNS');
        }
      }
      );
  }

  var callPredict = function(tweetData){
    console.log('calling predict');
    try{
      ml.predict(
        {
          Record : tweetData,
          PredictEndpoint : endpointUrl,
          MLModelId: mlModelId
        },
        function(err, data) {
          if (err) {
            console.log(err);
            console.log('11')
            context.done(null, 'Call to predict service failed.');
          }
          else {
            console.log('Predict call succeeded:'+data.Prediction.predictedLabel);
            //sendSns(data.Prediction.predictedLabel);
          }
        }
        );
      }
    catch (err) {
        console.log('####');
        console.log(err, err.stack);
        context.done(null, "failed call prd");
      }
    
  }

  var processRecords = function(){
    console.log('3')
    for(var i = 0; i < numMessagesToBeProcessed; ++i) {
      console.log('4')
      var approximateArrivalTimestamp = event.Records[i].kinesis.approximateArrivalTimestamp;
      // Amazon Kinesis data is base64 encoded so decode here
      //var payload = new Buffer(encodedPayload, 'base64').toString('utf-8');
      var prdData = new Map([['routeId', 1], ['timestamp', approximateArrivalTimestamp], ['dayOfWeek', 'weekday'], ['timeAt96', approximateArrivalTimestamp]]);
      console.log('!');
      try {
        var parsedPayload = {
            routeId: String(1),
            timestamp:  String(approximateArrivalTimestamp),
            dayOfWeek: 'weekday',
            timeAt96:  String(approximateArrivalTimestamp)
        }
        //var parsedPayload = JSON.parse(prdData);
        console.log('%');
        callPredict(parsedPayload);
        //callPredict(prdData);
        console.log('@');
      }
      catch (err) {
        console.log('#');
        console.log(err, err.stack);
        context.done(null, "failed prdData");
      }
    }
  }

  var checkRealtimeEndpoint = function(err, data){
    console.log('5');
    if (err){
      console.log(err);
      context.done(null, 'Failed to fetch endpoint status and url.');
    }
    else {
      var endpointInfo = data.EndpointInfo;

      if (endpointInfo.EndpointStatus === 'READY') {
        endpointUrl = endpointInfo.EndpointUrl;
        console.log('Fetched endpoint url :'+endpointUrl);
        processRecords();
      } else {
        console.log('Endpoint status : ' + endpointInfo.EndpointStatus);
        context.done(null, 'End point is not Ready.');
      }
    }
  }
  console.log('6');
  processRecords();
  //ml.getMLModel({MLModelId:mlModelId}, checkRealtimeEndpoint);
  console.log('complete');
};
