import * as R from "ramda";

import { parseLanguage, parseLanguageData } from "../Parse";
import { Language } from "../../../model/Language";

describe("parseLanguage", () => {
  const testParams = {
    item_id: "testItemId",
    value: "testValue"
  };
  test("raises error for missing properties", () => {
    R.forEach(
      key =>
        expect(() => {
          parseLanguage(R.dissoc(key, testParams));
        }).toThrowErrorMatchingSnapshot(),
      R.keys(testParams)
    );
  });

  test("build Language object from given object", () => {
    expect(parseLanguage(testParams)).toEqual(
      new Language(testParams.item_id, testParams.value)
    );
  });
});

describe("parseLanguageData", () => {
  /**
   * TODO: Behaviour here must be defined and tested
   */
  test("does what whith empty input?", () => {
    console.log(
      "parseLanguageData is passed empty object:",
      parseLanguageData({})
    );
  });
});

describe("parseResource", () => {});

describe("parseRoles", () => {});

describe("parseDataClient", () => {});

describe("parseSmallDataClient", () => {});

describe("parseDataSubject", () => {});

describe("parseChallenges", () => {});

describe("parseEMailWhitelistChallenge", () => {});

describe("parseEmailBlacklistChallenge", () => {});

describe("parsePasswordChallenge", () => {});

describe("parseQuestionnaire", () => {});

describe("parseTemplateQuestionnaire", () => {});

describe("parseShadowQuestionnaire", () => {});

describe("parseConcreteQuestionnaire", () => {});

describe("parseDimension", () => {});

describe("parseTemplateDimension", () => {});

describe("parseShadowDimension", () => {});

describe("parseConcreteDimension", () => {});

describe("parseQuestion", () => {});

describe("parseTemplateQuestion", () => {});

describe("parseShadowQuestion", () => {});

describe("parseConcreteQuestion", () => {});

describe("parsePropertyUpdatedTrackerEntry", () => {});

describe("parseTranslatedPropertyUpdatedTrackerEntry", () => {});

describe("parseItemAddedTrackeEntry", () => {});

describe("parseItemRemovedTrackerEntry", () => {});

describe("parseQuestionnaireRemovedTrackerEntry", () => {});

describe("parseTrackerEntry", () => {});

describe("parseSubmissionQuestion", () => {});

describe("parseSubmissionDimension", () => {});

describe("parseSubmissionQuestionnaire", () => {});

describe("parseQuestionStatistic", () => {});
