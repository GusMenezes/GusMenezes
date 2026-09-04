from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

WIDTH = 1200
HEIGHT = 630
BACKGROUND = "#090E14"
SURFACE = "#101820"
BORDER = "#24313D"
TEXT = "#D7E2EA"
MUTED = "#78909C"
CYAN = "#22D3EE"
GREEN = "#34D399"
YELLOW = "#FBBF24"
RED = "#FB7185"

LINES = [
    ("gustavo@github", " ~ $ ", "whoami"),
    ("", "", "Gustavo Alves — Full-stack Developer"),
    ("gustavo@github", " ~ $ ", "focus"),
    ("", "", "SaaS · automações · produtos com IA"),
    ("gustavo@github", " ~ $ ", "stack --active"),
    ("", "", "TypeScript · React · Next.js · Tailwind CSS"),
    ("", "", "PHP · Laravel · PostgreSQL · MongoDB · Redis"),
    ("", "", "Docker · AWS · Git · Bun"),
    ("gustavo@github", " ~ $ ", "status"),
    ("", "", "building reliable software_"),
]


def load_font(size: int):
    candidates = [
        "/System/Library/Fonts/SFNSMono.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def draw_frame(visible_characters: int, show_cursor: bool):
    image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((24, 24, WIDTH - 24, HEIGHT - 24), 18, fill=SURFACE, outline=BORDER, width=2)
    draw.rounded_rectangle((24, 24, WIDTH - 24, 90), 18, fill="#141F29")
    draw.rectangle((24, 72, WIDTH - 24, 90), fill="#141F29")

    for x, color in ((62, RED), (98, YELLOW), (134, GREEN)):
        draw.ellipse((x - 10, 47, x + 10, 67), fill=color)

    title_font = load_font(21)
    body_font = load_font(28)
    draw.text((WIDTH / 2, 57), "gustavo@github — profile", font=title_font, fill=MUTED, anchor="mm")

    remaining = visible_characters
    y = 128
    for user, prompt, content in LINES:
        shown = content[: max(0, min(len(content), remaining))]
        remaining -= len(content)

        if user:
            draw.text((62, y), user, font=body_font, fill=GREEN)
            user_width = draw.textlength(user, font=body_font)
            draw.text((62 + user_width, y), prompt, font=body_font, fill=CYAN)
            prompt_width = draw.textlength(prompt, font=body_font)
            draw.text((62 + user_width + prompt_width, y), shown, font=body_font, fill=TEXT)
        else:
            draw.text((62, y), shown, font=body_font, fill=TEXT)

        if remaining <= 0:
            if show_cursor:
                cursor_x = 62 + draw.textlength(shown, font=body_font)
                if user:
                    cursor_x += draw.textlength(user + prompt, font=body_font)
                draw.rectangle((cursor_x + 2, y + 5, cursor_x + 16, y + 34), fill=CYAN)
            break

        y += 46

    return image


def main():
    output = Path(__file__).resolve().parents[1] / "assets" / "terminal.gif"
    output.parent.mkdir(parents=True, exist_ok=True)
    total_characters = sum(len(content) for _, _, content in LINES)
    steps = list(range(0, total_characters + 1, 3))
    frames = [draw_frame(step, step % 12 < 8) for step in steps]
    frames.extend(draw_frame(total_characters, index % 2 == 0) for index in range(12))
    frames[0].save(
        output,
        save_all=True,
        append_images=frames[1:],
        duration=85,
        loop=0,
        optimize=True,
        disposal=2,
    )


if __name__ == "__main__":
    main()
