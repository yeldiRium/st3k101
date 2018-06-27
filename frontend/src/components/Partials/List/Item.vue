<template>
    <div class="list-item" :class="classes">
        <div class="list-item__text"
             :class="textClasses"
             :title="value"
             v-on="listeners"
        >
            <EditableText :value="value"
                          v-if="editableText && !disabled"
                          @input="$emit('input', $event)"
                          :ellipseText="ellipseText"
            />
            <template v-else>
                {{ value }}
            </template>
        </div>
        <div class="list-item__sub-text"
             :class="subTextClasses"
             :title="subtext"
             v-on="listeners"
        >
            {{ subtext }}
        </div>

        <div class="list-item̲_icons"
             v-if="icons"
        >
            <slot></slot>
        </div>
    </div>
</template>

<script>
    import {dissoc} from "ramda";

    import EditableText from "../Form/EditableText";

    export default {
        name: "ListItem",
        components: {
            EditableText
        },
        props: {
            value: {
                type: String
            },
            subtext: {
                type: String,
                default: ""
            },
            // Overrides editableText
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
            },
            editableText: {
                type: Boolean,
                default: true
            }
        },
        computed: {
            /**
             * Remove input listeners from passed events.
             * Since there is a manual listen on @input on the EditableText
             * component, this would make the listener redundant and fire on
             * unintended events.
             *
             * @returns {Object}
             */
            listeners() {
                return dissoc("input", this.$listeners);
            },
            classes() {
                return {
                    "list-item--mini": this.mini || this.subtext === "",
                    "list-item--big": !(this.mini || this.subtext === ""),
                    "list-item--disabled": this.disabled,
                    "list-item--with-icons": this.icons,
                    "list-item--no-icons": !this.icons
                };
            },
            textClasses() {
                return {
                    "list-item__text--ellipse": this.ellipseText
                }
            },
            subTextClasses() {
                return {
                    "list-item__sub-text--ellipse": this.ellipseSubText
                }
            }
        }
    }
</script>

<style lang="scss">
    @import "../../scss/_variables.scss";
    @import "../../scss/_mixins.scss";

    .list-item {
        min-height: 3em;

        display: grid;
        grid-template-columns: 2.5% 95% 2.5%;

        background-color: $primary;

        &--disabled {
            background-color: $slightlylight;
        }

        &--with-icons {
            grid-template-columns: 2.5% auto fit-content(25%) 2.5%;
        }

        &--no-icons .list-item̲_icons {
            display: none;
        }

        &--big {
            grid-template-areas: ". text ." ". subtext .";

            &.list-item--with-icons {
                grid-template-areas: ". text icons ." ". subtext icons .";
            }
        }

        &--mini {
            min-height: 2em;

            grid-template-rows: 100%;
            grid-template-areas: ". text .";

            &.list-item--with-icons {
                grid-template-areas: ". text icons .";
            }

            .list-item__text {
                align-self: center;
            }

            .list-item__sub-text {
                display: none;
            }
        }

        &__text {
            grid-area: text;
            align-self: end;

            font-size: 1.1em;

            &--ellipse {
                @include ellipse;
            }

            .editable-text {
                width: 100%;
            }
        }

        &__sub-text {
            grid-area: subtext;
            align-self: start;

            padding-right: 5px;

            font-size: 0.9em;

            &--ellipse {
                @include ellipse;
            }
        }

        &̲_icons {
            grid-area: icons;

            display: flex;
            align-items: center;
            justify-content: flex-end;
        }

        &__icon {
            fill: $verydark;

            margin-left: 0.5em;

            cursor: pointer;
        }
    }
</style>
