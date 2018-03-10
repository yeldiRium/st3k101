const angular = require("angular");
const Future = require("fluture");
const R = require("ramda");

require("angular-flash-alert");

angular.module("API", [])
    .factory("ResultHandling", ["Flash", function (Flash) {
        return {
            // Flashes the resulting error message.
            "flashError": function (scope) {
                return function (error) {
                    scope.$apply(() => {
                        Flash.create("danger", error.data.error);
                    });
                    return Future.of(error);
                }
            },
            // Flashes the resulting success message.
            "flashSuccess": function (scope) {
                return function (data) {
                    scope.$apply(() => {
                        Flash.create("success", data.result);
                    });
                    return Future.of(data);
                }
            },
            "extractDataAndLocale": function (result) {
                return Future.of({
                    "data": result.data,
                    "locale": result.headers("Content-Language")
                });
            },
            "extractData": function (result) {
                return Future.of(result.data);
            }
        }
    }])
    .factory("LanguageHandling", [function () {
        const getStringLocale = R.curry(function (locale, i15dString) {
            const defaultLocale = R.path(
                ["fields", "default_locale"], i15dString
            );
            return R.pathOr(
                R.path(["fields", "locales", defaultLocale]),
                ["fields", "locales", locale],
                i15dString
            )
        });

        const getSurveyTranslation = R.curry(
            function (locale, survey) {
                const name = R.path(["fields", "name"], survey);
                const questionnaires = R.path(
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
                )(survey);
            }
        );

        const getQuestionnaireTranslation = R.curry(
            function (locale, questionnaire) {
                const getString = getStringLocale(locale);

                const name = R.path(["fields", "name"], questionnaire);
                const description = R.path(
                    ["fields", "description"], questionnaire
                );
                const questionGroups = R.path(
                    ["fields", "questiongroups"], questionnaire
                );
                return R.pipe(
                    R.assocPath(
                        ["fields", "name"],
                        getString(name)
                    ),
                    R.assocPath(
                        ["fields", "description"],
                        getString(description)
                    ),
                    R.assocPath(
                        ["fields", "questiongroups"],
                        R.map(
                            getQuestionGroupTranslation(locale), questionGroups
                        )
                    )
                )(questionnaire);
            }
        );

        const getQuestionGroupTranslation = R.curry(
            function (locale, questionGroup) {
                const name = R.path(["fields", "name"], questionGroup);
                const questions = R.path(
                    ["fields", "questions"], questionGroup
                );
                return R.pipe(
                    R.assocPath(
                        ["fields", "name"],
                        getStringLocale(locale, name)
                    ),
                    R.assocPath(
                        ["fields", "questions"],
                        R.map(
                            getQuestionTranslation(locale), questions
                        )
                    )
                )(questionGroup);
            }
        );

        const getQuestionTranslation = R.curry(
            function (locale, question) {
                // TODO: implement
                return question;
            }
        );

        return {
            "getStringLocale": getStringLocale,
            "getSurveyTranslation": getSurveyTranslation,
            "getQuestionnaireTranslation": getQuestionnaireTranslation,
            "getQuestionGroupTranslation": getQuestionGroupTranslation,
            "getQuestionTranslation": getQuestionTranslation
        }
    }])
    .factory("PathHandling", [function () {
        return {
            "pathMaybeWithLocale": function (path, locale = "") {
                return path + (
                    (locale === "")
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
                    return Future.tryP(() => {
                        return $http.get("/api/account/current");
                    })
                        .chain(ResultHandling.extractData);
                },
                "update": function (data) {
                    const {email = null, locale = null} = data;
                    return Future.tryP(() => $http({
                        "method": "PUT",
                        "url": "/api/account/current",
                        "data": {
                            email,
                            locale
                        },
                        "headers": {
                            "Content-Type": "application/json"
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
                    return Future.tryP(() => {
                        return $http.get("/api/locales");
                    })
                        .chain(ResultHandling.extractData);
                }
            }
        }])
    .factory("Surveys", ["$http", "PathHandling", "ResultHandling",
        function ($http, PathHandling, ResultHandling) {
            return {
                "all": function (locale = "") {
                    let path = PathHandling.pathMaybeWithLocale(
                        "/api/survey", locale
                    );
                    return Future.tryP(() => {
                        return $http.get(path);
                    })
                        .chain(ResultHandling.extractDataAndLocale);
                },
                "create": function (name) {
                    return Future.tryP(() => $http({
                        "method": "POST",
                        "url": "/api/survey",
                        "data": {
                            "name": name
                        },
                        "headers": {
                            "Content-Type": "application/json"
                        }
                    }))
                        .chain(ResultHandling.extractData);
                },
                "delete": function (uuid) {
                    return Future.tryP(() => $http({
                        "method": "DELETE",
                        "url": `/api/survey/${uuid}`
                    }))
                        .chain(ResultHandling.extractData)
                }
            }
        }])
    .factory("Questionnaires", ["$http", "PathHandling", "ResultHandling",
        function ($http, PathHandling, ResultHandling) {
            return {
                "create": function (data) {
                    const {survey_uuid, name, description, template = null} =
                        data;
                    return Future.tryP(() => $http({
                        "method": "POST",
                        "url": "/api/questionnaire",
                        "data": {
                            "survey_uuid": survey_uuid,
                            "questionnaire": {
                                "name": name,
                                "description": description,
                                "template": template
                            }
                        },
                        "headers": {
                            "Content-Type": "application/json"
                        }
                    }))
                        .chain(ResultHandling.extractData)
                },
                "get": function (questionnaire_uuid, locale = "") {
                    const path = PathHandling.pathMaybeWithLocale(
                        `/api/questionnaire/${questionnaire_uuid}`, locale
                    );
                    return Future.tryP(() => {
                        return $http.get(path);
                    })
                        .chain(ResultHandling.extractDataAndLocale);
                },
                "update": function (questionnaire_uuid, data) {
                    const {name=null, description=null} = data;
                    return Future.tryP(() => $http({
                        "method": "PUT",
                        "url": `/api/questionnaire/${questionnaire_uuid}`,
                        "data": {
                            "name": name,
                            "description": description
                        },
                        "headers": {
                            "Content-Type": "application/json"
                        }
                    }))
                        .chain(ResultHandling.extractData);
                },
                "delete": function (questionnaire_uuid, survey_uuid) {
                    return Future.tryP(() => $http({
                        "method": "DELETE",
                        "url": `/api/questionnaire/${questionnaire_uuid}`,
                        "data": {
                            "survey_uuid": survey_uuid
                        },
                        "headers": {
                            "Content-Type": "application/json"
                        }
                    }))
                        .chain(ResultHandling.extractData)
                }
            }
        }])
    .factory("QuestionStatistic", ["$http", function ($http) {
        return {
            query: function (uuid) {
                return $http.get(`/api/question/${uuid}/statistic`).then(
                    function success(result) {
                        return new Promise(function (resolve, reject) {
                            let statistic = {
                                "biggest": R.path(["data", "fields", "biggest"], result),
                                "smallest": R.path(["data", "fields", "smallest"], result),
                                "q1": R.path(["data", "fields", "q1"], result),
                                "q2": R.path(["data", "fields", "q2"], result),
                                "q3": R.path(["data", "fields", "q3"], result)
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