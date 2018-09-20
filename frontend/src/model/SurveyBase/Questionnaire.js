import SurveyBase from "./SurveyBase";
import {clone, map} from "ramda";

class Questionnaire extends SurveyBase {
    /**
     * @param {string} href See Resource.
     * @param {String} id See Resource.
     * @param {Array<Party>} owners See OwnedResource.
     * @param {LanguageData} languageData See SurveyBase.
     * @param {Boolean} template See SurveyBase.
     * @param {String} referenceId See SurveyBase.
     * @param {string} name The Questionnaire's name.
     * @param {string} description A description for the Questionnaire.
     * @param {boolean} isPublic Whether the Questionnaire can be filled out and
     *  submitted.
     * @param {boolean} allowEmbedded Whether the Questionnaire can be used in
     *  embedded mode in alternate frontends.
     * @param {string} xapiTarget
     * @param ltiConsumerKey {String} Shared secret for embedding & lti launch
     * @param {Array<Dimension>} dimensions The Questionnaire's child dimen-
     *  sions.
     * @param {Array<Challenge>} challenges A list of Challenges
     */
    constructor(href,
                id,
                owners,
                languageData,
                template,
                referenceId,
                name,
                description,
                isPublic,
                allowEmbedded,
                xapiTarget,
                ltiConsumerKey,
                dimensions,
                challenges) {
        super(href, id, owners, languageData, template, referenceId);

        this.name = name;
        this.description = description;
        this.isPublic = isPublic;
        this.allowEmbedded = allowEmbedded;
        this.xapiTarget = xapiTarget;
        this.ltiConsumerKey = ltiConsumerKey;
        this.dimensions = dimensions;
        this.challenges = challenges;
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

    /**
     * @returns {Questionnaire}
     */
    clone() {
        return new Questionnaire(
            this._href,
            this._id,
            this._owners,
            this.languageData.clone(),
            this.template,
            this.referenceId,
            this.name,
            this.description,
            this.isPublic,
            this.allowEmbedded,
            this.xapiTarget,
            this.ltiConsumerKey,
            map(clone, this.dimensions),
            map(clone, this.challenges)
        );
    }
}

class ConcreteQuestionnaire extends Questionnaire {
    /**
     * @param {string} href See Resource.
     * @param {String} id See Resource.
     * @param {Array<Party>} owners See OwnedResource.
     * @param {LanguageData} languageData See SurveyBase.
     * @param {Boolean} template See SurveyBase.
     * @param {String} referenceId See SurveyBase.
     * @param {string} name See Questionnaire.
     * @param {string} description See Questionnaire.
     * @param {boolean} isPublic See Questionnaire.
     * @param {boolean} allowEmbedded See Questionnaire.
     * @param {string} xapiTarget See Questionnaire.
     * @param ltiConsumerKey {String} See Questionnaire.
     * @param {Array<Dimension>} dimensions See Questionnaire.
     * @param {Array<Challenge>} challenges A list of Challenges
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
                owners,
                languageData,
                template,
                referenceId,
                name,
                description,
                isPublic,
                allowEmbedded,
                xapiTarget,
                ltiConsumerKey,
                dimensions,
                challenges,
                incomingReferenceCount,
                ownedIncomingReferences) {
        super(
            href,
            id,
            owners,
            languageData,
            template,
            referenceId,
            name,
            description,
            isPublic,
            allowEmbedded,
            xapiTarget,
            ltiConsumerKey,
            dimensions,
            challenges
        );

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

    /**
     * @returns {ConcreteQuestionnaire}
     */
    clone() {
        return new ConcreteQuestionnaire(
            this._href,
            this._id,
            this._owners,
            this.languageData.clone(),
            this.template,
            this.referenceId,
            this.name,
            this.description,
            this.isPublic,
            this.allowEmbedded,
            this.xapiTarget,
            this.ltiConsumerKey,
            map(clone, this.dimensions),
            map(clone, this.challenges),
            this.incomingReferenceCount,
            map(clone, this.ownedIncomingReferences)
        );
    }
}

class ShadowQuestionnaire extends Questionnaire {
    /**
     * @param {string} href See Resource.
     * @param {String} id See Resource.
     * @param {Array<Party>} owners See OwnedResource.
     * @param {LanguageData} languageData See SurveyBase.
     * @param {String} referenceId See SurveyBase.
     * @param {string} name See Questionnaire.
     * @param {string} description See Questionnaire.
     * @param {boolean} isPublic See Questionnaire.
     * @param {boolean} allowEmbedded See Questionnaire.
     * @param {string} xapiTarget See Questionnaire.
     * @param ltiConsumerKey {String} See Questionnaire.
     * @param {Array<Dimension>} dimensions See Questionnaire.
     * @param {Array<Challenge>} challenges A list of Challenges
     * @param {Resource|ConcreteQuestionnaire} referenceTo Href or instance of the re-
     *  ferenced Questionnaire.
     */
    constructor(href,
                id,
                owners,
                languageData,
                referenceId,
                name,
                description,
                isPublic,
                allowEmbedded,
                xapiTarget,
                ltiConsumerKey,
                dimensions,
                challenges,
                referenceTo) {
        super(
            href,
            id,
            owners,
            languageData,
            false,
            referenceId,
            name,
            description,
            isPublic,
            allowEmbedded,
            xapiTarget,
            ltiConsumerKey,
            dimensions,
            challenges
        );

        this.referenceTo = referenceTo;
    }

    get isShadow() {
        return true;
    }

    get isConcrete() {
        return false;
    }

    /**
     * @returns {ShadowQuestionnaire}
     */
    clone() {
        return new ShadowQuestionnaire(
            this._href,
            this._id,
            [...this._owners],
            this.languageData.clone(),
            this.referenceId,
            this.name,
            this.description,
            this.isPublic,
            this.allowEmbedded,
            this.xapiTarget,
            this.ltiConsumerKey,
            map(clone, this.dimensions),
            map(clone, this.challenges),
            this.referenceTo.clone()
        );
    }
}

export default Questionnaire;

export {
    Questionnaire,
    ConcreteQuestionnaire,
    ShadowQuestionnaire
}
