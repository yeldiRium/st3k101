import {fetchApi} from "./Util/Request";
import {extractJson} from "./Util/Response";
import {map} from "ramda";
import {parseTrackerEntry} from "./Util/Parse";


function fetchMyTrackerEntries() {
    return fetchApi("/api/tracker", {authenticate: true})
        .chain(extractJson)
        .map(map(parseTrackerEntry));
}

function fetchTrackerEntriesByItemHref(href) {
    let url = href.concat("/tracker").replace("//", "/");
    return fetchApi(url, {authenticate: true})
        .chain(extractJson)
        .map(map(parseTrackerEntry));
}

export {
    fetchMyTrackerEntries,
    fetchTrackerEntriesByItemHref
};