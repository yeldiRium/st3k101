const angular = require("angular");
const Future = require("fluture");
const R = require("ramda");
const $ = require("jquery");

require("angular-route");
require("angular-flash-alert");
require("./API");

angular.module("Surveys", ["ngRoute", "ngFlash", "API"])
    .config(["FlashProvider", function (FlashProvider) {
        FlashProvider.setTimeout(5000);
        FlashProvider.setShowClose(true);
    }])
    .controller("SurveysController", [
        "$scope", "$http", "$timeout", "Flash", "Surveys", "Questionnaires",
        "ResultHandling", "LanguageHandling", "PathHandling", "StyleStuff",
        function ($scope, $http, $timeout, Flash, Surveys, Questionnaires,
                  ResultHandling, LanguageHandling, PathHandling, StyleStuff) {
            $scope.loading = "loading";

            /**
             * Queries surveys and writes them into $scope.surveys.
             * If something goes wrong, $scope.error will be set.
             * @returns Promise
             */
            $scope.init = function () {
                /**
                 * Queries for surveys and creates a list of templates that
                 * can be used for new questionnaires based on the surveys
                 * found.
                 * The default options for templates are 'efla_teacher' and
                 * 'efla_student', which are standardized tests.
                 *
                 * If something goes wrong, an error message is set and nothing
                 * else displayed.
                 */
                Surveys.all()
                    .mapRej(ResultHandling.flashError($scope))
                    .fork(
                        // Status 500 somehow doesn't reject. Why?
                        () => {
                            $scope.surveys = null;
                            $scope.$apply(() => {
                                $scope.loading = "error";
                            });
                        },
                        prepareView
                    );
            };

            /**
             * Stores and optionally parses the given data for Surveys, Ques-
             * tionnaires and Templates.
             *
             * @param data
             * @param locale
             */
            let prepareView = function ({data, locale}) {
                $scope.surveys = R.pipe(
                    R.map(LanguageHandling.getSurveyTranslation(locale)),
                    R.map(survey => {
                        let original_locale = R.head(R.map(
                            R.toLower,
                            [R.path(["fields", "original_locale"], survey)]
                        ));
                        if (original_locale !== locale.toLowerCase()) {
                            return R.pipe(
                                R.assoc(
                                    "original",
                                    LanguageHandling.getSurveyTranslation(
                                        original_locale, survey
                                    )
                                ),
                                R.assoc(
                                    "original_locale",
                                    original_locale
                                )
                            )(survey);
                        } else {
                            return R.assoc(
                                "original_locale",
                                null,
                                survey
                            );
                        }
                    })
                )(data);
                $scope.templates = prepareTemplates(
                    locale, $scope.surveys
                );
                $scope.$apply(() => {
                    $scope.loading = "done";
                });


                StyleStuff.equalizeSelectboxes(
                    ".as-checkbox", ".selectable"
                );
            };

            /**
             * Returns a function which takes a parsed Survey and:
             *
             * Generates the template options for the select field.
             *
             * At the beginning a dummy element and the efla templates are
             * added.
             *
             * For each Survey which has Questionnaires a paragraph is generated
             * which starts with the Survey's name and contains a list of all
             * Questionnaires.
             *
             * @param locale
             */
            let prepareTemplates = R.pipe(
                R.filter(survey =>
                    R.path(["fields", "questionnaires", "length"], survey)
                ),
                // Extract Questionnaires from Survey.
                R.map(survey => [
                    R.path(["fields", "name"], survey),
                    R.path(["fields", "questionnaires"], survey)
                ]),
                // Format them for use in a select field.
                R.map(([name, questionnaires]) => ([
                    name,
                    R.map(
                        questionnaire => ({
                            "value": R.path(["uuid"], questionnaire),
                            "name": R.path(
                                ["fields", "name"], questionnaire
                            )
                        }),
                        questionnaires
                    )
                ])),
                // Prepend a spacer element with the Survey name and return
                // only resulting list of select elements.
                R.map(([name, questionnaires]) => R.prepend(
                    {
                        "value": null,
                        "name": "-- from Survey " + name + " --"
                    },
                    questionnaires
                )),
                R.flatten,
                R.prepend({
                    "value": "efla_student",
                    "name": "EFLA Student"
                }),
                R.prepend({
                    "value": "efla_teacher",
                    "name": "EFLA Teacher"
                }),
                R.prepend({
                    "value": null,
                    "name": "You can optionally create a questionnaire from a template. Select one here."
                })
            );

            /**
             * Navigates to the frontend view of a Questionnaire.
             * @param questionnaire
             */
            $scope.gotoQuestionnaire = function (questionnaire) {
                if (!PathHandling.openQuestionnaire(questionnaire.uuid)) {
                    Flash.create("danger", `Tried to open the questionnaire, but the popup was blocked.`);
                }
            };

            $scope.startEditing = function (name, event, opt = null) {
                $scope.edit = {};
                const element = $(event.target);
                $scope.edit.name = name;
                $scope.edit.element = element;
                $scope.edit.old_value = (opt != null) ? opt : element.text();
            };

            $scope.isEditing = function (name) {
                return $scope.edit.name === name;
            };

            $scope.abortEditing = function (name, event, opt = null) {
                if ($scope.edit.name === name) {
                    if (name === "surveyname") {
                        opt.fields.name = $scope.edit.old_value;
                    } else if (name === "questionnairename") {
                        opt.fields.name = $scope.edit.old_value;
                    } else if (name === "questionnairedescription") {
                        opt.fields.description = $scope.edit.old_value;
                    }
                    $scope.edit = {};
                }
            };

            $scope.stopEditing = function (name, event, opt = null) {
                if ($scope.edit.name === name) {
                    const element = $(event.target);
                    let success;
                    if (name === "surveyname") {
                        success = Surveys.update(
                            element.data("uuid"), element[0].value
                        );
                    }
                    if (name === "questionnairename") {
                        success = Questionnaires.update(
                            element.data("uuid"),
                            {
                                "name": element[0].value
                            }
                        );
                    }
                    if (name === "questionnairedescription") {
                        console.log(element[0].value);
                        success = Questionnaires.update(
                            element.data("uuid"),
                            {
                                "description": element[0].value
                            }
                        );
                    }
                    success
                        .mapRej(error => {
                            $scope.abortEditing(name, event, opt);
                            return error
                        })
                        .map(data => {
                            $scope.edit = {};
                            return data;
                        })
                        .fork(
                            ResultHandling.flashError($scope),
                            ResultHandling.flashSuccess($scope)
                        );
                }
            };

            /**
             * Toggles the selection of a single questionnaire.
             * Selection is survey-based. It is not possible to select multi-
             * ple questionnaires across surveys.
             * So the previous selection is reset, if a questionnaire on a different survey is selected.
             *
             * @param survey
             * @param questionnaire
             */
            $scope.toggleSelect = function (survey, questionnaire) {
                if ($scope.selection.survey !== survey) {
                    $scope.resetEditing();
                }
                $scope.selection.survey = survey;
                if ($scope.selection.questionnaires[questionnaire.uuid] === true) {
                    $scope.selection.questionnaires[questionnaire.uuid] = false;
                    $scope.selection.count--;
                } else {
                    $scope.selection.questionnaires[questionnaire.uuid] = true;
                    $scope.selection.count++;
                }
                if ($scope.selection.count === 0) {
                    $scope.resetEditing();
                }
            };

            /**
             * Resets all editing forms and all temporary data.
             */
            $scope.resetEditing = function () {
                $scope.new = {
                    questionnaire: {
                        survey: null,
                        data: null,
                        template: null
                    },
                    survey: {
                        data: null
                    }
                };

                $scope.selection = {
                    survey: null,
                    questionnaires: {},
                    count: 0
                };

                $scope.edit = {};
            };

            /**
             * Opens a form for a new Survey by setting temporary data to
             * default values.
             */
            $scope.newSurvey = function () {
                $scope.resetEditing();
                $scope.new.survey.data = {
                    name: "name"
                }
            };

            /**
             * Sends a create request for a new Survey with the current tempora-
             * ry data.
             */
            $scope.createSurvey = function () {
                if ($scope.new.survey.data == null) {
                    return;
                }
                Surveys.create($scope.new.survey.data.name)
                    .chain(data => {
                        $scope.init();
                        return Future.of(data);
                    })
                    .fork(
                        ResultHandling.flashError($scope),
                        ResultHandling.flashSuccess($scope)
                    );
            };

            /**
             * Sends a delete request for a specific survey.
             * @param survey
             */
            $scope.deleteSurvey = function (survey) {
                Surveys.delete(survey.uuid)
                    .chain(data => {
                        $scope.surveys.splice(
                            $scope.surveys.indexOf(survey), 1
                        );
                        return Future.of(data);
                    })
                    .fork(
                        ResultHandling.flashError($scope),
                        ResultHandling.flashSuccess($scope)
                    );
            };

            /**
             * Opens a form for a new questionnaire by setting temporary data to
             * default values.
             * @param survey
             */
            $scope.newQuestionnaire = function (survey) {
                $scope.resetEditing();
                $scope.new.questionnaire.survey = survey;
                $scope.new.questionnaire.data = {
                    name: "name",
                    description: "description",
                    template: null
                };
            };

            /**
             * Sends a create request for a new Questionnaire.
             * Uses the current temporary data, which is bound to the template
             * form.
             */
            $scope.createQuestionnaire = function () {
                if (($scope.new.questionnaire.survey == null)
                    || $scope.new.questionnaire.data == null) {
                    return;
                }
                Questionnaires.create({
                    survey_uuid: $scope.new.questionnaire.survey.uuid,
                    name: $scope.new.questionnaire.data.name,
                    description: $scope.new.questionnaire.data.description,
                    template: $scope.new.questionnaire.data.template
                })
                    .chain(data => {
                        $scope.resetEditing();
                        $scope.init();
                        return Future.of(data);
                    })
                    .fork(
                        ResultHandling.flashError($scope),
                        ResultHandling.flashSuccess($scope)
                    );
            };

            /**
             * Publishes the Questionnaire. Enables the open button.
             */
            $scope.publishQuestionnaire = function (questionnaire) {
                Questionnaires.publish(questionnaire.uuid)
                    .map(result => {
                        $scope.$apply(() => {
                            questionnaire.fields.published = true;
                        });
                        return result;
                    })
                    .fork(
                        ResultHandling.flashError($scope),
                        ResultHandling.flashSuccess($scope)
                    )
            };

            /**
             * Unpublishes the Questionnaire.
             */
            $scope.unpublishQuestionnaire = function (questionnaire) {
                Questionnaires.unpublish(questionnaire.uuid)
                    .map(result => {
                        $scope.$apply(() => {
                            questionnaire.fields.published = false;
                        });
                        return result;
                    })
                    .fork(
                        ResultHandling.flashError($scope),
                        ResultHandling.flashSuccess($scope)
                    )
            };

            /**
             * Sends delete requests for all currently selected questionnaires.
             */
            $scope.deleteQuestionnaires = function () {
                const survey_uuid = $scope.selection.survey.uuid;
                const deleteFutures = R.pipe(
                    R.filter(([questionnaire_uuid, shouldDelete]) => shouldDelete),
                    R.map(([questionnaire_uuid]) => questionnaire_uuid),
                    R.map(questionnaire_uuid => Questionnaires.delete(
                        questionnaire_uuid, survey_uuid
                    ))
                )(Object.entries($scope.selection.questionnaires));

                Future.parallel(Infinity, deleteFutures)
                    .map(data => {
                            $scope.resetEditing();
                            $scope.init();
                            return data;
                        }
                    )
                    .fork(
                        R.map(ResultHandling.flashError($scope)),
                        R.map(ResultHandling.flashSuccess($scope))
                    );
            };

            $scope.resetEditing();
            $scope.init();
        }
    ])
    .controller("EditQuestionnaireController", [
        "$scope", "$http", "$timeout", "Flash", "$routeParams",
        "Questionnaires", "QuestionGroups", "Questions", "ResultHandling",
        "LanguageHandling", "PathHandling", "StyleStuff",
        function ($scope, $http, $timeout, Flash, $routeParams,
                  Questionnaires, QuestionGroups, Questions, ResultHandling,
                  LanguageHandling, PathHandling, StyleStuff) {
            $scope.loading = "loading";

            /**
             * Queries the current questionnaire and stores its data.
             * If something goes wrong, an error message is displayed and
             * nothing else.
             */
            $scope.init = function () {
                return Questionnaires.get($routeParams.questionnaire)
                // Load QACs for Questionnaire and store them
                    .chain(({data: questionnaire, locale}) => Questionnaires
                        .listQACs(questionnaire.uuid)
                        .map(qacList => ({
                            "questionnaire": R.assoc(
                                "qacs",
                                R.map(
                                    LanguageHandling.getQacTranslation(locale),
                                    qacList
                                ),
                                questionnaire
                            ),
                            "locale": locale
                        }))
                    )
                    // Parse original locale
                    .map(({questionnaire, locale}) => ({
                        "questionnaire": R.assoc(
                            "original_locale",
                            R.either(
                                () => R.apply(
                                    R.toLower,
                                    [R.path(
                                        ["fields", "original_locale"], questionnaire
                                    )]
                                ),
                                () => null
                            ),
                            questionnaire
                        ),
                        "locale": locale
                    }))
                    .mapRej(data => {
                        $scope.questionnaire = null;
                        $scope.$apply(() => {
                            $scope.loading = "error";
                        });
                        return data;
                    })
                    .fork(
                        ResultHandling.flashError($scope),
                        prepareView
                    );
            };

            function prepareView({questionnaire, locale}) {
                const parsed_questionnaire = LanguageHandling
                    .getQuestionnaireTranslation(locale, questionnaire);
                let parsed_questionnaire_original = false;

                if (questionnaire.original_locale !== locale.toLowerCase()) {
                    parsed_questionnaire_original = LanguageHandling
                        .getQuestionnaireTranslation(
                            questionnaire.original_locale, questionnaire
                        );
                }

                $scope.questionnaire = parsed_questionnaire;
                if (parsed_questionnaire_original) {
                    $scope.questionnaire_original =
                        parsed_questionnaire_original;
                    $scope.original_locale = R.map(R.toLower, questionnaire.original_locale);
                }
                $scope.$apply(() => {
                    $scope.loading = "done";
                });

                R.forEach(
                    function (questiongroup) {
                        setTimeout(StyleStuff.colorPicker(
                            R.path(["fields", "color"], questiongroup),
                            `#colorPicker_${questiongroup.uuid}`,
                            function (color) {
                                $scope.updateQuestionGroupColor(
                                    color, questiongroup
                                );
                            }
                        ), 0);
                        setTimeout(StyleStuff.colorPicker(
                            R.path(["fields", "text_color"], questiongroup),
                            `#textColorPicker_${questiongroup.uuid}`,
                            function (color) {
                                $scope.updateQuestionGroupTextColor(
                                    color, questiongroup
                                );
                            }
                        ), 0);
                    },
                    R.path(["fields", "questiongroups"], parsed_questionnaire)
                );

                StyleStuff.equalizeSelectboxes(
                    ".as-checkbox", ".selectable"
                );
            }

            /**
             * Navigates to the frontend view of a Questionnaire.
             */
            $scope.gotoQuestionnaire = function () {
                if (!PathHandling.openQuestionnaire($scope.questionnaire.uuid)) {
                    Flash.create("danger", `Tried to open the questionnaire, but the popup was blocked.`);
                }
            };

            $scope.startEditing = function (name, event, opt = null) {
                $scope.edit = {};
                const element = $(event.target);
                $scope.edit.name = name;
                $scope.edit.element = element;
                $scope.edit.old_value = (opt != null) ? opt : element.text();
            };

            $scope.isEditing = function (name) {
                return $scope.edit.name === name;
            };

            $scope.abortEditing = function (name, event, opt = null) {
                if ($scope.edit.name === name) {
                    if (name === "questionnairename") {
                        opt.fields.name = $scope.edit.old_value;
                    } else if (name === "questionnairedescription") {
                        opt.fields.description = $scope.edit.old_value;
                    } else if (name.indexOf("questiongroup") !== -1) {
                        opt.fields.name = $scope.edit.old_value;
                    } else if (name.indexOf("singlequestion") !== -1) {
                        opt.fields.text = $scope.edit.old_value;
                    }
                    $scope.edit = {};
                }
            };

            $scope.stopEditing = function (name, event, opt = null) {
                if ($scope.edit.name === name) {
                    const element = $(event.target);
                    let success;
                    if (name === "questionnairename" || name === "questionnairedescription") {
                        success = $scope.updateQuestionnaire();
                    }
                    if (name.indexOf("questiongroup") !== -1) {
                        success = $scope.updateQuestionGroup(element.data("uuid"), element[0].value);
                    }
                    if (name.indexOf("singlequestion") !== -1) {
                        success = $scope.updateQuestion(element.data("uuid"), element[0].value);
                    }

                    if (success)
                        $scope.edit = {};
                    else
                        $scope.abortEditing(name, event, opt);
                }
            };

            /**
             * Toggles the selection of a single question.
             * Selection is questionGroup-based. It is not possible to select
             * multiple questions across questionGroup.
             * So the previous selection is reset, if a question on a different
             * questionGroup is selected.
             *
             * @param questionGroup
             * @param question
             */
            $scope.toggleSelect = function (questionGroup, question) {
                if ($scope.selection.questionGroup !== questionGroup) {
                    $scope.resetEditing();
                }
                $scope.selection.questionGroup = questionGroup;
                if ($scope.selection.questions[question.uuid] === true) {
                    $scope.selection.questions[question.uuid] = false;
                    $scope.selection.count--;
                } else {
                    $scope.selection.questions[question.uuid] = true;
                    $scope.selection.count++;
                }
                if ($scope.selection.count === 0) {
                    $scope.resetEditing();
                }
            };

            /**
             * Resets all editing forms and all temporary data.
             */
            $scope.resetEditing = function () {
                $scope.new = {
                    question: {
                        questionGroup: null,
                        data: null
                    },
                    questionGroup: {
                        data: null
                    }
                };

                $scope.selection = {
                    questionGroup: null,
                    questions: {},
                    count: 0
                };

                $scope.edit = {};
            };

            /**
             * Sends updates with current questionnaire data
             */
            $scope.updateQuestionnaire = function () {
                const name = R.path(
                    ["fields", "name"], $scope.questionnaire
                );
                const description = R.path(
                    ["fields", "description"], $scope.questionnaire
                );

                if (name === "" || description === "") {
                    Flash.create("danger", "Name and description can't be empty!");
                    return false;
                }
                Questionnaires.update(
                    $scope.questionnaire.uuid,
                    {
                        "name": name,
                        "description": description
                    }
                )
                    .fork(
                        ResultHandling.flashError($scope),
                        ResultHandling.flashSuccess($scope)
                    );
                return true;
            };

            /**
             * Publishes the Questionnaire. Enables the open button.
             */
            $scope.publishQuestionnaire = function (questionnaire) {
                Questionnaires.publish(questionnaire.uuid)
                    .map(result => {
                        $scope.$apply(() => {
                            questionnaire.fields.published = true;
                        });
                        return result;
                    })
                    .fork(
                        ResultHandling.flashError($scope),
                        ResultHandling.flashSuccess($scope)
                    )
            };

            /**
             * Unpublishes the Questionnaire.
             */
            $scope.unpublishQuestionnaire = function (questionnaire) {
                Questionnaires.unpublish(questionnaire.uuid)
                    .map(result => {
                        $scope.$apply(() => {
                            questionnaire.fields.published = false;
                        });
                        return result;
                    })
                    .fork(
                        ResultHandling.flashError($scope),
                        ResultHandling.flashSuccess($scope)
                    )
            };

            /**
             * Opens a form for a new QuestionGroup by setting temporary data to
             * default values.
             */
            $scope.newQuestionGroup = function () {
                $scope.resetEditing();
                $scope.new.questionGroup.data = {
                    name: "name"
                }
            };

            /**
             * Sends a create request for a new QuestionGroup with the current
             * temporary data.
             */
            $scope.createQuestionGroup = function () {
                const name = R.path(
                    ["new", "questionGroup", "data", "name"], $scope
                );
                if (typeof name === "undefined" || name === "" || name === null) {
                    return;
                }

                QuestionGroups.create(
                    $scope.questionnaire.uuid,
                    $scope.new.questionGroup.data.name
                )
                    .map(data => {
                        $scope.resetEditing();
                        $scope.init();
                        return data;
                    })
                    .fork(
                        ResultHandling.flashError($scope),
                        ResultHandling.flashSuccess($scope)
                    );
            };

            /**
             * Updates a question_group's name based on the stored values in
             * $scope.edit.
             */
            $scope.updateQuestionGroup = function (uuid, name) {
                if (name === "") {
                    Flash.create("danger", "Name can't be empty!");
                    return false;
                }

                QuestionGroups
                    .update(uuid, {name})
                    .fork(
                        ResultHandling.flashError($scope),
                        ResultHandling.flashSuccess($scope)
                    );
                return true;
            };

            $scope.updateQuestionGroupColor = function (color, questionGroup) {
                QuestionGroups
                    .update(questionGroup.uuid, {color})
                    .map(data => {
                        questionGroup.fields.color = color;
                        return data;
                    })
                    .fork(
                        ResultHandling.flashError($scope),
                        ResultHandling.flashSuccess($scope)
                    );
            };

            $scope.updateQuestionGroupTextColor = function (color, questionGroup) {
                QuestionGroups
                    .update(questionGroup.uuid, {"textColor": color})
                    .map(data => {
                        questionGroup.fields.text_color = color;
                        return data;
                    })
                    .fork(
                        ResultHandling.flashError($scope),
                        ResultHandling.flashSuccess($scope)
                    );
            };

            /**
             * Sends a delete request for a specific QuestionGroup.
             */
            $scope.deleteQuestionGroup = function (questionGroup) {
                QuestionGroups.delete(
                    questionGroup.uuid, $scope.questionnaire.uuid
                )
                    .map(data => {
                        $scope.questionnaire.fields.questiongroups.splice(
                            $scope.questionnaire.fields.questiongroups.indexOf(questionGroup),
                            1
                        );
                        return data;
                    })
                    .fork(
                        ResultHandling.flashError($scope),
                        ResultHandling.flashSuccess($scope)
                    );
            };

            /**
             * Opens a form for a new Question by setting temporary data to
             * default values.
             */
            $scope.newQuestion = function (questiongroup) {
                $scope.resetEditing();
                $scope.new.question.questionGroup = questiongroup;
                $scope.new.question.data = {
                    text: "text"
                };
            };

            /**
             * Sends a create request for a new Question with the current tempora-
             * ry data.
             */
            $scope.createQuestion = function () {
                if (($scope.new.question.questionGroup == null)
                    || $scope.new.question.data == null) {
                    return;
                }
                Questions.create(
                    $scope.questionnaire.uuid,
                    $scope.new.question.questionGroup.uuid,
                    $scope.new.question.data.text
                )
                    .map(data => {
                        $scope.resetEditing();
                        $scope.init();
                        return data;
                    })
                    .fork(
                        ResultHandling.flashError($scope),
                        ResultHandling.flashSuccess($scope)
                    );
            };

            /**
             * Updates a question's name based on the stored values in
             * $scope.edit.
             */
            $scope.updateQuestion = function (uuid, text) {
                if (text === "") {
                    Flash.create("danger", "Text can't be empty!");
                    return false;
                }
                Questions.update(uuid, text)
                    .fork(
                        ResultHandling.flashError($scope),
                        ResultHandling.flashSuccess($scope)
                    );
                return true;
            };

            /**
             * Sends a delete request for each currently selected Question.
             * TODO: error handling
             */
            $scope.deleteQuestions = function () {
                const questionnaire_uuid = $scope.questionnaire.uuid;
                const questionGroup_uuid = $scope.selection.questionGroup.uuid;
                const deleteFutures = R.pipe(
                    R.filter(([question_uuid, shouldDelete]) => shouldDelete),
                    R.map(R.head),
                    R.map(question_uuid => Questions.delete(
                        question_uuid, questionnaire_uuid, questionGroup_uuid
                    ))
                )(Object.entries($scope.selection.questions));

                Future.parallel(Infinity, deleteFutures)
                    .map(data => {
                            $scope.resetEditing();
                            $scope.init();
                            return data;
                        }
                    )
                    .fork(
                        R.map(ResultHandling.flashError($scope)),
                        R.map(ResultHandling.flashSuccess($scope))
                    );
            };

            /* QAC related stuff */

            $scope.updateI15dTextParameter = function (qacName, parameter) {
                const questionnaireUuid = $scope.questionnaire.uuid;
                const parameterName = parameter.fields.name.msgid;

                const data = {};
                data[parameterName] = parameter.fields.text;

                Questionnaires.configureQAC(questionnaireUuid, qacName, data)
                    .fork(
                        ResultHandling.flashError($scope),
                        ResultHandling.flashSuccess($scope)
                    );
            };

            $scope.updateTextParameter = function (qacName, parameter) {
                const questionnaireUuid = $scope.questionnaire.uuid;
                const parameterName = parameter.fields.name.msgid;

                const data = {};
                data[parameterName] = parameter.fields.text;

                Questionnaires.configureQAC(questionnaireUuid, qacName, data)
                    .fork(
                        ResultHandling.flashError($scope),
                        ResultHandling.flashSuccess($scope)
                    );
            };

            $scope.resetEditing();
            $scope.init();
        }])
    .controller("QuestionnaireStatisticController", [
        "$scope", "$http", "$routeParams", "$timeout", "Questionnaires",
        "QuestionStatistics", "ResultHandling", "LanguageHandling",
        function ($scope, $http, $routeParams, $timeout, Questionnaires,
                  QuestionStatistics, ResultHandling, LanguageHandling) {
            $scope.properties = {
                "questionnaire_uuid": null,
                "graph_width": window.innerWidth - 400,
                "graph_height": 60, // 2 * bar_padding as default
                "graph_padding_left": 100,
                "graph_padding_right": 100,
                "text_padding_left": 5,
                "text_padding_right": 80,
                "bar_height": 50,
                "bar_padding": 30,
                "upper_scale_line_upper_y": 20,
                "upper_scale_line_lower_y": 25,
                "upper_scale_text_y": 15,
                "lower_scale_line_upper_y": 25,
                "lower_scale_line_lower_y": 20,
                "lower_scale_text_y": 5
            };

            $scope.init = function () {
                Questionnaires
                    .get($routeParams.questionnaire)
                    .map(({data: questionnaireData, locale}) => {
                        $scope.questionnaire_uuid = questionnaireData.uuid;

                        return R.pipe(
                            R.map(questionGroup => ({
                                "name": questionGroup.fields.name,
                                "color": questionGroup.fields.color,
                                "text_color": questionGroup.fields.text_color,
                                "questions": questionGroup.fields.questions
                            })),
                            R.map(questionGroup => R.assoc(
                                "questions",
                                R.map(question => QuestionStatistics.get(question.uuid)
                                        .map(statisticResult => {
                                            return {
                                                "text": cutQuestionText(
                                                    LanguageHandling.getStringLocale(locale, question.fields.text)
                                                ),
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
                        (questionnaireData.fields.questiongroups)
                    })
                    .chain(questionGroups => {
                        return Future.parallel(
                            Infinity,
                            questionGroups
                        );
                    })
                    .mapRej(data => {
                        $scope.questionnaire = null;
                        $scope.statistics = null;
                        return data;
                    })
                    .fork(
                        ResultHandling.flashError($scope),
                        questionGroups => {
                            $scope.statistics = {
                                "questionGroups": questionGroups
                            };

                            $scope.properties.graph_height = R.pipe(
                                R.map(questionGroup => questionGroup.questions),
                                R.flatten,
                                R.length
                            )(questionGroups) * (
                                $scope.properties.bar_height +
                                $scope.properties.bar_padding
                            ) - $scope.properties.bar_padding;
                        }
                    );
            };

            let cutQuestionText = function (text) {
                let width = $scope.getTextWidth(text, "12pt Arial");
                let cuts = 0;
                while (width > ($scope.properties.graph_padding_left - 2 * $scope.properties.text_padding_left)) {
                    text = text.slice(0, -1);
                    width = $scope.getTextWidth(text, "12pt Arial");
                    cuts++;
                }
                if (cuts > 0) {
                    text = text.slice(0, -3);
                    return `${text}...`;
                }
                return text;
            };

            $scope.getX = function (value) {
                const maxValue = 11;
                const effectiveWidth = $scope.properties.graph_width - $scope.properties.graph_padding_left - $scope.properties.graph_padding_right;

                return $scope.properties.graph_padding_left + effectiveWidth * value / maxValue;
            };

            $scope.getY = function (index) {
                let result = $scope.properties.bar_padding;
                if (index !== 0) {
                    result += index * ($scope.properties.bar_height + $scope.properties.bar_padding)
                }
                return result;
            };

            /**
             * Uses canvas.measureText to compute and return the width of the given text of given font in pixels.
             *
             * @param {String} text The text to be rendered.
             * @param {String} font The css font descriptor that text is to be rendered with (e.g. "bold 14px verdana").
             *
             * @see https://stackoverflow.com/questions/118241/calculate-text-width-with-javascript/21015393#21015393
             */
            $scope.getTextWidth = function (text, font) {
                // re-use canvas object for better performance
                const canvas = $scope.getTextWidth.canvas || ($scope.getTextWidth.canvas = document.createElement("canvas"));
                const context = canvas.getContext("2d");
                context.font = font;
                const metrics = context.measureText(text);
                return metrics.width;
            };

            $scope.init();
        }])
    .config(["$routeProvider", "$locationProvider",
        function ($routeProvider, $locationProvider) {
            $locationProvider.hashPrefix("");
            $routeProvider
                .when("/", {
                    templateUrl: "/static/js/templates/Surveys.html",
                    controller: "SurveysController"
                })
                .when("/surveys/", {
                    templateUrl: "/static/js/templates/Surveys.html",
                    controller: "SurveysController"
                })
                .when("/surveys/:questionnaire/", {
                    templateUrl: "/static/js/templates/Questionnaire.html",
                    controller: "EditQuestionnaireController"
                })
                .when("/surveys/:questionnaire/statistic", {
                    templateUrl: "/static/js/templates/QuestionnaireStatistics.html",
                    controller: "QuestionnaireStatisticController"
                });
        }]);