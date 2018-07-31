<template>
    <svg class="range-svg"
         :style="svgStyle"
    >
        <line :x1="`${(100-width)/2}%`"
              :y1="`${lineY}%`"
              :x2="`${(100-width)/2 + width}%`"
              :y2="`${lineY}%`"
              class="range-svg__middle-line"
        />

        <g>
            <line v-for="number in range.numbers"
                  :key="`number${number}`"
                  :x1="`${numberX(number)}%`"
                  :y1="`${lineY1}%`"
                  :x2="`${numberX(number)}%`"
                  :y2="`${lineY2}%`"
                  class="range-svg__number-line"
                  :class="[`range-svg__number-line-${number}`]"
            />
        </g>

        <g v-if="!preview">
            <g v-for="number in range.numbers"
               :key="`reactor${number}`"
               class="range-svg__number-reactor"
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

            <g class="range-svg__selector">
                <line :x1="`${numberX(selector)}%`"
                      :y1="`${selectorLineY1}%`"
                      :x2="`${numberX(selector)}%`"
                      :y2="`${selectorLineY2}%`"
                      class="range-svg__selector-line"
                />
                <text :x="`${numberX(selector)}%`"
                      :y="`${selectorNumberY}%`"
                      text-anchor="middle"
                      class="range-svg__selector-number"
                >
                    {{ selector }}
                </text>
            </g>
        </g>

        <g>
            <g v-if="preview">
                <text v-for="number in range.numbers"
                      :key="`label${number}`"
                      :x="`${numberX(number)}%`"
                      :y="`${numberY}%`"
                      text-anchor="middle"
                      class="range-svg__number"
                >
                    {{ number }}
                </text>
            </g>
            <g v-else>
                <text v-if="selector !== range.start"
                      :x="`${numberX(range.start)}%`"
                      :y="`${numberY}%`"
                      text-anchor="middle"
                      class="range-svg__number"
                      :class="[`range-svg__number-${range.start}`]"
                >
                    {{ range.start }}
                </text>
                <text v-if="selector !== range.end"
                      :x="`${numberX(range.end)}%`"
                      :y="`${numberY}%`"
                      text-anchor="middle"
                      class="range-svg__number"
                      :class="[`range-svg__number-${range.end}`]"
                >
                    {{ range.end }}
                </text>
            </g>
        </g>
    </svg>
</template>

<script>
    import {isNil, contains, forEach} from "ramda";

    import Range from "../../../../model/SurveyBase/Config/Range";

    export default {
        name: "RangeSVG",
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
                type: Number
            }
        },
        data() {
            return {
                selector: this.range.start,
                // In %
                width: 80
            }
        },
        created() {
            if (!isNil(this.startSelector)) {
                if (contains(this.startSelector, this.range.numbers)) {
                    this.selector = this.startSelector;
                }
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
                const lines = this.$el.getElementsByClassName(
                    `range-svg__number-line-${number}`
                );
                const texts = this.$el.getElementsByClassName(
                    `range-svg__number-${number}`
                );

                forEach(
                    elem => elem.classList.add("range-svg--hover"),
                    lines
                );
                forEach(
                    elem => elem.classList.add("range-svg--hover"),
                    texts
                );
            },
            endHover(number) {
                const lines = this.$el.getElementsByClassName(
                    `range-svg__number-line-${number}`
                );
                const texts = this.$el.getElementsByClassName(
                    `range-svg__number-${number}`
                );

                forEach(
                    elem => elem.classList.remove("range-svg--hover"),
                    lines
                );
                forEach(
                    elem => elem.classList.remove("range-svg--hover"),
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
            "range.start": function (newStart, oldStart) {
                if (!contains(this.selector, this.range.numbers)) {
                    this.selector = newStart;
                }
            },
            "range.end": function (newEnd, oldEnd) {
                if (!contains(this.selector, this.range.numbers)) {
                    this.selector = newEnd;
                }
            }
        }
    }
</script>

<style lang="scss">
    @import "../../../scss/_variables";

    .range-svg {
        width: 100%;

        &__middle-line {
            stroke: $slightlydark;
        }

        &__number-line {
            stroke: $slightlydark;
            stroke-width: 2px;
        }

        &__selector-line {
            stroke: $primary;
        }

        &__number-line.range-svg--hover {
            stroke: $primary;
        }

        &__number, &-selector-number {
            fill: $verydark;
        }

        &__number.range-svg--hover {
            stroke: $primary;
        }

        &__number-reactor {
            fill: rgba(0, 0, 0, 0);
        }

        &__selector {
            &-line {
                stroke-width: 3px;
            }

            &-number {
                font-size: 1.2em;
            }
        }
    }
</style>
