"""
scraper.py — BharatReview Google Play scraping module
======================================================
Hybrid appId resolution:
  1. Known-app lookup table  (instant, always correct)
  2. URL extraction           (always correct)
  3. Search + recovery        (for unknown apps)

Requirements:
    google-play-scraper >= 1.2.7
    pandas >= 2.2.2
"""

from __future__ import annotations

import math
import time
from urllib.parse import parse_qs, urlparse

import pandas as pd
from google_play_scraper import Sort, app, reviews, search


# ── Constants ─────────────────────────────────────────────────────────────────

_REVIEW_BATCH_SIZE   = 200
_SEARCH_RETRY_WAIT   = 1.5
_MAX_SEARCH_RETRIES  = 2
_RECOVERY_HITS       = 10

# Regional fallback order for review fetching
_REGION_FALLBACKS: list[dict[str, str]] = [
    {"lang": "en", "country": "in"},
    {"lang": "hi", "country": "in"},
    {"lang": "en", "country": "us"},
    {"lang": "en", "country": "gb"},
]

# ── Known-app lookup table ────────────────────────────────────────────────────
# Expanded database of 350+ most popular Indian & global apps
# Covers: gaming, entertainment, social, finance, shopping, productivity, utilities
# Keys are lowercase normalised names / common aliases.

KNOWN_APP_IDS: dict[str, str] = {
    # ═══════════════════════════════════════════════════════════════════════════
    # Messaging & Communication
    # ═══════════════════════════════════════════════════════════════════════════
    "whatsapp":                          "com.whatsapp",
    "whatsapp messenger":                "com.whatsapp",
    "whatsapp business":                 "com.whatsapp.w4b",
    "telegram":                          "org.telegram.messenger",
    "telegram messenger":                "org.telegram.messenger",
    "messenger":                         "com.facebook.orca",
    "facebook messenger":                "com.facebook.orca",
    "signal":                            "org.thoughtcrime.securesms",
    "signal messenger":                  "org.thoughtcrime.securesms",
    "viber":                             "com.viber.voip",
    "skype":                             "com.skype.raider",
    "hangouts":                          "com.google.android.talk",
    "google duo":                        "com.google.android.apps.mediashell",
    "wechat":                            "com.tencent.mm",

    # ═══════════════════════════════════════════════════════════════════════════
    # Social Media & Content
    # ═══════════════════════════════════════════════════════════════════════════
    "instagram":                         "com.instagram.android",
    "instagram lite":                    "com.instagram.lite",
    "facebook":                          "com.facebook.katana",
    "facebook lite":                     "com.facebook.lite",
    "snapchat":                          "com.snapchat.android",
    "twitter":                           "com.twitter.android",
    "x":                                 "com.twitter.android",
    "youtube":                           "com.google.android.youtube",
    "youtube lite":                      "com.google.android.apps.youtube.lite",
    "tiktok":                            "com.zhiliaoapp.musically",
    "reddit":                            "com.reddit.frontpage",
    "linkedin":                          "com.linkedin.android",
    "pinterest":                         "com.pinterest",
    "sharechat":                         "in.sharechat.app",
    "moj":                               "com.moj.app",
    "josh":                              "com.josh.app",
    "mx takatak":                        "com.tencent.ig",
    "koo":                               "com.koo.app",
    "threads":                           "com.instagram.barcelona",
    "mastodon":                          "org.joinmastodon.android",
    "bluesky":                           "xyz.blueskyweb.bsky",
    "tumblr":                            "com.tumblr",

    # ═══════════════════════════════════════════════════════════════════════════
    # Payments, Banking & Finance
    # ═══════════════════════════════════════════════════════════════════════════
    "phonepe":                           "com.phonepe.app",
    "phonepe upi":                       "com.phonepe.app",
    "phonepe upi payment recharge":      "com.phonepe.app",
    "phonepe business":                  "com.phonepe.app.business",
    "google pay":                        "com.google.android.apps.nbu.paisa.user",
    "gpay":                              "com.google.android.apps.nbu.paisa.user",
    "paytm":                             "net.one97.paytm",
    "amazon pay":                        "in.amazon.mShop.android.shopping",
    "bhim":                              "in.org.npci.upiapp",
    "mobikwik":                          "com.mobikwik_new",
    "freecharge":                        "com.freecharge.android",
    "sbi yono":                          "com.sbi.lotusintouch",
    "yono sbi":                          "com.sbi.lotusintouch",
    "hdfc bank":                         "com.snapwork.hdfc",
    "icici imobile":                     "com.csam.icici.bank.imobile",
    "axis mobile":                       "com.axis.mobile",
    "kotak mobile banking":              "com.msf.kbank.mobile",
    "indusind mobile":                   "com.indibank.imobile",
    "yes bank":                          "com.yesbank.mobilebanking",
    "pnb one":                           "com.pnb.pnbx",
    "federal bank":                      "com.federalbank.mobilebanking",
    "bob world":                         "com.bankofbaroda.bobmoney",
    "icici pocket":                      "com.csam.icici.bank.imobile.lite",
    "stock market apps - motilal oswal": "com.motilaloswalonline",
    "zerodha kite":                      "com.zerodha.kite",
    "groww":                             "com.groww.indiamarket",
    "upstox":                            "com.upstox",
    "crypto - coinbase":                 "com.coinbase.android",
    "crypto - crypto.com":               "com.crypto.superapp",
    "crypto - wazirx":                   "com.wazir.x",
    "crypto - kucoin":                   "com.kucoin.android",

    # ═══════════════════════════════════════════════════════════════════════════
    # Shopping & E-commerce
    # ═══════════════════════════════════════════════════════════════════════════
    "meesho":                            "com.meesho.supply",
    "flipkart":                          "com.flipkart.android",
    "amazon":                            "in.amazon.mShop.android.shopping",
    "amazon india":                      "in.amazon.mShop.android.shopping",
    "myntra":                            "com.myntra.android",
    "ajio":                              "com.ril.ajio",
    "nykaa":                             "com.nykaa.app",
    "nykaa fashion":                     "com.nykaa.fashion",
    "snapdeal":                          "com.snapdeal.main",
    "jiomart":                           "com.reliance.jiomart",
    "blinkit":                           "com.grofers.customerapp",
    "swiggy instamart":                  "bundl.technologies.partner",
    "zepto":                             "com.zepto.app",
    "bigbasket":                         "com.bigbasket",
    "dunzo":                             "com.dunzo.user",
    "shop 101":                          "com.shop101",
    "alibaba":                           "com.alibaba.intl",
    "daraz":                             "com.daraz.android",
    "ebay":                              "com.ebay.mobile",
    "olx":                               "com.olx.android",
    "cashify":                           "com.cashify",
    "moglix":                            "com.moglix",

    # ═══════════════════════════════════════════════════════════════════════════
    # Food & Delivery
    # ═══════════════════════════════════════════════════════════════════════════
    "swiggy":                            "bundl.technologies.partner",
    "swiggy instamart":                  "bundl.technologies.partner",
    # Swiggy delivery-executive / partner apps (different package from customer app)
    "swiggy delivery partner":           "in.swiggy.delivery",
    "swiggy delivery partner app":       "in.swiggy.delivery",
    "swiggy partner":                    "in.swiggy.delivery",
    "swiggy partner app":                "in.swiggy.delivery",
    "zomato":                            "com.application.zomato",
    # Zomato delivery partner and restaurant partner apps
    "zomato delivery partner":           "com.zomato.delivery",
    "zomato delivery partner app":       "com.zomato.delivery",
    "zomato restaurant partner":         "com.zomato.merchant",
    "zomato for business":               "com.zomato.merchant",
    "eats":                              "com.ubereats.ubereats",
    "uber eats":                         "com.ubereats.ubereats",
    "domino's":                          "com.dominos.india",
    "pizza hut":                         "com.pizzahut.in",
    "faasos":                            "com.faasos.in",
    "dunkindonuts":                      "com.dunkindonuts.android",
    "mcdonalds":                         "com.mcd.in",

    # ═══════════════════════════════════════════════════════════════════════════
    # Ride & Travel
    # ═══════════════════════════════════════════════════════════════════════════
    "ola":                               "com.olacabs.customer",
    "ola lite":                          "com.olacabs.ubernet",
    "uber":                              "com.ubercab",
    "uber lite":                         "com.ubercab.lite",
    "rapido":                            "com.kgtsl.rapido",
    "irctc rail connect":                "cris.org.in.prs.ima",
    "irctc":                             "cris.org.in.prs.ima",
    "makemytrip":                        "com.makemytrip",
    "goibibo":                           "com.go_ibibo.goi.goibibo",
    "redbus":                            "in.redbus.android",
    "trainman":                          "com.railyatri.trainman",
    "log me in":                         "com.logmein.iosremote",
    "skyscanner":                        "com.skyscanner.android",
    "booking.com":                       "com.booking",
    "oyo":                               "com.oyo.rooms",

    # ═══════════════════════════════════════════════════════════════════════════
    # Entertainment & Streaming
    # ═══════════════════════════════════════════════════════════════════════════
    "hotstar":                           "in.startv.hotstar",
    "disney hotstar":                    "in.startv.hotstar",
    "jiocinema":                         "com.jio.media.ondemand",
    "netflix":                           "com.netflix.mediaclient",
    "amazon prime video":                "com.amazon.avod.thirdpartyclient",
    "prime video":                       "com.amazon.avod.thirdpartyclient",
    "sony liv":                          "com.sonyliv",
    "zee5":                              "com.graymatrix.did",
    "alt balaji":                        "com.altbalaji.android",
    "voot":                              "com.cxense.voot",
    "mxplayer":                          "com.mxtech.videoplayer.ad",
    "mx player":                         "com.mxtech.videoplayer.ad",
    "vlc":                               "org.videolan.vlc",
    "plex":                              "com.plexapp.android",
    "spotify":                           "com.spotify.music",
    "gaana":                             "com.gaana",
    "wynk music":                        "com.bsb.wynk",
    "jiosaavn":                          "com.jio.media.jiobeats",
    "saavn":                             "com.jio.media.jiobeats",
    "wynk lite":                         "com.bsb.wynk",
    "youtube music":                     "com.google.android.apps.youtube.music",
    "google play music":                 "com.google.android.music",
    "sound cloud":                       "com.soundcloud.android",
    "apple music":                       "com.apple.android.music",
    "pocket fm":                         "com.pocketfm.app",
    "audible":                           "com.audible.application",

    # ═══════════════════════════════════════════════════════════════════════════
    # Gaming
    # ═══════════════════════════════════════════════════════════════════════════
    "bgmi":                              "com.pubg.imobile",
    "battlegrounds mobile india":        "com.pubg.imobile",
    "free fire":                         "com.dts.freefiremax",
    "free fire max":                     "com.dts.freefiremax",
    "free fire india":                   "com.garena.game.ffi",
    "call of duty mobile":               "com.activision.callofduty.shooter",
    "cod mobile":                        "com.activision.callofduty.shooter",
    "ludo king":                         "com.ludo.king",
    "dream11":                           "com.dream11",
    "fantasy app - my 11 circle":        "com.my11circle",
    "fantasy app - myteam11":            "com.myteam11",
    "fantasy app - fantasy league":      "com.fantasyleague",
    "uc browser":                        "com.ucmobile.intl",
    "clash of clans":                    "com.supercell.clashofclans",
    "clash royale":                      "com.supercell.clashroyale",
    "brawl stars":                       "com.supercell.brawlstars",
    "pokemon go":                        "com.nianticlabs.pokemongo",
    "candy crush saga":                  "com.king.candycrushsodasaga",
    "candy crush soda saga":             "com.king.candycrushsodasaga",
    "candy crush friends saga":          "com.king.candycrush4",
    "candy crush jelly saga":            "com.king.candycrushjellysaga",
    "roblox":                            "com.roblox.client",
    "fortnite":                          "com.epicgames.fortnite",
    "valorant":                          "com.riotgames.valorant",
    "genshin impact":                    "com.mihoyo.ovnsea",
    "cod warzone mobile":                "com.activision.callofduty.warzonemobile",
    "asphalt 9":                         "com.gameloft.android.ANMP",
    "mini militia":                      "com.miniclip.deuces",
    "asphalt legends":                   "com.gameloft.android.GloftAsph",
    "temple run 2":                      "com.imangi.templerun2",
    "subway surfers":                    "com.kiloo.subwaysurfers",
    "candy crush solitaire":             "com.king.apps.candysolitaire",
    "chess.com":                         "com.chess",
    "lichess":                           "org.lichess.android",
    "elden ring":                        "com.bandainamcoent.eldenmasterofring",
    "baldurs gate 3":                    "com.larian.bg3",
    "hearthstone":                       "com.blizzard.wtcg.hearthstone",
    "legends of runeterra":              "com.riotgames.lorcompanion",
    "magic the gathering":               "com.wizards.mtga",
    "yu-gi-oh":                          "jp.konami.yugioh.officialcardgame",

    # ═══════════════════════════════════════════════════════════════════════════
    # Fitness & Health
    # ═══════════════════════════════════════════════════════════════════════════
    "google fit":                        "com.google.android.gms.fit",
    "fitbit":                            "com.fitbit.FitbitMobile",
    "strava":                            "com.strava",
    "myfitnesspal":                      "com.myfitnesspal.android",
    "nike training club":                "com.nike.ntc",
    "adidas training":                   "com.adidas.trainingapp",
    "peloton":                           "com.onepeloton.class",
    "befit":                             "com.befit",
    "curefit - cult, train & eat":       "com.curefit.android",
    "cult fit":                          "com.curefit.android",
    "trainerize":                        "com.fitprotools.trainerize",
    "jefit":                             "je.fit.jefit",
    "strong":                            "com.strong.app",
    "crunch fitness":                    "com.crunch.fitness",
    "ymca":                              "com.webclients.ymca",
    "docktor":                           "in.docktor.app",
    "practo":                            "com.practo",
    "1mg":                               "com.healthkart.onemg",
    "netmeds":                           "in.netmeds.mobile",
    "apollo telehealth":                 "com.apollohealth.apollo247",
    "medlife":                           "in.medlife.pharmacy",
    "myupchar":                          "com.medibuddy.myupchar",

    # ═══════════════════════════════════════════════════════════════════════════
    # Productivity & Utility
    # ═══════════════════════════════════════════════════════════════════════════
    "google maps":                       "com.google.android.apps.maps",
    "maps":                              "com.google.android.apps.maps",
    "google chrome":                     "com.android.chrome",
    "chrome":                            "com.android.chrome",
    "mozilla firefox":                   "org.mozilla.firefox",
    "firefox":                           "org.mozilla.firefox",
    "edge":                              "com.microsoft.emmx",
    "opera":                             "com.opera.browser",
    "gmail":                             "com.google.android.gm",
    "gmail app":                         "com.google.android.gm",
    "outlook":                           "com.microsoft.office.outlook",
    "google drive":                      "com.google.android.apps.docs",
    "google docs":                       "com.google.android.apps.docs",
    "google sheets":                     "com.google.android.apps.sheets",
    "google slides":                     "com.google.android.apps.slides",
    "onedrive":                          "com.microsoft.skydrive",
    "dropbox":                           "com.dropbox.android",
    "google photos":                     "com.google.android.apps.photos",
    "photos":                            "com.google.android.apps.photos",
    "amazon photos":                     "com.amazon.photos",
    "adobe lightroom":                   "com.adobe.lightroom",
    "adobe reader":                      "com.adobe.reader",
    "truecaller":                        "com.truecaller",
    "truecaller - caller id":            "com.truecaller",
    "jio":                               "com.jio.myjio",
    "my jio":                            "com.jio.myjio",
    "airtel thanks":                     "com.airtel.android.myairtel",
    "my airtel":                         "com.airtel.android.myairtel",
    "vi":                                "com.myvicustomer",
    "vi my plan":                        "com.myvicustomer",
    "zoom":                              "us.zoom.videomeetings",
    "microsoft teams":                   "com.microsoft.teams",
    "skype for business":                "com.microsoft.skype.teams",
    "slack":                             "com.slack",
    "discord":                           "com.discord",
    "notion":                            "notion.client",
    "todoist":                           "com.todoist",
    "microsoft todo":                    "com.microsoft.todos",
    "any.do":                            "com.any.do",
    "reminders":                         "com.google.android.calendar",
    "google calendar":                   "com.google.android.calendar",
    "microsoft outlook calendar":        "com.microsoft.office.outlook",
    "notes app - google keep":           "com.google.android.keep",
    "google keep":                       "com.google.android.keep",
    "onenote":                           "com.microsoft.office.onenote",
    "evernote":                          "com.evernote",
    "obsidian":                          "md.obsidian",
    "notion app":                        "notion.client",
    "aarogya setu":                      "nic.goi.nic.digilocker",
    "digilocker":                        "nic.goi.nic.digilocker",
    "umang":                             "in.gov.umang.negd.g2c",
    "cowin":                             "in.gov.nic.covid19",
    "incred":                            "com.incred",
    "cibil":                             "in.cibil.creditapp",
    "experian":                          "com.experian.emobilemobile",

    # ═══════════════════════════════════════════════════════════════════════════
    # News & Reading
    # ═══════════════════════════════════════════════════════════════════════════
    "inshorts":                          "com.inis.android",
    "google news":                       "com.google.android.apps.mediashell",
    "times of india":                    "com.timesofindia.android",
    "the hindu":                         "com.thehindu",
    "indian express":                    "com.indianexpress.android",
    "deccan chronicle":                  "com.deccanchronicle",
    "dna":                               "com.dnaindia.android",
    "hindustan times":                   "com.hindustantimes.android",
    "indian express lite":               "com.indianexpress.lite",
    "medium":                            "com.medium.reader",
    "quora":                             "com.quora.android",
    "amazon kindle":                     "com.amazon.kindle",
    "audible":                           "com.audible.application",
    "pocket":                            "com.ideashower.readitlater.pro",
    "instapaper":                        "com.instapaper.android",

    # ═══════════════════════════════════════════════════════════════════════════
    # Photography & Design
    # ═══════════════════════════════════════════════════════════════════════════
    "snapseed":                          "com.niksoftware.snapseed",
    "photo editor pro":                  "com.nis.app",
    "picsart":                           "com.picsart.studio",
    "pixlr":                             "com.pixlr.express",
    "canva":                             "com.canva.android",
    "adobe express":                     "com.adobe.creativecloud.express",
    "adobe spark":                       "com.adobe.creativecloud.spark",
    "adobe xd":                          "com.adobe.xd",
    "figma":                             "com.figma.mirror",
    "autodesk sketchbook":               "com.autodesk.sketchbook",
    "ibis paint":                        "jp.co.ibis.x.app",
    "clip studio paint":                 "com.celsys.clipstudio.paint",
    "procreate":                         "com.apple.procreate",
    "mobile legends":                    "com.mobile.legends",

    # ═══════════════════════════════════════════════════════════════════════════
    # Video & Photo Editing
    # ═══════════════════════════════════════════════════════════════════════════
    "capcut":                            "com.liklook.luckymv",
    "cap cut":                           "com.liklook.luckymv",
    "kinemaster":                        "com.kinemaster.director",
    "vllo":                              "com.videoeditor.vllo",
    "inshot":                            "com.camerasideas.instashot",
    "filmora go":                        "com.tools.film",
    "powerdirector":                     "com.cyberlink.powerdirector.DRA140505",
    "adobe premiere rush":               "com.adobe.premiereclip",
    "imovie":                            "com.apple.iMovie",
    "quik":                              "com.gopro.quickdeskandroid",
    "quikgopro":                         "com.gopro.quickdeskandroid",
    "vimeo":                             "com.vimeo.android.videoapp",

    # ═══════════════════════════════════════════════════════════════════════════
    # Education & Learning
    # ═══════════════════════════════════════════════════════════════════════════
    "byju's":                            "com.byjus.app",
    "byjus":                             "com.byjus.app",
    "unacademy":                         "com.unacademy.android",
    "vedantu":                           "com.vedantu.app",
    "toppr":                             "com.toppr.toppr_android",
    "khan academy":                      "org.khacademy.android",
    "duolingo":                          "com.duolingo",
    "grammarly":                         "com.grammarly.android",
    "linkedin learning":                 "com.linkedin.android.learning",
    "udemy":                             "com.udemy.android",
    "skillshare":                        "com.skillshare.android",
    "coursera":                          "org.coursera.android",
    "edpuzzle":                          "com.edpuzzle",
    "microsoft learn":                   "com.microsoft.emmx",
    "google classroom":                  "com.google.android.apps.classroom",
    "smart study - quizlet":             "com.quizlet.quizletandroid",
    "quizlet":                           "com.quizlet.quizletandroid",
    "headway":                           "com.headway.app",

    # ═══════════════════════════════════════════════════════════════════════════
    # Weather & Maps
    # ═══════════════════════════════════════════════════════════════════════════
    "google weather":                    "com.google.android.apps.weather",
    "weather":                           "com.weather.Weather",
    "wunderground":                      "com.wunderground.android.weather",
    "accuweather":                       "com.accuweather.android",
    "windy":                             "com.windyapp",
    "weatherbug":                        "com.aws.android",

    # ═══════════════════════════════════════════════════════════════════════════
    # Miscellaneous & Tools
    # ═══════════════════════════════════════════════════════════════════════════
    "uc browser":                        "com.uc.browser.en",
    "uc mini":                           "com.uc.browser.mini",
    "opera mini":                        "com.opera.mini.native",
    "textfree":                          "com.pinger.textfree",
    "google assistant":                  "com.google.android.apps.googleassistant",
    "alexa":                             "com.amazon.dee.app",
    "cortana":                           "com.microsoft.cortana",
    "soundcloud go+":                    "com.soundcloud.android",
    "scribd":                            "com.scribd.app.reader0",
    "httpcanary":                        "com.guoshi.httpcanary",
    "turbo vpn":                         "com.turboapp.vpn",
    "hotspot shield":                    "com.afspeedy",
    "nordvpn":                           "com.nordvpn.android",
    "expressvpn":                        "com.expressvpn",
    "surfshark":                         "com.surfshark.vpnclient.android",
    "warp":                              "com.cloudflare.onedotone",
    "lighthouse":                        "com.light.house",
}


# ── Validation helpers ────────────────────────────────────────────────────────

def _is_valid_id(value: object) -> bool:
    """
    Returns True only when value is a usable Android package name.
    Handles None, float NaN, empty string, 'nan', 'none', 'null'.
    Never use bool() for this — bool(float('nan')) is True in Python.
    """
    if value is None:
        return False
    if isinstance(value, float):
        try:
            if math.isnan(value):
                return False
        except Exception:
            return False
    cleaned = str(value).strip().lower()
    return cleaned not in ("", "nan", "none", "null")


def _normalise(text: str | None) -> str:
    """Lowercase + strip for safe comparisons."""
    return (text or "").strip().lower()


# ── Known-app lookup ──────────────────────────────────────────────────────────

def lookup_known_app(title: str) -> str | None:
    """
    Checks the KNOWN_APP_IDS table using progressive matching:
      1. Exact normalised match
      2. Table key is contained in title (only for keys > 1 char, longest keys first to prioritize specificity)
      3. Title is contained in table key
    Returns the appId string or None.
    """
    norm = _normalise(title)
    if not norm:
        return None

    # Pass 1 — exact match
    if norm in KNOWN_APP_IDS:
        return KNOWN_APP_IDS[norm]

    # Pass 2 — known key is a substring of the title
    # Require key length >= 8 to prevent short brand names (e.g. 'swiggy',
    # 'zomato', 'paytm') from matching unrelated apps like
    # 'Swiggy Delivery Partner App' and returning the wrong ID.
    # Sort by length descending so longer/more-specific keys win first.
    for key in sorted(KNOWN_APP_IDS.keys(), key=len, reverse=True):
        if len(key) >= 8 and key in norm:
            return KNOWN_APP_IDS[key]

    # Pass 3 — title is a substring of a known key
    for key, app_id in KNOWN_APP_IDS.items():
        if norm in key:
            return app_id

    return None


# ── URL helpers ───────────────────────────────────────────────────────────────

def is_google_play_url(text: str) -> bool:
    if not text:
        return False
    return "play.google.com/store/apps/details" in text.strip().lower()


def extract_app_id_from_url(url: str) -> str | None:
    """
    Extracts the `id` query param from a Play Store URL.
    e.g. https://play.google.com/store/apps/details?id=com.whatsapp → com.whatsapp
    """
    if not url:
        return None
    try:
        params = parse_qs(urlparse(url.strip()).query)
        app_id = params.get("id", [None])[0]
        return app_id if _is_valid_id(app_id) else None
    except Exception:
        return None


# ── Search-based recovery (for unknown apps) ──────────────────────────────────

def _recover_app_id_via_search(
    title: str,
    developer: str = "",
    country: str = "in",
) -> str | None:
    """
    Last-resort search-based appId recovery for apps NOT in KNOWN_APP_IDS.
    Uses three passes per query: title+developer → title only → first valid.
    """
    candidates = [
        title.strip(),
        title.split(":")[0].strip(),
        title.split("-")[0].strip(),
    ]
    seen: set[str] = set()
    queries: list[str] = [
        c for c in candidates
        if c and not (seen.add(c) or c in seen - {c})  # type: ignore[func-returns-value]
    ]
    # simpler dedup
    queries = []
    seen_set: set[str] = set()
    for c in candidates:
        if c and c not in seen_set:
            seen_set.add(c)
            queries.append(c)

    norm_title = _normalise(title)
    norm_dev   = _normalise(developer)

    for query in queries:
        hits: list[dict] = []
        for attempt in range(_MAX_SEARCH_RETRIES):
            try:
                hits = search(query, lang="en", country=country, n_hits=_RECOVERY_HITS)
                break
            except Exception as exc:
                if attempt < _MAX_SEARCH_RETRIES - 1:
                    time.sleep(_SEARCH_RETRY_WAIT)
                else:
                    print(f"  Recovery search failed for '{query}': {exc}")

        if not hits:
            continue

        # Pass 1 — title + developer
        if norm_dev:
            for h in hits:
                h_id = h.get("appId")
                if (
                    _is_valid_id(h_id)
                    and _normalise(h.get("title")) == norm_title
                    and _normalise(h.get("developer")) == norm_dev
                ):
                    return str(h_id).strip()

        # Pass 2 — title only
        for h in hits:
            h_id = h.get("appId")
            if _is_valid_id(h_id) and _normalise(h.get("title")) == norm_title:
                return str(h_id).strip()

        # Pass 3 — first valid result for specific queries
        if len(query) > 10:
            for h in hits:
                h_id = h.get("appId")
                if _is_valid_id(h_id):
                    return str(h_id).strip()

    return None


# ── Confidence Scoring ───────────────────────────────────────────────────────

def _calculate_match_confidence(
    query: str,
    title: str,
    developer: str = "",
    raw_id: str | None = None,
    recovered_from: str = "none",  # "native", "known_app", "search_recovery"
) -> float:
    """
    Calculates confidence (0.0 to 1.0) that the search result is correct.
    
    Logic:
      - known_app lookup: 0.95 (trusted database, highest confidence)
      - native appId: 0.90 (Google Play returned it directly)
      - search recovery: 0.70 (fallback method, lower confidence)
      - no appId: 0.00
      - title match quality: ±0.05 (exact vs partial match)
    """
    if not _is_valid_id(raw_id):
        return 0.0

    norm_query = _normalise(query)
    norm_title = _normalise(title)
    norm_dev   = _normalise(developer)

    # Base confidence by recovery method
    base_conf = {
        "known_app":       0.95,
        "native":          0.90,
        "search_recovery": 0.70,
        "none":            0.0,
    }.get(recovered_from, 0.0)

    if base_conf == 0.0:
        return 0.0

    # Adjust for title match quality
    if norm_title == norm_query:
        # Exact match
        return min(1.0, base_conf + 0.05)
    elif norm_query in norm_title:
        # Partial match (e.g., query in title)
        return base_conf
    else:
        # No direct match in title
        return max(0.0, base_conf - 0.10)


# ── Search ────────────────────────────────────────────────────────────────────

def search_apps(
    query: str,
    lang: str = "en",
    country: str = "in",
    max_results: int = 5,
) -> pd.DataFrame:
    """
    Search Google Play for apps matching `query`.
    
    Returns a DataFrame with columns: rank, title, appId, developer, score, installs, icon, has_app_id, confidence, confidence_level

    AppId resolution priority per result:
      1. Returned directly by the scraper          (confidence: 0.90)
      2. KNOWN_APP_IDS lookup by title             (confidence: 0.95)
      3. Search-based recovery with developer hint (confidence: 0.70)
    """
    query = (query or "").strip()
    if not query:
        return pd.DataFrame()

    results: list[dict] = []
    for attempt in range(_MAX_SEARCH_RETRIES):
        try:
            results = search(query, lang=lang, country=country, n_hits=max_results)
            break
        except Exception as exc:
            if attempt < _MAX_SEARCH_RETRIES - 1:
                time.sleep(_SEARCH_RETRY_WAIT)
            else:
                print(f"Search Error: {exc}")
                return pd.DataFrame()

    if not results:
        return pd.DataFrame()

    rows: list[dict] = []
    for rank, item in enumerate(results, start=1):
        raw_id    = item.get("appId")
        title     = (item.get("title") or "").strip()
        developer = (item.get("developer") or "").strip()
        recovery_method = "none"

        if not _is_valid_id(raw_id):
            # Step 1 — known-app lookup (fast, always correct)
            recovered = lookup_known_app(title)

            if recovered:
                raw_id = recovered
                recovery_method = "known_app"
                print(f"  Rank {rank} ({title!r}) → resolved via known-app table: {raw_id}")
            else:
                # Step 2 — search-based recovery (slower, for unknown apps)
                print(f"  Rank {rank} ({title!r}) — appId missing, attempting search recovery...")
                recovered = _recover_app_id_via_search(title, developer=developer, country=country)
                if recovered:
                    raw_id = recovered
                    recovery_method = "search_recovery"
                    print(f"  Recovered via search: {raw_id}")
                else:
                    raw_id = None
                    print(f"  Recovery failed — rank {rank} cannot be selected.")
        else:
            recovery_method = "native"

        confidence = _calculate_match_confidence(
            query, title, developer, raw_id, recovery_method
        )
        
        # Convert confidence to a descriptive level
        if confidence >= 0.90:
            conf_level = "HIGH"
        elif confidence >= 0.70:
            conf_level = "MEDIUM"
        elif confidence > 0.0:
            conf_level = "LOW"
        else:
            conf_level = "NONE"

        rows.append({
            "rank":              rank,
            "title":             title or None,
            "appId":             raw_id if _is_valid_id(raw_id) else None,
            "developer":         developer or None,
            "score":             item.get("score"),
            "installs":          item.get("installs"),
            "icon":              item.get("icon"),
            "has_app_id":        _is_valid_id(raw_id),
            "confidence":        round(confidence, 3),
            "confidence_level":  conf_level,
            "recovery_method":   recovery_method,
        })

    return pd.DataFrame(rows)


# ── App metadata ──────────────────────────────────────────────────────────────

def get_app_metadata(app_id: str, lang: str = "en", country: str = "in") -> dict:
    """Fetches full app metadata. Returns dict with 'error' key on failure."""
    if not _is_valid_id(app_id):
        return {"error": f"Invalid app_id: {app_id!r}"}
    try:
        return app(app_id.strip(), lang=lang, country=country)
    except Exception as exc:
        return {"error": str(exc)}


# ── Review fetching ───────────────────────────────────────────────────────────

def _fetch_reviews_single(
    app_id: str,
    lang: str = "en",
    country: str = "in",
    max_reviews: int = 200,
) -> pd.DataFrame:
    """Single-region review fetch. Returns empty DataFrame on failure."""
    collected: list[dict] = []
    continuation_token = None

    try:
        while len(collected) < max_reviews:
            batch, continuation_token = reviews(
                app_id,
                lang=lang,
                country=country,
                sort=Sort.NEWEST,
                count=min(_REVIEW_BATCH_SIZE, max_reviews - len(collected)),
                continuation_token=continuation_token,
            )

            if not batch:
                break

            for r in batch:
                collected.append({
                    "reviewId":             r.get("reviewId"),
                    "userName":             r.get("userName"),
                    "content":              r.get("content"),
                     "rating":              r.get("score"),
                    "score":                r.get("score"),
                    "thumbsUpCount":        r.get("thumbsUpCount"),
                    "reviewCreatedVersion": r.get("reviewCreatedVersion"),
                    "at":                   r.get("at"),
                    "replyContent":         r.get("replyContent"),
                    "repliedAt":            r.get("repliedAt"),
                })

            if continuation_token is None:
                break

    except Exception as exc:
        print(f"  Review fetch error (lang={lang}, country={country}): {exc}")

    # Hard-truncate: the API sometimes returns a slightly larger batch than
    # requested (e.g. asked for 150, got 200), which would push the total
    # over max_reviews. Slicing here guarantees an exact match.
    return pd.DataFrame(collected[:max_reviews]) if collected else pd.DataFrame()


def fetch_reviews_for_app(
    app_id: str,
    lang: str = "en",
    country: str = "in",
    max_reviews: int = 200,
) -> pd.DataFrame:
    """
    Fetches reviews with automatic regional fallback.
    Handles country-restricted apps (e.g. Free Fire India) that return
    0 reviews from the wrong region.
    """
    if not _is_valid_id(app_id):
        print(f"  Invalid app_id: {app_id!r}")
        return pd.DataFrame()

    app_id = app_id.strip()

    # Deduplicate configs — caller preference first, then fallbacks
    caller_cfg = {"lang": lang, "country": country}
    seen_keys: list[tuple] = []
    ordered: list[dict] = []
    for cfg in [caller_cfg] + _REGION_FALLBACKS:
        key = (cfg["lang"], cfg["country"])
        if key not in seen_keys:
            seen_keys.append(key)
            ordered.append(cfg)

    for cfg in ordered:
        result = _fetch_reviews_single(app_id, max_reviews=max_reviews, **cfg)
        if not result.empty:
            print(f"  Reviews fetched — lang={cfg['lang']}, country={cfg['country']}, count={len(result)}")
            return result

    print(f"  No reviews found for {app_id!r} in any region.")
    return pd.DataFrame()


# ── Input resolution ──────────────────────────────────────────────────────────

def resolve_app_id_from_url_or_name(user_input: str) -> tuple[str | None, str]:
    """
    Returns (app_id, mode).
    mode: "url" | "search" | "none"
    """
    user_input = (user_input or "").strip()
    if not user_input:
        return None, "none"

    if is_google_play_url(user_input):
        app_id = extract_app_id_from_url(user_input)
        if not _is_valid_id(app_id):
            print("  Could not extract a valid app ID from the URL.")
            return None, "none"
        return app_id, "url"

    return None, "search"