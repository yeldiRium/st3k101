<template>
    <div class="a-dimension">
        <Dimension :key="dimension.href"
                  :dimension="dimension"
                  :deletable="false"
                  :style="itemStyle"
                  :initiallyExpanded="true"
        />
    </div>
</template>

<script>
    import {mapGetters, mapState} from "vuex-fluture";

    import Dimension from "../../Partials/SurveyBase/Dimension";

    export default {
        name: "ADimension",
        components: {
            Dimension
        },
        computed: {
            ...mapGetters("dimensions", ["dimensionById"]),
            ...mapState("global", ["window"]),
            dimension() {
                return this.dimensionById(this.$route.params.id);
            },
            itemStyle() {
                let width = "1200px";
                if (this.window.width * .8 < 1200) {
                    width = "80%";
                }

                return {
                    width: width
                };
            }
        }
    }
</script>

<style lang="scss">
    .a-dimension {
        display: grid;
        grid-template-columns: 100%;
        grid-auto-flow: row;
        grid-row-gap: 0.5em;

        justify-items: center;
    }
</style>
