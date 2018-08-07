<template>
<div class="graph">
    <canvas height="" v-bind:id="id"
         class="graph__canvas"
    >
    </canvas>
</div>
</template>

<script>
    import Chart from 'chart.js';
    import {map, prop} from "ramda";

    export default {
        name: "RadarChart",
        props: {
            title: {
                type: String
            },
            questionStatistics: {
                type: Array
            },
            truncateAfter: {
                type: Number,
                default: 30
            }
        },
        data () {
            return {
                id: null,
                chart: null
            }
        },
        computed: {
            graphConfig() {
                return {
                    type: 'radar',
                    data: this.graphData,
                    options: {
                        scale: this.scaleOptions,
                        tooltips: this.tooltipsOptions,
                        borderWidth: 0.001,  // stroke width
                    }
                };
            },
            graphData() {
                return {
                    labels: map(prop("questionText"), this.questionStatistics),
                    datasets: [
                        {
                            label: "Median",
                            data: map(prop("q2"), this.questionStatistics),
                            backgroundColor: "rgba(56, 207, 0, 0.3)",  // green
                            borderColor: "rgba(56, 207, 0, 0.8)",
                            pointBackgroundColor: "rgba(56, 207, 0, 0.8)"
                        },
                        {
                            label: "Q1",
                            data: map(prop("q1"), this.questionStatistics),
                            backgroundColor: "rgba(0, 0, 0, 0)",
                            borderColor: "#28A6F4",  // blue
                            pointBackgroundColor: "#28A6F4"
                        },
                        {
                            label: "Q3",
                            data: map(prop("q3"), this.questionStatistics),
                            backgroundColor: "rgba(0, 0, 0, 0)",
                            borderColor: "#F42840",  // red
                            pointBackgroundColor: "#F42840"
                        },
                    ]
                };
            },
            tooltipsOptions() {
                return {
                    // TODO: configure tooltips
                };
            },
            scaleOptions() {
                return {
                    ticks: {
                        min: this.minValue,
                        max: this.maxValue,
                    },
                    pointLabels: {  // labels around the graph
                        display: true,
                        fontFamily: "'FF Meta VF', 'Helvetica Neue', 'Helvetica', 'Arial'",
                        callback: (label) => {  // truncate labels
                            if (label.length > this.truncateAfter) {
                                return label.substr(0, this.truncateAfter - 3) + "..."
                            }
                            return label
                        }
                    }
                };
            },
            minValue() {
                if (this.questionStatistics.length < 1) {
                    return 0;
                }
                return Math.min(...map(
                    prop("questionRangeStart"),
                    this.questionStatistics
                    )
                );
            },
            maxValue() {
                if (this.questionStatistics.length < 1) {
                    return 10;
                }

                return Math.max(...map(
                    prop("questionRangeEnd"),
                    this.questionStatistics
                    )
                );
            }
        },
        created() {
            this.id = this._uid;
        },
        mounted() {
            this.chart = new Chart(
                document.getElementById(this.id),
                this.graphConfig
            );
        }
    }
</script>

<style lang="scss">
    @font-face {
      font-family: 'FF Meta VF';
      src: url('https://variablefonts.monotype.com/MetaVariableDemo-Set.woff2') format('woff2');
      font-display: swap;
      font-style: normal italic;
      font-weight: 100 900;
    }

    .graph {
        position: relative;
        padding: 1vw 0 1vw;
        background-color: white;
    }
</style>