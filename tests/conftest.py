"""Fixtures compartilhadas para os testes."""

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture()
def tmp_skills_dir(tmp_path: Path) -> Path:
    """Cria uma estrutura de skills temporária para testes."""
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()

    # Cria skill de exemplo
    skill_dir = skills_dir / "example-skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text(
        '---\nname: example-skill\ndescription: "Uma skill de exemplo"\n---\n\n# Example Skill\n',
        encoding="utf-8",
    )

    refs_dir = skill_dir / "references"
    refs_dir.mkdir()
    (refs_dir / "ref.md").write_text("# Referência\nConteúdo.", encoding="utf-8")

    return skills_dir


@pytest.fixture()
def tmp_agent_dir(tmp_path: Path) -> Path:
    """Cria uma estrutura de agente com skills temporária."""
    agent_dir = tmp_path / ".test-agent" / "skills"
    agent_dir.mkdir(parents=True)

    # Skill A
    skill_a = agent_dir / "skill-a"
    skill_a.mkdir()
    (skill_a / "SKILL.md").write_text(
        '---\nname: skill-a\ndescription: "Skill A para teste"\n---\n\n# Skill A\n',
        encoding="utf-8",
    )

    # Skill B
    skill_b = agent_dir / "skill-b"
    skill_b.mkdir()
    skill_b_content = (
        "---\nname: skill-b\ndescription: >\n"
        "  Skill B com descrição\n  multiline\n---\n\n# Skill B\n"
    )
    (skill_b / "SKILL.md").write_text(skill_b_content, encoding="utf-8")

    return agent_dir
