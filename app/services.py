from database.models import User, Author, Papers
from database.connection import async_session
from sqlalchemy import delete, select, update
from schemas import AuthorCreateInput, AuthorUpdateInput, PaperCreateInput


class UserService:
    async def create_user(name: str):
        async with async_session() as session:
            session.add(User(name=name))
            await session.commit()

    async def delete_user(user_id: int):
        async with async_session() as session:
            await session.execute(delete(User).where(User.id == user_id))
            await session.commit()

    async def list_user():
        async with async_session() as session:
            result = await session.execute(select(User))
            return result.scalars().all()


class AuthorService:
    async def create_author(author_input: AuthorCreateInput):
        async with async_session() as session:
            session.add(Author(name=author_input.name, picture=author_input.picture))

            await session.commit()

    async def delete_author(author_id: int):
        async with async_session() as session:
            await session.execute(delete(User).where(User.id == author_id))
            await session.commit()

    async def list_author():
        async with async_session() as session:
            result = await session.execute(select(Author))
            return result.scalars().all()

    async def search_author(name: str):
        async with async_session() as session:
            result = await session.execute(select(Author).where(Author.name == name))
            return result.scalars().all()

    async def update_author(author_id: int, author_input: AuthorUpdateInput):
        async with async_session() as session:
            await session.execute(
                update(Author)
                .where(Author.id == author_id)
                .values(name=author_input.name, picture=author_input.picture)
            )

            session.commit()

        return


class PaperService:
    async def search_title(title: str):
        async with async_session() as session:
            result = await session.execute(select(Papers).where(Papers.title == title))
            return result.scalars().all()

    async def create_paper(paper_input: PaperCreateInput):
        async with async_session() as session:
            session.add(Papers(category=paper_input.category, title=paper_input.title, summary=paper_input.summary,
                               firstParagraph=paper_input.firstParagraph, body=paper_input.body))

            await session.commit()
