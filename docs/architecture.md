# Project Architecture

## Project
AI-Powered Linux Infrastructure Monitoring & Auto-Remediation System

## Architecture Flow

1. Linux System
   - CPU monitoring
   - Memory monitoring
   - Disk monitoring
   - Process monitoring

2. Data Collection
   - Bash health check
   - Python and psutil
   - Prometheus exporters

3. Monitoring
   - Prometheus
   - Grafana dashboards
   - Alert rules

4. AI/ML Analysis
   - Pandas data processing
   - Isolation Forest anomaly detection
   - Incident classification
   - Decision reporting

5. Automation
   - Ansible playbooks
   - Controlled remediation tests
   - Recovery verification

6. Reporting
   - CSV reports
   - JSON health reports
   - Recovery verification logs

## Current Project Limitations

- Machine learning analysis currently runs as a separate pipeline.
- The Prometheus exporter reads the latest saved ML result.
- Ansible tests demonstrate controlled actions, not actual CPU recovery.
- Automatic Alertmanager-to-Flask notification forwarding still requires configuration and testing.
