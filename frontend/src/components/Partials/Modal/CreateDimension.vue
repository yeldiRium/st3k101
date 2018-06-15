<template>
    <modal name="modal-create-dimension"
           height="auto"
           @before-open="beforeOpen"
    >
        <CreateResource
                @cancel="cancel"
                @create="create"
        >
            <template slot="header">
                Create new Dimension
            </template>
            <template slot="body">
                <input class="modal-create-dimension__dimension-name"
                       name="dimension-name"
                       v-model="name"
                />
                <Toggle v-model="randomizeQuestions"
                >
                    <template slot="off">
                        in order
                    </template>
                    <template slot="on">
                        randomize
                    </template>
                </Toggle>
            </template>
        </CreateResource>
    </modal>
</template>

<script>
    import {isNil} from "ramda";
    import {mapState} from "vuex";

    import CreateResource from "./CreateResource";
    import Toggle from "../Form/ToggleButton";

    export default {
        name: "ModalCreateDimension",
        components: {
            CreateResource,
            Toggle
        },
        data() {
            return {
                language: null,
                handler: null,
                name: "Dimension name",
                randomizeQuestions: false
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
                this.$modal.hide("modal-create-dimension");
            },
            /**
             * Emits a "dimension-create" event with all needed data to create
             * the dimension.
             */
            create() {
                this.handler({
                    name: this.name,
                    randomizeQuestions: this.randomizeQuestions
                });
                this.$modal.hide("modal-create-dimension");
            }
        }
    }
</script>

<style lang="scss">
    .modal-create-dimension {
        &__dimension-name {
            width: 80%;
        }
    }
</style>
