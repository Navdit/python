'use strict';

angular.module('myApp.gameView', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/en', {
    templateUrl: '/static/view/en.html',
    controller: 'GameCtrl'
  })
}])

.controller('GameCtrl', ['$scope', '$http', function($scope, $http) {
  
  var diffs = ['easy', 'medium', 'hard'];
  var pos = 0;
  var challenge = null;

  $scope.newgame = function() {
    pos = 0;
    $scope.answer1 = '';
    $scope.answer2 = '';
    $scope.answer1css = '';
    $scope.answer2css = '';
    $scope.answered = false;
    $scope.diff = 'easy';
    $scope.score = 0;
    
    $http.get('/api/v1.0/get_challenge').then(function(data) {
      challenge = data.data;
      $scope.route = challenge[$scope.diff][0];
    });
  }
  
  $scope.select = function(pos) {
    
    if ($scope.answered) return;
    
    var milesData = {
      "1": { "Route": $scope.route[0]['route_csv'] },
      "2": { "Route": $scope.route[1]['route_csv'] }
    }
    
    $http.post('/api/v1.0/get_route_miles', milesData).then(function(data) {
      if (pos==0 && data.data[1].Miles < data.data[2].Miles
        || pos==1 && data.data[1].Miles > data.data[2].Miles
      ) {
        $scope.score++;
      }
      $scope.answer1 = data.data[1].Miles + " miles";
      $scope.answer2 = data.data[2].Miles + " miles";
      
      if (data.data[1].Miles<data.data[2].Miles) {
        $scope.answer1css = 'panel-success';
      } else {
        $scope.answer2css = 'panel-success';
      }
      
      $scope.answered = true;
    });

  };
  
  $scope.next = function() {
    $scope.answer1 = '';
    $scope.answer2 = '';
    $scope.answer1css = '';
    $scope.answer2css = '';
    $scope.answered = false;

    if ($scope.diff == 'hard' && pos >=2) {
      $scope.answer1 = 'Game over!';
      $scope.answer2 = 'Game over!';
      return false;
    }
    
    pos++;
    if (pos > 2) {
      $scope.diff = diffs[diffs.indexOf($scope.diff)+1];
      pos = 0;
    }
    $scope.route = challenge[$scope.diff][pos];
  };
  
  $scope.newgame();
}]);