# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**Vibefound 1.0**

---

## 2. Intended Use

Vibefound is designed to suggest songs from a small local catalog based on a
user's stated taste preferences. It is built for **classroom exploration** of
how content-based recommendation systems work — not for production use.

- It generates ranked song recommendations with plain-language explanations
  for why each song was suggested.
- It assumes the user can describe their preferences explicitly: favorite genre,
  favorite mood, target energy level, and whether they prefer acoustic or
  electronic music.
- It is intended for students and educators exploring how simple weighted
  algorithms can approximate musical taste, and how small design decisions
  (like weight values) shape what gets recommended.

---

## 3. How the Model Works

Think of Vibefound like a judge scoring contestants in a competition. Every
song in the catalog gets rated against the user's stated preferences, and the
songs with the highest scores win a recommendation spot.

The scoring works like this:

- **Genre match** is worth the most points (+2.0 for an exact match, +1.0 for a
  musically similar genre like "indie pop" for a pop fan). Genre is treated as
  the strongest signal of compatibility.
- **Mood match** is the second-most important factor (+1.5 for an exact match,
  +0.75 for a nearby mood like "chill" for someone who wants "calm" music).
- **Energy proximity** rewards songs whose energy level is close to what the
  user wants.
- **Valence proximity** rewards songs that match the user's emotional tone.
- **Acoustic preference** gives a small bonus (+0.5) for matching whether the
  user prefers acoustic or electronic sounds.

The final score for each song is the sum of all these points. Songs are then
sorted from highest to lowest, and the top 5 are returned with a list of reasons
explaining exactly which rules they matched.

I extended the starter logic by adding mood neighbors, valence proximity, and
acoustic preference so the system considers more than just genre and energy.

---

## 4. Data

- The catalog contains about **15 songs** stored in a CSV file.
- Genres represented include pop, lofi, rock, electronic, and indie pop.
- Moods represented include happy, chill, energetic, angry, and calm.
- I added songs beyond the original starter data to make the catalog more
  diverse.
- Some parts of musical taste are still missing. For example, there are no songs
  clearly labeled sad, romantic, jazz, classical, hip-hop, or bossa nova. That
  means users with those tastes may get weak or mismatched recommendations.

---

## 5. Strengths

- The system works well for clear, common profiles. For example, a happy
  high-energy pop user gets **Sunrise City** at the top, which feels correct.
- The Chill Lofi profile also worked well. Songs like **Library Rain** and
  **Midnight Coding** rose to the top because they matched low energy, calm mood,
  and acoustic preference.
- The explanations are a strength because the user can see exactly why each song
  was recommended.
- Genre neighbor logic helps the system feel a little less rigid, since similar
  genres can still score points.

---

## 6. Limitations and Bias

One major weakness is that the system **over-prioritizes genre**. Genre exact
match is worth +2.0, which is the biggest weight in the whole system. During
testing, a user with a **sad pop** profile still got **Gym Hero** as the top
result even though it is more of a hype/workout song than a sad one. This
happened because the genre match outweighed the missing mood match, so the
system focused more on category than emotional fit.

Other limitations:
- The dataset is small, so the same songs show up often across different
  profiles.
- If a user prefers a genre not in the catalog, the system cannot respond well.
- The model only uses a few handcrafted features and ignores things like lyrics,
  artist similarity, listening history, skips, and playlists.

---

## 7. Evaluation

I tested the recommender with five profiles:

- **High-Energy Pop** — pop, happy, energy 0.9
- **Chill Lofi** — lofi, calm, energy 0.3
- **Deep Intense Rock** — rock, angry, energy 0.95
- **Conflicting Profile** — pop, sad, energy 0.9
- **Unknown Genre** — bossa nova, romantic, energy 0.5

I looked at whether the top 5 results matched intuition and whether the same
songs kept appearing across profiles.

The standard profiles behaved well:
- High-Energy Pop gave upbeat pop songs like **Sunrise City**
- Chill Lofi gave softer lofi songs like **Library Rain**
- Deep Intense Rock gave **Storm Runner**, which made sense

The most surprising result came from the **Conflicting Profile**. Even though
the user wanted sad music, **Gym Hero** ranked first because genre and energy
still carried more weight than emotional mismatch.

I also ran a weight-shift experiment where I halved genre weight and doubled
energy weight. This changed the rankings noticeably, showing that the system is
very sensitive to the chosen weights.

---

## 8. Future Work

- Add more songs across more genres and moods so the system has better coverage
- Add more features such as danceability, tempo emphasis, or lyric sentiment
- Create multiple scoring modes like genre-first, mood-first, or energy-first
- Add a diversity rule so the top 5 are not all from the same genre or artist
- Improve explanations so they sound more natural and less formulaic

---

## 9. Personal Reflection

This project helped me understand that recommendation systems are really about
turning preferences into numbers and then making tradeoffs. I learned that even
a simple weighted scoring system can feel surprisingly realistic when the
features line up with human intuition. At the same time, I saw how easy it is
for bias to appear when one feature, like genre, is given too much importance.

What surprised me most was that a small change in weights could completely
change the ranking order. That made me think differently about apps like Spotify
or TikTok — their recommendations are not just “smart,” they are also shaped by
the assumptions and priorities built into the system.