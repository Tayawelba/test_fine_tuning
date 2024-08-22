import csv
import datetime
from slugify import slugify

def convert_date(date_str):
    try:
        return datetime.datetime.strptime(date_str, "%d %b %Y").strftime("%d/%m/%Y")
    except ValueError:
        return date_str

def create_slug(title):
    return slugify(title)

def convert_csv(input_file, output_file):
    with open(input_file, mode='r', encoding='utf-8') as infile, open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
        reader = csv.DictReader(infile, delimiter=';')
        fieldnames = ["csv_post_title", "csv_post_post", "csv_post_categories", "csv_post_date", "csv_post_author", "csv_post_slug", "csv_post_type", "csv_post_parent"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=';')

        writer.writeheader()

        for row in reader:
            new_row = {
                "csv_post_title": row["title"],
                "csv_post_post": row["content"],
                "csv_post_categories": row["category"],
                "csv_post_date": convert_date(row["date"]),
                "csv_post_author": row["author"],
                "csv_post_slug": create_slug(row["title"]),
                "csv_post_type": "post",  # assuming the post type is always "post"
                "csv_post_parent": ""  # assuming there's no parent post
            }
            writer.writerow(new_row)

input_file = 'articles2.csv'  # replace with your input CSV file path
output_file = 'output.csv'  # replace with your output CSV file path

convert_csv(input_file, output_file)
