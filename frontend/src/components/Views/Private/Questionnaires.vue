<template>
    <div class="questionnaire-overview"
         :style="style"
    >
        <Questionnaire :style="itemStyle"
                       v-for="questionnaire in questionnaires"
                       :key="questionnaire.href"
                       :questionnaire="questionnaire"
                       @questionnaire-delete="deleteQuestionnaire(questionnaire)"
        />

        <Button class="questionnaire-overview__add-questionnaire-button"
                @click="openNewQuestionnaireDialog"
        >
            Add new Questionnaire
        </Button>
    </div>
</template>

<script>
    import Future from "fluture";
    import {mapState} from "vuex";
    import {without} from "ramda";

    import Button from "../../Partials/Form/Button";
    import ListItem from "../../Partials/List/Item";
    import Questionnaire from "../../Partials/SurveyBase/Questionnaire";

    import {ConcreteQuestionnaire} from "../../../model/SurveyBase/Questionnaire";
    import {Language, LanguageData} from "../../../model/Language";
    import {
        createConcreteQuestionnaire,
        deleteQuestionnaire
    } from "../../../api2/Questionnaire";

    export default {
        name: "QuestionnaireOverview",
        components: {
            Button,
            ListItem,
            Questionnaire
        },
        data() {
            return {
                questionnaires: []
            }
        },
        created() {
            this.loadQuestionnaires();
        },
        computed: {
            ...mapState("global", ["window"]),
            ...mapState("session", ["dataClient"]),
            style() {
                return {};
            },
            itemStyle() {
                let width = "1200px";
                if (this.window.width * .8 < 1200) {
                    width = "80%";
                }

                return {
                    width: width
                };
            }
        },
        methods: {
            /**
             * Open the loading... modal;
             * Load the Questionnaires owned by the current DataClient from the
             * API;
             * Close the loading... modal
             */
            loadQuestionnaires() {
                // TODO: remove hardcoded sample data
                // TODO: open loading... modal
                // TODO: load questionnaires from API
                // TODO: close loading... modal

                let en = new Language("en", "English");
                let languageData = new LanguageData(en, en, [en]);

                this.$load(
                    Future((reject, resolve) => {
                        window.setTimeout(resolve, 1500);
                    }).chain(() => Future.of(
                        [
                            new ConcreteQuestionnaire(
                                "http://blubblab/api/questionnaire/1",
                                this.dataClient,
                                languageData,
                                "Dieser ConcreteQuestionnaire gehört mir.",
                                "Ein schöner Questionnaire, nicht wahr? Dies ist seine Beschreibung.",
                                true,
                                true,
                                "i don't even know, what this is",
                                [],
                                0,
                                []
                            ),
                            new ConcreteQuestionnaire(
                                "http://blubblab/api/questionnaire/2",
                                this.dataClient,
                                languageData,
                                "Dieser ShadowQuestionnaire gehört mir.",
                                "Ein schöner Questionnaire, nicht wahr? Dies ist seine Beschreibung.",
                                false,
                                true,
                                "i don't even know, what this is",
                                [],
                                0,
                                []
                            )
                        ]
                    ))
                ).fork(
                    console.error,
                    questionnaires => {
                        this.questionnaires = questionnaires;
                    }
                )
            },
            openNewQuestionnaireDialog() {
                this.$modal.show(
                    "modal-create-questionnaire",
                    {
                        language: this.dataClient.language,
                        handler: this.createQuestionnaire
                    }
                );
            },
            createQuestionnaire({
                                    name, description, isPublic, allowEmbedded,
                                    xapiTarget
                                }) {
                this.$load(
                    createConcreteQuestionnaire(
                        this.dataClient,
                        this.dataClient.language,
                        name,
                        description,
                        isPublic,
                        allowEmbedded,
                        xapiTarget
                    )
                ).fork(
                    console.error,
                    questionnaire => {
                        this.questionnaires.push(questionnaire);
                    }
                );
            },
            deleteQuestionnaire(questionnaire) {
                this.$load(
                    deleteQuestionnaire(questionnaire)
                ).fork(
                    console.error,
                    () => this.questionnaires = without(
                        [questionnaire], this.questionnaires
                    )
                );
                // Currently api function rejects since it's not implemented yet
                // Thus this has to be done again for demonstration and testing
                // TODO: remove this
                this.questionnaires = without(
                    [questionnaire], this.questionnaires
                )
            }
        }
    }
</script>

<style lang="scss">
    .questionnaire-overview {
        display: grid;
        grid-template-columns: 100%;
        grid-auto-flow: row;
        grid-row-gap: 0.5em;

        justify-items: center;
    }
</style>
