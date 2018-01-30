angular.module('Surveys', ['ngRoute', 'ngFlash'])
    .config(['FlashProvider', function(FlashProvider) {
        FlashProvider.setTimeout(5000);
        FlashProvider.setShowClose(true);
    }])
    .factory('Surveys', ['$http', function($http) {
        return {
            query: function() {
                return $http.get('/api/survey').then(
                    function(result) {
                        return new Promise(function(resolve, reject) {
                            resolve(result.data);
                        });
                    },
                    function(error) {
                        return new Promise(function(resolve, reject) {
                            reject(error);
                        });
                    }
                );
            }
        }
    }])
    .factory('Questionnaire', ['$http', function($http) {
        return {
            query: function(uuid) {
                return $http.get('/api/questionnaire/' + uuid).then(
                    function success(result) {
                        return new Promise(function(resolve, reject) {
                            resolve(result.data);
                        })
                    },
                    function fail(error) {
                        return new Promise(function(resolve, reject) {
                            reject(error);
                        });
                    }
                )
            }
        }
    }])
    .factory('QuestionStatistic', ['$http', function($http) {
        return {
            query: function(uuid) {
                return $http.get('/api/question/' + uuid + '/statistic').then(
                    function success(result) {
                        return new Promise(function(resolve, reject) {
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
                        return new Promise(function(resolve, reject) {
                            reject(error);
                        });
                    }
                )
            }
        }
    }])
    .controller('SurveysController', ['$scope', '$http', '$timeout', 'Flash', 'Surveys',
        function($scope, $http, $timeout, Flash, Surveys) {
            /**
             * Queries surveys and writes them into $scope.surveys.
             * If something goes wrong, $scope.error will be set.
             * @returns Promise
             */
            $scope.query = function() {
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
                return Surveys.query().then(
                    function(result) {
                        $scope.surveys = result;
                        $scope.templates = [
                            {
                                value: null,
                                name: 'You can optionally create a questionnaire from a template. Select one here.'
                            },
                            {
                                value: 'efla_teacher',
                                name: 'EFLA Teacher'
                            },
                            {
                                value: 'efla_student',
                                name: 'EFLA Student'
                            }
                        ];
                        $.each(result, function(index, survey) {
                            if (survey.fields.questionnaires.length > 0) {
                                $scope.templates.push({
                                    value: null,
                                    name: '-- from Survey ' + survey.fields.name + ' --'
                                });
                                $.each(survey.fields.questionnaires, function(index, questionnaire) {
                                    $scope.templates.push({
                                        value: questionnaire.uuid,
                                        name: questionnaire.fields.name
                                    })
                                });
                            }
                        })
                    },
                    function(error) {
                        $scope.surveys = null;
                        Flash.create('danger', error.data.error);
                    }
                );
            };

            /**
             * Resets all editing forms and all temporary data.
             */
            $scope.resetEditing = function() {
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

                $scope.selection =  {
                    survey: null,
                    questionnaires: {},
                    count: 0
                };
            };

            /**
             * Navigates to the frontend view of a Questionnaire.
             * @param questionnaire
             */
            $scope.gotoQuestionnaire = function(questionnaire) {
                var url = '/survey/' + questionnaire.uuid;
                var win = window.open('/survey/' + questionnaire.uuid, '_blank');
                if (win) {
                    win.focus();
                } else {
                    Flash.create('danger', 'Tried to open the survey at "' + url + '", but the popup was blocked.');
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
            $scope.toggleSelect = function(survey, questionnaire) {
                if ($scope.selection.survey != survey) {
                    $scope.resetEditing();
                }
                $scope.selection.survey = survey;
                if ($scope.selection.questionnaires[questionnaire.uuid] == true) {
                    $scope.selection.questionnaires[questionnaire.uuid] = false;
                    $scope.selection.count--;
                } else {
                    $scope.selection.questionnaires[questionnaire.uuid] = true;
                    $scope.selection.count++;
                }
                if ($scope.selection.count == 0) {
                    $scope.resetEditing();
                }
            };

            /**
             * Opens a form for a new questionnaire by setting temporary data to
             * default values.
             * @param survey
             */
            $scope.newQuestionnaire = function(survey) {
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
            $scope.createQuestionnaire = function() {
                if (($scope.new.questionnaire.survey == null)
                    || $scope.new.questionnaire.data == null) {
                    return;
                }
                $http({
                    method: 'POST',
                    url: '/api/questionnaire',
                    data: JSON.stringify({
                        survey: $scope.new.questionnaire.survey.uuid,
                        questionnaire: {
                            name: $scope.new.questionnaire.data.name,
                            description: $scope.new.questionnaire.data.description,
                            template: $scope.new.questionnaire.data.template
                        }
                    }),
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })
                    .then(
                        function success(result) {
                            if (result.status == 200
                                && result.data.result == 'Questionnaire created.') {
                                $scope.resetEditing();
                                Flash.create('success', 'Questionnaire successfully created.');
                                $scope.query();
                            } else {
                                Flash.create('danger', result.data.error);
                            }
                        },
                        function failure(error) {
                            console.log(error)
                            Flash.create('danger', error.data.error);
                        }
                    )
            };

            /**
             * Sends delete requests for all currently selected questionnaires.
             * TODO: Error handling.
             */
            $scope.deleteQuestionnaires = function() {
                promises = [];
                $.each($scope.selection.questionnaires, function(uuid, shouldDelete) {
                    if (shouldDelete == true) {
                        promises.push(
                            $http({
                                method: 'DELETE',
                                url: '/api/questionnaire',
                                data: {
                                    uuid: uuid,
                                    survey: $scope.selection.survey.uuid
                                },
                                headers: {'Content-Type': 'application/json'}
                            })
                        );
                    }
                });
                Promise.waitAll(promises).then(
                    function success(results) {
                        $scope.resetEditing();
                        Flash.create('success', 'Questionnaire(s) successfully deleted.');
                        $scope.query();
                    },
                    function fail(results) {
                        Flash.create('danger', 'Something went wrong with one of the Questionnaires:');
                        $.each(results, function(index, result) {
                            if (result.status != 200) {
                                Flash.create('danger', results.data);
                            }
                        })
                    }
                );
            };

            /**
             * Opens a form for a new Survey by setting temporary data to
             * default values.
             */
            $scope.newSurvey = function() {
                $scope.resetEditing();
                $scope.new.survey.data = {
                    name: "name"
                }
            };

            /**
             * Sends a create request for a new Survey with the current tempora-
             * ry data.
             */
            $scope.createSurvey = function() {
                if ($scope.new.survey.data == null) {
                    return;
                }
                $http({
                    method: 'POST',
                    url: '/api/survey',
                    data: JSON.stringify({
                        name: $scope.new.survey.data.name
                    }),
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })
                    .then(
                        function success(result) {
                            if (result.status == 200
                                && result.data.result == "Survey created.") {
                                $scope.resetEditing();
                                Flash.create('success', 'Survey successfully created.');
                                $scope.query();
                            } else {
                                Flash.create('danger', result.data.error);
                            }
                        },
                        function failure(error) {
                            Flash.create('danger', error.data.error);
                        }
                    )
            };

            /**
             * Sends a delete request for a specific survey.
             * @param survey
             */
            $scope.deleteSurvey = function(survey) {
                $http({
                    method: 'DELETE',
                    url: '/api/survey',
                    data: {
                        uuid: survey.uuid
                    },
                    headers: {
                        'Content-Type': 'application/json'
                    }
                }).then(
                    function success(result) {
                        $scope.surveys.splice($scope.surveys.indexOf(survey), 1);
                        Flash.create('success', 'Survey successfully deleted.');
                    },
                    function fail(error) {
                        Flash.create('danger', 'Survey could not be deleted. Please try again.');
                    }
                )
            };

            $scope.resetEditing();
            $scope.query();
        }])
    .controller('EditQuestionnaireController', ['$scope', '$http', '$timeout', 'Flash', '$routeParams', 'Questionnaire',
        function($scope, $http, $timeout, Flash, $routeParams, Questionnaire) {
            /**
             * Queries the current questionnaire and stores its data.
             * If something goes wrong, an error message is displayed and
             * nothing else.
             */
            $scope.query = function() {
                Questionnaire.query($routeParams.questionnaire).then(
                    function success(result) {
                        $.each(result.fields.questiongroups, function(index, questiongroup) {
                            setTimeout(
                                function() {
                                    $('#colorPicker_' + questiongroup.uuid).spectrum({
                                        color: questiongroup.fields.color,
                                        change: function(color) {
                                            $scope.updateColor(color.toHexString(), questiongroup);
                                        }
                                    });
                                }, 0);
                            setTimeout(
                                function() {
                                    $('#textColorPicker_' + questiongroup.uuid).spectrum({
                                        color: questiongroup.fields.text_color,
                                        change: function(color) {
                                            $scope.updateTextColor(color.toHexString(), questiongroup);
                                        }
                                    });
                                }, 0);
                        });
                        $scope.questionnaire = result;
                    },
                    function fail(error) {
                        $scope.questionnaire = null;
                        Flash.create('danger', error.data.error);
                    }
                )
            };

            /**
             * Resets all editing forms and all temporary data.
             */
            $scope.resetEditing = function() {
                $scope.new = {
                    question: {
                        questionGroup: null,
                        data: null
                    },
                    questionGroup: {
                        data: null
                    }
                };

                $scope.selection =  {
                    questionGroup: null,
                    questions: {},
                    count: 0
                };
            };

            /**
             * Navigates to the frontend view of a Questionnaire.
             */
            $scope.gotoQuestionnaire = function() {
                var url = '/survey/' + $scope.questionnaire.uuid;
                var win = window.open('/survey/' + $scope.questionnaire.uuid, '_blank');
                if (win) {
                    win.focus();
                } else {
                    Flash.create('danger', 'Tried to open the questionnaire at "' + url + '", but the popup was blocked.');
                }
            };

            /**
             * Sends updates with current questionnaire data
             */
            $scope.updateQuestionnaire = function() {
                $http({
                    method: 'PUT',
                    url: '/api/questionnaire',
                    data: {
                        uuid: $scope.questionnaire.uuid,
                        name: $scope.questionnaire.fields.name,
                        description: $scope.questionnaire.fields.description
                    },
                    headers: {
                        'Content-Type': 'application/json'
                    }
                }).then(
                    function success(result) {
                        Flash.create('success', 'Questionnaire updated!');
                    },
                    function fail(error) {
                        Flash.create('danger', error.data.error);
                    }
                )
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
            $scope.toggleSelect = function(questionGroup, question) {
                if ($scope.selection.questionGroup != questionGroup) {
                    $scope.resetEditing();
                }
                $scope.selection.questionGroup = questionGroup;
                if ($scope.selection.questions[question.uuid] == true) {
                    $scope.selection.questions[question.uuid] = false;
                    $scope.selection.count--;
                } else {
                    $scope.selection.questions[question.uuid] = true;
                    $scope.selection.count++;
                }
                if ($scope.selection.count == 0) {
                    $scope.resetEditing();
                }
            };

            /**
             * Opens a form for a new Question by setting temporary data to
             * default values.
             */
            $scope.newQuestion = function(questiongroup) {
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
            $scope.createQuestion = function() {
                if (($scope.new.question.questionGroup == null)
                    || $scope.new.question.data == null) {
                    return;
                }
                $http({
                    method: 'POST',
                    url: '/api/question',
                    data: JSON.stringify({
                        questionnaire: $scope.questionnaire.uuid,
                        question_group: $scope.new.question.questionGroup.uuid,
                        text: $scope.new.question.data.text
                    }),
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })
                    .then(
                        function success(result) {
                            if (result.status == 200
                                && result.data.result == 'Question created.') {
                                $scope.resetEditing();
                                Flash.create('success', 'Question successfully created.');
                                $scope.query();
                            } else {
                                Flash.create('danger', result.data.error);
                            }
                        },
                        function failure(error) {
                            Flash.create('danger', error.data.error);
                        }
                    )
            };

            /**
             * Sends a delete request for each currently selected Question.
             * TODO: error handling
             */
            $scope.deleteQuestions = function() {
                promises = [];
                $.each($scope.selection.questions, function(uuid, shouldDelete) {
                    if (shouldDelete == true) {
                        promises.push(
                            $http({
                                method: 'DELETE',
                                url: '/api/question',
                                data: {
                                    questionnaire: $scope.questionnaire.uuid,
                                    question_group: $scope.selection.questionGroup.uuid,
                                    uuid: uuid
                                },
                                headers: {'Content-Type': 'application/json'}
                            })
                        );
                    }
                });
                Promise.waitAll(promises).then(
                    function success(results) {
                        $scope.resetEditing();
                        Flash.create('success', 'Question(s) successfully deleted.');
                        $scope.query();
                    },
                    function fail(results) {
                        Flash.create('danger', 'Something went wrong with one of the Questions:');
                        $.each(results, function(index, result) {
                            if (result.status != 200) {
                                Flash.create('danger', results.data);
                            }
                        })
                    }
                );
            };

            /**
             * Opens a form for a new QuestionGroup by setting temporary data to
             * default values.
             */
            $scope.newQuestionGroup = function() {
                $scope.resetEditing();
                $scope.new.questionGroup.data = {
                    name: "name"
                }
            };

            /**
             * Sends a create request for a new QuestionGroup with the current
             * temporary data.
             */
            $scope.createQuestionGroup = function() {
                if ($scope.new.questionGroup.data == null) {
                    return;
                }
                $http({
                    method: 'POST',
                    url: '/api/question_group',
                    data: JSON.stringify({
                        questionnaire: $scope.questionnaire.uuid,
                        name: $scope.new.questionGroup.data.name,
                    }),
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })
                    .then(
                        function success(result) {
                            if (result.status == 200
                                && result.data.result == 'QuestionGroup created.') {
                                $scope.resetEditing();
                                Flash.create('success', 'QuestionGroup successfully created.');
                                $scope.query();
                            } else {
                                Flash.create('danger', result.data.error);
                            }
                        },
                        function failure(error) {
                            Flash.create('danger', error.data.error);
                        }
                    )
            };

            /**
             * Sends a delete request for a specific QuestionGroup.
             */
            $scope.deleteQuestionGroup = function(questionGroup) {
                $http({
                    method: 'DELETE',
                    url: '/api/question_group',
                    data: {
                        uuid: questionGroup.uuid,
                        questionnaire: $scope.questionnaire.uuid
                    },
                    headers: {
                        'Content-Type': 'application/json'
                    }
                }).then(
                    function success(result) {
                        Flash.create('success', 'QuestionGroup successfully deleted.');
                        $scope.questionnaire.fields.questiongroups.splice(
                            $scope.questionnaire.fields.questiongroups.indexOf(questionGroup),
                            1
                        );
                    },
                    function fail(error) {
                        Flash.create('danger', 'QuestionGroup could not be deleted. Please try again.');
                    }
                )
            };

            $scope.updateColor = function(color, questionGroup) {
                $http({
                    method: 'PUT',
                    url: '/api/question_group',
                    data: {
                        uuid: questionGroup.uuid,
                        color: color
                    },
                    headers: {
                        'Content-Type': 'application/json'
                    }
                }).then(
                    function success(result) {
                        if (result.status == 200 && result.data.result == 'QuestionGroup updated.') {
                            questionGroup.fields.color = color;
                            Flash.create('success', 'QuestionGroup color was updated!');
                        } else {
                            Flash.create('danger', result.data.error);
                        }
                    },
                    function fail(error) {
                        Flash.create('danger', 'QuestionGroup color could not be updated. Please try again.');
                    }
                )
            };

            $scope.updateTextColor = function(color, questionGroup) {
                $http({
                    method: 'PUT',
                    url: '/api/question_group',
                    data: {
                        uuid: questionGroup.uuid,
                        text_color: color
                    },
                    headers: {
                        'Content-Type': 'application/json'
                    }
                }).then(
                    function success(result) {
                        if (result.status == 200 && result.data.result == 'QuestionGroup updated.') {
                            questionGroup.fields.text_color = color;
                            Flash.create('success', 'QuestionGroup text color was updated!');
                        } else {
                            Flash.create('danger', result.data.error);
                        }
                    },
                    function fail(error) {
                        Flash.create('danger', 'QuestionGroup text color could not be updated. Please try again.');
                    }
                )
            };

            $scope.resetEditing();
            $scope.query();
        }])
    .controller('QuestionnaireStatisticController', ['$scope', '$http', '$routeParams', '$timeout', 'Questionnaire', 'QuestionStatistic',
        function($scope, $http, $routeParams, $timeout, Questionnaire, QuestionStatistic) {
            $scope.properties = {
                'questionnaire_uuid': null,
                'graph_width': window.innerWidth - 400,
                'graph_height': 60, // 2 * bar_padding as default
                'graph_padding_left': 100,
                'graph_padding_right': 100,
                'text_padding_left': 5,
                'text_padding_right': 80,
                'bar_height': 50,
                'bar_padding': 30,
                'upper_scale_line_upper_y': '20',
                'upper_scale_line_lower_y': '25',
                'upper_scale_text_y': '15',
                'lower_scale_line_upper_y': '25',
                'lower_scale_line_lower_y': '20',
                'lower_scale_text_y': '5'
            };

            $scope.query = function() {
                Questionnaire.query($routeParams.questionnaire).then(
                    function success(result) {
                        $scope.statistics = {
                            'questionGroups': []
                        };
                        $scope.properties.questionnaire_uuid = result.uuid;
                        $.each(result.fields.questiongroups, function(index, questionGroup) {
                            var questionGroupObject = {
                                'name': questionGroup.fields.name,
                                'color': questionGroup.fields.color,
                                'text_color': questionGroup.fields.text_color,
                                'questions': []
                            };
                            $.each(questionGroup.fields.questions, function(index, question) {
                                var questionObject = {
                                    'text': $scope.cutQuestionText(question.fields.text),
                                    'answers': question.fields.results.length,
                                    'statistic': null
                                };
                                questionGroupObject.questions.push(questionObject);
                                console.log(questionObject);

                                QuestionStatistic.query(question.uuid).then(
                                    function success(result) {
                                        questionObject.statistic = result;
                                        if($scope.properties.graph_height == 0) {
                                            $scope.properties.graph_height += $scope.properties.bar_height;
                                        } else {
                                            $scope.properties.graph_height += $scope.properties.bar_height + $scope.properties.bar_padding;
                                        }
                                    },
                                    function fail(error) {
                                        Flash.create('danger', error.data.error);
                                    }
                                );
                            });
                            $scope.statistics.questionGroups.push(questionGroupObject);
                        });
                        setTimeout(function() {
                        }, 0);
                        console.log($scope.statistics);
                        return $scope.statistics;
                    },
                    function fail(error) {
                        $scope.questionnaire = null;
                        $scope.statistics = null;
                        Flash.create('danger', error.data.error);
                    }
                )
            };

            $scope.getX = function(value) {
                var maxValue = 11;
                var effectiveWidth = $scope.properties.graph_width - $scope.properties.graph_padding_left - $scope.properties.graph_padding_right;

                return $scope.properties.graph_padding_left + effectiveWidth * value / maxValue;
            };

            $scope.getY = function(index) {
                var result = $scope.properties.bar_padding;
                if(index != 0) {
                    result += index * ($scope.properties.bar_height + $scope.properties.bar_padding)
                }
                return result;
            };

            $scope.cutQuestionText = function(text) {
                var width = $scope.getTextWidth(text, "12pt Arial");
                var cuts = 0;
                while(width > ($scope.properties.graph_padding_left - 2 * $scope.properties.text_padding_left)) {
                    text = text.slice(0, -1);
                    width = $scope.getTextWidth(text, "12pt Arial");
                    cuts++;
                }
                if(cuts > 0) {
                    text = text.slice(0, -3);
                    return text + '...';
                }
                return text;
            };

            /**
             * Uses canvas.measureText to compute and return the width of the given text of given font in pixels.
             *
             * @param {String} text The text to be rendered.
             * @param {String} font The css font descriptor that text is to be rendered with (e.g. "bold 14px verdana").
             *
             * @see https://stackoverflow.com/questions/118241/calculate-text-width-with-javascript/21015393#21015393
             */
            $scope.getTextWidth = function(text, font) {
                // re-use canvas object for better performance
                var canvas = $scope.getTextWidth.canvas || ($scope.getTextWidth.canvas = document.createElement("canvas"));
                var context = canvas.getContext("2d");
                context.font = font;
                var metrics = context.measureText(text);
                return metrics.width;
            };

            $scope.query();
        }])
    .config(['$routeProvider', '$locationProvider',
        function($routeProvider, $locationProvider) {
            $locationProvider.hashPrefix('');
            $routeProvider
                .when('/', {
                    templateUrl: '/static/js/templates/Surveys.html',
                    controller: 'SurveysController'
                })
                .when('/surveys/', {
                    templateUrl: '/static/js/templates/Surveys.html',
                    controller: 'SurveysController'
                })
                .when('/surveys/:questionnaire/', {
                    templateUrl: '/static/js/templates/EditSurvey.html',
                    controller: 'EditQuestionnaireController'
                })
                .when('/surveys/:questionnaire/statistic', {
                    templateUrl: '/static/js/templates/QuestionnaireStatistics.html',
                    controller: 'QuestionnaireStatisticController'
                });
        }]);