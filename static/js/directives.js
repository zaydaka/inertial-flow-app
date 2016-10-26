'use strict';

/* Directives */

//var inertialFlowDirectives = angular.module('inertialFlowDirectives', []);


var flowDirectives = angular.module('flowDirectives',[])


//////////////////////////////////////////////////////////////
//// Custom directive for file  type ////
//////////////////////////////////////////////////////////////

flowDirectives.directive('fileModel', ['$parse', function ($parse) {
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
            var model = $parse(attrs.fileModel);
            var modelSetter = model.assign;
            
            element.bind('change', function(){
                scope.$apply(function(){
                    modelSetter(scope, element[0].files[0]);
                });
            });
        }
    };
}]);



flowDirectives.directive('wordCountChart', ['$parse', function ($parse) {
  return {
    restrict: 'E',
    replace: true,
    template: '<div id="chart"></div>',
    link: function (scope) {}
   };
}]);
