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

    $scope.messages = [];

    $scope.connection = {};
    $scope.connection.status = 'Not Connected';

    mySocket.on('connecting', function() {
      $scope.connection.status = 'Connecting';
    });

    mySocket.on('connect', function() {
      $scope.connection.status = 'Connected';

      //Username system
      /*var message = {};
      message.user = 'Philip the Robot';
      message.time = 'Now';
      message.text = 'Hi there! what\'s your name:';
      message.server = true;
      $scope.messages.push(message);*/
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
    });

    $scope.sendMessage = function() {
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

    $scope.sayHello = function() {
      var message = {};
      message.user = 'Philip the Robot';
      message.time = 'Now';
      message.text = 'Nice to meet you ' + this.username + '! You can tell me everything.';
      message.server = true;
      $scope.messages.push(message);
    };

    $scope.submit = function() {
      this.sendMessage();

      //Username system
      /*if(this.usernameSet) {
        this.sendMessage();
      } else {
        var username = this.inputText.split(" ")[0];
        this.username = username;
        this.usernameSet = true;

        var message = {};
        message.user = 'Me';
        message.time = 'Now';
        message.text = this.inputText;
        message.server = false;
        $scope.messages.push(message);

        this.sayHello();
        this.inputText = '';
      }*/
    };
  });
