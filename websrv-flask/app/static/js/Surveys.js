angular.module('Surveys', ['ngRoute'])
    .controller('SurveysController', ['$scope',
        function($scope) {

        }])
    .config(['$routeProvider', '$locationProvider',
        function($routeProvider, $locationProvider) {
            $locationProvider.hashPrefix('');
            $routeProvider
                .when('/be/surveys/', {

                })
                .when('/be/surveys/:surveyID/', {
                    
                });
        }]);