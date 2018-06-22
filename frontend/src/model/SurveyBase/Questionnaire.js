import SurveyBase from "./SurveyBase";

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

export default Questionnaire;

export {
    Questionnaire,
    ConcreteQuestionnaire,
    ShadowQuestionnaire
}
