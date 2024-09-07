from tkinter import N
from uuid import UUID
from freezegun import freeze_time
import pytest
from src.core.cast_member.domain.cast_member import CastMember


class TestCastMember:
    def test_name_is_required(self):
        with pytest.raises(ValueError, match="name cannot be empty"):
            cast_member = CastMember(
                type="CONVIDADO"
            )
    
    def test_type_is_required(self):
        with pytest.raises(ValueError):
            cast_member = CastMember(
                name="Luciano"
            )

    def test_type_cannot_accept_random_values(self):
        with pytest.raises(ValueError):
            cast_member = CastMember(
                name="Luciano",
                type="Teste"
            )
    
    def test_id_must_be_uuid(self):
        cast_member = CastMember(
            name="Luciano",
            type="APRESENTADOR"
        )

        assert isinstance(cast_member.id, UUID)
    
    def test_type_convidado_and_apresentador_must_be_accept(self):
        cast_member1 = CastMember(
            name="Luciano",
            type="APRESENTADOR"
        )

        cast_member2 = CastMember(
            name="Luciano",
            type="CONVIDADO"
        )

        assert cast_member1.type == "APRESENTADOR"
        assert cast_member2.type == "CONVIDADO"
        
    def test_created_date_must_be_set_and_update_date_must_be_none(self):
        with freeze_time("2024-09-07 10:10:10"):
            cast_member = CastMember(
                name="Luciano",
                type="APRESENTADOR"
            )
        
        assert cast_member.created_date == "2024-09-07 10:10:10"
        assert cast_member.updated_date is None
    
    def test_update_cast_member(self):
        cast_member1 = CastMember(
            name="Luciano",
            type="CONVIDADO"
        )

        with freeze_time("2024-09-09 20:20:20"):
            cast_member1.update_cast_member(name="Atualizado", type="APRESENTADOR")

        assert cast_member1.name == "Atualizado"
        assert cast_member1.type == "APRESENTADOR"
        assert cast_member1.updated_date == "2024-09-09 20:20:20"

        