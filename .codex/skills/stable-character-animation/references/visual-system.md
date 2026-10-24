# Visual system

Ember (instagram.com/emberer00) is the style benchmark: pale field, faint scenery, strong
character outlines, selective colour, grounded props. Measured numbers are in
[benchmark evidence](benchmark-evidence.md); the rest below are working approximations.
When a number and the benchmark disagree, follow the benchmark and update the number.

## Composition and depth

- Default:1080x1920,24fps, full-bleed background and locked camera within a shot.
  Recompose at a deliberate cut; don't rescale the entire shot for each pose.
- Start with action safe area x=80..920,y=180..1600. Check the intended platform/player;
  this rectangle isn't a guarantee for every phone or screen.
- **Wide shots (Ember default):** characters small, about 12-20% of frame height (RK
  roughly 230-380 px tall at 1080x1920), placed in sparse scenery with room around
  them. Faces stay simple and readable at that size; the action reads by silhouette.
- **Medium shots** for dialogue and acting: RK around 40-48% of frame height, feet near
  y=1510..1570, full body visible.
- **Close inserts** land the payoff, a reaction or a key prop and may crop freely.
- Derive AI mascot sizes from the approved cast rather than each independent PNG.
  Keep the relative sizes of characters constant within a shot.
- **The style break:** the payoff may switch style for 0.5-3 s: a detailed painted
  close-up, a bold full-colour flat insert, a 3D-looking object, black-and-white impact
  frames, or a game/movie-parody title moment, then cut back to the line-art wide.
  Build these as their own shots; they never replace character identity.
- Avoid characters below a huge chat interface in every scene. Use compact essential
  text and let the physical prop carry the action when possible.

Build depth through a shared perspective, overlap and layer hierarchy:

1. Pale warm base field, such as #F3F1DF or #F5F2EA.
2. Far scenery: sparse desaturated silhouettes/lines. Start around15–30% of foreground
   contrast. A wall/window/skyline locates the scene without competing with faces.
3. Floor/support: faint edge, a few perspective lines or a flat pale plane. Simple
   soft oval contact shadows are enough; avoid changing realistic lighting.
4. Actors: readable dark contours and flat identifying costume colours.
5. Active object and foreground occluders: stronger contrast/colour when the prop matters.
6. Reaction marks/text: brief and local, away from faces and hands.

Adapt z-order to the actual interaction. A foreground desk may cover an arm only
when the relationship reads. Author layer splits or keep the interaction in one cel.

## Lines and colour

- Confident organic contours, fewer creases/stubble marks. Start around3–5px outer
  contour at1080p,1–2px internal detail and thinner paler scenery. Adjust for actor size.
- Flat fills, minimal texture/shading. Benchmark examples sometimes use sky gradients
  and effects; these are optional story choices.
- Preserve RK's red heart, Chad's teal-green, Claude's orange and Grok's black. Identity
  colours remain allowed alongside an active prop accent.
- Inactive scenery can be muted; an important object can gain saturation at its reveal.
  Motivate the change. Colour directs attention rather than decorating every object.

## Palette planning: flexible 60–30–10

Use Ember’s sparse color hierarchy: a dominant pale neutral field, faint environmental
line art for depth, clear character colors, and a small concentrated accent on the
story focus. Use 60–30–10 as a flexible palette-planning guide; preserve quiet space
rather than forcing exact proportions. Keep distant elements paler and lower in
contrast, and preserve approved character colors.

The conventional guide describes approximate visible color area: 60% dominant base,
30% secondary colors and 10% accent. These are not percentages of viewer attention,
and the saved Ember study does not establish that Ember uses this exact ratio.
Sparse wide shots may have much more than 60% neutral background. Do not enlarge
characters, add scenery or increase saturation merely to meet a quota.

- Plan the dominant base, supporting colors and story accent for each shot. Keep
  inactive scenery quiet; a key prop can carry the accent when the action needs it.
- Use minimal environmental lines, perspective, overlap and soft contact shadows
  to establish depth without competing with faces, hands or the active object.
- Keep the palette consistent within a shot. Motivate accent changes at reveals
  or deliberate cuts; brief impact frames and payoff style breaks may depart from it.
- Review opening, action and payoff frames at phone size. Check that the story focus
  reads clearly and that background details or unrelated bright objects do not compete.

## Props

Record owner/support, size, orientation and drawing before animation. Every prop is
held, resting, falling or visibly suspended for a specific reason. A mug is never
floating background decoration. Its bottom meets the tabletop in perspective.

Draw the hand around a phone edge; don't paste it over a closed mitten. Use a whole
pair drawing for difficult handoffs. Contact shadows support grounded objects.

Use original generic scenery/props. The benchmark's exact protagonist, distinctive
scenes, watermark, soundtrack and imported game assets aren't needed. Don't imply
endorsement or clone voices.
