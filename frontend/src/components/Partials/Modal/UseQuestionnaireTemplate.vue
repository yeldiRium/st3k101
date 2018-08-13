<template>
    <modal name="modal-use-questionnaire-template"
           height="auto"
           @before-open="beforeOpen"
    >
        <div class="modal-use-questionnaire-template__header">
            use Questionnaire template
        </div>
        <div class="modal-use-questionnaire-template__body">
            <Button
                    v-for="questionnaire in questionnaireTemplates"
                    :key="questionnaire.id"
                    @action="use(questionnaire)"
            >
                {{ questionnaire.name }}
            </Button>
            <span
                    v-if="questionnaireTemplates.length === 0"
            >
                Keine Templates gefunden!
            </span>
            <Button @action="cancel">
                Cancel
            </Button>
        </div>
    </modal>
</template>

<script>
    import {mapGetters} from "vuex-fluture";
    import {isNil} from "ramda";

    import Button from "../Form/Button";
    import {fetchQuestionnaireTemplates} from "../../../api/Questionnaire";

    export default {
        name: "ModalUseQuestionnaireTemplate",
        components: {
            Button
        },
        data() {
            return {
                questionnaire: null,
                handler: null
            }
        },
        computed: {
            ...mapGetters("questionnaires", ["questionnaireTemplates"])
        },
        methods: {
            beforeOpen({params: {handler}}) {
                if (isNil(handler)) {
                    throw new Error("Parameter handler required!");
                }
                this.handler = handler;

                this.$load(
                    this.$store.dispatch("questionnaires/fetchQuestionnaireTemplates", {})
                )
                    .fork(
                        this.$handleApiError,
                        () => {
                        }
                    );
            },
            cancel() {
                this.$modal.hide("modal-use-questionnaire-template");
            },
            /**
             * Emits a "questionnaire-create" event with all needed data to cre-
             * ate the questionnaire.
             */
            use(questionnaire) {
                this.$modal.hide("modal-use-questionnaire-template");
                this.handler({
                    questionnaire,
                });
            }
        }
    }
</script>

<style lang="scss">
    @import "../../scss/_variables";

    .modal-use-questionnaire-template {
        display: grid;
        grid-template-rows: 2em auto 2em;
        grid-row-gap: 10px;

        &__header {
            background-color: $primary-light;

            font-size: 1.4em;
            text-align: center;
        }

        &__body {
            padding-top: 10px;
            padding-left: 20px;
            padding-right: 20px;

            display: flex;
            flex-flow: column;
            align-items: center;

            > * {
                margin-bottom: 10px;
            }
        }
    }
</style>
