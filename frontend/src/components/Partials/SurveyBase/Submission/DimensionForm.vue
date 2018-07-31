<template>
    <div>
        <QuestionForm
                v-for="question in dimension.questions"
                :question="question"
                :key="question.href"
                @response-change="notifyParent($event)"
        />
    </div>
</template>

<script>
    import QuestionForm from "./QuestionForm";
    export default {
        name: "DimensionForm",
        components: {QuestionForm},
        props: {
            dimension: null
        },
        methods: {
            notifyParent({questionId, value}) {
                this.$emit(
                    "response-change",
                    {
                        questionId: questionId,
                        value: value
                    }
                );
            }
        }
    }
</script>

<style scoped>

</style>