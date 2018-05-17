<template>
    <div class="button-bar" :style="barStyle">
        <div class="button-bar_container">
            <div class="button-bar_lower-bar" :style="lowerBarStyle">
                <svg width="100%" height="100%">
                    <!--ButtonBar :num="2"
                               :buttonSize="buttonSize"
                               :padding="padding"
                               :spacing="buttonSize*0.5"
                    /-->
                </svg>
            </div>

            <div class="button-bar_button-container" :style="buttonBarStyle">
                <!--DiamondFloatingButton color="#55FF00"
                                       border-color="#119900"
                                       :border-thickness="2"
                                       :style="buttonStyle"
                                       :width="buttonSize"
                                       :height="buttonSize"
                /-->
                <!--DiamondFloatingButton color="#55FF00"
                                       border-color="#119900"
                                       :border-thickness="2"
                                       :style="buttonStyle"
                                       :width="buttonSize"
                                       :height="buttonSize"
                /-->
            </div>
        </div>
    </div>
</template>

<script>
    import {atLeastZero} from "../../Validators";

    export default {
        name: "ButtonBar",
        components: {},
        props: {
            buttonSize: {
                type: Number,
                default: 48,
                validator: atLeastZero
            },
            padding: {
                type: Number,
                default: 8,
                validator: atLeastZero
            }
        },
        computed: {
            height() {
                return this.buttonSize + this.padding;
            },
            barStyle() {
                return {
                    height: `${this.height}px`
                }
            },
            buttonBarStyle() {
                return {
                    marginTop: `-${this.height}px`
                }
            },
            lowerBarStyle() {
                return {
                    marginTop: `${this.buttonSize / 2}px`,
                    height: `${this.padding + this.buttonSize / 2}px`
                }
            },
            buttonStyle() {
                return {
                    marginTop: `-${this.buttonSize * 0.25}px`
                };
            }
        }
    }
</script>

<style lang="scss">
    .button-bar_container {
        width: 100%;
        height: 100%;
    }

    .button-bar_button-container {
        width: 100%;
        height: 100%;

        z-index: 12;

        background-color: lightgrey;

        display: flex;
        justify-content: center;
        align-content: center;
    }

    .button-bar_lower-bar {
        z-index: 8;
    }
</style>