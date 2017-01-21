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
    'btford.socket-io'
  ])
  .factory('mySocket', function (socketFactory) {
    var myIoSocket = io.connect('http://0.0.0.0:5000/event');

    var mySocket = socketFactory({
      ioSocket: myIoSocket
    });

    return mySocket;
  });
