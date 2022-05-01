import requests, re, json, os, threading
from bs4 import BeautifulSoup
from pprint import pprint

final, download = [
    dict(
        zip(
            [
                "image_url",
                "id",
                "name",
                "base_production",
                "version_added",
                "year_added",
            ],
            i,
        )
    )
    for i in [
        [i[0], int(i[1])]
        + i[2:4]
        + [i[4].split("(")[0].strip(), int(i[4].split("(")[1].replace(")", ""))]
        for i in [
            [
                "/".join(
                    re.findall(r'src="(https:\/\/.*?)"', str(i[0].find("img")))[
                        0
                    ].split("/")[:8]
                )
            ]
            + [
                [
                    i.strip()
                    for i in str(j)
                    .replace("\n", "")
                    .replace("<td>", "")
                    .replace("</td>", "")
                    .split("<br/>")
                ]
                if "<br/>" in str(j)
                else j.text.strip()
                if j.text.strip() != ""
                else None
                for j in i[1:]
            ]
            for i in [
                [j for j in i.findAll("td")]
                for i in BeautifulSoup(
                    requests.get(
                        "https://official-scrap-2.fandom.com/wiki/Barrels"
                    ).content,
                    "lxml",
                )
                .find("table", {"class": "article-table"})
                .findAll("tr")[1:]
            ]
        ]
    ]
], lambda url: open("barrels/" + url.split("/")[-1], "wb").write(
    requests.get(url).content
) if not os.path.exists(
    "barrels/" + url.split("/")[-1]
) else 0
os.mkdir("barrels") if not os.path.exists("barrels") else 0
[
    threading.Thread(target=download, args=(i,)).start()
    for i in (i["image_url"] for i in final)
]
json.dump(final, open("barrels_data.json", "w"), indent=4)
