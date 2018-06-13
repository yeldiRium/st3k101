<template>
    <div class="full-question"
         :class="classes"
         v-if="expanded"
    >
        <ListQuestion :question="question"
                      :disableSubText="true"
                      :draggable="true"
                      :ellipseText="false"
        >
            <IconExpandLess class="list-item__icon"
                            @click.native="toggleExpanded"
            />
        </ListQuestion>

        <div class="full-question__body"
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
            <div class="full-question__delete-button"
                 v-if="isDeletable(question)"
                 @click="deleteQuestion"
            >
                delete
            </div>
        </div>
    </div>
    <div class="full-question"
         :class="classes"
         v-else
    >
        <ListQuestion :question="question"
                      :draggable="draggable"
                      :ellipseText="true"
        >
            <IconExpandMore class="list-item__icon"
                            @click.native="toggleExpanded"
            />
        </ListQuestion>
    </div>
</template>

<script>
    import QuestionBase from "../QuestionBase";
    import ListQuestion from "../List/Question";
    import ReferenceCounter from "../Config/ReferenceCounter";
    import RangeEditor from "../Config/RangeEditor";
    import Range from "../Config/RangeSVG";

    import IconExpandLess from "../../../../assets/icons/baseline-expand_less-24px.svg";
    import IconExpandMore from "../../../../assets/icons/baseline-expand_more-24px.svg";

    import {deleteQuestion, setRange} from "../../../../api2/Question";

    export default {
        name: "FullQuestion",
        extends: QuestionBase,
        components: {
            ListQuestion,
            ReferenceCounter,
            RangeEditor,
            Range,
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
            classes() {
                return {
                    "full-question--disabled": !this.isEditable(this.question)
                }
            }
        },
        methods: {
            toggleExpanded() {
                this.expanded = !this.expanded;
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
            },
            updateRange(range) {
                setRange(this.question, range);
            }
        },
        created() {
            this.expanded = this.initiallyExpanded;
        }
    }
</script>

<style lang="scss">
    @import "../../../scss/_variables";

    .full-question {
        display: flex;
        flex-flow: column;

        background-color: $primary-light;

        &--disabled {
            background-color: $lighter;
        }

        &--bordered {
            border: 1px solid $primary;

            &.full-question--disabled {
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
                margin-top: 8px;
                margin-bottom: 8px;
                width: 100%;
                text-align: center;
            }

            .reference-counter {
                margin-bottom: 8px;
            }

        }

        &__delete-button {
            margin-top: 8px;
        }
    }
</style>
