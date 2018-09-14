import {Future} from "fluture";

import {fetchApi} from "./Util/Request";
import {extractJson} from "./Util/Response";
import {parseQuestionStatistic} from "./Util/Parse";


function fetchQuestionStatistic(authenticationToken, href = null) {
    let apiEndpoint = (href + "/statistic").replace("//", "/");
    return fetchApi(
        apiEndpoint,
        {
            authenticationToken
        })
        .chain(extractJson)
        .map(parseQuestionStatistic);
}

function fetchQuestionStatisticsByQuestionnaire(authenticationToken, href = null) {
    let apiEndpoint = (href + "/statistics").replace("//", "/");
    return fetchApi(
        apiEndpoint,
        {
            authenticationToken
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