<template>
    <div class="tracker-entry"
         v-if="trackerEntry.type === 'PropertyUpdatedTrackerEntry'"
    >
        <span class="tracker-entry__date">
            {{ trackerEntry.timestamp.toLocaleDateString() }}:
        </span>
        <span class="tracker-entry__body">
            {{ trackerEntry.dataclientEmail }} updated
            {{trackerEntry.propertyName}}
            <span v-if="all">
                of
                <router-link
                :to="buildRouterLinkParams(trackerEntry.itemType, trackerEntry.itemHref)"
                >
                {{ trackerEntry.itemName }}
            </router-link>
        </span>
            from  »{{trackerEntry.previousValue}}«
            to »{{ trackerEntry.newValue }}«

        </span>
    </div>
    <div class="tracker-entry"
         v-else-if="trackerEntry.type === 'TranslatedPropertyUpdatedTrackerEntry'"
    >
        {{ trackerEntry.timestamp.toLocaleDateString() }}:
        {{ trackerEntry.dataclientEmail }} updated
        {{ trackerEntry.language.value }} translation of
        {{ trackerEntry.propertyName }}
        <span v-if="all">
            of
            <router-link
            :to="buildRouterLinkParams(trackerEntry.itemType, trackerEntry.itemHref)"
            >
            {{ trackerEntry.itemName }}
            </router-link>
        </span>
        from  »{{trackerEntry.previousValue}}«
        to »{{ trackerEntry.newValue }}«
    </div>
    <div class="tracker-entry"
         v-else-if="trackerEntry.type === 'ItemAddedTrackerEntry'"
    >
        {{ trackerEntry.timestamp.toLocaleDateString() }}:
         {{ trackerEntry.dataclientEmail }} added {{ trackerEntry.addedItemType }}
        <router-link
            :to="buildRouterLinkParams(trackerEntry.addedItemType, trackerEntry.addedItemHref)"
        >{{ trackerEntry.addedItemName }}</router-link>
        <span v-if="all">
            to
            <router-link
            :to="buildRouterLinkParams(trackerEntry.parentItemType, trackerEntry.parentItemHref)"
            >
            {{ trackerEntry.parentItemName }}
            </router-link>
        </span>.
    </div>
    <div class="tracker-entry"
         v-else-if="trackerEntry.type === 'ItemRemovedTrackerEntry'"
    >
        {{ trackerEntry.timestamp.toLocaleDateString() }}:
        {{ trackerEntry.dataclientEmail }} removed
        »{{ trackerEntry.removedItemName }}«
        from this {{ trackerEntry.parentItemType }}.
    </div>
    <div class="tracker-entry"
         v-else-if="trackerEntry.type === 'QuestionnaireRemovedTrackerEntry'"
    >
        {{ trackerEntry.timestamp.toLocaleDateString() }}:
        {{ trackerEntry.dataclientEmail }} removed Questionnaire
        »{{ trackerEntry.questionnaireName }}«.
    </div>
</template>

<script>
    import {
        TrackerEntry
    } from "../../../model/TrackerEntry";


    export default {
        name: "TrackerEntry",
        props: {
            trackerEntry: {
                type: TrackerEntry
            },
            all: {
                type: Boolean
            }
        },
        methods: {
            buildRouterLinkParams(itemType, itemHref) {
                let name = "";
                let id = itemHref.match(/\/(\d+)\/?$/)[1];

                switch (itemType) {
                    case "ConcreteQuestion":
                    case "ShadowQuestion":
                    case "Question":
                        name = 'AQuestion';
                        break;
                    case "ConcreteDimension":
                    case "ShadowDimension":
                    case "Dimension":
                        name = 'ADimension';
                        break;
                    case "ConcreteQuestionnaire":
                    case "ShadowQuestionnaire":
                    case "Questionnaire":
                        name = 'AQuestionnaire';
                        break;
                }
                return {
                    name: name,
                    params: {
                        id: id
                    }
                };
            }
        }
    }
</script>

<style lang="scss">
    @import "../../scss/variables";
    .tracker-entry {
        display: inline-block;
        text-align: left;
        overflow-wrap: break-word;
        border-left: $primary 2px solid;
        padding-left: 8px;
        margin-bottom: .6em;
    }
</style>