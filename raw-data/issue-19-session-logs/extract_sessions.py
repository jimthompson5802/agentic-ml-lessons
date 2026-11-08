"""Export locally available issue-19 chat and tool records without internal context."""

from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re

SOURCE = Path('/home/vscode/.codex')
DEST = Path(__file__).resolve().parent
MATCH = re.compile(r'issues/19\b|issue\s*#?19\b|us-12-19|US-12-assessment-splits', re.I)
PRIMARY = {
    '01a1b7d9-b475-7073-bb2d-c3c553934564': 'Blockers and initial planning request',
    '01a1b7db-f5ca-79d0-b69b-d7272c503196': 'Plan, native-library reuse and two/three-way alignment',
    '01a1b7f6-55e9-7c70-811b-b549d5165a01': 'IP1 contracts and two-helper scope decision',
    '01a1b825-c4f9-7ca0-89b6-d406a801c481': 'IP2 assessment implementation and approval',
    '01a1b836-70fd-7e30-aab4-54c3cbf9ff1b': 'IP3 partitions implementation and approval',
    '01a1b893-b142-7be3-b088-bde970277877': 'IP4, acceptance, PR/review, merge and branch cleanup',
}
TOOL_TYPES = {'function_call', 'function_call_output', 'custom_tool_call', 'custom_tool_call_output', 'web_search_call'}
# Avoid exporting credentials if a session happens to contain an unmasked token.
TOKEN = re.compile(r'\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{20,})\b')
redactions = 0


def redact(text):
    global redactions
    result, count = TOKEN.subn('[REDACTED_TOKEN]', text)
    redactions += count
    return result


def text_content(payload):
    return '\n'.join(part.get('text', '') for part in payload.get('content', []) if isinstance(part, dict) and part.get('type') in ('input_text', 'output_text', 'text'))


index = {}
for line in (SOURCE / 'session_index.jsonl').read_text().splitlines():
    item = json.loads(line)
    index[item['id']] = item
manifest = {
    'extracted_at_utc': datetime.now(timezone.utc).isoformat(),
    'issue': 'https://github.com/jimthompson5802/agentic-ml/issues/19',
    'source_root': str(SOURCE),
    'selection': MATCH.pattern,
    'format': 'Filtered public conversation and tool activity, not byte-for-byte raw rollouts',
    'excluded_records': 'Reasoning/internal context, system/developer messages, duplicate event messages, runtime state and setup-only user preambles',
    'active_session_cutoff': 'Current session stops at the user extraction request, excluding the extraction operation itself',
    'scanned_sessions': [], 'sessions': [],
}
combined = ['# Issue #19 — primary chat sessions\n']
for source in sorted((SOURCE / 'sessions').rglob('*.jsonl')):
    snapshot = source.read_bytes()
    lines = snapshot.splitlines()
    records = []
    incomplete = 0
    for number, line in enumerate(lines, 1):
        try:
            records.append((number, json.loads(line)))
        except json.JSONDecodeError:
            if number == len(lines) and not snapshot.endswith(b'\n'):
                incomplete += 1
            else:
                raise
    meta = next(item['payload'] for _, item in records if item.get('type') == 'session_meta')
    sid = meta['id']
    matched = bool(MATCH.search(snapshot.decode('utf-8')))
    manifest['scanned_sessions'].append({'id': sid, 'source': str(source), 'matched': matched})
    if not matched:
        continue
    category = 'primary' if sid in PRIMARY else 'contextual'
    directory = DEST / category
    directory.mkdir(exist_ok=True)
    title = index.get(sid, {}).get('thread_name', sid)
    stem = source.stem
    public = []
    chat = []
    omitted = Counter()
    cutoff = False
    last_line = 0
    for number, item in records:
        payload = item.get('payload', {})
        kind = payload.get('type')
        if item.get('type') != 'response_item':
            omitted[item.get('type', 'unknown')] += 1
            continue
        record = {'source_line': number, 'timestamp': item.get('timestamp'), 'type': kind}
        if kind == 'message' and payload.get('role') in ('user', 'assistant'):
            if payload.get('phase') in ('analysis', 'reasoning'):
                omitted['internal_message'] += 1
                continue
            content = text_content(payload)
            if payload['role'] == 'user' and content.startswith(('# AGENTS.md', '<environment_context>', '<INSTRUCTIONS>')):
                omitted['setup_user_message'] += 1
                continue
            record.update(role=payload['role'], phase=payload.get('phase'), text=content)
            public.append(record)
            chat.append(record)
            last_line = number
            if payload['role'] == 'user' and content.startswith('extract the chat session log from /home/vscode/.codex'):
                cutoff = True
                break
        elif kind in TOOL_TYPES:
            record['payload'] = payload
            public.append(record)
            last_line = number
        else:
            omitted[kind or 'unknown_response'] += 1
    jsonl = directory / (stem + '.jsonl')
    jsonl.write_text(''.join(redact(json.dumps(item, ensure_ascii=False)) + '\n' for item in public), encoding='utf-8')
    header = f'# {title}\n\nSession: `{sid}`\n\nStarted: {meta.get("timestamp")}\n\nCategory: {category}\n\nSource: `{source}`\n\n'
    body = header + '\n\n'.join(f'## {item["timestamp"]} — {item["role"].title()}' + (f' ({item["phase"]})' if item.get('phase') else '') + '\n\n' + item['text'] for item in chat) + '\n'
    markdown = directory / (stem + '.md')
    markdown.write_text(redact(body), encoding='utf-8')
    if category == 'primary':
        combined.append(redact(body))
    metadata = {
        'id': sid, 'title': title, 'category': category,
        'reason': PRIMARY.get(sid, 'Issue #19 reference appears in conversation, tools or supporting repository context; not an issue-19 implementation session'),
        'source': str(source), 'source_snapshot_bytes': len(snapshot),
        'source_snapshot_sha256': hashlib.sha256(snapshot).hexdigest(),
        'started_at': meta.get('timestamp'), 'cwd': meta.get('cwd'),
        'last_exported_source_line': last_line, 'cutoff_at_export_request': cutoff,
        'partial_trailing_lines_ignored': incomplete,
        'chat_messages': len(chat), 'tool_records': len(public) - len(chat),
        'omitted_record_counts': dict(omitted),
        'transcript': str(markdown.relative_to(DEST)),
        'events': str(jsonl.relative_to(DEST)),
        'transcript_sha256': hashlib.sha256(markdown.read_bytes()).hexdigest(),
        'events_sha256': hashlib.sha256(jsonl.read_bytes()).hexdigest(),
    }
    manifest['sessions'].append(metadata)
(DEST / 'all-primary-chat.md').write_text('\n\n---\n\n'.join(combined), encoding='utf-8')
manifest['token_redactions'] = redactions
(DEST / 'manifest.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
readme = ['# GitHub issue #19 — session-log export\n',
    f'Extracted: {manifest["extracted_at_utc"]}\n',
    f'Scanned **{len(manifest["scanned_sessions"])}** local session rollouts; exported **{len(manifest["sessions"])}** matching sessions: **6 primary**, **6 contextual**.\n',
    '[Read all six primary conversations](all-primary-chat.md). [Machine-readable manifest](manifest.json).\n',
    'Each session has a readable `.md` chat transcript and a `.jsonl` event log containing public chat and tool activity with source-line references. Whole conversations are retained, including other topics discussed in the same session. Tool activity is omitted from Markdown to keep it readable.\n',
    'Matching uses explicit issue-19 URLs/names, `US-12-19` identifiers and the assessment-splits branch. Contextual sessions match supporting documents/tool output rather than primarily implementing issue #19; these are included separately for completeness. The manifest inventories all scanned sessions and records snapshot/output hashes and counts.\n',
    'Exports omit internal reasoning/context, system/developer instructions, runtime state, duplicated event notifications and setup-only user preambles. They are filtered logs, not copies of the raw rollouts. The active IP4 session is captured through the user extraction request, excluding this export operation. No account/authentication databases or credentials files are copied. Recognizable unmasked GitHub/OpenAI token strings are redacted if encountered.\n',
    'Coverage is limited to rollouts currently present under `/home/vscode/.codex/sessions`; missing, deleted, other-machine or future messages are not recoverable from this export. Original files remain untouched.\n',
    '## Primary sessions\n', '| Started (UTC) | Session | Scope |', '|---|---|---|']
for category in ('primary', 'contextual'):
    if category == 'contextual':
        readme += ['\n## Contextual sessions\n', '| Started (UTC) | Session | Scope |', '|---|---|---|']
    for item in manifest['sessions']:
        if item['category'] == category:
            readme.append(f'| {item["started_at"]} | [{item["title"]}]({item["transcript"]}) | {item["reason"]} |')
(DEST / 'README.md').write_text('\n'.join(readme) + '\n', encoding='utf-8')
print(json.dumps({'scanned': len(manifest['scanned_sessions']), 'exported': len(manifest['sessions']), 'primary': sum(s['category'] == 'primary' for s in manifest['sessions']), 'chat_messages': sum(s['chat_messages'] for s in manifest['sessions']), 'tool_records': sum(s['tool_records'] for s in manifest['sessions']), 'token_redactions': redactions, 'output': str(DEST)}, indent=2))
