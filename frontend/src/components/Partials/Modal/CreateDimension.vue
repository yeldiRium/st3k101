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
             * Creates the Dimension and emits it via a "dimension-created" e-
             * vent.
             * TODO: send API request with all data, then set href and owner to
             *       the returned values
             *       Also refactor this in general. This is currently as demon-
             *       strative of intent as possible and should be improved upon.
             */
            create() {
                const href = "someshittyhref" + String(Math.random());
                const owner = this.dataClient;
                const languageData = new LanguageData(
                    this.language,
                    this.language,
                    [this.language]
                );
                const name = this.name;
                const questions = [];
                const randomizeQuestions = this.randomizeQuestions;
                const incomingReferenceCount = 0;
                const ownedIncomingReferences = [];

                const dimension = new ConcreteDimension(
                    href,
                    owner,
                    languageData,
                    name,
                    questions,
                    randomizeQuestions,
                    incomingReferenceCount,
                    ownedIncomingReferences
                );

                this.$emit("dimension-created", dimension);
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
