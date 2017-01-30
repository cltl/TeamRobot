'use strict';

/**
 * @ngdoc function
 * @name wbApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the wbApp
 */
angular.module('wbApp')
  .controller('ResponseViewCtrl', function ($scope, $rootScope, $routeParams, $http) {
    $rootScope.bodyClass = 'response-editor';

    $scope.file = $routeParams.FILE;

    $scope.positives = [];
    $scope.neutrals = [];
    $scope.negatives = [];

    $scope.beautify = function(text) {
      var beautified = text.replace('<type>', '<span class="highlight-type">&lt;type&gt;</span>');
      return beautified;
    };

    $scope.addResponse = function(target) {
      var response = {};
      response.text = "New response with <type>";
      response.styled = $scope.beautify(response.text);
      response.edit = false;
      target.push(response);
    };

    $scope.removeResponse = function(target) {
      var remove = confirm('Are you sure you want to remove the last response?');
      if (remove === true) {
        target.pop();
      }
    };

    $scope.saveResponses = function() {
      var responses = {};
      responses.positive = $scope.positives.map(function(a) {return {question: a.text};});
      responses.neutral = $scope.neutrals.map(function(a) {return {question: a.text};});
      responses.negative = $scope.negatives.map(function(a) {return {question: a.text};});
      $http.post('http://' + location.hostname + ':5000/responses/' + $scope.file, responses).then(function(resp) {
        $scope.getFile();
      });
    };

    $scope.getFile = function() {
      $http.get('http://' + location.hostname + ':5000/responses/'+$scope.file).then(function(resp) {
        $scope.entityType = resp.data['type'];
        $scope.positives = [];
        $scope.neutrals = [];
        $scope.negatives = [];

        var response;
        var i;

        var positiveResponses = resp.data['responses']['positive'];
        for (i = 0; i < positiveResponses.length; i++) {
          response = {};
          response.text = positiveResponses[i].question;
          response.styled = $scope.beautify(response.text);
          response.edit = false;
          $scope.positives.push(response);
        }

        var neutralResponses = resp.data['responses']['neutral'];
        for (i = 0; i < neutralResponses.length; i++) {
          response = {};
          response.text = neutralResponses[i].question;
          response.styled = $scope.beautify(response.text);
          response.edit = false;
          $scope.neutrals.push(response);
        }

        var negativeResponses = resp.data['responses']['negative'];
        for(i = 0; i < negativeResponses.length; i++) {
          response = {};
          response.text = negativeResponses[i].question;
          response.styled = $scope.beautify(response.text);
          response.edit = false;
          $scope.negatives.push(response);
        }
      }, function(response) {
      });
    }

    $scope.getFile();
  })
  .controller('EditResponseCtrl', function ($scope, $element, $timeout) {
    var input = $('input', $element);

    $scope.updateResponse = function() {
      $scope.response.edit = !$scope.response.edit;
      $scope.response.styled = $scope.beautify($scope.response.text);
    }

    $scope.$watch('response.edit', function (newValue, oldValue) {
      if (newValue === true) {
        $timeout(function(){
          input.focus();
        });
      }
    });
  });
