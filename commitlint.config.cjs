// commitlint.config.cjs
module.exports = {
  extends: ['@commitlint/config-conventional'],

  // optional: ignore merge commits and your automated release/changelog commits
  ignores: [
    (msg) => msg.startsWith('Merge '),
    (msg) => /^chore\(release\): v\d+\.\d+\.\d+/.test(msg),
    (msg) => /^docs\(changelog\):/.test(msg),
  ],
};
