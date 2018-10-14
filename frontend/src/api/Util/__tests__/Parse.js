import * as R from "ramda";

import {
  parseDataClient,
  parseLanguage,
  parseLanguageData,
  parseResource,
  parseRoles,
  parseSmallDataClient
} from "../Parse";
import { Language, LanguageData } from "../../../model/Language";
import { Resource } from "../../../model/Resource";
import { DataClient } from "../../../model/DataClient";

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
  const testParams = {
    current_language: {
      item_id: "testItemId",
      value: "testValue"
    },
    original_language: {
      item_id: "testItemId",
      value: "testValue"
    },
    available_languages: [
      {
        item_id: "testItemId",
        value: "testValue"
      },
      {
        item_id: "testItemId",
        value: "testValue"
      }
    ]
  };

  test("raises error for missing properties", () => {
    R.forEach(
      key =>
        expect(() => {
          parseLanguageData(R.dissoc(key, testParams));
        }).toThrowErrorMatchingSnapshot(),
      R.keys(testParams)
    );
  });

  test("build LanguageData object from given object", () => {
    expect(parseLanguageData(testParams)).toEqual(
      new LanguageData(
        new Language(
          testParams.current_language.item_id,
          testParams.current_language.value
        ),
        new Language(
          testParams.original_language.item_id,
          testParams.original_language.value
        ),
        [
          new Language(
            testParams.available_languages[0].item_id,
            testParams.available_languages[0].value
          ),
          new Language(
            testParams.available_languages[1].item_id,
            testParams.available_languages[1].value
          )
        ]
      )
    );
  });
});

describe("parseResource", () => {
  const testParams = {
    href: "testHref",
    id: "testId"
  };

  test("raises error for missing properties", () => {
    R.forEach(
      key =>
        expect(() => {
          parseResource(R.dissoc(key, testParams));
        }).toThrowErrorMatchingSnapshot(),
      R.keys(testParams)
    );
  });

  test("build Language object from given object", () => {
    expect(parseResource(testParams)).toEqual(
      new Resource(testParams.href, testParams.id)
    );
  });
});

describe("parseRoles", () => {
  const testParams = [
    {
      value: "testValue"
    },
    {
      value: "testValue"
    },
    {
      value: "testValue"
    }
  ];

  test("raises error for missing properties", () => {
    expect(() => {
      parseRoles([{}, {}]);
    }).toThrowErrorMatchingSnapshot();
  });

  test("build Language object from given object", () => {
    expect(parseRoles(testParams)).toEqual([
      "testValue",
      "testValue",
      "testValue"
    ]);
  });
});

describe("parseDataClient", () => {
  const testParams = {
    email: "testEmail",
    id: "testId",
    href: "testHref",
    language: {
      item_id: "testItemId",
      value: "testValue"
    },
    roles: [
      {
        value: "testRole"
      },
      {
        value: "testRole2"
      }
    ]
  };

  test("raises error for missing properties", () => {
    R.forEach(
      key =>
        expect(() => {
          parseDataClient(R.dissoc(key, testParams));
        }).toThrowErrorMatchingSnapshot(),
      R.keys(testParams)
    );
  });

  test("build Language object from given object", () => {
    expect(parseDataClient(testParams)).toEqual(
      new DataClient(
        testParams.href,
        testParams.id,
        testParams.email,
        new Language(testParams.language.item_id, testParams.language.value),
        [testParams.roles[0].value, testParams.roles[1].value]
      )
    );
  });
});

describe("parseSmallDataClient", () => {
  const testParams = {
    id: "testId",
    href: "testHref"
  };

  test("raises error for missing properties", () => {
    R.forEach(
      key =>
        expect(() => {
          parseSmallDataClient(R.dissoc(key, testParams));
        }).toThrowErrorMatchingSnapshot(),
      R.keys(testParams)
    );
  });

  test("build Language object from given object", () => {
    expect(parseSmallDataClient(testParams)).toEqual(
      new DataClient(testParams.href, testParams.id, "", null, [])
    );
  });
});

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
