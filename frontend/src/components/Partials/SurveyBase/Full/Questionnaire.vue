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
            <IconExpandLess class="list-item__icon"
                            @click.native="toggleExpanded"
            />
        </ListQuestionnaire>

        <div class="full-questionnaire__body"
             ref="dropdown"
        >
            <ReferenceCounter :object="questionnaire"
                              v-if="questionnaire.isConcrete"
            />

            <EditableText :text="questionnaire.description"
                          @edit="updateDescription"
                          :textArea="true"
            />

            <div class="full-questionnaire__dimensions">
                <FullDimension class="full-dimension--bordered"
                               v-for="dimension in questionnaire.dimensions"
                               :key="dimension.href"
                               :dimension="dimension"
                               :deletable="questionnaire.isConcrete"
                               @dimension-delete="deleteDimension"
                />

                <ListItem class="full-questionnaire__add-dimension-button"
                          v-if="isEditable(questionnaire)"
                          text="Add new Dimension"
                          :disableSubtext="true"
                          :editableText="false"
                          @click="openNewDimensionDialog"
                />
                <CreateDimension v-if="isEditable(questionnaire)"
                                 :language="questionnaire.languageData.currentLanguage"
                                 @dimension-create="createDimension"
                />
            </div>

            <div class="full-questionnaire__delete-button"
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
            <IconExpandMore class="list-item__icon"
                            @click.native="toggleExpanded"
            />
        </ListQuestionnaire>
    </div>
</template>

<script>
    import {mapState} from "vuex";
    import {without} from "ramda";

    import QuestionnaireBase from "../QuestionnaireBase";
    import ListQuestionnaire from "../List/Questionnaire";
    import FullDimension from "../Full/Dimension";
    import ListItem from "../../List/Item";
    import EditableText from "../../Form/EditableText";

    import CreateDimension from "../../Modal/CreateDimension";

    import ReferenceCounter from "../Config/ReferenceCounter";
    import Toggle from "../../Form/ToggleButton";

    import IconExpandLess from "../../../../assets/icons/baseline-expand_less-24px.svg";
    import IconExpandMore from "../../../../assets/icons/baseline-expand_more-24px.svg";
    import {
        addConcreteDimension,
        removeDimension, setDescription
    } from "../../../../api2/Questionnaire";

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
            IconExpandMore,
            EditableText
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
            ...mapState("session", ["dataClient"]),
            classes() {
                return {
                    "full-questionnaire--disabled": !this.isEditable(this.questionnaire)
                }
            }
        },
        methods: {
            toggleExpanded() {
                this.expanded = !this.expanded;
            },
            openNewDimensionDialog() {
                this.$modal.show(
                    "modal-create-dimension"
                )
            },
            createDimension({name, randomizeQuestions}) {
                addConcreteDimension(
                    this.questionnaire,
                    this.dataClient,
                    name,
                    randomizeQuestions
                );
            },
            deleteDimension(dimension) {
                removeDimension(this.questionnaire, dimension);
            },
            /**
             * Asks for confirmation, if the Questionnaire should be deleted, and
             * emits an event commanding to do so, if the user confirms.
             */
            deleteQuestionnaire() {
                this.$modal.show(
                    "dialog",
                    {
                        title: `Really delete Questionnaire?`,
                        text: `Do you really want to delete Questionnaire "${this.questionnaire.name}"?`,
                        buttons: [
                            {
                                text: "Cancel"
                            },
                            {
                                text: "Confirm",
                                handler: () => this.$emit(
                                    "questionnaire-deleted",
                                    this.questionnaire
                                ),
                                default: true
                            }
                        ]
                    }
                )
            },
            updateDescription(description) {
                setDescription(
                    this.questionnaire,
                    this.questionnaire.languageData.currentLanguage,
                    description
                );
            }
        },
        created() {
            this.expanded = this.initiallyExpanded;
        }
    }
</script>

<style lang="scss">
    @import "../../../scss/_variables";

    .full-questionnaire {
        display: flex;
        flex-flow: column;

        background-color: $primary-light;

        &--disabled {
            background-color: $lighter;
        }

        &--bordered {
            border: 1px solid $primary;

            &.full-questionnaire--disabled {
                border-color: $slightlylight;
            }
        }

        &__add-dimension-button {
            background-color: $primary;
        }

        &__body {
            display: flex;
            flex-flow: column;
            align-items: center;

            > * {
                width: 95%;
                text-align: center;
                margin-top: 8px;
                margin-bottom: 8px;
            }
        }

        &__dimensions {
            display: flex;
            flex-flow: column;
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

</style>
