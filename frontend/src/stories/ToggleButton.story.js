import {storiesOf} from "@storybook/vue";
import {action} from "@storybook/addon-actions";
import {boolean, text, withKnobs} from "@storybook/addon-knobs";

import ToggleButton from "../components/Partials/Form/ToggleButton";

storiesOf('ToggleButton', module)
    .addDecorator(withKnobs)
    .addDecorator(() => ({
        template: '<div style="display: flex; justify-content: center"><story/></div>'
    }))
    .add('basic', () => ({
        components: {
            ToggleButton
        },
        data() {
            return {
                value: false,
                disabled: boolean("Disabled", false),
                leftText: text("Left Text", "Off"),
                rightText: text("Right Text", "On")
            }
        },
        template: '<ToggleButton v-model="value" @input="action" :disabled="disabled">' +
        '   <span slot="on">{{ rightText }}</span>' +
        '   <span slot="off">{{ leftText }}</span>' +
        '</ToggleButton>',
        methods: {
            action: action("text-edited")
        }
    }));
