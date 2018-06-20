<template>
    <div class="language-picker__container">
        <div class="language-picker__current-language"
             :title="languageData.currentLanguage.longName"
             ref="currentLanguage"
             @click="openLanguageMenu"
        >
            {{toUpper(languageData.currentLanguage.shortName)}}
        </div>

        <div class="language-picker__language-menu elevation-24"
             :style="menuStyle"
             v-click-outside="closeLanguageMenu"
             v-if="menuOpen"
        >
            <div class="language-picker__heading"
                 v-if="languageData.availableLanguages.length > 0"
            >
                Available languages
            </div>
            <div class="language-picker__item"
                 v-for="language in languageData.availableLanguages"
                 :key="language.shortName"
                 @click="chooseLanguage(language)"
            >
                <span class="language-picker__short-name">
                    {{ toUpper(language.shortName) }}
                </span>
                <span class="language-picker__long-name">
                    {{ language.longName }}
                </span>
            </div>

            <div class="language-picker__heading"
                 v-if="unusedLanguages.length > 0"
            >
                Unused languages
            </div>

            <div class="language-picker__item"
                 v-for="language in unusedLanguages"
                 :key="language.shortName"
                 @click="chooseLanguage(language, false)"
            >
                <span class="language-picker__short-name">
                    {{ toUpper(language.shortName) }}
                </span>
                <span class="language-picker__long-name">
                    {{ language.longName }}
                </span>
            </div>
        </div>
    </div>
</template>

<script>
    import {contains, toUpper, without} from "ramda";
    import {mapState} from "vuex-fluture";

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

    .language-picker {
        &__current-language {
            background-color: $lighter;
            border: 1px solid $slightlydark;
            border-radius: 4px;
            padding: 3px;

            cursor: pointer;
        }

        &__language-menu {
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
        }

        &__item {
            padding: 5px;

            display: grid;
            grid-template-columns: 25% 75%;

            background-color: $verylight;

            cursor: pointer;

            &:hover {
                background-color: $primary-light;
            }
        }

        &__heading {
            padding-left: 5px;
            padding-right: 5px;

            font-size: 0.9em;
            color: $darker;

            display: initial;
        }
    }
</style>
