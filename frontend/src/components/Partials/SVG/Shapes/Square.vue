<template>
    <rect :x="x"
          :y="y"
          :width="rectWidth"
          :height="rectHeight"
          :transform="transform"
          v-bind="$attrs"
    />
</template>

<script>
    /**
     * The Square is a Square-Shape, which can be rotated without changing its
     * bounding box's width and height.
     */
    export default {
        name: "Square",
        props: {
            x: {
                type: Number,
                default: 0
            },
            y: {
                type: Number,
                default: 0
            },
            width: {
                type: Number,
                default: 48
            },
            height: {
                type: Number,
                default: 48
            },
            deg: {
                type: Number,
                default: 0
            }
        },
        /**
         * The square has to be fully translated before the rotation. otherwise
         * it'll be all over the place.
         * If the square will be rotated, its width and height change. So when
         * the square is positioned, it's translated by x and y and its width
         * and height are scaled.
         * Its center point thus is no longer at the center of the bounding box,
         * which is the rotation center used below.
         * To fix this, the square has to be translated by half the missing
         * width and heigh, so that the center points align again.
         */
        computed: {
            sizeFactor() {
                const rad = this.deg*2*Math.PI/360;
                return Math.sqrt(
                    (Math.cos(rad)/(Math.cos(rad)+Math.sin(rad)))**2 +
                    (Math.sin(rad)/(Math.sin(rad)+Math.cos(rad)))**2
                );
            },
            rectWidth() {
                console.log(this.sizeFactor);
                return this.sizeFactor * this.width;
            },
            rectHeight() {
                return this.sizeFactor * this.height;
            },
            transform() {
                return `rotate(${this.deg} ${this.x + this.width / 2} ${this.y + this.height / 2})`
                    + ` translate(${(this.width - this.rectWidth) / 2} ${(this.height - this.rectHeight) / 2})`;
            }
        }
    };
</script>

<style lang="scss">

</style>
