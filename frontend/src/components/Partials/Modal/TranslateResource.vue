<template>
    <div class="modal-translate-resource">
        <div class="modal-translate-resource__header">
            <slot name="header"></slot>
        </div>
        <div class="modal-translate-resource__body">
            <slot name="body"></slot>
        </div>
        <div class="modal-translate-resource__buttons">
            <slot name="buttons"></slot>
            <template v-if="defaultButtons">
                <div class="modal-translate-resource__button">
                    <Button :offset="4"
                            @click="cancel"
                    >
                        Cancel
                    </Button>
                </div>
                <div class="modal-translate-resource__button">
                    <Button :offset="4"
                            @click="translate"
                    >
                        Add translation
                    </Button>
                </div>
            </template>
        </div>
    </div>
</template>

<script>
    import {has} from "ramda";

    import Button from "../Form/Button";

    export default {
        name: "ModalTranslateResource",
        components: {
            Button
        },
        computed: {
            /**
             * Returns true, if there is no content in the "buttons" slot and
             * thus the default buttons should be rendered.
             * @returns {boolean}
             */
            defaultButtons() {
                return !has("buttons", this.$slots);
            }
        },
        methods: {
            cancel() {
                this.$emit("cancel");
            },
            translate() {
                this.$emit("translate");
            },
            onKeyUp() {
                // Enter key was pressed
                if (event.which == 13) {
                    this.$emit("translate");
                    return;
                }

                // Escape key was pressed
                if (event.which == 27) {
                    this.$emit("cancel");
                    return;
                }
            }
        },
        beforeMount() {
            window.addEventListener("keyup", this.onKeyUp);
        },
        beforeDestroy() {
            window.removeEventListener("keyup", this.onKeyUp);
        }
    }
</script>

<style lang="scss">
    @import "../../scss/_variables";

    .modal-translate-resource {
        display: grid;
        grid-template-rows: 2em auto 2em;
        grid-row-gap: 10px;

        &__header {
            background-color: $primary-light;

            font-size: 1.4em;
            text-align: center;
        }

        &__body {
            padding-left: 20px;
            padding-right: 20px;

            display: flex;
            flex-flow: column;
            align-items: center;

            > * {
                margin-bottom: 10px;
            }
        }

        &__buttons {
            padding: 0 20px 0 20px;

            display: grid;
            grid-auto-columns: 1fr;
            grid-auto-flow: column;
            grid-column-gap: 1em;
            justify-content: center;
        }

        &__button {
            flex-grow: 1;
        }
    }
</style>
