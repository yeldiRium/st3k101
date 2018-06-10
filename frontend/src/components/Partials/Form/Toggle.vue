<template>
    <div class="toggle"
         :class="classes"
    >
        <div class="toggle-off"
             :class="toggleOffClasses"
        >
            <slot name="off" class="blub" />
        </div>
        <div class="toggle-button">
            <ToggleButton v-model="on"
                          :disabled="disabled"
                          @input="passToggle"
            />
        </div>
        <div class="toggle-on"
             :class="toggleOnClasses"
        >
            <slot name="on" />
        </div>
    </div>
</template>

<script>
    import ToggleButton from "./ToggleButton";

    export default {
        name: "Toggle",
        components: {
            ToggleButton
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
                    "toggle-on": this.on,
                    "toggle-off": !this.on,
                    "toggle-disabled": this.disabled
                };
            },
            toggleOffClasses() {
                return {
                    "toggle-off-active": !this.on
                }
            },
            toggleOnClasses() {
                return {
                    "toggle-on-active": this.on
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

    .toggle {
        display: grid;
        grid-template-columns: auto 2em auto;
        grid-column-gap: 1em;
        grid-template-areas: "left toggle right";

        > div {
            height: 1em;

            color: $slightlylight;
        }

        &-off {
            grid-area: left;

            justify-self: end;

            &.toggle-off-active {
                color: $verydark;
            }
        }

        &-button {
            grid-area: toggle;

            .togglebutton {
                width: 100%;
                height: 100%;
            }

            -webkit-user-select: none;
            -moz-user-select: none;
            -ms-user-select: none;
            user-select: none;
        }

        &-on {
            grid-area: right;

            justify-self: start;

            &.toggle-on-active {
                color: $primary;
            }
        }

        &-disabled {
            .toggle {
                &-off.toggle-off-active {
                    color: $slightlydark;
                }

                &-on.toggle-on-active {
                    color: $primary-light;
                }
            }
        }
    }
</style>
