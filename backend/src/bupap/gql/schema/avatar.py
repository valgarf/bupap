import json
from functools import cache
from typing import Self

import python_avatars as pa
import strawberry
from python_avatars.svg_parser import SVGParser

from bupap import db
from bupap.avatar import deserialize_avatar, random_avatar, serialize_avatar

from ..common.db_type import DBType, map_to_db


@strawberry.type
class AvatarPart:
    part: strawberry.Private[pa.core.AvatarPart]

    @strawberry.field()
    def name(self) -> str:
        return self.part.name

    @strawberry.field()
    def svg(self) -> str:
        return render_part(self.part)


def part_from_name(part_type: type[pa.core.AvatarPart], name: str) -> AvatarPart:
    for p in part_type.get_all():
        if p.name == name:
            return AvatarPart(part=p)
    raise RuntimeError(f"Unkown part '{name}' for type '{part_type.__name__}'.")


@strawberry.type
class Avatar:
    svg: str = strawberry.field()

    top: AvatarPart = strawberry.field()
    accessory: AvatarPart = strawberry.field()
    eyebrows: AvatarPart = strawberry.field()
    eyes: AvatarPart = strawberry.field()
    nose: AvatarPart = strawberry.field()
    mouth: AvatarPart = strawberry.field()
    beard: AvatarPart = strawberry.field()
    clothing: AvatarPart = strawberry.field()
    graphic: AvatarPart = strawberry.field()

    skin_color: str = strawberry.field()
    hair_color: str = strawberry.field()
    beard_color: str = strawberry.field()
    hat_color: str = strawberry.field()
    clothing_color: str = strawberry.field()
    background_color: str = strawberry.field()

    shirt_text: str = strawberry.field()

    @strawberry.field()
    def svg(self) -> str:
        return self.to_avatar_lib().render()

    @classmethod
    def from_avatar_lib(cls, value: pa.Avatar) -> Self:
        return Avatar(
            background_color=value.background_color,
            top=AvatarPart(part=value.top),
            hat_color=value.hat_color,
            eyebrows=AvatarPart(part=value.eyebrows),
            eyes=AvatarPart(part=value.eyes),
            nose=AvatarPart(part=value.nose),
            mouth=AvatarPart(part=value.mouth),
            beard=AvatarPart(part=value.facial_hair),
            skin_color=value.skin_color,
            hair_color=value.hair_color,
            beard_color=value.facial_hair_color,
            accessory=AvatarPart(part=value.accessory),
            clothing=AvatarPart(part=value.clothing),
            clothing_color=value.clothing_color,
            graphic=AvatarPart(part=value.shirt_graphic),
            shirt_text=value.shirt_text,
        )

    def to_avatar_lib(self) -> pa.Avatar:
        return pa.Avatar(
            style="bupap_avatar",
            background_color=self.background_color,
            top=self.top.part,
            hat_color=self.hat_color,
            eyebrows=self.eyebrows.part,
            eyes=self.eyes.part,
            nose=self.nose.part,
            mouth=self.mouth.part,
            facial_hair=self.beard.part,
            skin_color=self.skin_color,
            hair_color=self.hair_color,
            facial_hair_color=self.beard_color,
            accessory=self.accessory.part,
            clothing=self.clothing.part,
            clothing_color=self.clothing_color,
            shirt_graphic=self.graphic.part,
            shirt_text=self.shirt_text,
            title=None,
        )

    @classmethod
    def from_json(cls, value: str) -> Self:
        return cls.from_avatar_lib(deserialize_avatar(value))

    def to_json(self: Self) -> str:
        return serialize_avatar(self.to_avatar_lib())


@strawberry.input
class AvatarInput:
    top: str = strawberry.field()
    accessory: str = strawberry.field()
    eyebrows: str = strawberry.field()
    eyes: str = strawberry.field()
    nose: str = strawberry.field()
    mouth: str = strawberry.field()
    beard: str = strawberry.field()
    clothing: str = strawberry.field()
    graphic: str = strawberry.field()

    skin_color: str = strawberry.field()
    hair_color: str = strawberry.field()
    beard_color: str = strawberry.field()
    hat_color: str = strawberry.field()
    clothing_color: str = strawberry.field()
    background_color: str = strawberry.field()

    shirt_text: str = strawberry.field()


@strawberry.type
class AvatarAPI:
    tops: list[AvatarPart] = strawberry.field()
    accessories: list[AvatarPart] = strawberry.field()
    eyebrows: list[AvatarPart] = strawberry.field()
    eyes: list[AvatarPart] = strawberry.field()
    noses: list[AvatarPart] = strawberry.field()
    mouths: list[AvatarPart] = strawberry.field()
    beards: list[AvatarPart] = strawberry.field()
    clothings: list[AvatarPart] = strawberry.field()
    graphics: list[AvatarPart] = strawberry.field()

    @strawberry.field
    def create(self, avatar: AvatarInput) -> Avatar:
        return Avatar(
            top=part_from_name(pa.TopType, avatar.top),
            accessory=part_from_name(pa.AccessoryType, avatar.accessory),
            eyebrows=part_from_name(pa.EyebrowType, avatar.eyebrows),
            eyes=part_from_name(pa.EyeType, avatar.eyes),
            nose=part_from_name(pa.NoseType, avatar.nose),
            mouth=part_from_name(pa.MouthType, avatar.mouth),
            beard=part_from_name(pa.FacialHairType, avatar.beard),
            clothing=part_from_name(pa.ClothingType, avatar.clothing),
            graphic=part_from_name(pa.ClothingGraphic, avatar.graphic),
            skin_color=avatar.skin_color,
            hair_color=avatar.hair_color,
            beard_color=avatar.beard_color,
            hat_color=avatar.hat_color,
            clothing_color=avatar.clothing_color,
            background_color=avatar.background_color,
            shirt_text=avatar.shirt_text,
        )

    @strawberry.field
    def random(self) -> Avatar:
        return Avatar.from_avatar_lib(random_avatar())


@cache
def render_part(p: pa.core.AvatarPart) -> str:
    svg = SVGParser(pa.core._get_path(type(p), p))
    if isinstance(p, pa.HairType):
        el = svg.get_element_by_id("Hair-Color")
        if el is not None:
            el.set_attr("fill", pa.HairColor.BROWN)
    if isinstance(p, pa.HatType):
        el = svg.get_element_by_id("Fabric-Color")
        if el is not None:
            el.set_attr("fill", pa.ClothingColor.BLUE_03)
    if isinstance(p, pa.FacialHairType):
        el = svg.get_element_by_id("Facial-Hair-Color")
        if el is not None:
            el.set_attr("fill", pa.HairColor.BROWN)
    if isinstance(p, pa.ClothingType):
        el = svg.get_element_by_id("Fabric-Color")
        if el is not None:
            el.set_attr("fill", pa.ClothingColor.BLUE_03)
    return svg.render()


def get_parts(part_type: type[pa.core.AvatarPart]):
    result = []
    for p in part_type.get_all():
        result.append(AvatarPart(part=p))
    return result


@cache
def get_avatar_api():
    return AvatarAPI(
        tops=get_parts(pa.TopType),
        accessories=get_parts(pa.AccessoryType),
        eyebrows=get_parts(pa.EyebrowType),
        eyes=get_parts(pa.EyeType),
        noses=get_parts(pa.NoseType),
        mouths=get_parts(pa.MouthType),
        beards=get_parts(pa.FacialHairType),
        clothings=get_parts(pa.ClothingType),
        graphics=get_parts(pa.ClothingGraphic),
    )
