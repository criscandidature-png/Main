#!/bin/bash
# Installa tutto il necessario per l'editor video su Mac.
set -e
cd "$(dirname "$0")"
if ! command -v brew >/dev/null; then
  echo "Installo Homebrew..."
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  eval "$(/opt/homebrew/bin/brew shellenv 2>/dev/null || /usr/local/bin/brew shellenv)"
fi
brew install ffmpeg python@3.12
brew install --cask font-poppins || true
python3.12 -m venv .venv
.venv/bin/pip install -q --upgrade pip
.venv/bin/pip install -q -r requirements.txt
mkdir -p riferimenti/lavoro riferimenti/personale
echo ""
echo "Fatto. Per usarlo:"
echo "  cd $(pwd) && source .venv/bin/activate"
echo "  export ANTHROPIC_API_KEY=la_tua_chiave"
echo "  python editor.py tutto /percorso/video.mp4 --profilo lavoro"
