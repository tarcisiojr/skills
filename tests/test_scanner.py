"""Testes para o módulo de scanner."""

from __future__ import annotations

from pathlib import Path

from skills_sync.agents import AgentConfig
from skills_sync.comparator import compare
from skills_sync.scanner import SkillInfo, scan_agents, scan_directory


class TestScanDirectory:
    """Testes para scan_directory."""

    def test_escaneia_skills_existentes(self, tmp_skills_dir: Path) -> None:
        """Deve encontrar skills com SKILL.md no diretório."""
        skills = scan_directory(tmp_skills_dir)
        assert len(skills) == 1
        assert skills[0].name == "example-skill"
        assert skills[0].description == "Uma skill de exemplo"

    def test_retorna_vazio_para_diretorio_inexistente(self) -> None:
        """Deve retornar lista vazia para diretório que não existe."""
        skills = scan_directory(Path("/caminho/inexistente"))
        assert skills == []

    def test_calcula_hash_consistente(self, tmp_skills_dir: Path) -> None:
        """Hash deve ser consistente para o mesmo conteúdo."""
        skills1 = scan_directory(tmp_skills_dir)
        skills2 = scan_directory(tmp_skills_dir)
        assert skills1[0].content_hash == skills2[0].content_hash
        assert skills1[0].content_hash != ""

    def test_hash_muda_com_conteudo_diferente(self, tmp_skills_dir: Path) -> None:
        """Hash deve mudar quando o conteúdo é alterado."""
        skills_before = scan_directory(tmp_skills_dir)
        hash_before = skills_before[0].content_hash

        # Modifica o conteúdo
        skill_md = tmp_skills_dir / "example-skill" / "SKILL.md"
        skill_md.write_text(
            '---\nname: example-skill\ndescription: "Descrição alterada"\n---\n\n# Alterado\n',
            encoding="utf-8",
        )

        skills_after = scan_directory(tmp_skills_dir)
        assert skills_after[0].content_hash != hash_before

    def test_ignora_diretorios_sem_skill_md(self, tmp_path: Path) -> None:
        """Deve ignorar diretórios que não contêm SKILL.md."""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()
        (skills_dir / "no-skill").mkdir()
        (skills_dir / "no-skill" / "README.md").write_text("# Sem SKILL.md")

        skills = scan_directory(skills_dir)
        assert skills == []


class TestScanAgents:
    """Testes para scan_agents com deduplicação."""

    def test_escaneia_agente(self, tmp_agent_dir: Path) -> None:
        """Deve encontrar skills em diretório de agente."""
        agent = AgentConfig(
            name="test-agent",
            display_name="Test Agent",
            global_dir=tmp_agent_dir,
            project_dir=".test-agent/skills",
        )
        skills = scan_agents([agent])
        assert len(skills) == 2
        names = {s.name for s in skills}
        assert names == {"skill-a", "skill-b"}

    def test_deduplica_mesma_skill_em_multiplos_agentes(self, tmp_agent_dir: Path) -> None:
        """Deve deduplicar skills idênticas de agentes diferentes."""
        agent1 = AgentConfig(
            name="agent-1",
            display_name="Agent 1",
            global_dir=tmp_agent_dir,
            project_dir=".agent-1/skills",
        )
        agent2 = AgentConfig(
            name="agent-2",
            display_name="Agent 2",
            global_dir=tmp_agent_dir,
            project_dir=".agent-2/skills",
        )

        skills = scan_agents([agent1, agent2])
        # Mesmos diretórios, mesmas skills — deve deduplicar
        assert len(skills) == 2
        for skill in skills:
            assert "Agent 1" in skill.source_agents
            assert "Agent 2" in skill.source_agents

    def test_parse_descricao_multiline(self, tmp_agent_dir: Path) -> None:
        """Deve parsear corretamente descrição multiline com >."""
        agent = AgentConfig(
            name="test",
            display_name="Test",
            global_dir=tmp_agent_dir,
            project_dir=".test/skills",
        )
        skills = scan_agents([agent])
        skill_b = next(s for s in skills if s.name == "skill-b")
        assert skill_b.description == "Skill B com descrição multiline"


class TestCompare:
    """Testes para comparação de skills."""

    def test_detecta_skill_nova(self) -> None:
        """Deve identificar skills que existem na fonte mas não no repo."""
        source = [
            SkillInfo(
                name="nova",
                description="",
                source_path=Path("/tmp"),
                content_hash="abc123",
            )
        ]
        repo: list[SkillInfo] = []
        result = compare(source, repo)
        assert len(result.new) == 1
        assert result.new[0].name == "nova"

    def test_detecta_skill_modificada(self) -> None:
        """Deve identificar skills com hash diferente."""
        source = [
            SkillInfo(
                name="existente",
                description="",
                source_path=Path("/tmp"),
                content_hash="novo_hash",
            )
        ]
        repo = [
            SkillInfo(
                name="existente",
                description="",
                source_path=Path("/repo"),
                content_hash="hash_antigo",
            )
        ]
        result = compare(source, repo)
        assert len(result.modified) == 1

    def test_detecta_skill_igual(self) -> None:
        """Deve identificar skills com mesmo hash."""
        source = [
            SkillInfo(
                name="igual",
                description="",
                source_path=Path("/tmp"),
                content_hash="mesmo_hash",
            )
        ]
        repo = [
            SkillInfo(
                name="igual",
                description="",
                source_path=Path("/repo"),
                content_hash="mesmo_hash",
            )
        ]
        result = compare(source, repo)
        assert len(result.same) == 1

    def test_resultado_misto(self) -> None:
        """Deve categorizar corretamente uma mistura de estados."""
        source = [
            SkillInfo(name="nova", description="", source_path=Path("/s"), content_hash="h1"),
            SkillInfo(name="mod", description="", source_path=Path("/s"), content_hash="h2_new"),
            SkillInfo(name="ok", description="", source_path=Path("/s"), content_hash="h3"),
        ]
        repo = [
            SkillInfo(name="mod", description="", source_path=Path("/r"), content_hash="h2_old"),
            SkillInfo(name="ok", description="", source_path=Path("/r"), content_hash="h3"),
        ]
        result = compare(source, repo)
        assert len(result.new) == 1
        assert len(result.modified) == 1
        assert len(result.same) == 1
