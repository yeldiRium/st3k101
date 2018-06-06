<template>
    <div class="TestQuestion_container">
        <Question :question="questions[0]"/>
        <Question :question="questions[1]"/>
        <Question :question="questions[2]"
                  :mini="true"
        />
        <Question :question="questions[3]"
                  :mini="true"
        />
    </div>
</template>

<script>
    import Question from "../../Partials/List/Question";
    import {ConcreteQuestion, ShadowQuestion} from "../../../model/Question";

    export default {
        name: "TestQuestion",
        components: {
            Question
        },
        data() {
            return {
                questions: [
                    // Owned ConcreteQuestion with 5 incoming references.
                    // Two of those references are from owned Questions.
                    new ConcreteQuestion(
                        "Diese ConcreteQuestion gehört mir.",
                        {end: 5},
                        true,
                        5,
                        [
                            "http://blubblab/api/question/myidlel",
                            "http://blubblab/api/question/myid2lul"
                        ]
                    ),
                    // Owned ShadowQuestion.
                    new ShadowQuestion(
                        "Diese ShadowQuestion gehört mir.",
                        {start: 2, end: 10, step: 2},
                        true,
                        "http://blubblab/api/question/someonesidlel"
                    ),
                    // Not owned ConcreteQuestion with 3 incoming references.
                    // One of those reference is from an owned Question.
                    new ConcreteQuestion(
                        "Diese ConcreteQuestion gehört mir nicht.",
                        {start: 0, end: 7},
                        false,
                        3,
                        [
                            "http://blubblab/api/question/myotheridkek"
                        ]
                    ),
                    // Not owned ShadowQuestion.
                    new ShadowQuestion(
                        "Diese ShadowQuestion gehört mir nicht.",
                        {end: 5, step: 2},
                        false,
                        "http://blubblab/api/question/someonesotheridtrell"
                    )
                ]
            }
        }
    }
</script>

<style lang="scss">
    .TestQuestion_container {
        width: 100%;
        height: 100%;

        padding: 0;
        margin: 0;
    }

    .list-item {
        width: 90vw;
        height: 3em;

        &.mini {
            height: 2em;
        }
    }
</style>