<template>
    <svg class="rangesvg"
         :style="svgStyle"
    >
        <line :x1="`${(100-width)/2}%`"
              :y1="`${lineY}%`"
              :x2="`${(100-width)/2 + width}%`"
              :y2="`${lineY}%`"
              class="rangesvg-middleline"
        />

        <g>
            <line v-for="number in range.numbers"
                  :key="`number${number}`"
                  :x1="`${numberX(number)}%`"
                  :y1="`${lineY1}%`"
                  :x2="`${numberX(number)}%`"
                  :y2="`${lineY2}%`"
                  class="rangesvg-numberline"
                  :class="[`rangesvg-numberline-${number}`]"
            />
        </g>

        <g v-if="!preview">
            <g v-for="number in range.numbers"
               :key="`reactor${number}`"
               class="rangesvg-number-reactor"
            >
                <rect :x="`${reactorX(number)}%`"
                      :y="`${reactorY}%`"
                      :width="`${reactorWidth}%`"
                      :height="`${reactorHeight}%`"
                      @mouseenter="startHover(number)"
                      @mouseleave="endHover(number)"
                      @click="setSelector(number)"
                />
            </g>

            <line :x1="`${numberX(selector)}%`"
                  :y1="`${selectorLineY1}%`"
                  :x2="`${numberX(selector)}%`"
                  :y2="`${selectorLineY2}%`"
                  class="rangesvg-selectorline"
            />
            <text :x="`${numberX(selector)}%`"
                  :y="`${selectorNumberY}%`"
                  text-anchor="middle"
                  class="rangesvg-selectornumber"
            >
                {{ selector }}
            </text>
        </g>

        <g>
            <g v-if="preview">
                <text v-for="number in range.numbers"
                      :key="`label${number}`"
                      :x="`${numberX(number)}%`"
                      :y="`${numberY}%`"
                      text-anchor="middle"
                      class="rangesvg-number"
                >
                    {{ number }}
                </text>
            </g>
            <g v-else>
                <text v-if="selector !== range.start"
                      :x="`${numberX(range.start)}%`"
                      :y="`${numberY}%`"
                      text-anchor="middle"
                      class="rangesvg-number"
                      :class="[`rangesvg-number-${range.start}`]"
                >
                    {{ range.start }}
                </text>
                <text v-if="selector !== range.end"
                      :x="`${numberX(range.end)}%`"
                      :y="`${numberY}%`"
                      text-anchor="middle"
                      class="rangesvg-number"
                      :class="[`rangesvg-number-${range.end}`]"
                >
                    {{ range.end }}
                </text>
            </g>
        </g>
    </svg>
</template>

<script>
    import {concat, contains, map} from "ramda";

    import Range from "../../../../model/SurveyBase/Config/Range";

    export default {
        name: "Range",
        props: {
            range: {
                type: Range
            },
            /**
             * If true, all numbers are shown and nothing can be selected.
             */
            preview: {
                type: Boolean,
                default: false
            },
            /**
             * The currently selected number.
             * Irrelevant, if preview is true.
             */
            startSelector: {
                type: Number,
                default: 0
            }
        },
        data() {
            return {
                selector: 0,
                // In %
                width: 80
            }
        },
        created() {
            if (contains(this.startSelector, this.range.numbers)) {
                this.selector = this.startSelector;
            } else {
                this.selector = this.range.start;
            }
        },
        computed: {
            svgStyle() {
                if (this.preview) {
                    return {
                        height: "2em"
                    };
                } else {
                    return {
                        height: "3em"
                    };
                }
            },
            gap() {
                return this.width / (this.range.span - 1);
            },
            offset() {
                if (this.preview) {
                    return 20;
                } else {
                    return 10;
                }
            },
            /**
             * Y for middleline.
             */
            lineY() {
                return 65 + this.offset;
            },
            /**
             * Y for upper end of numberlines.
             */
            lineY1() {
                return 50 + this.offset;
            },
            /**
             * Y for lower end of numberlines.
             */
            lineY2() {
                return 80 + this.offset;
            },
            /**
             * Y for numbers.
             */
            numberY() {
                return 40 + this.offset;
            },
            // The reactor is the rectangle that reacts to clicking and dragging
            // and modifies the selector.
            /**
             * Y for reactor.
             */
            reactorY() {
                return 0;
            },
            /**
             * Width for reactor.
             */
            reactorWidth() {
                return this.gap;
            },
            /**
             * Height for reactor.
             */
            reactorHeight() {
                return 100;
            },
            // The selector displays the currently selected value.
            /**
             * Y for upper end of selectorline.
             */
            selectorLineY1() {
                return 40 + this.offset;
            },
            /**
             * Y for lower end of selectorline.
             */
            selectorLineY2() {
                return 90 + this.offset;
            },
            /**
             * Y for selector number.
             */
            selectorNumberY() {
                return 30 + this.offset;
            }
        },
        methods: {
            numberX(number) {
                return 10 + (number - this.range.start) * this.gap;
            },
            reactorX(number) {
                return this.numberX(number) - this.gap / 2;
            },
            startHover(number) {
                const lines = document.getElementsByClassName(
                    `rangesvg-numberline-${number}`
                );
                const texts = document.getElementsByClassName(
                    `rangesvg-number-${number}`
                );

                map(
                    elem => elem.classList.add("hover"),
                    lines
                );
                map(
                    elem => elem.classList.add("hover"),
                    texts
                );
            },
            endHover(number) {
                const lines = document.getElementsByClassName(
                    `rangesvg-numberline-${number}`
                );
                const texts = document.getElementsByClassName(
                    `rangesvg-number-${number}`
                );

                map(
                    elem => elem.classList.remove("hover"),
                    lines
                );
                map(
                    elem => elem.classList.remove("hover"),
                    texts
                );
            },
            /**
             * Set the selector to the given number.
             *
             * @param {number} number
             */
            setSelector(number) {
                this.selector = number;
            }
        },
        watch: {
            selector(newSelector, oldSelector) {
                this.$emit("selector-change", newSelector);
            },
            "range.start": function(newStart, oldStart) {
                if (!contains(this.selector, this.range.numbers)) {
                    this.selector = newStart;
                }
            },
            "range.end": function(newEnd, oldEnd) {
                if (!contains(this.selector, this.range.numbers)) {
                    this.selector = newEnd;
                }
            }
        }
    }
</script>

<style lang="scss">
    @import "../../../scss/_variables";

    .rangesvg {
        width: 100%;

        &-middleline, &-numberline, &-selectorline {
            stroke: $verydark;
            stroke-width: 2px;
        }

        &-numberline.hover {
            stroke: $primary;
        }

        &-number, &-selectornumber {
            fill: $verydark;
        }

        &-number.hover {
            stroke: $primary;
        }

        &-number-reactor {
            fill: rgba(0, 0, 0, 0);
        }

        &-selectorline {
            stroke-width: 3px;
        }

        &-selectornumber {
            font-size: 1.2em;
        }
    }
</style>
