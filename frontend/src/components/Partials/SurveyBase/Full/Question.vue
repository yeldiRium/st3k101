<template>
    <div class="full-question"
         :class="classes"
         v-if="expanded"
    >
        <ListQuestion :question="question"
                      :disableSubText="true"
                      :draggable="true"
                      :ellipseText="false"
                      @click="toggleExpanded"
        />

        <div class="full-question-body"
             ref="dropdown"
             v-if="expanded"
        >
            <References :object="question"
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
                      @click="toggleExpanded"
        />
    </div>
</template>

<script>
    import QuestionBase from "../QuestionBase";
    import ListQuestion from "../List/Question";
    import References from "../Config/References";
    import RangeEditor from "../Config/RangeEditor";

    export default {
        name: "Full-Question",
        extends: QuestionBase,
        components: {
            ListQuestion,
            References,
            RangeEditor
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

        .full-question-delete {
            margin-top: 8px;
        }
    }
</style>
