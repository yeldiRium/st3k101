import {mapGetters} from "vuex-fluture";
import {storiesOf} from "@storybook/vue";
import {boolean, withKnobs} from "@storybook/addon-knobs";
import {action} from "@storybook/addon-actions";
import StoryRouter from "storybook-vue-router";

import Dimension from "../components/Partials/SurveyBase/Dimension";
import Dialog from "../components/Partials/Modal/Dialog";
import CreateQuestion from "../components/Partials/Modal/CreateQuestion";
import TranslateQuestion from "../components/Partials/Modal/TranslateQuestion";
import TranslateDimension from "../components/Partials/Modal/TranslateDimension";

import store from "./Fixtures/TestStore";

storiesOf('Dimension', module)
    .addDecorator(StoryRouter())
    .addDecorator(withKnobs)
    .addDecorator(() => ({
        components: {
            Dialog,
            CreateQuestion,
            TranslateQuestion,
            TranslateDimension
        },
        template: '<div style="display: grid; justify-items: center; grid-row-gap: 50px">' +
        '   <div v-for="n in 10" :style="{\'min-width\': `${100 * n + 50}px`}">' +
        '       {{ 100 * n + 50 }}px: <story/>' +
        '   </div>' +
        '   <Dialog />' +
        '   <CreateQuestion />' +
        '   <TranslateQuestion />' +
        '   <TranslateDimension />' +
        '</div>',
        store
    }))
    .add('basic', () => ({
        components: {
            Dimension
        },
        data() {
            return {
                showLink: boolean("Show Link", true)
            }
        },
        computed: {
            ...mapGetters("dimensions", ["dimension"])
        },
        template: '<Dimension :dimension="dimension" :show-link="showLink" @dimension-delete="dimensionDelete"/>',
        store,
        methods: {
            dimensionDelete: action("dimension-delete")
        }
    }));
