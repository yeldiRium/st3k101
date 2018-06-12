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
                <RangeEditor :range="question.range"
                             v-if="isOwnedByCurrentDataClient(question)"
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
            deleteQuestion() {
                // TODO: delete via API.
                this.$emit("question-deleted", this.question);
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

        &__body {
            width: 80%;
            align-self: center;

            display: flex;
            flex-flow: column;
            align-items: center;

            > * {
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

        .list-question.list-item {
            cursor: pointer;

            background-color: $primary;

            &--disabled {
                background-color: $slightlylight;
            }
        }
    }
</style>
