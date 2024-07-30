"""display data"""

import json
from..templates import template
from .. import styles
import requests
import reflex as rx

def get_AML_guidelines():
    x = requests.get("http://127.0.0.1:8000/AML_guidelines/")
    return json.loads(x.text)['content']

def get_KYC_guidelines():
    x = requests.get("http://127.0.0.1:8000/KYC_guidelines/")
    return json.loads(x.text)['content']

@template(route="/data",title="RBI Guidelines")
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
                                        rx.markdown(get_AML_guidelines()),
                                    ),
                                        rx.box(
                                        rx.text_area(placeholder="Enter text here...", style=styles.text_area_style),

                                        rx.flex(
                                            rx.button("Save", style=styles.overlapping_button_style),
                                            direction="column",
                                        ),
                                    ),
                                    
                                    direction="row",
                                    spacing="4",
                                ),
                                value="tab1",
                            ),
                            rx.tabs.content(
                                rx.flex(
                                        rx.box(
                                        rx.markdown(get_KYC_guidelines()),
                                    ),
                                        rx.box(
                                        rx.text_area(placeholder="Enter text here...", style=styles.text_area_style),
                                        rx.flex(
                                            rx.button("Save", style=styles.overlapping_button_style),
                                            direction="column",
                                        ),
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
                            rx.button("Download", style=styles.overlapping_button_style),
                            direction="column",
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