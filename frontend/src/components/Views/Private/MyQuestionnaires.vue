<template>
    <div class="my-questionnaires">
        <div class="my-questionnaires__questionnaires">
            <Questionnaire :style="itemStyle"
                           v-for="questionnaire in myQuestionnaires"
                           :key="questionnaire.href"
                           :questionnaire="questionnaire"
                           @questionnaire-delete="deleteQuestionnaire(questionnaire)"
            />
        </div>

        <TrackerEntries :all="true" :style="itemStyle"></TrackerEntries>

        <div class="my-questionnaires__buttons">
            <Button class="my-questionnaires__add-questionnaire-button"
                    @action="openNewQuestionnaireDialog"
            >
                Add new Questionnaire
            </Button>
            <Button class="my-questionnaires__use-template-button"
                    @action="openUseQuestionnaireTemplateDialog"
            >
                Use Questionnaire template
            </Button>
        </div>
    </div>
</template>

<script>
    import {mapGetters, mapState} from "vuex-fluture";

    import Button from "../../Partials/Form/Button";
    import Questionnaire from "../../Partials/SurveyBase/Questionnaire";
    import TrackerEntries from "../../Partials/SurveyBase/TrackerEntries";

    export default {
        name: "MyQuestionnaires",
        components: {
            TrackerEntries,
            Button,
            Questionnaire
        },
        created() {
            this.loadQuestionnaires();
        },
        computed: {
            ...mapState("session", ["dataClient"]),
            ...mapGetters("questionnaires", ["myQuestionnaires"]),
            ...mapState("global", ["window"]),
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
                this.$load(
                    this.$store.dispatch("questionnaires/loadMyQuestionnaires")
                ).fork(
                    this.$handleApiError,
                    () => {
                    }
                )
            },
            openUseQuestionnaireTemplateDialog() {
                this.$modal.show(
                    "modal-use-questionnaire-template",
                    {
                        handler: this.useQuestionnaireTemplate
                    }
                );
            },
            useQuestionnaireTemplate({questionnaire}) {
                this.$load(
                    this.$store.dispatch(
                        "questionnaires/createShadowQuestionnaire",
                        {concreteQuestionnaire: questionnaire}
                    )
                )
                    .fork(
                        this.$handleApiError,
                        () => {
                        }
                    );
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
                    this.$store.dispatch(
                        "questionnaires/createConcreteQuestionnaire",
                        {
                            language: this.dataClient.language,
                            name,
                            description,
                            isPublic,
                            allowEmbedded,
                            xapiTarget
                        }
                    )
                ).fork(
                    this.$handleApiError,
                    () => {
                    }
                );
            },
            deleteQuestionnaire(questionnaire) {
                this.$load(
                    this.$store.dispatch(
                        "questionnaires/deleteQuestionnaire",
                        {questionnaire}
                    )
                ).fork(
                    this.$handleApiError,
                    () => {
                    }
                );
            }
        }
    }
</script>

<style lang="scss">
    @import "../../scss/_variables";

    .my-questionnaires {
        display: grid;
        grid-template-columns: 100%;
        grid-auto-flow: row;
        grid-row-gap: 0.5em;

        justify-items: center;

        &__questionnaires {
            width: 100%;

            display: grid;
            grid-template-columns: 100%;
            grid-auto-flow: row;
            grid-row-gap: 0.5em;

            justify-items: center;
        }

        &__buttons {
            display: grid;
            grid-auto-flow: column;
            grid-column-gap: 0.5em;
        }

    }
</style>
