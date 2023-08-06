SocialLoginInformation = {
    "Google": {
        "name": "Google",
        "valid_login_urls": ["https://accounts.google.com/"],
        "must_have_texts_in_valid_login_urls": [["client_id"]],
        "exclude_url_starts_with": ["accounts.google.", "account.google.", "google.", "developers.googleblog.com",
                                    "pki.goog", "support.google.", "patent.google.", "www.google.", "translate.google.",
                                    "maps.google.", "trends.google.", "adwords.google.", "picasa.google.",
                                    "books.google.", "edu.google.", "developers.google.", "mymaps.google.",
                                    "workspace.google.", "gsuite.google.", "mijnaccount.google.", "scholar.google."],
        "extra_texts": ["ورود با حساب گوگل"]
    },
    "Facebook": {
        "name": "Facebook",
        "valid_login_urls": ["https://m.facebook.com/login", "https://facebook.com/login",
                             "https://www.facebook.com/login"],
        "must_have_texts_in_valid_login_urls": [["client_id", "app_id"]],
        "exclude_url_starts_with": ["facebook.", "www.facebook.", "connect.facebook.", "developers.facebook."],
        "extra_texts": []
    },
    "Apple": {
        "name": "Apple",
        "valid_login_urls": ["https://appleid.apple.com/"],
        "must_have_texts_in_valid_login_urls": [["client_id"]],
        "exclude_url_starts_with": ["apple.", "appleid.apple.", "secure.apple.", "secure2.apple.",
                                    "secure2.store.apple.", "support.apple.", "music.apple.", "discussions.apple.",
                                    "www.apple.", "business.apple."],
        "extra_texts": []
    }
}
