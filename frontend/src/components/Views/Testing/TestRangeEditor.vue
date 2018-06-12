<template>
    <div class="TestRangeEditor_container">
        <RangeEditor :range="range"
        />
        <RangeSVG :range="range"
                  :preview="false"
        />
    </div>
</template>

<script>
    import RangeEditor from "../../Partials/SurveyBase/Config/RangeEditor";
    import RangeSVG from "../../Partials/SurveyBase/Config/RangeSVG";
    import Range from "../../../model/SurveyBase/Config/Range";

    export default {
        name: "TestRange",
        components: {
            RangeEditor,
            RangeSVG
        },
        data() {
            return {
                range: new Range({start: 0, end: 10})
            }
        }
    }
</script>

<style lang="scss">
    .TestRangeEditor_container {
        width: 100%;
        height: 100%;

        padding: 0;
        margin: 0;
    }

    .range-editor {
        width: 400px;
    }
</style>