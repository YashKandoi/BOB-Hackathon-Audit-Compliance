"""The overview page of the app."""

import reflex as rx
from .. import styles
from ..templates import template
from ..views.stats_cards import stats_cards
from ..views.charts import (
    users_chart,
    revenue_chart,
    orders_chart,
    area_toggle,
    pie_chart,
    timeframe_select,
    StatsState,
)
from ..views.adquisition_view import adquisition
from ..components.notification import notification
from ..components.card import card
from .profile import ProfileState
import datetime


def tab_content_header() -> rx.Component:
    return rx.hstack(
        area_toggle(),
        align="center",
        width="100%",
        spacing="4",
    )


@template(route="/", title="Overview", on_load=StatsState.randomize_data)
def index() -> rx.Component:
    """The overview page.

    Returns:
        The UI for the overview page.
    """
    return rx.vstack(
        rx.heading(f"Welcome, {ProfileState.profile.name}", size="5"),
        
        stats_cards(),
        
        rx.grid(
            card(
                rx.hstack(
                    rx.hstack(
                        rx.icon("user-round-search", size=20),
                        rx.text("Visitors Analytics", size="4", weight="medium"),
                        align="center",
                        spacing="2",
                    ),
                    timeframe_select(),
                    align="center",
                    width="100%",
                    justify="between",
                ),
                pie_chart(),
            ),
            card(
                rx.hstack(
                    rx.icon("globe", size=20),
                    rx.text("Acquisition Overview", size="4", weight="medium"),
                    align="center",
                    spacing="2",
                    margin_bottom="2.5em",
                ),
                rx.vstack(
                    adquisition(),
                ),
            ),
            gap="1rem",
            grid_template_columns=[
                "1fr",
                "repeat(1, 1fr)",
                "repeat(2, 1fr)",
                "repeat(2, 1fr)",
                "repeat(2, 1fr)",
            ],
            width="100%",
        ),
        spacing="8",
        width="100%",
    )
