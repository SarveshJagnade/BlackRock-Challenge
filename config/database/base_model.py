from datetime import datetime,timezone

from sqlalchemy import event
from sqlalchemy import Boolean, DateTime, Integer
from sqlalchemy.orm import Session, with_loader_criteria

from sqlalchemy.sql.dml import Delete
from sqlalchemy.sql import update, select

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import as_declarative

from sqlalchemy.orm import declared_attr, Mapped, mapped_column

# soft delete defination

def utc_now():
    return datetime.now(timezone.utc)

async def soft_delete(session: AsyncSession, stmt):
    if isinstance(stmt, Delete):
        model = stmt.table
        if hasattr(model.c, 'is_deleted'):
            soft_delete_stmt = update(model).where(stmt.whereclause).values(
                is_deleted=True, deleted_at=datetime.now(timezone.utc))
            return await session.execute(soft_delete_stmt)

    return await session.execute(stmt)


async def custom_execute(self, stmt, *args, **kwargs):
    if isinstance(stmt, Delete):
        return await soft_delete(self, stmt)
    return await self._original_execute(stmt, *args, **kwargs)

async def custom_get(self, model, ident, options=None):
    stmt = select(model).where(model.id == ident)
    if hasattr(model, "is_deleted"):
        stmt = stmt.where(model.is_deleted == False)
    result = await self.execute(stmt)
    return result.scalar_one_or_none()

# patching the functions
AsyncSession._original_execute = AsyncSession.execute
AsyncSession.execute = custom_execute

AsyncSession._original_get = AsyncSession.get
AsyncSession.get = custom_get

class SoftDeleteMixin:
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

@event.listens_for(Session, "do_orm_execute")
def _add_soft_delete_filter(execute_state):
    '''
        Note: To include deleted records use 
        ex: await session.execute(stmt.execution_options(include_deleted=True))
    '''
    if execute_state.is_select and not execute_state.execution_options.get("include_deleted", False):
        execute_state.statement = execute_state.statement.options(
            with_loader_criteria(
                SoftDeleteMixin,
                lambda cls: cls.is_deleted == False,
                include_aliases=True
            )
        )

@as_declarative()
class BaseModel(SoftDeleteMixin):
    _abstract_ = True

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, onupdate=utc_now)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    @declared_attr
    def _tablename_(cls) -> str:
        return cls._name_.lower()

mapped_metadata = {
    'investment_db': BaseModel.metadata
}