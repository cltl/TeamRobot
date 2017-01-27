'use strict';

/**
 * @ngdoc function
 * @name wbApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the wbApp
 */
angular.module('wbApp')
  .controller('ResponseCtrl', function ($scope, $rootScope, $routeParams, $http) {
    $rootScope.bodyClass = 'response-editor';

    $scope.files = [];

    $scope.getFiles = function() {
      $http.get('http://' + location.hostname + ':5000/responses').then(function(response) {
        $scope.files = response.data;
      }, function(response) {
      });
    };

    $scope.getFiles();
  });
