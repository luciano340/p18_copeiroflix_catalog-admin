import pytest
from uuid import UUID
import uuid
from src.core.genre.domain.genre import Genre
from freezegun import freeze_time

class TestGenre:
    def teste_name_is_required(self):
        with pytest.raises(TypeError):
            Genre()

    def test_name_must_have_less_than_255_characters(self):
        with pytest.raises(ValueError, match="name must have less than 255 characteres"):
            Genre(name="a" * 256)

    def test_id_must_by_uuid(self):
        c = Genre(name="Filme")
        assert isinstance(c.id, UUID)
    
    def test_created_genre_with_default_values(self):
        c = Genre(name="Filme")
        assert c.name == "Filme"
        assert c.is_active is True

    def test_genre_is_created_as_active_by_default(self):
        c = Genre(name="Filme")
        assert c.is_active is True

    def test_genre_is_created_with_provided_values(self):

        with freeze_time("2024-09-01 08:08:08"):
            genre_id = uuid.uuid4()
            c = Genre(
                id=genre_id,
                name="Filme",
                is_active=False
            )

        assert c.id == genre_id
        assert c.name == "Filme"
        assert c.is_active is False
        assert c.created_date == "2024-09-01 08:08:08"

    def test_cannot_create_genre_with_empty_name(self):
        with pytest.raises(ValueError, match="name cannot be empty"):
            c = Genre(name="")

class TestUpdategenre:
    def test_add_invalid_category_id(self):
        c = Genre(name="Filme")

        with pytest.raises(ValueError, match="Not a valid UUID"):
            c.add_caterogy(category_id="sdasad")

    
    def test_add_category(self):
        c = Genre(name="Filme")

        c.add_caterogy(category_id=uuid.uuid4)

        assert len(c.categories) == 1

    def test_update_genre_with_empty_name(self):
        c = Genre(name="Terror")

        with pytest.raises(ValueError, match="name cannot be empty"):
            c.change_name(name="")
    
    def test_update_genre_status_to_false(self):
        c = Genre(name="Filme")

        c.deactivate()

        assert c.is_active is False

    def test_update_genre_status_to_true(self):
        c = Genre(name="Filme", is_active=False)

        c.activate()

        assert c.is_active is True

class TestEquality:
    def test_when_categories_have_same_id_they_are_equal(self):
        common_id = uuid.uuid4()
        c1 = Genre(name="Filme", id=common_id)
        c2 = Genre(name="Filme", id=common_id)

        assert c1 == c2
    
    def test_categories_different_classes(self):
        class Dummy:
            pass

        common_id = uuid.uuid4()
        c1 = Genre(name="Filme", id=common_id)
        d = Dummy()
        d.id = common_id

        assert c1 != d