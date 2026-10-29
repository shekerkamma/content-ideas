from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest
pytest.importorskip("pptx.util")
pptx = pytest.importorskip(
    "pptx", reason="python-pptx is an opt-in skill dependency (see the skill's requirements.txt)"
)
Presentation = pptx.Presentation
Inches, Pt = pptx.util.Inches, pptx.util.Pt


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "pptx_toolkit.py"
SPEC = importlib.util.spec_from_file_location("pptx_toolkit", MODULE_PATH)
assert SPEC and SPEC.loader
toolkit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(toolkit)


def make_deck(path: Path) -> Path:
    prs = Presentation()
    while prs.slides:
        slide_id = prs.slides._sldIdLst[-1]
        prs.part.drop_rel(slide_id.rId)
        del prs.slides._sldIdLst[-1]
    for number in range(1, 4):
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        box = slide.shapes.add_textbox(Inches(1), Inches(1), Inches(5), Inches(1))
        run = box.text_frame.paragraphs[0].add_run()
        run.text = f"Slide {number}"
        run.font.bold = True
        run.font.size = Pt(24)
    prs.slides[1].notes_slide.notes_text_frame.text = "Original note"
    prs.save(path)
    return path


def test_inspect_records_shapes_and_native_notes(tmp_path: Path) -> None:
    source = make_deck(tmp_path / "source.pptx")

    inventory = toolkit.inspect_pptx(source)

    assert inventory["slide_count"] == 3
    assert inventory["slides"][1]["notes"] == "Original note"
    assert inventory["slides"][0]["shapes"][0]["text"] == "Slide 1"
    assert inventory["slides"][0]["shapes"][0]["paragraphs"][0]["runs"][0]["bold"] is True


def test_edit_replaces_shape_text_preserves_first_run_style_and_updates_notes(tmp_path: Path) -> None:
    source = make_deck(tmp_path / "source.pptx")
    shape_id = Presentation(source).slides[0].shapes[0].shape_id
    output = tmp_path / "edited.pptx"

    result = toolkit.edit_pptx(
        source,
        output,
        {
            "slides": [
                {
                    "slide": 1,
                    "replacements": [{"shape_id": shape_id, "text": "Updated title"}],
                    "notes": "Updated note",
                }
            ]
        },
    )

    edited = Presentation(output)
    run = edited.slides[0].shapes[0].text_frame.paragraphs[0].runs[0]
    assert run.text == "Updated title"
    assert run.font.bold is True
    assert run.font.size.pt == 24
    assert edited.slides[0].notes_slide.notes_text_frame.text == "Updated note"
    assert result["shapes_replaced"] == 1
    assert toolkit.validate_pptx(output) == []


def test_reorder_can_remove_omitted_slides(tmp_path: Path) -> None:
    source = make_deck(tmp_path / "source.pptx")
    output = tmp_path / "reordered.pptx"

    result = toolkit.reorder_pptx(source, output, [3, 1])

    reordered = Presentation(output)
    assert [slide.shapes[0].text for slide in reordered.slides] == ["Slide 3", "Slide 1"]
    assert result["removed"] == 1
    assert toolkit.validate_pptx(output) == []


def test_reorder_rejects_slide_duplication(tmp_path: Path) -> None:
    source = make_deck(tmp_path / "source.pptx")

    with pytest.raises(toolkit.ToolkitError, match="duplication is unsupported"):
        toolkit.reorder_pptx(source, tmp_path / "bad.pptx", [1, 1])


def test_unpack_pack_round_trip(tmp_path: Path) -> None:
    source = make_deck(tmp_path / "source.pptx")
    unpacked = tmp_path / "unpacked"
    rebuilt = tmp_path / "rebuilt.pptx"

    unpack_result = toolkit.unpack_pptx(source, unpacked)
    pack_result = toolkit.pack_pptx(unpacked, rebuilt)

    assert unpack_result["files_extracted"] > 0
    assert pack_result["files_packed"] > 0
    assert toolkit.validate_pptx(rebuilt) == []
    assert len(Presentation(rebuilt).slides) == 3
