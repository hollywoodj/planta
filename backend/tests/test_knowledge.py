from planta.knowledge import MODEL_LABELS, DISEASES, all_diseases, crops, get_disease


def test_every_model_label_has_knowledge():
    missing = [label for label in MODEL_LABELS if label not in DISEASES]
    extra = [label for label in DISEASES if label not in MODEL_LABELS]
    assert missing == []
    assert extra == []
    assert len(MODEL_LABELS) == 38
    assert len(all_diseases()) == 38


def test_required_fields_are_populated():
    for disease in all_diseases():
        assert disease.name
        assert disease.crop
        assert disease.summary
        assert disease.symptoms
        assert disease.treatments
        assert disease.prevention
        assert disease.pathogen_type in {
            "fungal",
            "bacterial",
            "viral",
            "oomycete",
            "pest",
            "healthy",
        }
        if disease.pathogen_type == "healthy":
            assert disease.severity == "none"
            assert disease.contagious is False
        else:
            assert disease.severity in {"low", "medium", "high", "critical"}
            assert disease.scientific_name


def test_lookup_unknown_is_none():
    assert get_disease("not-a-real-label") is None


def test_similar_ids_resolve():
    for disease in all_diseases():
        for related in disease.similar:
            assert related in DISEASES, f"{disease.id} points at missing {related}"


def test_crops_count_ailments_not_healthy():
    tomato = next(crop for crop in crops() if crop.name == "Tomato")
    assert tomato.disease_count == 9
    assert "Healthy tomato" not in tomato.ailments
    assert "Late blight" in tomato.ailments
