const Roles = Object.freeze({
  Root: 0,
  Admin: 10,
  Contributor: 20,
  User: 30
});

function isAtLeast(dataClient, role) {
  return Math.min(...dataClient.roles) <= role;
}

export default Roles;

export { Roles, isAtLeast };
