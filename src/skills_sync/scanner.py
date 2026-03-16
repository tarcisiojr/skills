"""Descoberta e varredura de skills em diretórios de agentes."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path

from skills_sync.agents import AgentConfig


@dataclass(slots=True)
class SkillInfo:
    """Informações de uma skill descoberta."""

    name: str
    description: str
    source_path: Path
    source_agents: list[str] = field(default_factory=list)
    files: list[Path] = field(default_factory=list)
    content_hash: str = ""


def _parse_frontmatter(content: str) -> dict[str, str]:
    """Extrai campos do frontmatter YAML usando regex (sem dependência PyYAML)."""
    match = re.search(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}

    block = match.group(1)
    result: dict[str, str] = {}

    # Extrai campos simples e multiline (com >)
    for key in ("name", "description"):
        # Tenta formato multiline primeiro: key: >\n  linhas...
        multiline = re.search(rf"^{key}:\s*>\s*\n((?:\s+.*\n?)+)", block, re.MULTILINE)
        if multiline:
            lines = multiline.group(1).strip().splitlines()
            result[key] = " ".join(line.strip() for line in lines)
            continue

        # Formato simples: key: valor
        simple = re.search(rf"^{key}:\s*(.+)$", block, re.MULTILINE)
        if simple:
            result[key] = simple.group(1).strip().strip("\"'")

    return result


def _compute_hash(skill_dir: Path) -> tuple[str, list[Path]]:
    """Calcula SHA-256 do conteúdo de todos os arquivos da skill, ordenados por path."""
    files: list[Path] = sorted(f for f in skill_dir.rglob("*") if f.is_file())
    hasher = hashlib.sha256()
    for f in files:
        # Inclui o path relativo no hash para detectar renomeações
        rel = f.relative_to(skill_dir)
        hasher.update(str(rel).encode("utf-8"))
        hasher.update(f.read_bytes())
    return hasher.hexdigest(), files


def scan_directory(path: Path) -> list[SkillInfo]:
    """Escaneia um diretório de skills, retornando lista de SkillInfo."""
    skills: list[SkillInfo] = []

    if not path.is_dir():
        return skills

    resolved = path.resolve()

    for entry in sorted(resolved.iterdir()):
        if not entry.is_dir():
            continue

        skill_md = entry / "SKILL.md"
        if not skill_md.exists():
            continue

        content = skill_md.read_text(encoding="utf-8")
        meta = _parse_frontmatter(content)
        name = meta.get("name", entry.name)
        description = meta.get("description", "")

        content_hash, files = _compute_hash(entry)

        skills.append(
            SkillInfo(
                name=name,
                description=description,
                source_path=entry,
                files=files,
                content_hash=content_hash,
            )
        )

    return skills


def scan_agents(agents: list[AgentConfig]) -> list[SkillInfo]:
    """Escaneia diretórios globais de cada agente, deduplicando por hash."""
    # Mapa: hash -> SkillInfo (para deduplicação)
    seen: dict[str, SkillInfo] = {}

    for agent in agents:
        resolved = agent.global_dir.resolve()
        for skill in scan_directory(resolved):
            if skill.content_hash in seen:
                # Mesma skill, adiciona agente como fonte
                existing = seen[skill.content_hash]
                if agent.display_name not in existing.source_agents:
                    existing.source_agents.append(agent.display_name)
            else:
                skill.source_agents = [agent.display_name]
                seen[skill.content_hash] = skill

    return list(seen.values())


def scan_projects(base_dir: Path, agents: list[AgentConfig]) -> list[SkillInfo]:
    """Busca skills em diretórios de projeto (nível de projeto, não global)."""
    seen: dict[str, SkillInfo] = {}
    project_dirs = set()

    if not base_dir.is_dir():
        return []

    # Coleta diretórios de projeto únicos
    for agent in agents:
        for skills_dir in base_dir.rglob(agent.project_dir):
            if skills_dir.is_dir():
                project_dirs.add((skills_dir.resolve(), agent.display_name))

    for skills_path, agent_name in sorted(project_dirs):
        for skill in scan_directory(skills_path):
            if skill.content_hash in seen:
                existing = seen[skill.content_hash]
                source = f"{agent_name} (projeto)"
                if source not in existing.source_agents:
                    existing.source_agents.append(source)
            else:
                skill.source_agents = [f"{agent_name} (projeto)"]
                seen[skill.content_hash] = skill

    return list(seen.values())
