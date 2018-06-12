<template>
    <div class="TestFullDimension_container">
        <FullDimension :dimension="dimensions[0]"/>
        <FullDimension :dimension="dimensions[1]"/>
        <FullDimension :dimension="dimensions[2]"/>
        <FullDimension :dimension="dimensions[3]"/>
        <FullDimension :dimension="dimensions[4]"/>
    </div>
</template>

<script>
    import {drop} from "ramda";

    import FullDimension from "../../Partials/SurveyBase/Full/Dimension";

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
        name: "TestFullDimension",
        components: {
            FullDimension
        },
        data: function () {
            const dataClient = this.$store.getters["session/dataClient"];
            const someoneElse = new DataClient("somehrefNOT", "blub@blub.blub", "en");
            const english = new Language("en", "English");
            const languageData = new LanguageData(
                english,
                english,
                [english]
            );
            const questions = [
                // Owned ConcreteQuestion with 5 incoming references.
                // Two of those references are from owned Questions.
                new ConcreteQuestion(
                    "http://blubblab/api/question/1",
                    dataClient,
                    languageData,
                    "Diese ConcreteQuestion gehört mir.Sie hat einen extra langen Text zum testen.",
                    new Range({end: 5}),
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
                    languageData,
                    "Diese ShadowQuestion gehört mir.",
                    new Range({start: 2, end: 10}),
                    new Resource("http://blubblab/api/question/someonesidlel")
                ),
                // Not owned ConcreteQuestion with 3 incoming references.
                // One of those reference is from an owned ListQuestion.
                new ConcreteQuestion(
                    "http://blubblab/api/question/3",
                    someoneElse,
                    languageData,
                    "Diese ConcreteQuestion gehört mir nicht.Sie hat einen extra langen Text zum testen.",
                    new Range({start: 0, end: 7}),
                    3,
                    [
                        new Resource("http://blubblab/api/question/myotheridkek")
                    ]
                ),
                // Not owned ShadowQuestion.
                new ShadowQuestion(
                    "http://blubblab/api/question/4",
                    someoneElse,
                    languageData,
                    "Diese ShadowQuestion gehört mir nicht.",
                    new Range({end: 5}),
                    new Resource("http://blubblab/api/question/someonesotheridtrell")
                )
            ];

            return {
                dimensions: [
                    // Owned ConcreteDimension with 5 incoming references.
                    // Two of those references are from owned Dimensions.
                    new ConcreteDimension(
                        "http://blubblab/api/dimension/1",
                        dataClient,
                        languageData,
                        "Diese ConcreteDimension gehört mir. Sie hat einen extra langen Text zum testen. Ihre Questions sind randomized.",
                        drop(0, questions),
                        true,
                        5,
                        [
                            new Resource("http://blubblab/api/dimension/myidlel"),
                            new Resource("http://blubblab/api/dimension/myid2lul")
                        ]
                    ),
                    // Owned ShadowDimension.
                    new ShadowDimension(
                        "http://blubblab/api/dimension/2",
                        dataClient,
                        languageData,
                        "Diese ShadowDimension gehört mir. Ihre Questions sind in fester Reihenfolge.",
                        drop(0, questions),
                        false,
                        new Resource("http://blubblab/api/dimension/someonesidlel")
                    ),
                    // Not owned ConcreteDimension with 3 incoming references.
                    // One of those reference is from an owned ListDimension.
                    new ConcreteDimension(
                        "http://blubblab/api/dimension/3",
                        someoneElse,
                        languageData,
                        "Diese ConcreteDimension gehört mir nicht. Sie hat einen extra langen Text zum testen. Ihre Questions sind randomized.",
                        drop(0, questions),
                        true,
                        3,
                        [
                            new Resource("http://blubblab/api/dimension/myotheridkek")
                        ]
                    ),
                    // Not owned ShadowDimension.
                    new ShadowDimension(
                        "http://blubblab/api/dimension/4",
                        someoneElse,
                        languageData,
                        "Diese ShadowDimension gehört mir nicht. Ihre Questions sind in fester Reihenfolge.",
                        drop(0, questions),
                        false,
                        new Resource("http://blubblab/api/dimension/someonesotheridtrell")
                    ),
                    new ConcreteDimension(
                        "http://blubblab/api/dimension/1",
                        dataClient,
                        languageData,
                        "Diese ConcreteDimension gehört mir. Sie hat einen extra langen Text zum testen. Ihre Questions sind randomized.",
                        drop(0, questions),
                        true,
                        5,
                        [
                            new Resource("http://blubblab/api/dimension/myidlel"),
                            new Resource("http://blubblab/api/dimension/myid2lul")
                        ]
                    )
                ]
            }
        }
    }
</script>

<style lang="scss">
    .TestFullDimension_container {
        width: 100%;
        height: 100%;

        padding: 0;
        margin: 0;

        .full-dimension {
            width: 90vw;
        }
    }
</style>