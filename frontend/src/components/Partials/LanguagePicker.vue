<template>
    <div class="languagepicker-container">
        <div class="languagepicker-currentlanguage"
             :title="languageData.currentLanguage.longName"
             ref="currentLanguage"
             @click="openLanguageMenu"
        >
            {{toUpper(languageData.currentLanguage.shortName)}}
        </div>

        <div class="languagepicker-languagemenu elevation-24"
             :style="menuStyle"
             v-click-outside="closeLanguageMenu"
             v-if="menuOpen"
        >
            <div class="languagepicker-languagemenu-heading"
                 v-if="languageData.availableLanguages.length > 0"
            >
                Available languages
            </div>
            <div class="languagepicker-languagemenu-item"
                 v-for="language in languageData.availableLanguages"
                 :key="language.shortName"
                 @click="chooseLanguage(language)"
            >
                <span class="languagepicker-languagemenu-short">
                    {{ toUpper(language.shortName) }}
                </span>
                <span class="languagepicker-languagemenu-long">
                    {{ language.longName }}
                </span>
            </div>

            <div class="languagepicker-languagemenu-heading"
                 v-if="unusedLanguages.length > 0"
            >
                Unused languages
            </div>

            <div class="languagepicker-languagemenu-item"
                 v-for="language in unusedLanguages"
                 :key="language.shortName"
                 @click="chooseLanguage(language, false)"
            >
                <span class="languagepicker-languagemenu-short">
                    {{ toUpper(language.shortName) }}
                </span>
                <span class="languagepicker-languagemenu-long">
                    {{ language.longName }}
                </span>
            </div>
        </div>
        <!-- dropdown select box of all languages -->
        <!-- preview with language.long, language.short as value -->
    </div>
</template>

<script>
    import {contains, toUpper, without} from "ramda";

    import {mapState} from "vuex";
    import {LanguageData} from "../../model/Language";

    export default {
        data() {
            return {
                menuOpen: false
            }
        },
        props: {
            /** @type {LanguageData} */
            languageData: {
                type: LanguageData
            }
        },
        computed: {
            ...mapState("language", ["languages"]),
            ...mapState("global", ["window"]),
            menuStyle() {
                const width = Math.min(
                    200,
                    Math.round(this.window.width * 0.8)
                );
                const x = Math.max(
                    0,
                    this.$refs.currentLanguage.offsetLeft - width
                );
                const y = Math.max(
                    0,
                    this.$refs.currentLanguage.offsetTop
                );
                return {
                    width: `${width}px`,
                    left: `${x}px`,
                    top: `${y}px`
                }
            },
            unusedLanguages() {
                return without(
                    this.languageData.availableLanguages,
                    this.languages
                );
            }
        },
        methods: {
            openLanguageMenu() {
                this.menuOpen = true;
            },
            closeLanguageMenu() {
                this.menuOpen = false;
            },
            chooseLanguage(language, available = true) {
                if (available) {
                    this.$emit('choose-language', language);
                } else {
                    this.$emit('choose-language-unavailable', language)
                }
                this.closeLanguageMenu();
            },
            toUpper
        }
    }
</script>

<style lang="scss">
    @import "../scss/_variables";
    @import "../scss/_elevation";

    .languagepicker-currentlanguage {
        background-color: $lighter;
        border: 1px solid $slightlydark;
        border-radius: 4px;
        padding: 3px;
    }

    .languagepicker-languagemenu {
        position: absolute;
        padding-top: 5px;
        padding-bottom: 5px;
        max-height: 40vh;
        overflow-y: scroll;
        overflow-x: hidden;

        background-color: $lighter;
        border-top: 5px solid $lighter;
        border-bottom: 5px solid $lighter;

        display: flex;
        flex-flow: column;

        &-item {
            padding: 5px;

            display: grid;
            grid-template-columns: 25% 75%;

            background-color: $verylight;

            cursor: pointer;

            &:hover {
                background-color: $primary-light;
            }
        }

        &-heading {
            padding-left: 5px;
            padding-right: 5px;

            font-size: 0.9em;
            color: $darker;

            display: initial;
        }
    }
</style>
