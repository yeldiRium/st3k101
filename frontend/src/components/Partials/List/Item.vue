<template>
    <div class="list-item" :class="classes">
        <div class="list-item-text" :title="text">
            {{ text }}
        </div>
        <div class="list-item-subtext" :title="subtext">
            {{ subtext }}
        </div>

        <div class="list-item-icons">
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
            }
        },
        computed: {
            classes() {
                return {
                    mini: this.mini,
                    disabled: this.disabled
                };
            }
        }
    }
</script>

<style lang="scss">
    @import "../../scss/_variables.scss";

    .list-item {
        display: grid;
        grid-template-columns: 2.5% 70% 25% 2.5%;
        grid-template-rows: 50% 50%;
        grid-template-areas: ". text icons ." ". subtext icons .";

        background-color: $primary;
    }

    .list-item-text {
        grid-area: text;
        align-self: end;
        max-height: 100%;
        overflow: hidden;

        font-size: 1.1em;
        white-space: nowrap;
        text-overflow: ellipsis;
    }

    .list-item-subtext {
        grid-area: subtext;
        align-self: start;
        max-height: 100%;
        overflow: hidden;

        font-size: 0.9em;
        white-space: nowrap;
        text-overflow: ellipsis;
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

    .list-item.mini {
        grid-template-rows: 100%;
        grid-template-areas: ". text icons .";

        .list-item-text {
            align-self: center;
        }
    }

    .list-item.disabled {
        background-color: $lighter;
    }
</style>