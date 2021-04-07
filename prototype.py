import yaml
import urllib
import datetime
from smw_utils.api import MediawikiApi


def get_property(page, property_label):
    for prop in page["properties"]:
        if prop["property"]["label"] == property_label:
            if "label" in prop:
                return prop["label"]
            else:
                return prop["value"]
    return ""


def get_funding_pages():
    with open("config.yml") as f:
        config = yaml.load(f, Loader=yaml.BaseLoader)

    api = MediawikiApi(
        config["url"],
        config["api"],
        config["lgname"],
        config["lgpassword"],
        verbose=True
    )

    page_titles = api.fetch_category("Funding")
    

    content = "# Fördermöglichkeiten"

    pages = []
    for page_title in page_titles:
        page_data = api.fetch_page(page_title)
        pages.append(page_data)

    content += f"\n\n* Stand: {datetime.datetime.now().isoformat()[:10]}"
    content += f"\n\n## Aktuelle Ausschreibungen\n"

    pages = sorted(pages, key=lambda x: get_property(x, "Has deadline"))

    for page_data in pages:
        deadline = get_property(page_data, "Has deadline")
        title = page_data["title"]
        content += f"\n* [{deadline} - {title}](#{title})"

    for page_data in pages:
        content += f"\n\n## {page_title}\n\n"
        deadline = get_property(page_data, "Has deadline")
        institution = get_property(page_data, "Has funding institution")
        homepage = get_property(page_data, "Has homepage")

        content += f"* Nächste Einreichung: {deadline}"
        content += f"\n* Institution: {institution}"

        free_text = page_data["free_text"]
        content += f"\n\n{free_text}"

        if homepage:
            content += f"\n\n* [Link]({homepage})"

    with open("index.md", "w") as f:
        f.write(content)

if __name__ == "__main__":
    get_funding_pages()