import json
from domain.entities.revision_cycle import RevisionCycle
from infrastructure.database.models.revision_cycle import RevisionCycleModel


class RevisionCycleMapper:
    @staticmethod
    def to_entity(row: RevisionCycleModel) -> RevisionCycle:
        return RevisionCycle(
            revision_cycle_id=row.id,
            user_id=row.user_id,
            name=row.name,
            days=row.days,
            created_at=row.created_at,
        )

    @staticmethod
    def to_model(revision_cycle: RevisionCycle) -> RevisionCycleModel:
        return RevisionCycleModel(
            id=revision_cycle.id,
            user_id=revision_cycle.user_id,
            name=revision_cycle.name,
            days=revision_cycle.days,
            created_at=revision_cycle.created_at,
        )
