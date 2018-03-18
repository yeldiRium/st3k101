const angular = require("angular");
const R = require("ramda");
const RadarChart = require("radar-chart-d3");

require("angular-route");
require("angular-flash-alert");
require("./API");

angular.module("Statistics", ["ngRoute", "ngFlash", "API"])
    .config(["FlashProvider", function (FlashProvider) {
        FlashProvider.setTimeout(5000);
        FlashProvider.setShowClose(true);
    }])
    .controller("StatisticController", [
        "$scope", "$routeParams", "Questionnaires", "ResultHandling",
        "LanguageHandling",
        function ($scope, $routeParams, Questionnaires, ResultHandling,
                  LanguageHandling) {
            $scope.loading = "loading";

            Questionnaires.get($routeParams.questionnaire)
                .mapRej(error => {
                    $scope.$apply(() => {
                        $scope.loading = "error";
                    });
                    return error;
                })
                .fork(
                    ResultHandling.flashError($scope),
                    ({data: questionnaire, locale}) => {
                        $scope.$apply(() => {
                            $scope.questionnaire_uuid = $routeParams.questionnaire;
                            $scope.questionnaire = LanguageHandling.getQuestionnaireTranslation(locale, questionnaire);
                            $scope.loading = "done";
                        });
                    }
                )
        }])
    .controller("BoxPlotStatisticController", [
        "$scope", "$http", "$routeParams", "$timeout", "Questionnaires",
        "QuestionStatistics", "ResultHandling",
        function ($scope, $http, $routeParams, $timeout, Questionnaires,
                  QuestionStatistics, ResultHandling) {
            $scope.loading = "loading";

            $scope.properties = {
                "questionnaire_uuid": null,
                // see marginsof #content
                "graph_width": window.innerWidth * 0.76,
                // 2 * bar_padding as default
                "graph_height": 60,
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
                let questionnaire_uuid = $routeParams.questionnaire;
                QuestionStatistics.getWholeQuestionnaire(questionnaire_uuid)
                    .mapRej(data => {
                        $scope.$apply(() => {
                            $scope.questionnaire = null;
                            $scope.statistics = null;
                            $scope.loading = "error";
                            console.log($scope.properties.graph_width);
                        });
                        return data;
                    })
                    .fork(
                        ResultHandling.flashError($scope),
                        questionGroups => {
                            $scope.$apply(() => {
                                $scope.questionnaire_uuid = questionnaire_uuid;

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
                                ) + $scope.properties.bar_padding; // 2x bar_padding as outer padding
                                $scope.loading = "done";
                            })
                        }
                    );
            };

            $scope.cutQuestionText = function (text) {
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

            $scope.getY = function (groupIndex, questionIndex) {
                const index = R.pipe(
                    R.take(groupIndex),
                    R.map(R.prop("questions")),
                    R.map(R.length),
                    R.sum
                )($scope.statistics.questionGroups) + questionIndex;
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
    .controller("RadarChartStatisticController", [
        "$scope", "$routeParams", "QuestionStatistics", "ResultHandling",
        "LanguageHandling",
        function ($scope, $routeParams, QuestionStatistics, ResultHandling,
                  LanguageHandling) {
            $scope.loading = "loading";

            $scope.init = function () {
                let questionnaire_uuid = $routeParams.questionnaire;
                QuestionStatistics.getWholeQuestionnaire(questionnaire_uuid)
                    .mapRej(data => {
                        $scope.$apply(() => {
                            $scope.statistics = null;
                            $scope.loading = "error";
                        });
                        return data;
                    })
                    .fork(
                        ResultHandling.flashError($scope),
                        prepareSpiderChart
                    );
            };

            let prepareSpiderChart = function (questionGroups) {
                const data = R.pipe(
                    R.map(questionGroup => R.assoc(
                        "questions",
                        R.addIndex(R.map)(
                            (question, index) =>
                                R.objOf(
                                    R.concat(
                                        R.pipe(
                                            LanguageHandling.getDefaultStringLocale,
                                            R.head,
                                            R.toUpper
                                        )(questionGroup.name),
                                        R.toString(index + 1)
                                    ),
                                    question
                                ),
                            questionGroup.questions
                        ),
                        questionGroup
                    )),
                    R.map(R.prop("questions")),
                    R.flatten,
                    R.mergeAll,
                    R.mapObjIndexed((value, key, obj) => ({
                        "axis": key,
                        "value": R.path(["statistic", "q2"], value)
                    })),
                    R.values,
                    values => [{
                        "className": "results",
                        "axes": values
                    }]
                )
                (questionGroups);
                $scope.$apply(() => {
                    $scope.questionnaire_uuid = $routeParams.questionnaire;
                    $scope.loading = "done";
                    setTimeout(() => RadarChart.draw(".chart-container", data, {
                        w: 700,
                        levels: 11
                    }), 0);
                })
            };

            $scope.init();
        }
    ])
    .config(["$routeProvider", "$locationProvider",
        function ($routeProvider, $locationProvider) {
            $locationProvider.hashPrefix("");
            $routeProvider
                .when("/surveys/:questionnaire/statistic", {
                    templateUrl: "/static/js/templates/Statistics.html",
                    controller: "StatisticController"
                })
                .when("/surveys/:questionnaire/statistic/boxplot", {
                    templateUrl: "/static/js/templates/BoxPlotStatistics.html",
                    controller: "BoxPlotStatisticController"
                })
                .when("/surveys/:questionnaire/statistic/radarchart", {
                    templateUrl: "/static/js/templates/RadarChartStatistics.html",
                    controller: "RadarChartStatisticController"
                });
        }]);