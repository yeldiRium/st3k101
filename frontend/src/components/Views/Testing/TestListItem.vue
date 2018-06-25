<template>
    <div class="TestListItem_container">
        <ListItem v-model="text1"
                  :key="text1"
                  subtext="Und das hier soll ein Subtext sein?!? Mach mal besser länger."
        >
            <icon-visible class="list-item-icon"/>
            <icon-reorder class="list-item-icon"/>
        </ListItem>
        <ListItem v-model="text2"
                  :key="text2"
                  subtext="Diesmal mit einem kürzeren Subtext."
                  :disabled="true"
        >
            <icon-invisible class="list-item-icon"/>
            <icon-reorder class="list-item-icon"/>
        </ListItem>
        <ListItem v-model="text3"
                  :key="text3"
                  subtext=""
                  :mini="true"
        >
            <icon-invisible class="list-item-icon"/>
            <icon-reorder class="list-item-icon"/>
        </ListItem>
        <ListItem v-model="text4"
                  :key="text4"
                  subtext=""
                  :mini="true"
                  :disabled="true"
        >
            <icon-visible class="list-item-icon"/>
            <icon-reorder class="list-item-icon"/>
        </ListItem>
    </div>
</template>

<script>
    import ListItem from "../../Partials/List/Item";

    import IconVisible from "../../../assets/icons/baseline-visibility-24px.svg";
    import IconInvisible from "../../../assets/icons/baseline-visibility_off-24px.svg";
    import IconReorder from "../../../assets/icons/baseline-reorder-24px.svg";

    export default {
        name: "TestListItem",
        components: {
            ListItem,
            IconVisible,
            IconInvisible,
            IconReorder
        },
        data() {
            return {
                text1: "Dies ist scheinbar ein ListItem.",
                text2: "Dieses ListItem ist disabled.",
                text3: "Und ein mini ListItem.",
                text4: "Mini und disabled."
            }
        }
    }
</script>

<style lang="scss">
    .TestListItem_container {
        width: 100%;
        height: 100%;

        padding: 0;
        margin: 0;
    }
</style>
