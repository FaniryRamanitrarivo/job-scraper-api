class StepExecutor:
    def __init__(self, dispatcher):
        self.dispatcher = dispatcher

    def execute(self, step, ctx):
        step_type = step["type"]
        if step_type not in self.dispatcher:
            raise ValueError(f"Unknown step type: {step_type}")
        self.dispatcher[step_type](step, ctx)
