#!/usr/bin/env bash
set -e

# ---- Colors ----
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m' # No Color

ok()   { echo -e "  ${GREEN}✔${NC} $1"; }
info() { echo -e "  ${BLUE}→${NC} $1"; }
warn() { echo -e "  ${YELLOW}!${NC} $1"; }
fail() { echo -e "  ${RED}✘${NC} $1"; exit 1; }

echo ""
echo -e "${BOLD}CTC Workshop Setup${NC}"
echo "─────────────────────────────────"
echo ""

# ---- cd to script directory ----
cd "$(dirname "$0")"

# ---- 1. Check / install uv ----
echo -e "${BOLD}1. Checking for uv...${NC}"
if command -v uv &>/dev/null; then
    ok "uv is installed ($(uv --version))"
else
    info "uv not found — installing..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # Make uv available in this session
    export PATH="$HOME/.local/bin:$PATH"
    if command -v uv &>/dev/null; then
        ok "uv installed successfully ($(uv --version))"
    else
        fail "uv installation failed. Try restarting your terminal and running this script again."
    fi
fi
echo ""

# ---- 2. Install Python ----
PYTHON_VERSION=$(cat .python-version)
echo -e "${BOLD}2. Installing Python ${PYTHON_VERSION}...${NC}"
uv python install "$PYTHON_VERSION" 2>/dev/null
ok "Python ${PYTHON_VERSION} is ready"
echo ""

# ---- 3. Install dependencies ----
echo -e "${BOLD}3. Installing dependencies...${NC}"
uv sync
ok "Project dependencies installed"
uv add openai
ok "openai package installed"
echo ""

# ---- 4. Environment file ----
echo -e "${BOLD}4. Checking .env file...${NC}"
if [ -f .env ]; then
    ok ".env file already exists"
else
    cp .env.example .env
    ok "Created .env from .env.example"
    warn "You still need to add your API key to .env"
fi
echo ""

# ---- Done ----
echo "─────────────────────────────────"
echo -e "${GREEN}${BOLD}Setup complete!${NC}"
echo ""
echo -e "${BOLD}Next steps:${NC}"
echo ""
echo "  1. Activate the virtual environment:"
echo -e "     ${YELLOW}source .venv/bin/activate${NC}"
echo ""
echo "  2. Set your Anthropic API key in .env:"
echo -e "     ${YELLOW}echo 'ANTHROPIC_API_KEY=sk-ant-...' > .env${NC}"
echo ""
echo "  3. Run the first exercise:"
echo -e "     ${YELLOW}cd workshops/01_file_organizer${NC}"
echo ""
