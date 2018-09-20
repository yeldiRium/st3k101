<template>
    <div class="language-picker__container">
        <div class="language-picker__current-language"
             :title="languageData.currentLanguage.longName"
             ref="currentLanguage"
             @click="openLanguageMenu"
        >
            {{currentLanguageLabel}}
        </div>

        <div class="language-picker__language-menu elevation-24"
             :style="menuStyle"
             v-click-outside="closeLanguageMenu"
             v-if="menuOpen"
        >
            <input
                    name="filter"
                    ref="filter"
                    v-model="filterString"
            />
            <div class="language-picker__heading"
                 v-if="filteredLanguages.length > 0"
            >
                Available languages
            </div>
            <div class="language-picker__item"
                 v-for="language in filteredLanguages"
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
                 v-if="filteredUnusedLanguages.length > 0"
                 v-show="!hideUnused"
            >
                Unused languages
            </div>

            <div class="language-picker__item"
                 v-for="language in filteredUnusedLanguages"
                 :key="language.shortName"
                 @click="chooseLanguage(language, false)"
                 v-show="!hideUnused"
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
import {
  __,
  curry,
  filter,
  intersperse,
  isNil,
  join,
  pipe,
  prop,
  split,
  test,
  toUpper,
  without
} from "ramda";
import { mapState } from "vuex-fluture";

import { LanguageData } from "../../model/Language";

export default {
  data() {
    return {
      filterString: "",
      menuOpen: false,
      recomputeHack: 0
    };
  },
  props: {
    /** @type {LanguageData} */
    languageData: {
      type: LanguageData
    },
    hideUnused: {
      type: Boolean
    },
    useLongNames: {
      type: Boolean
    }
  },
  computed: {
    ...mapState("language", ["languages"]),
    ...mapState("global", ["window"]),
    currentLanguageLabel() {
      let lang = this.languageData.currentLanguage;
      return this.useLongNames ? lang.longName : toUpper(lang.shortName);
    },
    menuStyle() {
      // Establish a dependency and force update on property change.
      this.recomputeHack;

      const boundingRect = this.$refs.currentLanguage.getBoundingClientRect();

      const width = Math.min(200, Math.round(this.window.width * 0.8));
      const x = Math.max(0, boundingRect.left - width);
      const y = Math.max(0, boundingRect.top);
      return {
        width: `${width}px`,
        left: `${x}px`,
        top: `${y}px`
      };
    },
    unusedLanguages() {
      return without(this.languageData.availableLanguages, this.languages);
    },
    filteredLanguages() {
      return this.fuzzyFilter(this.languageData.availableLanguages);
    },
    filteredUnusedLanguages() {
      return this.fuzzyFilter(this.unusedLanguages);
    }
  },
  methods: {
    openLanguageMenu() {
      this.menuOpen = true;
      this.filterString = "";
      this.recomputeHack++;

      this.$nextTick(() => {
        this.$refs.filter.focus();
      });
    },
    closeLanguageMenu() {
      this.menuOpen = false;
    },
    chooseLanguage(language, available = true) {
      if (available) {
        this.$emit("choose-language", language);
      } else {
        this.$emit("choose-language-unavailable", language);
      }
      this.closeLanguageMenu();
    },
    /**
     * Filters the list by fuzzy matching the current filterString a-
     * gainst each element.
     * @param {Array<Language>} list
     * @returns {Array<Language>}
     */
    fuzzyFilter(list) {
      return filter(
        pipe(
          prop("longName"),
          test(
            pipe(
              split(""),
              intersperse(".*"),
              join(""),
              curry(RegExp)(__, "i")
            )(this.filterString)
          )
        ),
        list
      );
    },
    onKeyUp(event) {
      // Enter key was pressed
      if (event.which === 27) {
        this.closeLanguageMenu();
      }
    },
    toUpper
  },
  beforeMount() {
    window.addEventListener("keyup", this.onKeyUp);
  },
  beforeDestroy() {
    window.removeEventListener("keyup", this.onKeyUp);
  }
};
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

    z-index: 1000;
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
