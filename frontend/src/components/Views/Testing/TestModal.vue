<template>
    <div class="TestModal_container">
        <button @click="click1">
            Normaler dialog mit Titel und Text.
        </button>
        <br/><br/>
        <button @click="click2">
            Dialog mit custom Buttons.
        </button>
        <br/><br/>
        <button @click="click3">
            Dialog mit Question drin.
        </button>
        <br/><br/>
        <button @click="click4">
            Create Question Dialog.
        </button>
        <CreateQuestion />
    </div>
</template>

<script>
    import {mapState} from "vuex";

    import {ConcreteQuestion} from "../../../model/SurveyBase/Question";
    import {Resource} from "../../../model/Resource";
    import {Range} from "../../../model/SurveyBase/Config/Range";
    import {Language, LanguageData} from "../../../model/Language";

    import FullQuestion from "../../Partials/SurveyBase/Full/Question";
    import CreateResource from "../../Partials/Popup/CreateResource";
    import CreateQuestion from "../../Partials/Popup/CreateQuestion";

    export default {
        name: "TestModal",
        components: {
            CreateQuestion
        },
        data() {
            const dataClient = this.$store.getters["session/dataClient"];
            const english = new Language("en", "English");
            const languageData = new LanguageData(
                english,
                english,
                [english]
            );
            return {
                question: new ConcreteQuestion(
                    "http://blubblab/api/question/1",
                    dataClient,
                    languageData,
                    "Diese ConcreteQuestion gehört mir. Sie hat einen extra langen Text zum testen.",
                    new Range({end: 5}),
                    5,
                    [
                        new Resource("http://blubblab/api/question/myidlel"),
                        new Resource("http://blubblab/api/question/myid2lul")
                    ]
                )
            };
        },
        methods: {
            click1() {
                this.$modal.show("dialog", {
                    title: "Normaler dialog mit Titel und Text.",
                    text: "Dies ist ein Test des vue-js-modal dialogs."
                })
            },
            click2() {
                this.$modal.show("dialog", {
                    title: "Dialog mit custom Buttons.",
                    text: "Dies ist ein Test des vue-js-modal dialogs.",
                    buttons: [
                        {
                            title: "Cancel",
                            handler: () => {
                                this.$modal.hide("dialog");
                            }
                        },
                        {
                            title: "Confirm",
                            default: true,
                            handler: () => {
                                alert("Confirmed!");
                            }
                        },
                        {
                            title: "What dis?",
                            handler: () => {
                                alert("Some kind of tomato?");
                            }
                        }
                    ]
                })
            },
            click3() {
                this.$modal.show(
                    FullQuestion,
                    {
                        question: this.question
                    },
                    {
                        height: "auto",
                        width: "80%"
                    }
                )
            },
            click4() {
                let width = "80%";
                if (this.window.width * .8 > 400) {
                    width = "400px";
                }

                let english = new Language("en", "English");

                this.$modal.show(
                    "create-question",
                    {
                        language: english
                    },
                    {
                        height: "auto",
                        width: width
                    }
                );
            }
        },
        computed: {
            ...mapState("global", ["window"])
        }
    }
</script>

<style lang="scss">
    .TestModal_container {
        width: 100%;
        height: 100%;

        padding: 0;
        margin: 0;
    }

    .toggle {
        width: 400px;
        margin-bottom: 20px;
    }

    .v--modal .full-question {
        width: 80vw;
    }
</style>