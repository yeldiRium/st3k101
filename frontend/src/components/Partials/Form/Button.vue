<template>
    <div class="button"
         :class="classes"
         v-on="$listeners"
         @mouseover="raise"
         @mouseout="lower"
    >
        <slot></slot>
    </div>
</template>

<script>
    /**
     * A button that is styled and supports raising elevation on mouseover.
     */
    export default {
        name: "Button",
        props: {
            elevation: {
                type: Number,
                default: 0
            },
            offset: {
                type: Number,
                default: 6
            }
        },
        data() {
            return {
                elevationOffset: 0
            }
        },
        computed: {
            /**
             * Calculate elevation based on offset and initial elevation.
             * Maximum is 24, since elevation level are only defined up to 24.
             *
             * @returns {Number}
             */
            actualElevation() {
                return Math.min(this.elevation + this.elevationOffset, 24);
            },
            /**
             * Sets the elevation class for the button.
             * @returns {Array<String>}
             */
            classes() {
                return [`elevation-${this.actualElevation}`];
            }
        },
        methods: {
            /**
             * Raises the button elevation offset to the predefined offset.
             */
            raise() {
                this.elevationOffset = this.offset;
            },
            /**
             * Lowers the button elevation offset to 0.
             */
            lower() {
                this.elevationOffset = 0;
            }
        }
    }
</script>

<style lang="scss">
    @import "../../scss/_variables";
    @import "../../scss/_elevation";

    .button {
        height: 1em;
        padding: 0.3em 0.5em 0.3em 0.5em;
        -webkit-border-radius: 3px;
        -moz-border-radius: 3px;
        border-radius: 3px;

        background-color: $primary-light;

        text-align: center;
    }
</style>
