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
            question: {
                type: Question
            },
            draggable: {
                type: Boolean,
                default: true
            }
        },
        computed: {
            ...mapGetters("session", ["dataClient"]),
            /**
             * Whether the SurveyBase is owned by the current DataClient.
             * @returns {boolean}
             */
            isOwnedByCurrentDataClient() {
                return this.question.isOwnedBy(this.dataClient);
            },
            /**
             * Whether the SurveyBase is editable.
             * @returns {boolean}
             */
            disabled() {
                return !this.isOwnedByCurrentDataClient || this.question.isShadow;
            },
            /**
             * Whether a ShadowQuestion can be converted to a ConcreteQuestion.
             * @returns {boolean}
             */
            convertable() {
                return this.question.isShadow
                    && this.isOwnedByCurrentDataClient;
            }
        }
    }
</script>

<style lang="scss">
</style>
