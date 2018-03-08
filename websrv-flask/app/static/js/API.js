angular.module("API", [])
    .factory("Account", [function() {
        return {
            current: function() {
                return Fluture.tryP(() => $.ajax({
                    "accepts": "application/json",
                    "method": "GET",
                    "url": "/api/account/current"
                }));
            },
            update: function() {
                var {email = null, locale = null} = arguments;
                return Fluture.tryP(() => $.ajax({
                    "accepts": "application/json",
                    "method": "PUT",
                    "url": "/api/account/current",
                    "content-type": "application/json",
                    "data": JSON.stringify({
                        email: email,
                        locale: locale
                    })
                }));
            }
        };
    }])
    .directive("ewLoad", function() {
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