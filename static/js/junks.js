$scope.getDataFiles = function() {
      // get the JSON file 
      $scope.filelist = null
      $log.log("in run of getting files")

      // fire the API request
      $http.post('/api/getFiles').
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
 class="logscroll"