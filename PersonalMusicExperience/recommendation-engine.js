// Recommendation Engine Prototype
// Simulates a backend recommendation system that uses context (platform, track, level) to serve dynamic music suggestions.

const RecommendationEngine = {
  // Our simulated database
  database: {
    'Spotify': {
      // Match for Arctic Monkeys (Requested test case)
      'arctic monkeys': {
        recommendations: {
          familiar: [
            { id: 'sp-am-f1', title: 'Reptilia', artist: 'The Strokes', genre: 'Indie Rock', reason: 'Closely related 2000s indie rock' },
            { id: 'sp-am-f2', title: 'Take Me Out', artist: 'Franz Ferdinand', genre: 'Indie Rock', reason: 'Similar angular guitar riffs' },
            { id: 'sp-am-f3', title: 'Mr. Brightside', artist: 'The Killers', genre: 'Alternative', reason: 'A staple of the same era' },
            { id: 'sp-am-f4', title: 'Fluorescent Adolescent', artist: 'Arctic Monkeys', genre: 'Indie Rock', reason: 'Another hit from the same artist' },
            { id: 'sp-am-f5', title: 'Seven Nation Army', artist: 'The White Stripes', genre: 'Garage Rock', reason: 'Similar raw energy' }
          ],
          balanced: [
            { id: 'sp-am-b1', title: 'Lonely Boy', artist: 'The Black Keys', genre: 'Blues Rock', reason: 'A bluesier take on modern rock' },
            { id: 'sp-am-b2', title: 'Elephant', artist: 'Tame Impala', genre: 'Psychedelic Rock', reason: 'Adds psychedelic textures' },
            { id: 'sp-am-b3', title: 'Are You Gonna Be My Girl', artist: 'Jet', genre: 'Hard Rock', reason: 'High energy rock with a retro feel' },
            { id: 'sp-am-b4', title: 'Out of the Black', artist: 'Royal Blood', genre: 'Hard Rock', reason: 'Heavier, modern British rock' },
            { id: 'sp-am-b5', title: 'Feel Good Inc.', artist: 'Gorillaz', genre: 'Alternative', reason: 'Blends rock with hip-hop elements' }
          ],
          exploratory: [
            { id: 'sp-am-e1', title: 'Marquee Moon', artist: 'Television', genre: 'Post-Punk', reason: 'The 70s roots of the indie rock sound' },
            { id: 'sp-am-e2', title: 'Disorder', artist: 'Joy Division', genre: 'Post-Punk', reason: 'Darker, atmospheric influence' },
            { id: 'sp-am-e3', title: 'I Wanna Be Adored', artist: 'The Stone Roses', genre: 'Madchester', reason: 'British rock history' },
            { id: 'sp-am-e4', title: 'Deceptacon', artist: 'Le Tigre', genre: 'Dance-Punk', reason: 'High energy, electronic twist on punk' },
            { id: 'sp-am-e5', title: 'Cannonball', artist: 'The Breeders', genre: 'Alt-Rock', reason: '90s alternative foundations' }
          ]
        }
      },
      // Match for The Weeknd (Additional Spotify test case)
      'the weeknd': {
        recommendations: {
          familiar: [
            { id: 'sp-wk-f1', title: 'Starboy', artist: 'The Weeknd', genre: 'R&B/Pop', reason: 'From the same artist' },
            { id: 'sp-wk-f2', title: 'Passionfruit', artist: 'Drake', genre: 'R&B', reason: 'Similar Toronto R&B sound' },
            { id: 'sp-wk-f3', title: 'Sunflower', artist: 'Post Malone', genre: 'Pop/Hip-Hop', reason: 'Modern atmospheric pop' },
            { id: 'sp-wk-f4', title: 'Heartless', artist: 'The Weeknd', genre: 'R&B', reason: 'More of that dark pop vibe' },
            { id: 'sp-wk-f5', title: 'Location', artist: 'Khalid', genre: 'R&B', reason: 'Smooth modern R&B' }
          ],
          balanced: [
            { id: 'sp-wk-b1', title: 'Redbone', artist: 'Childish Gambino', genre: 'Funk/Soul', reason: 'Adds a vintage funk element' },
            { id: 'sp-wk-b2', title: 'Pink + White', artist: 'Frank Ocean', genre: 'Alternative R&B', reason: 'More experimental R&B' },
            { id: 'sp-wk-b3', title: 'Good Days', artist: 'SZA', genre: 'Alternative R&B', reason: 'Atmospheric female vocal R&B' },
            { id: 'sp-wk-b4', title: 'Telepatía', artist: 'Kali Uchis', genre: 'Latin Pop', reason: 'Bilingual dream pop' },
            { id: 'sp-wk-b5', title: 'L$D', artist: 'A$AP Rocky', genre: 'Cloud Rap', reason: 'Psychedelic hip-hop crossover' }
          ],
          exploratory: [
            { id: 'sp-wk-e1', title: 'Purple Rain', artist: 'Prince', genre: 'Pop/Rock', reason: 'The 80s pop/R&B blueprint' },
            { id: 'sp-wk-e2', title: 'Running Up That Hill', artist: 'Kate Bush', genre: 'Synth-Pop', reason: 'Classic 80s synth atmosphere' },
            { id: 'sp-wk-e3', title: 'Blue Monday', artist: 'New Order', genre: 'Synth-Pop', reason: 'Pioneering dance music' },
            { id: 'sp-wk-e4', title: 'Teardrop', artist: 'Massive Attack', genre: 'Trip-Hop', reason: 'Dark, atmospheric 90s trip-hop' },
            { id: 'sp-wk-e5', title: 'Closer', artist: 'Nine Inch Nails', genre: 'Industrial', reason: 'Darker, industrial electronic edge' }
          ]
        }
      }
    },
    'YouTube Music': {
      // Match for Nujabes (Requested test case)
      'nujabes': {
        recommendations: {
          familiar: [
            { id: 'yt-nj-f1', title: 'Feather', artist: 'Nujabes', genre: 'Jazz-Hop', reason: 'Another classic by Nujabes' },
            { id: 'yt-nj-f2', title: 'City Lights', artist: 'J Dilla', genre: 'Instrumental Hip-Hop', reason: 'Similar foundational beatmaker' },
            { id: 'yt-nj-f3', title: 'Luv(sic) pt3', artist: 'Nujabes', genre: 'Jazz-Hop', reason: 'Essential Nujabes discography' },
            { id: 'yt-nj-f4', title: 'Accordion', artist: 'Madvillain', genre: 'Underground Hip-Hop', reason: 'Classic underground production' },
            { id: 'yt-nj-f5', title: 'Aruarian Dance', artist: 'Nujabes', genre: 'Instrumental', reason: 'More of what you love' }
          ],
          balanced: [
            { id: 'yt-nj-b1', title: 'Brock Berrigan', artist: 'The Scenic Route', genre: 'Chillhop', reason: 'Modern instrumental chillhop' },
            { id: 'yt-nj-b2', title: 'Tom Misch', artist: 'Disco Yes', genre: 'Neo-Soul', reason: 'Live instrumentation meets beats' },
            { id: 'yt-nj-b3', title: 'Vanilla', artist: 'Summer', genre: 'Vaporwave/Beats', reason: 'Sample-heavy instrumental grooves' },
            { id: 'yt-nj-b4', title: 'KAYTRANADA', artist: 'YOU\'RE THE ONE', genre: 'Electronic/Dance', reason: 'Upbeat, danceable production' },
            { id: 'yt-nj-b5', title: 'Flying Lotus', artist: 'Never Catch Me', genre: 'Experimental Beats', reason: 'Complex electronic hip-hop' }
          ],
          exploratory: [
            { id: 'yt-nj-e1', title: 'Take Five', artist: 'The Dave Brubeck Quartet', genre: 'Jazz', reason: 'The original jazz roots of the samples' },
            { id: 'yt-nj-e2', title: 'So What', artist: 'Miles Davis', genre: 'Jazz', reason: 'Classic modal jazz foundations' },
            { id: 'yt-nj-e3', title: 'Watermelon Man', artist: 'Herbie Hancock', genre: 'Jazz-Funk', reason: '70s jazz-funk grooves' },
            { id: 'yt-nj-e4', title: 'Music for 18 Musicians', artist: 'Steve Reich', genre: 'Minimalist', reason: 'Repetitive, mesmerizing structures' },
            { id: 'yt-nj-e5', title: 'Endtroducing.....', artist: 'DJ Shadow', genre: 'Trip-Hop', reason: 'Pioneering instrumental sampling' }
          ]
        }
      },
      // Match for Queen (Additional YT test case)
      'queen': {
        recommendations: {
          familiar: [
            { id: 'yt-qn-f1', title: 'Don\'t Stop Me Now', artist: 'Queen', genre: 'Classic Rock', reason: 'More classic Queen energy' },
            { id: 'yt-qn-f2', title: 'Tiny Dancer', artist: 'Elton John', genre: 'Classic Rock', reason: '70s piano rock contemporary' },
            { id: 'yt-qn-f3', title: 'Life on Mars?', artist: 'David Bowie', genre: 'Glam Rock', reason: 'Theatrical 70s rock' },
            { id: 'yt-qn-f4', title: 'Stairway to Heaven', artist: 'Led Zeppelin', genre: 'Classic Rock', reason: 'Epic 70s rock anthem' },
            { id: 'yt-qn-f5', title: 'Dream On', artist: 'Aerosmith', genre: 'Classic Rock', reason: 'Classic rock power ballad' }
          ],
          balanced: [
            { id: 'yt-qn-b1', title: 'Mr. Blue Sky', artist: 'Electric Light Orchestra', genre: 'Symphonic Rock', reason: 'Complex, upbeat orchestration' },
            { id: 'yt-qn-b2', title: 'Welcome to the Black Parade', artist: 'My Chemical Romance', genre: 'Emo Rock', reason: 'Modern theatrical rock anthem' },
            { id: 'yt-qn-b3', title: 'Knights of Cydonia', artist: 'Muse', genre: 'Alternative Rock', reason: 'Modern space-rock opera' },
            { id: 'yt-qn-b4', title: 'I Believe in a Thing Called Love', artist: 'The Darkness', genre: 'Hard Rock', reason: 'Revival of 70s glam rock energy' },
            { id: 'yt-qn-b5', title: 'Bohemian Like You', artist: 'The Dandy Warhols', genre: 'Alt-Rock', reason: 'Catchy, retro-inspired rock' }
          ],
          exploratory: [
            { id: 'yt-qn-e1', title: 'O Fortuna', artist: 'Carl Orff', genre: 'Classical', reason: 'Dramatic choral classical music' },
            { id: 'yt-qn-e2', title: 'Rhapsody in Blue', artist: 'George Gershwin', genre: 'Classical/Jazz', reason: 'Orchestral ambition meets jazz' },
            { id: 'yt-qn-e3', title: 'Bat Out of Hell', artist: 'Meat Loaf', genre: 'Rock Opera', reason: 'Operatic, theatrical rock storytelling' },
            { id: 'yt-qn-e4', title: 'Jesus Christ Superstar', artist: 'Andrew Lloyd Webber', genre: 'Musical', reason: '70s rock musical theater' },
            { id: 'yt-qn-e5', title: 'A Night at the Opera', artist: 'Blind Guardian', genre: 'Power Metal', reason: 'Queen-inspired epic metal' }
          ]
        }
      }
    },
    'Apple Music': {
      // Match for Dua Lipa (Apple Music test case)
      'dua lipa': {
        recommendations: {
          familiar: [
            { id: 'am-dl-f1', title: 'Don\'t Start Now', artist: 'Dua Lipa', genre: 'Dance-Pop', reason: 'Another huge hit' },
            { id: 'am-dl-f2', title: 'Say So', artist: 'Doja Cat', genre: 'Pop/R&B', reason: 'Similar disco-pop revival vibe' },
            { id: 'am-dl-f3', title: 'Blinding Lights', artist: 'The Weeknd', genre: 'Synth-Pop', reason: '80s-inspired mega-hit' },
            { id: 'am-dl-f4', title: 'Rain On Me', artist: 'Lady Gaga & Ariana Grande', genre: 'Dance-Pop', reason: 'Upbeat pop collaboration' },
            { id: 'am-dl-f5', title: 'Juice', artist: 'Lizzo', genre: 'Funk-Pop', reason: 'Fun, funky pop anthem' }
          ],
          balanced: [
            { id: 'am-dl-b1', title: 'September', artist: 'Earth, Wind & Fire', genre: 'Disco/Funk', reason: 'The original 70s disco sound' },
            { id: 'am-dl-b2', title: 'About Damn Time', artist: 'Lizzo', genre: 'Funk-Pop', reason: 'Modern groove' },
            { id: 'am-dl-b3', title: 'Get Lucky', artist: 'Daft Punk', genre: 'Nu-Disco', reason: 'Modern electronic disco' },
            { id: 'am-dl-b4', title: 'Heart of Glass', artist: 'Blondie', genre: 'New Wave/Disco', reason: '70s pop/rock crossover' },
            { id: 'am-dl-b5', title: 'I Feel Love', artist: 'Donna Summer', genre: 'Disco', reason: 'Pioneering electronic dance' }
          ],
          exploratory: [
            { id: 'am-dl-e1', title: 'Blue Monday', artist: 'New Order', genre: 'Synth-Pop', reason: '80s electronic foundations' },
            { id: 'am-dl-e2', title: 'Supernature', artist: 'Cerrone', genre: 'Euro-Disco', reason: 'Deep cuts from the disco era' },
            { id: 'am-dl-e3', title: 'You Make Me Feel (Mighty Real)', artist: 'Sylvester', genre: 'Hi-NRG Disco', reason: 'High energy 70s club classic' },
            { id: 'am-dl-e4', title: 'Groove Is in the Heart', artist: 'Deee-Lite', genre: 'Dance', reason: '90s dance club culture' },
            { id: 'am-dl-e5', title: 'Spacer', artist: 'Sheila & B. Devotion', genre: 'Space Disco', reason: 'Chic-produced obscure disco' }
          ]
        }
      },
      // Match for Billie Eilish (Additional AM test case)
      'billie eilish': {
        recommendations: {
          familiar: [
            { id: 'am-be-f1', title: 'bury a friend', artist: 'Billie Eilish', genre: 'Alt-Pop', reason: 'More of her dark pop sound' },
            { id: 'am-be-f2', title: 'Royals', artist: 'Lorde', genre: 'Art Pop', reason: 'Minimalist pop predecessor' },
            { id: 'am-be-f3', title: 'Liability', artist: 'Lorde', genre: 'Pop', reason: 'Intimate, emotional songwriting' },
            { id: 'am-be-f4', title: 'Heather', artist: 'Conan Gray', genre: 'Bedroom Pop', reason: 'Gen Z indie pop' },
            { id: 'am-be-f5', title: 'drivers license', artist: 'Olivia Rodrigo', genre: 'Pop', reason: 'Emotional contemporary pop' }
          ],
          balanced: [
            { id: 'am-be-b1', title: 'Video Games', artist: 'Lana Del Rey', genre: 'Dream Pop', reason: 'Moody, cinematic pop' },
            { id: 'am-be-b2', title: 'Kyoto', artist: 'Phoebe Bridgers', genre: 'Indie Rock', reason: 'Melancholy indie songwriting' },
            { id: 'am-be-b3', title: 'Me and Your Mama', artist: 'Childish Gambino', genre: 'R&B/Soul', reason: 'Atmospheric and intense' },
            { id: 'am-be-b4', title: 'Clairo', artist: 'Bags', genre: 'Bedroom Pop', reason: 'Lo-fi pop intimacy' },
            { id: 'am-be-b5', title: 'Mitski', artist: 'Nobody', genre: 'Indie Pop', reason: 'Theatrical indie emotion' }
          ],
          exploratory: [
            { id: 'am-be-e1', title: 'Glory Box', artist: 'Portishead', genre: 'Trip-Hop', reason: '90s dark electronic roots' },
            { id: 'am-be-e2', title: 'Angel', artist: 'Massive Attack', genre: 'Trip-Hop', reason: 'Heavy, brooding basslines' },
            { id: 'am-be-e3', title: 'Hyperballad', artist: 'Björk', genre: 'Electronic/Pop', reason: 'Avant-garde pop pioneer' },
            { id: 'am-be-e4', title: 'Fade Into You', artist: 'Mazzy Star', genre: 'Dream Pop', reason: '90s moody acoustic atmosphere' },
            { id: 'am-be-e5', title: 'Hurt', artist: 'Nine Inch Nails', genre: 'Industrial', reason: 'Raw, whispered intensity' }
          ]
        }
      }
    },
    
    // Universal defaults if no specific artist match is found
    'default': {
      recommendations: {
        familiar: [
          { id: 'def-f1', title: 'As It Was', artist: 'Harry Styles', genre: 'Pop', reason: 'A globally familiar hit' },
          { id: 'def-f2', title: 'Cruel Summer', artist: 'Taylor Swift', genre: 'Pop', reason: 'Broadly appealing pop' },
          { id: 'def-f3', title: 'Flowers', artist: 'Miley Cyrus', genre: 'Pop', reason: 'Popular contemporary radio' },
          { id: 'def-f4', title: 'Watermelon Sugar', artist: 'Harry Styles', genre: 'Pop', reason: 'Mainstream upbeat pop' },
          { id: 'def-f5', title: 'Anti-Hero', artist: 'Taylor Swift', genre: 'Pop', reason: 'A widely known contemporary hit' }
        ],
        balanced: [
          { id: 'def-b1', title: 'Dreams', artist: 'Fleetwood Mac', genre: 'Classic Rock', reason: 'A timeless classic' },
          { id: 'def-b2', title: 'Everybody Wants To Rule The World', artist: 'Tears For Fears', genre: 'New Wave', reason: '80s pop perfection' },
          { id: 'def-b3', title: 'Fast Car', artist: 'Tracy Chapman', genre: 'Folk Pop', reason: 'Acoustic storytelling' },
          { id: 'def-b4', title: 'Superstition', artist: 'Stevie Wonder', genre: 'Funk', reason: 'An essential groove' },
          { id: 'def-b5', title: 'Billie Jean', artist: 'Michael Jackson', genre: 'Pop', reason: 'Iconic 80s pop' }
        ],
        exploratory: [
          { id: 'def-e1', title: 'Once In A Lifetime', artist: 'Talking Heads', genre: 'New Wave', reason: 'Avant-garde pop classic' },
          { id: 'def-e2', title: 'Babooshka', artist: 'Kate Bush', genre: 'Art Pop', reason: 'Theatrical, eccentric 80s pop' },
          { id: 'def-e3', title: 'Wuthering Heights', artist: 'Kate Bush', genre: 'Art Pop', reason: 'Unique vocal delivery' },
          { id: 'def-e4', title: 'Born Under Punches', artist: 'Talking Heads', genre: 'Post-Punk', reason: 'Complex polyrhythms' },
          { id: 'def-e5', title: 'Love Will Tear Us Apart', artist: 'Joy Division', genre: 'Post-Punk', reason: 'Pioneering alternative rock' }
        ]
      }
    }
  },

  /**
   * Generates a list of recommended tracks based on context.
   */
  getRecommendations({ platform, currentTrack, discoveryLevel }) {
    // 1. Fallback to default platform if unknown
    const platformData = this.database[platform] || this.database['default'];
    
    // 2. Default to generic recommendations
    let matchedData = platformData['default'] || this.database['default'];
    
    // 3. Try to match the current track's artist or title to our demo data
    if (currentTrack && currentTrack.artist) {
      const searchString = (currentTrack.artist + ' ' + currentTrack.title).toLowerCase();
      
      const artistMatches = Object.keys(platformData).filter(key => 
        key !== 'default' && searchString.includes(key.toLowerCase())
      );
      
      if (artistMatches.length > 0) {
        matchedData = platformData[artistMatches[0]];
      }
    }
    
    // 4. Return the specific discovery level
    const level = discoveryLevel || 'balanced';
    return matchedData.recommendations[level] || matchedData.recommendations['balanced'];
  },

  // Simulated database for Vibe Feature
  vibeDatabase: {
    'Spotify': {
      'chill': [
        { id: 'v-sp-c1', title: 'Sunset Lover', artist: 'Petit Biscuit', genre: 'Electronic', reason: 'Warm, relaxed electronic beats.' },
        { id: 'v-sp-c2', title: 'Weightless', artist: 'Marconi Union', genre: 'Ambient', reason: 'Scientifically proven to reduce anxiety.' },
        { id: 'v-sp-c3', title: 'Locket', artist: 'Crumb', genre: 'Indie Pop', reason: 'Dreamy, slow-paced vocals.' }
      ],
      'focus': [
        { id: 'v-sp-f1', title: 'So It Goes', artist: 'Mac Miller', genre: 'Hip-Hop', reason: 'Steady, rhythmic flow for concentration.' },
        { id: 'v-sp-f2', title: 'Time', artist: 'Hans Zimmer', genre: 'Soundtrack', reason: 'Epic but unobtrusive background.' },
        { id: 'v-sp-f3', title: 'Avril 14th', artist: 'Aphex Twin', genre: 'Ambient', reason: 'Simple, repetitive piano.' }
      ],
      'energetic': [
        { id: 'v-sp-e1', title: 'Can\'t Stop', artist: 'Red Hot Chili Peppers', genre: 'Rock', reason: 'Driving bassline and high tempo.' },
        { id: 'v-sp-e2', title: 'Toxic', artist: 'Britney Spears', genre: 'Pop', reason: 'High BPM classic pop energy.' },
        { id: 'v-sp-e3', title: 'Levitating', artist: 'Dua Lipa', genre: 'Dance-Pop', reason: 'Upbeat modern disco.' }
      ]
    },
    'YouTube Music': {
      'chill': [
        { id: 'v-yt-c1', title: 'Lofi Hip Hop Radio', artist: 'Lofi Girl', genre: 'Lofi', reason: 'The ultimate chill stream.' },
        { id: 'v-yt-c2', title: 'Affection', artist: 'Jinsang', genre: 'Lofi Hip-Hop', reason: 'Smooth, nostalgic sampling.' },
        { id: 'v-yt-c3', title: 'Snowman', artist: 'WYS', genre: 'Chillhop', reason: 'Cozy winter vibes.' }
      ],
      'sad': [
        { id: 'v-yt-s1', title: 'Someone Like You', artist: 'Adele', genre: 'Pop', reason: 'Raw, emotional piano ballad.' },
        { id: 'v-yt-s2', title: 'Skinny Love', artist: 'Bon Iver', genre: 'Indie Folk', reason: 'Acoustic heartbreak.' },
        { id: 'v-yt-s3', title: 'Hurt', artist: 'Johnny Cash', genre: 'Country/Folk', reason: 'Profoundly somber reflection.' }
      ],
      'workout': [
        { id: 'v-yt-w1', title: 'Eye of the Tiger', artist: 'Survivor', genre: 'Rock', reason: 'The ultimate training montage anthem.' },
        { id: 'v-yt-w2', title: 'Stronger', artist: 'Kanye West', genre: 'Hip-Hop', reason: 'High energy electronic rap.' },
        { id: 'v-yt-w3', title: 'Till I Collapse', artist: 'Eminem', genre: 'Hip-Hop', reason: 'Intense motivational energy.' }
      ]
    },
    'Apple Music': {
      'late night': [
        { id: 'v-am-l1', title: 'Nightcall', artist: 'Kavinsky', genre: 'Synthwave', reason: 'Perfect for a midnight drive.' },
        { id: 'v-am-l2', title: 'Blinding Lights', artist: 'The Weeknd', genre: 'Synth-Pop', reason: '80s nighttime aesthetic.' },
        { id: 'v-am-l3', title: 'Midnight City', artist: 'M83', genre: 'Electronic', reason: 'Euphoric late-night synth.' }
      ],
      'romantic': [
        { id: 'v-am-r1', title: 'Perfect', artist: 'Ed Sheeran', genre: 'Pop', reason: 'Classic modern love song.' },
        { id: 'v-am-r2', title: 'At Last', artist: 'Etta James', genre: 'Soul', reason: 'Timeless romance.' },
        { id: 'v-am-r3', title: 'All of Me', artist: 'John Legend', genre: 'R&B', reason: 'Dedicated piano ballad.' }
      ],
      'relaxing': [
        { id: 'v-am-rx1', title: 'Weightless', artist: 'Marconi Union', genre: 'Ambient', reason: 'Designed for relaxation.' },
        { id: 'v-am-rx2', title: 'Orinoco Flow', artist: 'Enya', genre: 'New Age', reason: 'Soothing vocal layering.' },
        { id: 'v-am-rx3', title: 'Clair de Lune', artist: 'Claude Debussy', genre: 'Classical', reason: 'Gentle, floating piano.' }
      ]
    },
    'default': {
      'chill': [ { id: 'v-d-1', title: 'Breathe', artist: 'Telepopmusik', genre: 'Chill', reason: 'Classic chillout track.' } ],
      'focus': [ { id: 'v-d-2', title: 'Weightless', artist: 'Marconi Union', genre: 'Ambient', reason: 'Scientifically proven to calm the mind.' } ],
      'energetic': [ { id: 'v-d-3', title: 'Don\'t Stop Me Now', artist: 'Queen', genre: 'Rock', reason: 'Undeniable upbeat energy.' } ],
      'sad': [ { id: 'v-d-4', title: 'Fix You', artist: 'Coldplay', genre: 'Alternative', reason: 'Emotional and building.' } ],
      'late night': [ { id: 'v-d-5', title: 'Drive', artist: 'The Cars', genre: 'New Wave', reason: 'A nostalgic late night drive.' } ],
      'workout': [ { id: 'v-d-6', title: 'Gonna Fly Now', artist: 'Bill Conti', genre: 'Soundtrack', reason: 'Motivational instrumental.' } ],
      'romantic': [ { id: 'v-d-7', title: 'Make You Feel My Love', artist: 'Adele', genre: 'Pop', reason: 'Deeply romantic vocals.' } ],
      'relaxing': [ { id: 'v-d-8', title: 'Gymnopédie No.1', artist: 'Erik Satie', genre: 'Classical', reason: 'Gentle, relaxing piano.' } ]
    }
  },

  /**
   * Generates vibe-based recommendations, prioritizing the selected vibe and platform.
   */
  getVibeRecommendations({ platform, vibe, currentTrack }) {
    const pData = this.vibeDatabase[platform] || this.vibeDatabase['default'];
    const vibeKey = vibe.toLowerCase();
    
    // Use platform specific vibe if available, else fallback to default for that vibe
    return pData[vibeKey] || this.vibeDatabase['default'][vibeKey] || this.vibeDatabase['default']['chill'];
  }
};
