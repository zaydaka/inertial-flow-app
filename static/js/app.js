
'use strict';

var InertialFlowApp = angular.module('InertialFlowApp', [
  'ngRoute','flowControllers', 'flowDirectives', 'flowServices', 'checklist-model',
]);


InertialFlowApp.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/', {
        templateUrl: '../static/partials/home.html',
        // controller: 'IndexCtrl'
      }).
      when('/about', {
        templateUrl: '../static/partials/about.html',
        // controller: 'AboutCtrl'
      }).
      when('/uploaddata', {
        templateUrl: '../static/partials/uploaddata.html',
        controller: 'UploadDataController'
      }).
      when('/uploadjson', {
        templateUrl: '../static/partials/uploadjson.html',
        controller: 'UploadJsonController'
      }).
      when('/runnetwork', {
        templateUrl: '../static/partials/runnetwork.html',
        controller: 'RunNetworkController'
      }).
      otherwise({
        redirectTo: '/'
      });
}]);

