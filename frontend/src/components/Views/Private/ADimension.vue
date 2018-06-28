<template>
    <div class="a-dimension">
        <Dimension v-if="dimension"
                   :key="dimension.href"
                   :dimension="dimension"
                   :deletable="false"
                   :style="itemStyle"
                   :initiallyExpanded="true"
                   :showLink="false"
                   @updated="reloadDimension"
        />
    </div>
</template>

<script>
    import {mapGetters, mapState} from "vuex-fluture";
    import {isNil} from "ramda";

    import Dimension from "../../Partials/SurveyBase/Dimension";

    export default {
        name: "ADimension",
        components: {
            Dimension
        },
        data() {
            return {
                dimension: null
            };
        },
        created() {
            this.reloadDimension();

            if (isNil(this.dimension)) {
                this.$load(
                    this.$store.dispatch(
                        "dimensions/fetchDimension",
                        {
                            id: this.$route.params.id
                        }
                    )
                ).fork(
                    this.$handleApiError,
                    () => {
                        this.reloadDimension();
                    }
                );
            }
        },
        computed: {
            ...mapGetters("dimensions", ["dimensionById"]),
            ...mapState("global", ["window"]),
            itemStyle() {
                let width = "1200px";
                if (this.window.width * .8 < 1200) {
                    width = "80%";
                }

                return {
                    width: width
                };
            }
        },
        methods: {
            reloadDimension() {
                this.dimension = this.dimensionById(
                    Number(this.$route.params.id)
                );
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
