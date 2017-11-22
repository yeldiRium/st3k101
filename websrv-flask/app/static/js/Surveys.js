angular.module('Surveys', ['ngRoute'])
    .factory('Surveys', ['$http', function($http) {
        return {
            query: function() {
                return $http.get('/api/surveys').then(
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
    .controller('SurveysController', ['$scope', '$http', 'Surveys',
        function($scope, $http, Surveys) {
            /**
             * Queries surveys and writes them into $scope.surveys.
             * If something goes wrong, $scope.error will be set.
             * @returns Promise
             */
            $scope.query = function() {
                return Surveys.query().then(
                    function(result) {
                        $scope.surveys = null;
                        $scope.error = null;
                        $scope.surveys = result;
                    },
                    function(error) {
                        $scope.surveys = null;
                        $scope.error = null;
                        $scope.error = error;
                    }
                );
            };

            $scope.resetEditing = function() {
                $scope.newForm = {
                    questionnaire: {
                        survey: null,
                        data: null
                    },
                    survey: {
                        data: null
                    }
                };
            };

            $scope.newQuestionnaire = function(survey) {
                $scope.resetEditing();
                $scope.newForm.questionnaire.survey = survey;
                $scope.newForm.questionnaire.data = {
                    name: "name",
                    description: "description"
                };
            };

            $scope.createQuestionnaire = function() {
                if (($scope.newForm.questionnaire.survey == null)
                    || $scope.newForm.questionnaire.data == null) {
                    return;
                }
                $http({
                    method: 'POST',
                    url: '/api/questionnaire',
                    data: JSON.stringify({
                        survey: $scope.newForm.questionnaire.survey.uuid,
                        questionnaire: {
                            name: $scope.newForm.questionnaire.data.name,
                            description: $scope.newForm.questionnaire.data.description
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
                                $scope.error = "Something went wrong. Please try again!";
                            }
                        },
                        function failure(error) {
                            $scope.error = error;
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