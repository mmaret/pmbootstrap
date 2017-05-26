"""
Copyright 2017 Oliver Smith

This file is part of pmbootstrap.

pmbootstrap is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pmbootstrap is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pmbootstrap.  If not, see <http://www.gnu.org/licenses/>.
"""
import logging
import pmb.chroot
import pmb.config
import pmb.install.losetup


def partitions_mount(args):
    """
    Mount blockdevices of partitions inside native chroot
    """
    prefix = args.sdcard
    if not args.sdcard:
        img_path = "/home/user/rootfs/" + args.device + ".img"
        prefix = pmb.install.losetup.device_by_back_file(args, img_path)
    for suffix in ["p1", "p2"]:
        pmb.helpers.mount.bind_blockdevice(args, prefix + suffix,
                                           args.work + "/chroot_native/dev/install" + suffix)


def partition(args):
    """
    Partition /dev/install and create /dev/install{p1,p2}
    """

    size_boot = pmb.config.install_size_boot
    logging.info("(native) partition /dev/install (boot: " + size_boot +
                 ", root: the rest)")
    commands = [
        ["mktable", "msdos"],
        ["mkpart", "primary", "ext2", "2048s", size_boot],
        ["mkpart", "primary", size_boot, "100%"],
        ["set", "1", "boot", "on"]
    ]
    for command in commands:
        pmb.chroot.root(args, ["parted", "-s", "/dev/install"] +
                        command)

    # Mount new partitions
    partitions_mount(args)