angular.module('Surveys', ['ngRoute'])
    .factory('Surveys', ['$http', function($http) {
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
        )
    }])
    .controller('SurveysController', ['$scope', 'Surveys',
        function($scope, Surveys) {
            Surveys.then(
                function(result) {
                    $scope.surveys = result;
                },
                function(error) {
                    $scope.error = error;
                }
            );
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