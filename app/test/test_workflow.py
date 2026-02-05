# app/test/test_workflow.py
from app.engine.workflow import run_workflow
from app.engine.dispatcher import STEP_HANDLERS
from app.engine.context import WorkflowContext

def test_for_each_continue_on_error():
    print("\n=== TEST for_each continue on error ===")

    processed_items = []

    # Handler mock
    def fake_fetch_urls(step, ctx: WorkflowContext):
        item = ctx.data["item"]
        print(f"Processing item: {item}")

        if item == "BAD":
            print("❌ Error simulated")
            raise Exception("Simulated error")

        processed_items.append(item)
        print("✅ Success")

    # Injection du handler
    STEP_HANDLERS["fetch_urls"] = fake_fetch_urls

    # Workflow de test
    workflow = {
        "steps": [
            {
                "type": "for_each",
                "collection": "items",
                "steps": [
                    {"type": "fetch_urls"}
                ]
            }
        ]
    }

    ctx = WorkflowContext(run_id="MANUAL-TEST", headless=True)
    ctx.data["items"] = ["A", "B", "BAD", "C", "D"]

    result = run_workflow(workflow, ctx)

    print("\nProcessed items:", processed_items)
    print("\nWorkflow logs:")
    for log in result["logs"]:
        print(log)

    assert processed_items == ["A", "B", "C", "D"], "❌ Test FAILED"
    print("🎉 TEST PASSED")

if __name__ == "__main__":
    test_for_each_continue_on_error()
