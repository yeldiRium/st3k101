<template>
    <modal name="modal-create-questionnaire"
           height="auto"
           @before-open="beforeOpen"
    >
        <CreateResource
                @cancel="cancel"
                @create="create"
        >
            <template slot="header">
                Create new Questionnaire
            </template>
            <template slot="body">
                <input class="modal-create-questionnaire__questionnaire-name"
                       name="questionnaire-name"
                       v-model="name"
                />

                <textarea v-model="description"/>

                <Toggle v-model="isPublic">
                    <template slot="off">
                        locked
                    </template>
                    <template slot="on">
                        published
                    </template>
                </Toggle>

                <Toggle v-model="allowEmbedded">
                    <template slot="off">
                        only in browser
                    </template>
                    <template slot="on">
                        allow embedding
                    </template>
                </Toggle>

                <input v-model="xapiTarget"/>
            </template>
        </CreateResource>
    </modal>
</template>

<script>
    import {isNil} from "ramda";
    import {mapState} from "vuex-fluture";

    import CreateResource from "./CreateResource";
    import Toggle from "../Form/ToggleButton";

    export default {
        name: "ModalCreateQuestionnaire",
        components: {
            CreateResource,
            Toggle
        },
        data() {
            return {
                language: null,
                handler: null,
                name: "Questionnaire name",
                description: "Questionnaire description",
                isPublic: false,
                allowEmbedded: false,
                xapiTarget: "xapi target"
            }
        },
        computed: {
            ...mapState("session", ["dataClient"])
        },
        methods: {
            beforeOpen({params: {language, handler}}) {
                if (isNil(language)) {
                    throw new Error("Parameter language required!");
                }
                if (isNil(handler)) {
                    throw new Error("Parameter handler required!");
                }
                this.language = language;
                this.handler = handler;
            },
            cancel() {
                this.$modal.hide("modal-create-questionnaire");
            },
            /**
             * Emits a "questionnaire-create" event with all needed data to cre-
             * ate the questionnaire.
             */
            create() {
                this.handler({
                    name: this.name,
                    description: this.description,
                    isPublic: this.isPublic,
                    allowEmbedded: this.allowEmbedded,
                    xapiTarget: this.xapiTarget
                });
                this.$modal.hide("modal-create-questionnaire");
            }
        }
    }
</script>

<style lang="scss">
    .modal-create-questionnaire {
        &__questionnaire-name {
            width: 80%;
        }
    }
</style>
