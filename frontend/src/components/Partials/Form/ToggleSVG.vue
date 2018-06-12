<template>
    <svg class="toggle-svg"
         :class="classes"
         preserveAspectRatio="xMidYMid meet"
         viewBox="0 0 181 101"
    >
        <rect x="0" y="0" width="181" height="101"
              rx="50" ry="50"
              class="toggle-svg__background"
        />

        <rect :x="buttonX" y="10" width="81" height="81"
              rx="40" ry="40"
              class="toggle-svg__button"
        >
            <animate attributeName="x"
                     from="11" to="92" dur=".2"
                     ref="to-on"
                     begin="indefinite"
                     fill="freeze"
                     values="11; 92"
                     keyTimes="0; 1"
                     keySplines=".2 .3 .5 1"
                     calcMode="spline"
            />
            <animate attributeName="x"
                     from="92" to="11" dur="0.2"
                     ref="to-off"
                     begin="indefinite"
                     fill="freeze"
                     values="92; 11"
                     keyTimes="0; 1"
                     keySplines=".2 .3 .5 1"
                     calcMode="spline"
            />
        </rect>

        <rect x="0" y="0" width="181" height="101"
              rx="50" ry="50"
              class="toggle-svg__reactor"
              @click.prevent="toggle"
        />
    </svg>
</template>

<script>
    export default {
        name: "ToggleSVG",
        props: {
            /** @type Boolean */
            value: {
                type: Boolean,
            },
            /** If set to true, the toggle isn't usable. */
            disabled: {
                type: Boolean,
                default: false
            }
        },
        data() {
            return {
                on: false
            };
        },
        created() {
            this.on = this.value;
        },
        computed: {
            /**
             * Class object on the svg element.
             */
            classes() {
                return {
                    "toggle-svg--on": this.on,
                    "toggle-svg--off": !this.on,
                    "toggle-svg--disabled": this.disabled
                };
            },
            buttonX() {
                if (this.on) {
                    return 92;
                } else {
                    return 11;
                }
            }
        },
        methods: {
            toggle() {
                if (this.disabled) {
                    return;
                }

                this.on = !this.on;
                let animation;
                if (this.on) {
                    animation = this.$refs["to-on"];
                } else {
                    animation = this.$refs["to-off"];
                }
                animation.beginElement();
                this.$emit("input", this.on);
            }
        }
    }
</script>

<style lang="scss">
    @import "../../scss/_variables";

    .toggle-svg {
        &__background {
            fill: $slightlydark;
        }

        &__button {
            fill: $verylight;
        }

        &__reactor {
            fill: rgba(0, 0, 0, 0);
        }

        &--on {
            .toggle-svg__background {
                fill: $primary;
            }
        }

        &--disabled {
            .toggle-svg__background {
                fill: $slightlylight;
            }
        }
    }
</style>
