import {storiesOf} from "@storybook/vue";
import {action} from "@storybook/addon-actions";

import store from "./Fixtures/TestStore";
import LanguagePicker from "../components/Partials/LanguagePicker";
import {LanguageData} from "../model/Language";
import {slice} from "ramda";

storiesOf('LanguagePicker', module)
    .addDecorator(() => ({
        template: '<div style="display: flex; justify-content: center"><story/></div>'
    }))
    .add('basic', () => ({
        components: {
            LanguagePicker
        },
        store,
        data() {
            const languages = this.$store.state.language.languages;
            return {
                languageData: new LanguageData(
                    languages[0],
                    languages[0],
                    slice(0, 2, languages)
                )
            };
        },
        methods: {
            chooseLanguage: action("chose-available-language"),
            chooseLanguageUnavailable: action("chose-unavailable-language")
        },
        template: '<LanguagePicker :language-data="languageData" @choose-language="chooseLanguage" @choose-language-unavailable="chooseLanguageUnavailable"/>'
    }));
