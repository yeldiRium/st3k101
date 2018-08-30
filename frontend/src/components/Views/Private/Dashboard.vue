<template>
    <div class="dashboard">
        <div v-for="questionnaire in myQuestionnaires"
             class="dashboard__questionnaire"
        >
            <span class="dashboard__questionnaire__title">
                {{ questionnaire.name }}
            </span>
            <table class="dashboard__questionnaire__general-info">
                <tr v-if="questionnaire.description.length > 0">
                    <td>Description:</td>
                    <td>{{ questionnaire.description }}</td>
                </tr>
                <tr>
                    <td>Total number of submissions:</td>
                    <td>{{ submissionCount(questionnaire) }}</td>
                </tr>
            </table>
            <div class="dashboard__questionnaire__body">
                <div v-for="dimension in questionnaire.dimensions"
                     class="dashboard__dimension"
                >
                    <div class="dashboard__dimension__chart">
                        <span class="chart-title">
                            {{ dimension.name }}
                        </span>
                        <RadarChart :title="dimension.name"
                                    :questionStatistics="statisticsByDimension(dimension)"
                                    :truncateAfter="16"
                                    v-if="showGraphFor(dimension)"
                        />
                        <div v-else
                             class="chart-placeholder"
                        >
                            There are no answers for this dimension yet.
                        </div>
                        <TrackerEntries :surveyBase="dimension"
                                        :recurse="true"
                                        class="collapsible--no-border collapsible--border-top"
                        ></TrackerEntries>
                        <!--TrackerEntries v-for="question in dimension"
                                :surveyBase="question"></TrackerEntries
                                TODO: make trackerentries accept list of surveybases
                                -->
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import {mapGetters} from "vuex-fluture";
    import {Future} from "fluture";
    import {map, prop, reject, isNil} from "ramda";

    import RadarChart from "../../Partials/Graph/RadarChart";
    import TrackerEntries from "../../Partials/SurveyBase/TrackerEntries";

    export default {
        components: {
            RadarChart,
            TrackerEntries
        },
        computed: {
            ...mapGetters("questionnaires", ["myQuestionnaires"]),
            ...mapGetters("statistics", ["statisticByQuestionHref"]),
            submissionCount() {
               return (questionnaire) => {
                   if (questionnaire.dimensions.length < 1) {
                       return 0;
                   }
                   return this.statisticsByDimension(questionnaire.dimensions[0])[0].n;
               };
            },
        },
        created() {
            this.loadData();
        },
        methods: {
            showGraphFor(dimension) {
                if (dimension.questions.length < 1) {
                    return false;
                }
                return this.statisticsByDimension(dimension)[0].n > 0;
            },
            statisticsByDimension(dimension) {
                return reject(
                    isNil,
                    map(
                        (href) => this.statisticByQuestionHref(href),
                        map(prop('href'), dimension.questions)
                    )
                );
            },
            loadData() {
                return this.$load(
                    this.$store.dispatch("questionnaires/loadMyQuestionnaires")
                        .chain(this.loadStatistics)
                ).fork(
                    this.$handleApiError,
                    () => {
                    }
                )
            },
            loadStatistics() {
                let futures = [];
                for (let questionnaire of this.myQuestionnaires) {
                    for (let dimension of questionnaire.dimensions) {
                        for (let question of dimension.questions) {
                            futures.push(
                                this.$store.dispatch("statistics/fetchQuestionStatistic", {question})
                            );
                        }
                    }
                }
                return Future.parallel(Infinity, futures);
            }
        }
    }
</script>

<style lang="scss">
    @import "../../scss/variables";

    .dashboard {
        display: flex;
        flex-direction: column;
        width: 98%;
        margin: 0 auto 0 auto;

        &__questionnaire {
            border: $primary 1px solid;
            display: flex;
            flex-direction: column;
            margin: 1em 0 1em 0;
            min-width: 210px;

            -webkit-box-shadow: -1px 6px 25px 9px rgba(0,0,0,0.22);
            -moz-box-shadow: -1px 6px 25px 9px rgba(0,0,0,0.22);
            box-shadow: -1px 6px 25px 9px rgba(0,0,0,0.22);

            &__title {
                background-color: $primary-light;
                //height: 3em;
                padding: 1em;
            }

            &__general-info {
                width: 80vw;
                padding-top: 1em;
                margin: auto;
            }

            &__body {
                margin-top: 1em;
                width: 100%;
                display: flex;
                flex-direction: row;
                align-items: stretch;
                flex-wrap: wrap;
                justify-content: space-evenly;
            }
        }

        &__dimension {
            display: block;
            position: center;
            margin-bottom: 1em;

            &__chart {
                background-color: $primary-light;
                border: $primary 1px solid;
                border-radius: 5px;
                display: flex;
                flex-direction: column;
                width: 80vw;
                min-width: 250px;
            }
        }

        .chart-title {
            text-align: center;
            padding: 0 auto 0 auto;
            border-bottom: $primary 1px solid;
        }
    }

    @media (min-width: 1000px) {
        .dashboard__dimension__chart {
            width: 38vw;
        }
    }

    .chart-placeholder {
        text-align: center;
        background-color: $lighter;
        padding: 2em 0 2em 0;
    }
</style>
