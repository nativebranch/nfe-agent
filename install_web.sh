#!/bin/bash
cd /home/csg/Documentos/moneyloop/ata-agent
.venv/bin/pip install -q fastapi uvicorn python-multipart
echo INSTALL_DONE
.venv/bin/python -c "from nfe_agent.webapp import app; print('webapp import OK')"
