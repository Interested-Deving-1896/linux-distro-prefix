#!/usr/bin/env python3
"""
Generate GitHub Actions matrix JSON from config/matrix.yml.

Usage:
  python3 scripts/gen-matrix.py [--tier 1] [--distro debian] [--arch amd64]

Outputs a JSON object suitable for use as a GitHub Actions matrix strategy.
"""

import argparse
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    # Minimal block-style YAML parser — no external dependencies required
    def _parse_block_yaml(text):
        root = {}
        stack = [(root, -1)]
        current_list_key = None

        for raw_line in text.splitlines():
            if not raw_line.strip() or raw_line.strip().startswith('#'):
                continue
            stripped = raw_line.lstrip()
            indent = len(raw_line) - len(stripped)

            # Pop stack to current indent level
            while len(stack) > 1 and stack[-1][1] >= indent:
                stack.pop()
            parent = stack[-1][0]

            if stripped.startswith('- '):
                val = stripped[2:].strip()
                if isinstance(parent, list):
                    parent.append(val)
                else:
                    if current_list_key and isinstance(parent.get(current_list_key), list):
                        parent[current_list_key].append(val)
            elif ':' in stripped:
                key, _, val = stripped.partition(':')
                key = key.strip()
                val = val.strip().strip('"').strip("'")
                if val == '':
                    # mapping or list follows
                    new_node = {}
                    if isinstance(parent, dict):
                        parent[key] = new_node
                        current_list_key = key
                    stack.append((new_node, indent))
                else:
                    if isinstance(parent, dict):
                        # Try int/float coercion
                        try:
                            parent[key] = int(val)
                        except ValueError:
                            try:
                                parent[key] = float(val)
                            except ValueError:
                                parent[key] = val
        return root

    class yaml:  # noqa: N801
        @staticmethod
        def safe_load(text):
            return _parse_block_yaml(text)


def load_matrix(path: Path) -> dict:
    with open(path) as f:
        return yaml.safe_load(f.read())


def build_matrix(config: dict, tier_max: int, distro_filter: str, arch_filter: str) -> list:
    entries = []
    for distro, dcfg in config.get('distros', {}).items():
        if distro_filter and distro != distro_filter:
            continue
        default_release = dcfg.get('default_release', '')
        for arch, acfg in dcfg.get('arches', {}).items():
            if arch_filter and arch != arch_filter:
                continue
            tier = acfg.get('tier', 99)
            if tier > tier_max:
                continue
            entries.append({
                'distro': distro,
                'release': default_release,
                'arch': arch,
                'tier': tier,
            })
    return entries


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--tier', type=int, default=1, help='Maximum tier to include (default: 1)')
    parser.add_argument('--distro', default='', help='Filter to a single distro')
    parser.add_argument('--arch', default='', help='Filter to a single arch')
    parser.add_argument('--matrix-file', default='config/matrix.yml')
    args = parser.parse_args()

    matrix_path = Path(__file__).parent.parent / args.matrix_file
    if not matrix_path.exists():
        print(f"Matrix file not found: {matrix_path}", file=sys.stderr)
        sys.exit(1)

    config = load_matrix(matrix_path)
    entries = build_matrix(config, args.tier, args.distro, args.arch)

    if not entries:
        print("No matrix entries matched the given filters", file=sys.stderr)
        sys.exit(1)

    print(json.dumps({'include': entries}, indent=2))


if __name__ == '__main__':
    main()
