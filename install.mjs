#!/usr/bin/env node
/**
 * gsd-dsx installer.
 *
 * Installs the capability as a GSD overlay (~/.gsd/capabilities/dsx) and projects
 * its agents and skills into the host runtime's directories. No dependencies —
 * Node stdlib only, matching gsd-core's own toolchain.
 *
 *   node install.mjs                    # install for Claude Code (global)
 *   node install.mjs --runtime cursor   # another runtime
 *   node install.mjs --local            # into ./.claude instead of ~/.claude
 *   node install.mjs --check            # verify an existing install
 *   node install.mjs --uninstall
 */

import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import process from 'node:process';
import { fileURLToPath } from 'node:url';

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const CAPABILITY_ID = 'dsx';

/** Runtime config homes. Mirrors gsd-core's runtime descriptors for the tier-1 set. */
const RUNTIMES = {
  claude: { global: '.claude', local: '.claude' },
  cursor: { global: '.cursor', local: '.cursor' },
  codex: { global: '.codex', local: '.codex' },
  opencode: { global: path.join('.config', 'opencode'), local: '.opencode' },
  kilo: { global: path.join('.config', 'kilo'), local: '.kilo' },
  windsurf: { global: path.join('.codeium', 'windsurf'), local: '.windsurf' },
  copilot: { global: '.copilot', local: '.github' },
  antigravity: { global: path.join('.gemini', 'antigravity'), local: '.agents' },
};

/** Payload copied into the capability overlay root, in order. */
const CAPABILITY_PAYLOAD = [
  { from: path.join('capabilities', CAPABILITY_ID, 'capability.json'), to: 'capability.json' },
  { from: path.join('capabilities', CAPABILITY_ID, 'fragments'), to: 'fragments' },
  { from: 'dsx', to: 'dsx' },
  { from: 'bin', to: 'bin' },
  { from: 'references', to: 'references' },
  { from: 'templates', to: 'templates' },
  { from: 'examples', to: 'examples' },
];

// ── argv ─────────────────────────────────────────────────────────────────────

function parseArgs(argv) {
  const args = { runtime: 'claude', local: false, check: false, uninstall: false, force: false };
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (token === '--runtime') args.runtime = argv[++i];
    else if (token === '--local') args.local = true;
    else if (token === '--check') args.check = true;
    else if (token === '--uninstall') args.uninstall = true;
    else if (token === '--force') args.force = true;
    else if (token === '--help' || token === '-h') args.help = true;
    else if (token.startsWith('--runtime=')) args.runtime = token.slice('--runtime='.length);
    else die(`unknown argument: ${token}`);
  }
  return args;
}

function die(message) {
  console.error(`gsd-dsx: ${message}`);
  process.exit(1);
}

const log = (message) => console.log(`  ${message}`);

// ── fs helpers ───────────────────────────────────────────────────────────────

function copyRecursive(from, to) {
  const stat = fs.statSync(from);
  if (stat.isDirectory()) {
    fs.mkdirSync(to, { recursive: true });
    for (const entry of fs.readdirSync(from)) {
      if (entry === '__pycache__' || entry === '.DS_Store' || entry.endsWith('.pyc')) continue;
      copyRecursive(path.join(from, entry), path.join(to, entry));
    }
    return;
  }
  fs.mkdirSync(path.dirname(to), { recursive: true });
  fs.copyFileSync(from, to);
  fs.chmodSync(to, stat.mode);
}

function removeIfPresent(target) {
  if (fs.existsSync(target)) fs.rmSync(target, { recursive: true, force: true });
}

function resolveRuntimeHome(runtime, local) {
  const descriptor = RUNTIMES[runtime];
  if (!descriptor) {
    die(`unknown runtime "${runtime}". Known: ${Object.keys(RUNTIMES).join(', ')}`);
  }
  return local
    ? path.resolve(process.cwd(), descriptor.local)
    : path.join(os.homedir(), descriptor.global);
}

// ── preflight ────────────────────────────────────────────────────────────────

function findPython() {
  for (const candidate of [process.env.DSX_PYTHON, 'python3', 'python'].filter(Boolean)) {
    try {
      const version = execFileSync(candidate, ['--version'], { encoding: 'utf8' }).trim();
      const match = /(\d+)\.(\d+)/.exec(version);
      if (match && (Number(match[1]) > 3 || (Number(match[1]) === 3 && Number(match[2]) >= 9))) {
        return { command: candidate, version };
      }
    } catch {
      /* try the next candidate */
    }
  }
  return null;
}

// ── commands ─────────────────────────────────────────────────────────────────

function install(args) {
  const python = findPython();
  if (!python) {
    die(
      'no Python 3.9+ found on PATH. dsx gates are Python; install python3 or set DSX_PYTHON, ' +
        'then re-run. (No third-party packages are needed — the checks are stdlib-only.)',
    );
  }

  const overlayRoot = path.join(os.homedir(), '.gsd', 'capabilities', CAPABILITY_ID);
  const runtimeHome = resolveRuntimeHome(args.runtime, args.local);
  const manifest = JSON.parse(
    fs.readFileSync(path.join(ROOT, 'capabilities', CAPABILITY_ID, 'capability.json'), 'utf8'),
  );

  console.log(`\ngsd-dsx — data science, analytics and BI rigour for GSD\n`);
  log(`python:   ${python.command} (${python.version})`);
  log(`overlay:  ${overlayRoot}`);
  log(`runtime:  ${runtimeHome}\n`);

  if (fs.existsSync(overlayRoot) && !args.force) {
    log('existing install found — replacing capability payload');
  }

  // 1. Capability overlay
  removeIfPresent(overlayRoot);
  fs.mkdirSync(overlayRoot, { recursive: true });
  for (const item of CAPABILITY_PAYLOAD) {
    const source = path.join(ROOT, item.from);
    if (!fs.existsSync(source)) die(`missing payload: ${item.from}`);
    copyRecursive(source, path.join(overlayRoot, item.to));
  }
  fs.chmodSync(path.join(overlayRoot, 'bin', 'dsx'), 0o755);
  log(`capability installed (${CAPABILITY_PAYLOAD.length} payload entries)`);

  // 2. Agents
  const agentsDir = path.join(runtimeHome, 'agents');
  fs.mkdirSync(agentsDir, { recursive: true });
  let agentCount = 0;
  for (const entry of fs.readdirSync(path.join(ROOT, 'agents'))) {
    if (!entry.endsWith('.md')) continue;
    fs.copyFileSync(path.join(ROOT, 'agents', entry), path.join(agentsDir, entry));
    agentCount += 1;
  }
  log(`${agentCount} agents -> ${path.relative(os.homedir(), agentsDir) || agentsDir}`);

  // 3. Skills
  const skillsDir = path.join(runtimeHome, 'skills');
  fs.mkdirSync(skillsDir, { recursive: true });
  // Only skills the manifest declares are projected. Sweeping the directory
  // instead would install anything that happened to be sitting in skills/ —
  // a working copy, a personal house-style skill — into the user's runtime.
  // `--check` already verifies against manifest.skills; install now agrees.
  let skillCount = 0;
  for (const entry of manifest.skills) {
    const source = path.join(ROOT, 'skills', entry);
    if (!fs.existsSync(path.join(source, 'SKILL.md'))) {
      throw new Error(`manifest declares skill '${entry}' but skills/${entry}/SKILL.md is missing`);
    }
    removeIfPresent(path.join(skillsDir, entry));
    copyRecursive(source, path.join(skillsDir, entry));
    skillCount += 1;
  }
  log(`${skillCount} skills -> ${path.relative(os.homedir(), skillsDir) || skillsDir}`);

  // 4. PATH shim — gates fall back to the overlay path, so this is convenience only.
  const shimDir = path.join(os.homedir(), '.local', 'bin');
  const shim = path.join(shimDir, 'dsx');
  try {
    fs.mkdirSync(shimDir, { recursive: true });
    removeIfPresent(shim);
    fs.symlinkSync(path.join(overlayRoot, 'bin', 'dsx'), shim);
    const onPath = (process.env.PATH || '').split(path.delimiter).includes(shimDir);
    log(`cli shim  -> ${shim}${onPath ? '' : '   (add ~/.local/bin to PATH)'}`);
  } catch {
    log('cli shim  -> skipped (gates use the overlay path directly)');
  }

  // 5. Self-test
  const result = selfTest(overlayRoot, python.command);
  console.log('');
  if (!result.ok) {
    die(`self-test failed:\n${result.output}`);
  }
  log('self-test passed');

  console.log(`
Installed. Next:

  1. Enable it:            gsd config set dsx.enforce true
  2. Scaffold a spec:      dsx init
  3. See what it catches:  dsx audit --spec ${path.join(overlayRoot, 'examples', 'bad-ANALYSIS-SPEC.yaml')}

Gates now run at plan:post, execute:post, verify:post and ship:pre.
Phases without an ANALYSIS-SPEC pass through untouched, so this is safe to enable
in a mixed repository. Set dsx.require_spec true in a pure analytics project.
`);
}

function selfTest(overlayRoot, python) {
  const good = path.join(overlayRoot, 'examples', 'good-ANALYSIS-SPEC.yaml');
  const bad = path.join(overlayRoot, 'examples', 'bad-ANALYSIS-SPEC.yaml');
  const run = (spec) => {
    try {
      execFileSync(python, ['-m', 'dsx', 'gate', 'ship', '--spec', spec], {
        cwd: overlayRoot,
        env: { ...process.env, PYTHONPATH: overlayRoot },
        encoding: 'utf8',
        stdio: 'pipe',
      });
      return 0;
    } catch (error) {
      return error.status ?? 2;
    }
  };
  const goodCode = run(good);
  const badCode = run(bad);
  if (goodCode !== 0) {
    return { ok: false, output: `the known-good spec was rejected (exit ${goodCode})` };
  }
  if (badCode !== 1) {
    return { ok: false, output: `the known-bad spec was not blocked (exit ${badCode}, expected 1)` };
  }
  return { ok: true, output: '' };
}

function check(args) {
  const overlayRoot = path.join(os.homedir(), '.gsd', 'capabilities', CAPABILITY_ID);
  if (!fs.existsSync(overlayRoot)) die(`not installed (no ${overlayRoot})`);
  const python = findPython();
  if (!python) die('no Python 3.9+ on PATH');

  const manifest = JSON.parse(fs.readFileSync(path.join(overlayRoot, 'capability.json'), 'utf8'));
  const runtimeHome = resolveRuntimeHome(args.runtime, args.local);

  console.log(`\ngsd-dsx ${manifest.version}\n`);
  log(`overlay:  ${overlayRoot}`);
  log(`python:   ${python.command} (${python.version})`);

  const missingAgents = manifest.agents.filter(
    (name) => !fs.existsSync(path.join(runtimeHome, 'agents', `${name}.md`)),
  );
  const missingSkills = manifest.skills.filter(
    (name) => !fs.existsSync(path.join(runtimeHome, 'skills', name, 'SKILL.md')),
  );
  log(`agents:   ${manifest.agents.length - missingAgents.length}/${manifest.agents.length} present`);
  log(`skills:   ${manifest.skills.length - missingSkills.length}/${manifest.skills.length} present`);
  log(`gates:    ${manifest.gates.length} declared`);

  const result = selfTest(overlayRoot, python.command);
  log(`self-test: ${result.ok ? 'passed' : `FAILED — ${result.output}`}`);
  console.log('');

  const problems = missingAgents.length + missingSkills.length + (result.ok ? 0 : 1);
  if (problems) {
    if (missingAgents.length) console.error(`  missing agents: ${missingAgents.join(', ')}`);
    if (missingSkills.length) console.error(`  missing skills: ${missingSkills.join(', ')}`);
    process.exit(1);
  }
}

function uninstall(args) {
  const overlayRoot = path.join(os.homedir(), '.gsd', 'capabilities', CAPABILITY_ID);
  const runtimeHome = resolveRuntimeHome(args.runtime, args.local);
  const manifestPath = path.join(overlayRoot, 'capability.json');

  let manifest = { agents: [], skills: [] };
  if (fs.existsSync(manifestPath)) manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));

  for (const name of manifest.agents) removeIfPresent(path.join(runtimeHome, 'agents', `${name}.md`));
  for (const name of manifest.skills) removeIfPresent(path.join(runtimeHome, 'skills', name));
  removeIfPresent(path.join(os.homedir(), '.local', 'bin', 'dsx'));
  removeIfPresent(overlayRoot);

  console.log('\ngsd-dsx removed. Your ANALYSIS-SPEC files are untouched.\n');
}

function help() {
  console.log(`
gsd-dsx installer

  node install.mjs [--runtime <name>] [--local] [--force]
  node install.mjs --check
  node install.mjs --uninstall

  --runtime   ${Object.keys(RUNTIMES).join(' | ')}   (default: claude)
  --local     install into ./<runtime-dir> instead of the home directory
  --check     verify an existing install and run the self-test
  --force     replace an existing install without prompting
`);
}

const args = parseArgs(process.argv.slice(2));
if (args.help) help();
else if (args.uninstall) uninstall(args);
else if (args.check) check(args);
else install(args);
