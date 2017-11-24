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
    .controller('EditSurveyController', ['$scope',
        function($scope) {

        }])
    .config(['$routeProvider', '$locationProvider',
        function($routeProvider, $locationProvider) {
            $locationProvider.hashPrefix('');
            $routeProvider
                .when('/surveys/', {
                    templateUrl: '/static/js/templates/Surveys.html',
                    controller: 'SurveysController'
                })
                .when('/surveys/:surveyID/', {
                    templateUrl: '/static/js/templates/EditSurvey.html',
                    controller: 'EditSurveyController'
                });
        }]);