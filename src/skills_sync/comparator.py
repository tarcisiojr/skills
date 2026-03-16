"""Comparação de skills entre fontes e repositório."""

from __future__ import annotations

from dataclasses import dataclass, field

from skills_sync.scanner import SkillInfo


@dataclass(slots=True)
class CompareResult:
    """Resultado da comparação entre skills de fontes e repositório."""

    new: list[SkillInfo] = field(default_factory=list)
    modified: list[tuple[SkillInfo, SkillInfo]] = field(default_factory=list)  # (fonte, repo)
    same: list[SkillInfo] = field(default_factory=list)


def compare(sources: list[SkillInfo], repo: list[SkillInfo]) -> CompareResult:
    """Compara skills das fontes com as do repositório."""
    repo_by_name: dict[str, SkillInfo] = {s.name: s for s in repo}
    result = CompareResult()

    for source in sources:
        repo_skill = repo_by_name.get(source.name)
        if repo_skill is None:
            result.new.append(source)
        elif source.content_hash != repo_skill.content_hash:
            result.modified.append((source, repo_skill))
        else:
            result.same.append(source)

    return result
