<template>
    <div class="popup-createresource">
        <div class="popup-createresource-header">
            <slot name="header"></slot>
        </div>
        <div class="popup-createresource-body">
            <slot name="body"></slot>
        </div>
        <div class="popup-createresource-buttons">
            <slot name="buttons"></slot>
            <template v-if="defaultButtons">
                <div class="popup-createresource-button">
                    <Button :offset="4"
                            @click="cancel"
                    >
                        Cancel
                    </Button>
                </div>
                <div class="popup-createresource-button">
                    <Button :offset="4"
                            @click="create"
                    >
                        Create
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
        name: "Popup-CreateResource",
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
            create() {
                this.$emit("create");
            }
        }
    }
</script>

<style lang="scss">
    @import "../../scss/_variables";

    .popup-createresource {
        display: grid;
        grid-template-rows: 2em auto 2em;
        grid-row-gap: 10px;

        &-header {
            background-color: $primary-light;

            font-size: 1.4em;
            text-align: center;
        }

        &-body {
            padding-left: 20px;
            padding-right: 20px;

            display: flex;
            flex-flow: column;
            align-items: center;

            > * {
                margin-bottom: 10px;
            }
        }

        &-buttons {
            padding: 0 20px 0 20px;

            display: grid;
            grid-auto-columns: 1fr;
            grid-auto-flow: column;
            grid-column-gap: 1em;
            justify-content: center;
        }

        &-button {
            flex-grow: 1;
        }
    }
</style>
