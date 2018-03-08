angular.module('Account', ['ngRoute', 'API', 'Utility'])
    .config(['FlashProvider', function (FlashProvider) {
        FlashProvider.setTimeout(5000);
        FlashProvider.setShowClose(true);
    }])
    .controller('AccountController', ['$scope', '$http', 'Flash', 'Account', 'Locales', "ResultHandling",
        function ($scope, $http, Flash, Account, Locales, ResultHandling) {
            $scope.loading = "loading";

            Fluture.both(Account.current(), Locales.all())
                .chainRej(errors => {
                    errors.map(ResultHandling.flashError($scope))
                })
                .fork(
                    error => {
                        scope.$apply(() => scope.loading = "error");
                    },
                    data => {
                        var [account, locales] = data;
                        $scope.$apply(() => {
                            $scope.account = {
                                uuid: account.uuid,
                                email: account.fields.email,
                                locale: account.fields.locale_name
                            };
                            $scope.locales = locales;
                            $scope.loading = "done";
                        });
                    }
                );

            $scope.updateAccount = function (email, locale) {
                Flash.create("info", "Updating; Please wait a moment...");
                Account.update({
                        email,
                        locale
                    })
                    .fork(
                        ResultHandling.flashError($scope),
                        ResultHandling.flashSuccess($scope)
                    );
            };

            $scope.updateEmail = function () {
                $scope.updateAccount($scope.account.email, null);
            };

            $scope.updateLocale = function () {
                $scope.updateAccount(null, $scope.account.locale);
            };
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