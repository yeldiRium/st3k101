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
            },
            "extractDataAndLocale": function (result) {
                return Fluture.of({
                    "data": result.data,
                    "locale": result.headers("Content-Language")
                });
            },
            "extractData": function (result) {
                return Fluture.of(result.data);
            }
        }
    }])
    .factory("LanguageHandling", [function () {
        var getStringLocale = R.curry(function (locale, i15dString) {
            var defaultLocale = R.path(
                ["fields", "default_locale"], i15dString
            );
            return R.pathOr(
                R.path(["fields", "locales", defaultLocale]),
                ["fields", "locales", locale],
                i15dString
            )
        });

        var getSurveyTranslation = R.curry(function (locale, survey) {
            var name = R.path(["fields", "name"], survey);
            var questionnaires = R.path(
                ["fields", "questionnaires"], survey
            );
            return R.pipe(
                R.assocPath(
                    ["fields", "name"],
                    getStringLocale(locale, name)
                ),
                R.assocPath(
                    ["fields", "questionnaires"],
                    R.map(
                        getQuestionnaireTranslation(locale), questionnaires
                    )
                )
            )(survey)
        });

        var getQuestionnaireTranslation = R.curry(
            function (locale, questionnaire) {
                // TODO: implement
                return questionnaire;
            }
        );

        return {
            "getStringLocale": getStringLocale,
            "getSurveyTranslation": getSurveyTranslation,
            "getQuestionnaireTranslation": getQuestionnaireTranslation
        }
    }])
    .factory("PathHandling", [function () {
        return {
            "pathMaybeWithLocale": function (path, locale = "") {
                return path + (
                        (locale == "")
                            ? ""
                            : "?locale_cookie=0&locale=" + locale
                    );
            }
        }
    }])
    .factory("Account", ["$http", "ResultHandling",
        function ($http, ResultHandling) {
            return {
                "current": function () {
                    return Fluture.tryP(() => $http.get("/api/account/current"))
                        .chain(ResultHandling.extractData);
                },
                "update": function (data) {
                    var {email = null, locale = null} = data;
                    return Fluture.tryP(() => $http({
                            "method": "PUT",
                            "url": "/api/account/current",
                            "data": {
                                "email": email,
                                "locale": locale
                            },
                            "headers": {
                                'Content-Type': 'application/json'
                            }
                        }))
                        .chain(ResultHandling.extractData);
                }
            };
        }
    ])
    .factory("Locales", ["$http", "ResultHandling",
        function ($http, ResultHandling) {
            return {
                "all": function () {
                    return Fluture.tryP(() => $http.get("/api/locales"))
                        .chain(ResultHandling.extractData);
                }
            }
        }])
    .factory("Surveys", ["$http", "PathHandling", "ResultHandling",
        function ($http, PathHandling, ResultHandling) {
            return {
                "all": function (locale = "") {
                    var path = PathHandling.pathMaybeWithLocale(
                        "/api/survey", locale
                    );
                    return Fluture.tryP(() => $http.get(path))
                        .chain(ResultHandling.extractDataAndLocale);
                },
                "query": function (locale = "") {
                    var path = PathHandling.pathMaybeWithLocale(
                        "/api/survey", locale
                    );
                    return $http.get(path).then(
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
    .factory('Questionnaire', ['$http', function ($http) {
        return {
            query: function (uuid, locale = "") {
                var path = "/api/questionnaire/" + uuid;
                path += (locale == "") ? "" : "?locale_cookie=0&locale=" + locale;
                return $http.get(path).then(
                    function success(result) {
                        return new Promise(function (resolve, reject) {
                            resolve({
                                result: result.data,
                                locale: result.headers("Content-Language")
                            });
                        })
                    },
                    function fail(error) {
                        return new Promise(function (resolve, reject) {
                            reject(error);
                        });
                    }
                )
            }
        }
    }])
    .factory('QuestionStatistic', ['$http', function ($http) {
        return {
            query: function (uuid) {
                return $http.get('/api/question/' + uuid + '/statistic').then(
                    function success(result) {
                        return new Promise(function (resolve, reject) {
                            var statistic = {
                                'biggest': result.data.fields.biggest,
                                'smallest': result.data.fields.smallest,
                                'q1': result.data.fields.q1,
                                'q2': result.data.fields.q2,
                                'q3': result.data.fields.q3
                            };
                            resolve(statistic);
                        })
                    },
                    function fail(error) {
                        return new Promise(function (resolve, reject) {
                            reject(error);
                        });
                    }
                )
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