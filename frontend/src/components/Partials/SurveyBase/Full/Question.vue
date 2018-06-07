<template>
    <div class="question-full"
         :class="classes"
    >
        <ListQuestion :question="question"
                      :mini="true"
                      :draggable="false"
                      :disableIcons="true"
        />
        <div class="question-full-body">
            <References :object="question"
                        v-if="question.isConcrete"
            />
        </div>
        <div class="question-full-footer">

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
        computed: {
            classes() {
                return {
                    disabled: this.disabled
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

    .question-full {
        display: flex;
        flex-flow: column;

        background-color: $primary-light;

        &.disabled {
            background-color: $lighter;
        }
    }

    .question-full-body {
        display: flex;
        flex-flow: column;
        align-items: center;
    }
</style>
