<template>
    <div class="question"
         :class="classes"
    >
        <ListItem :text="question.text"
                  class="question__title"
                  :ellipseText="!expanded"
                  :mini="true"
                  :disabled="!isEditable(question)"
                  @edit="updateQuestionText"
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
                            :language-data="question.languageData"
                            @choose-language="changeLanguage"
                            @choose-language-unavailable="addNewTranslation"
            />
            <IconReorder class="list-item__icon"
                         v-if="draggable"
            />
        </ListItem>

        <div class="question__body"
             v-if="expanded"
             ref="dropdown"
        >
            <ReferenceCounter :object="question"
                              v-if="question.isConcrete"
            />
            <template>
                <RangeEditor :value="question.range"
                             @input="updateRange"
                             v-if="isOwnedByCurrentDataClient(question) && question.isConcrete"
                />
                <Range :range="question.range"
                       :preview="true"
                       v-else
                />
            </template>
        </div>
        <div class="question__buttons"
             v-if="expanded"
        >
            <Button v-if="isDeletable(question)"
                    @click="deleteQuestion"
            >
                delete
            </Button>
        </div>
    </div>
</template>

<script>
    import {Question} from "../../../model/SurveyBase/Question";

    import {fetchTranslation, setRange, setText} from "../../../api/Question";

    import SurveyBase from "./SurveyBase";
    import ListItem from "../List/Item";
    import LanguagePicker from "../LanguagePicker";
    import ReferenceCounter from "./Config/ReferenceCounter";
    import RangeEditor from "./Config/RangeEditor";
    import Range from "./Config/RangeSVG";
    import Button from "../Form/Button";

    import IconReorder from "../../../assets/icons/baseline-reorder-24px.svg";
    import IconExpandLess from "../../../assets/icons/baseline-expand_less-24px.svg";
    import IconExpandMore from "../../../assets/icons/baseline-expand_more-24px.svg";

    export default {
        name: "Question",
        extends: SurveyBase,
        components: {
            ListItem,
            LanguagePicker,
            ReferenceCounter,
            RangeEditor,
            Range,
            Button,
            IconReorder,
            IconExpandMore,
            IconExpandLess
        },
        props: {
            /** @type {Question} */
            question: {
                type: Question
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
        created() {
            this.expanded = this.initiallyExpanded;
        },
        computed: {
            classes() {
                return {
                    "question--disabled": !this.isEditable(this.question)
                }
            }
        },
        methods: {
            toggleExpanded() {
                this.expanded = !this.expanded;
            },
            /**
             * Switch the Question to the given language.
             * @param {Language} language
             */
            changeLanguage(language) {
                this.$load(
                    fetchTranslation(this.question, language)
                ).fork(
                    this.$handleApiError,
                    console.log
                );
            },
            /**
             * Add a new translation to the Question.
             * This means set new field values via API for the given languages
             * and then fetch the question anew in the now existing language.
             * @param language
             */
            addNewTranslation(language) {
                // TODO: clarify, when this should be available
                // TODO: display dialog which asks for data
                const text = "tbd";

                this.$load(
                    setText(this.question, language, text)
                        .chain(() => this.changeLanguage(language))
                ).fork(
                    this.$handleApiError,
                    console.log
                );
            },
            updateQuestionText(text) {
                if (!this.isEditable(this.question)) {
                    return;
                }
                this.$load(
                    setText(
                        this.question,
                        this.question.languageData.currentLanguage,
                        text
                    )
                ).fork(
                    this.$handleApiError,
                    console.log
                );
            },
            updateRange(range) {
                if (!this.isEditable(this.question)) {
                    return;
                }
                this.$load(
                    setRange(this.question, range)
                ).fork(
                    this.$handleApiError,
                    console.log
                );
            },
            /**
             * Asks for confirmation, if the Question should be deleted, and
             * emits an event which commands to do so, if the users confirms.
             */
            deleteQuestion() {
                this.$modal.show(
                    "dialog",
                    {
                        title: `Really delete Question?`,
                        text: `Do you really want to delete Question "${this.question.name}"?`,
                        buttons: [
                            {
                                text: "Cancel"
                            },
                            {
                                text: "Confirm",
                                handler: () => this
                                    .$emit("question-delete", this.question),
                                default: true
                            }
                        ]
                    }
                )
            }
        }
    }
</script>

<style lang="scss">
    @import "../../scss/_variables";

    .question {
        display: flex;
        flex-flow: column;

        background-color: $primary-light;

        &--disabled {
            background-color: $lighter;
        }

        &--bordered {
            border: 1px solid $primary;

            &.question--disabled {
                border-color: $slightlylight;
            }
        }

        &__body {
            width: 80%;
            align-self: center;

            display: flex;
            flex-flow: column;
            align-items: center;

            > * {
                width: 100%;
                text-align: center;
                margin-top: 8px;
                margin-bottom: 8px;
            }

            .reference-counter {
                margin-bottom: 8px;
            }

        }

        &__buttons {
            display: flex;
            justify-content: center;

            margin-bottom: 8px;

            .button {
                margin: 0 8px 0 8px;
            }
        }
    }
</style>
