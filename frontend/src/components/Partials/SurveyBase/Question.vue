<template>
    <div class="question"
         :class="classes"
    >
        <ListItem :value="question.text"
                  class="question__title"
                  :ellipseText="!expanded"
                  :mini="true"
                  :disabled="!isEditable(question)"
                  @input="updateQuestion('text', $event, true)"
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
                            @choose-language-unavailable="openAddNewTranslationDialog"
            />
        </ListItem>

        <div class="question__body"
             v-if="expanded"
             ref="dropdown"
        >
            <template>
                <template v-if="question.isConcrete">
                    <span class="question__table-label">
                        References:
                    </span>
                    <ReferenceCounter :object="question"
                    />
                </template>
                <template v-else>
                    <span class="question__table-label question__table-label--span-2">
                        <router-link :to="{name: 'AQuestion', params: {id: question.referenceTo.id}}">Go to template</router-link>
                    </span>
                </template>
            </template>

            <span class="question__table-label">
                Reference ID:
            </span>
            <template>
                <EditableText v-if="question.isConcrete"
                              :value="question.referenceId"
                              @input="updateQuestion('referenceId', $event, true)"
                              :edit-left="true"
                />
                <div v-else>
                    {{ question.referenceId }}
                </div>
            </template>

            <span class="questionnaire__table-label">
                Range:
            </span>
            <template>
                <RangeEditor :value="question.range"
                             @input="updateQuestion('range', $event, true)"
                             v-if="isOwnedByCurrentDataClient(question) && question.isConcrete"
                />
                <Range :range="question.range"
                       :preview="true"
                       v-else
                />
            </template>
            <TrackerEntries :surveyBase="question"></TrackerEntries>
        </div>


        <div class="question__buttons"
             v-if="expanded"
        >
            <Button v-if="isDeletable(question)"
                    @click="deleteQuestion"
                    :class="{'button--grey': question.isShadow}"
            >
                delete
            </Button>
        </div>
    </div>
</template>

<script>
    import {assoc} from "ramda";

    import {Question} from "../../../model/SurveyBase/Question";

    import {setRange, setText} from "../../../api/Question";

    import SurveyBase from "./SurveyBase";
    import ListItem from "../List/Item";
    import LanguagePicker from "../LanguagePicker";
    import ReferenceCounter from "./Config/ReferenceCounter";
    import RangeEditor from "./Config/RangeEditor";
    import Range from "./Config/RangeSVG";
    import Button from "../Form/Button";
    import EditableText from "../Form/EditableText";
    import TrackerEntries from "./TrackerEntries";

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
            EditableText,
            TrackerEntries,
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
                        this.$emit("updated");
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
                        this.$emit("updated");
                    }
                );
            },
            /**
             * Generically updates the Question via the Store.
             *
             * @param {String} prop The name of the updated property.
             * @param {*} value The new value for it.
             * @param {Boolean} mustBeEditable Whether the Question must be
             *  editable for this to work.
             */
            updateQuestion(prop, value, mustBeEditable=false) {
                if (mustBeEditable && !this.isEditable(this.question)) {
                    return;
                }
                this.$load(
                    this.$store.dispatch(
                        "questions/updateQuestion",
                        {
                            question: this.question,
                            params: assoc(prop, value, {})
                        }
                    )
                ).fork(
                    this.$handleApiError,
                    () => {
                        this.$emit("updated");
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
            padding: 0.5em 2em 0.5em 2em;

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

            &--span-2 {
                grid-column: 1 / span 2;
            }
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
