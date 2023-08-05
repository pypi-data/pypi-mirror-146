from __future__ import annotations

from rich.console import ConsoleOptions, Console, RenderResult
from rich.style import StyleType
from rich.text import Text


class UnderlineBar:
    """Thin horizontal bar with a portion highlighted.

    Args:
        highlight_range (tuple[float, float]): The range to highlight. Defaults to ``(0, 0)`` (no highlight)
        highlight_style (StyleType): The style of the highlighted range of the bar.
        background_style (StyleType): The style of the non-highlighted range(s) of the bar.
        width (int, optional): The width of the bar, or ``None`` to fill available width.
    """

    def __init__(
        self,
        highlight_range: tuple[float, float] = (0, 0),
        highlight_style: StyleType = "magenta",
        background_style: StyleType = "grey37",
        clickable_ranges: dict[str, tuple[int, int]] | None = None,
        width: int | None = None,
    ) -> None:
        self.highlight_range = highlight_range
        self.highlight_style = highlight_style
        self.background_style = background_style
        self.clickable_ranges = clickable_ranges or {}
        self.width = width

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        highlight_style = console.get_style(self.highlight_style)
        background_style = console.get_style(self.background_style)

        half_bar_right = "╸"
        half_bar_left = "╺"
        bar = "━"

        width = self.width or options.max_width
        start, end = self.highlight_range

        start = max(start, 0)
        end = min(end, width)

        output_bar = Text("", end="")

        if start == end == 0 or end < 0 or start > end:
            output_bar.append(Text(bar * width, style=background_style, end=""))
            yield output_bar
            return

        # Round start and end to nearest half
        start = round(start * 2) / 2
        end = round(end * 2) / 2

        # Check if we start/end on a number that rounds to a .5
        half_start = start - int(start) > 0
        half_end = end - int(end) > 0

        # Initial non-highlighted portion of bar
        output_bar.append(
            Text(bar * (int(start - 0.5)), style=background_style, end="")
        )
        if not half_start and start > 0:
            output_bar.append(Text(half_bar_right, style=background_style, end=""))

        # The highlighted portion
        bar_width = int(end) - int(start)
        if half_start:
            output_bar.append(
                Text(
                    half_bar_left + bar * (bar_width - 1), style=highlight_style, end=""
                )
            )
        else:
            output_bar.append(Text(bar * bar_width, style=highlight_style, end=""))
        if half_end:
            output_bar.append(Text(half_bar_right, style=highlight_style, end=""))

        # The non-highlighted tail
        if not half_end and end - width != 0:
            output_bar.append(Text(half_bar_left, style=background_style, end=""))
        output_bar.append(
            Text(bar * (int(width) - int(end) - 1), style=background_style, end="")
        )

        # Fire actions when certain ranges are clicked (e.g. for tabs)
        for range_name, (start, end) in self.clickable_ranges.items():
            output_bar.apply_meta(
                {"@click": f"range_clicked('{range_name}')"}, start, end
            )

        yield output_bar
