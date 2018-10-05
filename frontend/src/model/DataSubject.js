class DataSubject {
  // does not extend Party, as this is not a real resource
  /**
   * A user who submits data to the survey platform.
   *
   * @param {string} id
   * @param {string} email
   * @param {string} ltiUserId
   * @param {string} moodleUsername
   * @param {string} source The source LMS.
   */
  constructor(id, email, ltiUserId, moodleUsername, source) {
    this._id = id;
    this._email = email;
    this._ltiUserId = ltiUserId;
    this._moodleUsername = moodleUsername;
    this._source = source;
  }

  clone() {
    return new DataSubject(
      this._id,
      this._email,
      this._ltiUserId,
      this._moodleUsername,
      this._source
    );
  }

  get id() {
    return this._id;
  }

  get source() {
    return this._source;
  }

  get moodleUsername() {
    return this._moodleUsername;
  }

  get ltiUserId() {
    return this._ltiUserId;
  }

  get email() {
    return this._email;
  }
}

export default DataSubject;

export { DataSubject };
