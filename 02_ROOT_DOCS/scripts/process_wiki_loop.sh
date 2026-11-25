#!/bin/bash
# Nexus Brain Wiki — AUTO PROCESSOR v3
set -o pipefail

CHECKPOINT="/sdcard/Nexus_Brain/Nexus_Brain/0_System/CHECKPOINT.md"
AUTO_GUIDE="/sdcard/Nexus_Brain/AUTO_GUIDE.md"
ERROR_LOG="/sdcard/Nexus_Brain/Nexus_Brain/0_System/ERROR_LOG.md"
INDEX="/sdcard/Nexus_Brain/Nexus_Brain/wiki/index.md"
LOG="/sdcard/Nexus_Brain/auto_loop.log"
BRAIN_DIR="/sdcard/Nexus_Brain/brain"
LOCKFILE="/tmp/nexus_wiki_loop.lock"

MAX_BATCHES=500
STALL_LIMIT=3
RETRY_LIMIT=3
MIN_DISK_MB=500

# Prevent double runs
if [ -f "$LOCKFILE" ] && kill -0 $(cat "$LOCKFILE") 2>/dev/null; then
    echo "✗ Loop already running (PID $(cat $LOCKFILE))"
    exit 1
fi
echo $$ > "$LOCKFILE"

echo "=== AUTO PROCESSOR v3 ===" | tee "$LOG"
date | tee -a "$LOG"
echo "Limits: max=$MAX_BATCHES stall=$STALL_LIMIT retry=$RETRY_LIMIT disk_min=${MIN_DISK_MB}MB" | tee -a "$LOG"

BATCH=1
STALL_COUNT=0

while [ $BATCH -le $MAX_BATCHES ]; do
    echo "" | tee -a "$LOG"
    echo "========== BATCH $BATCH ==========" | tee -a "$LOG"
    date | tee -a "$LOG"

    # === GAP 1: NO FILES LEFT ===
    FILE_COUNT=$(ls "$BRAIN_DIR"/*.txt 2>/dev/null | wc -l)
    if [ "$FILE_COUNT" -eq 0 ]; then
        grep -qi "ALL DONE" "$CHECKPOINT" 2>/dev/null && \
            echo "✓ DONE — no files, CHECKPOINT confirms" | tee -a "$LOG" || \
            echo "⚠ No files but CHECKPOINT not DONE" | tee -a "$LOG"
        break
    fi

    # === GAP 2: CHECKPOINT MISSING ===
    [ ! -f "$CHECKPOINT" ] && echo "✗ CHECKPOINT.md missing!" | tee -a "$LOG" && date >> "$ERROR_LOG" && echo "FATAL: CHECKPOINT.md not found" >> "$ERROR_LOG" && break

    # === GAP 10: DISK SPACE ===
    AVAIL_MB=$(df -m /sdcard 2>/dev/null | awk 'NR==2{print $4}')
    [ -n "$AVAIL_MB" ] && [ "$AVAIL_MB" -lt $MIN_DISK_MB ] && \
        echo "✗ Low disk: ${AVAIL_MB}MB < ${MIN_DISK_MB}MB" | tee -a "$LOG" && \
        date >> "$ERROR_LOG" && echo "DISK_LOW: ${AVAIL_MB}MB" >> "$ERROR_LOG" && break

    # === GAP 11: INDEX CREATION ===
    [ ! -f "$INDEX" ] && echo "# Wiki Index — AUTO" > "$INDEX"

    # Snapshot CHECKPOINT
    CP_HASH=$(md5sum "$CHECKPOINT" 2>/dev/null | cut -d' ' -f1)

    RETRY=0
    SUCCESS=false
    while [ $RETRY -lt $RETRY_LIMIT ] && [ "$SUCCESS" = false ]; do
        [ $RETRY -gt 0 ] && echo "Retry $((RETRY+1))/$RETRY_LIMIT ..." | tee -a "$LOG" && sleep $((RETRY * 30))

        # === GAP 3: INDEPENDENT SESSIONS (no --continue) ===
        # Cheap: reads AUTO_GUIDE (568 words) + CHECKPOINT + source batch
        # Simple: no context overflow, no session management
        opencode run --model opencode/big-pickle --dangerously-skip-permissions \
            "read $AUTO_GUIDE and $CHECKPOINT, then read the source file (dd command in CHECKPOINT), extract wiki pages, update index.md, NEXUS_LLM_WIKI.md stats, keywords/, and CHECKPOINT.md. Do NOT read NEXUS_LLM_WIKI.md or index.md or keywords/—AUTO_GUIDE has all rules. Just process the batch and stop."

        EXIT_CODE=$?

        # === GAP 4: CHECK IF WORK WAS DONE ===
        if [ $EXIT_CODE -eq 0 ]; then
            NEW_HASH=$(md5sum "$CHECKPOINT" 2>/dev/null | cut -d' ' -f1)
            [ "$CP_HASH" != "$NEW_HASH" ] && SUCCESS=true && echo "✓ Batch $BATCH completed" | tee -a "$LOG" || \
                echo "⚠ Model ran but CHECKPOINT unchanged" | tee -a "$LOG" && RETRY=$((RETRY + 1))
        else
            [ $EXIT_CODE -eq 124 ] && echo "⚠ Model timeout" | tee -a "$LOG" || echo "⚠ Model crashed (exit $EXIT_CODE)" | tee -a "$LOG"
            RETRY=$((RETRY + 1))
        fi
    done

    # === GAP 5: EXHAUSTED RETRIES ===
    if [ "$SUCCESS" = false ]; then
        date >> "$ERROR_LOG"
        echo "RETRY_EXHAUSTED: batch $BATCH files=$FILE_COUNT" >> "$ERROR_LOG"
        STALL_COUNT=$((STALL_COUNT + 1))
    else
        STALL_COUNT=0
    fi

    # === GAP 6: STALL DETECTION ===
    [ $STALL_COUNT -ge $STALL_LIMIT ] && echo "✗ Stalled $STALL_LIMIT times — aborting" | tee -a "$LOG" && break

    # === GAP 7: ALL DONE ===
    grep -qi "ALL DONE" "$CHECKPOINT" 2>/dev/null && echo "✓ CHECKPOINT says DONE!" | tee -a "$LOG" && break

    # === GAP 13: PROGRESS REPORT (every 5 batches) ===
    if [ $((BATCH % 5)) -eq 0 ] && [ "$SUCCESS" = true ]; then
        PAGES=$(grep -i "اجمالي\|إجمالي\|total" "$CHECKPOINT" 2>/dev/null | head -1)
        PCT=$(grep -oP '\d+\.?\d*%' "$CHECKPOINT" 2>/dev/null | head -1)
        echo "" > "/sdcard/Nexus_Brain/PROGRESS_REPORT.md"
        echo "# Progress Report — Batch $BATCH" >> "/sdcard/Nexus_Brain/PROGRESS_REPORT.md"
        date >> "/sdcard/Nexus_Brain/PROGRESS_REPORT.md"
        echo "" >> "/sdcard/Nexus_Brain/PROGRESS_REPORT.md"
        echo "**$PAGES**" >> "/sdcard/Nexus_Brain/PROGRESS_REPORT.md"
        echo "**File progress:** $PCT" >> "/sdcard/Nexus_Brain/PROGRESS_REPORT.md"
        echo "**Last batch:** $BATCH" >> "/sdcard/Nexus_Brain/PROGRESS_REPORT.md"
        echo "---" >> "/sdcard/Nexus_Brain/PROGRESS_REPORT.md"
        echo "Status: running in background (process_wiki_loop.sh)" >> "/sdcard/Nexus_Brain/PROGRESS_REPORT.md"
        echo "Log: /tmp/wiki_loop.log" >> "/sdcard/Nexus_Brain/PROGRESS_REPORT.md"
        echo "*Auto-generated every 5 batches*" >> "/sdcard/Nexus_Brain/PROGRESS_REPORT.md"
    fi

    BATCH=$((BATCH + 1))
    sleep 5
done

rm -f "$LOCKFILE"
echo "" | tee -a "$LOG"
echo "=== PROCESSOR FINISHED ===" | tee -a "$LOG"
date | tee -a "$LOG"
