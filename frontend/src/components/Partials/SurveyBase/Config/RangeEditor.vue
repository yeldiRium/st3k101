<template>
    <div class="range-editor">
        <div class="range-editor__config">
            <label>
                start
                <input type="number"
                       name="start"
                       min="0"
                       step="1"
                       :max="range.end - 1"
                       class="range-editor__input"
                       v-model="range.start"
                >
            </label>
            <label>
                end
                <input type="number"
                       name="end"
                       :min="range.start + 1"
                       step="1"
                       class="range-editor__input"
                       v-model="range.end"
                >
            </label>
        </div>
        <div class="range-editor__preview">
            <RangeSVG :range="range"
                            :preview="true"
            />
        </div>
    </div>
</template>

<script>
    import Range from "../../../../model/SurveyBase/Config/Range";
    import RangeSVG from "./RangeSVG";

    export default {
        name: "RangeEditor",
        components: {
            RangeSVG
        },
        props: {
            /** @type {Range} */
            range: {
                type: Range
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
