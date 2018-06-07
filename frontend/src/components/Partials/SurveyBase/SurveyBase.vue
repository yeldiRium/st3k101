<template>
</template>

<script>
    import {mapGetters} from "vuex";

    /**
     * Defines some properties and methods for OwnedResources.
     *
     * Can and should be used as BaseComponent for all SurveyBase components.
     */
    export default {
        name: "SurveyBase",
        props: {
            /** @type boolean */
            draggable: {
                type: Boolean,
                default: true
            }
        },
        computed: {
            ...mapGetters("session", ["dataClient"])
        },
        methods: {
            /**
             * Whether the given resource is owned by the current DataClient.
             * @param {OwnedResource} ownedResource
             * @returns {boolean}
             */
            isOwnedByCurrentDataClient(ownedResource) {
                return ownedResource.isOwnedBy(this.dataClient);
            },
            /**
             * Whether the SurveyBase is editable.
             *
             * Expects ownedResource to have an `isShadow` getter.
             *
             * @param {OwnedResource} ownedResource
             * @returns {boolean}
             */
            disabled(ownedResource) {
                return !this.isOwnedByCurrentDataClient(ownedResource)
                    || ownedResource.isShadow;
            },
            /**
             * Whether a ShadowObject can be converted to a ConcreteObject.
             *
             * Expects ownedResource to have an `isShadow` getter.
             *
             * @param {OwnedResource} ownedResource
             * @returns {boolean}
             */
            convertable(ownedResource) {
                return ownedResource.isShadow
                    && this.isOwnedByCurrentDataClient;
            }
        }
    }
</script>

<style lang="scss">
</style>
