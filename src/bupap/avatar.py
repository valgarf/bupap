from pathlib import Path

import python_avatars as pa

folder = Path(__file__).parent


def random_avatar():
    return pa.Avatar.random(style=pa.AvatarStyle.BUPAP_AVATAR).render()


def install_style():
    try:
        pa.install_part(str((folder / "data" / "bupap_avatar.svg").resolve()), pa.AvatarStyle)
    except FileExistsError:
        pass
