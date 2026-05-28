# linux-distro-prefix

A distro-agnostic, architecture-agnostic Gentoo prefix builder.

Builds a self-contained Gentoo prefix (`/usr/local/gentoo`) on top of any supported Linux distro and CPU architecture. The prefix is independent of the host distro after installation — only the bootstrap chroot depends on the base distro.

Stage3 rootfs tarballs are sourced from [linux-distro-stage3](https://github.com/Interested-Deving-1896/linux-distro-stage3) releases.

## Supported distros and architectures

| Distro | amd64 | arm64 | armhf | riscv64 | ppc64el | s390x | loong64 | i386 |
|--------|-------|-------|-------|---------|---------|-------|---------|------|
| Debian | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Ubuntu | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | — | ✓ |
| Devuan | ✓ | ✓ | ✓ | ✓ | ✓ | — | — | ✓ |
| Arch | ✓ | ✓ | ✓ | ✓ | — | — | — | ✓ |
| Fedora | ✓ | ✓ | ✓ | — | ✓ | ✓ | — | ✓ |
| Alpine | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Void | ✓ | ✓ | ✓ | — | ✓ | — | — | ✓ |
| openSUSE | ✓ | ✓ | ✓ | — | ✓ | ✓ | — | ✓ |
| Gentoo | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

Tier-1 (CI on every push): amd64, arm64, armhf. See `config/matrix.yml` for full tier assignments.

## What the prefix contains

- Gentoo prefix bootstrap stages 1–3 (`bootstrap-prefix.sh`)
- `app-portage/prefix-toolkit`
- `startprefix` launcher at `/usr/local/bin/startprefix`

No display stack, no ChromeOS-specific packages. Forks can add those on top.

## Building locally

Requirements: root access, `curl`, `coreutils`, ~10 GB free disk space, ~1–2 hours build time.

```bash
git clone https://github.com/Interested-Deving-1896/linux-distro-prefix
cd linux-distro-prefix
sudo ./build.sh --distro debian --release trixie --arch amd64
```

Cross-arch builds require `qemu-user-static` (installed automatically on Debian/Ubuntu hosts).

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `--distro` | `debian` | Base distro for bootstrap chroot |
| `--release` | `trixie` | Distro release |
| `--arch` | `amd64` | Target architecture |
| `--output` | `./` | Output directory for tarball |
| `--jobs` | `nproc` | Parallel jobs |
| `--stage3` | _(fetched)_ | Path to a local stage3 tarball |

### Output

```
linux_distro_prefix_{distro}_{arch}_{YYYYMMDD}.tar.gz
linux_distro_prefix_{distro}_{arch}_{YYYYMMDD}.tar.gz.sha256
linux_distro_prefix_{distro}_{arch}.tar.gz          ← symlink to latest
```

## Installing the prefix

```bash
# Extract to /usr/local (takes ~2 GB)
sudo tar zxf linux_distro_prefix_debian_amd64_YYYYMMDD.tar.gz -C /usr/local

# Enter the prefix
/usr/local/bin/startprefix
```

## Relationship to other projects

```
linux-distro-stage3   →   linux-distro-prefix   →   penguins-eggs-prefix
     (stage3 tarballs)         (prefix tarballs)          (prefix + ISO)
```

- **linux-distro-stage3**: provides the bootstrap chroot base
- **linux-distro-prefix**: this repo — builds the Gentoo prefix
- **penguins-eggs-prefix**: fork that adds penguins-eggs integration for ISO production

## License

MIT
