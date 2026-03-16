"""Interface de linha de comando para o skills-sync."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from skills_sync.agents import AGENTS, detect_installed
from skills_sync.comparator import compare
from skills_sync.scanner import SkillInfo, scan_agents, scan_directory, scan_projects
from skills_sync.sync import sync_skill

# Cores ANSI (respeitam NO_COLOR e detecção de TTY)
_USE_COLOR = sys.stdout.isatty() and "NO_COLOR" not in os.environ

_GREEN = "\033[32m" if _USE_COLOR else ""
_YELLOW = "\033[33m" if _USE_COLOR else ""
_GRAY = "\033[90m" if _USE_COLOR else ""
_BOLD = "\033[1m" if _USE_COLOR else ""
_RESET = "\033[0m" if _USE_COLOR else ""
_CYAN = "\033[36m" if _USE_COLOR else ""


def _resolve_repo_dir() -> Path:
    """Encontra o diretório 'skills/' do repositório automaticamente."""
    # Sobe a partir do diretório do pacote até encontrar skills/ com SKILL.md
    current = Path(__file__).resolve().parent
    for _ in range(10):
        candidate = current / "skills"
        if candidate.is_dir() and any(candidate.glob("*/SKILL.md")):
            return candidate
        parent = current.parent
        if parent == current:
            break
        current = parent
    # Fallback: diretório atual
    return Path.cwd() / "skills"


def _format_agents(agents: list[str]) -> str:
    """Formata lista de agentes para exibição."""
    return ", ".join(agents)


def _print_header(title: str) -> None:
    print(f"\n{_BOLD}{title}{_RESET}")
    print("─" * 60)


def cmd_agents(args: argparse.Namespace) -> None:
    """Lista agentes detectados na máquina."""
    installed = detect_installed()

    if not installed:
        print("Nenhum agente com diretório de skills detectado.")
        return

    _print_header(f"Agentes detectados ({len(installed)})")
    for agent in sorted(installed, key=lambda a: a.display_name):
        skills = scan_directory(agent.global_dir.resolve())
        count = len(skills)
        suffix = "skill" if count == 1 else "skills"
        print(f"  {_CYAN}{agent.display_name:<25}{_RESET} {agent.global_dir}  ({count} {suffix})")


def cmd_list(args: argparse.Namespace) -> None:
    """Lista skills no repositório."""
    repo_dir = Path(args.repo_dir) if args.repo_dir else _resolve_repo_dir()

    if not repo_dir.is_dir():
        print(f"Diretório do repositório não encontrado: {repo_dir}")
        return

    skills = scan_directory(repo_dir)

    if not skills:
        print("Nenhuma skill encontrada no repositório.")
        return

    _print_header(f"Skills no repositório ({len(skills)})")
    for skill in sorted(skills, key=lambda s: s.name):
        desc = skill.description[:70] + "..." if len(skill.description) > 70 else skill.description
        print(f"  {_BOLD}{skill.name:<25}{_RESET} {desc}")


def cmd_scan(args: argparse.Namespace) -> None:
    """Escaneia skills de agentes e compara com o repositório."""
    repo_dir = Path(args.repo_dir) if args.repo_dir else _resolve_repo_dir()

    # Filtra agentes se especificado
    if args.agent:
        if args.agent not in AGENTS:
            print(f"Agente '{args.agent}' não reconhecido.")
            print(f"Agentes disponíveis: {', '.join(sorted(AGENTS.keys()))}")
            sys.exit(1)
        target_agents = [AGENTS[args.agent]]
    else:
        target_agents = detect_installed()

    if not target_agents:
        print("Nenhum agente com skills detectado na máquina.")
        return

    # Escaneia skills globais
    print(f"{_GRAY}Escaneando skills de {len(target_agents)} agente(s)...{_RESET}")
    all_sources: list[SkillInfo] = scan_agents(target_agents)

    # Escaneia projetos (a menos que --global-only)
    if not args.global_only and args.projects_dir:
        projects_dir = Path(args.projects_dir)
        print(f"{_GRAY}Escaneando projetos em {projects_dir}...{_RESET}")
        project_skills = scan_projects(projects_dir, target_agents)
        # Mescla com deduplicação por hash
        seen_hashes = {s.content_hash for s in all_sources}
        for ps in project_skills:
            if ps.content_hash not in seen_hashes:
                all_sources.append(ps)
                seen_hashes.add(ps.content_hash)

    if not all_sources:
        print("Nenhuma skill encontrada nos agentes.")
        return

    # Filtra por nome se --skill especificado
    if args.skill:
        all_sources = [s for s in all_sources if args.skill.lower() in s.name.lower()]
        if not all_sources:
            print(f"Nenhuma skill com nome contendo '{args.skill}' encontrada.")
            return

    # Compara com repositório
    repo_skills = scan_directory(repo_dir)
    result = compare(all_sources, repo_skills)

    # Exibe resultados
    actionable: list[tuple[str, SkillInfo]] = []

    if result.new:
        _print_header("Skills novas")
        for skill in sorted(result.new, key=lambda s: s.name):
            idx = len(actionable) + 1
            actionable.append(("new", skill))
            agents_str = _format_agents(skill.source_agents)
            print(
                f"  {_GREEN}[{idx:>2}] [NEW]{_RESET} "
                f"{_BOLD}{skill.name:<25}{_RESET} "
                f"← {agents_str}"
            )

    if result.modified:
        _print_header("Skills modificadas")
        for source, _repo in sorted(result.modified, key=lambda t: t[0].name):
            idx = len(actionable) + 1
            actionable.append(("mod", source))
            agents_str = _format_agents(source.source_agents)
            print(
                f"  {_YELLOW}[{idx:>2}] [MOD]{_RESET} "
                f"{_BOLD}{source.name:<25}{_RESET} "
                f"← {agents_str}"
            )

    if result.same:
        _print_header("Skills iguais")
        for skill in sorted(result.same, key=lambda s: s.name):
            agents_str = _format_agents(skill.source_agents)
            print(f"  {_GRAY}[ OK] {skill.name:<25}{_RESET} ← {agents_str}")

    if not actionable:
        print(f"\n{_GREEN}Tudo sincronizado! Nenhuma ação necessária.{_RESET}")
        return

    # Modo não-interativo
    if args.yes or args.dry_run:
        selected = actionable
    else:
        # Seleção interativa
        print(f"\n{_BOLD}Selecione as skills para sincronizar:{_RESET}")
        print("  Números separados por vírgula (ex: 1,3,5), 'all' para todas, ou 'q' para sair")

        try:
            choice = input(f"\n{_CYAN}>{_RESET} ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nCancelado.")
            return

        if choice.lower() in ("q", "quit", "sair"):
            return

        if choice.lower() in ("all", "todos", "*"):
            selected = actionable
        else:
            try:
                indices = [int(x.strip()) for x in choice.split(",") if x.strip()]
                selected = []
                for i in indices:
                    if 1 <= i <= len(actionable):
                        selected.append(actionable[i - 1])
                    else:
                        print(f"Índice {i} fora do intervalo.")
                        return
            except ValueError:
                print("Entrada inválida.")
                return

    if not selected:
        print("Nenhuma skill selecionada.")
        return

    # Sincroniza
    print()
    for status, skill in selected:
        dest = sync_skill(skill, repo_dir, dry_run=args.dry_run)
        label = "NEW" if status == "new" else "MOD"
        prefix = "[DRY-RUN] " if args.dry_run else ""
        print(f"  {prefix}{_GREEN}✓{_RESET} [{label}] {skill.name} → {dest}")

    total = len(selected)
    suffix = "skill sincronizada" if total == 1 else "skills sincronizadas"
    dry = " (dry-run)" if args.dry_run else ""
    print(f"\n{_GREEN}{_BOLD}{total} {suffix}{dry}.{_RESET}")


def _build_parser() -> argparse.ArgumentParser:
    """Constrói o parser de argumentos."""
    parser = argparse.ArgumentParser(
        prog="skills-sync",
        description="Sincroniza skills de agentes de IA com o repositório central.",
    )
    parser.add_argument(
        "--repo-dir",
        default=None,
        help="Caminho para o diretório skills/ do repositório (detectado automaticamente).",
    )

    subparsers = parser.add_subparsers(dest="command", help="Comandos disponíveis")

    # Subcomando: scan
    scan_parser = subparsers.add_parser("scan", help="Escanear e sincronizar skills")
    scan_parser.add_argument("--agent", help="Escanear apenas um agente específico")
    scan_parser.add_argument(
        "--global-only",
        action="store_true",
        help="Escanear apenas diretórios globais (sem projetos)",
    )
    scan_parser.add_argument("--projects-dir", help="Diretório base para buscar projetos")
    scan_parser.add_argument(
        "--yes",
        "-y",
        action="store_true",
        help="Sincronizar todas as skills sem confirmação",
    )
    scan_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Mostrar o que seria feito sem executar",
    )
    scan_parser.add_argument("--skill", help="Filtrar por nome da skill")

    # Subcomando: agents
    subparsers.add_parser("agents", help="Listar agentes detectados")

    # Subcomando: list
    subparsers.add_parser("list", help="Listar skills no repositório")

    return parser


def main() -> None:
    """Ponto de entrada principal do CLI."""
    parser = _build_parser()
    args = parser.parse_args()

    if args.command == "scan":
        cmd_scan(args)
    elif args.command == "agents":
        cmd_agents(args)
    elif args.command == "list":
        cmd_list(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
