import { extractJson } from "../Response";

describe("extractJson", () => {
  test("return future of json content", done => {
    const testContent = {
      lorem: "ipsum"
    };
    const mockJson = {
      json() {
        return new Promise((resolve, ignore) => {
          resolve(testContent);
        });
      }
    };

    extractJson(mockJson).fork(
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
