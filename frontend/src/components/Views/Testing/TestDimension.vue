<template>
    <div class="TestDimension_container">
        <Dimension :dimension="dimensions[0]"/>
        <Dimension :dimension="dimensions[1]"/>
        <Dimension :dimension="dimensions[2]"/>
        <Dimension :dimension="dimensions[3]"/>
        <Dimension :dimension="dimensions[4]"/>
    </div>
</template>

<script>
    import {drop} from "ramda";

    import Dimension from "../../Partials/SurveyBase/Dimension";

    import DataClient from "../../../model/DataClient";
    import Resource from "../../../model/Resource";
    import {
        ConcreteQuestion,
        ShadowQuestion
    } from "../../../model/SurveyBase/Question";
    import {
        ConcreteDimension,
        ShadowDimension
    } from "../../../model/SurveyBase/Dimension";
    import {Language, LanguageData} from "../../../model/Language";
    import {Range} from "../../../model/SurveyBase/Config/Range";

    export default {
        name: "TestDimension",
        components: {
            Dimension
        },
        data: function () {
            const dataClient = this.$store.getters["session/dataClient"];
            const english = new Language("en", "English");
            const someoneElse = new DataClient("somehrefNOT", "somehrefNOT", "blub@blub.blub", english);
            const languageData = new LanguageData(
                english,
                english,
                [english]
            );
            const questions = [
                // Owned ConcreteQuestion with 5 incoming references.
                // Two of those references are from owned Questions.
                new ConcreteQuestion("http://blubblab/api/question/1", "1", dataClient, languageData, false, "Diese ConcreteQuestion gehört mir.Sie hat einen extra langen Text zum testen.", new Range({end: 5}), 5, [
                    new Resource("http://blubblab/api/question/myidlel", "myidlel"),
                    new Resource("http://blubblab/api/question/myid2lul", "myid2lul")
                ]),
                // Owned ShadowQuestion.
                new ShadowQuestion("http://blubblab/api/question/2", "2", dataClient, languageData, "Diese ShadowQuestion gehört mir.", new Range({
                    start: 2,
                    end: 10
                }), new Resource("http://blubblab/api/question/someonesidlel", "someonesidlel")),
                // Not owned ConcreteQuestion with 3 incoming references.
                // One of those reference is from an owned ListQuestion.
                new ConcreteQuestion("http://blubblab/api/question/3", "3", someoneElse, languageData, false, "Diese ConcreteQuestion gehört mir nicht.Sie hat einen extra langen Text zum testen.", new Range({
                    start: 0,
                    end: 7
                }), 3, [
                    new Resource("http://blubblab/api/question/myotheridkek", "myotheridkek")
                ]),
                // Not owned ShadowQuestion.
                new ShadowQuestion("http://blubblab/api/question/4", "4", someoneElse, languageData, "Diese ShadowQuestion gehört mir nicht.", new Range({end: 5}), new Resource("http://blubblab/api/question/someonesotheridtrell", 0))
            ];

            return {
                dimensions: [
                    // Owned ConcreteDimension with 5 incoming references.
                    // Two of those references are from owned Dimensions.
                    new ConcreteDimension("http://blubblab/api/dimension/1", "1", dataClient, languageData, "Diese ConcreteDimension gehört mir. Sie hat einen extra langen Text zum testen. Ihre Questions sind randomized.", drop(0, questions), true, 5, [
                        new Resource("http://blubblab/api/dimension/myidlel", "myidlel"),
                        new Resource("http://blubblab/api/dimension/myid2lul", "myid2lul")
                    ], false),
                    // Owned ShadowDimension.
                    new ShadowDimension("http://blubblab/api/dimension/2", "2", dataClient, languageData, "Diese ShadowDimension gehört mir. Ihre Questions sind in fester Reihenfolge.", drop(0, questions), false, new Resource("http://blubblab/api/dimension/someonesidlel", 0)),
                    // Not owned ConcreteDimension with 3 incoming references.
                    // One of those reference is from an owned ListDimension.
                    new ConcreteDimension("http://blubblab/api/dimension/3", "3", someoneElse, languageData, "Diese ConcreteDimension gehört mir nicht. Sie hat einen extra langen Text zum testen. Ihre Questions sind randomized.", drop(0, questions), true, 3, [
                        new Resource("http://blubblab/api/dimension/myotheridkek", "myotheridkek")
                    ], false),
                    // Not owned ShadowDimension.
                    new ShadowDimension("http://blubblab/api/dimension/4", "4", someoneElse, languageData, "Diese ShadowDimension gehört mir nicht. Ihre Questions sind in fester Reihenfolge.", drop(0, questions), false, new Resource("http://blubblab/api/dimension/someonesotheridtrell", 0)),
                    new ConcreteDimension("http://blubblab/api/dimension/1", "1", dataClient, languageData, "Diese ConcreteDimension gehört mir. Sie hat einen extra langen Text zum testen. Ihre Questions sind randomized.", drop(0, questions), true, 5, [
                        new Resource("http://blubblab/api/dimension/myidlel", "myidlel"),
                        new Resource("http://blubblab/api/dimension/myid2lul", "myid2lul")
                    ], false)
                ]
            }
        }
    }
</script>

<style lang="scss">
    .TestDimension_container {
        width: 100%;
        height: 100%;

        padding: 0;
        margin: 0;

        .dimension {
            width: 90vw;
        }
    }
</style>
