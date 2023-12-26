import json
from pathlib import Path

import python_avatars as pa

folder = Path(__file__).parent


def random_avatar():
    result = pa.Avatar.random(style="bupap_avatar")
    result.shirt_text = ""
    return result


def install_style():
    file_path = (folder / "data" / "bupap_avatar.svg").resolve()
    assert file_path.exists()
    try:
        pa.install_part(str((folder / "data" / "bupap_avatar.svg").resolve()), pa.AvatarStyle)
    except FileExistsError:
        pass


def serialize_avatar(avatar: pa.Avatar) -> str:
    return json.dumps(
        {
            "background_color": str(avatar.background_color),
            "hat": str(avatar.top) if isinstance(avatar.top, pa.HatType) else None,
            "hair": str(avatar.top) if isinstance(avatar.top, pa.HairType) else None,
            "hat_color": str(avatar.hat_color),
            "eyebrows": str(avatar.eyebrows),
            "eyes": str(avatar.eyes),
            "nose": str(avatar.nose),
            "mouth": str(avatar.mouth),
            "facial_hair": str(avatar.facial_hair),
            "skin_color": str(avatar.skin_color),
            "hair_color": str(avatar.hair_color),
            "facial_hair_color": str(avatar.facial_hair_color),
            "accessory": str(avatar.accessory),
            "clothing": str(avatar.clothing),
            "clothing_color": str(avatar.clothing_color),
            "shirt_graphic": str(avatar.shirt_graphic),
            "shirt_text": str(avatar.shirt_text),
            "title": str(avatar.title),
        }
    )


def deserialize_avatar(value: str) -> pa.Avatar:
    data = json.loads(value)

    return pa.Avatar(
        style="bupap_avatar",
        background_color=data["background_color"],
        top=pa.HairType(data["hair"]) if data["hair"] else pa.HatType(data["hat"]),
        hat_color=data["hat_color"],
        eyebrows=pa.EyebrowType(data["eyebrows"]),
        eyes=pa.EyeType(data["eyes"]),
        nose=pa.NoseType(data["nose"]),
        mouth=pa.MouthType(data["mouth"]),
        facial_hair=pa.FacialHairType(data["facial_hair"]),
        skin_color=data["skin_color"],
        hair_color=data["hair_color"],
        facial_hair_color=data["facial_hair_color"],
        accessory=pa.AccessoryType(data["accessory"]),
        clothing=pa.ClothingType(data["clothing"]),
        clothing_color=data["clothing_color"],
        shirt_graphic=pa.ClothingGraphic(data["shirt_graphic"]),
        shirt_text=data["shirt_text"],
        title=None,
    )
