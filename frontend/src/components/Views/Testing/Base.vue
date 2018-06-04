<template>
    <div class="testing-centered">
        <div class="testing-bordered">
            <router-view/>
        </div>
    </div>
</template>

<script>
    export default {
        name: "TestingBase"
    };
</script>

<style lang="scss" scoped>
    * {
        padding: 0;
        margin: 0;
    }

    .testing-centered {
        margin: auto;
        display: grid;
        justify-items: center;
        align-items: center;
    }

    .testing-bordered {
        border: 1px solid black;
        padding: 15px;
    }
</style>
