import { fetchApi } from "./Util/Request";
import { extractJson } from "./Util/Response";
import { map } from "ramda";
import { parseTrackerEntry } from "./Util/Parse";

function fetchMyTrackerEntries(authenticationToken) {
  return fetchApi("/api/tracker", { authenticationToken })
    .chain(extractJson)
    .map(map(parseTrackerEntry));
}

function fetchTrackerEntriesByItemHref(authenticationToken, href) {
  let url = href.concat("/tracker").replace("//", "/");
  return fetchApi(url, { authenticationToken })
    .chain(extractJson)
    .map(map(parseTrackerEntry));
}

export { fetchMyTrackerEntries, fetchTrackerEntriesByItemHref };
