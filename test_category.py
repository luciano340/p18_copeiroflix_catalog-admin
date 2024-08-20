import pytest
from uuid import UUID
import uuid
from category import Category

class TestCategory:
    def teste_name_is_required(self):
        with pytest.raises(TypeError):
            Category()

    def test_name_must_have_less_than_255_characters(self):
        with pytest.raises(ValueError, match="name must have less than 255 characteres"):
            Category(name="a" * 256)

    def test_id_must_by_uuid(self):
        c = Category(name="Filme")
        assert isinstance(c.id, UUID)
    
    def test_created_category_with_default_values(self):
        c = Category(name="Filme")
        assert c.name == "Filme"
        assert c.description == ""
        assert c.is_active is True

    def test_category_is_created_as_active_by_default(self):
        c = Category(name="Filme")
        assert c.is_active is True

    def test_category_is_created_with_provided_values(self):
        category_id = uuid.uuid4()
        c = Category(
            id=category_id,
            name="Filme",
            description="Muito legal",
            is_active=False
        )

        assert c.id == category_id
        assert c.name == "Filme"
        assert c.description == "Muito legal"
        assert c.is_active is False

    
    def test_str_must_return_custom(self):
        category_id = uuid.uuid4()
        c = Category(
            id=category_id,
            name="Filme",
            description="Muito legal",
            is_active=False
        )

        assert str(c) == f"str {category_id} - Filme - Muito legal - False"

    def test_repr_must_return_custom(self):
        category_id = uuid.uuid4()
        c = Category(
            id=category_id,
            name="Filme",
            description="Muito legal",
            is_active=False
        )

        assert repr(c) == f"repr {category_id} - Filme - Muito legal - False"
    
    def test_cannot_create_category_with_empty_name(self):
        with pytest.raises(ValueError, match="name cannot be empty"):
            c = Category(name="")

class TestUpdateCategory:
    def test_udpate_category_with_name_description(self):
        c = Category(name="Filme")

        c.update_category(name="Terror", description="Geral")

        assert c.name == "Terror"
        assert c.description == "Geral"
    
    def test_update_category_with_invalid_name(self):
        c = Category(name="Filme")

        with pytest.raises(ValueError):
            c.update_category(name="2"*352)

    def test_update_category_with_empty_name(self):
        with pytest.raises(ValueError, match="name cannot be empty"):
            c = Category(name="")
    
    def test_update_category_status_to_false(self):
        c = Category(name="Filme")

        c.deactivate()

        assert c.is_active is False

    def test_update_category_status_to_true(self):
        c = Category(name="Filme", is_active=False)

        c.activate()

        assert c.is_active is True

class TestEquality:
    def test_when_categories_have_same_id_they_are_equal(self):
        common_id = uuid.uuid4()
        c1 = Category(name="Filme", id=common_id)
        c2 = Category(name="Filme", id=common_id)

        assert c1 == c2
    
    def test_categories_different_classes(self):
        class Dummy:
            pass

        common_id = uuid.uuid4()
        c1 = Category(name="Filme", id=common_id)
        d = Dummy()
        d.id = common_id

        assert c1 != d