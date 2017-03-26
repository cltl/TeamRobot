'use strict';

/**
 * @ngdoc function
 * @name wbApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the wbApp
 */
angular.module('wbApp')
  .controller('MainCtrl', function ($scope, $rootScope, mySocket) {
    var connected = false;

    $scope.response = {};
    $scope.response.concept = 'Hold on, we are connecting to the server!';
    $scope.response.emotion = 'Hold on, we are connecting to the server!';
    $scope.response.mixed = 'Hold on, we are connecting to the server!';
    $scope.emotion = '...';
    $scope.topic = '...';
    $scope.concept = '...';
    $scope.conceptType = '...';


    $scope.connection = {};
    $scope.connection.true = false;
    $scope.connection.status = 'Not Connected';

    mySocket.on('connecting', function() {
      $scope.connection.status = 'Connecting';
    });

    mySocket.on('connect', function() {
      $scope.connection.status = 'Connected';
      $scope.connection.true = true;

      if(connected == false) {
        connected = true;
        $scope.response.concept = 'We have connected to the server :)';
        $scope.response.emotion = 'Please enter some text into the input box.';
        $scope.response.mixed = 'Generating the response might take a few seconds so please be patient!';
      }
    });

    mySocket.on('reconnecting', function() {
      $scope.connection.status = 'Reconnecting';
      $scope.connection.true = false;
    });

    mySocket.on('disconnect', function() {
      $scope.connection.status = 'Disconnect';
      $scope.connection.true = false;
    });

    mySocket.on('response', function (data) {
      console.log(data);
      $scope.response.concept = data.responses.concept;
      $scope.response.emotion = data.responses.emotion;
      $scope.response.mixed = data.responses.mixed;
      $scope.emotion = data.emotion;
      $scope.topic = data.topic;
      $scope.concept = data.concept;
      $scope.conceptType = data.concept_type;
    });

    $scope.sendMessage = function() {
      if(this.inputText) {
        mySocket.emit('annotate', this.inputText);
      }
    };


    $scope.submit = function($event) {
      $event.preventDefault();
      console.log('Do submit');
      this.sendMessage();
    };
  });
