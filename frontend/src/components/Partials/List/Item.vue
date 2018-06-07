<template>
    <div class="list-item" :class="classes">
        <div class="list-item-text"
             :class="textClasses"
             :title="text"
        >
            {{ text }}
        </div>
        <div class="list-item-subtext"
             :class="subTextClasses"
             :title="subtext"
        >
            {{ subtext }}
        </div>

        <div class="list-item-icons"
             v-if="icons"
        >
            <slot></slot>
        </div>
    </div>
</template>

<script>
    export default {
        name: "List-Item",
        props: {
            text: {
                type: String
            },
            subtext: {
                type: String
            },
            disabled: {
                type: Boolean,
                default: false
            },
            mini: {
                type: Boolean,
                default: false
            },
            icons: {
                type: Boolean,
                default: true
            },
            ellipseText: {
                type: Boolean,
                default: true
            },
            ellipseSubText: {
                type: Boolean,
                default: true
            }
        },
        computed: {
            classes() {
                return {
                    mini: this.mini,
                    big: !this.mini,
                    disabled: this.disabled,
                    icons: this.icons,
                    "no-icons": !this.icons
                };
            },
            textClasses() {
                return {
                    ellipse: this.ellipseText
                }
            },
            subTextClasses() {
                return {
                    ellipse: this.ellipseSubText
                }
            }
        }
    }
</script>

<style lang="scss">
    @import "../../scss/_variables.scss";
    @import "../../scss/_mixins.scss";

    .list-item {
        display:grid;
        grid-template-columns: 2.5% 95% 2.5%;

        background-color: $primary-light;

        &.big {
            grid-template-areas: ". text ." ". subtext .";

            &.icons {
                grid-template-columns: 2.5% 70% 25% 2.5%;
                grid-template-areas: ". text icons ." ". subtext icons .";
            }
        }

        &.mini {
            grid-template-rows: 100%;
            grid-template-areas: ". text .";

            &.icons {
                grid-template-columns: 2.5% 70% 25% 2.5%;
                grid-template-areas: ". text icons .";
            }

            .list-item-text {
                align-self: center;
            }

            .list-item-subtext {
                display: none;
            }
        }

        &.no-icons .list-item-icons {
            display: none;
        }
    }

    .list-item-text {
        grid-area: text;
        align-self: end;

        font-size: 1.1em;

        &.ellipse {
            @include ellipse;
        }
    }

    .list-item-subtext {
        grid-area: subtext;
        align-self: start;

        font-size: 0.9em;

        &.ellipse {
            @include ellipse;
        }
    }

    .list-item-icons {
        grid-area: icons;

        display: flex;
        align-items: center;
        justify-content: flex-end;

        > .list-item-icon {
            fill: $verydark;

            margin-left: 0.5em;
        }
    }

    .list-item.disabled {
        background-color: $lighter;
    }
</style>