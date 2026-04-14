
import typer
from cli.commands import audit, duplicates, analyze, stats, watch, fix
from cli.commands import list_cmd, search, export, score, compare, init_cmd, lint
from cli.commands import usage, cleanup

app = typer.Typer(help="SkillForge — skill file audit and management CLI.")

app.command("audit")(audit.audit_cmd)
app.command("duplicates")(duplicates.duplicates_cmd)
app.command("analyze")(analyze.analyze_cmd)
app.command("stats")(stats.stats_cmd)
app.command("watch")(watch.watch_cmd)
app.command("fix")(fix.fix_cmd)
app.command("list")(list_cmd.list_cmd)
app.command("search")(search.search_cmd)
app.command("export")(export.export_cmd)
app.command("score")(score.score_cmd)
app.command("compare")(compare.compare_cmd)
app.command("init")(init_cmd.init_cmd)
app.command("lint")(lint.lint_cmd)
app.command("usage")(usage.usage_cmd)
app.command("cleanup")(cleanup.cleanup_cmd)

if __name__ == "__main__":
    app()
