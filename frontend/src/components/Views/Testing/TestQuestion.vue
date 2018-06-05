<template>
    <div class="TestQuestion_container">
        <Question text="Dies ist scheinbar eine Question."
                  subtext="Und das hier soll ein Subtext sein?!? Mach mal besser länger."
                  class="mini"
        />
    </div>
</template>

<script>
    import Question from "../../Partials/Question/Question";

    export default {
        name: "TestQuestion",
        components: {Question}
    }
</script>

<style lang="scss">
    .TestQuestion_container {
        width: 100%;
        height: 100%;

        padding: 0;
        margin: 0;
    }

    .question {
        width: 90vw;
        height: 3em;
    }
</style>