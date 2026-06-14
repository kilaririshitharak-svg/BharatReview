from scraper import search_apps, fetch_reviews_for_app, resolve_app_id_from_url_or_name

user_input = input("Enter app name or Google Play URL: ").strip()

# URL path
app_id, mode = resolve_app_id_from_url_or_name(user_input)

if mode == "url":
    if not app_id:
        print("Could not extract app id from URL.")
    else:
        print("URL mode detected.")
        print("App ID:", app_id)

        reviews_df = fetch_reviews_for_app(app_id, max_reviews=200)
        print("\nREVIEWS SHAPE:", reviews_df.shape)
        print(reviews_df.head())

# App-name search path
elif mode == "search":
    apps_df = search_apps(user_input, max_results=5)

    if apps_df.empty:
        print("No matching apps found.")
    else:
        print("\nTop matches:")
        print(apps_df[["rank", "title", "appId", "developer", "score", "installs", "has_app_id"]].to_string(index=False))

        # only allow valid appId rows
        valid_apps = apps_df[apps_df["has_app_id"] == True].copy()

        if valid_apps.empty:
            print("\nNo valid appId found in the search results.")
            print("Please use the Google Play URL for the exact app.")
        else:
            choice = int(input("\nEnter the rank number of the correct app: ").strip())

            selected_row = valid_apps.loc[valid_apps["rank"] == choice]

            if selected_row.empty:
                print("Invalid selection, or selected app has no usable appId.")
            else:
                selected_row = selected_row.iloc[0]
                app_id = selected_row["appId"]

                print("\nSelected app:", selected_row["title"])
                print("App ID:", app_id)

                reviews_df = fetch_reviews_for_app(app_id, max_reviews=200)
                print("\nREVIEWS SHAPE:", reviews_df.shape)
                print(reviews_df.head())

else:
    print("Empty input.")