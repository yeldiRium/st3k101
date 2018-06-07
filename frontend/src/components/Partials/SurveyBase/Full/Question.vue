<template>
    <div class="full-question"
         :class="classes"
    >
        <ListQuestion :question="question"
                      :disableSubText="true"
                      :draggable="draggable"
                      :disableIcons="true"
                      :ellipseText="false"
        />
        <div class="full-question-body">
            <References :object="question"
                        v-if="question.isConcrete"
            />
        </div>
        <div class="full-question-footer">

        </div>
    </div>
</template>

<script>
    import QuestionBase from "../QuestionBase";
    import ListQuestion from "../List/Question";
    import References from "../Config/References";

    export default {
        name: "Full-Question",
        extends: QuestionBase,
        components: {
            ListQuestion,
            References
        },
        props: {
            /**
             * Override this to change the default value.
             * @type boolean
             */
            draggable: {
                type: Boolean,
                default: false
            }
        },
        computed: {
            classes() {
                return {
                    disabled: this.disabled(this.question)
                }
            }
        }
    }
</script>

<style lang="scss">
    @import "../../../scss/_variables";

    .list-item.list-question {
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
    }
</style>
