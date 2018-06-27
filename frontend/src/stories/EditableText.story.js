import {storiesOf} from "@storybook/vue";
import {action} from "@storybook/addon-actions";
import {boolean, withKnobs} from "@storybook/addon-knobs";

import EditableText from "../components/Partials/Form/EditableText";

storiesOf('EditableText', module)
    .addDecorator(withKnobs)
    .addDecorator(() => ({
        template: '<div style="display: flex; justify-content: center"><story/></div>'
    }))
    .add('basic', () => ({
        components: {
            EditableText
        },
        data() {
            return {
                text: "This text is editable",
                textArea: boolean("TextArea", false)
            }
        },
        template: '<EditableText v-model="text" @input="action" :textArea="textArea" />',
        methods: {
            action: action("text-edited")
        }
    }));
