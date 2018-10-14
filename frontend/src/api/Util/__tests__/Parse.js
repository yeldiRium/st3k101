import * as R from "ramda";

import {
  parseDataClient,
  parseDataSubject,
  parseEmailBlacklistChallenge,
  parseEMailWhitelistChallenge,
  parseLanguage,
  parseLanguageData,
  parsePasswordChallenge,
  parseResource,
  parseRoles,
  parseSmallDataClient
} from "../Parse";
import { Language, LanguageData } from "../../../model/Language";
import { Resource } from "../../../model/Resource";
import { DataClient } from "../../../model/DataClient";
import { DataSubject } from "../../../model/DataSubject";
import EMailWhitelist from "../../../model/SurveyBase/Challenge/EMailWhitelist";
import Password from "../../../model/SurveyBase/Challenge/Password";

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

  test("build Resource object from given object", () => {
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

  test("build role list from given object", () => {
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

  test("build DataClient object from given object", () => {
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

  test("build small DataClient object from given object", () => {
    expect(parseSmallDataClient(testParams)).toEqual(
      new DataClient(testParams.href, testParams.id, "", null, [])
    );
  });
});

describe("parseDataSubject", () => {
  const testParams = {
    id: "testId",
    email: "testEmail",
    lti_user_id: "testLtiUserUd",
    moodle_username: "testMoodleUsername",
    source: "testSource"
  };

  test("raises error for missing properties", () => {
    R.forEach(
      key =>
        expect(() => {
          parseDataSubject(R.dissoc(key, testParams));
        }).toThrowErrorMatchingSnapshot(),
      R.keys(testParams)
    );
  });

  test("build DataSubject object from given object", () => {
    expect(parseDataSubject(testParams)).toEqual(
      new DataSubject(
        testParams.id,
        testParams.email,
        testParams.lti_user_id,
        testParams.moodle_username,
        testParams.source
      )
    );
  });
});

describe("parseChallenges", () => {});

describe("parseEMailWhitelistChallenge", () => {
  const testParams = {
    email_whitelist_enabled: true,
    email_whitelist: "test"
  };

  test("raises error for missing properties", () => {
    R.forEach(
      key =>
        expect(() => {
          parseEMailWhitelistChallenge(R.dissoc(key, testParams));
        }).toThrowErrorMatchingSnapshot(),
      R.keys(testParams)
    );
  });

  test("build EMailWhiteList object from given object", () => {
    expect(parseEMailWhitelistChallenge(testParams)).toEqual(
      new EMailWhitelist(
        testParams.email_whitelist_enabled,
        testParams.email_whitelist
      )
    );
  });
});

describe("parseEmailBlacklistChallenge", () => {
  const testParams = {
    email_blacklist_enabled: true,
    email_blacklist: "test"
  };

  test("raises error for missing properties", () => {
    R.forEach(
      key =>
        expect(() => {
          parseEmailBlacklistChallenge(R.dissoc(key, testParams));
        }).toThrowErrorMatchingSnapshot(),
      R.keys(testParams)
    );
  });

  test("build EmailWhiteList object from given object", () => {
    expect(parseEmailBlacklistChallenge(testParams)).toEqual(
      new EMailWhitelist(
        testParams.email_blacklist_enabled,
        testParams.email_blacklist
      )
    );
  });
});

describe("parsePasswordChallenge", () => {
  const testParams = {
    password_enabled: true,
    password: "test"
  };

  test("raises error for missing properties", () => {
    R.forEach(
      key =>
        expect(() => {
          parsePasswordChallenge(R.dissoc(key, testParams));
        }).toThrowErrorMatchingSnapshot(),
      R.keys(testParams)
    );
  });

  test("build EmailWhiteList object from given object", () => {
    expect(parsePasswordChallenge(testParams)).toEqual(
      new Password(testParams.password_enabled, testParams.password)
    );
  });
});

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
