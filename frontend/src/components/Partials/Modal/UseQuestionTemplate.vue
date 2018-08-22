<template>
    <modal name="modal-use-question-template"
           height="auto"
           @before-open="beforeOpen"
    >
        <div class="modal-use-question-template__header">
            use Question template
        </div>
        <div class="modal-use-question-template__body">
            <Button
                    v-for="question in questionTemplates"
                    :key="question.id"
                    @action="use(question)"
            >
                {{ question.text }}
            </Button>
            <span
                    v-if="questionTemplates.length === 0"
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

    export default {
        name: "ModalUseQuestionTemplate",
        components: {
            Button
        },
        data() {
            return {
                question: null,
                handler: null
            }
        },
        computed: {
            ...mapGetters("questions", ["questionTemplates"])
        },
        methods: {
            beforeOpen({params: {handler}}) {
                if (isNil(handler)) {
                    throw new Error("Parameter handler required!");
                }
                this.handler = handler;

                this.$load(
                    this.$store.dispatch("questions/fetchQuestionTemplates", {})
                )
                    .fork(
                        this.$handleApiError,
                        () => {
                        }
                    );
            },
            cancel() {
                this.$modal.hide("modal-use-question-template");
            },
            /**
             * Emits a "question-create" event with all needed data to cre-
             * ate the question.
             */
            use(question) {
                this.$modal.hide("modal-use-question-template");
                this.handler({
                    question,
                });
            }
        }
    }
</script>

<style lang="scss">
    @import "../../scss/_variables";

    .modal-use-question-template {
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
