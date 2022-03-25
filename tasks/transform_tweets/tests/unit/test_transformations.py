from tests.conftest import transformations

# expected place candidate extraction output
# wrt the datapoints fixtures in tests.conftest
expected_place_candidates = [
    # datapoint_without_place
    {"candidates": None},
    # datapoint_with_gpe
    {"candidates": {"GPE": ["Rio de Janeiro", "Paris"]}},
    # datapoint_with_loc
    {"candidates": {"LOC": ["Roccacannuccia nella pianura pontina"]}},
]


def test_extract_place_candidates(allowed_tags):
    """Test if extract_place_candidates returns the correct places wrt the allowed tags for each texts."""
    deeppavlov_output_payload = [
        [
            ["a", "text", "in", "english", "without", "place", "candidates", "."],
            [
                "Un",
                "texte",
                "d",
                "`",
                "information",
                "sur",
                "Rio",
                "de",
                "Janeiro",
                ",",
                "écrit",
                "à",
                "Paris",
                ".",
            ],
            [
                "ed",
                "uno",
                "in",
                "italiano",
                "da",
                "Roccacannuccia",
                "nella",
                "pianura",
                "pontina",
            ],
        ],
        [
            ["O", "O", "O", "B-LANGUAGE", "O", "O", "O", "O"],
            [
                "O",
                "O",
                "O",
                "O",
                "O",
                "O",
                "B-GPE",
                "I-GPE",
                "I-GPE",
                "O",
                "O",
                "O",
                "B-GPE",
                "O",
            ],
            [
                "O",
                "B-CARDINAL",
                "O",
                "B-LANGUAGE",
                "O",
                "B-LOC",
                "I-LOC",
                "I-LOC",
                "I-LOC",
            ],
        ],
    ]
    place_candidates = transformations.extract_place_candidates(
        deeppavlov_output_payload, allowed_tags
    )
    assert place_candidates == expected_place_candidates


def test_extract_place_candidates_non_alpha_gpe(allowed_tags):
    """Test if extract_place_candidates removes non-alphanumeric tokens wrongly tagged by DeepPavlov."""
    deeppavlov_output_payload = [
        [["fake", "text", "with", "wrongly", "tagged", ")", "chars", "!", "?"]],
        [["O", "O", "O", "B-GPE", "I-GPE", "I-GPE", "I-GPE", "O", "B-LOC"]],
    ]
    place_candidates = transformations.extract_place_candidates(
        deeppavlov_output_payload, allowed_tags
    )
    assert place_candidates == [
        {"candidates": {"GPE": ["wrongly tagged chars"], "LOC": []}}
    ]


def test_normalize_places(
    datapoint_without_place, datapoint_with_gpe, datapoint_with_loc
):
    """Test if normalize_places returns the normalized texts i.e. _loc_ tag for each recognized place candidate."""

    texts = [
        datapoint_without_place["text"],
        datapoint_with_gpe["text"],
        datapoint_with_loc["text"],
    ]

    result = transformations.normalize_places(
        texts[1], expected_place_candidates[1]["candidates"]
    )
    assert result == "Un texte d`information sur _loc_, écrit à _loc_."


def test_apply_transformations():
    """Test if apply transformations return the input text transformed as expected."""
    text = "@Toroloco Nos nos \\ 'vemos' @ 12:12 a.m. or 1 pm or 12:05:06 or 13:33 en \"\" la SB Nick &amp; CIA... _loc_ #RunToMiami #SBLIV #100Yardas #Yarders #NFL 🏈🏈🏈 https://t.co/nVdULr6JXG,     badurl  https://...."
    result = transformations.apply_transformations(text)
    expected = "nos nos vemos   or or or en la sb nick and cia  runtomiami sbliv 100yardas yarders nfl  badurl   _urlincl_ _locincl_"
    assert result == expected
