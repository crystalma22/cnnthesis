#!/bin/bash
# Monitor the FOMC event-level job

echo "========================================"
echo "FOMC EVENT-LEVEL JOB MONITOR"
echo "========================================"
echo ""

# Get latest job
LATEST_JOB=$(ssh laguna "ls -t ~/cnnthesis/logs/fomc_event_level_*.out 2>/dev/null | head -1")

if [ -z "$LATEST_JOB" ]; then
    echo "No job logs found"
    exit 1
fi

echo "Monitoring: $LATEST_JOB"
echo ""

# Show job status
echo "Job Queue Status:"
ssh laguna "squeue -u \$USER"
echo ""

# Show last 50 lines
echo "Last 50 lines of output:"
echo "----------------------------------------"
ssh laguna "tail -50 $LATEST_JOB"
echo "----------------------------------------"
echo ""

# Check for errors
echo "Checking for errors..."
ERR_FILE="${LATEST_JOB%.out}.err"
if ssh laguna "[ -f $ERR_FILE ] && [ -s $ERR_FILE ]"; then
    echo "⚠️  Errors detected:"
    ssh laguna "tail -20 $ERR_FILE"
else
    echo "✅ No errors in error log"
fi

echo ""
echo "========================================"

