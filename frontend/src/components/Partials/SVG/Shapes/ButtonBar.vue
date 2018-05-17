<template>
    <polygon :points="points"
    />
</template>

<script>
    import {atLeastZero} from "../../../Validators";

    export default {
        name: "SVGButtonBar",
        props: {
            num: {
                type: Number,
                default: 1,
                validator: atLeastZero
            },
            buttonSize: {
                type: Number,
                default: 48,
                validator: atLeastZero
            },
            padding: {
                type: Number,
                default: 8,
                validator: atLeastZero
            },
            spacing: {
                type: Number,
                default: 24,
                validator: atLeastZero
            }
        },
        computed: {
            points() {
                let out = "0,0";
// es muss seine breite wissen <.<
                    out += ""
            }
        }
    }
</script>

<style lang="scss">

</style>