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

export {
    fetchQuestionStatistic
};