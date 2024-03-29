'use strict';

//var inertialFlowControllers = angular.module('inertialFlowControllers', []);
var flowControllers = angular.module('flowControllers',[])

////////////////////////////////
//// Main Controller  ////
////////////////////////////////


////////////////////////////////
//// Controller for showing a particular project////
////////////////////////////////
flowControllers.controller('MyProjectController', ['$scope', '$location', '$http', '$log', 'AuthService',
 function($scope, $location, $http, $log, $timeout, $AuthService) {

  $scope.projectName = '';
  $scope.editProjectDescription = true;
  $scope.getCurrentProject = function(){
    $scope.editProjectDescription = true;
    $http.get('/api/currentProject').success(function(prj_name) {
      $log.log("Project name = " + prj_name);
      if(prj_name!="None"){
        $scope.projectName = prj_name;
      }
    }).error(function(error) {
      $log.log("there is an error getting the current project name :(");
      $log.log(error);
    });
  };

  $scope.editName = function(){
    if($scope.editProjectDescription){
      $scope.editProjectDescription = false;
    }else{
      $scope.editProjectDescription = true;
    }
    $log.log("disabled = " + $scope.editProjectDescription);
  };
  $scope.getJSONFiles = function() {
      $scope.json_files = null;
      $scope.checked_json_files = [];
      $log.log("in run of getting files");
      $http.get('/api/getJSONFiles').
        success(function(results) {
          $log.log(results);
          $scope.json_files = results;
        }).
        error(function(error) {
          $log.log("there is an error :(");
          $log.log(error);
        });
  };

}]);

////////////////////////////////
//// Controller for showing a user's projects ////
////////////////////////////////
flowControllers.controller('ProjectsController',['$scope', '$location', '$http','$log', function($scope, $location, $http,$log) {

  $scope.createNewProject = function() {
    $log.log("Creating a new project!");
    var project_name = $scope.newProject.project_name;
    $http.post('/api/createNewProject', {"project_name":project_name}).success(function(results) {
      $log.log("Success!");
      $log.log(results);
      $location.path('/project');
    }).error(function(error) {
      $log.log("there is an error creating the project! :(")
       $log.log(error);
    });
  };

  $scope.getUserProjects = function(){
    $log.log("Getting a list of all user projects");
    $scope.project_names = null;
    $scope.project_descriptions = null;
    $http.get('/api/getListOfUserProjects').success(function(prj_names) {
      $log.log(prj_names);
      $scope.project_names = prj_names ;
    }).error(function(error) {
      $log.log("there is an error getting a list of the projects :(");
      $log.log(error);
    });
  }

  $scope.DeleteProject = function(project_to_delete){
    $log.log("Removing Project " + project_to_delete);
    $http.post('/api/deleteProject', {"project_to_delete":project_to_delete}).success(function(results) {
      $log.log("Success!");
      $log.log(results);
      //$location.path('/projects');
      $scope.getUserProjects();
    }).error(function(error) {
      $log.log("there is an error deleting the project! :(")
       $log.log(error);
    });
  }
 
  $scope.ViewProject = function(project_to_view){
    $http.post('/api/setCurrentProject', {"project_name":project_to_view}).success(function(results) {
      $log.log("Success!");
      $log.log(results);
      $location.path('/project');
      $scope.getUserProjects();
    }).error(function(error) {
      $log.log("there is an error viewing the project! :(")
       $log.log(error);
    });
  }

}]);
////////////////////////////////
//// Controller for creating an account in ////
////////////////////////////////

flowControllers.controller('registerController',
  ['$scope', '$location', 'AuthService',
  function ($scope, $location, AuthService) {

    $scope.register = function () {

      // initial values
      $scope.error = false;
      $scope.disabled = true;

      // call register from service
      AuthService.register($scope.registerForm.email,
                           $scope.registerForm.password)
        // handle success
        .then(function () {
          $location.path('/login');
          $scope.disabled = false;
          $scope.registerForm = {};
        })
        // handle error
        .catch(function () {
          $scope.error = true;
          $scope.errorMessage = "Something went wrong!";
          $scope.disabled = false;
          $scope.registerForm = {};
        });

    };

}]);

////////////////////////////////
//// Controller for logging out ////
////////////////////////////////

flowControllers.controller('logoutController',
  ['$scope', '$location', 'AuthService',
  function ($scope, $location, AuthService) {

    $scope.logout = function () {

      // call logout from service
      AuthService.logout()
        .then(function () {
          $location.path('/login');
        });

    };

}]);

////////////////////////////////
//// Controller for logging in ////
////////////////////////////////

flowControllers.controller('loginController',
  ['$scope', '$location', 'AuthService',
  function ($scope, $location, AuthService) {

    $scope.login = function () {

      // initial values
      $scope.error = false;
      $scope.disabled = true;

      // call login from service
      AuthService.login($scope.loginForm.email, $scope.loginForm.password)
        // handle success
        .then(function () {
          $location.path('/');
          $scope.disabled = false;
          $scope.loginForm = {};
        })
        // handle error
        .catch(function () {
          $scope.error = true;
          $scope.errorMessage = "Invalid username and/or password";
          $scope.disabled = false;
          $scope.loginForm = {};
        });

    };

}]);

////////////////////////////////
//// Controller for upload data ////
////////////////////////////////


flowControllers.controller('UploadDataController', ['$scope', '$location','$log','$http','fileUpload', function($scope, $location, $log, $http, fileUpload) {
  // Function to upload a data file


  $scope.uploadDataFile = function() {
    var file = $scope.myFile;
    $scope.fileError = false;
    var fd = new FormData();
    fd.append('file',file);

    $http({method: 'POST', url: '/api/uploaddata',
                         data: fd,
                         headers: {'Content-Type': undefined},
                         transformRequest: angular.identity}).
        success(function(results) {
          if(results=="-1"){
            $scope.fileError = true;
            $log.log("not good");
          }else{
            $scope.getDataFiles();
          }
        }).
        error(function(error) {
          $log.log("there is an error :(");
          $log.log(error);
          $scope.urlerror = true;
        });



  };
  $scope.getDataFiles = function() {
      // get the JSON file 
      $scope.filelist = null;
      $log.log("in run of getting files");

      // fire the API request
      $http.post('/api/getDataFiles').
        success(function(results) {
          $log.log(results);
          $scope.filelist = results;
          //getNetworkResults(results); 
        }).
        error(function(error) {
          $log.log("there is an error :(");
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
            $log.log("not good");
          }else{
            $scope.getJSONFiles();
          }
        }).
        error(function(error) {
          $log.log("there is an error :(");
          $log.log(error);
          $scope.urlerror = true;
        });



  };
  $scope.getJSONFiles = function() {
      // get the JSON file 
      $scope.filelist = null;
      $log.log("in run of getting files");

      // fire the API request
      $http.post('/api/getJSONFiles').
        success(function(results) {
          $log.log(results);
          $scope.filelist = results;
          //getNetworkResults(results); 
        }).
        error(function(error) {
          $log.log("there is an error :(");
          $log.log(error);
        });

  };





}]);


////////////////////////////////
//// Controller for running a network ////
////////////////////////////////

flowControllers.controller('RunNetworkController', ['$scope', '$location', '$http', '$log', '$timeout', 'AuthService',
 function($scope, $location, $http, $log, $timeout, $AuthService) {

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
      $scope.json_files = null;
      $scope.checked_json_files = [];
      //$scope.user.json_files = null
      $log.log("in run of getting files");

      // fire the API request
      $http.get('/api/getJSONFiles').
        success(function(results) {
          $log.log(results);
          //$scope.json_files = []
          //for(var i = 0, size = results.length; i < size ; i++){
          //  $scope.json_files.push({file_name:results[i],checked:false})
          //}

          $scope.json_files = results;
          //getNetworkResults(results); 
        }).
        error(function(error) {
          $log.log("there is an error :(");
          $log.log(error);
        });

  };




  // Function to run the network
  $scope.runNetwork = function() {
      // get the JSON file 
      //$log.log($scope.user.json_files)
      $log.log($scope.checked_json_files);
      //var userInput = $scope.file;
      //$log.log("in run of RunNetworkController")
      //$log.log(userInput)
      // fire the API request
      for(var i=0; i < $scope.checked_json_files.length; i++){
        $log.log("running network:");
        $log.log($scope.checked_json_files[i]);
        var file_to_run = "JSON/"+$scope.checked_json_files[i];
        $http.post('/api/runnetwork', {"file":file_to_run}).
        success(function(results) {
          $log.log(results);
          getNetworkResults(results);
          $scope.runresults = null;
          $scope.loading = true;
          $scope.submitButtonText = 'Running...';
        }).
        error(function(error) {
          $log.log("there is an error :(");
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
              $scope.submitButtonText = "Submit";
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



