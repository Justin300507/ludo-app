from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app.models.users import Users
from app.models.games import Game
from app.models.game_players import GamePlayer
from app.models.chat_messages import ChatMessage
from app.models.moves import Move
from app.utils.auth import get_password_hash
import random
import string

seed_router = APIRouter()

def _random_lobby_code() -> str:
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=6))

@seed_router.post("/seed", status_code=status.HTTP_201_CREATED)
def seed_database(db: Session = Depends(get_db)):
    # ---- Users ----
    user_data = [
        {"email": "alex.chen@example.com", "username": "alexc", "password": "Password123", "display_name": "Alex Chen"},
        {"email": "maria.garcia@example.com", "username": "mariag", "password": "Password123", "display_name": "Maria Garcia"},
        {"email": "james.kim@example.com", "username": "jamesk", "password": "Password123", "display_name": "James Kim"},
        {"email": "lina.park@example.com", "username": "linap", "password": "Password123", "display_name": "Lina Park"},
        {"email": "omar.nasir@example.com", "username": "omarn", "password": "Password123", "display_name": "Omar Nasir"},
    ]
    for u in user_data:
        existing = db.query(Users).filter(Users.email == u["email"]).first()
        if existing:
            continue
        hashed = get_password_hash(u["password"])  # type: ignore
        user = Users(
            email=u["email"],
            username=u["username"],
            password=hashed,
            display_name=u["display_name"],
        )
        db.add(user)
    db.commit()

    # ---- Games ----
    game_data = [
        {"title": "Space Adventure", "description": "Explore the galaxy", "is_private": False, "status": "waiting"},
        {"title": "Mystery Mansion", "description": "Solve the mystery", "is_private": True, "status": "in_progress"},
        {"title": "Battle Arena", "description": "Fight to the top", "is_private": False, "status": "waiting"},
        {"title": "Puzzle Quest", "description": "Puzzle challenges", "is_private": True, "status": "finished"},
        {"title": "Race Rush", "description": "High speed racing", "is_private": False, "status": "waiting"},
    ]
    created_games = []
    for g in game_data:
        # Ensure unique lobby_code
        while True:
            code = _random_lobby_code()
            if not db.query(Game).filter(Game.lobby_code == code).first():
                break
        game = Game(
            title=g["title"],
            description=g["description"],
            is_private=g["is_private"],
            lobby_code=code,
            status=g["status"],
        )
        db.add(game)
        db.flush()  # obtain id without committing
        created_games.append(game)
    db.commit()

    # ---- Game Players ----
    # Assign first three users to first three games, plus some guest players
    users = db.query(Users).all()
    for i, game in enumerate(created_games[:3]):
        player = GamePlayer(
            game_id=game.id,
            user_id=users[i].id,
            guest_name=None,
            order=i + 1,
            ready=True,
        )
        db.add(player)
    # Guest players for remaining games
    for i, game in enumerate(created_games[3:]):
        guest = GamePlayer(
            game_id=game.id,
            user_id=None,
            guest_name=f"Guest{i + 1}",
            order=1,
            ready=False,
        )
        db.add(guest)
    db.commit()

    # ---- Moves ----
    move_data = []
    for game in created_games:
        for player in db.query(GamePlayer).filter(GamePlayer.game_id == game.id).all():
            move = Move(
                game_id=game.id,
                player_id=player.id,
                move_type="start",
            )
            move_data.append(move)
    db.bulk_save_objects(move_data)
    db.commit()

    # ---- Chat Messages ----
    chat_messages = []
    sample_contents = [
        "Hello everyone!",
        "Good luck!",
        "Watch out for the trap.",
        "Nice move!",
        "Game over, well played!",
    ]
    for game in created_games:
        for idx, content in enumerate(sample_contents):
            msg = ChatMessage(
                game_id=game.id,
                sender_id=users[idx % len(users)].id,
                content=content,
            )
            chat_messages.append(msg)
    db.bulk_save_objects(chat_messages)
    db.commit()

    return {"detail": "Demo data seeded successfully"}
