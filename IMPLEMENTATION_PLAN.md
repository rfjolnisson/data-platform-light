# Data Platform Light - Implementation Plan

## Overview
Building a lightweight EL (Extract-Load) data platform using `dlt` that captures complete raw JSON payloads from Jira, Bitbucket, and Jenkins into a Bronze layer (JSONL files), with Silver transformation capabilities to be added later.

## Implementation Units

### Unit 1: Project Foundation & Structure
**Estimated Time: 30-45 minutes**

**Goals:**
- Create the complete directory structure
- Set up Python environment with dlt
- Create basic configuration system
- Implement secrets management pattern

**Deliverables:**
```
/data-platform-light/
  /config/
    sources.yaml
    time.yaml
    identity.yaml
    ai_policy.yaml
    secrets.example.env
  /bronze/           # Will be populated by pipelines
  /pipelines/
    /dlt/
      __init__.py
      pipelines.py
      /resources/
        __init__.py
  /sql/              # Placeholder for Silver/Gold
  /agent/            # Placeholder for LlamaIndex tools
  /scripts/          # Utility scripts
  requirements.txt
  Makefile
  .env.example
  .gitignore
  README.md
```

**Key Components:**
1. **requirements.txt** with dlt, PyYAML, pandas, pyarrow
2. **Basic YAML configs** matching the spec
3. **Environment variable patterns** for secrets
4. **Makefile skeleton** with placeholder targets
5. **Basic validation scripts** for environment setup

**Acceptance Criteria:**
- `make check` validates environment and API connectivity
- `make bootstrap` sets up Python environment
- Configuration files load without errors
- Directory structure matches specification

---

### Unit 2: dlt Foundation & Core Infrastructure
**Estimated Time: 45-60 minutes**

**Goals:**
- Implement dlt pipeline foundation
- Create manifest and cursor tracking system
- Build Bronze layer file management
- Implement JSONL + Parquet pattern

**Deliverables:**
1. **Core dlt pipeline structure** in `pipelines/dlt/pipelines.py`
2. **Manifest tracking system** (manifest.parquet writes)
3. **Cursor management** (cursors.parquet upserts)
4. **Bronze file organization** (YYYY/MM/DD partitioning)
5. **Record envelope system** (`__source`, `__stream`, `__ingested_at_utc`, `__run_id`)

**Key Components:**
- Base pipeline class with common functionality
- File chunking logic (50-200MB compressed)
- Incremental sync with safety windows
- Error handling and retry logic
- UTF-8 normalization and error tracking

**Acceptance Criteria:**
- Can create and update manifest.parquet files
- Cursor tracking works with upsert logic
- JSONL files are properly partitioned and compressed
- Record envelopes are correctly applied
- Basic incremental sync logic functions

---

### Unit 3: Jira Pipeline Implementation
**Estimated Time: 60-90 minutes**

**Goals:**
- Implement complete Jira Cloud REST v3 integration
- Handle all specified streams (issues, changelogs, projects, sprints, etc.)
- Implement JQL-based incremental sync
- Handle Jira-specific pagination and rate limiting

**Deliverables:**
1. **Jira resource extractors** for each stream type
2. **JQL query building** with project filtering
3. **Expand parameter handling** (renderedFields, changelog, transitions)
4. **Child stream extraction** (worklogs, attachments metadata)
5. **Account ID field handling**

**Key Streams:**
- `issues` (with configurable expands)
- `issue_changelogs` (separate stream even when expanded)
- `projects`
- `boards` and `sprints`
- `users` (referenced only)
- `worklogs`
- `attachments` (metadata only)

**Acceptance Criteria:**
- `make sync-jira` successfully extracts all streams
- Incremental sync by `updated` field works correctly
- Full payloads are preserved (no field drops)
- Rate limiting is handled gracefully
- Safety window logic prevents data gaps

---

### Unit 4: Bitbucket Pipeline Implementation
**Estimated Time: 60-90 minutes**

**Goals:**
- Implement Bitbucket Cloud v2 API integration
- Handle repository enumeration and filtering
- Implement PR and commit extraction with activities
- Handle Bitbucket-specific pagination

**Deliverables:**
1. **Bitbucket resource extractors** for each stream type
2. **Repository discovery** (explicit list or workspace-wide)
3. **Pull request extraction** with participants, links, merge fields
4. **Activity stream extraction** (comments, approvals, changes)
5. **Commit extraction** with PR mapping

**Key Streams:**
- `pull_requests` (all states: OPEN/MERGED/DECLINED)
- `pr_activities` (comments, approvals, changes requested)
- `commits` (per repo, with PR mapping when possible)
- `repositories` (metadata)
- `refs/branches` (for main/release pattern identification)

**Acceptance Criteria:**
- `make sync-bitbucket` successfully extracts all streams
- Incremental sync by `updated_on` (PRs) and `date` (commits)
- PR activities are correctly linked to PRs
- Repository filtering works as configured
- Commit-to-PR relationships are preserved

---

### Unit 5: Jenkins Pipeline Implementation
**Estimated Time: 45-60 minutes**

**Goals:**
- Implement Jenkins JSON API integration
- Handle job enumeration with pattern matching
- Extract build data with parameters and changesets
- Implement build number-based incremental sync

**Deliverables:**
1. **Jenkins resource extractors** for jobs and builds
2. **Job pattern matching** (include/exclude patterns)
3. **Build extraction** with full metadata
4. **Changeset inclusion** (configurable)
5. **Queue snapshots** (optional)

**Key Streams:**
- `jobs` (names, URLs, metadata)
- `builds` (per job: number, timestamp, duration, result, actions, changeSets)
- `queue` (optional snapshots)

**Acceptance Criteria:**
- `make sync-jenkins` successfully extracts all streams
- Job pattern filtering works correctly
- Build incremental sync by number or timestamp
- ChangeSets are included when configured
- Build parameters and actions are fully captured

---

### Unit 6: CLI Interface & Automation
**Estimated Time: 30-45 minutes**

**Goals:**
- Complete Makefile implementation
- Add utility scripts for monitoring and maintenance
- Implement backfill functionality
- Create status and reporting commands

**Deliverables:**
1. **Complete Makefile** with all specified targets
2. **Backfill pipeline** with configurable lookback days
3. **Status reporting** (cursors, manifest, stats)
4. **Utility scripts** for Bronze layer inspection

**Makefile Targets:**
- `make check` - Environment validation
- `make bootstrap` - Setup and installation
- `make sync-jira/bitbucket/jenkins` - Individual syncs
- `make sync-all` - Run all pipelines
- `make backfill DAYS=120` - Historical data extraction
- `make show-cursors/manifest` - Status reporting
- `make stats SOURCE=X STREAM=Y` - Data statistics

**Acceptance Criteria:**
- All Makefile targets execute successfully
- Backfill can reset cursors and re-extract historical data
- Status commands provide useful operational information
- Error handling and logging are comprehensive
- Concurrent execution works as configured

---

### Unit 7: Testing & Validation
**Estimated Time: 45-60 minutes**

**Goals:**
- Create comprehensive testing framework
- Implement data validation checks
- Add Bronze layer quality assurance
- Create operational monitoring tools

**Deliverables:**
1. **Unit tests** for core pipeline functionality
2. **Integration tests** with mock APIs
3. **Data validation scripts** for Bronze layer quality
4. **Operational monitoring** tools
5. **Bronze reporting utility**

**Key Components:**
- Test fixtures for API responses
- Manifest and cursor validation
- JSONL file integrity checks
- Performance monitoring
- Error detection and alerting

**Acceptance Criteria:**
- Test suite covers all major functionality
- Data validation catches common issues
- Performance metrics are tracked
- Error conditions are properly handled
- Operational tools provide actionable insights

---

---

### Unit 8: Remote Deployment & Cursor Integration
**Estimated Time: 45-60 minutes**

**Goals:**
- Set up minimal remote deployment with zero-config push from Cursor
- Automate environment setup and scheduling
- Enable seamless development workflow

**Deployment Strategy: GitHub Actions + Self-hosted Runner**

#### Workflow Overview
```yaml
# .github/workflows/sync-data.yml
name: Data Platform Sync
on:
  push: 
    branches: [main]
    paths: ['pipelines/**', 'config/**', 'Makefile', 'requirements.txt']
  schedule: 
    - cron: '0 2 * * *'    # 2 AM Berlin time daily
  workflow_dispatch:       # Manual trigger
    inputs:
      action:
        type: choice
        options: ['sync-all', 'sync-jira', 'sync-bitbucket', 'sync-jenkins', 'backfill']
      backfill_days:
        type: string
        default: '7'

jobs:
  sync:
    runs-on: self-hosted
    timeout-minutes: 120
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          cache: 'pip'
      - name: Install dependencies
        run: make bootstrap
      - name: Validate environment
        run: make check
      - name: Run data sync
        run: |
          if [ "${{ github.event_name }}" == "workflow_dispatch" ]; then
            if [ "${{ inputs.action }}" == "backfill" ]; then
              make backfill DAYS=${{ inputs.backfill_days }}
            else
              make ${{ inputs.action }}
            fi
          else
            make sync-all
          fi
        env:
          JIRA_BASE_URL: ${{ secrets.JIRA_BASE_URL }}
          JIRA_EMAIL: ${{ secrets.JIRA_EMAIL }}
          JIRA_API_TOKEN: ${{ secrets.JIRA_API_TOKEN }}
          BITBUCKET_BASE_URL: ${{ secrets.BITBUCKET_BASE_URL }}
          BITBUCKET_USERNAME: ${{ secrets.BITBUCKET_USERNAME }}
          BITBUCKET_APP_PASSWORD: ${{ secrets.BITBUCKET_APP_PASSWORD }}
          JENKINS_BASE_URL: ${{ secrets.JENKINS_BASE_URL }}
          JENKINS_USERNAME: ${{ secrets.JENKINS_USERNAME }}
          JENKINS_TOKEN: ${{ secrets.JENKINS_TOKEN }}
      - name: Upload Bronze artifacts
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: bronze-data-${{ github.run_number }}
          path: |
            bronze/**/manifest.parquet
            bronze/**/cursors.parquet
          retention-days: 30
```

#### Self-hosted Runner Setup
```bash
# One-time runner setup on your VPS/server
# GitHub will provide the exact commands when you add the runner
./config.sh --url https://github.com/yourusername/data-platform-light --token YOUR_TOKEN
sudo ./svc.sh install
sudo ./svc.sh start
```

**Deliverables:**
1. **GitHub Actions workflow** (`.github/workflows/sync-data.yml`)
2. **Self-hosted runner setup scripts** (`scripts/setup-runner.sh`)
3. **Manual trigger interface** (GitHub UI with action dropdown)
4. **Automated scheduling** (2 AM Berlin time daily)
5. **Secrets management** (GitHub repository secrets)
6. **Artifact collection** (manifest/cursor files uploaded to GitHub)

**Key Components:**
- GitHub Actions workflow with multiple triggers
- Self-hosted runner installation and service setup
- Repository secrets for API credentials
- Workflow dispatch for manual runs with parameters
- Artifact upload for manifest/cursor tracking
- Smart path-based triggering (only run when code changes)

**Your Development Workflow from Cursor:**
```bash
# 1. Develop locally as normal
# 2. Commit and push to main branch
git add .
git commit -m "Update Jira extraction logic"
git push origin main
# 3. GitHub Actions automatically runs sync-all

# Or trigger manually with specific action:
# Go to GitHub Actions tab → "Data Platform Sync" → "Run workflow"
# Choose: sync-jira, backfill with 30 days, etc.
```

**Acceptance Criteria:**
- Push to main automatically triggers data sync
- Manual workflow dispatch works with all sync options
- Daily scheduled runs execute at 2 AM Berlin time
- All API secrets are securely stored in GitHub
- Bronze data persists on self-hosted runner between runs
- Manifest and cursor files are uploaded as artifacts for monitoring

---

## Implementation Strategy

### Phase 1: Foundation (Units 1-2)
Build the core infrastructure and dlt foundation. This creates the platform for all data extraction work.

### Phase 2: Data Sources (Units 3-5)
Implement each data source pipeline individually. Each can be developed and tested independently.

### Phase 3: Operations (Units 6-7)
Complete the operational tooling and testing framework.

### Phase 4: Deployment (Unit 8)
Set up remote deployment and automation for production use.

## Success Metrics

1. **Completeness**: All specified API endpoints and fields are captured
2. **Reliability**: Incremental sync works correctly with no data gaps
3. **Performance**: Files are appropriately chunked and compressed
4. **Maintainability**: Clear error messages and operational visibility
5. **Extensibility**: Easy to add new data sources or modify existing ones

## Next Steps

Ready to begin with **Unit 1: Project Foundation & Structure**. This will establish the basic project layout, configuration system, and development environment.

Would you like me to proceed with Unit 1 implementation?
