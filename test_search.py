from scraper import search_apps

apps = search_apps("Instagram Lite")
if apps.empty:
    print("No results found")
else:
    print(apps[
        [
            "rank",
            "title",
            "appId",
            "confidence",
            "confidence_level",
            "recovery_method"
        ]
    ])