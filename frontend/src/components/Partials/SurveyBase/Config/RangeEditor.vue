<template>
    <div class="rangeeditor">
        <div class="rangeeditor-config">
            <label>
                start
                <input type="number"
                       name="start"
                       class="rangeeditor-config-input"
                       v-model="range.start"
                >
            </label>
            <label>
                end
                <input type="number"
                       name="end"
                       class="rangeeditor-config-input"
                       v-model="range.end"
                >
            </label>
        </div>
        <div class="rangeeditor-preview">
            <RangeComponent :range="range"
                            :preview="false"
                            :startSelector="3"
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
