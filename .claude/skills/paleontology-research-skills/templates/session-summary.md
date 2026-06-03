# Session Summary — `{{session_id}}`

**Title**: `{{title}}`
**Started**: `{{started_at}}`
**Ended**: `{{ended_at}}`
**Topic tags**: `{{topic_tags}}`

---

## 1. What was investigated

{{summary_paragraph}}

## 2. Commands run

| Tool | Args (truncated) | Result |
|------|------------------|--------|
{{command_table}}

## 3. Key conclusions

{{conclusions_bullets}}

## 4. Open questions for follow-up

{{open_questions_bullets}}

## 5. References cited

{{reference_list}}

---

## How to resume

```bash
python3 .claude/skills/paleontology-research-skills/paleo-session/scripts/session_resume.py --id {{session_id}}
```

The output of `session_resume.py` is suitable to inject into a new conversation's
context to continue this line of research.
