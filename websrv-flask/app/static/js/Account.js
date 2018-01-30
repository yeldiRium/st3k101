angular.module('Account', ['ngRoute'])
    .controller('AccountController', ['$scope',
        function($scope) {

        }])
    .factory('Account', ['$http', function($http) {
        return {
            query: function() {
                return $http.get('/api/account').then(
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
    .config(['$routeProvider', '$locationProvider',
        function($routeProvider, $locationProvider) {
            $locationProvider.hashPrefix('');
            $routeProvider
                .when('/account', {
                    templateUrl: '/static/js/templates/Account.html',
                    controller: 'AccountController'
                });
        }]);