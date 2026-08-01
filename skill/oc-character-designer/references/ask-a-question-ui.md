# Ask interaction adapter

The skill does not assume a private widget name.

1. If the runtime exposes a native question tool, call it without printing tool JSON.
2. In an App runtime, render the same question object through the App component.
3. Otherwise show a numbered structured-text batch.

Every question has a stable ID, one selection mode, 2–6 meaningfully different options when applicable, a short concept explanation and a custom-answer field. Typed text overrides a conflicting selected option.
