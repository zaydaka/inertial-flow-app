'use strict';

/* Directives */

//var inertialFlowDirectives = angular.module('inertialFlowDirectives', []);


var flowServices = angular.module('flowServices',[])


//////////////////////////////////////////////////////////////
//// Service for uploading a file //
//////////////////////////////////////////////////////////////

flowServices.service('fileUpload', ['$http', function ($http) {
    this.uploadFileToUrl = function(file, uploadUrl){
        var fd = new FormData();
        fd.append('file', file);
        $http.post(uploadUrl, fd, {
            transformRequest: angular.identity,
            headers: {'Content-Type': undefined}
        })
        .success(function(){
        })
        .error(function(){
        });
    }
}]);



