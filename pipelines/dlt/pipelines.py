"""
Data Platform Light - DLT Pipeline Entrypoints

This module contains the main pipeline functions for extracting data from:
- Jira (issues, changelogs, projects, sprints, users, worklogs)
- Bitbucket (pull requests, activities, commits, repositories, branches)
- Jenkins (jobs, builds, queue snapshots)

All pipelines write to Bronze layer as JSONL files with manifest/cursor tracking.
"""

import os
import sys
import yaml
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional

import dlt
from dlt.common.typing import TDataItem
from dlt.extract.source import DltSource


def load_config() -> Dict[str, Any]:
    """Load configuration from YAML files."""
    config_dir = Path(__file__).parent.parent.parent / "config"
    
    with open(config_dir / "sources.yaml", "r") as f:
        sources_config = yaml.safe_load(f)
    
    with open(config_dir / "time.yaml", "r") as f:
        time_config = yaml.safe_load(f)
    
    return {
        "sources": sources_config,
        "time": time_config
    }


def jira_pipeline() -> DltSource:
    """
    Jira data extraction pipeline.
    
    Extracts:
    - issues (with configurable expands)
    - issue_changelogs
    - projects
    - boards and sprints
    - users (referenced)
    - worklogs
    - attachments (metadata only)
    """
    # TODO: Implement in Unit 3
    raise NotImplementedError("Jira pipeline will be implemented in Unit 3")


def bitbucket_pipeline() -> DltSource:
    """
    Bitbucket data extraction pipeline.
    
    Extracts:
    - pull_requests (all states)
    - pr_activities
    - commits
    - repositories
    - refs/branches
    """
    # TODO: Implement in Unit 4
    raise NotImplementedError("Bitbucket pipeline will be implemented in Unit 4")


def jenkins_pipeline() -> DltSource:
    """
    Jenkins data extraction pipeline.
    
    Extracts:
    - jobs
    - builds (with parameters, actions, changesets)
    - queue (optional)
    """
    # TODO: Implement in Unit 5
    raise NotImplementedError("Jenkins pipeline will be implemented in Unit 5")


def backfill_pipeline(days: int = 120) -> None:
    """
    Backfill pipeline - resets cursors and re-extracts historical data.
    
    Args:
        days: Number of days to backfill
    """
    # TODO: Implement cursor reset logic in Unit 2
    raise NotImplementedError("Backfill pipeline will be implemented in Unit 2")


if __name__ == "__main__":
    # CLI entrypoint for individual pipeline testing
    if len(sys.argv) < 2:
        print("Usage: python pipelines.py [jira|bitbucket|jenkins|backfill] [args...]")
        sys.exit(1)
    
    pipeline_name = sys.argv[1]
    
    if pipeline_name == "jira":
        source = jira_pipeline()
        print(f"Jira pipeline created: {source}")
    elif pipeline_name == "bitbucket":
        source = bitbucket_pipeline()
        print(f"Bitbucket pipeline created: {source}")
    elif pipeline_name == "jenkins":
        source = jenkins_pipeline()
        print(f"Jenkins pipeline created: {source}")
    elif pipeline_name == "backfill":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 120
        backfill_pipeline(days)
        print(f"Backfill completed for {days} days")
    else:
        print(f"Unknown pipeline: {pipeline_name}")
        sys.exit(1)
