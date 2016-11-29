
'use strict';

var InertialFlowApp = angular.module('InertialFlowApp', [
  'ngRoute','flowControllers', 'flowDirectives', 'flowServices', 'checklist-model','FlowFactory',
]);


InertialFlowApp.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/', {
        templateUrl: '../static/partials/home.html',
        access: {restricted: false}
        // controller: 'IndexCtrl'
      }).
      when('/login', {
        templateUrl: '../static/partials/login.html',
        controller: 'loginController',
        access: {restricted: false}
        // controller: 'AboutCtrl'
      }).
      when('/register', {
        templateUrl: '../static/partials/register.html',
        controller: 'registerController',
        access: {restricted: false}
        // controller: 'AboutCtrl'
      }).
      when('/projects', {
        templateUrl: '../static/partials/projects.html',
        access: {restricted: false},
        controller: 'ProjectsController'
      }).
      when('/about', {
        templateUrl: '../static/partials/about.html',
        access: {restricted: true}
        // controller: 'AboutCtrl'
      }).
      when('/uploaddata', {
        templateUrl: '../static/partials/uploaddata.html',
        controller: 'UploadDataController',
        access: {restricted: true}
      }).
      when('/uploadjson', {
        templateUrl: '../static/partials/uploadjson.html',
        controller: 'UploadJsonController',
        access: {restricted: true}
      }).
      when('/runnetwork', {
        templateUrl: '../static/partials/runnetwork.html',
        controller: 'RunNetworkController',
        access: {restricted: true}
      }).
      when('/contact', {
        templateUrl: '../static/partials/contact.html',
        access: {restricted: false}
      }).
      when('/project', {
        templateUrl: '../static/partials/project.html',
        access: {restricted: true},
        controller: 'MyProjectController'
      }).
      otherwise({
        redirectTo: '/',
        access: {restricted: false}
      });
}]);

InertialFlowApp.run(function ($rootScope, $location, $route, $log, AuthService) {
  $rootScope.$on('$routeChangeStart',
    function (event, next, current) {
      AuthService.getUserStatus()
      .then(function(){

        if(AuthService.isLoggedIn()){
          $rootScope.example="Logout";
        }else{$rootScope.example="Login";}

        if (next.access.restricted && !AuthService.isLoggedIn()){
          $location.path('/login');
          $route.reload();
        }else{
          if(next.loadedTemplateUrl=="../static/partials/login.html"){
            AuthService.logout()
              .then(function () {
                $rootScope.example="Login"
              $location.path('/login');
            }); 
          }
        }




      });
  });
});



