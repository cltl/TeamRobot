'use strict';
var io;

/**
 * @ngdoc overview
 * @name wbApp
 * @description
 * # wbApp
 *
 * Main module of the application.
 */
angular
  .module('wbApp', [
    'ngAnimate',
    'btford.socket-io',
    'ngRoute',
    'ngSanitize'
  ])
  .factory('mySocket', function (socketFactory) {
    var myIoSocket = io.connect('http://' + location.hostname + ':5000/event');

    var mySocket = socketFactory({
      ioSocket: myIoSocket
    });

    return mySocket;
  })
  .config(function($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl : 'views/home.html',
        controller: 'MainCtrl'
      })
      .when('/responses', {
        templateUrl : 'views/responses.html',
        controller: 'ResponseCtrl'
      })
      .when('/responses/:FILE', {
        templateUrl : 'views/responseView.html',
        controller: 'ResponseViewCtrl'
      });
  });
