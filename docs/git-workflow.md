# Git workflow and source-control procedure

1. `main` is the stable branch; `develop` is the integration branch.
2. Create feature branches from `develop`: `feature/<short-description>`.
3. Commit small, meaningful changes using messages such as `feat: add user endpoint`.
4. Push the feature branch and open a PR into `develop`.
5. Require review and passing Jenkins checks before merging.
6. Promote tested changes from `develop` to `main` through a release PR.
7. Use `hotfix/<short-description>` from `main` for urgent fixes, then merge back into `develop`.

Suggested Git commands:

```bash
git checkout main
git pull origin main
git checkout -b develop
git push -u origin develop

git checkout develop
git pull origin develop
git checkout -b feature/my-change
git add .
git commit -m "feat: describe the change"
git push -u origin feature/my-change
```

Never commit secrets. If a secret is exposed, revoke/rotate it immediately and clean history as appropriate.
