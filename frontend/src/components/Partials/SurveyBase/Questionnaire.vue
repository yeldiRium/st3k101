<template>
    <div class="questionnaire"
         :class="classes"
    >
        <ListItem class="questionnaire__title"
                  :value="questionnaire.name"
                  :subtext="subtext"
                  :mini="expanded"
                  :ellipseText="!expanded"
                  :disabled="!isEditable(questionnaire)"
                  @input="updateQuestionnaire('name', $event, true)"
        >
            <a :href="$router.resolve({name: 'SurveyForSubmission', params: {id: questionnaire.id}}).href"
               target="_blank"
            >
                <IconLink class="list-item__icon"
                          v-if="showLink"
                />
            </a>
            <template>
                <IconExpandLess class="list-item__icon"
                                v-if="expanded"
                                @click.native="toggleExpanded"
                />
                <IconExpandMore class="list-item__icon"
                                v-else
                                @click.native="toggleExpanded"
                />
            </template>
            <LanguagePicker class="list-item__language-picker"
                            :language-data="questionnaire.languageData"
                            @choose-language="changeLanguage"
                            @choose-language-unavailable="openAddNewTranslationDialog"
            />
        </ListItem>

        <div class="questionnaire__body"
             v-if="expanded"
             ref="dropdown"
        >
            <div class="questionnaire__dimensions">
                <Dimension class="dimension--bordered"
                           v-for="dimension in questionnaire.dimensions"
                           :key="dimension.href"
                           :dimension="dimension"
                           :deletable="questionnaire.isConcrete"
                           @dimension-delete="deleteDimension"
                />
            </div>

            <div class="questionnaire__buttons"
                 v-if="expanded"
            >
                <Button v-if="isEditable(questionnaire)"
                        @click="openNewDimensionDialog"
                >
                    Add new Dimension
                </Button>
                <Button v-if="isEditable(questionnaire)"
                        @click="openUseDimensionTemplateDialog"
                >
                    Use Dimension template
                </Button>
                <Button v-if="isDeletable(questionnaire)"
                        @click="deleteQuestionnaire"
                        :class="{'button--grey': questionnaire.isShadow}"
                >
                    delete
                </Button>
            </div>

            <Collapsible>
                <span slot="head">preferences</span>
                <div slot="body"
                     class="questionnaire__preferences"
                >
                    <template>
                        <template v-if="questionnaire.isConcrete">
                            <span class="questionnaire__table-label">
                                References:
                            </span>
                            <ReferenceCounter :object="questionnaire"
                            />
                        </template>
                        <template v-else>
                            <span class="questionnaire__table-label questionnaire__table-label--span-2">
                                <router-link
                                        :to="{name: 'AQuestionnaire', params: {id: questionnaire.referenceTo.id}}">Go to template</router-link>
                            </span>
                        </template>
                    </template>

                    <span class="questionnaire__table-label">
                        Description:
                    </span>
                    <template>
                        <EditableText v-if="questionnaire.isConcrete"
                                      :value="questionnaire.description"
                                      @input="updateQuestionnaire('description', $event, true)"
                                      :text-area="true"
                                      :edit-left="true"
                        />
                        <div v-else>
                            {{ questionnaire.description }}
                        </div>
                    </template>

                    <span class="questionnaire__table-label">
                        XAPI Target:
                    </span>
                    <template>
                        <EditableText v-if="questionnaire.isConcrete"
                                      :value="questionnaire.xapiTarget"
                                      @input="updateQuestionnaire('xapiTarget', $event)"
                                      :edit-left="true"
                        />
                        <div v-else>
                            {{ questionnaire.xapiTarget }}
                        </div>
                    </template>

                    <span class="questionnaire__table-label">
                        Reference ID:
                    </span>
                    <template>
                        <EditableText v-if="questionnaire.isConcrete"
                                      :value="questionnaire.referenceId"
                                      @input="updateQuestionnaire('referenceId', $event, true)"
                                      :edit-left="true"
                        />
                        <div v-else>
                            {{ questionnaire.referenceId }}
                        </div>
                    </template>

                    <span class="questionnaire__table-label">
                        Published:
                    </span>
                    <Toggle :value="questionnaire.isPublic"
                            :disabled="!isOwnedByCurrentDataClient(questionnaire)"
                            @input="updateQuestionnaire('isPublic', $event)"
                    >
                    </Toggle>

                    <span class="questionnaire__table-label">
                        Allow Embedding:
                    </span>
                    <Toggle :value="questionnaire.allowEmbedded"
                            :disabled="!isOwnedByCurrentDataClient(questionnaire)"
                            @input="updateQuestionnaire('allowEmbedded', $event)"
                    >
                    </Toggle>
                </div>
            </Collapsible>

            <Collapsible>
                <span slot="head">challenges</span>
                <div slot="body"
                     class="questionnaire__challnges">
                    <ChooseChallengeForm
                            v-for="challenge in questionnaire.challenges"
                            :key="challenge.name"
                            :challenge="challenge"
                            @input="updateChallenge"
                    />
                </div>
            </Collapsible>

            <TrackerEntries :surveyBase="questionnaire"></TrackerEntries>

        </div>
    </div>
</template>

<script>
    import {mapState} from "vuex-fluture";
    import {assoc, map, path, sum} from "ramda";

    import {Questionnaire} from "../../../model/SurveyBase/Questionnaire";

    import SurveyBase from "./SurveyBase";
    import Dimension from "./Dimension";
    import ListItem from "../List/Item";
    import EditableText from "../Form/EditableText";
    import LanguagePicker from "../LanguagePicker";
    import ReferenceCounter from "./Config/ReferenceCounter";
    import Toggle from "../Form/ToggleButton";
    import Button from "../Form/Button";
    import ChooseChallengeForm from "./Challenge/ChooseChallengeForm";
    import Collapsible from "../Collapsible";
    import TrackerEntries from "./TrackerEntries";

    import IconLink from "../../../assets/icons/baseline-link-24px.svg";
    import IconExpandLess from "../../../assets/icons/baseline-expand_less-24px.svg";
    import IconExpandMore from "../../../assets/icons/baseline-expand_more-24px.svg";
    import IconReorder from "../../../assets/icons/baseline-reorder-24px.svg";

    export default {
        name: "Questionnaire",
        extends: SurveyBase,
        components: {
            Collapsible,
            ListItem,
            Dimension,
            LanguagePicker,
            ReferenceCounter,
            Toggle,
            EditableText,
            Button,
            ChooseChallengeForm,
            IconLink,
            IconReorder,
            IconExpandLess,
            IconExpandMore,
            TrackerEntries
        },
        props: {
            /** @type {Questionnaire} */
            questionnaire: {
                type: Questionnaire
            },
            initiallyExpanded: {
                type: Boolean,
                default: false
            },
            showLink: {
                type: Boolean,
                default: true
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
                },
                expandChallenges: false
            }
        },
        computed: {
            ...mapState("session", ["dataClient"]),
            classes() {
                return {
                    "questionnaire--disabled": !this.isEditable(this.questionnaire)
                }
            },
            /**
             * Returns a message displaying the number of Dimensions and Ques-
             * tions in the Questionnaire.
             *
             * @returns {string}
             */
            subtext() {
                let questionCount = sum(
                    map(
                        path(["questions", "length"]),
                        this.questionnaire.dimensions
                    )
                );
                return `Contains ${this.questionnaire.dimensions.length} dimensions and ${questionCount} questions.`;
            }
        },
        methods: {
            toggleExpanded() {
                this.expanded = !this.expanded;
            },
            toggleExpandChallenges() {
                this.expandChallenges = !this.expandChallenges;
            },
            /**
             * Switch the Questionnaire to the given language.
             * @param {Language} language
             */
            changeLanguage(language) {
                this.$load(
                    this.$store.dispatch(
                        "questionnaires/fetchQuestionnaire",
                        {href: this.questionnaire.href, language}
                    )
                ).fork(
                    this.$handleApiError,
                    () => {
                        this.$emit("updated");
                    }
                );
            },
            /**
             * Opens a dialog for entering a new translation.
             *
             * @param {Language} language
             */
            openAddNewTranslationDialog(language) {
                if (!this.isEditable(this.questionnaire)) {
                    return;
                }
                this.$modal.show(
                    "modal-translate-questionnaire",
                    {
                        language,
                        handler: this.addNewTranslation,
                        name: this.questionnaire.name,
                        description: this.questionnaire.description
                    }
                );
            },
            /**
             * Add a new translation to the Questionnaire.
             * This means set new field values via API for the given languages
             * and then fetch the questionnaire anew in the now existing language.
             *
             * @param {Language} language
             * @param {String} name
             * @param {String} description
             */
            addNewTranslation({language, name, description}) {
                if (!this.isEditable(this.questionnaire)) {
                    return;
                }

                this.$load(
                    this.$store.dispatch(
                        "questionnaires/updateQuestionnaire",
                        {
                            questionnaire: this.questionnaire,
                            language,
                            params: {
                                name,
                                description
                            }
                        }
                    )
                        .chain(
                            questionnaire => this.$store.dispatch(
                                "questionnaires/fetchQuestionnaire",
                                {href: questionnaire.href, language}
                            )
                        )
                ).fork(
                    this.$handleApiError,
                    () => {
                        this.$emit("updated");
                    }
                );
            },
            /**
             * Generically updates the Questionnaire via the Store.
             *
             * @param {String} prop The name of the updated property.
             * @param {*} value The new value for it.
             * @param {Boolean} mustBeEditable Whether the Questionnaire must be
             *  editable for this to work.
             */
            updateQuestionnaire(prop, value, mustBeEditable = false) {
                if (mustBeEditable && !this.isEditable(this.questionnaire)) {
                    return;
                }
                this.$load(
                    this.$store.dispatch(
                        "questionnaires/updateQuestionnaire",
                        {
                            questionnaire: this.questionnaire,
                            params: assoc(prop, value, {})
                        }
                    )
                ).fork(
                    this.$handleApiError,
                    () => {
                        this.$emit("updated");
                    }
                );
            },
            openUseDimensionTemplateDialog() {
                this.$modal.show(
                    "modal-use-dimension-template",
                    {
                        handler: this.useDimensionTemplate
                    }
                );
            },
            useDimensionTemplate({dimension}) {
                console.log(dimension);
            },
            openNewDimensionDialog() {
                if (!this.isEditable(this.questionnaire)) {
                    return;
                }
                this.$modal.show(
                    "modal-create-dimension",
                    {
                        language: this.questionnaire.languageData.currentLanguage,
                        handler: this.createDimension
                    }
                )
            },
            createDimension({name, randomizeQuestions}) {
                if (!this.isEditable(this.questionnaire)) {
                    return;
                }
                this.$load(
                    this.$store.dispatch(
                        "questionnaires/addConcreteDimension",
                        {
                            questionnaire: this.questionnaire,
                            params: {
                                name,
                                randomizeQuestions
                            }
                        }
                    )
                ).fork(
                    this.$handleApiError,
                    () => {
                        this.$emit("updated");
                    }
                );
            },
            deleteDimension(dimension) {
                if (!this.isEditable(this.questionnaire)) {
                    return;
                }
                this.$load(
                    this.$store.dispatch(
                        "questionnaires/removeDimension",
                        {
                            questionnaire: this.questionnaire,
                            dimension
                        }
                    )
                ).fork(
                    this.$handleApiError,
                    () => {
                        this.$emit("updated");
                    }
                );
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
                                    "questionnaire-delete",
                                    this.questionnaire
                                ),
                                default: true
                            }
                        ]
                    }
                )
            },
            /**
             * Replaces the given challenge in the questionnaire.
             *
             * @param {Challenge} newChallenge
             */
            updateChallenge(newChallenge) {
                this.$load(
                    this.$store.dispatch(
                        "questionnaires/updateChallengeOnQuestionnaire",
                        {
                            questionnaire: this.questionnaire,
                            challenge: newChallenge
                        }
                    )
                ).fork(
                    this.$handleApiError,
                    () => {
                        this.$emit("updated");
                    }
                );
            }
        },
        created() {
            this.expanded = this.initiallyExpanded;
        }
    }
</script>

<style lang="scss">
    @import "../../scss/_variables";

    .questionnaire {
        display: flex;
        flex-flow: column;

        background-color: $primary-light;

        &--disabled {
            background-color: $lighter;
        }

        &--bordered {
            border: 1px solid $primary;

            &.questionnaire--disabled {
                border-color: $slightlylight;
            }
        }

        &__add-dimension-button {
            background-color: $primary;
        }

        &__body {
            padding: 0.5em 2em 0.5em 2em;

            display: grid;
            grid-template-columns: minmax(max-content, 1fr) 5fr;
            grid-row-gap: 0.5em;
            align-items: center;

            > *:not(.questionnaire__dimensions) {
                text-align: center;
            }
        }

        &__preferences {
            display: grid;
            grid-template-columns: minmax(max-content, 1fr) 5fr;
            grid-row-gap: 0.5em;
            align-items: center;
            text-align: center;
        }

        &__challenges {
            display: flex;
            flex-direction: column;
        }

        &__table-label {
            padding: 0 0.5em 0 0.5em;

            &--span-2 {
                grid-column: 1 / span 2;
            }
        }

        &__dimensions {
            width: 100%;

            display: flex;
            flex-flow: column;

            grid-column: 1 / span 2;
        }

        &__buttons {
            grid-column: 1 / span 2;
            display: flex;
            flex-wrap: wrap;
            justify-content: center;

            margin-bottom: 8px;

            .button {
                margin: 0 8px 0 8px;
                background-color: $primary-light;
                border: $primary 1px solid;
            }
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
