# How to Generate UML Final Image

To create the `uml_final.png` file required by the assignment:

1. Open the Mermaid Live Editor: https://mermaid.live/
2. Copy the Mermaid code from `uml_diagram.md` (the code block between the backticks)
3. Paste it into the Mermaid Live Editor
4. Click the "Download PNG" button in the editor
5. Save the file as `uml_final.png` in the project root directory

Alternatively, if you have the Mermaid CLI installed:
```bash
mmdc -i uml_diagram.md -o uml_final.png
```

The UML diagram visualizes the four core classes (Task, Pet, Owner, Scheduler) and their relationships.
