<template>
    <div class="question-full">
        <ListQuestion :question="question" />
        some more stuff lul.
    </div>
</template>

<script>
    import Question from "../../../../model/Question";

    import ListQuestion from "../List/Question";

    export default {
        name: "Full-ListQuestion",
        components: {
            ListQuestion
        },
        props: {
            question: {
                type: Question
            }
        }
    }
</script>

<style lang="scss">

</style>
