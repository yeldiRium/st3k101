<template>
    <div class="full-question"
         :class="classes"
         v-if="expanded"
    >
        <ListQuestion :question="question"
                      :disableSubText="true"
                      :draggable="true"
                      :ellipseText="false"
                      :disableEditing="disableEditing"
        >
            <IconExpandLess class="list-item-icon"
                            v-if="expanded"
                            @click.native="toggleExpanded"
            />
            <IconExpandMore class="list-item-icon"
                            v-else
                            @click.native="toggleExpanded"
            />
        </ListQuestion>

        <div class="full-question-body"
             ref="dropdown"
             v-if="expanded"
        >
            <ReferenceCounter :object="question"
                              v-if="question.isConcrete"
            />
            <RangeEditor :range="question.range"
                         v-if="!disabled(question)"
            />
            <div class="full-question-delete"
                 v-if="!disabled(question)"
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
                      :disableEditing="disableEditing"
        >
            <IconExpandLess class="list-item-icon"
                            v-if="expanded"
                            @click.native="toggleExpanded"
            />
            <IconExpandMore class="list-item-icon"
                            v-else
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

    import IconExpandLess from "../../../../assets/icons/baseline-expand_less-24px.svg";
    import IconExpandMore from "../../../../assets/icons/baseline-expand_more-24px.svg";

    export default {
        name: "Full-Question",
        extends: QuestionBase,
        components: {
            ListQuestion,
            ReferenceCounter,
            RangeEditor,
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
                    disabled: this.disabled(this.question)
                }
            }
        },
        methods: {
            toggleExpanded() {
                this.expanded = !this.expanded;
            },
        },
        created() {
            this.expanded = this.initiallyExpanded;
        }
    }
</script>

<style lang="scss">
    @import "../../../scss/_variables";

    .list-item.list-question {
        cursor: pointer;

        background-color: $primary;

        &.disabled {
            background-color: $slightlylight;
        }
    }

    .full-question {
        display: flex;
        flex-flow: column;

        background-color: $primary-light;

        &.disabled {
            background-color: $lighter;
        }
    }

    .full-question-body {
        display: flex;
        flex-flow: column;
        align-items: center;

        .referencecounter {
            margin-bottom: 8px;
        }

        .full-question-delete {
            margin-top: 8px;
        }
    }
</style>
