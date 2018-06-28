<template>
    <modal name="modal-use-dimension-template"
           height="auto"
           @before-open="beforeOpen"
    >
        <div class="modal-use-dimension-template__header">
            use Dimension template
        </div>
        <div class="modal-use-dimension-template__body">
            <Button
                    v-for="dimension in dimensionTemplates"
                    :key="dimension.id"
                    @click="use(dimension)"
            >
                {{ dimension.name }}
            </Button>
            <span
                    v-if="dimensionTemplates.length === 0"
            >
                Keine Templates gefunden!
            </span>
            <Button @click="cancel">
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
        name: "ModalUseDimensionTemplate",
        components: {
            Button
        },
        data() {
            return {
                dimension: null,
                handler: null
            }
        },
        computed: {
            ...mapGetters("dimensions", ["dimensionTemplates"])
        },
        methods: {
            beforeOpen({params: {handler}}) {
                if (isNil(handler)) {
                    throw new Error("Parameter handler required!");
                }
                this.handler = handler;

                this.$load(
                    this.$store.dispatch("dimensions/fetchDimensionTemplates", {})
                )
                    .fork(
                        this.$handleApiError,
                        () => {
                        }
                    );
            },
            cancel() {
                this.$modal.hide("modal-use-dimension-template");
            },
            /**
             * Emits a "dimension-create" event with all needed data to cre-
             * ate the dimension.
             */
            use(dimension) {
                this.$modal.hide("modal-use-dimension-template");
                this.handler({
                    dimension,
                });
            }
        }
    }
</script>

<style lang="scss">
    @import "../../scss/_variables";

    .modal-use-dimension-template {
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
