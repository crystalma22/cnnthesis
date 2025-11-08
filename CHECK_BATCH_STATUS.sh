#!/bin/bash
# Quick script to check your batch job status on Laguna

echo "========================================"
echo "CHECKING BATCH JOB STATUS"
echo "========================================"
echo ""

echo "1. Checking job queue..."
ssh laguna "squeue -u \$USER"
echo ""

echo "2. Recent log files (last 10)..."
ssh laguna "ls -lht ~/cnnthesis/logs/*.out 2>/dev/null | head -10"
echo ""

echo "3. Checking for error files..."
ssh laguna "ls -lht ~/cnnthesis/logs/*.err 2>/dev/null | head -5"
echo ""

echo "4. Last 20 lines of most recent log..."
LATEST_LOG=$(ssh laguna "ls -t ~/cnnthesis/logs/*.out 2>/dev/null | head -1")
if [ ! -z "$LATEST_LOG" ]; then
    echo "File: $LATEST_LOG"
    ssh laguna "tail -20 $LATEST_LOG"
else
    echo "No log files found yet"
fi
echo ""

echo "5. Checking for output files..."
ssh laguna "ls -lh ~/cnnthesis/CACHE_DIR/fomc/*.csv 2>/dev/null | tail -10"
echo ""

echo "========================================"
echo "STATUS CHECK COMPLETE"
echo "========================================"




