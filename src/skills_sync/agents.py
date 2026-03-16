"""Registro de agentes de IA e seus diretórios de skills."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class AgentConfig:
    """Configuração de um agente de IA com seus diretórios de skills."""

    name: str
    display_name: str
    global_dir: Path
    project_dir: str  # caminho relativo dentro do projeto


def _home() -> Path:
    return Path.home()


def _xdg_config() -> Path:
    return Path(os.environ.get("XDG_CONFIG_HOME", _home() / ".config"))


# Mapa completo de agentes suportados pelo npx skills (v1.4.5+)
AGENTS: dict[str, AgentConfig] = {
    "claude-code": AgentConfig(
        name="claude-code",
        display_name="Claude Code",
        global_dir=Path(os.environ.get("CLAUDE_HOME", _home() / ".claude")) / "skills",
        project_dir=".claude/skills",
    ),
    "codex": AgentConfig(
        name="codex",
        display_name="Codex",
        global_dir=Path(os.environ.get("CODEX_HOME", _home() / ".codex")) / "skills",
        project_dir=".codex/skills",
    ),
    "gemini-cli": AgentConfig(
        name="gemini-cli",
        display_name="Gemini CLI",
        global_dir=_home() / ".gemini" / "skills",
        project_dir=".gemini/skills",
    ),
    "github-copilot": AgentConfig(
        name="github-copilot",
        display_name="GitHub Copilot",
        global_dir=_home() / ".copilot" / "skills",
        project_dir=".copilot/skills",
    ),
    "cursor": AgentConfig(
        name="cursor",
        display_name="Cursor",
        global_dir=_home() / ".cursor" / "skills",
        project_dir=".cursor/skills",
    ),
    "opencode": AgentConfig(
        name="opencode",
        display_name="OpenCode",
        global_dir=_xdg_config() / "opencode" / "skills",
        project_dir=".opencode/skills",
    ),
    "windsurf": AgentConfig(
        name="windsurf",
        display_name="Windsurf",
        global_dir=_home() / ".codeium" / "windsurf" / "skills",
        project_dir=".windsurf/skills",
    ),
    "roo-code": AgentConfig(
        name="roo-code",
        display_name="Roo Code",
        global_dir=_home() / ".roo" / "skills",
        project_dir=".roo/skills",
    ),
    "continue": AgentConfig(
        name="continue",
        display_name="Continue",
        global_dir=_home() / ".continue" / "skills",
        project_dir=".continue/skills",
    ),
    "generic": AgentConfig(
        name="generic",
        display_name="Genérico (.agents)",
        global_dir=_home() / ".agents" / "skills",
        project_dir=".agents/skills",
    ),
    # Agentes adicionais
    "aider": AgentConfig(
        name="aider",
        display_name="Aider",
        global_dir=_home() / ".aider" / "skills",
        project_dir=".aider/skills",
    ),
    "cline": AgentConfig(
        name="cline",
        display_name="Cline",
        global_dir=_home() / ".cline" / "skills",
        project_dir=".cline/skills",
    ),
    "amp": AgentConfig(
        name="amp",
        display_name="Amp",
        global_dir=_home() / ".amp" / "skills",
        project_dir=".amp/skills",
    ),
    "void": AgentConfig(
        name="void",
        display_name="Void",
        global_dir=_home() / ".void" / "skills",
        project_dir=".void/skills",
    ),
    "zed": AgentConfig(
        name="zed",
        display_name="Zed",
        global_dir=_home() / ".zed" / "skills",
        project_dir=".zed/skills",
    ),
    "trae": AgentConfig(
        name="trae",
        display_name="Trae",
        global_dir=_home() / ".trae" / "skills",
        project_dir=".trae/skills",
    ),
    "augment": AgentConfig(
        name="augment",
        display_name="Augment",
        global_dir=_home() / ".augment" / "skills",
        project_dir=".augment/skills",
    ),
    "pear-ai": AgentConfig(
        name="pear-ai",
        display_name="PearAI",
        global_dir=_home() / ".pear-ai" / "skills",
        project_dir=".pear-ai/skills",
    ),
    "kilo-code": AgentConfig(
        name="kilo-code",
        display_name="Kilo Code",
        global_dir=_home() / ".kilo-code" / "skills",
        project_dir=".kilo-code/skills",
    ),
    "aide": AgentConfig(
        name="aide",
        display_name="Aide",
        global_dir=_home() / ".aide" / "skills",
        project_dir=".aide/skills",
    ),
    "bb": AgentConfig(
        name="bb",
        display_name="BB",
        global_dir=_home() / ".bb" / "skills",
        project_dir=".bb/skills",
    ),
    "goose": AgentConfig(
        name="goose",
        display_name="Goose",
        global_dir=_home() / ".goose" / "skills",
        project_dir=".goose/skills",
    ),
    "cloi": AgentConfig(
        name="cloi",
        display_name="Cloi",
        global_dir=_home() / ".cloi" / "skills",
        project_dir=".cloi/skills",
    ),
    "hal": AgentConfig(
        name="hal",
        display_name="HAL",
        global_dir=_home() / ".hal" / "skills",
        project_dir=".hal/skills",
    ),
    "junie": AgentConfig(
        name="junie",
        display_name="Junie",
        global_dir=_home() / ".junie" / "skills",
        project_dir=".junie/skills",
    ),
    "devin": AgentConfig(
        name="devin",
        display_name="Devin",
        global_dir=_home() / ".devin" / "skills",
        project_dir=".devin/skills",
    ),
    "replit": AgentConfig(
        name="replit",
        display_name="Replit Agent",
        global_dir=_home() / ".replit" / "skills",
        project_dir=".replit/skills",
    ),
    "bolt": AgentConfig(
        name="bolt",
        display_name="Bolt",
        global_dir=_home() / ".bolt" / "skills",
        project_dir=".bolt/skills",
    ),
    "tabnine": AgentConfig(
        name="tabnine",
        display_name="Tabnine",
        global_dir=_home() / ".tabnine" / "skills",
        project_dir=".tabnine/skills",
    ),
    "codeium": AgentConfig(
        name="codeium",
        display_name="Codeium",
        global_dir=_home() / ".codeium" / "skills",
        project_dir=".codeium/skills",
    ),
    "sourcegraph-cody": AgentConfig(
        name="sourcegraph-cody",
        display_name="Sourcegraph Cody",
        global_dir=_home() / ".cody" / "skills",
        project_dir=".cody/skills",
    ),
    "double": AgentConfig(
        name="double",
        display_name="Double",
        global_dir=_home() / ".double" / "skills",
        project_dir=".double/skills",
    ),
    "composio": AgentConfig(
        name="composio",
        display_name="Composio",
        global_dir=_home() / ".composio" / "skills",
        project_dir=".composio/skills",
    ),
    "sweep": AgentConfig(
        name="sweep",
        display_name="Sweep",
        global_dir=_home() / ".sweep" / "skills",
        project_dir=".sweep/skills",
    ),
    "mentat": AgentConfig(
        name="mentat",
        display_name="Mentat",
        global_dir=_home() / ".mentat" / "skills",
        project_dir=".mentat/skills",
    ),
    "gpt-engineer": AgentConfig(
        name="gpt-engineer",
        display_name="GPT Engineer",
        global_dir=_home() / ".gpt-engineer" / "skills",
        project_dir=".gpt-engineer/skills",
    ),
    "smol-developer": AgentConfig(
        name="smol-developer",
        display_name="Smol Developer",
        global_dir=_home() / ".smol-developer" / "skills",
        project_dir=".smol-developer/skills",
    ),
    "auto-gpt": AgentConfig(
        name="auto-gpt",
        display_name="AutoGPT",
        global_dir=_home() / ".auto-gpt" / "skills",
        project_dir=".auto-gpt/skills",
    ),
    "open-interpreter": AgentConfig(
        name="open-interpreter",
        display_name="Open Interpreter",
        global_dir=_home() / ".open-interpreter" / "skills",
        project_dir=".open-interpreter/skills",
    ),
    "devon": AgentConfig(
        name="devon",
        display_name="Devon",
        global_dir=_home() / ".devon" / "skills",
        project_dir=".devon/skills",
    ),
}


def detect_installed(agents: dict[str, AgentConfig] | None = None) -> list[AgentConfig]:
    """Detecta quais agentes possuem diretório de skills na máquina."""
    agents = agents or AGENTS
    installed: list[AgentConfig] = []
    for agent in agents.values():
        resolved = agent.global_dir.resolve()
        if resolved.is_dir():
            installed.append(agent)
    return installed
