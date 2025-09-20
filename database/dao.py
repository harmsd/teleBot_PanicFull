from bot import logger
from .base import connection
from .models import User, Panic
from sqlalchemy import select
from typing import List, Dict, Any, Optional
from sqlalchemy.exc import SQLAlchemyError

@connection
async def set_user(session, tg_id: int, username: str, full_name: str) -> Optional[User]:
    try:
        user = await session.scalar(select(User).filter_by(id=tg_id))

        if not user:
            new_user = User(id=tg_id, username=username, full_name=full_name)
            session.add(new_user)
            await session.commit()
            logger.info(f"Зарегистрировал пользователя с ID {tg_id}!")
            return None
        else:
            logger.info(f"Пользователь с ID {tg_id} найден!")
            return user
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при добавлении пользователя: {e}")
        await session.rollback()

@connection
async def add_panic(session, user_id: int, name: Optional[str] = None, panic_string: Optional[str]= None, description: Optional[str] = None,
                    comment: Optional[str] = None) -> Optional[Panic]:
    try:
        user = await session.scalar(select(User).filter_by(id=user_id))
        if not user:
            logger.error(f"Пользователь с ID {user_id} не найден.")
            return None
        new_panic = Panic(
            user_id=user_id,
            name=name,
            panic_string=panic_string,
            description=description,
            comment=comment
        )
        session.add(new_panic)
        await session.commit()
        logger.info(f"Panic для пользователя с ID {user_id} успешно добавлен!")
        return new_panic
    
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при добавлении panic: {e}")
        await session.rollback()

@connection
async def update_name_panic(session, panic_id: int, name: Optional[str] = None) -> Optional[Panic]:
    try:
        panic = await session.scalar(select(Panic).filter_by(id=panic_id))
        if not panic:
            logger.error(f"Panic с ID {panic_id} не найден.")
            return None

        panic.name = name
        await session.commit()
        logger.info(f"Panic с ID {panic_id} успешно обновлен!")
        return panic
    
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при обновлении Panic: {e}")
        await session.rollback()

@connection
async def update_panicString_panic(session, panic_id: int, panic_string: Optional[str] = None) -> Optional[Panic]:
    try:
        panic = await session.scalar(select(Panic).filter_by(id=panic_id))
        if not panic:
            logger.error(f"Panic с ID {panic_id} не найден.")
            return None

        panic.panic_string = panic_string
        await session.commit()
        logger.info(f"Panic с ID {panic_id} успешно обновлен!")
        return panic
    
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при обновлении Panic: {e}")
        await session.rollback()

@connection
async def update_description_panic(session, panic_id: int, description: Optional[str] = None) -> Optional[Panic]:
    try:
        panic = await session.scalar(select(Panic).filter_by(id=panic_id))
        if not panic:
            logger.error(f"Panic с ID {panic_id} не найден.")
            return None

        panic.desription = description
        await session.commit()
        logger.info(f"Panic с ID {panic_id} успешно обновлен!")
        return panic
    
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при обновлении Panic: {e}")
        await session.rollback()

@connection
async def update_comment_panic(session, panic_id: int, comment: Optional[str] = None) -> Optional[Panic]:
    try:
        panic = await session.scalar(select(Panic).filter_by(id=panic_id))
        if not panic:
            logger.error(f"Panic с ID {panic_id} не найден.")
            return None

        panic.comment = comment
        await session.commit()
        logger.info(f"Panic с ID {panic_id} успешно обновлен!")
        return panic
    
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при обновлении Panic: {e}")
        await session.rollback()

@connection
async def get_panic_by_id(session, panic_id: int) -> Optional[Dict[str, Any]]:
    try:
        panic = await session.get(Panic, panic_id)
        if not panic:
            logger.info(f"Заметка с ID {panic_id} не найдена.")
            return None

        return {
            'id': panic.id,
            'name': panic.name,
            'panic_string': panic.panic_string,
            'description': panic.description,
            'comment': panic.comment
        }
    
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при получении заметки: {e}")
        return None
    
@connection
async def delete_panic_by_id(session, panic_id: int) -> Optional[Panic]:
    try:
        panic = await session.get(Panic, panic_id)
        if not panic:
            logger.error(f"Panic с ID {panic_id} не найдена.")
            return None

        await session.delete(panic)
        await session.commit()
        logger.info(f"Заметка с ID {panic_id} успешно удален.")
        return panic
    
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при удалении panic: {e}")
        await session.rollback()
        return None
    
@connection
async def get_all_panics(session, user_id: int, name: Optional[str] = None, panic_string: Optional[str] = None, 
                            description: Optional[str] = None, comment: Optional[str] = None) -> List[Dict[str, Any]]:
    try:
        result = await session.execute(select(Panic))
        panics = result.scalars().all()

        if not panics:
            logger.info(f"Panics для пользователя с ID {user_id} не найдены.")
            return []

        panic_list = [
            {
                'id': panic.id,
                'name': panic.name,
                'panic_string': panic.panic_string,
                'description': panic.description,
                'comment': panic.comment
            } for panic in panics
        ]

        return panic_list
    
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при получении заметок: {e}")
        return []