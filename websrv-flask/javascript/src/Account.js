const angular = require("angular");
const Future = require("fluture");
const R = require("ramda");

require("angular-route");
require("angular-flash-alert");
require("./API");
require("./Utility");

angular.module("Account", ["ngRoute", "API", "Utility"])
    .config(["FlashProvider", function (FlashProvider) {
        FlashProvider.setTimeout(5000);
        FlashProvider.setShowClose(true);
    }])
    .controller("AccountController", [
        "$scope", "$http", "Flash", "Account", "Locales", "ResultHandling",
        function ($scope, $http, Flash, Account, Locales, ResultHandling) {
            $scope.loading = "loading";

            Future.both(Account.current(), Locales.all())
                .mapRej(
                    ResultHandling.flashError($scope)
                )
                .fork(
                    () => {
                        $scope.$apply(() => $scope.loading = "error");
                    },
                    storeData
                );

            /**
             * Splits the incoming data and stores them for display.
             *
             * @param account
             * @param locales
             */
            function storeData([account, locales]) {
                $scope.$apply(() => {
                    $scope.account = {
                        uuid: account.uuid,
                        email: R.path(["fields", "email"], account),
                        locale: R.path(["fields", "locale_name"], account)
                    };
                    $scope.locales = locales;
                    $scope.loading = "done";
                });
            }

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
    .config(["$routeProvider", "$locationProvider",
        function ($routeProvider, $locationProvider) {
            $locationProvider.hashPrefix("");
            $routeProvider
                .when("/account", {
                    template: require("./templates/Account.html"),
                    controller: "AccountController"
                });
        }]);