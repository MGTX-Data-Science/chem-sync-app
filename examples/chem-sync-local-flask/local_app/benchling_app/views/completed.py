from benchling_sdk.apps.canvas.framework import CanvasBuilder
from benchling_sdk.apps.canvas.types import UiBlock
from benchling_sdk.apps.status.framework import SessionContextManager
from benchling_sdk.apps.status.helpers import ref
from benchling_sdk.models import (
    AppSessionMessageCreate,
    AppSessionMessageStyle,
    AppSessionUpdateStatus,
    MarkdownUiBlock,
    MarkdownUiBlockType,
    Molecule,
)


def render_completed_canvas(
    molecule: Molecule,
    canvas_id: str,
    canvas_builder: CanvasBuilder,
    session: SessionContextManager,
    already_registered: bool = False,  # <-- new optional flag
) -> None:
    canvas_builder = canvas_builder.with_blocks(_completed_blocks(already_registered))
    session.app.benchling.apps.update_canvas(
        canvas_id,
        canvas_builder.with_enabled().to_update(),
    )

    messages = []
    if already_registered:
        messages.append(
            AppSessionMessageCreate(
                f"The molecule {ref(molecule)} is already registered in Benchling.",
                style=AppSessionMessageStyle.INFO,
            )
        )
    else:
        messages.append(
            AppSessionMessageCreate(
                f"Created the molecule {ref(molecule)} in Benchling!",
                style=AppSessionMessageStyle.SUCCESS,
            )
        )

    session.close_session(
        AppSessionUpdateStatus.SUCCEEDED,
        messages=messages,
    )



def _completed_blocks(already_registered: bool = False) -> list[UiBlock]:
    message = (
        "The molecule was already registered in Benchling."
        if already_registered
        else "The chemical has been synced into Benchling! Please follow procedures for next steps."
    )
    return [
        MarkdownUiBlock(
            id="completed",
            type=MarkdownUiBlockType.MARKDOWN,
            value=message,
        ),
    ]

