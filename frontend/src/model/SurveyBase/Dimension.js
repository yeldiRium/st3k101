import SurveyBase from "./SurveyBase";

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

export default Dimension;

export {
    Dimension,
    ConcreteDimension,
    ShadowDimension
}
