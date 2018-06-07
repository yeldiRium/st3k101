<template>
    <div class="config-references">
        {{ referenceLine }}
    </div>
</template>

<script>
    /**
     * Displays the references to a ConcreteObject. Works with Questions,
     * Dimension and Questionnaires by duck-typing.
     */
    export default {
        name: "Config-References",
        props: {
            object: {
                type: Object
            }
        },
        computed: {
            referenceLine() {
                return `${this.object.incomingReferenceCount} references.`
            }
        }
    }
</script>

<style lang="scss">

</style>
