import {
  categorizeResponse,
  extractJson,
  extractJsonPlusLanguage
} from "../Response";
import {
  AuthorizationError,
  BadRequestError,
  ConflictError,
  ForbiddenError,
  InternalServerError,
  NotFoundError,
  UnknownError
} from "../../Errors";
import * as Future from "fluture";
import * as R from "ramda";

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
  },
  status: 200
};

describe("categorizeResponse", () => {
  const knownStatus = [
    // Creates a list of the numbers 200..299.
    ...Array.from({ length: 100 }, (x, i) => i + 200),
    400,
    401,
    403,
    404,
    409,
    500
  ];

  afterEach(() => {
    mockResponse.status = 200;
  });

  /**
   * Tests all status codes from 200 to 299.
   */
  test("resolves 200 <= status < 300 with its json content", done => {
    const futures = R.compose(
      R.map(([mockResponse, categorizedResponse]) =>
        categorizedResponse.chain(success => {
          expect(success).toEqual(mockResponse);
          return Future.of();
        })
      ),
      R.map(mockResponse => [mockResponse, categorizeResponse(mockResponse)]),
      R.map(R.assoc("status", R.__, mockResponse))
    )(R.range(200, 300));

    Future.parallel(Infinity, futures).fork(
      () => {
        done.fail("A future rejected. This should be impossible.");
      },
      () => {
        done();
      }
    );
  });

  test("categorizes 400 as BadRequestError", done => {
    mockResponse.status = 400;
    categorizeResponse(mockResponse).fork(
      error => {
        expect(error).toEqual(new BadRequestError("Bad request.", testContent));
        done();
      },
      () => {
        done.fail("resolved a 400 response.");
      }
    );
  });

  test("categorizes 401 as AuthorizationError", done => {
    mockResponse.status = 401;
    categorizeResponse(mockResponse).fork(
      error => {
        expect(error).toEqual(new AuthorizationError("Not authorized."));
        done();
      },
      () => {
        done.fail("resolved a 401 response.");
      }
    );
  });

  test("categorizes 403 as ForbiddenError", done => {
    mockResponse.status = 403;
    categorizeResponse(mockResponse).fork(
      error => {
        expect(error).toEqual(new ForbiddenError("Forbidden."));
        done();
      },
      () => {
        done.fail("resolved a 403 response.");
      }
    );
  });

  test("categorizes 404 as NotFoundError", done => {
    mockResponse.status = 404;
    categorizeResponse(mockResponse).fork(
      error => {
        expect(error).toEqual(new NotFoundError("Resource not found."));
        done();
      },
      () => {
        done.fail("resolved a 404 response.");
      }
    );
  });

  test("categorizes 409 as ConflictError", done => {
    mockResponse.status = 409;
    categorizeResponse(mockResponse).fork(
      error => {
        expect(error).toEqual(
          new ConflictError("Conflicting data.", testContent)
        );
        done();
      },
      () => {
        done.fail("resolved a 409 response.");
      }
    );
  });

  test("categorizes 500 as InternalServerError", done => {
    mockResponse.status = 500;
    categorizeResponse(mockResponse).fork(
      error => {
        expect(error).toEqual(
          new InternalServerError("Internal server error.")
        );
        done();
      },
      () => {
        done.fail("resolved a 500 response.");
      }
    );
  });

  /**
   * Tests 200 random status codes which are not in the `knownStatus` array.
   */
  test("categorizes everything unknown as UnknownError", done => {
    const futures = R.compose(
      R.map(categorizedResponse =>
        categorizedResponse.chainRej(error => {
          expect(error).toEqual(
            new UnknownError("Conflicting data.", testContent)
          );
          return Future.of();
        })
      ),
      R.map(categorizeResponse),
      R.map(R.assoc("status", R.__, mockResponse)),
      R.difference(R.__, knownStatus)
    )(R.times(() => Math.round(Math.random() * 500 + 100), 200));

    Future.parallel(Infinity, futures).fork(
      () => {
        done.fail("A future rejected. This should be impossible.");
      },
      () => {
        done();
      }
    );
  });
});

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
