angular.module("API", [])
    .factory("ResultHandling", ["Flash", function (Flash) {
        return {
            // Flashes the resulting error message.
            "flashError": function (scope) {
                return function (error) {
                    scope.$apply(() => {
                        Flash.create("danger", error.responseJSON.error);
                    });
                    return Fluture.of(error);
                }
            },
            // Flashes the resulting success message.
            "flashSuccess": function (scope) {
                return function (data) {
                    scope.$apply(() => {
                        Flash.create("success", data.result);
                    });
                    return Fluture.of(data);
                }
            }
        }
    }])
    .factory("Account", [function () {
        return {
            "current": function () {
                return Fluture.tryP(() => $.ajax({
                    "accepts": "application/json",
                    "method": "GET",
                    "url": "/api/account/current"
                }));
            },
            "update": function (data) {
                var {email = null, locale = null} = data;
                return Fluture.tryP(() => $.ajax({
                    "accepts": "application/json",
                    "method": "PUT",
                    "url": "/api/account/current",
                    "content-type": "application/json",
                    "data": JSON.stringify({
                        "email": email,
                        "locale": locale
                    })
                }));
            }
        };
    }])
    .factory("Locales", [function () {
        return {
            "all": function () {
                return Fluture.tryP(() => $.ajax({
                    "accepts": "application/json",
                    "methods": "GET",
                    "url": "/api/locales"
                }));
            }
        }
    }])
    .directive("ewLoad", function () {
        return {
            "restrict": "EA",
            "replace": true,
            "transclude": true,
            "scope": {
                "loading": "=loading"
            },
            "templateUrl": "/static/js/templates/loading.html",
            "link": function (scope) {
                scope.$watch("loading", new_value => {
                    scope.loading = new_value;
                });
            }
        }
    });