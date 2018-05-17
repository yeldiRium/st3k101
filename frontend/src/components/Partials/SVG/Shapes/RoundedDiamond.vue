<template>
    <path :d="d"
             :fill="color"
             :stroke="borderColor"
             stroke-linejoin="round"
             :stroke-width="strokeWidth"></path>
</template>

<script>
    import {roundedDiamond} from "../Paths";

    const hexColorValidator = function (hexColor) {
        return hexColor.match(/^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$/) !== null;
    };

    export default {
        name: "DiamondFloatingButton",
        props: {
            color: {
                type: String,
                default: "#FFFFFF",
                validator: hexColorValidator
            },
            borderColor: {
                type: String,
                default: "#000000",
                validator: hexColorValidator
            },
            radius: {
                type: Number,
                default: 0,
                validator: a => a > 0
            },
            strokeWidth: {
                type: Number,
                default: 1,
                validator: a => a > 0
            },
            width: {
                type: Number,
                default: 48
            },
            height: {
                type: Number,
                default: 48
            },
            x: {
                type: Number,
                default: 0
            },
            y: {
                type: Number,
                default: 0
            }
        },
        computed: {
            d() {
                return roundedDiamond(this.width, this.height, this.radius, this.x, this.y);
            }
        }
    };
</script>

<style lang="scss">

</style>