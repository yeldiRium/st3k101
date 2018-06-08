import Future from "fluture";

import Party from "./Party";
import Question, {populateOwnedIncomingReferences} from "./Question";
import SurveyBase from "./SurveyBase";

class Dimension extends SurveyBase {
    /**
     * @param {string} href See Resource.
     * @param {Party}  owner See OwnedResource.
     * @param {LanguageData} languageData See SurveyBase.
     * @param {string} name The Dimension's name.
     * @param {Array.<Question>} questions An Array of all connected Questions.
     * @param {boolean} randomizeQuestions Whether the Questions should be dis-
     *  played in a random order to DataSubjects.
     */
    constructor(href,
                owner,
                languageData,
                name,
                questions,
                randomizeQuestions) {
        super(href, owner, languageData);
        this.name = name;
        this.questions = questions;
        this.randomizeQuestions = randomizeQuestions;
    }

    /**
     * True, if this Question is a ShadowQuestion.
     *
     * @returns {boolean}
     */
    get isShadow() {
        throw new Error("Please override this.");
    };

    /**
     * True, if this Question is a ConcreteQuestion.
     *
     * @returns {boolean}
     */
    get isConcrete() {
        throw new Error("Please override this.");
    }
}

class ConcreteDimension extends Dimension {
    /**
     *
     * @param {string} href See Resource.
     * @param {Party}  owner See OwnedResource.
     * @param {LanguageData} languageData See SurveyBase.
     * @param {string} name See Dimension.
     * @param {Array.<Question>} questions See Dimension.
     * @param {boolean} randomizeQuestions See Dimension.
     * @param {number}  incomingReferenceCount Number of references to this
     *  Dimension.
     *  This counts references not owned by the current user and can thus be
     *  bigger than the number of ownedIncomingReferences.
     * @param {Array.<Resource|ShadowDimension>} ownedIncomingReferences List of
     *  all references (in form of hrefs or ShadowDimension instances) to this
     *  Dimension, which the current user owns.
     */
    constructor(href,
                owner,
                languageData,
                name,
                questions,
                randomizeQuestions,
                incomingReferenceCount,
                ownedIncomingReferences) {
        super(href, owner, languageData, name, questions, randomizeQuestions);

        this.incomingReferenceCount = incomingReferenceCount;
        this.ownedIncomingReferences = ownedIncomingReferences;
    }

    get isShadow() {
        return false;
    }

    get isConcrete() {
        return true;
    }

    /**
     * Number of reference to this Dimension, which are owned by the current
     * user.
     *
     * @returns {number}
     */
    ownedIncomingReferenceCount() {
        return this.ownedIncomingReferences.length;
    }
}

class ShadowDimension extends Dimension {
    /**
     *
     * @param {string} href See Resource.
     * @param {Party}  owner See OwnedResource.
     * @param {LanguageData} languageData See SurveyBase.
     * @param {string} name See Dimension.
     * @param {Array.<Question>} questions See Dimension.
     * @param {boolean} randomizeQuestions See Dimension.
     * @param {Resource|ConcreteDimension} referenceTo Href or instance of the
     *  referenced Dimension.
     */
    constructor(href,
                owner,
                languageData,
                name,
                questions,
                randomizeQuestions,
                referenceTo) {
        super(href, owner, languageData, name, questions, randomizeQuestions);
        this.referenceTo = referenceTo;
    }

    get isShadow() {
        return true;
    }

    get isConcrete() {
        return false;
    }
}

/**
 * Takes in a Dimension and populates its incoming references field by replacing
 * all resolvable References with their corresponding ShadowDimension instances.
 *
 * Accesses the API to load the Dimensions.
 *
 * TODO: implement. currently this replaces all Resource-type references with
 *       empty objects.
 *
 * @param {ConcreteDimension} concreteDimension
 * @return {Future}
 * @resolve with nothing, since the change is made in place.
 * @reject with an API error message.
 * @cancel TODO: can this actually be cancelled?
 */
function populateOwnedIncomingReferences(concreteDimension) {
    const resolvedShadowDimensionFutures = [];

    // Use basic for loop to easily replace values.
    for (let i = 0; i < concreteDimension.ownedIncomingReferences.length; i++) {
        let reference = concreteDimension.ownedIncomingReferences[i];

        if (instanceOf(reference, Resource)) {
            // TODO: fetch ShadowDimension and replace
            const shadowDimensionFuture = Future.of({}) // <- replace with actual API call
                .map(shadowDimension => {
                    concreteDimension.ownedIncomingReferences[i] =
                        shadowDimension;
                    return true;
                });

            resolvedShadowDimensionFutures.push(shadowDimensionFuture);
        }
    }
    return Future.parallel(Infinity, resolvedShadowDimensionFutures);
}

/**
 * If the referenceTo field contains a Resource, it is resolved to a
 * ConcreteDimension instance. Otherwise it is left as is.
 *
 * Accesses the API to load the Dimension.
 *
 * If it is invalid or does not resolve to anything, an error is thrown.
 *
 * TODO: implement this. currently it replaces the reference with an empty
 *       object.
 *
 * @param {ShadowDimension} shadowDimension
 * @return {Future}
 * @resolve with nothing, since the change is made in place.
 * @reject with an API error message.
 * @cancel TODO: can this actually be cancelled?
 */
function populateReferenceTo(shadowDimension) {
    if (instanceOf(shadowDimension.referenceTo, Resource)) {
        // TODO: fetch ConcreteDimension and replace
        return Future.of({}) // <- replace with actual API call
            .map(concreteDimension => {
                shadowDimension.referenceTo = concreteDimension;
            });
    }
    return Future.of(true);
}

/**
 * Based on the type of the given Dimension this either populates its incoming
 * references or its referenceTo field.
 *
 * @param {Dimension} dimension
 * @return {Future}
 * @resolve with nothing, since the change is made in place.
 * @reject with an API error message.
 * @cancel TODO: can this actually be cancelled?
 */
function populateDimension(dimension) {
    if (instanceOf(dimension, ShadowDimension)) {
        return populateReferenceTo(dimension);
    }
    if (instanceOf(dimension, ConcreteDimension)) {
        return populateOwnedIncomingReferences(dimension);
    }
}

export default Dimension;

export {
    Dimension,
    ConcreteDimension,
    ShadowDimension,
    populateOwnedIncomingReferences,
    populateReferenceTo,
    populateDimension
}