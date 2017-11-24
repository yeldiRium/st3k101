angular.module('Surveys', ['ngRoute'])
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
    .controller('SurveysController', ['$scope', '$http', '$timeout', 'Surveys',
        function($scope, $http, $timeout, Surveys) {
            /**
             * Queries surveys and writes them into $scope.surveys.
             * If something goes wrong, $scope.error will be set.
             * @returns Promise
             */
            $scope.query = function() {
                return Surveys.query().then(
                    function(result) {
                        $scope.error = null;
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
                        $scope.templates = [];
                        $scope.error = error;
                    }
                );
            };

            $scope.showError = function(message) {
                $scope.error = message;
                $timeout(function() {
                    $scope.error = null;
                }, 3000);
            };

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

            $scope.newQuestionnaire = function(survey) {
                $scope.resetEditing();
                $scope.new.questionnaire.survey = survey;
                $scope.new.questionnaire.data = {
                    name: "name",
                    description: "description",
                    template: null
                };
            };

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
                                && result.data.result == "Questionnaire created.") {
                                $scope.resetEditing();
                                $scope.query();
                            } else {
                                $scope.showError("Something went wrong. Please try again!");
                            }
                        },
                        function failure(error) {
                            $scope.showError(error);
                        }
                    )
            };

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
                        $scope.query();
                    },
                    function fail(results) {}
                );
            };

            $scope.newSurvey = function() {
                $scope.resetEditing();
                $scope.new.survey.data = {
                    name: "name"
                }
            };

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
                                $scope.query();
                            } else {
                                $scope.showError("Something went wrong. Please try again!");
                            }
                        },
                        function failure(error) {
                            $scope.showError(error);
                        }
                    )
            };

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
                    },
                    function fail(error) {
                        $scope.showError("Survey could not be deleted. Please try again.");
                    }
                )
            };

            $scope.resetEditing();
            $scope.query();
        }])
    .controller('EditQuestionnaireController', ['$scope', '$http', '$timeout', '$routeParams', 'Questionnaire',
        function($scope, $http, $timeout, $routeParams, Questionnaire) {
            $scope.query = function() {
                Questionnaire.query($routeParams.questionnaire).then(
                    function success(result) {
                        $scope.error = null;
                        $scope.questionnaire = result;
                    },
                    function fail(error) {
                        $scope.questionnaire = null;
                        $scope.error = error;
                    }
                )
            };

            $scope.showError = function(message) {
                $scope.error = message;
                $timeout(function() {
                    $scope.error = null;
                }, 3000);
            };

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

            $scope.newQuestion = function(questiongroup) {
                $scope.resetEditing();
                $scope.new.question.questionGroup = questiongroup;
                $scope.new.question.data = {
                    text: "text"
                };
            };

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
                                && result.data.result == "Question created.") {
                                $scope.resetEditing();
                                $scope.query();
                            } else {
                                $scope.showError("Something went wrong. Please try again!");
                            }
                        },
                        function failure(error) {
                            $scope.showError(error);
                        }
                    )
            };

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
                        $scope.query();
                    },
                    function fail(results) {}
                );
            };

            $scope.newQuestionGroup = function() {
                $scope.resetEditing();
                $scope.new.questionGroup.data = {
                    name: "name"
                }
            };

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
                                && result.data.result == "QuestionGroup created.") {
                                $scope.resetEditing();
                                $scope.query();
                            } else {
                                $scope.showError("Something went wrong. Please try again!");
                            }
                        },
                        function failure(error) {
                            $scope.showError(error);
                        }
                    )
            };

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
                        $scope.questionnaire.fields.questiongroups.splice(
                            $scope.questionnaire.fields.questiongroups.indexOf(questionGroup),
                            1
                        );
                    },
                    function fail(error) {
                        $scope.showError("QuestionGroup could not be deleted. Please try again.");
                    }
                )
            };

            $scope.resetEditing();
            $scope.query();
        }])
    .config(['$routeProvider', '$locationProvider',
        function($routeProvider, $locationProvider) {
            $locationProvider.hashPrefix('');
            $routeProvider
                .when('/surveys/', {
                    templateUrl: '/static/js/templates/Surveys.html',
                    controller: 'SurveysController'
                })
                .when('/surveys/:questionnaire/', {
                    templateUrl: '/static/js/templates/EditSurvey.html',
                    controller: 'EditQuestionnaireController'
                });
        }]);