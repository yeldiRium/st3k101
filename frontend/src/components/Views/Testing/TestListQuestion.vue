<template>
    <div class="TestListQuestion_container">
        <ListQuestion :question="questions[0]"/>
        <ListQuestion :question="questions[1]"/>
        <ListQuestion :question="questions[2]"/>
        <ListQuestion :question="questions[3]"/>
    </div>
</template>

<script>
    import ListQuestion from "../../Partials/SurveyBase/List/Question";
    import Resource from "../../../model/Resource";
    import {ConcreteQuestion, ShadowQuestion} from "../../../model/Question";
    import DataClient from "../../../model/DataClient";

    export default {
        name: "TestQuestion",
        components: {
            ListQuestion
        },
        data() {
            const dataClient = this.$store.getters["session/dataClient"];
            const someoneElse = new DataClient("somehrefNOT", "blub@blub.blub", "en");
            return {
                questions: [
                    // Owned ConcreteQuestion with 5 incoming references.
                    // Two of those references are from owned Questions.
                    new ConcreteQuestion(
                        "http://blubblab/api/question/1",
                        dataClient,
                        "Diese ConcreteQuestion gehört mir.Sie hat einen extra langen Text zum testen.",
                        {end: 5},
                        5,
                        [
                            new Resource("http://blubblab/api/question/myidlel"),
                            new Resource("http://blubblab/api/question/myid2lul")
                        ]
                    ),
                    // Owned ShadowQuestion.
                    new ShadowQuestion(
                        "http://blubblab/api/question/2",
                        dataClient,
                        "Diese ShadowQuestion gehört mir.",
                        {start: 2, end: 10, step: 2},
                        new Resource("http://blubblab/api/question/someonesidlel")
                    ),
                    // Not owned ConcreteQuestion with 3 incoming references.
                    // One of those reference is from an owned ListQuestion.
                    new ConcreteQuestion(
                        "http://blubblab/api/question/3",
                        someoneElse,
                        "Diese ConcreteQuestion gehört mir nicht.Sie hat einen extra langen Text zum testen.",
                        {start: 0, end: 7},
                        3,
                        [
                            new Resource("http://blubblab/api/question/myotheridkek")
                        ]
                    ),
                    // Not owned ShadowQuestion.
                    new ShadowQuestion(
                        "http://blubblab/api/question/4",
                        someoneElse,
                        "Diese ShadowQuestion gehört mir nicht.",
                        {end: 5, step: 2},
                        new Resource("http://blubblab/api/question/someonesotheridtrell")
                    )
                ]
            }
        }
    }
</script>

<style lang="scss">
    .TestListQuestion_container {
        width: 100%;
        height: 100%;

        padding: 0;
        margin: 0;
    }

    .list-item {
        width: 90vw;
    }
</style>