<template>
    <div class="diamondFloatingButton-outer">
        <a :click="callback">
            <svg viewBox="0 0 64 64">
                <defs>
                    <DropShadowFilter :thickness="3"
                                      :offsetX="0"
                                      :offsetY="0"
                                      :width="64"
                                      :height="64"
                                      :x="-8"
                                      :y="-8"
                    />
                </defs>
                <RoundedDiamond :color="color"
                                :border-color="borderColor"
                                :radius="4"
                                :x="8"
                                :y="8"
                                :width="48"
                                :height="48"
                                :strokeWidth="2"
                                filter="url(#DropShadowFilter)"
                />
            </svg>
        </a>
    </div>
</template>

<script>
    import RoundedDiamond from "../SVG/Shapes/RoundedDiamond";
    import DropShadowFilter from "../SVG/Filter/DropShadowFilter";

    export default {
        name: "DiamondFloatingButton",
        components: {RoundedDiamond, DropShadowFilter},
        props: {
            color: {
                type: String,
                default: "#FFFFFF"
            },
            borderColor: {
                type: String,
                default: "#000000"
            },
            /**
             * Executed when the button is clicked.
             */
            callback: {
                type: Function,
                default: () => null
            }
        }
    };
</script>

<style lang="scss">
    .diamondFloatingButton-outer {
        width: 64px;
        height: 64px;

        > a {
            width: 100%;
            height: 100%;

            > svg {
                width: 100%;
                height: 100%;
            }
        }
    }
</style>