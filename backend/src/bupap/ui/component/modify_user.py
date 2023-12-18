from __future__ import annotations

from typing import TYPE_CHECKING, Callable

import python_avatars as pa
import sqlalchemy as sa
from loguru import logger
from nicegui import ui
from python_avatars.core import AvatarPart, _get_path
from python_avatars.svg_parser import SVGParser

from bupap import db
from bupap.avatar import deserialize_avatar, random_avatar
from bupap.ui.crud.user import update_user
from bupap.ui.viewmodel.user import ModifiedUser

from .avatar import Avatar
from .errors import Errors


class PartSelector:
    def __init__(self, avatar: Avatar, part_type: type[AvatarPart]) -> None:
        self.avatar = avatar
        self.part_type = part_type
        with ui.dialog() as self.select_dialog, ui.card() as card:
            card.style("max-width: 962px")  # 8 buttons / row, 100 px / button, 18px gap
            with ui.column():
                with ui.row():
                    for t in self.part_type.get_all():
                        with ui.button(on_click=self.set_avatar_cb(t)).props(
                            'color="secondary"'
                        ).classes("w-[100px] h-[100px]") as btn:
                            if t.value == "":
                                btn.text = "None"
                            else:
                                btn.text = ""
                                ui.html(self._get_svg(t)).classes(
                                    "w-20 [&_svg]:w-20 h-20 [&_svg]:h-20"
                                )
        self.select_button = (
            ui.button(on_click=self.select_dialog.open)
            .props('color="secondary"')
            .classes("w-[100px] h-[100px]")
        )
        self._render_select_button()

    def _get_svg(self, t):
        svg = SVGParser(_get_path(type(t), t))
        if isinstance(t, pa.HairType):
            el = svg.get_element_by_id("Hair-Color")
            if el is not None:
                el.set_attr("fill", pa.HairColor.BROWN)
        if isinstance(t, pa.HatType):
            el = svg.get_element_by_id("Fabric-Color")
            if el is not None:
                el.set_attr("fill", pa.ClothingColor.BLUE_03)
        if isinstance(t, pa.FacialHairType):
            el = svg.get_element_by_id("Facial-Hair-Color")
            if el is not None:
                el.set_attr("fill", pa.HairColor.BROWN)
        if isinstance(t, pa.ClothingType):
            el = svg.get_element_by_id("Fabric-Color")
            if el is not None:
                el.set_attr("fill", pa.ClothingColor.BLUE_03)
        return svg.render()

    def _render_select_button(self):
        t = getattr(self.avatar.value, self._key())
        self.select_button.clear()
        with self.select_button:
            if t.value == "":
                self.select_button.text = "None"
            else:
                self.select_button.text = ""
                ui.html(self._get_svg(t)).classes("w-20 [&_svg]:w-20 h-20 [&_svg]:h-20")

    def _key(self):
        return {
            pa.TopType: "top",
            pa.AccessoryType: "accessory",
            pa.EyebrowType: "eyebrows",
            pa.EyeType: "eyes",
            pa.NoseType: "nose",
            pa.MouthType: "mouth",
            pa.FacialHairType: "facial_hair",
            pa.ClothingType: "clothing",
            pa.ClothingGraphic: "shirt_graphic",
        }[self.part_type]

    def set_avatar_cb(self, value):
        def cb():
            setattr(self.avatar.value, self._key(), value)
            self.avatar.update_content()
            self.select_dialog.close()
            self.select_button.clear()
            self._render_select_button()

        return cb


class PartColorSelector:
    def __init__(self, avatar: Avatar, key: str, name: str) -> None:
        self.avatar = avatar
        self.key = key
        self.name = name
        with ui.button(name) as self.button:
            ui.color_picker(on_pick=lambda e: self.pick_color(e.color))
        color = getattr(self.avatar.value, key)
        if not isinstance(color, str):
            color = color.value
        self.pick_color(color)

    def pick_color(self, color):
        self.button.style(f"background-color:{color}!important")
        setattr(self.avatar.value, self.key, color)
        self.avatar.update_content()


class ModifyUser:
    def __init__(self, user: db.User, cb_on_modify: Callable[[], None] | None = None):
        self.model = ModifiedUser(
            db_id=user.id,
            name=user.name,
            full_name=user.full_name,
            avatar=deserialize_avatar(user.avatar),
        )
        self.cb_on_modify = cb_on_modify
        with ui.dialog() as self.dialog, ui.card() as card:
            # 5 buttons / row with 100px / button + 6 * 18px for gaps / margins = 490 px
            card.style("max-width: 608px").classes("items-center")
            ps_clothing_graphic = None
            ps_clothing_text = None

            def avatar_update(_):
                if ps_clothing_graphic is None or ps_clothing_text is None or self.avatar is None:
                    return
                if self.avatar.value.clothing != pa.ClothingType.GRAPHIC_SHIRT:
                    ps_clothing_graphic.select_button.disable()
                    ps_clothing_text.disable()
                else:
                    ps_clothing_graphic.select_button.enable()
                    if self.avatar.value.shirt_graphic != pa.ClothingGraphic.CUSTOM_TEXT:
                        ps_clothing_text.disable()
                    else:
                        ps_clothing_text.enable()

            self.avatar = Avatar(self.model.avatar, on_update_content=avatar_update).classes("h-80")
            ui.button("Random", on_click=lambda evt: self.set_random_avatar()).props(
                'color="secondary"'
            )
            with ui.row().classes("items-center"):
                PartSelector(self.avatar, pa.TopType)
                PartSelector(self.avatar, pa.AccessoryType)
                PartSelector(self.avatar, pa.EyebrowType)
                PartSelector(self.avatar, pa.EyeType)
                PartSelector(self.avatar, pa.NoseType)
                PartSelector(self.avatar, pa.MouthType)
                PartSelector(self.avatar, pa.FacialHairType)
                PartSelector(self.avatar, pa.ClothingType)
                ps_clothing_graphic = PartSelector(self.avatar, pa.ClothingGraphic)

                def change_text(evt):
                    self.avatar.value.shirt_text = evt.value
                    self.avatar.update_content()

                ps_clothing_text = ui.input(
                    label="Shirt Text", value=self.avatar.value.shirt_text, on_change=change_text
                ).classes("w-[100px]")
            with ui.row():
                PartColorSelector(self.avatar, "skin_color", "Skin")
                PartColorSelector(self.avatar, "hair_color", "Hair")
                PartColorSelector(self.avatar, "facial_hair_color", "Beard")
                PartColorSelector(self.avatar, "hat_color", "Hat")
                PartColorSelector(self.avatar, "clothing_color", "Clothing")
                PartColorSelector(self.avatar, "background_color", "Background")

            ui.input(label="Username").props("outline").classes("full-width").bind_value(
                self.model, "name"
            )
            ui.input(label="Display Name").props("outline").classes("full-width").bind_value(
                self.model, "full_name"
            )
            with ui.row().classes("full-width"):
                ui.button("Save", on_click=self.save).classes("grow")
                ui.button("Cancel", on_click=self.cancel).classes("grow bg-negative")

    @Errors.wrap_error("Failed to create a user")
    def save(self):
        try:
            update_user(self.model)
        finally:
            self.dialog.close()
        if self.cb_on_modify:
            self.cb_on_modify()

    def set_random_avatar(self):
        self.model.new_random_avatar()
        self.avatar.value = self.model.avatar

    def open(self):
        self.avatar.value = self.model.avatar
        self.dialog.open()

    def cancel(self):
        self.dialog.close()
