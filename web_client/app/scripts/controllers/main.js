'use strict';

/**
 * @ngdoc function
 * @name wbApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the wbApp
 */
angular.module('wbApp')
  .controller('MainCtrl', function ($scope, mySocket) {
    this.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];

    $scope.messages = [];

    $scope.connection = {};
    $scope.connection.status = 'Not Connected';

    mySocket.on('connecting', function() {
      $scope.connection.status = 'Connecting';
    });

    mySocket.on('connect', function() {
      $scope.connection.status = 'Connected';
    });

    mySocket.on('reconnecting', function() {
      $scope.connection.status = 'Reconnecting';
    });

    mySocket.on('disconnect', function() {
      $scope.connection.status = 'Disconnect';
    });

    mySocket.on('response', function (data) {
      var message = {};
      message.user = 'Philip the Robot';
      message.time = 'Now';
      message.text = data;
      message.server = true;
      $scope.messages.push(message);

      $scope.bar = true;
    });

    $scope.submit = function() {
      if(this.inputText) {
        mySocket.emit('annotate', this.inputText);

        var message = {};
        message.user = 'Me';
        message.time = 'Now';
        message.text = this.inputText;
        message.server = false;
        $scope.messages.push(message);
        this.inputText = '';
      }
    };
  });
