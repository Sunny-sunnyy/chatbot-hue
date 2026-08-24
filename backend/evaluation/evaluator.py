from pathlib import Path

import gradio as gr

from evaluation.eval import (
    ANSWER_COLUMNS,
    ANSWER_RESULTS_FILE,
    RETRIEVAL_COLUMNS,
    RETRIEVAL_RESULTS_FILE,
    run_answer_batch,
    run_retrieval_batch,
)
from evaluation.test import DEFAULT_TEST_FILE


def summary_text(title: str, summary: dict, result_path: str | Path) -> str:
    lines = [f"## {title}"]
    lines.extend(f"- {key}: {value}" for key, value in summary.items())
    lines.append(f"- File kết quả: `{result_path}`")
    return "\n".join(lines)


def format_table(rows: list[dict], columns: list[str]) -> dict:
    data = [[row.get(col, "") for col in columns] for row in rows]
    return {"headers": columns, "data": data}


def run_retrieval_ui(test_path, concurrency, progress=gr.Progress()):
    rows, summary = run_retrieval_batch(test_path, concurrency, "dense_only")
    table = format_table(rows, RETRIEVAL_COLUMNS)
    return summary_text("Kết quả retrieval", summary, RETRIEVAL_RESULTS_FILE), table


async def run_answer_ui(test_path, concurrency, progress=gr.Progress()):
    rows, summary = await run_answer_batch(
        test_path, concurrency, "dense_only", progress
    )
    table = format_table(rows, ANSWER_COLUMNS)
    return summary_text("Kết quả câu trả lời", summary, ANSWER_RESULTS_FILE), table


def build_app():
    with gr.Blocks(title="Đánh giá Hue RAG") as app:
        gr.Markdown("# Đánh giá Hue RAG")
        test_path = gr.Textbox(
            value=str(DEFAULT_TEST_FILE), label="File câu hỏi"
        )
        concurrency = gr.Slider(
            minimum=1,
            maximum=10,
            value=3,
            step=1,
            label="Số câu chạy cùng lúc",
        )
        with gr.Row():
            retrieval_button = gr.Button("Đánh giá retrieval")
            answer_button = gr.Button("Đánh giá câu trả lời")
        summary = gr.Markdown()
        results = gr.Dataframe(interactive=False, wrap=True)
        retrieval_button.click(
            run_retrieval_ui, [test_path, concurrency], [summary, results]
        )
        answer_button.click(
            run_answer_ui, [test_path, concurrency], [summary, results]
        )
    return app


def main():
    build_app().launch(inbrowser=True)


if __name__ == "__main__":
    main()
