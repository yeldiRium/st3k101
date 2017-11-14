angular.module('Dashboard', ['ngRoute'])
    .controller('DashboardController', ['$scope',
        function($scope) {
            
        }])
    .config(['$routeProvider', '$locationProvider',
        function($routeProvider, $locationProvider) {
            $locationProvider.hashPrefix('');
            $routeProvider
                .when('/', {
                    redirectTo: '/dashboard',
                    templateUrl: '/static/js/templates/Dashboard.html',
                    controller: 'DashboardController'
                })
                .when('/dashboard', {
                    templateUrl: '/static/js/templates/Dashboard.html',
                    controller: 'DashboardController'
                });
        }]);