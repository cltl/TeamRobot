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
    this.username = '';
    this.usernameSet = false;

    $scope.response = {};
    $scope.response.concept = 'Hold on, we are connecting to the server!'
    $scope.response.emotion = 'Input some text!'
    $scope.response.mixed = 'Input some text!'

    $scope.connection = {};
    $scope.connection.status = 'Not Connected';

    mySocket.on('connecting', function() {
      $scope.connection.status = 'Connecting';
    });

    mySocket.on('connect', function() {
      $scope.connection.status = 'Connected';
      $scope.response.emotion = 'We have connected!'
      $scope.response.mixed = 'Input some text!'
    });

    mySocket.on('reconnecting', function() {
      $scope.connection.status = 'Reconnecting';
    });

    mySocket.on('disconnect', function() {
      $scope.connection.status = 'Disconnect';
    });

    mySocket.on('response', function (data) {
      console.log(data);
      $scope.response.concept = data.concept;
      $scope.response.emotion = data.emotion;
      $scope.response.mixed = data.mixed;
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
