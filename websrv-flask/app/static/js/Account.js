angular.module('Account', ['ngRoute'])
    .controller('AccountController', ['$scope',
        function($scope) {

        }])
    .config(['$routeProvider', '$locationProvider',
        function($routeProvider, $locationProvider) {
            $locationProvider.hashPrefix('');
            $routeProvider
                .when('/be/account', {

                });
        }]);