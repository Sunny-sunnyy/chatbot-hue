# Design: Curate Cơm hến

## Scope

Create the curated knowledge-base entry at
`knowledge-base-hue/foods/local_specialties/com hen.md`.

The entry will represent Cơm hến as a Huế local specialty. It will use the
user-provided material as the primary content source and the existing curated
restaurant entries only for addresses of three representative locations.

## Content structure

The Markdown file will contain only sections supported by the supplied data:

- `# Cơm hến`
- `## Tóm tắt`
- `## Thành phần và đặc điểm`
- `## Cách làm tóm tắt`
- `## Nguồn gốc và bối cảnh`
- `## Các biến thể liên quan`
- `## Cách thưởng thức`
- `## Địa điểm tiêu biểu`
- `## Nguồn dữ liệu`

The location table will include Cơm hến Bà Cam, Cơm hến Hoa Đông and Cơm hến
17 Hàn Mặc Tử with addresses taken from their existing curated entries. Prices
and opening hours will remain in those location entries to avoid duplication.

## Editorial policy

- Keep the body natural and answer-facing in Vietnamese.
- Remove SEO keyword strings, promotional phrasing and unnecessary repetition.
- Preserve uncertainty for oral-history claims with wording such as
  “tương truyền”.
- Include bún hến and mì hến as related variations, without treating them as
  separate entities.
- Do not add unsupported ingredients, history, nutrition claims or factual
  details.
- Use `Khám phá Huế` as the primary source in `## Nguồn dữ liệu`; mention the
  restaurant information source used for the location addresses.
- Do not add YAML frontmatter or a `Liên kết nội bộ` section.

## Validation

- File starts with `# Cơm hến` and contains no YAML frontmatter.
- Required sections contain only supplied or already-curated data.
- The three location names and addresses match the existing restaurant files.
- No SEO keyword block, placeholder text or unsupported empty section remains.
- Run `git diff --check` on the changed Markdown file.
