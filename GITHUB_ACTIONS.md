# GitHub Actions Setup Guide

This document explains the GitHub Actions workflows configured for Toddle Ops.

## 📋 Workflows Overview

### 1. Code Quality (`ruff.yml`) ✅
**Status:** Improved from existing workflow

- **Linting:** Runs `ruff check` with GitHub annotations
- **Formatting:** Verifies code formatting with `ruff format --check`
- **Triggers:** Push and PR to `main` and `develop`
- **Changes from original:**
  - Split into separate lint and format jobs
  - Uses `setup-uv` for consistency
  - Added proper Python setup
  - Uses GitHub output format for better PR annotations

### 2. Type Checking (`typecheck.yml`) ✨ NEW
**Type checking with both mypy and pyright**

- **mypy:** Traditional type checker with ignore-missing-imports
- **pyright:** Modern type checker from Microsoft
- **Continue on error:** Won't block PRs initially
- **Recommendation:** Fix type issues incrementally

### 3. Tests (`test.yml`) ✨ NEW
**Automated test suite**

- **Matrix testing:** Python 3.13 and 3.14
- **Coverage:** Uploads to Codecov (needs `CODECOV_TOKEN` secret)
- **Dependencies:** Installs all extras via uv
- **Environment:** Requires `GOOGLE_API_KEY` secret

### 4. Database Tests (`database-tests.yml`) ✨ NEW
**Supabase/PostgreSQL integration testing**

- **PostgreSQL service:** Runs Supabase-compatible Postgres 15
- **Health checks:** Ensures DB is ready before tests
- **Connection testing:** Validates session service
- **Secrets needed:**
  - `GOOGLE_API_KEY`
  - `SUPABASE_USER` (optional, defaults to postgres)
  - `SUPABASE_PASSWORD` (optional, defaults to postgres)

### 5. Release & Changelog (`release.yml`) ✨ NEW
**Automated semantic versioning and releases**

- **Release Please:** Google's automated release tool
- **Conventional Commits:** Uses commit messages to determine version bumps
  - `feat:` → Minor version bump
  - `fix:` → Patch version bump
  - `feat!:` or `BREAKING CHANGE:` → Major version bump
- **Changelog:** Auto-generated from commit messages
- **PyPI publishing:** Builds and publishes on release (needs `PYPI_API_TOKEN`)

**Commit message format:**
```
feat: add new safety validation rule
fix: handle None in memory service callback
docs: update README with Supabase info
perf: optimize agent response time
refactor: simplify plugin error handling
```

### 6. Performance Benchmarks (`benchmark.yml`) ✨ NEW
**Track performance over time**

- **pytest-benchmark:** Runs performance tests
- **Trend tracking:** Stores results and tracks changes
- **Alert on regression:** Warns if performance degrades >150%
- **Agent metrics:** Measures response time and token usage
- **PR comments:** Posts performance results on pull requests

### 7. Docker Build (`docker.yml`) ✨ NEW
**Container image building and publishing**

- **Multi-platform:** Builds for linux/amd64
- **GitHub Container Registry:** Publishes to ghcr.io
- **Tagging strategy:**
  - Branch pushes: `main`, `develop`
  - PRs: `pr-123`
  - Tags: `v1.0.0`, `1.0`, `latest`
- **Caching:** Uses GitHub Actions cache for faster builds
- **Testing:** Smoke tests on PR builds

### 8. Security Scanning (`security.yml`) ✨ NEW
**Automated security vulnerability scanning**

- **Bandit:** Python security linter
- **Safety:** Dependency vulnerability checker
- **CodeQL:** GitHub's semantic code analysis
- **Schedule:** Runs weekly on Mondays
- **Reports:** Uploads findings as artifacts

### 9. Dependabot (`dependabot.yml`) ✅
**Status:** Improved from existing config

**Additions:**
- GitHub Actions dependency updates
- Docker base image updates
- Grouped updates by category (google-adk, pydantic, database, dev)
- Ignores major version updates by default
- PR limits and scheduling
- Auto-assigns reviewers

## 🔐 Required Secrets

Add these in GitHub Settings → Secrets and Variables → Actions:

### Essential
- `GOOGLE_API_KEY` - Your Gemini API key (required for tests)

### Optional but Recommended
- `PYPI_API_TOKEN` - For automated PyPI publishing
- `CODECOV_TOKEN` - For coverage reporting
- `SUPABASE_USER` - For database tests (defaults to postgres)
- `SUPABASE_PASSWORD` - For database tests (defaults to postgres)

## 🎯 Next Steps

### 1. Enable Workflows
All workflows are created but need to be enabled:
```bash
git add .github/
git commit -m "feat: add comprehensive GitHub Actions workflows"
git push
```

### 2. Configure Secrets
Go to Settings → Secrets → Actions and add required secrets

### 3. Set Up Branch Protection
Recommended rules for `main` branch:
- Require status checks to pass:
  - Ruff Linting
  - Ruff Formatting
  - Test Python 3.13
  - Type Check with mypy
- Require branches to be up to date
- Require conversation resolution

### 4. Configure Codecov (Optional)
1. Sign up at https://codecov.io
2. Connect your repository
3. Copy the upload token
4. Add as `CODECOV_TOKEN` secret

### 5. Enable Release Please
On first merge to main, Release Please will:
1. Create a release PR with changelog
2. Update version in pyproject.toml
3. When you merge that PR, it creates a GitHub release

### 6. Docker Registry Setup
Images will be published to: `ghcr.io/asenetcky/toddle-ops`
- Automatically enabled with `GITHUB_TOKEN`
- Images are private by default
- Make public: Package settings → Change visibility

## 📊 Workflow Status Badges

Add these to your README.md:

```markdown
[![Code Quality](https://github.com/asenetcky/toddle-ops/actions/workflows/ruff.yml/badge.svg)](https://github.com/asenetcky/toddle-ops/actions/workflows/ruff.yml)
[![Tests](https://github.com/asenetcky/toddle-ops/actions/workflows/test.yml/badge.svg)](https://github.com/asenetcky/toddle-ops/actions/workflows/test.yml)
[![Type Check](https://github.com/asenetcky/toddle-ops/actions/workflows/typecheck.yml/badge.svg)](https://github.com/asenetcky/toddle-ops/actions/workflows/typecheck.yml)
[![Security](https://github.com/asenetcky/toddle-ops/actions/workflows/security.yml/badge.svg)](https://github.com/asenetcky/toddle-ops/actions/workflows/security.yml)
[![Docker](https://github.com/asenetcky/toddle-ops/actions/workflows/docker.yml/badge.svg)](https://github.com/asenetcky/toddle-ops/actions/workflows/docker.yml)
```

## 🐛 Troubleshooting

### Tests fail with API key error
Add `GOOGLE_API_KEY` to repository secrets

### Docker build fails
Check that Dockerfile and .dockerignore are committed

### Release Please not creating PRs
- Ensure commits follow conventional commit format
- Check workflow has `contents: write` permission

### Type checks failing
- Set `continue-on-error: true` (already configured)
- Fix issues incrementally
- Remove flag once codebase is fully typed

## 💡 Tips

1. **Commit messages matter** - Use conventional commits for automatic versioning
2. **Small PRs** - Easier to pass all checks
3. **Local testing** - Run `make ruff` and `pytest` before pushing
4. **Docker testing** - Test locally: `docker build -t toddle-ops .`
5. **Monitor costs** - GitHub Actions has usage limits on free tier

## 🎨 Customization

### Adjust Python versions
Edit `test.yml` matrix:
```yaml
python-version: ["3.13", "3.14", "3.15"]
```

### Change benchmark threshold
Edit `benchmark.yml`:
```yaml
alert-threshold: '200%'  # More lenient
```

### Modify release types
Edit `release.yml` changelog types to customize what appears in releases

### Docker platforms
Add ARM support in `docker.yml`:
```yaml
platforms: linux/amd64,linux/arm64
```
