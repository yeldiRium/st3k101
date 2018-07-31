import {fetchApi} from "./Util/Request";
import {extractJson} from "./Util/Response";

function submitResponse(submissionQuestionnaire, {email, password}) {
    let dimensions = [];
    for (let dimension of submissionQuestionnaire.dimensions) {
        let questions = [];
        for (let question of dimension.questions) {
            questions.push({
                id: question.id,
                value: question.value,
            });
        }
        dimensions.push({
            id: dimension.id,
            questions: questions
        });
    }
    let payload = {
        data_subject: {
            email: email
        },
        password: password,
        captcha_token: "IAmNotARobot",  // TODO
        dimensions: dimensions
    };
    let api_endpoint = (submissionQuestionnaire.href + "/response")
        .replace("//", "/");
    return fetchApi(
        api_endpoint,
        {
            authenticate: false,
            method: "POST",
            body: JSON.stringify(payload)
        }
        ).chain(extractJson);
}

export {
    submitResponse
};