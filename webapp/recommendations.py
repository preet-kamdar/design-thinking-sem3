"""Server-side recommendation data for the companion web dashboard.

Mirrors the demo database in PersonalMusicExperience/recommendation-engine.js so
the web dashboard and the Chrome extension show the same content. Kept separate
because the extension cannot import Python and the web app cannot import JS.
"""

DEFAULT = {
    "familiar": [
        ("As It Was", "Harry Styles", "Pop", "A globally familiar hit"),
        ("Cruel Summer", "Taylor Swift", "Pop", "Broadly appealing pop"),
        ("Flowers", "Miley Cyrus", "Pop", "Popular contemporary radio"),
        ("Watermelon Sugar", "Harry Styles", "Pop", "Mainstream upbeat pop"),
        ("Anti-Hero", "Taylor Swift", "Pop", "A widely known contemporary hit"),
    ],
    "balanced": [
        ("Dreams", "Fleetwood Mac", "Classic Rock", "A timeless classic"),
        ("Everybody Wants To Rule The World", "Tears For Fears", "New Wave", "80s pop perfection"),
        ("Fast Car", "Tracy Chapman", "Folk Pop", "Acoustic storytelling"),
        ("Superstition", "Stevie Wonder", "Funk", "An essential groove"),
        ("Billie Jean", "Michael Jackson", "Pop", "Iconic 80s pop"),
    ],
    "exploratory": [
        ("Once In A Lifetime", "Talking Heads", "New Wave", "Avant-garde pop classic"),
        ("Babooshka", "Kate Bush", "Art Pop", "Theatrical, eccentric 80s pop"),
        ("Wuthering Heights", "Kate Bush", "Art Pop", "Unique vocal delivery"),
        ("Born Under Punches", "Talking Heads", "Post-Punk", "Complex polyrhythms"),
        ("Love Will Tear Us Apart", "Joy Division", "Post-Punk", "Pioneering alternative rock"),
    ],
}

DB = {
    "Spotify": {
        "arctic monkeys": {
            "familiar": [
                ("Reptilia", "The Strokes", "Indie Rock", "Closely related 2000s indie rock"),
                ("Take Me Out", "Franz Ferdinand", "Indie Rock", "Similar angular guitar riffs"),
                ("Mr. Brightside", "The Killers", "Alternative", "A staple of the same era"),
                ("Fluorescent Adolescent", "Arctic Monkeys", "Indie Rock", "Another hit from the same artist"),
                ("Seven Nation Army", "The White Stripes", "Garage Rock", "Similar raw energy"),
            ],
            "balanced": [
                ("Lonely Boy", "The Black Keys", "Blues Rock", "A bluesier take on modern rock"),
                ("Elephant", "Tame Impala", "Psychedelic Rock", "Adds psychedelic textures"),
                ("Are You Gonna Be My Girl", "Jet", "Hard Rock", "High energy rock with a retro feel"),
                ("Out of the Black", "Royal Blood", "Hard Rock", "Heavier, modern British rock"),
                ("Feel Good Inc.", "Gorillaz", "Alternative", "Blends rock with hip-hop elements"),
            ],
            "exploratory": [
                ("Marquee Moon", "Television", "Post-Punk", "The 70s roots of the indie rock sound"),
                ("Disorder", "Joy Division", "Post-Punk", "Darker, atmospheric influence"),
                ("I Wanna Be Adored", "The Stone Roses", "Madchester", "British rock history"),
                ("Deceptacon", "Le Tigre", "Dance-Punk", "High energy, electronic twist on punk"),
                ("Cannonball", "The Breeders", "Alt-Rock", "90s alternative foundations"),
            ],
        },
        "the weeknd": {
            "familiar": [
                ("Starboy", "The Weeknd", "R&B/Pop", "From the same artist"),
                ("Passionfruit", "Drake", "R&B", "Similar Toronto R&B sound"),
                ("Sunflower", "Post Malone", "Pop/Hip-Hop", "Modern atmospheric pop"),
                ("Heartless", "The Weeknd", "R&B", "More of that dark pop vibe"),
                ("Location", "Khalid", "R&B", "Smooth modern R&B"),
            ],
            "balanced": [
                ("Redbone", "Childish Gambino", "Funk/Soul", "Adds a vintage funk element"),
                ("Pink + White", "Frank Ocean", "Alternative R&B", "More experimental R&B"),
                ("Good Days", "SZA", "Alternative R&B", "Atmospheric female vocal R&B"),
                ("Telepatía", "Kali Uchis", "Latin Pop", "Bilingual dream pop"),
                ("L$D", "A$AP Rocky", "Cloud Rap", "Psychedelic hip-hop crossover"),
            ],
            "exploratory": [
                ("Purple Rain", "Prince", "Pop/Rock", "The 80s pop/R&B blueprint"),
                ("Running Up That Hill", "Kate Bush", "Synth-Pop", "Classic 80s synth atmosphere"),
                ("Blue Monday", "New Order", "Synth-Pop", "Pioneering dance music"),
                ("Teardrop", "Massive Attack", "Trip-Hop", "Dark, atmospheric 90s trip-hop"),
                ("Closer", "Nine Inch Nails", "Industrial", "Darker, industrial electronic edge"),
            ],
        },
    },
    "YouTube Music": {
        "nujabes": {
            "familiar": [
                ("Feather", "Nujabes", "Jazz-Hop", "Another classic by Nujabes"),
                ("City Lights", "J Dilla", "Instrumental Hip-Hop", "Similar foundational beatmaker"),
                ("Luv(sic) pt3", "Nujabes", "Jazz-Hop", "Essential Nujabes discography"),
                ("Accordion", "Madvillain", "Underground Hip-Hop", "Classic underground production"),
                ("Aruarian Dance", "Nujabes", "Instrumental", "More of what you love"),
            ],
            "balanced": [
                ("The Scenic Route", "Brock Berrigan", "Chillhop", "Modern instrumental chillhop"),
                ("Disco Yes", "Tom Misch", "Neo-Soul", "Live instrumentation meets beats"),
                ("Never Catch Me", "Flying Lotus", "Experimental Beats", "Complex electronic hip-hop"),
            ],
            "exploratory": [
                ("Take Five", "The Dave Brubeck Quartet", "Jazz", "The original jazz roots of the samples"),
                ("So What", "Miles Davis", "Jazz", "Classic modal jazz foundations"),
                ("Endtroducing.....", "DJ Shadow", "Trip-Hop", "Pioneering instrumental sampling"),
            ],
        },
    },
    "Apple Music": {
        "dua lipa": {
            "familiar": [
                ("Don't Start Now", "Dua Lipa", "Dance-Pop", "Another huge hit"),
                ("Say So", "Doja Cat", "Pop/R&B", "Similar disco-pop revival vibe"),
                ("Blinding Lights", "The Weeknd", "Synth-Pop", "80s-inspired mega-hit"),
                ("Rain On Me", "Lady Gaga & Ariana Grande", "Dance-Pop", "Upbeat pop collaboration"),
                ("Juice", "Lizzo", "Funk-Pop", "Fun, funky pop anthem"),
            ],
            "balanced": [
                ("September", "Earth, Wind & Fire", "Disco/Funk", "The original 70s disco sound"),
                ("About Damn Time", "Lizzo", "Funk-Pop", "Modern groove"),
                ("Get Lucky", "Daft Punk", "Nu-Disco", "Modern electronic disco"),
                ("Heart of Glass", "Blondie", "New Wave/Disco", "70s pop/rock crossover"),
                ("I Feel Love", "Donna Summer", "Disco", "Pioneering electronic dance"),
            ],
            "exploratory": [
                ("Blue Monday", "New Order", "Synth-Pop", "80s electronic foundations"),
                ("Supernature", "Cerrone", "Euro-Disco", "Deep cuts from the disco era"),
                ("Groove Is in the Heart", "Deee-Lite", "Dance", "90s dance club culture"),
            ],
        },
    },
}

VIBES = {
    "Spotify": {
        "chill": [("Sunset Lover", "Petit Biscuit", "Electronic", "Warm, relaxed electronic beats"),
                  ("Weightless", "Marconi Union", "Ambient", "Scientifically proven to reduce anxiety"),
                  ("Locket", "Crumb", "Indie Pop", "Dreamy, slow-paced vocals")],
        "focus": [("So It Goes", "Mac Miller", "Hip-Hop", "Steady, rhythmic flow for concentration"),
                  ("Avril 14th", "Aphex Twin", "Ambient", "Simple, repetitive piano")],
        "energetic": [("Can't Stop", "Red Hot Chili Peppers", "Rock", "Driving bassline and high tempo"),
                      ("Levitating", "Dua Lipa", "Dance-Pop", "Upbeat modern disco")],
    },
    "YouTube Music": {
        "chill": [("Lofi Hip Hop Radio", "Lofi Girl", "Lofi", "The ultimate chill stream"),
                  ("Affection", "Jinsang", "Lofi Hip-Hop", "Smooth, nostalgic sampling")],
        "sad": [("Someone Like You", "Adele", "Pop", "Raw, emotional piano ballad"),
                ("Skinny Love", "Bon Iver", "Indie Folk", "Acoustic heartbreak")],
        "workout": [("Eye of the Tiger", "Survivor", "Rock", "The ultimate training anthem"),
                    ("Till I Collapse", "Eminem", "Hip-Hop", "Intense motivational energy")],
    },
    "Apple Music": {
        "late night": [("Nightcall", "Kavinsky", "Synthwave", "Perfect for a midnight drive"),
                       ("Midnight City", "M83", "Electronic", "Euphoric late-night synth")],
        "romantic": [("Perfect", "Ed Sheeran", "Pop", "Classic modern love song"),
                     ("All of Me", "John Legend", "R&B", "Dedicated piano ballad")],
        "relaxing": [("Weightless", "Marconi Union", "Ambient", "Designed for relaxation"),
                     ("Clair de Lune", "Claude Debussy", "Classical", "Gentle, floating piano")],
    },
    "default": {
        "chill": [("Breathe", "Telepopmusik", "Chill", "Classic chillout track")],
        "focus": [("Weightless", "Marconi Union", "Ambient", "Scientifically proven to calm the mind")],
        "energetic": [("Don't Stop Me Now", "Queen", "Rock", "Undeniable upbeat energy")],
        "sad": [("Fix You", "Coldplay", "Alternative", "Emotional and building")],
        "late night": [("Drive", "The Cars", "New Wave", "A nostalgic late night drive")],
        "workout": [("Gonna Fly Now", "Bill Conti", "Soundtrack", "Motivational instrumental")],
        "romantic": [("Make You Feel My Love", "Adele", "Pop", "Deeply romantic vocals")],
        "relaxing": [("Gymnopédie No.1", "Erik Satie", "Classical", "Gentle, relaxing piano")],
    },
}

VIBE_TAGS = ["chill", "focus", "energetic", "sad", "late night", "workout", "romantic", "relaxing"]
LEVELS = ["familiar", "balanced", "exploratory"]


def _as_items(rows: list[tuple]) -> list[dict]:
    """Convert compact tuples into the same dict shape used by the extension."""
    platform_prefix = ""
    return [
        {
            "id": f"web-{platform_prefix}-{i}-{title.lower().replace(' ', '-')}",
            "title": title,
            "artist": artist,
            "genre": genre,
            "reason": reason,
        }
        for i, (title, artist, genre, reason) in enumerate(rows, start=1)
    ]


def get_recommendations(platform: str, level: str, artist: str = "") -> list[dict]:
    pdata = DB.get(platform, {})
    level = level if level in LEVELS else "balanced"
    rows = DEFAULT[level]
    if artist:
        key = artist.lower()
        for candidate in pdata:
            if candidate in key or key in candidate:
                rows = pdata[candidate][level]
                break
    return _as_items(rows)


def get_vibe_recommendations(platform: str, vibe: str) -> list[dict]:
    pdata = VIBES.get(platform, VIBES["default"])
    rows = pdata.get(vibe.lower()) or VIBES["default"].get(vibe.lower()) or VIBES["default"]["chill"]
    return _as_items(rows)
