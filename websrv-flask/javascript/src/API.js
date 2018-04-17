import ResultHandling from "./API/Utility/ResultHandling";
import Future from "fluture";
import * as R from "ramda";

import Api from "./API/";

const angular = require("angular");
require("angular-flash-alert");

angular.module("API", [])
    .factory("ResultHandling", ["Flash", function (Flash) {
        return {
            // Flashes the resulting error message.
            "flashError": function (scope) {
                return function (error) {
                    scope.$apply(() => {
                        Flash.create("danger", error.error);
                    });
                    return error;
                }
            },
            // Flashes the resulting success message.
            "flashSuccess": function (scope) {
                return function (data) {
                    scope.$apply(() => {
                        Flash.create("success", data.result);
                    });
                    return data;
                }
            },
            "extractDataAndLocale": function (result) {
                return Api.ResultHandling.extractDataAndLocale(result);
            },
            "extractData": function (result) {
                return Api.ResultHandling.extractData(result);
            },
            /**
             * Checks, if a given HttpResponse has a 403 status code and exits
             * the Backend, if so.
             * @param result
             */
            "check403": function (result) {
                if (result.status === 403) {
                    window.location.reload(true);
                }
                return result;
            },

            /**
             * Checks a server response for an invalid credentials error.
             * If an error of the kind is found, the user is logged out.
             *
             * @param result
             * @returns {*}
             */
            "checkLoggedIn": function (result) {
                if ("error" in result &&
                    result.error == "Lacking credentials.") {
                    window.location.reload(true);
                }
                return result;
            }
        }
    }])
    .factory("LanguageHandling", [function () {
        return Api.LanguageHandling;
    }])
    .factory("PathHandling", [function () {
        return Api.PathHandling;
    }])
    .factory("Account", ["ResultHandling", function (ResultHandling) {
        return {
            "current": function () {
                return Api.Account.current()
                    .mapRej(ResultHandling.checkLoggedIn);
            },
            /**
             * Updates the currently logged in account.
             *
             * @param email
             * @param locale
             * @returns A Future rejecting with the result of the update process.
             */
            "update": function ({email = null, locale = null}) {
                return Api.Account.update({email, locale})
                    .mapRej(ResultHandling.checkLoggedIn);
            }
        };
    }])
    .factory("Locales", [
        function () {
            return Api.Locale;
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
                        .mapRej(ResultHandling.check403)
                        .map(ResultHandling.extractDataAndLocale);
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
                        .mapRej(ResultHandling.check403)
                        .map(ResultHandling.extractData);
                },
                "update": function (uuid, name) {
                    return Future.tryP(() => $http({
                        "method": "PUT",
                        "url": `/api/survey/${uuid}`,
                        "data": {
                            "name": name
                        },
                        "headers": {
                            "Content-Type": "application/json"
                        }
                    }))
                        .mapRej(ResultHandling.check403)
                        .map(ResultHandling.extractData);
                },
                "delete": function (uuid) {
                    return Future.tryP(() => $http({
                        "method": "DELETE",
                        "url": `/api/survey/${uuid}`
                    }))
                        .mapRej(ResultHandling.check403)
                        .map(ResultHandling.extractData)
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
                        .mapRej(ResultHandling.check403)
                        .map(ResultHandling.extractData)
                },
                "get": function (questionnaire_uuid, locale = "") {
                    const path = PathHandling.pathMaybeWithLocale(
                        `/api/questionnaire/${questionnaire_uuid}`, locale
                    );
                    return Future.tryP(() => {
                        return $http.get(path);
                    })
                        .mapRej(ResultHandling.check403)
                        .map(ResultHandling.extractDataAndLocale);
                },
                "update": function (questionnaire_uuid, data) {
                    const {name = null, description = null} = data;
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
                        .mapRej(ResultHandling.check403)
                        .map(ResultHandling.extractData);
                },
                "publish": function (questionnaire_uuid) {
                    return Future.tryP(() => $http({
                        "method": "PATCH",
                        "url": `/api/questionnaire/${questionnaire_uuid}/publish`
                    }))
                        .mapRej(ResultHandling.check403)
                        .map(ResultHandling.extractData);
                },
                "unpublish": function (questionnaire_uuid) {
                    return Future.tryP(() => $http({
                        "method": "PATCH",
                        "url": `/api/questionnaire/${questionnaire_uuid}/unpublish`
                    }))
                        .mapRej(ResultHandling.check403)
                        .map(ResultHandling.extractData);
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
                        .mapRej(ResultHandling.check403)
                        .map(ResultHandling.extractData)
                },
                "listTemplates": function () {
                    return Future.tryP(() => $http({
                        "method": "GET",
                        "url": "/api/questionnaire/templates"
                    }))
                        .mapRej(ResultHandling.check403)
                        .map(ResultHandling.extractData);
                },
                "listQACs": function (questionnaire_uuid) {
                    return Future.tryP(() => $http({
                        "method": "GET",
                        "url": `/api/questionnaire/${questionnaire_uuid}/qac`
                    }))
                        .mapRej(ResultHandling.check403)
                        .map(ResultHandling.extractData);
                },
                "getQACConfig": function (questionnaire_uuid, qac_name) {
                    return Future.tryP(() => $http({
                        "method": "GET",
                        "url": `/api/questionnaire/${questionnaire_uuid}/qac/${qac_name}`
                    }))
                        .mapRej(ResultHandling.check403)
                        .map(ResultHandling.extractData);
                },
                "enableQAC": function (questionnaire_uuid, qac_name) {
                    return Future.tryP(() => $http({
                        "method": "POST",
                        "url": `/api/questionnaire/${questionnaire_uuid}/qac/${qac_name}`
                    }))
                        .mapRej(ResultHandling.check403)
                        .map(ResultHandling.extractData);
                },
                "configureQAC": function (questionnaire_uuid, qac_name, data) {
                    return Future.tryP(() => $http({
                        "method": "PUT",
                        "url": `/api/questionnaire/${questionnaire_uuid}/qac/${qac_name}`,
                        "data": data,
                        "headers": {
                            "Content-Type": "application/json"
                        }
                    }))
                        .mapRej(ResultHandling.check403)
                        .map(ResultHandling.extractData);
                },
                "disableQAC": function (questionnaire_uuid, qac_name) {
                    return Future.tryP(() => $http({
                        "method": "DELETE",
                        "url": `/api/questionnaire/${questionnaire_uuid}/qac/${qac_name}`
                    }))
                        .mapRej(ResultHandling.check403)
                        .map(ResultHandling.extractData);
                },
            }
        }])
    .factory("QuestionGroups", ["$http", "ResultHandling",
        function ($http, ResultHandling) {
            return {
                "create": function (questionnaire_uuid, name) {
                    return Future.tryP(() => $http({
                        "method": "POST",
                        "url": "/api/question_group",
                        "data": {
                            "questionnaire_uuid": questionnaire_uuid,
                            "name": name,
                        },
                        "headers": {
                            "Content-Type": "application/json"
                        }
                    }))
                        .mapRej(ResultHandling.check403)
                        .map(ResultHandling.extractData);
                },
                "update": function (questionGroup_uuid, data) {
                    const {name = null, color = null, textColor = null} = data;
                    return Future.tryP(() => $http({
                        "method": "PUT",
                        "url": `/api/question_group/${questionGroup_uuid}`,
                        "data": {
                            "name": name,
                            "color": color,
                            "text_color": textColor
                        },
                        "headers": {
                            "Content-Type": "application/json"
                        }
                    }))
                        .mapRej(ResultHandling.check403)
                        .map(ResultHandling.extractData);
                },
                "delete": function (questionGroup_uuid, questionnaire_uuid) {
                    return Future.tryP(() => $http({
                        "method": "DELETE",
                        "url": `/api/question_group/${questionGroup_uuid}`,
                        "data": {
                            "questionnaire_uuid": questionnaire_uuid
                        },
                        "headers": {
                            "Content-Type": "application/json"
                        }
                    }))
                        .mapRej(ResultHandling.check403)
                        .map(ResultHandling.extractData);
                }
            }
        }])
    .factory("Questions", ["$http", "ResultHandling",
        function ($http, ResultHandling) {
            return {
                "create": function (questionnaire_uuid, questionGroup_uuid,
                                    text) {
                    return Future.tryP(() => $http({
                        "method": "POST",
                        "url": "/api/question",
                        "data": {
                            "questionnaire_uuid": questionnaire_uuid,
                            "question_group_uuid": questionGroup_uuid,
                            "text": text
                        },
                        "headers": {
                            "Content-Type": "application/json"
                        }
                    }))
                        .mapRej(ResultHandling.check403)
                        .map(ResultHandling.extractData);
                },
                "update": function (question_uuid, text) {
                    return Future.tryP(() => $http({
                        "method": "PUT",
                        "url": `/api/question/${question_uuid}`,
                        "data": {
                            "text": text
                        },
                        "headers": {
                            "Content-Type": "application/json"
                        }
                    }))
                        .mapRej(ResultHandling.check403)
                        .map(ResultHandling.extractData);
                },
                "delete": function (question_uuid, questionnaire_uuid,
                                    questionGroup_uuid) {
                    return Future.tryP(() => $http({
                        "method": "DELETE",
                        "url": `/api/question/${question_uuid}`,
                        "data": {
                            "questionnaire_uuid": questionnaire_uuid,
                            "question_group_uuid": questionGroup_uuid
                        },
                        "headers": {
                            "Content-Type": "application/json"
                        }
                    }))
                        .mapRej(ResultHandling.check403)
                        .map(ResultHandling.extractData);
                }
            }
        }])
    .factory("QACs", ["$http", "ResultHandling",
        function ($http, ResultHandling) {
            return {
                "list": function () {
                    return Future.tryP(() => $http({
                        "method": "GET",
                        "url": "/api/qac_module"
                    }))
                        .mapRej(ResultHandling.check403)
                        .map(ResultHandling.extractData);
                }
            }
        }])
    .factory("QuestionStatistics", [
        "$http", "Questionnaires", "ResultHandling", "LanguageHandling",
        function ($http, Questionnaires, ResultHandling, LanguageHandling) {
            let get = function (question_uuid) {
                return Future.tryP(() => $http({
                    "method": "GET",
                    "url": `/api/question/${question_uuid}/statistic`
                }))
                    .mapRej(ResultHandling.check403)
                    .map(ResultHandling.extractData)
                    .map(result => ({
                        "biggest": R.path(["fields", "biggest"], result),
                        "smallest": R.path(["fields", "smallest"], result),
                        "q1": R.path(["fields", "q1"], result),
                        "q2": R.path(["fields", "q2"], result),
                        "q3": R.path(["fields", "q3"], result),
                        "answer_count": R.path(
                            ["fields", "answer_count"],
                            result
                        )
                    }));
            };

            return {
                "get": get,
                "getWholeQuestionnaire": function (questionnaire_uuid) {
                    return Questionnaires
                        .get(questionnaire_uuid)
                        .map(({data: questionnaireData, locale}) => {
                            return R.pipe(
                                R.map(questionGroup => ({
                                    "name": questionGroup.fields.name,
                                    "color": questionGroup.fields.color,
                                    "text_color": questionGroup.fields.text_color,
                                    "questions": questionGroup.fields.questions
                                })),
                                R.map(questionGroup => R.assoc(
                                    "questions",
                                    R.map(question => get(question.uuid)
                                            .map(statisticResult => {
                                                return {
                                                    "text": LanguageHandling.getStringLocale(locale, question.fields.text),
                                                    "answers": R.pathOr([], ["fields", "results"], question).length,
                                                    "statistic": statisticResult
                                                }
                                            }),
                                        questionGroup.questions
                                    ),
                                    questionGroup
                                )),
                                R.map(questionGroup =>
                                    Future.parallel(
                                        Infinity,
                                        questionGroup.questions
                                    )
                                        .map(questions => {
                                            return R.assoc(
                                                "questions",
                                                questions,
                                                questionGroup
                                            )
                                        })
                                ))
                            (questionnaireData.fields.questiongroups);
                        })
                        .chain(questionGroups => {
                            return Future.parallel(
                                Infinity,
                                questionGroups
                            );
                        });
                },
                "update": function (questionnaire_uuid, force = false) {
                    if (force) {
                        return Future.tryP(() => $http({
                            "method": "POST",
                            "url": "/api/statistics/update/force"
                        }))
                            .map(ResultHandling.extractData);
                    } else {
                        return Future.tryP(() => $http({
                            "method": "POST",
                            "url": "/api/statistics/update"
                        }))
                            .map(ResultHandling.extractData);
                    }
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
            "template": require("./templates/loading.html"),
            "link": function (scope) {
                scope.$watch("loading", new_value => {
                    scope.loading = new_value;
                });
            }
        }
    });
