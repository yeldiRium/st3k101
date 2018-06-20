<template>
    <div class="dimension"
         :class="classes"
    >
        <ListItem class="dimension__title"
                  :text="dimension.name"
                  :subtext="subtext"
                  :mini="expanded"
                  :ellipseText="!expanded"
                  :disabled="!isEditable(dimension)"
                  @edit="updateDimensionName"
        >
            <template>
                <IconExpandLess class="list-item__icon"
                                v-if="expanded"
                                @click.native="toggleExpanded"
                />
                <IconExpandMore class="list-item__icon"
                                v-else
                                @click.native="toggleExpanded"
                />
            </template>
            <LanguagePicker class="list-item__language-picker"
                            :language-data="dimension.languageData"
                            @choose-language="changeLanguage"
                            @choose-language-unavailable="addNewTranslation"
            />
            <IconReorder class="list-item__icon"
                         v-if="draggable"
            />
        </ListItem>

        <div class="dimension__body"
             v-if="expanded"
             ref="dropdown"
        >
            <ReferenceCounter :object="dimension"
                              v-if="dimension.isConcrete"
            />

            <Toggle :value="dimension.randomizeQuestions"
                    :disabled="!isOwnedByCurrentDataClient(dimension)"
                    @input="updateRandomizeQuestions"
            >
                <template slot="off">
                    in order
                </template>
                <template slot="on">
                    randomize
                </template>
            </Toggle>

            <div class="dimension__questions">
                <Question class="question--bordered"
                          v-for="question in dimension.questions"
                          :key="question.href"
                          :question="question"
                          :deletable="dimension.isConcrete"
                          @question-delete="deleteQuestion"
                />

            </div>
        </div>
        <div class="dimension__buttons"
             v-if="expanded"
        >
            <Button v-if="isEditable(dimension)"
                    @click="openNewQuestionDialog"
            >
                Add new Question
            </Button>
            <Button v-if="isDeletable(dimension)"
                    @click="deleteDimension"
            >
                delete
            </Button>
        </div>
    </div>
</template>

<script>
    import {mapState} from "vuex";
    import {without} from "ramda";

    import {Dimension} from "../../../model/SurveyBase/Dimension";

    import {
        addConcreteQuestion,
        fetchTranslation,
        removeQuestion,
        setName,
        setRandomizeQuestions
    } from "../../../api2/Dimension";

    import SurveyBase from "./SurveyBase";
    import Question from "./Question";
    import ListItem from "../List/Item";
    import LanguagePicker from "../LanguagePicker";
    import ReferenceCounter from "./Config/ReferenceCounter";
    import Toggle from "../Form/ToggleButton";
    import Button from "../Form/Button";

    import IconExpandLess from "../../../assets/icons/baseline-expand_less-24px.svg";
    import IconExpandMore from "../../../assets/icons/baseline-expand_more-24px.svg";
    import IconReorder from "../../../assets/icons/baseline-reorder-24px.svg";

    export default {
        name: "Dimension",
        extends: SurveyBase,
        components: {
            ListItem,
            Question,
            LanguagePicker,
            ReferenceCounter,
            Toggle,
            Button,
            IconReorder,
            IconExpandLess,
            IconExpandMore
        },
        props: {
            /** @type {Dimension} */
            dimension: {
                type: Dimension
            },
            initiallyExpanded: {
                type: Boolean,
                default: false
            }
        },
        data() {
            return {
                expanded: false,
                header: {
                    height: 0
                },
                dropdown: {
                    height: 0
                }
            }
        },
        computed: {
            ...mapState("session", ["dataClient"]),
            classes() {
                return {
                    "dimension--disabled": !this.isEditable(this.dimension)
                }
            },
            /**
             * Returns a message displaying the number of Questions in the Di-
             * mension.
             *
             * @returns {string}
             */
            subtext() {
                return `Contains ${this.dimension.questions.length} questions.`;
            }
        },
        methods: {
            toggleExpanded() {
                this.expanded = !this.expanded;
            },
            /**
             * Switch the Dimension to the given language.
             * @param {Language} language
             */
            changeLanguage(language) {
                this.$load(
                    fetchTranslation(this.dimension, language)
                ).fork(
                    this.$handleApiError,
                    console.log
                );
            },
            /**
             * Add a new translation to the Dimension.
             * This means set new field values via API for the given languages
             * and then fetch the dimension anew in the now existing language.
             * @param language
             */
            addNewTranslation(language) {
                if (!this.isEditable(this.dimension)) {
                    return;
                }
                // TODO: display dialog which asks for data
                const name = "tbd";

                this.$load(
                    setName(this.dimension, language, name)
                        .chain(() => this.changeLanguage(language))
                ).fork(
                    this.$handleApiError,
                    console.log
                );
            },
            updateDimensionName(name) {
                if (!this.isEditable(this.dimension)) {
                    return;
                }
                this.$load(
                    setName(
                        this.dimension,
                        this.dimension.languageData.currentLanguage,
                        name
                    )
                ).fork(
                    this.$handleApiError,
                    console.log
                );
            },
            updateRandomizeQuestions(randomizeQuestions) {
                this.$load(
                    setRandomizeQuestions(this.dimension, randomizeQuestions)
                ).fork(
                    this.$handleApiError,
                    console.log
                );
            },
            openNewQuestionDialog() {
                if (!this.isEditable(this.dimension)) {
                    return;
                }
                this.$modal.show(
                    "modal-create-question",
                    {
                        language: this.dimension.languageData.currentLanguage,
                        handler: this.createQuestion
                    }
                )
            },
            createQuestion({text, range}) {
                if (!this.isEditable(this.dimension)) {
                    return;
                }
                this.$load(
                    addConcreteQuestion(
                        this.dimension, this.dataClient, text, range
                    )
                ).fork(
                    this.$handleApiError,
                    console.log
                );
            },
            /**
             * Only handles removal from the dimension in reaction to Question
             * being deleted.
             */
            deleteQuestion(question) {
                if (!this.isEditable(this.dimension)) {
                    return;
                }
                this.$load(
                    removeQuestion(this.dimension, question)
                ).fork(
                    this.$handleApiError,
                    console.log
                );
            },
            /**
             * Asks for confirmation, if the Dimension should be deleted, and
             * emits event that commands to do so, if the users confirms.
             */
            deleteDimension() {
                this.$modal.show(
                    "dialog",
                    {
                        title: `Really delete Dimension?`,
                        text: `Do you really want to delete Dimension "${this.dimension.name}"?`,
                        buttons: [
                            {
                                text: "Cancel"
                            },
                            {
                                text: "Confirm",
                                handler: () => this
                                    .$emit("dimension-delete", this.dimension),
                                default: true
                            }
                        ]
                    }
                )
            }
        },
        created() {
            this.expanded = this.initiallyExpanded;
        }
    }
</script>

<style lang="scss">
    @import "../../scss/_variables";

    .dimension {
        display: flex;
        flex-flow: column;

        background-color: $primary-light;

        &--disabled {
            background-color: $lighter;
        }

        &--bordered {
            border: 1px solid $primary;

            &.dimension--disabled {
                border-color: $slightlylight;
            }
        }

        &__add-question-button {
            background-color: $primary;
        }

        &__body {
            display: flex;
            flex-flow: column;
            align-items: center;

            > * {
                width: 95%;
                margin-top: 8px;
                margin-bottom: 8px;
            }

            > *:not(.dimension__questions) {
                text-align: center;
            }
        }

        &__questions {
            display: flex;
            flex-flow: column;
        }

        &__buttons {
            display: flex;
            justify-content: center;

            margin-bottom: 8px;

            .button {
                margin: 0 8px 0 8px;
            }
        }

        .toggle-button {
            > div {
                color: $darker;
            }

            &--off-side.toggle-button__off-side--active,
            &--on-side.toggle-button__on-side--active {
                color: $verydark;
            }
        }
    }
</style>
