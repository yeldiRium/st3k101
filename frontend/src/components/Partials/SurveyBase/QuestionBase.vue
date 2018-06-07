<template>
</template>

<script>
    import {mapGetters} from "vuex";

    import {Question} from "../../../model/Question";

    /**
     * Defines some properties and computed propertes for OwnedResources.
     *
     * Can and should be used as BaseComponent for all SurveyBase components.
     */
    export default {
        name: "QuestionBase",
        props: {
            /** @type {Question} */
            question: {
                type: Question
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
             * Whether the QuestionBase is editable.
             *
             * Expects ownedResource to have a `isShadow` getter.
             *
             * @param {OwnedResource} ownedResource
             * @returns {boolean}
             */
            disabled(ownedResource) {
                return !this.isOwnedByCurrentDataClient(ownedResource)
                    || ownedResource.isShadow;
            },
            /**
             * Whether a ShadowQuestion can be converted to a ConcreteQuestion.
             *
             * Expects ownedResource to have a `isShadow` getter.
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
