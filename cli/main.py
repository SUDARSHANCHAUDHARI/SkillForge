
import typer
from cli.commands import audit, duplicates, analyze, stats, watch, fix
from cli.commands import list_cmd

app = typer.Typer(help="SkillForge — skill file audit and management CLI.")

app.command("audit")(audit.audit_cmd)
app.command("duplicates")(duplicates.duplicates_cmd)
app.command("analyze")(analyze.analyze_cmd)
app.command("stats")(stats.stats_cmd)
app.command("watch")(watch.watch_cmd)
app.command("fix")(fix.fix_cmd)
app.command("list")(list_cmd.list_cmd)

if __name__ == "__main__":
    app()
