<template>
    <div class="dimension"
         :class="classes"
    >
        <ListItem class="dimension__title"
                  :value="dimension.name"
                  :subtext="subtext"
                  :mini="expanded"
                  :ellipseText="!expanded"
                  :disabled="!isEditable(dimension)"
                  @input="updateDimensionName"
        >
            <router-link :to="{name: 'ADimension', params: {id: dimension.id}}">
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
                            :language-data="dimension.languageData"
                            @choose-language="changeLanguage"
                            @choose-language-unavailable="openAddNewTranslationDialog"
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
    import {mapState} from "vuex-fluture";
    import {without} from "ramda";

    import {Dimension} from "../../../model/SurveyBase/Dimension";

    import SurveyBase from "./SurveyBase";
    import Question from "./Question";
    import ListItem from "../List/Item";
    import LanguagePicker from "../LanguagePicker";
    import ReferenceCounter from "./Config/ReferenceCounter";
    import Toggle from "../Form/ToggleButton";
    import Button from "../Form/Button";

    import IconLink from "../../../assets/icons/baseline-link-24px.svg";
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
            IconLink,
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
            },
            showLink: {
                type: Boolean,
                default: true
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
                    this.$store.dispatch(
                        "dimensions/fetchDimension",
                        {href: this.dimension.href, language}
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
                if (!this.isEditable(this.dimension)) {
                    return;
                }
                this.$modal.show(
                    "modal-translate-dimension",
                    {
                        language,
                        handler: this.addNewTranslation,
                        name: this.dimension.name
                    }
                );
            },
            /**
             * Add a new translation to the Dimension.
             * This means set new field values via API for the given languages
             * and then fetch the Dimension anew in the now existing language.
             * @param {Language} language
             * @param {String} name
             */
            addNewTranslation({language, name}) {
                if (!this.isEditable(this.dimension)) {
                    return;
                }

                this.$load(
                    this.$store.dispatch(
                        "dimensions/updateDimension",
                        {
                            dimension: this.dimension,
                            language,
                            params: {
                                name
                            }
                        }
                    )
                        .chain(dimension => this.$store.dispatch(
                            "dimensions/fetchDimension",
                            {href: dimension.href, language}
                        ))
                ).fork(
                    this.$handleApiError,
                    () => {
                    }
                );
            },
            updateDimensionName(name) {
                if (!this.isEditable(this.dimension)) {
                    return;
                }
                this.$load(
                    this.$store.dispatch(
                        "dimensions/updateDimension",
                        {
                            dimension: this.dimension,
                            params: {
                                name
                            }
                        }
                    )
                ).fork(
                    this.$handleApiError,
                    () => {
                    }
                );
            },
            updateRandomizeQuestions(randomizeQuestions) {
                this.$load(
                    this.$store.dispatch(
                        "dimensions/updateDimension",
                        {
                            dimension: this.dimension,
                            params: {
                                randomizeQuestions
                            }
                        }
                    )
                ).fork(
                    this.$handleApiError,
                    () => {
                    }
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
                    this.$store.dispatch(
                        "dimensions/addConcreteQuestion",
                        {
                            dimension: this.dimension,
                            params: {
                                text, range
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
             * Only handles removal from the dimension in reaction to Question
             * being deleted.
             */
            deleteQuestion(question) {
                if (!this.isEditable(this.dimension)) {
                    return;
                }
                this.$load(
                    this.$store.dispatch(
                        "dimensions/removeQuestion",
                        {
                            dimension: this.dimension,
                            question
                        }
                    )
                ).fork(
                    this.$handleApiError,
                    () => {
                    }
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
