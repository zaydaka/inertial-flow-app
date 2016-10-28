'use strict';

//var inertialFlowControllers = angular.module('inertialFlowControllers', []);


////////////////////////////////
//// Controller for upload data ////
////////////////////////////////
var flowControllers = angular.module('flowControllers',[])

flowControllers.controller('UploadDataController', ['$scope', '$location','$log','$http','fileUpload', function($scope, $location, $log, $http, fileUpload) {
  // Function to upload a data file


  $scope.uploadDataFile = function() {
    var file = $scope.myFile;
    $scope.fileError = false;
    var fd = new FormData();
    fd.append('file',file);

    $http({method: 'POST', url: '/uploaddata',
                         data: fd,
                         headers: {'Content-Type': undefined},
                         transformRequest: angular.identity}).
        success(function(results) {
          if(results=="-1"){
            $scope.fileError = true;
            $log.log("not good")
          }else{
            $scope.getDataFiles();
          }
        }).
        error(function(error) {
          $log.log("there is an error :(")
          $log.log(error);
          $scope.urlerror = true;
        });



  };
  $scope.getDataFiles = function() {
      // get the JSON file 
      $scope.filelist = null
      $log.log("in run of getting files")

      // fire the API request
      $http.post('/api/getDataFiles').
        success(function(results) {
          $log.log(results);
          $scope.filelist = results
          //getNetworkResults(results); 
        }).
        error(function(error) {
          $log.log("there is an error :(")
          $log.log(error);
        });

  };
 




}]);


///////////////////////////////
//// Controller for uploading json files ////
///////////////////////////////

flowControllers.controller('UploadJsonController', ['$scope', '$location', '$http','$log', function($scope, $location, $http,$log) {

  $scope.uploadJSONFile = function() {
    var file = $scope.myFile;
    $scope.fileError = false;
    var fd = new FormData();
    fd.append('file',file);

    $http({method: 'POST', url: '/uploadjson',
                         data: fd,
                         headers: {'Content-Type': undefined},
                         transformRequest: angular.identity}).
        success(function(results) {
          if(results=="-1"){
            $scope.fileError = true;
            $log.log("not good")
          }else{
            $scope.getJSONFiles();
          }
        }).
        error(function(error) {
          $log.log("there is an error :(")
          $log.log(error);
          $scope.urlerror = true;
        });



  };
  $scope.getJSONFiles = function() {
      // get the JSON file 
      $scope.filelist = null
      $log.log("in run of getting files")

      // fire the API request
      $http.post('/api/getJSONFiles').
        success(function(results) {
          $log.log(results);
          $scope.filelist = results
          //getNetworkResults(results); 
        }).
        error(function(error) {
          $log.log("there is an error :(")
          $log.log(error);
        });

  };





}]);


////////////////////////////////
//// Controller for running a network ////
////////////////////////////////

flowControllers.controller('RunNetworkController', ['$scope', '$location', '$http', '$log', '$timeout',
 function($scope, $location, $http, $log, $timeout) {

  $scope.submitButtonText = 'Submit';
  $scope.loading = false;
  $scope.urlerror = false;

  // helper method to get selected fruits
  $scope.selectedFruits = function selectedJSONFiles() {
    return filterFilter($scope.json_files, { checked: true });
  };



  $scope.getJSONFiles = function() {
      // get the JSON file 
      //$scope.checked_json_files = null
      $scope.json_files = null
      $scope.checked_json_files = []
      //$scope.user.json_files = null
      $log.log("in run of getting files")

      // fire the API request
      $http.post('/api/getJSONFiles').
        success(function(results) {
          $log.log(results);
          //$scope.json_files = []
          //for(var i = 0, size = results.length; i < size ; i++){
          //  $scope.json_files.push({file_name:results[i],checked:false})
          //}

          $scope.json_files = results
          //getNetworkResults(results); 
        }).
        error(function(error) {
          $log.log("there is an error :(")
          $log.log(error);
        });

  };




  // Function to run the network
  $scope.runNetwork = function() {
      // get the JSON file 
      //$log.log($scope.user.json_files)
      $log.log($scope.checked_json_files)
      //var userInput = $scope.file;
      //$log.log("in run of RunNetworkController")
      //$log.log(userInput)
      // fire the API request
      for(var i=0; i < $scope.checked_json_files; i++){
        $log.log("running network:")
        $log.log($scope.checked_json_files[i])
        $http.post('/api/runnetwork', {"file": $scope.checked_json_files[i]}).
        success(function(results) {
          $log.log(results);
          getNetworkResults(results);
          $scope.runresults = null;
          $scope.loading = true;
          $scope.submitButtonText = 'Running...';
        }).
        error(function(error) {
          $log.log("there is an error :(")
          $log.log(error);
        });
      }
      

  };






function getNetworkResults(jobID) {

      var timeout = "";


      var poller = function() {
        // fire another request
        $http.get('/results/'+jobID).
          success(function(data, status, headers, config) {
            if(status === 202) {
              $log.log(status);
              $scope.runresults = data;
            } else if (status === 200){
              $log.log("finished!!")
              $log.log(data);
              $scope.loading = false;
              $scope.submitButtonText = "Submit"
              $scope.runresults = data;
              $scope.urlerror = false;
              $timeout.cancel(timeout);
              return false;
            }
            // continue to call the poller() function every 2 seconds
            // until the timeout is cancelled
            timeout = $timeout(poller, 1000);
          }).
          error(function(error) {
            $log.log(error);
            $scope.loading = false;
            $scope.submitButtonText = "Submit";
            $scope.urlerror = true;
        });

      };
      poller();
    }


// END
}]);



