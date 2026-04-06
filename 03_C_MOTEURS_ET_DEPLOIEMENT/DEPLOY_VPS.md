# VPS Deployment Guide

This project can run on a small Ubuntu VPS with a fixed public IPv4.

## 1. System setup

You can run the automation script instead of typing everything manually:

```bash
cd /opt/FRACTAL_CHIASTE_UNIVERSEL
bash 03_C_MOTEURS_ET_DEPLOIEMENT/install_vps.sh
```

The script will prompt for:

- repository URL
- Bitget API key
- Bitget secret
- Bitget passphrase
- whether to enable live trading

If you prefer the manual steps, keep reading.

```bash
sudo apt update
sudo apt install -y git python3 python3-venv python3-pip
```

## 2. Clone the repository

```bash
git clone <your-repo-url>
cd FRACTAL_CHIASTE_UNIVERSEL
```

## 3. Create the virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 4. Configure environment variables

```bash
cp 03_C_MOTEURS_ET_DEPLOIEMENT/.env.example .env
nano .env
```

Fill in:

- `BITGET_API_KEY`
- `BITGET_SECRET`
- `BITGET_PASSPHRASE`
- `LIVE_TRADING=false` for testing first

The VPS installer now uses `03_C_MOTEURS_ET_DEPLOIEMENT/requirements-bitget.txt`, which keeps the Python install minimal.

## 5. Whitelist the VPS IP in Bitget

Use the VPS public IPv4 only, for example `123.123.123.123`.

Do not paste CIDR ranges such as `74.220.48.0/24`.

## 6. Test the dashboard

```bash
streamlit run 03_C_MOTEURS_ET_DEPLOIEMENT/bitget_dashboard.py --server.address 0.0.0.0 --server.port 8501
```

## 7. Run the bot

```bash
python 03_C_MOTEURS_ET_DEPLOIEMENT/bitget_market_bot.py
```

## 8. Switch to live trading

After the dry run is validated, set:

```bash
sed -i 's/LIVE_TRADING=false/LIVE_TRADING=true/' .env
```

Then restart the bot service:

```bash
sudo systemctl restart bitget-bot.service
```

## 9. Suggested process model

- Use `systemd` for the bot process.
- Run the dashboard separately.
- Keep the bot and UI in the same repository but not in the same process in production.
