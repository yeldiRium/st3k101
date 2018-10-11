import { extractJson, extractJsonPlusLanguage } from "../Response";

const testContent = {
  lorem: "ipsum"
};
const mockResponse = {
  json() {
    return new Promise((resolve, ignore) => {
      resolve(testContent);
    });
  },
  headers: {
    get(what) {
      if (what === "Content-Language") {
        return "testLanguage";
      }
      return "somethingElse";
    }
  }
};

describe("extractJson", () => {
  test("return future of json content", done => {
    extractJson(mockResponse).fork(
      () => {
        done.fail("Future rejected when it shouldn't.");
      },
      success => {
        expect(success).toEqual(testContent);
        done();
      }
    );
  });
});

describe("extractJsonPlusLanguage", () => {
  test("returns future of content and language", done => {
    extractJsonPlusLanguage(mockResponse).fork(
      () => {
        done.fail("Future rejected when it shouldn't.");
      },
      success => {
        expect(success).toEqual({
          data: testContent,
          language: "testLanguage"
        });
        done();
      }
    );
  });
});
