from domain.entities.subject import Subject
from domain.value_objects.hex_color import HexColor
from infrastructure.database.models.subjects import SubjectModel


class SubjectMapper:
    @staticmethod
    def to_entity(row: SubjectModel) -> Subject:
        return Subject(
            subject_id=row.id,
            user_id=row.user_id,
            name=row.name,
            color=HexColor(row.color),
            created_at=row.created_at,
        )

    @staticmethod
    def to_model(subject: Subject) -> SubjectModel:
        return SubjectModel(
            id=subject.id,
            user_id=subject.user_id,
            name=subject.name,
            color=str(subject.color),
            created_at=subject.created_at,
        )
