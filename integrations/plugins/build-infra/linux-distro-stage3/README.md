# linux-distro-stage3 integration

This plugin documents how `linux-distro-prefix` consumes stage3 tarballs
produced by [linux-distro-stage3](https://github.com/Interested-Deving-1896/linux-distro-stage3).

## How it works

`build.sh` fetches the appropriate stage3 tarball from the `linux-distro-stage3`
GitHub releases API, matching on `{distro}_stage3_{release}_{arch}_*.tar.gz`.

The stage3 tarball is unpacked into a temporary chroot directory. The Gentoo
prefix bootstrap then runs inside that chroot. The stage3 itself is not included
in the output prefix tarball — only `/usr/local` contents are packaged.

## Overriding the stage3 source

To use a locally built stage3 instead of a release download:

```bash
sudo ./build.sh \
  --distro debian --release trixie --arch amd64 \
  --stage3 /path/to/debian_stage3_trixie_amd64_20250101.tar.gz
```

Or set the environment variable:

```bash
export STAGE3_TARBALL=/path/to/tarball.tar.gz
sudo ./build.sh --distro debian --arch amd64
```

## Pointing at a different stage3 repo

```bash
export STAGE3_REPO=myorg/my-stage3-fork
sudo ./build.sh --distro debian --arch amd64
```
