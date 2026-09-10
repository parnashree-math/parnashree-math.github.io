"""
teaching.py
-----------
Generates one Jekyll collection file per row of teaching.csv, for the
`_teaching/` collection used by the academicpages template.

Usage:
    Place this script and teaching.csv together in the markdown_generator/
    folder of your academicpages repo (that's where the equivalent
    publications/talks scripts already live), then from inside that folder run:

        python teaching.py

    It writes one markdown file per CSV row into ../_teaching/, named
    YYYY-MM-DD-url_slug.md, matching the naming convention the rest of
    the template's collections use.

CSV columns expected (header row required):
    title, type, url_slug, venue, date, location, description

    - title, url_slug, date are required for every row.
    - type, venue, location, description may be left blank.
    - date must be YYYY-MM-DD (use the 1st of the month if you only
      know the month/year).
"""

import os
import pandas as pd


def yaml_single_quote(value):
    """Wrap `value` as a single-quoted YAML scalar, doubling any
    embedded single quotes as YAML requires. Single-quoted strings
    don't need backslash-escaping, which keeps this safe for titles
    containing colons, parentheses, etc."""
    return "'" + str(value).replace("'", "''") + "'"


def build_markdown(item):
    date = str(item["date"]).strip()
    url_slug = str(item["url_slug"]).strip()

    lines = ["---"]
    lines.append(f"title: {yaml_single_quote(item['title'])}")
    lines.append("collection: teaching")

    type_value = str(item.get("type", "")).strip()
    lines.append(f"type: {yaml_single_quote(type_value if type_value else 'Course')}")

    lines.append(f"permalink: /teaching/{date}-{url_slug}")

    venue = str(item.get("venue", "")).strip()
    if venue and venue.lower() != "nan":
        lines.append(f"venue: {yaml_single_quote(venue)}")

    if date and date.lower() != "nan":
        lines.append(f"date: {date}")

    location = str(item.get("location", "")).strip()
    if location and location.lower() != "nan":
        lines.append(f"location: {yaml_single_quote(location)}")

    lines.append("---")

    body = str(item.get("description", "")).strip()
    content = "\n".join(lines)
    if body and body.lower() != "nan":
        content += "\n" + body + "\n"

    return content


def main():
    teaching = pd.read_csv("teaching.csv", sep=",", encoding="utf-8")
    teaching = teaching.fillna("")

    output_dir = "../_teaching"
    os.makedirs(output_dir, exist_ok=True)

    for _, item in teaching.iterrows():
        date = str(item["date"]).strip()
        url_slug = str(item["url_slug"]).strip()
        md_filename = f"{date}-{url_slug}.md"
        filepath = os.path.join(output_dir, md_filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(build_markdown(item))

        print(f"Wrote {filepath}")

    print(f"\nDone -- generated {len(teaching)} files in {output_dir}/")


if __name__ == "__main__":
    main()
