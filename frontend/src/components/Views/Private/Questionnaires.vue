<template>
    <div class="questionnaire-overview"
         :style="style"
    >
        <FullQuestionnaire :style="itemStyle"
                           v-for="questionnaire in questionnaires"
                           :key="questionnaire.href"
                           :questionnaire="questionnaire"

        />

        <ListItem class="questionnaire-overview__add-questionnaire-button"
                  :style="itemStyle"
                  text="Add new Questionnaire"
                  :mini="true"
                  :editableText="false"
                  @click="openNewQuestionnaireDialog"
        />
        <CreateQuestionnaire :language="dataClient.language"
                             @questionnaire-create="createQuestionnaire"
        />
    </div>
</template>

<script>
    import {mapState} from "vuex";

    import ListItem from "../../Partials/List/Item";
    import FullQuestionnaire from "../../Partials/SurveyBase/Full/Questionnaire";
    import CreateQuestionnaire from "../../Partials/Modal/CreateQuestionnaire";

    import {ConcreteQuestionnaire} from "../../../model/SurveyBase/Questionnaire";
    import {Language, LanguageData} from "../../../model/Language";
    import {createConcreteQuestionnaire} from "../../../api2/Questionnaire";

    export default {
        name: "QuestionnaireOverview",
        components: {
            ListItem,
            FullQuestionnaire,
            CreateQuestionnaire
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

                this.questionnaires = [
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
                ];
            },
            openNewQuestionnaireDialog() {
                this.$modal.show("modal-create-questionnaire");
            },
            createQuestionnaire({
                                    name, description, isPublic, allowEmbedded,
                                    xapiTarget
                                }) {
                createConcreteQuestionnaire(
                    this.dataClient,
                    this.dataClient.language,
                    name,
                    description,
                    isPublic,
                    allowEmbedded,
                    xapiTarget
                ).fork(
                    console.error,
                    questionnaire => {
                        this.questionnaires.push(questionnaire);
                    }
                );
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
