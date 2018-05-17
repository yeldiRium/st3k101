<template>
    <div class="diamondFloatingButton-outer" :style="styles">
        <a :click="callback">
            <svg :viewBox="viewBox">
                <defs>
                    <DropShadowFilter :thickness="elevation/4"
                                      :offsetX="0"
                                      :offsetY="0"
                                      :width="width*1.5"
                                      :height="height*1.5"
                                      :x="-width*0.25"
                                      :y="-height*0.25"
                    />
                </defs>
                <Square class="shape_square"
                        :x="0.25*width"
                        :y="0.25*height"
                        :width="width"
                        :height="height"
                        :rx="radius"
                        :ry="radius"
                        :deg="45"
                        v-bind="$attrs"
                        filter="url(#DropShadowFilter)"
                />
            </svg>
        </a>
    </div>
</template>

<script>
    import Square from "../SVG/Shapes/Square";
    import DropShadowFilter from "../SVG/Filter/DropShadowFilter";

    import {atLeastZero} from "../../Validators";

    /**
     * Careful! Resulting element-size is always 1.5 times of the given value
     * due to the shadow taking up space around it.
     */
    export default {
        name: "DiamondFloatingButton",
        components: {Square, DropShadowFilter},
        props: {
            width: {
                type: Number,
                default: 48,
                validator: atLeastZero
            },
            height: {
                type: Number,
                default: 48,
                validator: atLeastZero
            },
            radius: {
                type: Number,
                default: 4,
                validator: atLeastZero
            },
            elevation: {
                type: Number,
                default: 12,
                validator: atLeastZero
            },
            /**
             * Executed when the button is clicked.
             */
            callback: {
                type: Function,
                default: () => null
            }
        },
        computed: {
            viewBox() {
                return `0 0 ${this.width*1.5} ${this.height*1.5}`;
            },
            styles() {
                return {
                    width: `${this.width*1.5}px`,
                    height: `${this.height*1.5}px`
                }
            }
        }
    };
</script>

<style lang="scss">
    .diamondFloatingButton-outer {
        > a {
            width: 100%;
            height: 100%;

            > svg {
                width: 100%;
                height: 100%;
            }
        }
    }

    .shape_square {
        fill: "#FFFFFF";
        stroke: "#000000";
        stroke-width: 3;
    }
</style>