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
        <CreateQuestion/>
        <br/><br/>
        <button @click="click5">
            Create Dimension Dialog.
        </button>
        <CreateDimension/>
        <br/><br/>
        <button @click="click6">
            Create generic Dialog.
        </button>
        <br/><br/>
        <button @click="click7">
            Confirm Dialog
        </button>
    </div>
</template>

<script>
    import {ConcreteQuestion} from "../../../model/SurveyBase/Question";
    import {Resource} from "../../../model/Resource";
    import {Range} from "../../../model/SurveyBase/Config/Range";
    import {Language, LanguageData} from "../../../model/Language";

    import Question from "../../Partials/SurveyBase/Question";
    import CreateQuestion from "../../Partials/Modal/CreateQuestion";
    import CreateDimension from "../../Partials/Modal/CreateDimension";
    import Dialog from "../../Partials/Modal/Dialog";

    export default {
        name: "TestModal",
        components: {
            CreateQuestion,
            CreateDimension,
            Dialog
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
                question: new ConcreteQuestion("http://blubblab/api/question/1", "1", dataClient, languageData, "Diese ConcreteQuestion gehört mir. Sie hat einen extra langen Text zum testen.", new Range({end: 5}), 5, [
                    new Resource("http://blubblab/api/question/myidlel", "myidlel"),
                    new Resource("http://blubblab/api/question/myid2lul", "myid2lul")
                ])
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
                    Question,
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
                let english = new Language("en", "English");

                this.$modal.show(
                    "modal-create-question",
                    {
                        language: english
                    }
                );
            },
            click5() {
                let english = new Language("en", "English");

                this.$modal.show(
                    "modal-create-dimension",
                    {
                        language: english
                    }
                );
            },
            click6() {
                this.$modal.show(
                    "dialog",
                    {
                        title: "Title",
                        text: "Text",
                        buttons: [
                            {
                                text: "Blub",
                                handler: () => console.log("blub")
                            },
                            {
                                text: "Blab",
                                handler: () => console.log("Should be default"),
                                default: true
                            },
                            {
                                text: "Bleb",
                                default: false
                            },
                            {
                                text: "Invalid Handler",
                                handler: 5
                            },
                            {
                                text: "Second default",
                                handler: () => console.log("should not be invoked by default")
                            },
                            {
                                text: "filler"
                            }
                        ]
                    }
                )
            },
            click7() {
                this.$modal.show(
                    "dialog",
                    {
                        title: "Confirm",
                        text: "ORLY?",
                        buttons: [
                            {
                                text: "Cancel",
                                handler: () => this.$modal.hide("dialog")
                            },
                            {
                                text: "Confirm",
                                handler: () => console.log("confirmed"),
                                default: true
                            }
                        ]
                    }
                )
            }
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