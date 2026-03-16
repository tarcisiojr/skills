"""Sincronização de skills para o repositório central."""

from __future__ import annotations

import shutil
from pathlib import Path

from skills_sync.scanner import SkillInfo


def sync_skill(skill: SkillInfo, repo_skills_dir: Path, *, dry_run: bool = False) -> Path:
    """Copia uma skill da fonte para o repositório.

    Retorna o caminho de destino.
    """
    dest = repo_skills_dir / skill.name

    if dry_run:
        return dest

    # Remove arquivos antigos do destino que não existem mais na fonte
    if dest.exists():
        source_rel_paths = {f.relative_to(skill.source_path) for f in skill.files}
        for existing in list(dest.rglob("*")):
            if existing.is_file():
                rel = existing.relative_to(dest)
                if rel not in source_rel_paths:
                    existing.unlink()

    # Copia a skill inteira preservando estrutura
    shutil.copytree(
        skill.source_path,
        dest,
        dirs_exist_ok=True,
    )

    return dest
