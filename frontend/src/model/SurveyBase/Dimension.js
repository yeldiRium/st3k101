import Future from "fluture";

import Party from "../Party";
import Question from "./Question";
import SurveyBase from "./SurveyBase";
import {fetchDimension} from "../../api/Dimension";

class Dimension extends SurveyBase {
    /**
     * @param {string} href See Resource.
     * @param {String} id See Resource.
     * @param {Party}  owner See OwnedResource.
     * @param {LanguageData} languageData See SurveyBase.
     * @param {string} name The Dimension's name.
     * @param {Array.<Question>} questions An Array of all connected Questions.
     * @param {boolean} randomizeQuestions Whether the Questions should be dis-
     *  played in a random order to DataSubjects.
     */
    constructor(href,
                id,
                owner,
                languageData,
                name,
                questions, randomizeQuestions) {
        super(href, id, owner, languageData);
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

    // TODO: implement fetchTranslation(language)
}

class ConcreteDimension extends Dimension {
    /**
     *
     * @param {string} href See Resource.
     * @param {String} id See Resource.
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
                id,
                owner,
                languageData,
                name,
                questions,
                randomizeQuestions,
                incomingReferenceCount, ownedIncomingReferences) {
        super(href, id, owner, languageData, name, questions, randomizeQuestions);

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
     * @param {String} id See Resource.
     * @param {Party}  owner See OwnedResource.
     * @param {LanguageData} languageData See SurveyBase.
     * @param {string} name See Dimension.
     * @param {Array.<Question>} questions See Dimension.
     * @param {boolean} randomizeQuestions See Dimension.
     * @param {Resource|ConcreteDimension} referenceTo Href or instance of the
     *  referenced Dimension.
     */
    constructor(href,
                id,
                owner,
                languageData,
                name,
                questions,
                randomizeQuestions, referenceTo) {
        super(href, id, owner, languageData, name, questions, randomizeQuestions);
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
 * If this rejects, then some dimensions might be populated and some might still
 * be Resources. The exact state will have to be tested.
 *
 * @param {ConcreteDimension} concreteDimension
 * @return {Future}
 * @resolve {Array<ShadowDimension>}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function populateOwnedIncomingReferences(concreteDimension) {
    const resolvedShadowDimensionFutures = [];

    // Use basic for loop to easily replace values.
    for (let i = 0; i < concreteDimension.ownedIncomingReferences.length; i++) {
        let reference = concreteDimension.ownedIncomingReferences[i];

        if (instanceOf(reference, Resource)) {
            const shadowDimensionFuture = fetchDimension(
                reference.href,
                concreteDimension.languageData.currentLanguage
            )
                .chain(shadowDimension => {
                    concreteDimension.ownedIncomingReferences[i] =
                        shadowDimension;
                    return Future.of(shadowDimension);
                });

            resolvedShadowDimensionFutures.push(shadowDimensionFuture);
        }
    }
    // MAYBE: is Infinity appropriate?
    return Future.parallel(Infinity, resolvedShadowDimensionFutures);
}

/**
 * If the referenceTo field contains a Resource, it is resolved to a
 * ConcreteDimension instance. Otherwise it is left as is.
 *
 * Accesses the API to load the Dimension.
 *
 * @param {ShadowDimension} shadowDimension
 * @return {Future}
 * @resolve {ConcreteDimension}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function populateReferenceTo(shadowDimension) {
    if (instanceOf(shadowDimension.referenceTo, Resource)) {
        return fetchDimension(
            shadowDimension.referenceTo.href,
            shadowDimension.languageData.currentLanguage
        )
            .chain(concreteDimension => {
                shadowDimension.referenceTo = concreteDimension;
                return Future.of(concreteDimension);
            });
    }
    return Future.of(shadowDimension.referenceTo);
}

/**
 * Based on the type of the given Dimension this either populates its incoming
 * references or its referenceTo field.
 *
 * @param {Dimension} dimension
 * @return {Future}
 * @resolve {Array<ShadowDimension>|ConcreteDimension}
 * @reject {TypeError|ApiError}
 * @cancel
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
