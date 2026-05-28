# Building linux-distro-prefix

## Requirements

- Root access
- `curl`, `coreutils`, `tar`
- ~10 GB free disk space
- ~1–2 hours build time (depends on CPU and I/O speed)
- For cross-arch builds: `qemu-user-static` (auto-installed on Debian/Ubuntu hosts)

## Quick start

```bash
git clone https://github.com/Interested-Deving-1896/linux-distro-prefix
cd linux-distro-prefix
sudo ./build.sh --distro debian --release trixie --arch amd64
```

## Using a local stage3 tarball

If you have already built a stage3 with [linux-distro-stage3](https://github.com/Interested-Deving-1896/linux-distro-stage3), pass it directly to skip the download:

```bash
sudo ./build.sh \
  --distro debian --release trixie --arch amd64 \
  --stage3 /path/to/debian_stage3_trixie_amd64_20250101.tar.gz
```

## Resume support

If a previous build produced a partial prefix tarball in the output directory, `build.sh` will pre-seed the chroot with it before running the bootstrap. This allows resuming interrupted builds.

## Cross-arch builds

Cross-arch builds use QEMU binfmt_misc. On Debian/Ubuntu hosts, `qemu-user-static` is installed automatically. On other hosts, install it manually before running `build.sh`.

Example — build an arm64 prefix on an amd64 host:

```bash
sudo ./build.sh --distro debian --release trixie --arch arm64
```

## CI matrix

The GitHub Actions workflow builds all tier-1 combinations on every push and all tier-1/2 combinations monthly. See `config/matrix.yml` for tier assignments.

To trigger a manual build for a specific combination:

1. Go to **Actions → Build linux-distro-prefix → Run workflow**
2. Fill in `distro`, `release`, `arch`, and optionally `tier`
