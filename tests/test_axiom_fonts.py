"""The shared axiom-fonts pin and the release builds that must embed it."""
from pathlib import Path
import re
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]


def workflow(name):
    return yaml.load((ROOT / '.github/workflows' / name).read_text(), Loader=yaml.BaseLoader)


def default_ref(name):
    return workflow(name)['on']['workflow_call']['inputs']['axiom-fonts-ref']['default']


class AxiomFontsTests(unittest.TestCase):
    def test_shared_workflows_share_one_pinned_commit(self):
        ref = default_ref('release.yml')
        self.assertRegex(ref, r'^[0-9a-f]{40}$')
        for name in ('freebsd.yml', 'gate.yml'):
            with self.subTest(workflow=name):
                self.assertEqual(default_ref(name), ref)

    def test_release_builds_that_check_out_fonts_require_them(self):
        for job, data in workflow('release.yml')['jobs'].items():
            steps = data.get('steps', [])
            if not any('checkout-axiom-fonts' in step.get('uses', '') for step in steps):
                continue
            with self.subTest(job=job):
                builds = [step for step in steps
                          if step.get('env', {}).get('AXIOM_FONTS_DIR')
                          or 'AXIOM_FONTS_DIR=' in step.get('run', '')]
                self.assertTrue(builds, f'{job} checks out axiom-fonts but no step uses it')
                for step in builds:
                    required = step.get('env', {}).get('AXIOM_FONTS_REQUIRED') == '1' or re.search(
                        r'\bAXIOM_FONTS_REQUIRED=1\b', step.get('run', ''))
                    self.assertTrue(required, f'{job}: {step.get("name")} sets AXIOM_FONTS_DIR without AXIOM_FONTS_REQUIRED=1')


if __name__ == '__main__':
    unittest.main()
