from pathlib import Path

import python_avatars as pa

folder = Path(__file__).parent


def random_avatar():
    return pa.Avatar.random(style='bupap_avatar').render()


def install_style():
    file_path = (folder / "data" / "bupap_avatar.svg").resolve()
    assert file_path.exists()
    try:
        pa.install_part(str((folder / "data" / "bupap_avatar.svg").resolve()), pa.AvatarStyle)
    except FileExistsError:
        pass
