import Future from "fluture";

import SurveyBase from "./SurveyBase";
import {fetchQuestionnaire} from "../../api/Questionnaire";

class Questionnaire extends SurveyBase {
    /**
     * @param {string} href See Resource.
     * @param {String} id See Resource.
     * @param {Party} owner See OwnedResource.
     * @param {LanguageData} languageData See SurveyBase.
     * @param {string} name The Questionnaire's name.
     * @param {string} description A description for the Questionnaire.
     * @param {boolean} isPublic Whether the Questionnaire can be filled out and
     *  submitted.
     * @param {boolean} allowEmbedded Whether the Questionnaire can be used in
     *  embedded mode in alternate frontends.
     * @param {string} xapiTarget TODO: find out, what this means exactly
     * @param {Array.<Dimension>} dimensions The Questionnaire's child dimen-
     *  sions.
     */
    constructor(href,
                id,
                owner,
                languageData,
                name,
                description,
                isPublic,
                allowEmbedded,
                xapiTarget, dimensions) {
        super(href, id, owner, languageData);

        this.name = name;
        this.description = description;
        this.isPublic = isPublic;
        this.allowEmbedded = allowEmbedded;
        this.xapiTarget = xapiTarget;
        this.dimensions = dimensions;
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

class ConcreteQuestionnaire extends Questionnaire {
    /**
     * @param {string} href See Resource.
     * @param {String} id See Resource.
     * @param {Party} owner See OwnedResource.
     * @param {LanguageData} languageData See SurveyBase.
     * @param {string} name See Questionnaire.
     * @param {string} description See Questionnaire.
     * @param {boolean} isPublic See Questionnaire.
     * @param {boolean} allowEmbedded See Questionnaire.
     * @param {string} xapiTarget See Questionnaire.
     * @param {Array.<Dimension>} dimensions See Questionnaire.
     * @param {number}  incomingReferenceCount Number of references to this
     *  Questionnaire.
     *  This counts references not owned by the current user and can thus be
     *  bigger than the number of ownedIncomingReferences.
     * @param {Array.<Resource|ShadowQuestionnaire>} ownedIncomingReferences
     *  List of all references (in form of hrefs or ShadowQuestionnaire instan-
     *  ces) to this Questionnaire, which the current user owns.
     */
    constructor(href,
                id,
                owner,
                languageData,
                name,
                description,
                isPublic,
                allowEmbedded,
                xapiTarget,
                dimensions,
                incomingReferenceCount, ownedIncomingReferences) {
        super(href, id, owner, languageData, name, description, isPublic, allowEmbedded, xapiTarget, dimensions);

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
     * Number of reference to this Questionnaire, which are owned by the current
     * user.
     *
     * @returns {number}
     */
    ownedIncomingReferenceCount() {
        return this.ownedIncomingReferences.length;
    }
}

class ShadowQuestionnaire extends Questionnaire {
    /**
     * @param {string} href See Resource.
     * @param {String} id See Resource.
     * @param {Party} owner See OwnedResource.
     * @param {LanguageData} languageData See SurveyBase.
     * @param {string} name See Questionnaire.
     * @param {string} description See Questionnaire.
     * @param {boolean} isPublic See Questionnaire.
     * @param {boolean} allowEmbedded See Questionnaire.
     * @param {string} xapiTarget See Questionnaire.
     * @param {Array.<Dimension>} dimensions See Questionnaire.
     * @param {Resource|ConcreteQuestionnaire} referenceTo Href or instance of the re-
     *  ferenced Questionnaire.
     */
    constructor(href,
                id,
                owner,
                languageData,
                name,
                description,
                isPublic,
                allowEmbedded,
                xapiTarget,
                dimensions, referenceTo) {
        super(href, id, owner, languageData, name, description, isPublic, allowEmbedded, xapiTarget, dimensions);

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
 * Takes in a Questionnaire and populates its incoming references field by re-
 * placing all resolvable References with their corresponding ShadowQuestion-
 * naire instances.
 *
 * Accesses the API to load the Questionnaires.
 *
 * If this rejects, then some questionnaires might be populated and some might
 * still be Resources. The exact state will have to be tested.
 *
 * @param {ConcreteQuestionnaire} concreteQuestionnaire
 * @return {Future}
 * @resolve {Array<ShadowQuestionnaire>}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function populateOwnedIncomingReferences(concreteQuestionnaire) {
    const resolvedShadowQuestionnaireFutures = [];

    // Use basic for loop to easily replace values.
    for (let i = 0;
         i < concreteQuestionnaire.ownedIncomingReferences.length;
         i++) {
        let reference = concreteQuestionnaire.ownedIncomingReferences[i];

        if (instanceOf(reference, Resource)) {
            const shadowQuestionnaireFuture = fetchQuestionnaire(
                reference.href,
                concreteQuestionnaire.languageData.currentLanguage
            )
                .chain(shadowQuestionnaire => {
                    concreteQuestionnaire.ownedIncomingReferences[i] =
                        shadowQuestionnaire;
                    return Future.of(shadowQuestionnaire);
                });

            resolvedShadowQuestionnaireFutures.push(shadowQuestionnaireFuture);
        }
    }
    // MAYBE: is Infinity appropriate?
    return Future.parallel(Infinity, resolvedShadowQuestionnaireFutures);
}

/**
 * If the referenceTo field contains a Resource, it is resolved to a
 * ConcreteQuestionnaire instance. Otherwise it is left as is.
 *
 * Accesses the API to load the Questionnaire.
 *
 * @param {ShadowQuestionnaire} shadowQuestionnaire
 * @return {Future}
 * @resolve {ConcreteQuestionnaire}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function populateReferenceTo(shadowQuestionnaire) {
    if (instanceOf(shadowQuestionnaire.referenceTo, Resource)) {
        // TODO: fetch ConcreteQuestionnaire and replace
        return fetchQuestionnaire(
            shadowQuestionnaire.referenceTo.href,
            shadowQuestionnaire.languageData.currentLanguage
        )
            .chain(concreteQuestionnaire => {
                shadowQuestionnaire.referenceTo = concreteQuestionnaire;
                return Future.of(concreteQuestionnaire);
            });
    }
    return Future.of(shadowQuestionnaire.referenceTo);
}

/**
 * Based on the type of the given Questionnaire this either populates its inco-
 * ming references or its referenceTo field.
 *
 * @param {Questionnaire} questionnaire
 * @return {Future}
 * @resolve {Array<ShadowQuestionnaire>|ConcreteQuestionnaire}
 * @reject {TypeError|ApiError}
 * @cancel
 */
function populateQuestionnaire(questionnaire) {
    if (instanceOf(questionnaire, ShadowQuestionnaire)) {
        return populateReferenceTo(questionnaire);
    }
    if (instanceOf(questionnaire, ConcreteQuestionnaire)) {
        return populateOwnedIncomingReferences(questionnaire);
    }
}

export default Questionnaire;

export {
    Questionnaire,
    ConcreteQuestionnaire,
    ShadowQuestionnaire,
    populateOwnedIncomingReferences,
    populateReferenceTo,
    populateQuestionnaire
}
