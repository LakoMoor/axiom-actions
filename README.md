# axiom-actions

Reusable GitHub Actions workflows and composite actions for Axiom (https://github.com/LakoMoor/Axiom).
They hold the quality gate, the release pipeline and the packaging checks in one place, so the
application's own workflows only say what to build and with which inputs.

## Workflows

Call them from the application's repository with `uses: LakoMoor/axiom-actions/.github/workflows/<name>.yml@main`.

| Workflow | What it does |
|---|---|
| `gate.yml` | The quality gate for pull requests and pushes to `main`: one job per runner, running the project's own checks (`cargo xtask ci`), with optional build-time fonts. |
| `release.yml` | The multi-platform release: builds the desktop app, the CLI and the web viewer, packages them for each system, writes checksums and publishes a draft GitHub release. |
| `freebsd.yml` | Builds and tests on FreeBSD in a guest machine. |
| `windows-arm64.yml` | Builds and packages for Windows on ARM64. |
| `packaging-lint.yml` | Checks the desktop entry, the metadata file, the Windows installer source and the Flatpak manifests. |

## Actions

Composite actions under `actions/`, used by the workflows above and usable on their own:
`arch-package`, `checkout-axiom-fonts`, `checkout-axiom-i18n`, `draft-release`, `freebsd-cargo-cache`,
`install-apt-packages`, `install-linux-deps`, `install-nfpm`, `install-riscv64-cross`, `install-trunk`,
`install-wix`, `packaging-lint` and `resolve-version`.

`checkout-axiom-fonts` checks out [axiom-fonts](https://github.com/LakoMoor/axiom-fonts) at the commit the
caller pins and sets `AXIOM_FONTS_DIR` for the build. `checkout-axiom-i18n` does nothing unless the caller
has an `axiom-i18n.rev` file.

## Pinning

The workflows are called at `@main`, so a fix here reaches every caller. A caller that needs a stable
version pins a commit instead.

## Tests

`tests/` holds Python tests for the scripts embedded in the workflows and actions. Run them with
`python3 -I -m unittest discover -s tests` from a checkout you trust.

## Licence

MIT OR Apache-2.0, as for Axiom.
