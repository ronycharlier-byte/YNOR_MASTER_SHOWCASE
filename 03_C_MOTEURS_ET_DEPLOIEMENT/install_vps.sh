#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${APP_DIR:-/opt/FRACTAL_CHIASTE_UNIVERSEL}"
REPO_URL="${REPO_URL:-}"
BRANCH="${BRANCH:-main}"

if [[ "${EUID}" -eq 0 ]]; then
  SUDO=""
else
  SUDO="sudo"
fi

prompt_secret() {
  local var_name="$1"
  local prompt_text="$2"
  local value="${!var_name:-}"

  if [[ -z "${value}" ]]; then
    read -r -s -p "${prompt_text}: " value
    echo
  fi

  printf -v "${var_name}" '%s' "${value}"
}

prompt_value() {
  local var_name="$1"
  local prompt_text="$2"
  local value="${!var_name:-}"

  if [[ -z "${value}" ]]; then
    read -r -p "${prompt_text}: " value
  fi

  printf -v "${var_name}" '%s' "${value}"
}

prompt_yes_no() {
  local var_name="$1"
  local prompt_text="$2"
  local default_value="${3:-false}"
  local value="${!var_name:-}"

  if [[ -z "${value}" ]]; then
    read -r -p "${prompt_text} [y/N]: " value
    value="${value:-${default_value}}"
  fi

  case "${value}" in
    y|Y|yes|YES|true|TRUE|1)
      printf -v "${var_name}" '%s' "true"
      ;;
    *)
      printf -v "${var_name}" '%s' "false"
      ;;
  esac
}

echo "[1/8] Installing system packages"
$SUDO apt update
$SUDO apt install -y git python3 python3-venv python3-pip

echo "[2/8] Preparing app directory"
$SUDO mkdir -p "${APP_DIR}"
$SUDO chown -R "${USER}:${USER}" "${APP_DIR}"

if [[ -n "${REPO_URL}" ]]; then
  if [[ ! -d "${APP_DIR}/.git" ]]; then
    echo "[3/8] Cloning repository"
    git clone --branch "${BRANCH}" "${REPO_URL}" "${APP_DIR}"
  else
    echo "[3/8] Repository already exists, pulling latest changes"
    cd "${APP_DIR}"
    git pull --ff-only
  fi
else
  if [[ ! -d "${APP_DIR}/.git" ]]; then
    prompt_value REPO_URL "Repository URL"
    if [[ -z "${REPO_URL}" ]]; then
      echo "Repository URL is required."
      exit 1
    fi
    echo "[3/8] Cloning repository"
    git clone --branch "${BRANCH}" "${REPO_URL}" "${APP_DIR}"
  fi
fi

cd "${APP_DIR}"

echo "[4/8] Creating virtual environment"
python3 -m venv .venv
source .venv/bin/activate

echo "[5/8] Installing Python dependencies"
pip install --upgrade pip setuptools wheel
pip install --no-cache-dir -r 03_C_MOTEURS_ET_DEPLOIEMENT/requirements-bitget.txt

echo "[6/8] Ensuring environment file exists"
if [[ ! -f .env ]]; then
  cp 03_C_MOTEURS_ET_DEPLOIEMENT/.env.example .env
fi

prompt_secret BITGET_API_KEY "Bitget API Key"
prompt_secret BITGET_SECRET "Bitget Secret"
prompt_secret BITGET_PASSPHRASE "Bitget Passphrase"
prompt_yes_no LIVE_TRADING "Enable live trading now" "false"

cat > .env <<EOF
BITGET_API_KEY=${BITGET_API_KEY}
BITGET_SECRET=${BITGET_SECRET}
BITGET_PASSPHRASE=${BITGET_PASSPHRASE}
LIVE_TRADING=${LIVE_TRADING}
EOF

chmod 600 .env
echo "Wrote .env with Bitget credentials."

echo "[7/8] Installing systemd services"
$SUDO cp 03_C_MOTEURS_ET_DEPLOIEMENT/systemd/bitget-bot.service /etc/systemd/system/
$SUDO cp 03_C_MOTEURS_ET_DEPLOIEMENT/systemd/bitget-dashboard.service /etc/systemd/system/
$SUDO systemctl daemon-reload
$SUDO systemctl enable bitget-bot.service
$SUDO systemctl enable bitget-dashboard.service

echo "[8/8] Starting services"
$SUDO systemctl restart bitget-bot.service
$SUDO systemctl restart bitget-dashboard.service

echo
echo "Done."
echo "Edit ${APP_DIR}/.env to add your Bitget keys, then use:"
echo "  sudo systemctl status bitget-bot.service"
echo "  sudo systemctl status bitget-dashboard.service"
echo "  journalctl -u bitget-bot.service -f"
echo "  journalctl -u bitget-dashboard.service -f"
