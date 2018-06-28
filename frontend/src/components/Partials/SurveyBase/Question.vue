<template>
    <div class="question"
         :class="classes"
    >
        <ListItem :value="question.text"
                  class="question__title"
                  :ellipseText="!expanded"
                  :mini="true"
                  :disabled="!isEditable(question)"
                  @input="updateQuestionText"
        >
            <router-link :to="{name: 'AQuestion', params: {id: question.id}}">
                <IconLink class="list-item__icon"
                          v-if="showLink"
                />
            </router-link>
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
                            @choose-language-unavailable="openAddNewTranslationDialog"
            />
            <IconReorder class="list-item__icon"
                         v-if="draggable"
            />
        </ListItem>

        <div class="question__body"
             v-if="expanded"
             ref="dropdown"
        >
            <span class="questionnaire__table-label">
                References:
            </span>
            <ReferenceCounter :object="question"
                              v-if="question.isConcrete"
            />

            <span class="questionnaire__table-label">
                Range:
            </span>
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

    import {setRange, setText} from "../../../api/Question";

    import SurveyBase from "./SurveyBase";
    import ListItem from "../List/Item";
    import LanguagePicker from "../LanguagePicker";
    import ReferenceCounter from "./Config/ReferenceCounter";
    import RangeEditor from "./Config/RangeEditor";
    import Range from "./Config/RangeSVG";
    import Button from "../Form/Button";

    import IconLink from "../../../assets/icons/baseline-link-24px.svg";
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
            IconLink,
            IconReorder,
            IconExpandMore,
            IconExpandLess
        },
        props: {
            /** @type {Question} */
            question: {
                type: Question
            },
            /** @type {Boolean} */
            initiallyExpanded: {
                type: Boolean,
                default: false
            },
            showLink: {
                type: Boolean,
                default: true
            }
        },
        data() {
            return {
                /** @type {Boolean} */
                expanded: false
            }
        },
        created() {
            this.expanded = this.initiallyExpanded;
        },
        computed: {
            /**
             * CSS Classes for Question container div.
             */
            classes() {
                return {
                    "question--disabled": !this.isEditable(this.question)
                }
            }
        },
        methods: {
            /**
             * Toggle whether the Question is collapsed or expanded.
             */
            toggleExpanded() {
                this.expanded = !this.expanded;
            },
            /**
             * Switch the Question to the given language.
             * @param {Language} language
             */
            changeLanguage(language) {
                const cancel = this.$load(
                    this.$store.dispatch(
                        "questions/fetchQuestion",
                        {href: this.question.href, language}
                    )
                ).fork(
                    this.$handleApiError,
                    () => {
                    }
                );
            },
            /**
             * Opens a dialog for entering a new translation.
             *
             * @param {Language} language
             */
            openAddNewTranslationDialog(language) {
                if (!this.isEditable(this.question)) {
                    return;
                }
                this.$modal.show(
                    "modal-translate-question",
                    {
                        language,
                        handler: this.addNewTranslation,
                        text: this.question.text
                    }
                );
            },
            /**
             * Add a new translation to the Question.
             * This means set new field values via API for the given languages
             * and then fetch the question anew in the now existing language.
             *
             * @param {Language} language
             * @param {String} text
             */
            addNewTranslation({language, text}) {
                if (!this.isEditable(this.question)) {
                    return;
                }

                const cancel = this.$load(
                    this.$store.dispatch(
                        "questions/updateQuestion",
                        {
                            question: this.question,
                            language,
                            params: {
                                text
                            }
                        }
                    )
                        .chain(question => this.$store.dispatch(
                            "questions/fetchQuestion",
                            {href: question.href, language}
                        ))
                ).fork(
                    this.$handleApiError,
                    () => {
                    }
                );
            },
            /**
             * Update the question's text.
             *
             * @param {String} text
             */
            updateQuestionText(text) {
                if (!this.isEditable(this.question)) {
                    return;
                }
                const cancel = this.$load(
                    this.$store.dispatch(
                        "questions/updateQuestion",
                        {
                            question: this.question,
                            params: {
                                text
                            }
                        }
                    )
                ).fork(
                    this.$handleApiError,
                    () => {
                    }
                );
            },
            /**
             * Update the question's range.
             *
             * This is asynchronous, since the API is informed and then the
             * update is executed.
             *
             * @param {Range} range
             */
            updateRange(range) {
                if (!this.isEditable(this.question)) {
                    return;
                }
                const cancel = this.$load(
                    this.$store.dispatch(
                        "questions/updateQuestion",
                        {
                            question: this.question,
                            params: {
                                range
                            }
                        }
                    )
                ).fork(
                    this.$handleApiError,
                    () => {
                    }
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
            padding: 0.5em 2em 0.5em 0;

            display: grid;
            grid-template-columns: minmax(max-content, 1fr) 5fr;
            grid-row-gap: 0.5em;
            align-items: center;

            > * {
                text-align: center
            }

        }

        &__table-label {
            padding: 0 0.5em 0 0.5em;
        }

        &__buttons {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;

            margin-bottom: 8px;

            .button {
                margin: 0 8px 0 8px;
            }
        }
    }
</style>
