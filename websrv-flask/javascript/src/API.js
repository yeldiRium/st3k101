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
    .factory("Locales", ["$http", "ResultHandling",
        function ($http, ResultHandling) {
            return Api.Locale;
        }])
    .factory("Surveys", ["ResultHandling",
        function (ResultHandling) {
            return {
                "all": function (locale = "") {
                    return Api.Survey.all()
                        .chainRej(ResultHandling.checkLoggedIn);
                },
                "create": function (name) {
                    return Api.Survey.create(name)
                        .chainRej(ResultHandling.checkLoggedIn);
                },
                "update": function (uuid, name) {
                    return Api.Survey.update(uuid, name)
                        .chainRej(ResultHandling.checkLoggedIn);
                },
                "delete": function (uuid) {
                    return Api.Survey.delete(uuid)
                        .chainRej(ResultHandling.checkLoggedIn);
                }
            }
        }])
    .factory("Questionnaires", ["ResultHandling",
        function (ResultHandling) {
            return {
                "create": function (data) {
                    return Api.Questionnaire.create(data)
                        .chainRej(ResultHandling.checkLoggedIn);
                },
                "get": function (questionnaire_uuid, locale = "") {
                    return Api.Questionnaire.get(questionnaire_uuid, locale)
                        .chainRej(ResultHandling.checkLoggedIn);
                },
                "update": function (questionnaire_uuid, data) {
                    return Api.Questionnaire.update(questionnaire_uuid, data)
                        .chainRej(ResultHandling.checkLoggedIn);
                },
                "publish": function (questionnaire_uuid) {
                    return Api.Questionnaire.publish(questionnaire_uuid)
                        .chainRej(ResultHandling.checkLoggedIn);
                },
                "unpublish": function (questionnaire_uuid) {
                    return Api.Questionnaire.unpublish(questionnaire_uuid)
                        .chainRej(ResultHandling.checkLoggedIn);
                },
                "delete": function (questionnaire_uuid, survey_uuid) {
                    return Api.Questionnaire.delete(
                        questionnaire_uuid, survey_uuid
                    )
                        .chainRej(ResultHandling.checkLoggedIn);
                },
                "listTemplates": function () {
                    return Api.Questionnaire.listTemplates()
                        .chainRej(ResultHandling.checkLoggedIn);
                },
                "listQACs": function (questionnaire_uuid) {
                    return Api.Questionnaire.listQACs(questionnaire_uuid)
                        .chainRej(ResultHandling.checkLoggedIn);
                },
                "getQACConfig": function (questionnaire_uuid, qac_name) {
                    return Api.Questionnaire.getQACConfig(
                        questionnaire_uuid, qac_name
                    )
                        .chainRej(ResultHandling.checkLoggedIn);
                },
                "enableQAC": function (questionnaire_uuid, qac_name) {
                    return Api.Questionnaire.enableQAC(
                        questionnaire_uuid, qac_name
                    )
                        .chainRej(ResultHandling.checkLoggedIn);
                },
                "configureQAC": function (questionnaire_uuid, qac_name, data) {
                    return Api.Questionnaire.configureQAC(
                        questionnaire_uuid, qac_name, data
                    )
                        .chainRej(ResultHandling.checkLoggedIn);
                },
                "disableQAC": function (questionnaire_uuid, qac_name) {
                    return Api.Questionnaire.disableQAC(
                        questionnaire_uuid, qac_name
                    )
                        .chainRej(ResultHandling.checkLoggedIn);
                },
            }
        }])
    .factory("QuestionGroups", ["ResultHandling",
        function (ResultHandling) {
            return {
                "create": function (questionnaire_uuid, name) {
                    return Api.QuestionGroup.create(questionnaire_uuid, name)
                        .chainRej(ResultHandling.checkLoggedIn);
                },
                "update": function (questionGroup_uuid, data) {
                    return Api.QuestionGroup.update(questionGroup_uuid, data)
                        .chainRej(ResultHandling.checkLoggedIn);
                },
                "delete": function (questionGroup_uuid, questionnaire_uuid) {
                    return Api.QuestionGroup.delete(
                        questionGroup_uuid,
                        questionnaire_uuid
                    )
                        .chainRej(ResultHandling.checkLoggedIn)
                }
            }
        }])
    .factory("Questions", ["ResultHandling",
        function (ResultHandling) {
            return {
                "create": function (questionnaire_uuid, questionGroup_uuid,
                                    text) {
                    return Api.Question.create(
                        questionnaire_uuid, questionGroup_uuid, text
                    )
                        .mapRej(ResultHandling.checkLoggedIn);
                },
                "update": function (question_uuid, text) {
                    return Api.Question.update(question_uuid, text)
                        .mapRej(ResultHandling.checkLoggedIn);
                },
                "delete": function (question_uuid, questionnaire_uuid,
                                    questionGroup_uuid) {
                    return Api.Question.delete(
                        question_uuid, questionnaire_uuid, questionGroup_uuid
                    )
                        .mapRej(ResultHandling.checkLoggedIn);
                }
            }
        }])
    .factory("QACs", [function () {
        return Api.QAC;
    }])
    .factory("QuestionStatistics", ["ResultHandling",
        function (ResultHandling) {
            return {
                "get": function (question_uuid) {
                    return Api.QuestionStatistic.get(question_uuid)
                        .mapRej(ResultHandling.checkLoggedIn);
                },
                "getWholeQuestionnaire": function (questionnaire_uuid) {
                    return Api.QuestionStatistic.getWholeQuestionnaire(
                        questionnaire_uuid
                    )
                        .mapRej(ResultHandling.checkLoggedIn);
                },
                "update": function (questionnaire_uuid, force = false) {
                    return Api.QuestionStatistic.update(
                        questionnaire_uuid, force
                    )
                        .mapRej(ResultHandling.checkLoggedIn);
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
