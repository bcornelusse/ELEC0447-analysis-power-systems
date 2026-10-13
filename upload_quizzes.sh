#!/usr/bin/env bash
# =============================================================================
# ELEC0447: Upload Interactive Quizzes to ULiège Web Server
# =============================================================================
# This script stages and uploads the interactive course quizzes to:
#   gaston.montefiore.ulg.ac.be:WWW/ELEC0447/
# 
# Once uploaded, quizzes are immediately accessible under:
#   https://people.montefiore.uliege.be/<username>/ELEC0447/
# =============================================================================

set -e

# Repository directory
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

TL_SRC="$REPO_DIR/Lectures/TransmissionLine/quiz_transmission_lines.html"
PF_SRC="$REPO_DIR/Lectures/IntroPowerFlow/quiz_power_flow.html"
TR_SRC="$REPO_DIR/Lectures/TransfomerAndPF/quiz_transformers.html"

# Verify that all quiz source files exist
for f in "$TL_SRC" "$PF_SRC" "$TR_SRC"; do
    if [ ! -f "$f" ]; then
        echo "❌ Error: Required file not found: $f" >&2
        exit 1
    fi
done

# Server details
REMOTE_HOST="gaston.montefiore.ulg.ac.be"
REMOTE_DIR="WWW/ELEC0447"

echo "============================================================================="
echo " ELEC0447: Deploy Quizzes to Montefiore Web Server"
echo " Target: ${REMOTE_HOST}:${REMOTE_DIR}"
echo "============================================================================="
echo ""

# Prompt for username
read -rp "Enter username for ${REMOTE_HOST}: " REMOTE_USER
if [ -z "$REMOTE_USER" ]; then
    echo "❌ Error: Username cannot be empty." >&2
    exit 1
fi

# Prompt for password (masked)
read -rsp "Enter password for ${REMOTE_USER}@${REMOTE_HOST} (leave blank if using SSH key): " REMOTE_PASS
echo ""
echo ""

# Function to run an SSH/SCP command with password or SSH key
run_ssh_cmd() {
    if [ -n "$REMOTE_PASS" ] && command -v expect >/dev/null 2>&1; then
        expect -f - "$REMOTE_PASS" "$@" << 'EOF'
            set timeout 60
            set password [lindex $argv 0]
            set cmd_args [lrange $argv 1 end]
            spawn {*}$cmd_args
            expect {
                -nocase "*yes/no*" {
                    send "yes\r"
                    exp_continue
                }
                -nocase "*password:*" {
                    send "$password\r"
                    exp_continue
                }
                eof
            }
            catch wait result
            set exit_code [lindex $result 3]
            exit $exit_code
EOF
    else
        "$@"
    fi
}

echo "🚀 Uploading to ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR}..."

# Step 1: Ensure target directory exists on server
echo "📁 Ensuring remote directory exists (${REMOTE_DIR})..."
run_ssh_cmd ssh -o StrictHostKeyChecking=accept-new "${REMOTE_USER}@${REMOTE_HOST}" mkdir -p "${REMOTE_DIR}"

# Step 2: Upload quiz files directly into WWW/ELEC0447/
echo "📤 Uploading quiz files..."
run_ssh_cmd scp -o StrictHostKeyChecking=accept-new "$TL_SRC" "$PF_SRC" "$TR_SRC" "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR}/"

# Step 3: Ensure files and directory are readable by the Apache web server
echo "🔓 Setting web permissions (chmod -R a+rX ${REMOTE_DIR})..."
run_ssh_cmd ssh -o StrictHostKeyChecking=accept-new "${REMOTE_USER}@${REMOTE_HOST}" chmod -R a+rX "${REMOTE_DIR}"

echo ""
echo "============================================================================="
echo "✅ Quizzes successfully uploaded!"
echo "============================================================================="
echo "Published quizzes are now accessible at:"
echo "  👉 Transmission Lines: https://people.montefiore.uliege.be/${REMOTE_USER}/ELEC0447/quiz_transmission_lines.html"
echo "  👉 Power Flow:        https://people.montefiore.uliege.be/${REMOTE_USER}/ELEC0447/quiz_power_flow.html"
echo "  👉 Transformers:      https://people.montefiore.uliege.be/${REMOTE_USER}/ELEC0447/quiz_transformers.html"
echo "============================================================================="
