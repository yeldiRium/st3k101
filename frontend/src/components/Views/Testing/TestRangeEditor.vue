<template>
    <div class="TestRange_container">
        <RangeEditor/>
    </div>
</template>

<script>
    import RangeEditor from "../../Partials/SurveyBase/Config/RangeEditor";

    export default {
        name: "TestRange",
        components: {
            RangeEditor
        }
    }
</script>

<style lang="scss">
    .TestRange_container {
        width: 100%;
        height: 100%;

        padding: 0;
        margin: 0;
    }
</style>