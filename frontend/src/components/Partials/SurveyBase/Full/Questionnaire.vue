<template>
    <div class="full-questionnaire"
         :class="classes"
         v-if="expanded"
    >
        <ListQuestionnaire :questionnaire="questionnaire"
                       :disableSubText="true"
                       :draggable="true"
                       :ellipseText="false"
        >
            <IconExpandLess class="list-item-icon"
                            @click.native="toggleExpanded"
            />
        </ListQuestionnaire>

        <div class="full-questionnaire-body"
             ref="dropdown"
        >
            <ReferenceCounter :object="questionnaire"
                              v-if="questionnaire.isConcrete"
            />

            <Toggle v-model="questionnaire.randomizeDimensions"
                    :disabled="!isOwnedByCurrentDataClient(questionnaire)"
            >
                <template slot="off">
                    in order
                </template>
                <template slot="on">
                    randomize
                </template>
            </Toggle>

            <div class="full-questionnaire-dimensions">
                <FullDimension v-for="dimension in questionnaire.dimensions"
                              :key="dimension.href"
                              :dimension="dimension"
                              :deletable="questionnaire.isConcrete"
                              @dimension-deleted="handleDeletedDimension"
                />

                <ListItem class="full-questionnaire-add-dimension"
                          v-if="isEditable(questionnaire)"
                          text="Add new Dimension"
                          :disableSubtext="true"
                          @click="addNewDimension"
                />
                <CreateDimension v-if="isEditable(questionnaire)"
                                :language="questionnaire.languageData.currentLanguage"
                                @dimension-created="handleCreatedDimension"
                />
            </div>

            <div class="full-questionnaire-delete"
                 v-if="isDeletable(questionnaire)"
                 @click="deleteQuestionnaire"
            >
                delete
            </div>
        </div>
    </div>
    <div class="full-questionnaire"
         :class="classes"
         v-else
    >
        <ListQuestionnaire :questionnaire="questionnaire"
                       :draggable="draggable"
                       :ellipseText="true"
        >
            <IconExpandMore class="list-item-icon"
                            @click.native="toggleExpanded"
            />
        </ListQuestionnaire>
    </div>
</template>

<script>
    import {without} from "ramda";

    import QuestionnaireBase from "../QuestionnaireBase";
    import ListQuestionnaire from "../List/Questionnaire";
    import FullDimension from "../Full/Dimension";
    import ListItem from "../../List/Item";

    import CreateDimension from "../../Popup/CreateDimension";

    import ReferenceCounter from "../Config/ReferenceCounter";
    import Toggle from "../../Form/Toggle";

    import IconExpandLess from "../../../../assets/icons/baseline-expand_less-24px.svg";
    import IconExpandMore from "../../../../assets/icons/baseline-expand_more-24px.svg";

    export default {
        name: "Full-Questionnaire",
        extends: QuestionnaireBase,
        components: {
            ListQuestionnaire,
            FullDimension,
            CreateDimension,
            ListItem,
            ReferenceCounter,
            Toggle,
            IconExpandLess,
            IconExpandMore
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
                    disabled: !this.isEditable(this.questionnaire)
                }
            }
        },
        methods: {
            toggleExpanded() {
                this.expanded = !this.expanded;
            },
            addNewDimension() {
                this.$modal.show(
                    "create-dimension"
                )
            },
            handleCreatedDimension(dimension) {
                // TODO: update questionnaire via API.
                this.questionnaire.dimensions.push(dimension);
            },
            handleDeletedDimension(dimension) {
                // TODO: delete via api
                this.questionnaire.dimensions = without(
                    [dimension],
                    this.questionnaire.dimensions
                );
            },
            deleteQuestionnaire() {
                // TODO: delete via api
                this.$emit("questionnaire-deleted");
            }
        },
        created() {
            this.expanded = this.initiallyExpanded;
        }
    }
</script>

<style lang="scss">
    @import "../../../scss/_variables";

    .list-item.list-questionnaire {
        cursor: pointer;

        background-color: $primary;

        &.disabled {
            background-color: $slightlylight;
        }
    }

    .full-questionnaire {
        display: flex;
        flex-flow: column;

        background-color: $primary-light;

        &.disabled {
            background-color: $lighter;
        }

        &-dimensions {
            width: 95%;

            display: flex;
            flex-flow: column;
        }

        .full-questionnaire-add-dimension {
            background-color: $primary;
        }

        .toggle {
            > div {
                color: $darker;
            }

            &-off.toggle-off-active,
            &-on.toggle-on-active {
                color: $verydark;
            }
        }
    }

    .full-questionnaire-body {
        display: flex;
        flex-flow: column;
        align-items: center;

        > * {
            margin-top: 8px;
            margin-bottom: 8px;
        }
    }
</style>
