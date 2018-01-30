angular.module('Account', ['ngRoute'])
    .config(['FlashProvider', function (FlashProvider) {
        FlashProvider.setTimeout(5000);
        FlashProvider.setShowClose(true);
    }])
    .factory('Account', ['$http', function ($http) {
        return {
            query: function () {
                return $http.get('/api/account/current').then(
                    function (result) {
                        return new Promise(function (resolve, reject) {
                            resolve(result.data);
                        });
                    },
                    function (error) {
                        return new Promise(function (resolve, reject) {
                            reject(error);
                        });
                    }
                );
            }
        }
    }])
    .controller('AccountController', ['$scope', 'Flash', 'Account', 'Locales',
        function ($scope, Flash, Account, Locales) {
            $scope.getLocales = function() {
                return Locales.query().then(
                    function success(result) {
                        $scope.locales = result
                    }, function fail(error) {
                        Flash.create('danger', error.data.result);
                    }
                )
            };

            $scope.query = function () {
                return Account.query().then(
                    function success(result) {
                        $scope.account = {
                            uuid: result.uuid,
                            email: result.fields.email,
                            locale: result.fields.locale_name
                        }
                    }, function fail(error) {
                        Flash.create('danger', error.data.result);
                    }
                )
            };

            $scope.getLocales();
            $scope.query();
        }])
    .config(['$routeProvider', '$locationProvider',
        function ($routeProvider, $locationProvider) {
            $locationProvider.hashPrefix('');
            $routeProvider
                .when('/account', {
                    templateUrl: '/static/js/templates/Account.html',
                    controller: 'AccountController'
                });
        }]);