from __future__ import annotations

from planta.schemas import CropSummary, Disease, Treatment

MODEL_LABELS: tuple[str, ...] = (
    "Apple___Apple_scab",
    "Apple___Black_rot",
    "Apple___Cedar_apple_rust",
    "Apple___healthy",
    "Blueberry___healthy",
    "Cherry_(including_sour)___Powdery_mildew",
    "Cherry_(including_sour)___healthy",
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
    "Corn_(maize)___Common_rust_",
    "Corn_(maize)___Northern_Leaf_Blight",
    "Corn_(maize)___healthy",
    "Grape___Black_rot",
    "Grape___Esca_(Black_Measles)",
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
    "Grape___healthy",
    "Orange___Haunglongbing_(Citrus_greening)",
    "Peach___Bacterial_spot",
    "Peach___healthy",
    "Pepper,_bell___Bacterial_spot",
    "Pepper,_bell___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Raspberry___healthy",
    "Soybean___healthy",
    "Squash___Powdery_mildew",
    "Strawberry___Leaf_scorch",
    "Strawberry___healthy",
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites Two-spotted_spider_mite",
    "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___Tomato_mosaic_virus",
    "Tomato___healthy",
)


def _t(kind: str, title: str, details: str) -> Treatment:
    return Treatment(kind=kind, title=title, details=details)  # type: ignore[arg-type]


def _healthy(crop: str, label: str, extra: str) -> Disease:
    return Disease(
        id=label,
        crop=crop,
        name=f"Healthy {crop.lower()}",
        scientific_name=None,
        pathogen_type="healthy",
        severity="none",
        contagious=False,
        summary=extra,
        symptoms=[
            "Even green color without spots, rings, or powdery films",
            "Leaves hold their shape — no cupping, mosaic, or crisp scorch",
            "No sticky residue, webbing, or clusters of tiny moving dots",
        ],
        causes=[
            "Balanced light, water, and airflow",
            "Clean tools and resistant varieties when they are available",
        ],
        treatments=[
            _t("cultural", "Keep the rhythm", "Water at the soil line in the morning, feed according to the crop, and keep scouting weekly so new spots are caught early."),
            _t("organic", "Support, don't spray", "A healthy leaf does not need fungicide. Compost tea or a light kelp feed can help vigor if growth looks pale."),
        ],
        prevention=[
            "Rotate families year to year where you can",
            "Don't overhead-water in the evening",
            "Remove nearby wild hosts and rotting fruit",
        ],
        similar=[],
    )


DISEASES: dict[str, Disease] = {
    "Apple___Apple_scab": Disease(
        id="Apple___Apple_scab",
        crop="Apple",
        name="Apple scab",
        scientific_name="Venturia inaequalis",
        pathogen_type="fungal",
        severity="medium",
        contagious=True,
        summary="Olive-brown velvety spots that cork over and can defoliate the tree and russet the fruit. Worst in cool, wet spring weather.",
        symptoms=[
            "Olive to brown spots with a velvety surface on young leaves",
            "Spots later turn corky; leaves yellow and drop early",
            "Fruit shows dark, scabby lesions that crack as it grows",
        ],
        causes=[
            "Fungus overwinters in fallen leaves",
            "Spores splash up during prolonged spring leaf wetness",
        ],
        treatments=[
            _t("cultural", "Sanitation first", "Rake and destroy fallen leaves in autumn. Prune for an open canopy so leaves dry faster after rain."),
            _t("organic", "Sulfur or copper at green tip", "Apply according to label from green tip through petal fall in wet springs. Do not mix sulfur with oil or spray in high heat."),
            _t("chemical", "Protectant fungicide program", "Commercial orchards often rotate captan, myclobutanil, or similar scab materials on a weather-based schedule. Follow local labels."),
        ],
        prevention=[
            "Plant scab-resistant cultivars (Liberty, Enterprise, many modern cider apples)",
            "Avoid overhead irrigation",
            "Shred or remove leaf litter before bud break",
        ],
        similar=["Apple___Black_rot", "Apple___Cedar_apple_rust"],
    ),
    "Apple___Black_rot": Disease(
        id="Apple___Black_rot",
        crop="Apple",
        name="Black rot",
        scientific_name="Botryosphaeria obtusa",
        pathogen_type="fungal",
        severity="high",
        contagious=True,
        summary="Frog-eye leaf spots, cankers on branches, and fruit that mummifies into shiny black globes still hanging on the spur.",
        symptoms=[
            "Leaf spots with a purple border and tan center (frog-eye)",
            "Sunken reddish-brown cankers on twigs and scaffold limbs",
            "Fruit rots from the calyx, then turns black and shriveled",
        ],
        causes=[
            "Fungus survives in mummified fruit, dead wood, and cankers",
            "Warm, humid weather during bloom and fruit swell",
        ],
        treatments=[
            _t("cultural", "Cut out the reservoir", "Prune cankered wood 6–8 inches below the lesion. Pick mummies off the tree and off the ground."),
            _t("organic", "Copper at delayed dormant", "A dormant copper spray plus summer sanitation slows new infections. Keep the canopy open."),
            _t("chemical", "Cover sprays from bloom", "Captan and several strobilurins are labeled for black rot; rotate modes of action."),
        ],
        prevention=[
            "Remove fire blight strikes and any dead wood promptly",
            "Don't leave storage bins of rotten fruit near the orchard",
            "Avoid wounding trunks with mowers",
        ],
        similar=["Apple___Apple_scab"],
    ),
    "Apple___Cedar_apple_rust": Disease(
        id="Apple___Cedar_apple_rust",
        crop="Apple",
        name="Cedar-apple rust",
        scientific_name="Gymnosporangium juniperi-virginianae",
        pathogen_type="fungal",
        severity="medium",
        contagious=True,
        summary="A rust that needs both apple and eastern red cedar. Bright orange leaf spots on apple; gelatinous orange galls on cedar in spring rain.",
        symptoms=[
            "Yellow-orange spots on upper leaf surfaces, later with tiny tubes underneath",
            "Fruit may show similar orange lesions near the calyx",
            "Nearby junipers/cedars carry brown galls that 'bloom' orange after rain",
        ],
        causes=[
            "Spores blow from cedar galls to apple during spring rains",
            "A few hundred yards of cedar is enough for serious infection",
        ],
        treatments=[
            _t("cultural", "Break the two-host cycle", "Remove nearby volunteer eastern red cedars if local rules allow, or prune galls before spring rain."),
            _t("organic", "Sulfur during the infection window", "Protectant sulfur from tight cluster through first cover helps in light pressure years."),
            _t("chemical", "Sterol-inhibitor sprays", "Myclobutanil-type materials timed to cedar spore release are the orchard standard."),
        ],
        prevention=[
            "Choose rust-resistant apple varieties",
            "Don't plant apples against a cedar windbreak",
            "Watch spring forecasts and spray before long wet periods",
        ],
        similar=["Apple___Apple_scab"],
    ),
    "Apple___healthy": _healthy(
        "Apple",
        "Apple___healthy",
        "This leaf looks like a healthy apple leaf — keep airflow in the canopy and clean up fallen leaves so scab and rot stay rare.",
    ),
    "Blueberry___healthy": _healthy(
        "Blueberry",
        "Blueberry___healthy",
        "Healthy blueberry foliage is a good sign. Keep soil acidic (pH ~4.5–5.5), mulch with pine, and water evenly while fruit is sizing.",
    ),
    "Cherry_(including_sour)___Powdery_mildew": Disease(
        id="Cherry_(including_sour)___Powdery_mildew",
        crop="Cherry",
        name="Powdery mildew",
        scientific_name="Podosphaera clandestina",
        pathogen_type="fungal",
        severity="medium",
        contagious=True,
        summary="White felt on young cherry leaves and shoots. Leaves curl, look dusty, and shoot tips can stunt, especially in dense, humid canopies.",
        symptoms=[
            "White to gray powder on upper leaf surfaces and new shoots",
            "Leaves cup, twist, or look narrower than normal",
            "Severe cases russet fruit and stall terminal growth",
        ],
        causes=[
            "Dry leaf surfaces with high humidity — unlike most fungi, mildew hates free water but loves still, humid air",
            "Lush, shaded growth from heavy nitrogen",
        ],
        treatments=[
            _t("cultural", "Open the tree", "Thin interior shoots. Avoid late nitrogen that pushes succulent growth."),
            _t("organic", "Potassium bicarbonate or sulfur", "Spray at first white patches. Horticultural oil (summer rate) can knock down colonies — not in high heat."),
            _t("chemical", "Mildew-specific fungicides", "Rotate QoI, SDHI, or DMI materials labeled for cherry mildew; resistance is common if you repeat one group."),
        ],
        prevention=[
            "Prune for light through the canopy",
            "Don't overhead-water",
            "Start scouting at shuck split",
        ],
        similar=[],
    ),
    "Cherry_(including_sour)___healthy": _healthy(
        "Cherry",
        "Cherry_(including_sour)___healthy",
        "A clean cherry leaf. Watch new shoots in early summer — that's when powdery mildew usually appears.",
    ),
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": Disease(
        id="Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
        crop="Corn",
        name="Gray leaf spot",
        scientific_name="Cercospora zeae-maydis",
        pathogen_type="fungal",
        severity="high",
        contagious=True,
        summary="Rectangular gray-tan lesions that run between the veins. In humid, no-till fields it can blight whole leaves after tasseling.",
        symptoms=[
            "Long, rectangular lesions with straight sides following the veins",
            "Color tan to gray, sometimes with a yellow halo",
            "Lesions merge until large sections of leaf die",
        ],
        causes=[
            "Residue-borne fungus in corn-on-corn rotations",
            "Long dew periods and warm nights",
        ],
        treatments=[
            _t("cultural", "Rotation and residue", "Rotate away from corn for a year. If you no-till, a hybrid with strong GLS scores matters more than a rescue spray."),
            _t("chemical", "Tassel-time fungicide", "If lesions are climbing toward the ear leaf at VT–R1, a labeled foliar fungicide can protect yield. Scout first — spraying healthy corn rarely pays."),
        ],
        prevention=[
            "Choose hybrids rated resistant to gray leaf spot",
            "Avoid continuous corn in river-bottom humidity",
            "Don't overcrowd — tighter rows hold dew longer",
        ],
        similar=["Corn_(maize)___Northern_Leaf_Blight", "Corn_(maize)___Common_rust_"],
    ),
    "Corn_(maize)___Common_rust_": Disease(
        id="Corn_(maize)___Common_rust_",
        crop="Corn",
        name="Common rust",
        scientific_name="Puccinia sorghi",
        pathogen_type="fungal",
        severity="medium",
        contagious=True,
        summary="Cinnamon-brown pustules scattered on both leaf surfaces. Sweet corn in cool, humid summers is hit hardest; field corn often shrugs it off.",
        symptoms=[
            "Small oval cinnamon to brown pustules on upper and lower leaf surfaces",
            "Pustules rupture and leave a dusty rust spore mass",
            "Severe cases yellow the leaf and pull down sugar in sweet corn",
        ],
        causes=[
            "Spores blow in on weather systems from warmer regions",
            "Cool nights and frequent dew",
        ],
        treatments=[
            _t("cultural", "Plant on time", "Early planting often outruns the rust flight. Avoid excessive nitrogen that keeps leaves wet with lush tissue."),
            _t("organic", "Sulfur on sweet corn", "Home gardeners can use labeled sulfur at first pustules; wash produce as directed."),
            _t("chemical", "Foliar fungicide on sweet corn", "If rust is building before harvest on a susceptible sweet-corn hybrid, a labeled strobilurin or mix can protect ears."),
        ],
        prevention=[
            "Resistant sweet-corn hybrids",
            "Don't plant in deep shade where dew lingers",
            "Destroy volunteer corn",
        ],
        similar=["Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot"],
    ),
    "Corn_(maize)___Northern_Leaf_Blight": Disease(
        id="Corn_(maize)___Northern_Leaf_Blight",
        crop="Corn",
        name="Northern leaf blight",
        scientific_name="Exserohilum turcicum",
        pathogen_type="fungal",
        severity="high",
        contagious=True,
        summary="Large cigar-shaped gray-green lesions, often with a wavy margin. Can strip photosynthetic area from the ear leaf down in wet seasons.",
        symptoms=[
            "Long (1–6 inch) cigar or elliptical lesions, gray-green then tan",
            "Lesions may show dark zones of sporulation on the underside",
            "Starts on lower leaves and moves up in wet weather",
        ],
        causes=[
            "Infected corn residue",
            "Moderate temperatures and long leaf wetness",
        ],
        treatments=[
            _t("cultural", "Hybrid and rotation", "The cheapest control is a hybrid with Ht genes / high NCLB scores plus crop rotation."),
            _t("chemical", "Protect the ear leaf", "Treat if blight is on or approaching the ear leaf around tasseling. One well-timed spray beats two late ones."),
        ],
        prevention=[
            "Bury or shred residue where erosion allows",
            "Scout from V10 through blister",
            "Avoid highly susceptible hybrids in river bottoms",
        ],
        similar=["Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot"],
    ),
    "Corn_(maize)___healthy": _healthy(
        "Corn",
        "Corn_(maize)___healthy",
        "This maize leaf looks clean. After tasseling, keep watching the ear leaf — that's the one that pays the yield bill.",
    ),
    "Grape___Black_rot": Disease(
        id="Grape___Black_rot",
        crop="Grape",
        name="Black rot",
        scientific_name="Guignardia bidwellii",
        pathogen_type="fungal",
        severity="high",
        contagious=True,
        summary="The classic backyard grape killer. Tan leaf spots with black pycnidia, then berries that turn into hard black mummies.",
        symptoms=[
            "Circular tan leaf spots with a dark rim and tiny black dots",
            "Young shoots may show oval lesions",
            "Berries brown, then shrivel into black mummies that hang on the cluster",
        ],
        causes=[
            "Mummies and cane lesions leftover from last year",
            "Rain splash from bloom through bunch closure",
        ],
        treatments=[
            _t("cultural", "Pick every mummy", "Remove mummified berries, infected tendrils, and old cluster stems in winter. Keep the fruiting zone leaf-pulled for sun and spray coverage."),
            _t("organic", "Copper plus sanitation", "Copper and/or sulfur on a tight pre-bloom to post-bloom schedule, plus ruthless sanitation, can hold a backyard vine."),
            _t("chemical", "Protect from bloom to veraison", "Mancozeb, captan, strobilurins, or DMIs labeled for grapes — start before bloom if last year was bad."),
        ],
        prevention=[
            "Don't leave last year's clusters on the trellis",
            "Train to a system with good spray access",
            "Resistant hybrids (many American/French hybrids) if vinifera is too hard in your climate",
        ],
        similar=["Grape___Esca_(Black_Measles)", "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)"],
    ),
    "Grape___Esca_(Black_Measles)": Disease(
        id="Grape___Esca_(Black_Measles)",
        crop="Grape",
        name="Esca (black measles)",
        scientific_name="Phaeomoniella / Phaeoacremonium complex",
        pathogen_type="fungal",
        severity="high",
        contagious=True,
        summary="A wood-infecting complex. Leaves show tiger-stripe yellowing between the veins; berries speckle; vines can collapse ('apoplexy') in heat.",
        symptoms=[
            "Interveinal chlorosis and browning that looks striped or scorched (tiger stripes)",
            "Dark specks on berries ('measles')",
            "Cross-section of older wood may show dark spots or white rot",
        ],
        causes=[
            "Fungi enter pruning wounds and live in the vascular wood for years",
            "Stress (drought, overcropping) brings symptoms to the canopy",
        ],
        treatments=[
            _t("cultural", "Surgery and delayed pruning", "Cut back to healthy wood. Prune late in dry weather, and protect large cuts. Remove dead spurs; don't leave pruning piles next to the block."),
            _t("chemical", "Wound protection", "There is no reliable foliar cure. Focus on pruning-wound protectants and vine replacement when the cordon is hollowed out."),
        ],
        prevention=[
            "Avoid huge pruning cuts in wet weather",
            "Don't overcrop young vines",
            "Source clean nursery stock",
        ],
        similar=["Grape___Black_rot"],
    ),
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": Disease(
        id="Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
        crop="Grape",
        name="Isariopsis leaf blight",
        scientific_name="Pseudocercospora vitis",
        pathogen_type="fungal",
        severity="medium",
        contagious=True,
        summary="Angular dark leaf spots that can coalesce and defoliate vines late in the season, exposing fruit to sunburn and reducing next year's reserves.",
        symptoms=[
            "Angular reddish-brown to black spots, often vein-limited",
            "Spots merge into blighted patches",
            "Heavy defoliation from the bottom of the canopy up",
        ],
        causes=[
            "Warm, wet late summer",
            "Dense canopies and leftover infected leaves",
        ],
        treatments=[
            _t("cultural", "Canopy and cleanup", "Leaf-pull the fruit zone. Rake leaves after harvest in small plantings."),
            _t("organic", "Copper in the late season", "Labeled copper sprays help where this blight is chronic. Watch phytotoxicity on young tissue."),
            _t("chemical", "Broad-spectrum grape fungicides", "Programs aimed at black rot and downy often suppress leaf blight as a side benefit — keep coverage through veraison if spots are climbing."),
        ],
        prevention=[
            "Don't let vines become a hedge",
            "Space arms so sprays can reach inner leaves",
        ],
        similar=["Grape___Black_rot"],
    ),
    "Grape___healthy": _healthy(
        "Grape",
        "Grape___healthy",
        "Healthy grape foliage. After fruit set, keep the cluster zone open — sunlight and spray coverage prevent most fruit rots.",
    ),
    "Orange___Haunglongbing_(Citrus_greening)": Disease(
        id="Orange___Haunglongbing_(Citrus_greening)",
        crop="Orange",
        name="Huanglongbing (citrus greening)",
        scientific_name="Candidatus Liberibacter asiaticus",
        pathogen_type="bacterial",
        severity="critical",
        contagious=True,
        summary="The most serious citrus disease worldwide. An unculturable bacterium spread by Asian citrus psyllid. There is no backyard cure — focus on vector control and removal of infected trees.",
        symptoms=[
            "Asymmetric yellow mottling that does not match the veins (blotchy mottle)",
            "Leaves may be upright, small, and thickened",
            "Fruit stays green at the stylar end, is lopsided, bitter, and drops early",
        ],
        causes=[
            "Psyllids feeding on infected trees inject the bacterium",
            "Moving infected nursery stock or backyard trees",
        ],
        treatments=[
            _t("cultural", "Confirm, then remove", "Have a citrus specialist or extension lab confirm HLB. Infected trees remain a source for neighbors — removal is the responsible control."),
            _t("organic", "Psyllid suppression", "Horticultural oils and regular scouting for waxy psyllid nymphs on new flush. This slows spread; it does not cure a positive tree."),
            _t("chemical", "Follow regional HLB programs", "Commercial groves use systemic insecticides, nutritional programs, and regulated budwood. Home growers should follow their state's citrus quarantine rules."),
        ],
        prevention=[
            "Buy only certified disease-free citrus",
            "Never move citrus material out of quarantine zones",
            "Inspect new flush weekly for psyllids",
        ],
        similar=[],
    ),
    "Peach___Bacterial_spot": Disease(
        id="Peach___Bacterial_spot",
        crop="Peach",
        name="Bacterial spot",
        scientific_name="Xanthomonas arboricola pv. pruni",
        pathogen_type="bacterial",
        severity="high",
        contagious=True,
        summary="Angular leaf spots that fall out and leave a shot-hole look, plus raised or pitted fruit lesions. Brutal in warm, wind-driven rain on susceptible peaches.",
        symptoms=[
            "Small angular water-soaked leaf spots that turn purple-brown and drop out",
            "Leaves look tattered; severe cases cause early defoliation",
            "Fruit spots are brown, sunken or pitted, sometimes with gumming",
        ],
        causes=[
            "Bacteria overwinter in cankers and buds",
            "Splashing rain and wind, especially on light, sandy sites",
        ],
        treatments=[
            _t("cultural", "Resistant cultivars", "If bacterial spot is annual, replanting a resistant peach (many modern ones are rated) beats spraying."),
            _t("organic", "Dormant copper, then caution", "Copper at leaf drop and delayed dormant reduces inoculum. Summer copper easily russets fruit — use labeled low rates only."),
            _t("chemical", "Oxytetracycline where labeled", "Some regions allow antibiotic bloom/cover sprays. Resistance and residue rules apply — read the label and local guidance."),
        ],
        prevention=[
            "Avoid highly susceptible heirlooms in humid climates",
            "Don't work trees when they are wet",
            "Reduce wind with a break, not a solid wall that traps humidity",
        ],
        similar=[],
    ),
    "Peach___healthy": _healthy(
        "Peach",
        "Peach___healthy",
        "A healthy peach leaf. In humid climates, start watching for bacterial spot as soon as shoots are a few inches long.",
    ),
    "Pepper,_bell___Bacterial_spot": Disease(
        id="Pepper,_bell___Bacterial_spot",
        crop="Bell pepper",
        name="Bacterial spot",
        scientific_name="Xanthomonas spp.",
        pathogen_type="bacterial",
        severity="high",
        contagious=True,
        summary="Water-soaked leaf specks that brown and yellow the canopy. Fruit gets raised scabs. Spreads fast in warm rain and on wet hands.",
        symptoms=[
            "Tiny water-soaked spots on leaves that turn brown with yellow halos",
            "Leaves yellow and drop, leaving a turkey-neck stem of fruit",
            "Fruit lesions are corky, raised, and scab-like",
        ],
        causes=[
            "Infested seed or transplants",
            "Splashing irrigation and working plants when wet",
        ],
        treatments=[
            _t("cultural", "Pull the worst plants", "Remove severely infected plants. Switch to drip. Stake for airflow. Don't pick or prune after a rain."),
            _t("organic", "Copper + mancozeb alternatives", "Copper sprays slow but rarely stop an epidemic. Fixed copper plus a labeled coprecipitate or biopesticide (Bacillus) is the organic toolkit."),
            _t("chemical", "Copper programs on a short interval", "Begin at first spots and keep a 5–7 day interval in stormy weather. Rotate with any labeled SAR inducers."),
        ],
        prevention=[
            "Hot-water or bleach-treat seed; buy certified transplants",
            "Resistant pepper varieties (Bs2 and others)",
            "Rotate off solanaceous crops for 2+ years",
        ],
        similar=["Tomato___Bacterial_spot"],
    ),
    "Pepper,_bell___healthy": _healthy(
        "Bell pepper",
        "Pepper,_bell___healthy",
        "Healthy pepper foliage. Drip irrigation and keeping hands off wet leaves prevent most bacterial spot outbreaks.",
    ),
    "Potato___Early_blight": Disease(
        id="Potato___Early_blight",
        crop="Potato",
        name="Early blight",
        scientific_name="Alternaria solani",
        pathogen_type="fungal",
        severity="medium",
        contagious=True,
        summary="Target-board brown spots on older potato leaves. It usually starts after plants are stressed or beginning to senesce, then climbs the canopy.",
        symptoms=[
            "Brown lesions with concentric rings (bull's-eye) on older leaves",
            "Yellowing around spots; lower canopy dies first",
            "Tubers can show dark, sunken surface lesions in storage",
        ],
        causes=[
            "Spores on residue and volunteer potatoes",
            "Alternating wet/dry weather and nitrogen stress",
        ],
        treatments=[
            _t("cultural", "Keep plants growing", "Adequate nitrogen and even moisture reduce early blight. Hill well; don't wound tubers at harvest."),
            _t("organic", "Copper at first target spots", "Begin when lower leaves spot, not after the canopy is brown. Remove volunteer potatoes."),
            _t("chemical", "Protectant program", "Chlorothalonil, mancozeb, or SDHI mixes on a weather-based schedule from row closure in problem fields."),
        ],
        prevention=[
            "Certified seed tubers",
            "Rotate out of potato/tomato for 2 years",
            "Don't plant next to last year's potato ground",
        ],
        similar=["Potato___Late_blight", "Tomato___Early_blight"],
    ),
    "Potato___Late_blight": Disease(
        id="Potato___Late_blight",
        crop="Potato",
        name="Late blight",
        scientific_name="Phytophthora infestans",
        pathogen_type="oomycete",
        severity="critical",
        contagious=True,
        summary="The Irish famine pathogen. Water-soaked lesions, white fuzz on the underside in the morning, and tubers that rot into a coppery foul mess. Act the same day.",
        symptoms=[
            "Large water-soaked, rapidly expanding lesions, often at leaf tips or edges",
            "Pale halo; white downy sporulation on the underside in humid weather",
            "Stems blacken; tubers show reddish-brown granular rot under the skin",
        ],
        causes=[
            "Infected seed, cull piles, or volunteer plants",
            "Cool (60–70°F), wet, foggy stretches",
        ],
        treatments=[
            _t("cultural", "Kill the source", "Destroy cull piles. Rogue infected plants in bags, not on the compost. If the patch is gone, cut vines before harvest so tubers don't infect in the hill."),
            _t("organic", "Copper as a protectant only", "Copper must be on the leaf before infection. It will not rescue a canopy that is already greasy. In an outbreak, harvest early and sort tubers."),
            _t("chemical", "Late-blight specific materials", "Use products with activity on oomycetes (e.g. cyazofamid, oxathiapiprolin, fluopicolide — whatever is labeled locally). Report outbreaks to extension; this disease travels on the wind."),
        ],
        prevention=[
            "Certified, late-blight-tested seed",
            "No uncovered cull piles",
            "Resistant cultivars and DSS/forecast tools (Blitecast-style)",
        ],
        similar=["Potato___Early_blight", "Tomato___Late_blight"],
    ),
    "Potato___healthy": _healthy(
        "Potato",
        "Potato___healthy",
        "This potato leaf looks healthy. After row closure, scout twice a week in cool wet weather — late blight can jump overnight.",
    ),
    "Raspberry___healthy": _healthy(
        "Raspberry",
        "Raspberry___healthy",
        "Healthy raspberry foliage. Thin canes for airflow and keep the fruiting zone weeded to cut gray mold later.",
    ),
    "Soybean___healthy": _healthy(
        "Soybean",
        "Soybean___healthy",
        "A healthy soybean leaf. This model was trained mainly on clean soybean tissue — unusual spots may need a specialist, not just this scan.",
    ),
    "Squash___Powdery_mildew": Disease(
        id="Squash___Powdery_mildew",
        crop="Squash",
        name="Powdery mildew",
        scientific_name="Podosphaera xanthii",
        pathogen_type="fungal",
        severity="medium",
        contagious=True,
        summary="White talc on squash and pumpkin leaves that ages to tan. Plants senesce early, fruit sugars drop, and sunscald shows up on exposed squash.",
        symptoms=[
            "White powdery colonies on upper (and later lower) leaf surfaces",
            "Leaves yellow, crisp, and collapse from the oldest ones up",
            "Fruit may sunburn once the leaf umbrella is gone",
        ],
        causes=[
            "Dry days, humid nights, crowded vines",
            "Spores that blow in — you don't need infected residue to start it",
        ],
        treatments=[
            _t("cultural", "Give them air and a living cover", "Space plants. Pull a few leaves in the center. Don't water the canopy. A healthy plant with PM-resistant genes outlasts a spray-only approach."),
            _t("organic", "Bicarbonate, milk, or sulfur", "Potassium bicarbonate, dilute milk sprays, or sulfur at first specks. Sulfur burns cucurbits in heat above ~90°F — spray evening, skip hot spells."),
            _t("chemical", "Rotate mildew fungicides", "QoI resistance is widespread. Alternate modes of action and start preventively on susceptible zucchini."),
        ],
        prevention=[
            "PM-resistant zucchini, cucumber, and pumpkin varieties",
            "Morning sun on the leaves",
            "Don't plant a solid mat of vines",
        ],
        similar=["Cherry_(including_sour)___Powdery_mildew"],
    ),
    "Strawberry___Leaf_scorch": Disease(
        id="Strawberry___Leaf_scorch",
        crop="Strawberry",
        name="Leaf scorch",
        scientific_name="Diplocarpon earlianum",
        pathogen_type="fungal",
        severity="medium",
        contagious=True,
        summary="Purple spots that coalesce until the leaf looks scorched and the whole planting browns from the outside in. Yield drops the following spring.",
        symptoms=[
            "Irregular purple spots on upper leaf surfaces",
            "Spots merge; leaflets dry from the margins and look burned",
            "Petioles and runners can show purple lesions too",
        ],
        causes=[
            "Fungus in old infected leaves",
            "Long wet periods in crowded matted rows",
        ],
        treatments=[
            _t("cultural", "Renovate after harvest", "Mow the foliage, narrow the rows, and rake out old leaves. That's the single best control in June-bearing beds."),
            _t("organic", "Open the row + copper", "Keep rows narrow. Copper or labeled biofungicides during long wet spells in spring."),
            _t("chemical", "Pre-bloom fungicides", "Captan and several modern fungicides are labeled; time them to bloom and renovation, not after the bed is already brown."),
        ],
        prevention=[
            "Start with certified plants",
            "Don't let matted rows exceed ~18 inches",
            "Drip instead of sprinklers",
        ],
        similar=[],
    ),
    "Strawberry___healthy": _healthy(
        "Strawberry",
        "Strawberry___healthy",
        "Healthy strawberry leaves are glossy and flat. After harvest, renovate June-bearers so leaf spots don't carry into next year.",
    ),
    "Tomato___Bacterial_spot": Disease(
        id="Tomato___Bacterial_spot",
        crop="Tomato",
        name="Bacterial spot",
        scientific_name="Xanthomonas spp.",
        pathogen_type="bacterial",
        severity="high",
        contagious=True,
        summary="Greasy specks on tomato leaves and raised scabs on fruit. Spreads on water, stakes, and fingers. Very hard to stop once a humid storm train starts.",
        symptoms=[
            "Small water-soaked leaf spots that brown and may have yellow halos",
            "Spots on stems and pedicels; leaves drop from the bottom up",
            "Fruit shows slightly raised, scabby black spots",
        ],
        causes=[
            "Contaminated seed or transplants",
            "Splashing rain, overhead irrigation, wet pruning",
        ],
        treatments=[
            _t("cultural", "Dry leaves, clean tools", "Switch to drip. Stake/trellis. Disinfect pruners. Remove the worst plants rather than pruning through them."),
            _t("organic", "Copper as a suppressant", "Fixed copper on a short interval can slow new spots. It will not erase existing lesions. Actigard-type SAR products are used in some organic-adjacent programs where allowed."),
            _t("chemical", "Copper + EBDC where labeled", "Tank mixes of copper and mancozeb are a commercial standard. Watch pre-harvest intervals."),
        ],
        prevention=[
            "Hot-water treated seed; never save seed from spotted fruit",
            "Resistant varieties where available",
            "Keep tomatoes away from last year's pepper/tomato ground",
        ],
        similar=["Pepper,_bell___Bacterial_spot", "Tomato___Septoria_leaf_spot"],
    ),
    "Tomato___Early_blight": Disease(
        id="Tomato___Early_blight",
        crop="Tomato",
        name="Early blight",
        scientific_name="Alternaria solani",
        pathogen_type="fungal",
        severity="medium",
        contagious=True,
        summary="The bull's-eye leaf spot of garden tomatoes. Starts on the oldest leaves after fruit set and can strip a plant by August if you never mulch or prune.",
        symptoms=[
            "Brown spots with concentric rings on older leaves",
            "Yellow halo; a collar rot can girdle the stem near the soil line",
            "Fruit lesions (usually at the stem end) are leathery and dark",
        ],
        causes=[
            "Soil-splashed spores",
            "Crowding, overhead water, and plants that have been carrying a heavy fruit load",
        ],
        treatments=[
            _t("cultural", "Mulch and strip the bottom", "Mulch to stop soil splash. Remove leaves that touch the soil. Stake. Don't compost obviously blighted vines in a cold pile."),
            _t("organic", "Copper or Bacillus at first rings", "Begin when the first bull's-eyes appear on the lowest leaves, not when the plant is a brown stick."),
            _t("chemical", "Protectants from fruit set", "Chlorothalonil or copper on a 7–10 day interval in wet weather is usually enough for home gardens."),
        ],
        prevention=[
            "Determinate varieties still need staking and mulch",
            "Rotate; don't plant into last year's tomato bed",
            "Water the soil, not the foliage",
        ],
        similar=["Tomato___Septoria_leaf_spot", "Tomato___Target_Spot", "Potato___Early_blight"],
    ),
    "Tomato___Late_blight": Disease(
        id="Tomato___Late_blight",
        crop="Tomato",
        name="Late blight",
        scientific_name="Phytophthora infestans",
        pathogen_type="oomycete",
        severity="critical",
        contagious=True,
        summary="Greasy, fast-moving blight that can kill a tomato patch in days. White fuzz on the underside of lesions in the morning is the tell. Treat as an emergency.",
        symptoms=[
            "Large, water-soaked gray-green lesions that turn brown overnight",
            "White sporulation on the underside in humid weather",
            "Fruit develops large, firm brown blotches; the whole vine can collapse",
        ],
        causes=[
            "Spores from infected potatoes, cull piles, or neighboring gardens",
            "Cool, wet, overcast stretches",
        ],
        treatments=[
            _t("cultural", "Remove and bag", "Pull infected plants immediately, bag them, and trash them. Do not compost. Strip nearby foliage that looks greasy."),
            _t("organic", "Copper ahead of the storm", "Only protectant. Once lesions are greasy and spreading, copper will not save that tissue. Harvest any sound green fruit to ripen indoors."),
            _t("chemical", "Oomycete fungicides now", "Materials with specific late-blight activity, applied at the forecast, not after the patch is brown. Alert neighbors — spores travel miles."),
        ],
        prevention=[
            "Don't start tomatoes next to potatoes in a wet climate",
            "Destroy volunteer tomatoes",
            "Watch regional late-blight alerts during cool rainy weeks",
        ],
        similar=["Potato___Late_blight", "Tomato___Early_blight"],
    ),
    "Tomato___Leaf_Mold": Disease(
        id="Tomato___Leaf_Mold",
        crop="Tomato",
        name="Leaf mold",
        scientific_name="Passalora fulva",
        pathogen_type="fungal",
        severity="medium",
        contagious=True,
        summary="A greenhouse classic. Pale spots on the upper leaf, olive-green to gray velvety mold underneath. Rare in dry open gardens, rampant in still, humid high tunnels.",
        symptoms=[
            "Yellow or pale green spots on the upper leaf surface",
            "Olive, velvety mold on the corresponding underside",
            "Leaves brown and drop from the inside of the canopy",
        ],
        causes=[
            "Humidity above ~85% with poor airflow",
            "Spores that persist on greenhouse structures and debris",
        ],
        treatments=[
            _t("cultural", "Dry the air", "Vent, fan, and space plants. Strip lower leaves. Water in the morning. Drop night humidity if you can heat-vent."),
            _t("organic", "Sulfur or potassium bicarbonate", "Sulfur burners are used in some greenhouses (follow safety rules). Foliar bicarbonates at first pale spots."),
            _t("chemical", "Labeled greenhouse fungicides", "Several DMIs and SDHIs are labeled; resistance to some groups is documented — rotate."),
        ],
        prevention=[
            "Cf-resistant greenhouse varieties",
            "Don't let leaves stay wet overnight",
            "Sanitize strings, clips, and last year's debris",
        ],
        similar=["Tomato___Septoria_leaf_spot"],
    ),
    "Tomato___Septoria_leaf_spot": Disease(
        id="Tomato___Septoria_leaf_spot",
        crop="Tomato",
        name="Septoria leaf spot",
        scientific_name="Septoria lycopersici",
        pathogen_type="fungal",
        severity="medium",
        contagious=True,
        summary="Many small round spots with dark borders and tiny dots (pycnidia) in the center. It climbs from the bottom and can defoliate a plant without touching the fruit.",
        symptoms=[
            "Lots of small (2–5 mm) circular spots, gray centers, dark rims",
            "Black pinhead pycnidia in the spot centers — the diagnostic clue",
            "Bottom leaves yellow and drop; fruit usually clean",
        ],
        causes=[
            "Splashed soil and infected debris",
            "Warm rain after plants are established",
        ],
        treatments=[
            _t("cultural", "Mulch, prune, don't splash", "Heavy mulch. Remove spotted lower leaves and bag them. Stake. Water at the base."),
            _t("organic", "Copper on a short wet-weather interval", "Start at the first lower-leaf spots. Combine with aggressive leaf removal."),
            _t("chemical", "Chlorothalonil / captan-type protectants", "Home garden products with chlorothalonil work well if you keep the new growth covered."),
        ],
        prevention=[
            "Rotate off tomatoes for a year or two",
            "Don't compost diseased vines in a cold pile",
            "Give each plant real space — a jungle canopy is a Septoria factory",
        ],
        similar=["Tomato___Early_blight", "Tomato___Bacterial_spot"],
    ),
    "Tomato___Spider_mites Two-spotted_spider_mite": Disease(
        id="Tomato___Spider_mites Two-spotted_spider_mite",
        crop="Tomato",
        name="Two-spotted spider mites",
        scientific_name="Tetranychus urticae",
        pathogen_type="pest",
        severity="medium",
        contagious=True,
        summary="Not a pathogen — a tiny mite. Leaves look stippled, dusty, and bronzed; fine webbing shows up on the underside in hot, dry weather.",
        symptoms=[
            "Fine pale stippling on the upper leaf; bronze or gray cast later",
            "Tiny moving dots on the underside (a hand lens helps)",
            "Fine silk webbing in heavy infestations, especially at the shoot tips",
        ],
        causes=[
            "Hot, dusty, dry weather",
            "Dusty leaves and plants stressed by drought; broad-spectrum insecticides that kill mite predators",
        ],
        treatments=[
            _t("cultural", "Wash and water", "A firm spray of water on leaf undersides every couple of days knocks populations back. Keep plants from drought stress. Reduce dust on nearby paths."),
            _t("organic", "Soap, oil, or predators", "Insecticidal soap or horticultural oil on the undersides, evening application. Release Phytoseiulus persimilis in greenhouses. Avoid pyrethroids — they flare mites."),
            _t("chemical", "True miticides, not general insecticides", "If you must spray, use a product labeled for mites (bifenazate, spiromesifen, etc.) and cover the undersides. Rotate mite-specific modes of action."),
        ],
        prevention=[
            "Don't let plants wilt in heat waves",
            "Encourage beneficials — skip casual pyrethroid use",
            "Inspect new transplants, especially greenhouse ones, before they go out",
        ],
        similar=["Tomato___Target_Spot"],
    ),
    "Tomato___Target_Spot": Disease(
        id="Tomato___Target_Spot",
        crop="Tomato",
        name="Target spot",
        scientific_name="Corynespora cassiicola",
        pathogen_type="fungal",
        severity="medium",
        contagious=True,
        summary="A warm-climate tomato leaf and fruit spot with concentric rings, often more aggressive than early blight in the humid South and in tunnels.",
        symptoms=[
            "Brown lesions with distinct concentric rings on leaves and petioles",
            "Cracks or sunken brown spots on fruit",
            "Rapid blighting in hot, humid weather",
        ],
        causes=[
            "Spores on debris and volunteers",
            "Long periods of leaf wetness at high temperature",
        ],
        treatments=[
            _t("cultural", "Keep the canopy open", "Prune suckers, mulch, and avoid overhead irrigation. Remove blighted lower leaves."),
            _t("organic", "Copper plus sanitation", "Same cultural package as early blight; copper is only a partial brake."),
            _t("chemical", "Protectant + SDHI programs", "Commercial growers rotate strobilurin/SDHI mixes with chlorothalonil. Don't rely on one FRAC group."),
        ],
        prevention=[
            "Rotate; destroy volunteers",
            "Don't crowd determinate plants in a humid tunnel without fans",
        ],
        similar=["Tomato___Early_blight"],
    ),
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": Disease(
        id="Tomato___Tomato_Yellow_Leaf_Curl_Virus",
        crop="Tomato",
        name="Tomato yellow leaf curl virus",
        scientific_name="Tomato yellow leaf curl virus (Begomovirus)",
        pathogen_type="viral",
        severity="high",
        contagious=True,
        summary="A whitefly-spread virus. New leaves cup upward, turn yellow at the edges, and internodes stack. Plants look stunted and set little fruit. No spray cures a virus.",
        symptoms=[
            "Upward cupping and chlorosis of the youngest leaves",
            "Severe stunting; bushy appearance from short internodes",
            "Flowers drop; fruit set collapses on plants infected young",
        ],
        causes=[
            "Silverleaf whitefly (Bemisia tabaci) feeding",
            "Infected transplants moved from warmer regions",
        ],
        treatments=[
            _t("cultural", "Rogue and cover", "Pull infected plants. Use insect-proof netting or a living screen. Reflective mulch can reduce landings. Don't keep a 'hospital' plant in the corner."),
            _t("organic", "Whitefly management", "Oils, soaps, and predators (Encarsia, Amblyseius) reduce vectors. They will not make a curled plant uncurl."),
            _t("chemical", "Vector control, not a viricide", "Systemic insecticides are used commercially against whiteflies. There is no chemical that removes TYLCV from a plant."),
        ],
        prevention=[
            "TYLCV-resistant hybrids in regions where it is established",
            "Inspect transplants; quarantine new plants for a week",
            "Control weeds that host whiteflies around the garden",
        ],
        similar=["Tomato___Tomato_mosaic_virus"],
    ),
    "Tomato___Tomato_mosaic_virus": Disease(
        id="Tomato___Tomato_mosaic_virus",
        crop="Tomato",
        name="Tomato mosaic virus",
        scientific_name="Tomato mosaic virus (Tobamovirus)",
        pathogen_type="viral",
        severity="high",
        contagious=True,
        summary="A mechanically spread virus. Mottled, blistered leaves, ferny distortion, and uneven fruit ripening. It hitchhikes on hands, tools, and sometimes tobacco.",
        symptoms=[
            "Light and dark green mosaic; leaves may be puckered or fern-like",
            "Stunting; brown streaks internally on some strains",
            "Fruit with uneven color, bronzing, or necrotic spots",
        ],
        causes=[
            "Sap on hands, pruners, and trellis twine",
            "Infected seed; smoking/handling tobacco then touching plants",
        ],
        treatments=[
            _t("cultural", "Stop the chain", "Rogue symptomatic plants. Wash hands, dip tools in 10% bleach or a labeled disinfectant between plants. Don't compost the vines."),
            _t("organic", "Milk dip for tools", "A milk dip for hands/tools is an old greenhouse trick that can reduce tobamovirus spread. Still rogue the obviously mosaic plants."),
            _t("chemical", "None", "No pesticide cures mosaic. Replace the planting with resistant (Tm-2²) varieties next round."),
        ],
        prevention=[
            "Resistant varieties",
            "Don't smoke in the tomato house; wash after handling tobacco",
            "Buy seed from reputable sources; don't save seed from mosaic plants",
        ],
        similar=["Tomato___Tomato_Yellow_Leaf_Curl_Virus"],
    ),
    "Tomato___healthy": _healthy(
        "Tomato",
        "Tomato___healthy",
        "This tomato leaf looks healthy. Keep mulching, watering at the soil line, and scouting the lowest leaves — that's where early blight and Septoria start.",
    ),
}


def get_disease(label: str) -> Disease | None:
    return DISEASES.get(label)


def all_diseases() -> list[Disease]:
    return [DISEASES[label] for label in MODEL_LABELS]


def crops() -> list[CropSummary]:
    grouped: dict[str, list[Disease]] = {}
    for disease in all_diseases():
        grouped.setdefault(disease.crop, []).append(disease)
    summaries: list[CropSummary] = []
    for name in sorted(grouped):
        entries = grouped[name]
        ailments = [d.name for d in entries if d.pathogen_type != "healthy"]
        summaries.append(
            CropSummary(name=name, disease_count=len(ailments), ailments=ailments)
        )
    return summaries


def display_name(label: str) -> tuple[str, str]:
    disease = DISEASES.get(label)
    if disease:
        return disease.crop, disease.name
    if "___" in label:
        crop, name = label.split("___", 1)
        crop = crop.replace("_(maize)", "").replace("_(including_sour)", "")
        crop = crop.replace("Pepper,_bell", "Bell pepper").replace("_", " ")
        name = name.replace("_", " ").strip()
        return crop.strip(), name.strip()
    return "Unknown", label
