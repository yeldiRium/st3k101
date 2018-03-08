angular.module('Account', ['ngRoute', 'API', 'Utility'])
    .config(['FlashProvider', function (FlashProvider) {
        FlashProvider.setTimeout(5000);
        FlashProvider.setShowClose(true);
    }])
    .controller('AccountController', ['$scope', '$http', 'Flash', 'Account', 'Locales',
        function ($scope, $http, Flash, Account, Locales) {
            $scope.loading = "init";

            $scope.$watch("loading", new_value => {
                console.log(new_value);
                $scope.loading = new_value;
            });

            Account.current().fork(data => {
                $scope.loading = "error";
                console.error(data)
            }, data => {
                $scope.loading = "done";
                console.log(data)
            });

            $scope.loading = "loading";

            Account.update({"email": "blub@blub.blub"}).fork(console.error, console.log);

/*
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
            */
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