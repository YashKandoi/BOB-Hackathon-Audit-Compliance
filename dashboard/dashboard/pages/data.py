"""display data"""

from..templates import template
from .. import styles

import reflex as rx

def read_text_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

@template(route="/data",title="data")
def data()->rx.Component:
    return rx.box(
            rx.flex(
                rx.box(
                    rx.heading("RBI GUIDELINES", as_="h1"),
                ),
                rx.box(
                    rx.flex(
                        rx.box(
                            rx.tabs.root(
                            rx.tabs.list(
                            rx.tabs.trigger("AML", value="tab1"),
                            rx.tabs.trigger("KYC", value="tab2"),
                            ),
                            rx.tabs.content(
                                    rx.flex(
                                        rx.box(
                                        rx.text(read_text_file("testing.txt")),
                                    ),
                                        rx.box(
                                        rx.text_area(placeholder="Enter text here...", style=styles.text_area_style),
                                    ),
                                    
                                    direction="row",
                                    spacing="4",
                                ),
                                value="tab1",
                            ),
                            rx.tabs.content(
                                rx.flex(
                                        rx.box(
                                        rx.text(read_text_file("testing.txt")),
                                    ),
                                        rx.box(
                                        rx.text_area(placeholder="Enter text here...", style=styles.text_area_style),
                                    ),
                                    
                                    direction="row",
                                    spacing="4",
                                ),
                                value="tab2",
                            ),
                            default_value="tab1",
                            spacing='4',
                            width="100%" 
                        ),
                            width="100%"
                        ),
                        rx.box(
                            rx.flex(
                                rx.button("Save", style=styles.overlapping_button_style),
                                rx.button("Download", style=styles.overlapping_button_style),
                                spacing="4",
                            ),
                            width="100%",
                        ),
                    direction="column",
                    ),
                    width="100%"
                ),
                direction="column",
                width="100%",
            )
        
        )