#!/usr/bin/env node
// Claude Code skill audit: budget estimate, duplicates, long descriptions, unused candidates.
// Adapted from steipete/agent-scripts (Codex-oriented) for Claude Code's skill roots.
'use strict';
const fs = require('fs');
const path = require('path');
const os = require('os');

function parseArgs(argv) {
  const opts = { months: 3, contextTokens: 200000, budgetPercent: 2, roots: [], logs: true };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--months') opts.months = Number(argv[++i]);
    else if (a === '--context-tokens') opts.contextTokens = Number(argv[++i]);
    else if (a === '--budget-percent') opts.budgetPercent = Number(argv[++i]);
    else if (a === '--root') opts.roots.push(argv[++i]);
    else if (a === '--no-logs') opts.logs = false;
    else if (a === '--self-test') opts.selfTest = true;
  }
  return opts;
}

// ponytail: hand-rolled two-key frontmatter parser, a real YAML dep is overkill for name/description
function parseFrontmatter(text) {
  const m = text.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!m) return null;
  const out = {};
  for (const line of m[1].split(/\r?\n/)) {
    const kv = line.match(/^(\w[\w-]*):\s*(.*)$/);
    if (!kv) continue;
    let val = kv[2].trim();
    if ((val.startsWith('"') && val.endsWith('"')) || (val.startsWith("'") && val.endsWith("'"))) {
      val = val.slice(1, -1);
    }
    out[kv[1]] = val;
  }
  return out;
}

function findSkillFiles(root) {
  const results = [];
  if (!fs.existsSync(root)) return results;
  const stack = [root];
  while (stack.length) {
    const dir = stack.pop();
    let entries;
    try { entries = fs.readdirSync(dir, { withFileTypes: true }); } catch { continue; }
    for (const e of entries) {
      const p = path.join(dir, e.name);
      if (e.isDirectory()) stack.push(p);
      else if (e.name === 'SKILL.md') results.push(p);
    }
  }
  return results;
}

function collectSkills(opts) {
  const home = os.homedir();
  const roots = [
    { label: 'personal', dir: path.join(home, '.claude', 'skills') },
    { label: 'project', dir: path.join(process.cwd(), '.claude', 'skills') },
    { label: 'plugin', dir: path.join(home, '.claude', 'plugins', 'cache') },
    ...opts.roots.map((r) => ({ label: 'extra', dir: r.replace(/^~/, home) })),
  ];
  const seenRealpath = new Set();
  const skills = [];
  for (const root of roots) {
    for (const file of findSkillFiles(root.dir)) {
      let real;
      try { real = fs.realpathSync(file); } catch { real = file; }
      if (seenRealpath.has(real)) continue;
      seenRealpath.add(real);
      const raw = fs.readFileSync(file, 'utf8');
      const fm = parseFrontmatter(raw) || {};
      const name = fm.name || path.basename(path.dirname(file));
      const description = fm.description || '';
      skills.push({ root: root.label, file, name, description, bytes: Buffer.byteLength(description, 'utf8') });
    }
  }
  return skills;
}

function tokenCost(bytes) {
  return Math.ceil(bytes / 4);
}

function findDuplicates(skills) {
  const byName = new Map();
  for (const s of skills) {
    if (!byName.has(s.name)) byName.set(s.name, []);
    byName.get(s.name).push(s);
  }
  const dupes = [];
  for (const [name, group] of byName) {
    if (group.length > 1) dupes.push({ name, entries: group });
  }
  return dupes;
}

// ponytail: usage check is a substring scan over recent session transcripts, not a real
// tool-call audit like Codex's history.jsonl parser. Good enough to flag likely-dead skills.
function findUnused(skills, opts) {
  if (!opts.logs) return [];
  const home = os.homedir();
  const projectsDir = path.join(home, '.claude', 'projects');
  if (!fs.existsSync(projectsDir)) return [];
  const cutoff = Date.now() - opts.months * 30 * 24 * 60 * 60 * 1000;
  let text = '';
  const stack = [projectsDir];
  while (stack.length) {
    const dir = stack.pop();
    let entries;
    try { entries = fs.readdirSync(dir, { withFileTypes: true }); } catch { continue; }
    for (const e of entries) {
      const p = path.join(dir, e.name);
      if (e.isDirectory()) { stack.push(p); continue; }
      if (!e.name.endsWith('.jsonl')) continue;
      const stat = fs.statSync(p);
      if (stat.mtimeMs < cutoff) continue;
      text += fs.readFileSync(p, 'utf8') + '\n';
    }
  }
  return skills.filter((s) => !text.includes(s.name));
}

function report(opts) {
  const skills = collectSkills(opts);
  const budgetTokens = Math.floor(opts.contextTokens * (opts.budgetPercent / 100));
  const totalTokens = skills.reduce((sum, s) => sum + tokenCost(s.bytes), 0);

  console.log(`\n== Skill Budget ==`);
  console.log(`${skills.length} skills found, ~${totalTokens} description tokens vs ${budgetTokens} budget (${opts.budgetPercent}% of ${opts.contextTokens}).`);
  if (totalTokens > budgetTokens) console.log(`OVER budget by ~${totalTokens - budgetTokens} tokens.`);

  console.log(`\n== Description candidates (>400 chars) ==`);
  skills.filter((s) => s.description.length > 400)
    .sort((a, b) => b.description.length - a.description.length)
    .forEach((s) => console.log(`- ${s.name} (${s.description.length} chars) [${s.root}] ${s.file}`));

  console.log(`\n== Duplicates ==`);
  findDuplicates(skills).forEach((d) => {
    console.log(`- ${d.name}: ${d.entries.map((e) => `${e.root}:${e.file}`).join(' | ')}`);
  });

  console.log(`\n== Unused candidates (no mention in last ${opts.months}mo of session logs) ==`);
  findUnused(skills, opts).forEach((s) => console.log(`- ${s.name} [${s.root}] ${s.file}`));

  console.log(`\n== Root summary ==`);
  const byRoot = {};
  for (const s of skills) byRoot[s.root] = (byRoot[s.root] || 0) + 1;
  Object.entries(byRoot).forEach(([root, count]) => console.log(`- ${root}: ${count}`));
  console.log('');
}

function selfTest() {
  const assert = require('assert');
  const fm = parseFrontmatter('---\nname: foo\ndescription: "bar baz"\n---\nbody');
  assert.strictEqual(fm.name, 'foo');
  assert.strictEqual(fm.description, 'bar baz');
  assert.strictEqual(tokenCost(4), 1);
  const dupes = findDuplicates([
    { name: 'a', root: 'x', file: '1' },
    { name: 'a', root: 'y', file: '2' },
    { name: 'b', root: 'x', file: '3' },
  ]);
  assert.strictEqual(dupes.length, 1);
  assert.strictEqual(dupes[0].name, 'a');
  console.log('self-test OK');
}

const opts = parseArgs(process.argv.slice(2));
if (opts.selfTest) selfTest();
else report(opts);
