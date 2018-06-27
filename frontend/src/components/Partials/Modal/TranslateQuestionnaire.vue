<template>
    <modal name="modal-translate-questionnaire"
           height="auto"
           @before-open="beforeOpen"
    >
        <TranslateResource
                @cancel="cancel"
                @translate="translate"
        >
            <template slot="header">
                {{ headerText }}
            </template>
            <template slot="body">
                <input class="modal-translate-questionnaire__questionnaire-name"
                       name="questionnaire-name"
                       v-model="name"
                />

                <textarea v-model="description"/>
            </template>
        </TranslateResource>
    </modal>
</template>

<script>
    import {isNil, propOr, toLower} from "ramda";
    import {mapState} from "vuex-fluture";

    import TranslateResource from "./TranslateResource";
    import Toggle from "../Form/ToggleButton";

    export default {
        name: "ModalTranslateQuestionnaire",
        components: {
            TranslateResource,
            Toggle
        },
        data() {
            return {
                language: null,
                handler: null,
                name: null,
                description: null
            }
        },
        computed: {
            ...mapState("session", ["dataClient"]),
            headerText() {
                const longName = toLower(propOr("", "longName", this.language));
                return `Translate Questionnaire into ${longName}`;
            }
        },
        methods: {
            beforeOpen({params: {language, handler, name, description}}) {
                if (isNil(language)) {
                    throw new Error("Parameter language required!");
                }
                if (isNil(handler)) {
                    throw new Error("Parameter handler required!");
                }
                if (isNil(name)) {
                    throw new Error("Parameter name required!");
                }
                if (isNil(description)) {
                    throw new Error("Parameter description required!");
                }
                this.language = language;
                this.handler = handler;
                this.name = name;
                this.description = description;
            },
            cancel() {
                this.$modal.hide("modal-translate-questionnaire");
            },
            /**
             * Emits a "questionnaire-translate" event with all needed data to
             * translate the questionnaire.
             */
            translate() {
                this.handler({
                    language: this.language,
                    name: this.name,
                    description: this.description
                });
                this.$modal.hide("modal-translate-questionnaire");
            }
        }
    }
</script>

<style lang="scss">
    .modal-translate-questionnaire {
        &__questionnaire-name {
            width: 80%;
        }
    }
</style>
