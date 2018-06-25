import {storiesOf} from "@storybook/vue";
import {action} from "@storybook/addon-actions";
import {withKnobs} from "@storybook/addon-knobs";

import ListItem from "../components/Partials/List/Item";

storiesOf('ListItem', module)
    .addDecorator(withKnobs)
    .addDecorator(() => ({
        template: '<div style="display: flex; justify-content: center"><story/></div>'
    }))
    .add('basic', () => ({
        components: {
            ListItem
        },
        data() {
            return {
                text: "This is a ListElement",
            }
        },
        template: '<ListItem v-model="text" @input="action" style="min-width: 300px"/>',
        methods: {
            action: action("text-edited")
        }
    }));
