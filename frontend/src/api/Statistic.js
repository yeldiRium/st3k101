import {Future} from "fluture";

import {fetchApi} from "./Util/Request";
import {extractJson} from "./Util/Response";
import {parseQuestionStatistic} from "./Util/Parse";


function fetchQuestionStatistic({href = null}) {
    let apiEndpoint = (href + "/statistic").replace("//", "/");
    return fetchApi(
        apiEndpoint,
        {
            authenticate: true
        })
        .chain(extractJson)
        .map(parseQuestionStatistic);
}

function fetchQuestionStatisticsByQuestionnaire({href = null}) {
    let apiEndpoint = (href + "/statistics").replace("//", "/");
    return fetchApi(
        apiEndpoint,
        {
            authenticate: true
        })
        .chain(extractJson)
        .chain(statistics => {
            let parsedStatistics = [];
            for (let statistic of statistics) {
                parsedStatistics = parsedStatistics.concat(parseQuestionStatistic(statistic));
            }
            return Future.of(parsedStatistics);
        });
}

export {
    fetchQuestionStatistic,
    fetchQuestionStatisticsByQuestionnaire
};