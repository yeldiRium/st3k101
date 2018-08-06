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

export {
    fetchQuestionStatistic
};