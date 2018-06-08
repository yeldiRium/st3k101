<template>
    <div class="TestListItem_container">
        <ListItem text="Dies ist scheinbar ein ListItem."
                  subtext="Und das hier soll ein Subtext sein?!? Mach mal besser länger."
        >
            <icon-visible class="list-item-icon" />
            <icon-reorder class="list-item-icon" />
        </ListItem>
        <ListItem text="Dieses ListItem ist disabled."
                  subtext="Diesmal mit einem kürzeren Subtext."
                  :disabled="true"
        >
            <icon-invisible class="list-item-icon" />
            <icon-reorder class="list-item-icon" />
        </ListItem>
        <ListItem text="Und ein mini ListItem."
                  subtext=""
                  :mini="true"
        >
            <icon-invisible class="list-item-icon" />
            <icon-reorder class="list-item-icon" />
        </ListItem>
        <ListItem text="Mini und disabled."
                  subtext=""
                  :mini="true"
                  :disabled="true"
        >
            <icon-visible class="list-item-icon" />
            <icon-reorder class="list-item-icon" />
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