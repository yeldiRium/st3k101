<template>
    <div class="range-editor">
        <div class="range-editor__config">
            <label>
                start
                <input class="range-editor__input"
                       type="number"
                       name="start"
                       min="0"
                       :max="value.end - 1"
                       step="1"
                       :value="value.start"
                       @input="updateStart"
                >
            </label>
            <label>
                end
                <input class="range-editor__input"
                       type="number"
                       name="end"
                       :min="value.start + 1"
                       step="1"
                       :value="value.end"
                       @input="updateEnd"
                >
            </label>
        </div>
        <div class="range-editor__preview">
            <RangeSVG :range="value"
                      :preview="true"
            />
        </div>
    </div>
</template>

<script>
    import RangeSVG from "./RangeSVG";

    import Range from "../../../../model/SurveyBase/Config/Range";

    export default {
        name: "RangeEditor",
        components: {
            RangeSVG
        },
        props: {
            /** @type {Range} */
            value: {
                type: Range
            }
        },
        methods: {
            updateStart(event) {
                this.$emit(
                    "input",
                    new Range({
                        start: Number(event.target.value),
                        end: this.value.end
                    })
                );
            },
            updateEnd(event) {
                this.$emit(
                    "input",
                    new Range({
                        start: this.value.start,
                        end: Number(event.target.value)
                    })
                );
            }
        }
    }
</script>

<style lang="scss">
    @import "../../../scss/_variables";

    .range-editor {
        display: grid;
        justify-items: center;

        &__input {
            width: 3em;
        }

        &__preview {
            width: 100%;
        }
    }
</style>
