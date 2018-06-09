<template>
    <div class="rangeeditor">
        <div class="rangeeditor-config">
            <label>
                start
                <input type="number"
                       name="start"
                       min="0"
                       step="1"
                       :max="range.end - 1"
                       class="rangeeditor-config-input"
                       v-model="range.start"
                >
            </label>
            <label>
                end
                <input type="number"
                       name="end"
                       :min="range.start + 1"
                       step="1"
                       class="rangeeditor-config-input"
                       v-model="range.end"
                >
            </label>
        </div>
        <div class="rangeeditor-preview">
            <RangeComponent :range="range"
                            :preview="true"
            />
        </div>
    </div>
</template>

<script>
    import Range from "../../../../model/SurveyBase/Config/Range";
    import RangeComponent from "./Range";

    export default {
        name: "RangeEditor",
        components: {
            RangeComponent
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

    .rangeeditor {
        display: grid;
        justify-items: center;

        &-config-input {
            width: 3em;
        }

        &-preview {
            width: 100%;
        }
    }
</style>
