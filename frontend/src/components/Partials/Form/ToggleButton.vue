<template>
    <div class="toggle-button"
         :class="classes"
    >
        <div class="toggle-button__off-side"
             :class="toggleButtonOffClasses"
        >
            <slot name="off" />
        </div>
        <div class="toggle-button__button">
            <ToggleSVG v-model="on"
                          :disabled="disabled"
                          @input="passToggle"
            />
        </div>
        <div class="toggle-button__on-side"
             :class="toggleButtonOnClasses"
        >
            <slot name="on" />
        </div>
    </div>
</template>

<script>
    import ToggleSVG from "./ToggleSVG";

    export default {
        name: "ToggleButton",
        components: {
            ToggleSVG
        },
        props: {
            value: {
                type: Boolean
            },
            disabled: {
                type: Boolean,
                default: false
            }
        },
        data() {
            return {
                on: true
            }
        },
        created() {
            this.on = this.value;
        },
        computed: {
            /** Classes on the outer div */
            classes() {
                return {
                    "toggle-button--on": this.on,
                    "toggle-button--off": !this.on,
                    "toggle-button--disabled": this.disabled
                };
            },
            toggleButtonOffClasses() {
                return {
                    "toggle-button__off-side--active": !this.on
                }
            },
            toggleButtonOnClasses() {
                return {
                    "toggle-button__on-side--active": this.on
                }
            }
        },
        methods: {
            passToggle(value) {
                this.$emit("input", value);
            }
        }
    }
</script>

<style lang="scss">
    @import "../../scss/_variables";

    .toggle-button {
        display: grid;
        grid-template-columns: auto 2em auto;
        grid-column-gap: 1em;
        grid-template-areas: "left toggle-button right";

        align-items: center;

        > div {
            color: $slightlylight;
        }

        &__off-side {
            grid-area: left;

            justify-self: end;

            &.toggle-button__off-side--active {
                color: $verydark;
            }
        }

        &__button {
            grid-area: toggle-button;

            -webkit-user-select: none;
            -moz-user-select: none;
            -ms-user-select: none;
            user-select: none;
        }

        &__on-side {
            grid-area: right;

            justify-self: start;

            &.toggle-button__on-side--active {
                color: $primary;
            }
        }

        &--disabled {
            &-off.toggle-button-off-active {
                color: $slightlydark;
            }

            &-on.toggle-button-on-active {
                color: $primary-light;
            }
        }
    }
</style>
