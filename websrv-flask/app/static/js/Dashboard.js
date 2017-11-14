angular.module('Dashboard', ['ngRoute'])
    .controller('DashboardController', ['$scope',
        function($scope) {

        }])
    .config(['$routeProvider', '$locationProvider',
        function($routeProvider, $locationProvider) {
            $locationProvider.hashPrefix('');
            $routeProvider
                .when('/be', {
                    redirectTo: '/be/dashboard'
                })
                .when('/be/dashboard', {

                });
        }]);