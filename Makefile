# Data Platform Light - Makefile
# CLI interface for all pipeline operations

.PHONY: help bootstrap check sync-all sync-jira sync-bitbucket sync-jenkins backfill show-cursors show-manifest stats clean

# Default target
help:
	@echo "Data Platform Light - Available Commands:"
	@echo ""
	@echo "Setup & Validation:"
	@echo "  make bootstrap       - Install dependencies and setup environment"
	@echo "  make check          - Validate environment and API connectivity"
	@echo ""
	@echo "Data Sync Operations:"
	@echo "  make sync-all       - Run all data pipelines (jira + bitbucket + jenkins)"
	@echo "  make sync-jira      - Sync Jira data only"
	@echo "  make sync-bitbucket - Sync Bitbucket data only"  
	@echo "  make sync-jenkins   - Sync Jenkins data only"
	@echo ""
	@echo "Backfill & Maintenance:"
	@echo "  make backfill DAYS=120  - Backfill historical data (default: 120 days)"
	@echo "  make show-cursors       - Display current cursor positions"
	@echo "  make show-manifest      - Display manifest summary"
	@echo "  make stats SOURCE=jira STREAM=issues  - Show data statistics"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean          - Clean temporary files"

# Setup and validation
bootstrap:
	@echo "🚀 Setting up Data Platform Light..."
	pip install -r requirements.txt
	@mkdir -p bronze/jira bronze/bitbucket bronze/jenkins
	@mkdir -p logs
	@echo "✅ Bootstrap complete"

check:
	@echo "🔍 Validating environment..."
	python3 scripts/validate_env.py

# Main sync operations
sync-all:
	@echo "🔄 Starting full data sync..."
	@$(MAKE) sync-jira
	@$(MAKE) sync-bitbucket  
	@$(MAKE) sync-jenkins
	@echo "✅ Full sync complete"

sync-jira:
	@echo "📋 Syncing Jira data..."
	# TODO: Implement in Unit 3
	@echo "⚠️  Jira sync not yet implemented (Unit 3)"

sync-bitbucket:
	@echo "🔧 Syncing Bitbucket data..."
	# TODO: Implement in Unit 4
	@echo "⚠️  Bitbucket sync not yet implemented (Unit 4)"

sync-jenkins:
	@echo "🏗️  Syncing Jenkins data..."
	# TODO: Implement in Unit 5
	@echo "⚠️  Jenkins sync not yet implemented (Unit 5)"

# Backfill operations
backfill:
	@echo "⏪ Starting backfill for $(DAYS) days..."
	# TODO: Implement in Unit 2
	@echo "⚠️  Backfill not yet implemented (Unit 2)"

# Status and reporting
show-cursors:
	@echo "📍 Current cursor positions:"
	# TODO: Implement in Unit 2
	@echo "⚠️  Cursor display not yet implemented (Unit 2)"

show-manifest:
	@echo "📊 Manifest summary:"
	# TODO: Implement in Unit 2  
	@echo "⚠️  Manifest display not yet implemented (Unit 2)"

stats:
	@echo "📈 Data statistics for $(SOURCE)/$(STREAM):"
	# TODO: Implement in Unit 6
	@echo "⚠️  Stats not yet implemented (Unit 6)"

# Utilities
clean:
	@echo "🧹 Cleaning temporary files..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type f -name ".DS_Store" -delete
	@echo "✅ Clean complete"

# Development helpers (will be used in later units)
dev-setup: bootstrap
	@echo "🛠️  Development setup complete"

test:
	@echo "🧪 Running tests..."
	# TODO: Implement in Unit 7
	@echo "⚠️  Tests not yet implemented (Unit 7)"
