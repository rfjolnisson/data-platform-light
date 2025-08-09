# Data Platform Light

A lightweight EL (Extract-Load) data platform using `dlt` that captures complete raw JSON payloads from Jira, Bitbucket, and Jenkins into a Bronze layer for later Silver/Gold transformations.

## Quick Start

1. **Setup environment**:
   ```bash
   make bootstrap
   ```

2. **Configure secrets** (copy your actual values):
   ```bash
   cp config/secrets.example.env .env
   # Edit .env with your actual API credentials
   ```

3. **Validate setup**:
   ```bash
   make check
   ```

4. **Run data sync**:
   ```bash
   make sync-all
   ```

## Architecture

### Bronze Layer (Raw Data)
- **Format**: JSONL files, gzipped
- **Partitioning**: `YYYY/MM/DD` by collection date
- **Location**: `./bronze/{source}/{stream}/YYYY/MM/DD/*.jsonl.gz`
- **Metadata**: `manifest.parquet` and `cursors.parquet` per source

### Data Sources

#### Jira (Atlassian Cloud)
- **Issues** with configurable expands (renderedFields, changelog)
- **Projects**, **Boards**, **Sprints**  
- **Users**, **Worklogs**, **Attachments** (metadata only)
- **Incremental**: by `updated` field with safety window

#### Bitbucket (Cloud v2)
- **Pull Requests** (all states) with participants, links
- **PR Activities** (comments, approvals, changes)
- **Commits**, **Repositories**, **Branches**
- **Incremental**: by `updated_on` (PRs) and `date` (commits)

#### Jenkins (JSON API)
- **Jobs** and **Builds** with parameters, actions, changesets
- **Queue** snapshots (optional)
- **Incremental**: by build number or timestamp

## Configuration

All configuration is in `config/` directory:

- `sources.yaml` - API endpoints, pagination, incremental settings
- `time.yaml` - Timezone (Europe/Berlin), scheduling preferences  
- `identity.yaml` - User matching rules across systems
- `ai_policy.yaml` - AI processing policies (for future use)
- `secrets.example.env` - Template for API credentials

## Commands

### Setup & Validation
```bash
make bootstrap       # Install dependencies, create directories
make check          # Validate environment and API connectivity
```

### Data Operations
```bash
make sync-all       # Run all pipelines
make sync-jira      # Jira only
make sync-bitbucket # Bitbucket only  
make sync-jenkins   # Jenkins only
make backfill DAYS=120  # Historical data extraction
```

### Status & Monitoring
```bash
make show-cursors   # Current incremental positions
make show-manifest  # Files and record counts
make stats SOURCE=jira STREAM=issues  # Data statistics
```

## GitHub Actions Deployment

Push to `main` branch automatically triggers data sync. Manual triggers available in GitHub Actions tab:

- **Scheduled**: Daily at 2 AM Berlin time
- **On Push**: When pipeline code changes
- **Manual**: Choose specific action (sync-all, backfill, etc.)

### Setup Self-hosted Runner

1. Go to repo Settings → Actions → Runners → Add runner
2. Follow GitHub's setup instructions on your server
3. Add repository secrets for all API credentials

## Development

### Project Structure
```
├── config/           # YAML configurations
├── pipelines/dlt/    # DLT pipeline code
├── scripts/          # Utility scripts  
├── bronze/           # Raw data output (gitignored)
├── .github/workflows/ # GitHub Actions
└── Makefile          # CLI interface
```

### Implementation Status

- ✅ **Unit 1**: Project foundation and structure
- ⏳ **Unit 2**: DLT foundation and manifest/cursor tracking
- ⏳ **Unit 3**: Jira pipeline implementation  
- ⏳ **Unit 4**: Bitbucket pipeline implementation
- ⏳ **Unit 5**: Jenkins pipeline implementation
- ⏳ **Unit 6**: CLI interface completion
- ⏳ **Unit 7**: Testing and validation
- ⏳ **Unit 8**: Deployment automation

## Next Steps

1. **Unit 2**: Implement core DLT infrastructure with manifest/cursor tracking
2. **Unit 3**: Build Jira extraction pipeline with full API coverage
3. **Unit 4**: Build Bitbucket extraction pipeline  
4. **Unit 5**: Build Jenkins extraction pipeline
5. **Silver Layer**: Transform Bronze → normalized tables (future)

## License

MIT License - see LICENSE file for details.
