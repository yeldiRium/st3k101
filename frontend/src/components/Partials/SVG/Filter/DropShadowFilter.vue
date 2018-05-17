<template>
    <filter id="DropShadowFilter">
        <feGaussianBlur in="SourceAlpha" :stdDeviation="thickness"/>
        <!-- stdDeviation is how much to blur -->
        <feOffset :dx="offsetX" :dy="offsetY" result="offsetblur"/>
        <!-- how much to offset -->
        <feComponentTransfer>
            <feFuncA type="linear" :slope="opacity"/>
            <!-- slope is the opacity of the shadow -->
        </feComponentTransfer>
        <feMerge>
            <feMergeNode/> <!-- this contains the offset blurred image -->
            <feMergeNode in="SourceGraphic"/>
            <!-- this contains the element that the filter is applied to -->
        </feMerge>
    </filter>
</template>

<script>
    export default {
        name: "DropShadowFilter",
        props: {
            opacity: {
                type: Number,
                default: 0.5,
                validator: a => (0 <= a && a <= 1)
            },
            offsetX: {
                type: Number,
                default: 0,
                validator: a => a >= 0
            },
            offsetY: {
                type: Number,
                default: 0,
                validator: a => a >= 0
            },
            thickness: {
                type: Number,
                default: 0,
                validator: a => a >= 0
            }
        }
    }
</script>

<style lang="scss">

</style>