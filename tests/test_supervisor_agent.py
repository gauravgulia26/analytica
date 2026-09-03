import pytest
from analytica.agents.schema.agents_schema import NextAction, SupervisorOutput, Task
from analytica.graph.build import SupervisorBuild
from analytica.graph.state.supervisor_state import SupervisorState


def test_supervisor_schema_task():
    task = Task(
        task_id="task_1",
        action=NextAction.DATA_ANALYSIS,
        objective="Profile customer and subscription tables",
        description="Check schemas, identify candidate primary keys, and detect missing values",
        depends_on=[],
        expected_output=["Data profiling summary", "List of data quality flags"],
    )
    assert task.task_id == "task_1"
    assert task.action == NextAction.DATA_ANALYSIS
    assert len(task.expected_output) == 2


def test_supervisor_output_schema():
    output = SupervisorOutput(
        objective="Investigate SaaS business deterioration",
        tasks=[
            Task(
                task_id="task_1",
                action=NextAction.DATA_ANALYSIS,
                objective="Profile datasets",
                description="Inspect schemas and data quality",
                depends_on=[],
                expected_output=["Data profile"],
            ),
            Task(
                task_id="task_2",
                action=NextAction.PYTHON_ANALYSIS,
                objective="Compute churn metrics",
                description="Aggregate customer retention by cohort",
                depends_on=["task_1"],
                expected_output=["Cohort retention table"],
            ),
        ],
        final_deliverable="Executive churn and root-cause report",
    )
    assert len(output.tasks) == 2
    assert output.tasks[1].depends_on == ["task_1"]


def test_supervisor_graph_build():
    builder = SupervisorBuild()
    workflow = builder.get_compiled_graph()
    assert workflow is not None
    assert builder.graph_input_variable == ["user_request"]
