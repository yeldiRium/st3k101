<template>
    <div class="full-dimension"
         :class="classes"
         v-if="expanded"
    >
        <ListDimension :dimension="dimension"
                       :disableSubText="true"
                       :draggable="true"
                       :ellipseText="false"
        >
            <IconExpandLess class="list-item__icon"
                            @click.native="toggleExpanded"
            />
        </ListDimension>

        <div class="full-dimension__body"
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

            <div class="full-dimension__questions">
                <FullQuestion class="full-question--bordered"
                              v-for="question in dimension.questions"
                              :key="question.href"
                              :question="question"
                              :deletable="dimension.isConcrete"
                              @question-delete="deleteQuestion"
                />

                <ListItem class="full-dimension__add-question-button"
                          v-if="isEditable(dimension)"
                          text="Add new Question"
                          :disableSubtext="true"
                          @click="openNewQuestionDialog"
                />
                <CreateQuestion v-if="isEditable(dimension)"
                                :language="dimension.languageData.currentLanguage"
                                @question-create="handleCreateQuestion"
                />
            </div>

            <div class="full-dimension__delete-button"
                 v-if="isDeletable(dimension)"
                 @click="deleteDimension"
            >
                delete
            </div>
        </div>
    </div>
    <div class="full-dimension"
         :class="classes"
         v-else
    >
        <ListDimension :dimension="dimension"
                       :draggable="draggable"
                       :ellipseText="true"
        >
            <IconExpandMore class="list-item__icon"
                            @click.native="toggleExpanded"
            />
        </ListDimension>
    </div>
</template>

<script>
    import {mapState} from "vuex";
    import {without} from "ramda";

    import DimensionBase from "../DimensionBase";
    import ListDimension from "../List/Dimension";
    import FullQuestion from "../Full/Question";
    import ListItem from "../../List/Item";
    import CreateQuestion from "../../Modal/CreateQuestion";

    import ReferenceCounter from "../Config/ReferenceCounter";
    import Toggle from "../../Form/ToggleButton";

    import IconExpandLess from "../../../../assets/icons/baseline-expand_less-24px.svg";
    import IconExpandMore from "../../../../assets/icons/baseline-expand_more-24px.svg";
    import {
        addConcreteQuestion,
        removeQuestion,
        setRandomizeQuestions
    } from "../../../../api2/Dimension";

    export default {
        name: "FullDimension",
        extends: DimensionBase,
        components: {
            ListDimension,
            FullQuestion,
            CreateQuestion,
            ListItem,
            ReferenceCounter,
            Toggle,
            IconExpandLess,
            IconExpandMore
        },
        props: {
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
                    "full-dimension--disabled": !this.isEditable(this.dimension)
                }
            }
        },
        methods: {
            toggleExpanded() {
                this.expanded = !this.expanded;
            },
            openNewQuestionDialog() {
                this.$modal.show(
                    "modal-create-question"
                )
            },
            handleCreateQuestion({text, range}) {
                addConcreteQuestion(
                    this.dimension, this.dataClient, text, range
                );
            },
            /**
             * Only handles removal from the dimension in reaction to Question
             * being deleted.
             */
            deleteQuestion(question) {
                removeQuestion(this.dimension, question);
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
            },
            updateRandomizeQuestions(randomizeQuestions) {
                setRandomizeQuestions(this.dimension, randomizeQuestions);
            }
        },
        created() {
            this.expanded = this.initiallyExpanded;
        }
    }
</script>

<style lang="scss">
    @import "../../../scss/_variables";

    .full-dimension {
        display: flex;
        flex-flow: column;

        background-color: $primary-light;

        &--disabled {
            background-color: $lighter;
        }

        &--bordered {
            border: 1px solid $primary;

            &.full-dimension--disabled {
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
                text-align: center;
                margin-top: 8px;
                margin-bottom: 8px;
            }
        }

        &__questions {
            display: flex;
            flex-flow: column;
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
