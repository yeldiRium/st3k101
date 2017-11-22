angular.module('Surveys', ['ngRoute'])
    .factory('Surveys', ['$http', function($http) {
        return {
            query: function() {
                return $http.get('/api/surveys').then(
                    function(result) {
                        return new Promise(function(resolve, reject) {
                            resolve(result.data);
                        });
                    },
                    function(error) {
                        return new Promise(function(resolve, reject) {
                            reject(error);
                        });
                    }
                );
            }
        }
    }])
    .controller('SurveysController', ['$scope', 'Surveys',
        function($scope, Surveys) {
            /**
             * Queries surveys and writes them into $scope.surveys.
             * If something goes wrong, $scope.error will be set.
             * @returns Promise
             */
            $scope.query = function() {
                return Surveys.query().then(
                    function(result) {
                        $scope.surveys = null;
                        $scope.error = null;
                        $scope.surveys = result;
                    },
                    function(error) {
                        $scope.surveys = null;
                        $scope.error = null;
                        $scope.error = error;
                    }
                );
            };
            
            $scope.query();
        }])
    .controller('EditSurveyController', ['$scope',
        function($scope) {

        }])
    .config(['$routeProvider', '$locationProvider',
        function($routeProvider, $locationProvider) {
            $locationProvider.hashPrefix('');
            $routeProvider
                .when('/surveys/', {
                    templateUrl: '/static/js/templates/Surveys.html',
                    controller: 'SurveysController'
                })
                .when('/surveys/:surveyID/', {
                    templateUrl: '/static/js/templates/EditSurvey.html',
                    controller: 'EditSurveyController'
                });
        }]);