<template>
    <div class="submission"
         :style="itemStyle"
    >
        <div v-if="submissionQuestionnaire !== null"
             class="submission__questionnaire"
        >
            <span class="submission__questionnaire__header">
                <span>{{ submissionQuestionnaire.name }}</span>
                <LanguagePicker
                        :language-data="submissionQuestionnaire.languageData"
                        :hideUnused="true"
                        :useLongNames="true"
                        @choose-language="changeLanguage"
                />
            </span>
            <div class="submission__questionnaire__body">
                <div class="submission__questionnaire__description"
                     v-if="submissionQuestionnaire.description.length > 0"
                >
                    {{submissionQuestionnaire.description}}
                </div>

                <div class="submission__questionnaire__dimension-head">
                    <div class="submission__questionnaire__dimension-head__item"
                         v-for="dimension in submissionQuestionnaire.dimensions"
                         @click.prevent="selectedDimensionId = dimension.id"
                         v-bind:class="{'submission__questionnaire__dimension-head__item-selected': selectedDimensionId === dimension.id}"
                    >
                        {{ dimension.name }}
                    </div>
                </div>
                <div class="submission__questionnaire__body__dimension">
                    <DimensionForm
                            v-for="dimension in submissionQuestionnaire.dimensions"
                            v-show="selectedDimensionId === dimension.id"
                            :dimension="dimension"
                            :key="dimension.href"
                            @response-change="updateResponseValue($event)"
                    />
                </div>
            </div>
            <div class="submission__footer">
                <label>
                    <span>Email Address</span>
                    <input type="email"
                           v-model="inputData.email"
                    />
                </label>

                <label v-if="submissionQuestionnaire.passwordEnabled">
                    <span>Password</span>
                    <input type="password"
                           v-model="inputData.password">
                </label>

                <Button @click="submit"
                        :class="{'button--grey': !isReadyToSubmit}"
                >
                    <span v-if="isReadyToSubmit">Submit</span>
                    <span v-else>Please complete the survey to submit.</span>
                </Button>
            </div>
        </div>
    </div>
</template>

<script>
    import {mapState} from "vuex-fluture";
    import {findIndex, equals} from "ramda";

    import DimensionForm from "../../Partials/SurveyBase/Submission/DimensionForm";
    import Button from "../../Partials/Form/Button";
    import LanguagePicker from "../../Partials/LanguagePicker"
    import {submitResponse} from "../../../api/Submission";

    export default {
        name: "SurveyForSubmission",
        components: {
            Button,
            DimensionForm,
            LanguagePicker
        },
        data() {
            return {
                submissionQuestionnaire: null,
                inputData: {
                    password: "",
                    email: ""
                },
                selectedDimensionId: null,
            };
        },
        computed: {
            ...mapState("global", ["window"]),
            itemStyle() {
                let width = "1200px";
                if (this.window.width * .8 < 1200) {
                    width = "80%";
                }

                return {
                    width: width
                };
            },
            questionnaireId() {
                return Number(this.$route.params.id);
            },
            isReadyToSubmit() {
                if (this.inputData.email.length < 6) {
                    return false; // a@b.de ==> 6 chars
                }
                if (this.inputData.email.includes("@") === false) {
                    return false;
                }
                if (this.submissionQuestionnaire.passwordEnabled
                    && this.inputData.password.length < 1
                ) {
                    return false;
                }
                for (let dimension of this.submissionQuestionnaire.dimensions) {
                    for (let question of dimension.questions) {
                        if (question.value < 0) {
                            return false;
                        }
                    }
                }
                return true;
            }
        },
        methods: {
            /**
             * Loads SubmissionQuestionnaire into vuex store and returns
             * Future of result.
             *
             * @param {Language} language
             * @returns {Future}
             */
            loadQuestionnaire(language = null) {
                return this.$load(
                    this.$store.dispatch(
                        "submission/fetchSubmissionQuestionnaireById",
                        {
                            id: this.questionnaireId,
                            language: language
                        }
                    )
                );
            },
            /**
             * Updates response value for given questionId in component state.
             *
             * @param {Integer} questionId
             * @param {Integer} value
             */
            updateResponseValue({questionId, value}) {
                for (let dimension of this.submissionQuestionnaire.dimensions) {
                    for (let question of dimension.questions) {
                        if (question.id === questionId) {
                            question.value = value;
                        }
                    }
                }
            },
            /**
             * Reloads SubmissionQuestionnaire in given language.
             * Updates component state to keep answers.
             *
             * @param {Language} language
             */
            changeLanguage(language) {
                this.loadQuestionnaire(language).fork(
                    this.$handleApiError,
                    questionnaire => {
                        this.submissionQuestionnaire = this.reconstructState(questionnaire);
                    }
                );
            },
            /**
             * Copies over answer values from current component state to
             * newQuestionnaire.
             *
             * @param {SubmissionQuestionnaire} newQuestionnaire
             * @returns {SubmissionQuestionnaire}
             */
            reconstructState(newQuestionnaire) {
                const previousState = this.submissionQuestionnaire;
                for (let prevDimension of previousState.dimensions) {
                    let dimensionIndex = findIndex(
                        equals(prevDimension),
                        newQuestionnaire.dimensions
                    );
                    if (dimensionIndex < 0) {
                        continue;  // skip, dimension was removed
                    }
                    let newDimension = newQuestionnaire.dimensions[dimensionIndex];
                    for (let prevQuestion of prevDimension.questions) {
                        let questionIndex = findIndex(
                            equals(prevQuestion),
                            newDimension.questions
                        );
                        if (questionIndex < 0) {
                            continue;  // skip, question was removed
                        }
                        newDimension.questions[questionIndex].value = prevQuestion.value;
                    }
                }
                return newQuestionnaire;
            },
            /**
             * Submits response values to API.
             */
            submit() {
                if (!this.isReadyToSubmit) {
                    return;
                }
                this.$load(
                    submitResponse(this.submissionQuestionnaire, this.inputData)
                ).fork(
                    this.$handleApiError,
                    console.log
                );
            }
        },
        created() {
            this.loadQuestionnaire().fork(
                this.$handleApiError,
                questionnaire => {
                    this.submissionQuestionnaire = questionnaire;
                    if (questionnaire.dimensions.length > 0) {
                        this.selectedDimensionId = questionnaire.dimensions[0].id;
                    }
                }
            );
        }
    }
</script>

<style lang="scss">
    @import "../../scss/variables";

    .submission {
        margin-left: auto;
        margin-right: auto;
        margin-top: 2em;

        &__questionnaire {
            &__header {
                display: flex;
                background-color: $primary-light;
                justify-content: space-between;
                padding: 1em;
                align-items: center;
            }

            &__description {
                margin-bottom: 2em;
            }

            &__body {
                padding: 1em;
                border: $primary-light 1px solid;

                &__dimension {
                    border: $primary-light 1px solid;
                    padding: 1em;
                }
            }

            &__dimension-head {
                display: flex;
                flex-direction: row;
                flex-wrap: wrap;

                &__item {
                    display: block;
                    border: $slightlylight 1px solid;
                    background-color: $lighter;
                    padding-left: 1em;
                    padding-right: 1em;
                    flex-grow: 1;
                    word-break: break-word;

                    &-selected {
                        background-color: $primary-light;
                        border: $primary-light 1px solid;
                    }
                }
            }
        }

        &__footer {
            display: flex;
            flex-direction: column;
            margin-top: 2em;
            padding: 1em;
            border: $primary-light 1px solid;

            label {
                display: flex;
                justify-content: space-between;
                margin-bottom: 1em;

                input {
                    width: 45%;
                }
            }
        }

    }
</style>
