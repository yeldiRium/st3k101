<template>
    <modal name="modal-create-dimension"
           height="auto"
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
    import {mapState} from "vuex";

    import {Language, LanguageData} from "../../../model/Language";
    import {ConcreteDimension} from "../../../model/SurveyBase/Dimension";

    import CreateResource from "./CreateResource";
    import Toggle from "../Form/ToggleButton";

    export default {
        name: "ModalCreateDimension",
        components: {
            CreateResource,
            Toggle
        },
        props: {
            /** @type {Language} */
            language: {
                type: Language
            }
        },
        data() {
            return {
                name: "Dimension name",
                randomizeQuestions: false
            }
        },
        computed: {
            ...mapState("session", ["dataClient"])
        },
        methods: {
            cancel() {
                this.$modal.hide("modal-create-dimension");
            },
            /**
             * Emits a "dimension-create" event with all needed data to create
             * the dimension.
             */
            create() {
                this.$emit(
                    "dimension-create",
                    {
                        name: this.name,
                        randomizeQuestions: this.randomizeQuestions
                    }
                );
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
