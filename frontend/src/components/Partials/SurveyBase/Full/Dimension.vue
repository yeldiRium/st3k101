<template>
    <div class="full-dimension"
         :class="classes"
         v-if="expanded"
    >
        <ListDimension :dimension="dimension"
                       :disableSubText="true"
                       :draggable="true"
                       :ellipseText="false"
                       @click="toggleExpanded"
        />

        <div class="full-dimension-body"
             ref="dropdown"
             v-if="expanded"
        >
            <ReferenceCounter :object="dimension"
                              v-if="dimension.isConcrete"
            />

            <!-- TODO: add body here -->

            <div class="full-dimension-delete"
                 v-if="!disabled(dimension)"
            >
                delete
            </div>
        </div>
    </div>
    <div class="full-dimension"
         :class="classes"
         v-else
    >
        <ListDimension :dimension="dimension"
                       :draggable="draggable"
                       :ellipseText="true"
                       @click="toggleExpanded"
        />
    </div>
</template>

<script>
    import DimensionBase from "../DimensionBase";
    import ListDimension from "../List/Dimension";
    import ReferenceCounter from "../Config/ReferenceCounter";

    export default {
        name: "Full-Dimension",
        extends: DimensionBase,
        components: {
            ListDimension,
            ReferenceCounter
        },
        props: {
            initiallyExpanded: {
                type: Boolean,
                default: false
            }
        },
        data() {
            return {
                expanded: false,
                header: {
                    height: 0
                },
                dropdown: {
                    height: 0
                }
            }
        },
        computed: {
            classes() {
                return {
                    disabled: this.disabled(this.dimension)
                }
            }
        },
        methods: {
            toggleExpanded() {
                this.expanded = !this.expanded;
            },
        },
        created() {
            this.expanded = this.initiallyExpanded;
        }
    }
</script>

<style lang="scss">
    @import "../../../scss/_variables";

    .list-item.list-dimension {
        cursor: pointer;

        background-color: $primary;

        &.disabled {
            background-color: $slightlylight;
        }
    }

    .full-dimension {
        display: flex;
        flex-flow: column;

        background-color: $primary-light;

        &.disabled {
            background-color: $lighter;
        }
    }

    .full-dimension-body {
        display: flex;
        flex-flow: column;
        align-items: center;

        .referencecounter {
            margin-bottom: 8px;
        }

        .full-dimension-delete {
            margin-top: 8px;
        }
    }
</style>
