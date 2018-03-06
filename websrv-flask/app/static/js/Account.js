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
    .controller('AccountController', ['$scope', '$http', 'Flash', 'Account', 'Locales',
        function ($scope, $http, Flash, Account, Locales) {
            $scope.getLocales = function() {
                return Locales.query().then(
                    function success(result) {
                        $scope.locales = result;
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
                        };
                    }, function fail(error) {
                        Flash.create('danger', error.data.result);
                    }
                )
            };

            $scope.updateEmail = function() {
                $http({
                    method: 'PUT',
                    url: '/api/account/' + $scope.account.uuid,
                    data: JSON.stringify({
                        email: $scope.account.email
                    }),
                    headers: {
                        'Content-Type': 'application/json'
                    }
                }).then(
                    function success(result) {
                        Flash.create('success', 'Email updated.');
                    }, function fail(result) {
                        Flash.create('danger', result.data.error);
                    }
                );
            };

            $scope.updateLocale = function() {
                $http({
                    method: 'PUT',
                    url: '/api/account/' + $scope.account.uuid,
                    data: JSON.stringify({
                        locale: $scope.account.locale
                    }),
                    headers: {
                        'Content-Type': 'application/json'
                    }
                }).then(
                    function success(result) {
                        Flash.create('success', 'Language updated.');
                    }, function fail(result) {
                        Flash.create('danger', result.data.error);
                    }
                );
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