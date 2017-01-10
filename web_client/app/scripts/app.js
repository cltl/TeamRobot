'use strict';

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
    var myIoSocket = io.connect('http://localhost:5000/event');

    var mySocket = socketFactory({
      ioSocket: myIoSocket
    });

    return mySocket;
  });
