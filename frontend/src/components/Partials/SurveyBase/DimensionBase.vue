<template>
</template>

<script>
    import {Dimension} from "../../../model/SurveyBase/Dimension";

    import SurveyBase from "./SurveyBase";

    /**
     * Defines some properties and computed propertes for Dimensions.
     */
    export default {
        name: "DimensionBase",
        extends: SurveyBase,
        props: {
            /** @type {Dimension} */
            dimension: {
                type: Dimension
            },
        }
    }
</script>

<style lang="scss">
</style>
