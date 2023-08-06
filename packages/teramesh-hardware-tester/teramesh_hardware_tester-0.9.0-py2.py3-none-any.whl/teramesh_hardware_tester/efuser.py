#!/bin/env python3

import asyncio
import click
import logging
import os
import sys
import tempfile

import serial.tools.list_ports
import esptool
import espefuse

from asciimatics.widgets import (
    Frame,
    ListBox,
    Layout,
    Divider,
    VerticalDivider,
    Text,
    Button,
    TextBox,
    Widget,
    Label,
    CheckBox,
    PopUpDialog,
)
from asciimatics.widgets.utilities import THEMES
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.event import KeyboardEvent
from asciimatics.exceptions import StopApplication
from collections import defaultdict


logger = logging.getLogger("efuser")
logger.setLevel(logging.INFO)

do_check_ports = True

BASE_DIR = os.path.dirname(__file__)
TMP_DIR = os.path.join(os.environ["HOME"], ".hwtester")

# bit_no is from LSB, and we currently have 14 bits for feature flags
# so bit_no 0 goes to binary_blob[13]
HW_FEATURES_FLAG_BASE = 13
HW_FEATURES = [
    {"name": "SHTC3 sensor", "default": True, "bit_no": 0},
    {"name": "PIR sensor", "default": False, "bit_no": 1},
    {"name": "IAQ sensor", "default": False, "bit_no": 2},
    {"name": "1-Wire sensor", "default": False, "bit_no": 3},
    {"name": "Modbus RS485 iface", "default": False, "bit_no": 4},
    {"name": "Cellular iface (NB/Cat1)", "default": False, "bit_no": 5},
    {"name": "TM1650 LED display", "default": False, "bit_no": 6},
    {"name": "4x Thermostat btn (legacy)", "default": False, "bit_no": 7},
    {"name": "6x Thermostat buttons", "default": False, "bit_no": 8},
    {"name": "6x Switch buttons", "default": False, "bit_no": 9},
]


THEMES["monochrome2"] = defaultdict(
    lambda: (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK),
    {
        "invalid": (Screen.COLOUR_BLACK, Screen.A_NORMAL, Screen.COLOUR_RED),
        "label": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLACK),
        "title": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLACK),
        "selected_field": (Screen.COLOUR_YELLOW, Screen.A_BOLD, Screen.COLOUR_BLACK),
        "selected_focus_field": (
            Screen.COLOUR_YELLOW,
            Screen.A_BOLD,
            Screen.COLOUR_BLACK,
        ),
        "focus_button": (Screen.COLOUR_YELLOW, Screen.A_BOLD, Screen.COLOUR_BLUE),
        "selected_focus_control": (
            Screen.COLOUR_YELLOW,
            Screen.A_BOLD,
            Screen.COLOUR_BLACK,
        ),
        "disabled": (Screen.COLOUR_BLACK, Screen.A_BOLD, Screen.COLOUR_BLACK),
        "edit_text": (Screen.COLOUR_YELLOW, Screen.A_NORMAL, Screen.COLOUR_BLACK),
        "focus_edit_text": (Screen.COLOUR_YELLOW, Screen.A_BOLD, Screen.COLOUR_BLACK),
    },
)


class HidePrint:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, "w")

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


class EfuserView(Frame):
    """
    Main view.
    """

    def __init__(self, screen):
        super(EfuserView, self).__init__(
            screen,
            max([30, int(screen.height / 1.5)]),
            max([40, int(screen.width / 1.5)]),
            hover_focus=True,
            can_scroll=False,
            title="eFuse Burner v.0.0.1",
        )

        layout = Layout([10, 1, 40, 1, 20], fill_frame=True)
        self.add_layout(layout)

        layout.add_widget(Label("Installed modules:"), 0)
        layout.add_widget(Divider(), 0)
        for feature in HW_FEATURES:
            layout.add_widget(CheckBox(feature["name"], on_change=self._on_change, name="features_%s" % feature["bit_no"]), 0)
            self.data["features_%s" % feature["bit_no"]] = feature["default"]

        layout.add_widget(VerticalDivider(), 1)

        layout.add_widget(Label("Hardware version:"), 2)
        layout.add_widget(Divider(), 2)
        self.data["major"] = "3"
        self.data["minor"] = "4"
        self.data["patch"] = "5"
        self.data["output"] = ["Output will appear here..."]
        layout.add_widget(Text("Major:", "major", on_change=self._on_change), 2)
        layout.add_widget(Divider(), 2)
        layout.add_widget(Text("Minor:", "minor", on_change=self._on_change), 2)
        layout.add_widget(Divider(), 2)
        layout.add_widget(Text("Patch:", "patch", on_change=self._on_change), 2)
        layout.add_widget(Divider(), 2)
        self.output = TextBox(Widget.FILL_FRAME, "Output:", "output", readonly=True, line_wrap=True)
        layout.add_widget(self.output, 2)

        layout.add_widget(VerticalDivider(), 3)

        self.ports = TextBox(Widget.FILL_FRAME, "Devices:", "ports", readonly=True, line_wrap=True)
        layout.add_widget(self.ports, 4)

        divider = Layout([1])
        self.add_layout(divider)
        divider.add_widget(Divider())

        bottom = Layout([1, 1, 1, 1])
        self.add_layout(bottom)
        bottom.add_widget(Button("Burn eFuses!", self._go), 0)
        bottom.add_widget(Button("Quit", self._quit), 3)

        self.set_theme("monochrome2")
        self.fix()

        self._on_change()

    def _get_binary(self):
        self.save()
        if self.data.get("features_0") is None:
            return
        flags = ["0"] * 14 + [
            f"{int(self.data['major']):06b}"[:6],
            f"{int(self.data['minor']):06b}"[:6],
            f"{int(self.data['patch']):06b}"[:6],
        ]
        for feature in HW_FEATURES:
            flags[HW_FEATURES_FLAG_BASE - feature["bit_no"]] = self.data["features_%s" % feature["bit_no"]] and "1" or "0"
        return "".join(flags)

    def _on_change(self):
        self.save()
        if self.data.get("features_0") is None:
            return
        try:
            binary = list(self._get_binary())
            uint32 = int("".join(binary), 2)
            binary.insert(24, " ")
            binary.insert(16, " ")
            binary.insert(8, " ")
            output = [
                "Data to be written:",
                "".join(binary),
                f"or in uint32_t form: {uint32}",
            ]
        except Exception as e:
            output = [str(e)]
        self.output.value = output
        self.output.reset()
        self.screen.force_update(True)

    def _go(self):
        self.save()
        self._scene.add_effect(
            PopUpDialog(self._screen, "Are you sure?", ["No...", "YESSS"], has_shadow=True, on_close=self._confirm_burn)
        )

    def _confirm_burn(self, choice_idx):
        global do_check_ports
        if choice_idx == 0:
            # No...
            return

        do_check_ports = False
        os.makedirs(TMP_DIR, exist_ok=True)

        data = int(self._get_binary(), 2).to_bytes(4, "little")
        ports = []
        with tempfile.NamedTemporaryFile(dir=TMP_DIR, suffix=".bin") as f:
            f.write(data)
            f.flush()
            # espefuse -p PORT burn_block_data --offset 28 BLOCK3 data.bin
            for port in serial.tools.list_ports.comports():
                try:
                    with HidePrint():
                        esptool.get_default_connected_device([port.device], None, 1, 115200, chip="esp32").read_mac()
                except Exception:
                    continue
                try:
                    with HidePrint():
                        espefuse.main(
                            [
                                "-p",
                                port.device,
                                "burn_block_data",
                                "--offset",
                                str(32 - 4),
                                "--force-write-always",
                                "--do-not-confirm",
                                "BLOCK3",
                                f.name,
                            ]
                        )
                    ports.append(f"Burned {port.device}!")
                except Exception as e:
                    ports.append(f"{port.device} error {e}")
                self.ports.value = ports
                self.ports.reset()
                self.screen.force_update(True)
                self.screen.draw_next_frame()
        ports.append("Done.")
        self.ports.value = ports
        self.ports.reset()
        self.screen.force_update(True)
        self.screen.draw_next_frame()

    @staticmethod
    def _quit():
        sys.exit(0)


async def check_ports(efuser_view):
    while do_check_ports:
        ports = []
        for port in serial.tools.list_ports.comports():
            try:
                with HidePrint():
                    mac = esptool.get_default_connected_device([port.device], None, 1, 115200, chip="esp32").read_mac()
            except Exception:
                pass
            else:
                ports.append("%s: %s" % (port.device, bytes(mac).hex().rjust(12, "0")))
            await asyncio.sleep(0.1)
        if not ports:
            ports = ["No ESP32 devices detected!"]
        efuser_view.ports.value = ports
        efuser_view.ports.reset()
        efuser_view.screen.force_update(True)
        efuser_view.screen.draw_next_frame()
        await asyncio.sleep(3)


async def screen_loop(screen):
    efuser_view = EfuserView(screen)
    screen.set_scenes([Scene([efuser_view], -1, name="Main")])
    asyncio.create_task(check_ports(efuser_view))
    while True:
        efuser_view.output.reset()
        screen.draw_next_frame()
        await asyncio.sleep(0.02)


def efusizer_ui(screen):
    asyncio.run(screen_loop(screen))


@click.command()
def main():
    Screen.wrapper(efusizer_ui)


def run_efuser():
    main()


if __name__ == "__main__":
    run_efuser()
