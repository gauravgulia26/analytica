import sys

from dotenv import load_dotenv
from rich import print
from rich.progress import Progress, SpinnerColumn, TextColumn

from analytica.core.config.paths import ROOT_DIR
from analytica.exception.custom_exception import AnalyticaException
from analytica.graph.build import SupervisorBuild

load_dotenv()

txt = (ROOT_DIR / "input.md").read_text().strip()


def main():
    builder = SupervisorBuild()
    workflow = builder.get_compiled_graph()

    accumulated_state = {}

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
    ) as progress:
        task = progress.add_task(
            description="Starting Supervisor workflow...",
            total=None,
        )

        try:
            for event in workflow.stream({builder.graph_input_variable[0]: txt}):
                for node_name, node_output in event.items():
                    progress.update(
                        task,
                        description=f"Running step: {node_name}",
                    )
                    if isinstance(node_output, dict):
                        accumulated_state.update(node_output)

        except Exception as e:  # noqa: BLE001
            progress.update(
                task,
                description="Supervisor workflow failed",
            )
            raise AnalyticaException(
                error=e,
                error_detail=sys,
            )

        progress.update(
            task,
            description="Supervisor workflow completed",
        )

    return accumulated_state


if __name__ == "__main__":
    res = main()
    print("\n[bold green]=== Supervisor Analytical Workflow Plan ===[/bold green]\n")
    print(f"[bold cyan]Objective:[/bold cyan] {res.get('objective')}\n")
    tasks = res.get("tasks", [])
    print(f"[bold cyan]Total Planned Tasks:[/bold cyan] {len(tasks)}\n")
    for t in tasks:
        deps = f" (Depends on: {', '.join(t.depends_on)})" if t.depends_on else ""
        action_tag = f"[{t.action.value}]"
        prefix = f"  [bold yellow]{t.task_id}[/bold yellow] {action_tag}: "
        print(f"{prefix}[bold]{t.objective}[/bold]{deps}")
        print(f"    [dim]Scope:[/dim] {t.description}")
        if t.expected_output:
            print(f"    [dim]Expected Deliverables:[/dim] {', '.join(t.expected_output)}")
        print()
    print(f"[bold cyan]Final Deliverable:[/bold cyan] {res.get('final_deliverable')}\n")
