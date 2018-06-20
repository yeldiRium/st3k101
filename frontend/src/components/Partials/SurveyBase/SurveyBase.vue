<template>
</template>

<script>
    import {mapGetters} from "vuex-fluture";

    /**
     * Defines some properties and methods for OwnedResources.
     *
     * Can and should be used as BaseComponent for all SurveyBase components.
     */
    export default {
        name: "SurveyBase",
        props: {
            /**
             * Set to false to prevent this from being deleted.
             */
            deletable: {
                type: Boolean,
                default: true
            },
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
             * This usually means if adding/removing children and changing cer-
             * tain fields is allowed.
             *
             * @param {OwnedResource} ownedResource
             * @returns {Boolean}
             */
            isEditable(ownedResource) {
                return this.isOwnedByCurrentDataClient(ownedResource)
                    && ownedResource.isConcrete;
            },
            /**
             * Whether the SurveyBase is deletable.
             *
             * @param {OwnedResource} ownedResource
             * @returns {Boolean}
             */
            isDeletable(ownedResource) {
                return this.isOwnedByCurrentDataClient(ownedResource)
                    && this.deletable;
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
                    && this.isOwnedByCurrentDataClient(ownedResource);
            }
        }
    }
</script>

<style lang="scss">
</style>
